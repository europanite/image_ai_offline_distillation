---
layout: page
title: "🇯🇵 日本語"
permalink: /ja/
lang: ja
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

**公開画像モデルからのオフライン知識蒸留**を体験するための、小さな GitHub-ready template です。

このプロジェクトはシンプルな full-stack 構成を保っています:

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## このリポジトリで学べること

この repository は大規模な diffusion model を train するものではありません。public image classifier を使って offline distillation pattern を学ぶためのものです:

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

Default teacher は public ImageNet weights を持つ `torchvision.models.resnet18` です。`resnet50` または `mobilenet_v3_large` も使用できます。

Student は同じ 1000 個の ImageNet logits を output する tiny CNN です。Teacher の softened probability distribution を模倣するように train されます。

## なぜ offline distillation なのか

重要な artifact は次の file です:

```text
artifacts/teacher_logits_train.pt
```

この file が作成された後は、teacher model を再度 call せずに student を train できます。

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test。実画像は不要です。 |
| `cifar10` | CIFAR-10 を download し、ImageNet input size に resize します。 |
| `image_folder` | `data/images` 配下にある独自の unlabeled images を使用します。 |

Real experiment では、images をここに置きます:

```text
data/images/
```

Nested folders も使用できます。Labels は不要です。

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> Frontend service は Docker の `network_mode: host` と Expo Web を使用するため、`expo start --web --localhost --port 8081` に host browser からアクセスできます。これは Linux Docker environments 向けです。

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

Frontend は Expo-based のままです。Docker は `expo export --platform web` を実行し、exported web build を `0.0.0.0:19006` で serve します。これにより、web build では Expo を使い続けながら、interactive Expo dev server に伴う Docker networking problems を回避できます。

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

独自の image folder を使う場合:

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

`report.json` には次が含まれます:

- `teacher_student_top1_agreement`
- `distillation_kl`
- `student_parameters`
- training loss history

## Tests

```bash
docker compose -f docker-compose.test.yml run --rm backend_test
docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm frontend_test
```

## Diffusion models についての notes

Stable Diffusion のような text-to-image diffusion models を distill するのは、より重い task です。通常は latent-space objectives、scheduler changes、multi-step teacher sampling、GPU-heavy training が必要になります。

この repository は最初の stage です。public image models を使って offline logits-cache pattern を学びます。これが動作した後の next step は、LCM-LoRA または teacher latent predictions を使った diffusion-specific branch を作成することです。
