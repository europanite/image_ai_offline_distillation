from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

from PIL import Image

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp"}


class FlatImageFolderDataset:
    """A label-free recursive image folder dataset.

    It is intentionally not class-folder based. Offline distillation can use unlabeled images
    because the student only needs teacher logits.
    """

    def __init__(self, root: Path, transform: Callable):
        self.root = Path(root)
        self.transform = transform
        self.paths = sorted(
            path for path in self.root.rglob("*") if path.suffix.lower() in IMAGE_EXTENSIONS
        )
        if not self.paths:
            raise FileNotFoundError(
                f"No images found under {self.root}. Put jpg/png/webp files there, "
                "or use dataset='fake' for a smoke test."
            )

    def __len__(self) -> int:
        return len(self.paths)

    def __getitem__(self, index: int):
        image = Image.open(self.paths[index]).convert("RGB")
        return self.transform(image), -1


def build_dataset(dataset: str, samples: int | None = None):
    """Build a deterministic dataset and return (dataset, effective_samples).

    Torch/torchvision are imported lazily so API metadata endpoints remain lightweight.
    """

    import torch
    from torch.utils.data import Subset
    from torchvision import datasets, transforms

    from distillation.settings import data_dir, image_folder

    transform = transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
        ]
    )

    if dataset == "fake":
        effective = samples or 128
        base = datasets.FakeData(
            size=effective,
            image_size=(3, 224, 224),
            num_classes=1000,
            transform=transforms.Compose([
                transforms.ToTensor(),
                transforms.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
            ]),
            random_offset=0,
        )
        return base, effective

    if dataset == "cifar10":
        base = datasets.CIFAR10(
            root=str(data_dir()),
            train=True,
            download=True,
            transform=transform,
        )
    elif dataset == "image_folder":
        base = FlatImageFolderDataset(image_folder(), transform=transform)
    else:
        raise ValueError(f"Unsupported dataset: {dataset}")

    effective = min(samples or len(base), len(base))
    generator = torch.Generator().manual_seed(20260510)
    indices = torch.randperm(len(base), generator=generator)[:effective].tolist()
    return Subset(base, indices), effective
