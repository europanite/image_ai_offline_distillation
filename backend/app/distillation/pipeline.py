from __future__ import annotations

import json
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Any

from distillation.settings import SUPPORTED_DATASETS, SUPPORTED_TEACHERS, artifact_dir


@dataclass(frozen=True)
class CacheMetadata:
    teacher: str
    dataset: str
    samples: int
    batch_size: int
    logits_path: str


def _device(requested: str):
    import torch

    if requested == "cuda" and not torch.cuda.is_available():
        raise RuntimeError("CUDA was requested, but torch.cuda.is_available() is False.")
    return torch.device(requested)


def _paths() -> dict[str, Path]:
    root = artifact_dir()
    return {
        "root": root,
        "teacher_logits": root / "teacher_logits_train.pt",
        "metadata": root / "teacher_cache_metadata.json",
        "student": root / "student_model.pt",
        "report": root / "report.json",
    }


def get_config() -> dict[str, Any]:
    paths = _paths()
    return {
        "supported_teachers": SUPPORTED_TEACHERS,
        "supported_datasets": SUPPORTED_DATASETS,
        "artifact_dir": str(paths["root"]),
        "has_teacher_cache": paths["teacher_logits"].exists(),
        "has_student_model": paths["student"].exists(),
        "has_report": paths["report"].exists(),
        "recommended_first_run": {
            "teacher": "resnet18",
            "dataset": "fake",
            "samples": 128,
            "batch_size": 16,
            "epochs": 2,
            "temperature": 3.0,
        },
    }


def cache_teacher_logits(
    teacher: str = "resnet18",
    dataset: str = "fake",
    samples: int = 128,
    batch_size: int = 16,
    device: str = "cpu",
) -> dict[str, Any]:
    import torch
    from torch.utils.data import DataLoader

    from distillation.data import build_dataset
    from distillation.models import build_teacher, count_parameters

    paths = _paths()
    runtime_device = _device(device)
    ds, effective_samples = build_dataset(dataset, samples=samples)
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False, num_workers=0)

    model = build_teacher(teacher).to(runtime_device)
    logits_chunks: list[torch.Tensor] = []

    with torch.inference_mode():
        for images, _targets in loader:
            images = images.to(runtime_device)
            logits = model(images).detach().cpu().to(torch.float16)
            logits_chunks.append(logits)

    teacher_logits = torch.cat(logits_chunks, dim=0)
    torch.save(teacher_logits, paths["teacher_logits"])

    metadata = CacheMetadata(
        teacher=teacher,
        dataset=dataset,
        samples=effective_samples,
        batch_size=batch_size,
        logits_path=str(paths["teacher_logits"]),
    )
    paths["metadata"].write_text(json.dumps(asdict(metadata), indent=2), encoding="utf-8")

    return {
        "teacher": teacher,
        "dataset": dataset,
        "samples": effective_samples,
        "teacher_parameters": count_parameters(model),
        "logits_shape": list(teacher_logits.shape),
        "logits_path": str(paths["teacher_logits"]),
        "metadata_path": str(paths["metadata"]),
    }


def _load_metadata() -> CacheMetadata:
    paths = _paths()
    if not paths["metadata"].exists() or not paths["teacher_logits"].exists():
        raise FileNotFoundError("Teacher cache is missing. Run cache-teacher first.")
    data = json.loads(paths["metadata"].read_text(encoding="utf-8"))
    return CacheMetadata(**data)


