---
layout: page
title: "🇰🇷 한국어"
permalink: /ko/
lang: ko
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

**공개 이미지 모델에서 offline knowledge distillation**을 체험하기 위한 작은 GitHub-ready template입니다.

이 프로젝트는 단순한 full-stack 구조를 유지합니다:

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## 여기서 배우는 것

이 repository는 대형 diffusion model을 train하지 않습니다. public image classifier를 사용해 offline distillation pattern을 가르칩니다:

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

Default teacher는 public ImageNet weights를 사용하는 `torchvision.models.resnet18`입니다. `resnet50` 또는 `mobilenet_v3_large`도 사용할 수 있습니다.

Student는 동일한 1000개의 ImageNet logits를 output하는 tiny CNN입니다. Teacher의 softened probability distribution을 모방하도록 train됩니다.

## 왜 offline distillation인가

핵심 artifact는 다음입니다:

```text
artifacts/teacher_logits_train.pt
```

이 file이 생성된 후에는 teacher model을 다시 call하지 않고 student를 train할 수 있습니다.

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test. Real images가 필요하지 않습니다. |
| `cifar10` | CIFAR-10을 download하고 ImageNet input size로 resize합니다. |
| `image_folder` | `data/images` 아래의 자체 unlabeled images를 사용합니다. |

Real experiment를 위해 images를 여기에 넣으세요:

```text
data/images/
```

Nested folders를 사용할 수 있습니다. Labels는 필요하지 않습니다.

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> Frontend service는 Docker `network_mode: host`와 함께 Expo Web을 사용하므로 `expo start --web --localhost --port 8081`에 host browser에서 접근할 수 있습니다. 이는 Linux Docker environments를 intended한 것입니다.

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

Frontend는 Expo-based 상태를 유지합니다. Docker는 `expo export --platform web`을 실행한 다음 exported web build를 `0.0.0.0:19006`에서 serve합니다. 이렇게 하면 web build에는 계속 Expo를 사용하면서 interactive Expo dev server의 Docker networking problems를 피할 수 있습니다.

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

자체 image folder를 사용하는 경우:

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

`report.json`에는 다음이 포함됩니다:

- `teacher_student_top1_agreement`
- `distillation_kl`
- `student_parameters`
- training loss history

## Tests

```bash
docker compose -f docker-compose.test.yml run --rm backend_test
docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm frontend_test
```

## Diffusion models에 대한 notes

Stable Diffusion 같은 text-to-image diffusion models를 distill하는 것은 더 무거운 task입니다. 일반적으로 latent-space objectives, scheduler changes, multi-step teacher sampling, GPU-heavy training이 포함됩니다.

이 repository는 첫 번째 stage입니다. public image models로 offline logits-cache pattern을 가르칩니다. 이것이 작동하면 다음 step은 LCM-LoRA 또는 teacher latent predictions를 사용해 diffusion-specific branch를 만드는 것입니다.
