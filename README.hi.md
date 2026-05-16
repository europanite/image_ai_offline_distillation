---
layout: page
title: "🇮🇳 हिन्दी"
permalink: /hi/
lang: hi
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

**सार्वजनिक इमेज मॉडल से offline knowledge distillation** का अनुभव करने के लिए एक छोटा, GitHub-ready template।

यह प्रोजेक्ट एक सरल full-stack संरचना रखता है:

- **Backend**: FastAPI + PyTorch + torchvision
- **Frontend**: Expo / React Native Web
- **Container**: Docker Compose
- **No Makefile**

## यह क्या सिखाता है

यह repository कोई बड़ा diffusion model train नहीं करती। यह public image classifier के साथ offline distillation pattern सिखाती है:

```text
public ImageNet teacher model
  -> run once on images
  -> save teacher logits
  -> train a small CNN student from cached logits
  -> compare teacher/student agreement
```

Default teacher public ImageNet weights वाला `torchvision.models.resnet18` है। आप `resnet50` या `mobilenet_v3_large` भी उपयोग कर सकते हैं।

Student एक tiny CNN है जो वही 1000 ImageNet logits output करता है। इसे teacher के softened probability distribution की नकल करने के लिए train किया जाता है।

## यह offline distillation क्यों है

मुख्य artifact है:

```text
artifacts/teacher_logits_train.pt
```

यह file बनने के बाद, student को teacher model को फिर से call किए बिना train किया जा सकता है।

## Dataset modes

| Dataset | Purpose |
| --- | --- |
| `fake` | Smoke test. Real images की आवश्यकता नहीं होती। |
| `cifar10` | CIFAR-10 download करता है और उसे ImageNet input size में resize करता है। |
| `image_folder` | `data/images` के अंदर आपकी अपनी unlabeled images का उपयोग करता है। |

Real experiment के लिए, images यहाँ रखें:

```text
data/images/
```

Nested folders की अनुमति है। Labels आवश्यक नहीं हैं।

## Start

```bash
docker compose down -v
docker compose down -v
docker compose up --build
```


> Frontend service Docker `network_mode: host` के साथ Expo Web का उपयोग करती है ताकि `expo start --web --localhost --port 8081` host browser से reachable रहे। यह Linux Docker environments के लिए intended है।

Open:

```text
Frontend: http://localhost:8081
Frontend direct Metro: http://localhost:8081
Backend:  http://localhost:8000/docs
```


## Frontend note

Frontend Expo-based ही रहता है। Docker `expo export --platform web` चलाता है और फिर exported web build को `0.0.0.0:19006` पर serve करता है। इससे interactive Expo dev server के साथ Docker networking problems से बचा जाता है, जबकि web build के लिए Expo का उपयोग जारी रहता है।

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

अपना image folder उपयोग करने के लिए:

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

`report.json` में शामिल है:

- `teacher_student_top1_agreement`
- `distillation_kl`
- `student_parameters`
- training loss history

## Tests

```bash
docker compose -f docker-compose.test.yml run --rm backend_test
docker compose -f docker-compose.yml -f docker-compose.test.yml run --rm frontend_test
```

## Diffusion models के बारे में notes

Stable Diffusion जैसे text-to-image diffusion models को distill करना अधिक भारी task है। इसमें आम तौर पर latent-space objectives, scheduler changes, multi-step teacher sampling, और GPU-heavy training शामिल होते हैं।

यह repository पहला stage है: यह public image models के साथ offline logits-cache pattern सिखाती है। यह काम करने के बाद, अगला step LCM-LoRA या teacher latent predictions का उपयोग करके diffusion-specific branch बनाना है।
