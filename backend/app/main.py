from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import distillation

app = FastAPI(
    title="Public Image Offline Distillation API",
    description="Cache logits from a public image teacher model and train a small student offline.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root() -> dict[str, object]:
    return {
        "status": "ok",
        "service": "Public Image Offline Distillation API",
        "docs": "/docs",
        "health": "/health",
        "endpoints": {
            "config": "/api/v1/distillation/config",
            "report": "/api/v1/distillation/report",
            "cache_teacher": "/api/v1/distillation/cache-teacher",
            "train_student": "/api/v1/distillation/train-student",
            "run_all": "/api/v1/distillation/run-all",
        },
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(distillation.router)
