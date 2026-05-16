---
layout: page
title: "🇪🇸 Español"
permalink: /es/
lang: es
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

Un pequeño GitHub-ready template para experimentar la **offline knowledge distillation desde un modelo público de imágenes**.

El proyecto mantiene una estructura full-stack sencilla:

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## Qué se aprende aquí

Este repository no entrena un diffusion model grande. Enseña el offline distillation pattern con un public image classifier:

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

El default teacher es `torchvision.models.resnet18` con public ImageNet weights. También puedes usar `resnet50` o `mobilenet_v3_large`.

El student es una tiny CNN que output los mismos 1000 ImageNet logits. Se train para imitar la softened probability distribution del teacher.

## Por qué esto es offline distillation

El artifact clave es:

```text
artifacts/teacher_logits_train.pt
```

Después de crear este file, el student puede train sin volver a call el teacher model.

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test. No requiere real images. |
| `cifar10` | Descarga CIFAR-10 y lo resize al ImageNet input size. |
| `image_folder` | Usa tus propias unlabeled images bajo `data/images`. |

Para un real experiment, coloca images aquí:

```text
data/images/
```

Se permiten nested folders. No se requieren labels.

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> El frontend service usa Expo Web con Docker `network_mode: host`, de modo que `expo start --web --localhost --port 8081` sea reachable desde el host browser. Esto está intended para Linux Docker environments.

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

El frontend sigue siendo Expo-based. Docker ejecuta `expo export --platform web` y luego sirve el exported web build en `0.0.0.0:19006`. Esto evita Docker networking problems con el interactive Expo dev server, mientras se sigue usando Expo para el web build.

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

Para usar tu propio image folder:

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

`report.json` incluye:

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

Distilling text-to-image diffusion models como Stable Diffusion es una task más pesada. Normalmente implica latent-space objectives, scheduler changes, multi-step teacher sampling y GPU-heavy training.

Este repository es la primera stage: enseña el offline logits-cache pattern con public image models. Después de que esto funcione, el siguiente step es crear una diffusion-specific branch usando LCM-LoRA o teacher latent predictions.