def train_student(
    epochs: int = 2,
    batch_size: int = 16,
    learning_rate: float = 1e-3,
    temperature: float = 3.0,
    device: str = "cpu",
) -> dict[str, Any]:
    import torch
    import torch.nn.functional as F
    from torch.utils.data import DataLoader, TensorDataset

    from distillation.data import build_dataset
    from distillation.models import build_student, count_parameters

    paths = _paths()
    metadata = _load_metadata()
    runtime_device = _device(device)

    ds, effective_samples = build_dataset(metadata.dataset, samples=metadata.samples)
    loader = DataLoader(ds, batch_size=batch_size, shuffle=False, num_workers=0)

    teacher_logits = torch.load(paths["teacher_logits"], map_location="cpu").to(torch.float32)
    if teacher_logits.shape[0] != effective_samples:
        raise RuntimeError(
            "Dataset sample count and cached teacher logits count do not match: "
            f"{effective_samples} != {teacher_logits.shape[0]}"
        )

    # Materialize image tensors once so shuffled student training can align images and cached logits.
    images: list[torch.Tensor] = []
    for batch_images, _targets in loader:
        images.append(batch_images)
    image_tensor = torch.cat(images, dim=0)
    train_ds = TensorDataset(image_tensor, teacher_logits)
    train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, num_workers=0)

    student = build_student(num_classes=teacher_logits.shape[1]).to(runtime_device)
    optimizer = torch.optim.AdamW(student.parameters(), lr=learning_rate)

    history: list[dict[str, float]] = []
    for epoch in range(1, epochs + 1):
        student.train()
        total_loss = 0.0
        total_items = 0
        for batch_images, batch_teacher_logits in train_loader:
            batch_images = batch_images.to(runtime_device)
            batch_teacher_logits = batch_teacher_logits.to(runtime_device)
            optimizer.zero_grad(set_to_none=True)
            student_logits = student(batch_images)
            loss = F.kl_div(
                F.log_softmax(student_logits / temperature, dim=1),
                F.softmax(batch_teacher_logits / temperature, dim=1),
                reduction="batchmean",
            ) * (temperature**2)
            loss.backward()
            optimizer.step()
            total_loss += float(loss.detach().cpu()) * batch_images.shape[0]
            total_items += batch_images.shape[0]
        history.append({"epoch": float(epoch), "loss": total_loss / max(total_items, 1)})

    student.eval()
    with torch.inference_mode():
        eval_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=False, num_workers=0)
        total = 0
        agree = 0
        kl_total = 0.0
        for batch_images, batch_teacher_logits in eval_loader:
            batch_images = batch_images.to(runtime_device)
            batch_teacher_logits = batch_teacher_logits.to(runtime_device)
            student_logits = student(batch_images)
            teacher_top1 = batch_teacher_logits.argmax(dim=1)
            student_top1 = student_logits.argmax(dim=1)
            agree += int((teacher_top1 == student_top1).sum().detach().cpu())
            total += batch_images.shape[0]
            kl = F.kl_div(
                F.log_softmax(student_logits / temperature, dim=1),
                F.softmax(batch_teacher_logits / temperature, dim=1),
                reduction="batchmean",
            ) * (temperature**2)
            kl_total += float(kl.detach().cpu()) * batch_images.shape[0]

    torch.save(student.state_dict(), paths["student"])
    report = {
        "teacher": metadata.teacher,
        "dataset": metadata.dataset,
        "samples": metadata.samples,
        "epochs": epochs,
        "temperature": temperature,
        "student_parameters": count_parameters(student),
        "teacher_student_top1_agreement": agree / max(total, 1),
        "distillation_kl": kl_total / max(total, 1),
        "history": history,
        "student_path": str(paths["student"]),
        "teacher_logits_path": metadata.logits_path,
    }
    paths["report"].write_text(json.dumps(report, indent=2), encoding="utf-8")
    return report


def run_all(
    teacher: str = "resnet18",
    dataset: str = "fake",
    samples: int = 128,
    batch_size: int = 16,
    epochs: int = 2,
    learning_rate: float = 1e-3,
    temperature: float = 3.0,
    device: str = "cpu",
) -> dict[str, Any]:
    teacher_report = cache_teacher_logits(
        teacher=teacher,
        dataset=dataset,
        samples=samples,
        batch_size=batch_size,
        device=device,
    )
    student_report = train_student(
        epochs=epochs,
        batch_size=batch_size,
        learning_rate=learning_rate,
        temperature=temperature,
        device=device,
    )
    return {"teacher_cache": teacher_report, "student": student_report}


def read_report() -> dict[str, Any]:
    path = _paths()["report"]
    if not path.exists():
        return {"status": "missing", "message": "No report yet. Run train-student or run-all first."}
    return json.loads(path.read_text(encoding="utf-8"))
