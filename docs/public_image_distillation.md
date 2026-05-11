# Public image offline distillation

This project demonstrates offline distillation from a public image model.

The teacher is a pretrained torchvision ImageNet model such as `resnet18` or `resnet50`.
The student is a much smaller CNN with the same 1000-logit output space.

## Why offline?

Online distillation runs the teacher during every student training step. That is expensive.
Offline distillation runs the teacher once, saves the logits, and trains the student from those saved logits.

```text
public teacher model
  -> image batch
  -> teacher logits cache
  -> student training without calling teacher again
```

## Dataset modes

- `fake`: smoke test data. Use this to verify the pipeline without preparing images.
- `cifar10`: downloads CIFAR-10 and resizes images to ImageNet input size.
- `image_folder`: reads unlabeled images recursively from `data/images`.

For a real experiment, use `image_folder` with your own images. Labels are not required.

## Metrics

This project does not primarily optimize human ground-truth accuracy. It measures whether the
student imitates the teacher:

- `teacher_student_top1_agreement`
- `distillation_kl`
- student parameter count

## Relation to diffusion distillation

Diffusion distillation such as LCM or SDXL Turbo is a different, much heavier problem. It usually
requires latent-space objectives, schedulers, and GPU-heavy training. This repository is intended as
a small first step: it teaches the offline-cache pattern before moving to diffusion models.
