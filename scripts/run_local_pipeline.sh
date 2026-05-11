#!/usr/bin/env bash
set -euo pipefail

python /app/cli.py run-all \
  --teacher "${TEACHER:-resnet18}" \
  --dataset "${DATASET:-fake}" \
  --samples "${SAMPLES:-128}" \
  --batch-size "${BATCH_SIZE:-16}" \
  --epochs "${EPOCHS:-2}" \
  --temperature "${TEMPERATURE:-3.0}" \
  --device "${DEVICE:-cpu}"
