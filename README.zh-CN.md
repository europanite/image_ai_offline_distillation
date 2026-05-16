---
layout: page
title: "🇨🇳 中文"
permalink: /zh-CN/
lang: zh-CN
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

一个小型 GitHub-ready template，用于体验**从公开图像模型进行 offline knowledge distillation**。

该项目保持简单的 full-stack 结构：

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## 本项目学习什么

这个 repository 不会训练大型 diffusion model。它通过 public image classifier 教你 offline distillation pattern：

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

Default teacher 是带有 public ImageNet weights 的 `torchvision.models.resnet18`。你也可以使用 `resnet50` 或 `mobilenet_v3_large`。

Student 是一个 tiny CNN，会输出相同的 1000 个 ImageNet logits。它会被 train 来模仿 teacher 的 softened probability distribution。

## 为什么这是 offline distillation

关键 artifact 是：

```text
artifacts/teacher_logits_train.pt
```

创建这个 file 之后，就可以在不再次 call teacher model 的情况下 train student。

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test。不需要真实 images。 |
| `cifar10` | 下载 CIFAR-10，并将其 resize 到 ImageNet input size。 |
| `image_folder` | 使用 `data/images` 下你自己的 unlabeled images。 |

如果要做 real experiment，请把 images 放在这里：

```text
data/images/
```

允许使用 nested folders。不需要 labels。

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> Frontend service 使用带有 Docker `network_mode: host` 的 Expo Web，因此 `expo start --web --localhost --port 8081` 可以从 host browser 访问。这适用于 Linux Docker environments。

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

Frontend 仍然基于 Expo。Docker 会运行 `expo export --platform web`，然后在 `0.0.0.0:19006` 上 serve exported web build。这样可以避免 interactive Expo dev server 带来的 Docker networking problems，同时仍然使用 Expo 生成 web build。

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

如果使用你自己的 image folder：

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

`report.json` 包含：

- `teacher_student_top1_agreement`
- `distillation_kl`
- `student_parameters`
- training loss history

## Tests

```bash
docker compose -f docker-compose.test.yml run --rm backend_test
docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm frontend_test
```

## 关于 diffusion models 的 notes

Distilling Stable Diffusion 等 text-to-image diffusion models 是更重的 task。它通常涉及 latent-space objectives、scheduler changes、multi-step teacher sampling，以及 GPU-heavy training。

这个 repository 是第一阶段：它通过 public image models 教你 offline logits-cache pattern。这个流程跑通之后，下一步是使用 LCM-LoRA 或 teacher latent predictions 创建 diffusion-specific branch。
