from __future__ import annotations

from fastapi import APIRouter, HTTPException

from distillation import pipeline
from distillation.schemas import CacheTeacherRequest, PipelineResponse, RunAllRequest, TrainStudentRequest

router = APIRouter(prefix="/api/v1/distillation", tags=["distillation"])


@router.get("/config")
def config() -> dict:
    return pipeline.get_config()


@router.get("/report")
def report() -> dict:
    return pipeline.read_report()


@router.post("/cache-teacher", response_model=PipelineResponse)
def cache_teacher(payload: CacheTeacherRequest) -> PipelineResponse:
    try:
        report_data = pipeline.cache_teacher_logits(**payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return PipelineResponse(ok=True, message="Teacher logits were cached offline.", report=report_data)


@router.post("/train-student", response_model=PipelineResponse)
def train_student(payload: TrainStudentRequest) -> PipelineResponse:
    try:
        report_data = pipeline.train_student(**payload.model_dump())
    except FileNotFoundError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return PipelineResponse(ok=True, message="Student was trained from cached teacher logits.", report=report_data)


@router.post("/run-all", response_model=PipelineResponse)
def run_all(payload: RunAllRequest) -> PipelineResponse:
    try:
        report_data = pipeline.run_all(**payload.model_dump())
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    return PipelineResponse(ok=True, message="Offline image distillation pipeline completed.", report=report_data)
