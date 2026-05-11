from __future__ import annotations


def build_teacher(name: str):
    """Build a public torchvision teacher model with ImageNet weights."""

    from torchvision import models

    normalized = name.lower().strip()
    if normalized == "resnet18":
        weights = models.ResNet18_Weights.IMAGENET1K_V1
        model = models.resnet18(weights=weights)
    elif normalized == "resnet50":
        weights = models.ResNet50_Weights.IMAGENET1K_V2
        model = models.resnet50(weights=weights)
    elif normalized == "mobilenet_v3_large":
        weights = models.MobileNet_V3_Large_Weights.IMAGENET1K_V2
        model = models.mobilenet_v3_large(weights=weights)
    else:
        raise ValueError(f"Unsupported teacher: {name}")
    model.eval()
    return model


def build_student(num_classes: int = 1000):
    """Small CNN student for 224x224 ImageNet-style logits."""

    import torch.nn as nn

    return nn.Sequential(
        nn.Conv2d(3, 16, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(16),
        nn.ReLU(inplace=True),
        nn.Conv2d(16, 32, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(32),
        nn.ReLU(inplace=True),
        nn.Conv2d(32, 64, kernel_size=3, stride=2, padding=1),
        nn.BatchNorm2d(64),
        nn.ReLU(inplace=True),
        nn.AdaptiveAvgPool2d((1, 1)),
        nn.Flatten(),
        nn.Linear(64, num_classes),
    )


def count_parameters(model) -> int:
    return sum(parameter.numel() for parameter in model.parameters())
