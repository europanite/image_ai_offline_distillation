---
layout: page
title: "🇧🇷 PT-BR"
permalink: /pt-BR/
lang: pt-BR
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

Um pequeno GitHub-ready template para experimentar **offline knowledge distillation a partir de um modelo público de imagens**.

O projeto mantém uma estrutura full-stack simples:

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## O que este projeto ensina

Este repository não treina um diffusion model grande. Ele ensina o offline distillation pattern com um public image classifier:

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

O default teacher é `torchvision.models.resnet18` com public ImageNet weights. Você também pode usar `resnet50` ou `mobilenet_v3_large`.

O student é uma tiny CNN que output os mesmos 1000 ImageNet logits. Ele é train para imitar a softened probability distribution do teacher.

## Por que isso é offline distillation

O artifact principal é:

```text
artifacts/teacher_logits_train.pt
```

Depois que este file é criado, o student pode ser train sem call novamente o teacher model.

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test. Não requer real images. |
| `cifar10` | Faz download do CIFAR-10 e resize para o ImageNet input size. |
| `image_folder` | Usa suas próprias unlabeled images em `data/images`. |

Para um real experiment, coloque as images aqui:

```text
data/images/
```

Nested folders são permitidas. Labels não são obrigatórios.

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> O frontend service usa Expo Web com Docker `network_mode: host`, para que `expo start --web --localhost --port 8081` fique reachable a partir do host browser. Isso é intended para Linux Docker environments.

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

O frontend continua Expo-based. O Docker executa `expo export --platform web` e depois serve o exported web build em `0.0.0.0:19006`. Isso evita Docker networking problems com o interactive Expo dev server, mantendo o uso do Expo para o web build.

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

Para usar seu próprio image folder:

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

`report.json` inclui:

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

Distilling text-to-image diffusion models como Stable Diffusion é uma task mais pesada. Normalmente envolve latent-space objectives, scheduler changes, multi-step teacher sampling e GPU-heavy training.

Este repository é a primeira stage: ele ensina o offline logits-cache pattern com public image models. Depois que isso funcionar, o próximo step é criar uma diffusion-specific branch usando LCM-LoRA ou teacher latent predictions.
