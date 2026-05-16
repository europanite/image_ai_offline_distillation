---
layout: page
title: "🇩🇪 Deutsch"
permalink: /de/
lang: de
---

# [Image Offline Distillation](https://github.com/europanite/image_ai_offline_distillation "Image Offline Distillation")

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
![OS](https://img.shields.io/badge/OS-Linux%20%7C%20macOS%20%7C%20Windows-blue)
[![Python](https://img.shields.io/badge/python-3.10%20|%203.11|%203.12|%203.13-blue)](https://www.python.org/)

[![CodeQL Advanced](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/codeql.yml/badge.svg)](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/codeql.yml)
[![Python Lint](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/lint.yml/badge.svg)](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/lint.yml)
[![CI](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/ci.yml/badge.svg)](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/ci.yml)
[![Pytest](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/pytest.yml/badge.svg)](https://github.com/europanite/image_ai_offline_distillation/actions/workflows/pytest.yml)

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![Pytest](https://img.shields.io/badge/pytest-%23ffffff.svg?style=for-the-badge&logo=pytest&logoColor=2f9fe3)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![React Native](https://img.shields.io/badge/react_native-%2320232a.svg?style=for-the-badge&logo=react&logoColor=%2361DAFB)
![TypeScript](https://img.shields.io/badge/typescript-%23007ACC.svg?style=for-the-badge&logo=typescript&logoColor=white)
![Jest](https://img.shields.io/badge/-jest-%23C21325?style=for-the-badge&logo=jest&logoColor=white)
![Expo](https://img.shields.io/badge/expo-1C1E24?style=for-the-badge&logo=expo&logoColor=#D04A37)

<p align="right">
  <a href="https://europanite.github.io/image_ai_offline_distillation/">🇺🇸 English</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/hi/">🇮🇳 हिंदी</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/ja/">🇯🇵 日本語</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/zh-CN/">🇨🇳 简体中文</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/es/">🇪🇸 Español</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/pt-BR/">🇧🇷 Português (Brasil)</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/ko/">🇰🇷 한국어</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/de/">🇩🇪 Deutsch</a> |
  <a href="https://europanite.github.io/image_ai_offline_distillation/fr/">🇫🇷 Français</a>
</p>

Ein kleines GitHub-ready template, um **offline knowledge distillation aus einem öffentlichen Bildmodell** zu erleben.

Das Projekt behält eine einfache full-stack Struktur bei:

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## Was hier gelernt wird

Dieses repository trainiert kein großes diffusion model. Es vermittelt das offline distillation pattern mit einem public image classifier:

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

Der default teacher ist `torchvision.models.resnet18` mit public ImageNet weights. Du kannst auch `resnet50` oder `mobilenet_v3_large` verwenden.

Der student ist eine tiny CNN, die dieselben 1000 ImageNet logits output. Sie wird trainiert, um die softened probability distribution des teacher nachzuahmen.

## Warum dies offline distillation ist

Das zentrale artifact ist:

```text
artifacts/teacher_logits_train.pt
```

Nachdem diese file erstellt wurde, kann der student trainiert werden, ohne das teacher model erneut zu callen.

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test. Erfordert keine real images. |
| `cifar10` | Lädt CIFAR-10 herunter und resized es auf die ImageNet input size. |
| `image_folder` | Verwendet deine eigenen unlabeled images unter `data/images`. |

Für ein real experiment lege images hier ab:

```text
data/images/
```

Nested folders sind erlaubt. Labels sind nicht erforderlich.

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> Der frontend service verwendet Expo Web mit Docker `network_mode: host`, sodass `expo start --web --localhost --port 8081` vom host browser aus reachable ist. Dies ist für Linux Docker environments intended.

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

Das frontend bleibt Expo-based. Docker führt `expo export --platform web` aus und serviert anschließend den exported web build auf `0.0.0.0:19006`. Dadurch werden Docker networking problems mit dem interactive Expo dev server vermieden, während Expo weiterhin für den web build genutzt wird.

## Run from API

```bash
curl -X POST http://localhost:8000/api/v1/distillation/run-all   -H 'Content-Type: application/json'   -d '{
    "teacher": "resnet18",
    "dataset": "fake",
    "samples": 128,
    "batch_size": 16,
    "epochs": 2,
    "learning_rate": 0.001,
    "temperature": 3.0,
    "device": "cpu"
  }'
```

## Run from CLI

```bash
docker compose run --rm backend python /app/cli.py run-all   --teacher resnet18   --dataset fake   --samples 128   --batch-size 16   --epochs 2   --temperature 3.0   --device cpu
```

Für deinen eigenen image folder:

```bash
docker compose run --rm backend python /app/cli.py run-all   --teacher resnet18   --dataset image_folder   --samples 256   --epochs 3   --device cpu
```

## Outputs

```text
artifacts/
├── teacher_logits_train.pt
├── teacher_cache_metadata.json
├── student_model.pt
└── report.json
```

`report.json` enthält:

- `teacher_student_top1_agreement`
- `distillation_kl`
- `student_parameters`
- training loss history

## Tests

```bash
docker compose -f docker-compose.test.yml run --rm backend_test
docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm frontend_test
```

## Notes about diffusion models

Das Distilling von text-to-image diffusion models wie Stable Diffusion ist eine schwerere task. Üblicherweise umfasst es latent-space objectives, scheduler changes, multi-step teacher sampling und GPU-heavy training.

Dieses repository ist die erste stage: Es vermittelt das offline logits-cache pattern mit public image models. Nachdem dies funktioniert, ist der nächste step, eine diffusion-specific branch mit LCM-LoRA oder teacher latent predictions zu erstellen.
