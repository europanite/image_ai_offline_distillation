from __future__ import annotations

import os
from pathlib import Path


SUPPORTED_TEACHERS = ["resnet18", "resnet50", "mobilenet_v3_large"]
SUPPORTED_DATASETS = ["fake", "cifar10", "image_folder"]


def artifact_dir() -> Path:
    path = Path(os.getenv("DISTILLATION_ARTIFACT_DIR", "artifacts"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def data_dir() -> Path:
    path = Path(os.getenv("DISTILLATION_DATA_DIR", "data"))
    path.mkdir(parents=True, exist_ok=True)
    return path


def image_folder() -> Path:
    return Path(os.getenv("DISTILLATION_IMAGE_FOLDER", str(data_dir() / "images")))
