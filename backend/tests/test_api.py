from http import HTTPStatus

from fastapi.testclient import TestClient
from main import app


client = TestClient(app)


def test_health_ok():
    response = client.get("/health")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"status": "ok"}


def test_root_exposes_api_links():
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert body["docs"] == "/docs"
    assert body["endpoints"]["run_all"] == "/api/v1/distillation/run-all"


def test_config_exposes_public_teacher_options():
    response = client.get("/api/v1/distillation/config")
    assert response.status_code == HTTPStatus.OK
    body = response.json()
    assert "resnet18" in body["supported_teachers"]
    assert "image_folder" in body["supported_datasets"]
    assert body["recommended_first_run"]["dataset"] == "fake"


def test_report_missing_is_explicit():
    response = client.get("/api/v1/distillation/report")
    assert response.status_code == HTTPStatus.OK
    assert response.json()["status"] in {"missing", "ok"}


def test_train_student_requires_teacher_cache():
    response = client.post("/api/v1/distillation/train-student", json={"epochs": 1})
    assert response.status_code == HTTPStatus.CONFLICT
    assert "Teacher cache is missing" in response.text
