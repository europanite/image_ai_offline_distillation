---
layout: page
title: "🇫🇷 Français"
permalink: /fr/
lang: fr
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

Un petit GitHub-ready template pour découvrir **offline knowledge distillation à partir d’un modèle d’image public**.

Le projet conserve une structure full-stack simple :

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## Ce que ce projet apprend

Ce repository n’entraîne pas un grand diffusion model. Il enseigne le offline distillation pattern avec un public image classifier :

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

Le default teacher est `torchvision.models.resnet18` avec des public ImageNet weights. Vous pouvez aussi utiliser `resnet50` ou `mobilenet_v3_large`.

Le student est une tiny CNN qui output les mêmes 1000 ImageNet logits. Il est train pour imiter la softened probability distribution du teacher.

## Pourquoi il s’agit de offline distillation

L’artifact clé est :

```text
artifacts/teacher_logits_train.pt
```

Une fois ce file créé, le student peut être train sans call à nouveau le teacher model.

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test. Ne nécessite pas de real images. |
| `cifar10` | Télécharge CIFAR-10 et le resize à la ImageNet input size. |
| `image_folder` | Utilise vos propres unlabeled images sous `data/images`. |

Pour un real experiment, placez les images ici :

```text
data/images/
```

Les nested folders sont autorisés. Les labels ne sont pas requis.

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> Le frontend service utilise Expo Web avec Docker `network_mode: host`, afin que `expo start --web --localhost --port 8081` soit reachable depuis le host browser. C’est intended pour les Linux Docker environments.

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

Le frontend reste Expo-based. Docker exécute `expo export --platform web`, puis sert le exported web build sur `0.0.0.0:19006`. Cela évite les Docker networking problems avec l’interactive Expo dev server, tout en continuant à utiliser Expo pour le web build.

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

Pour votre propre image folder :

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

`report.json` inclut :

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

Distilling des text-to-image diffusion models comme Stable Diffusion est une task plus lourde. Cela implique généralement des latent-space objectives, des scheduler changes, du multi-step teacher sampling et un GPU-heavy training.

Ce repository est la première stage : il enseigne le offline logits-cache pattern avec des public image models. Une fois que cela fonctionne, le prochain step consiste à créer une diffusion-specific branch avec LCM-LoRA ou teacher latent predictions.
