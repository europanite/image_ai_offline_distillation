from __future__ import annotations

from pydantic import BaseModel, Field


class CacheTeacherRequest(BaseModel):
    teacher: str = Field(default="resnet18", description="Public torchvision teacher model.")
    dataset: str = Field(default="fake", description="fake, cifar10, or image_folder.")
    samples: int = Field(default=128, ge=1, le=50000)
    batch_size: int = Field(default=16, ge=1, le=256)
    device: str = Field(default="cpu", description="cpu or cuda.")


class TrainStudentRequest(BaseModel):
    epochs: int = Field(default=2, ge=1, le=100)
    batch_size: int = Field(default=16, ge=1, le=256)
    learning_rate: float = Field(default=1e-3, gt=0, le=1.0)
    temperature: float = Field(default=3.0, gt=0.1, le=20.0)
    device: str = Field(default="cpu", description="cpu or cuda.")


class RunAllRequest(CacheTeacherRequest, TrainStudentRequest):
    pass


class PipelineResponse(BaseModel):
    ok: bool
    message: str
    report: dict | None = None
