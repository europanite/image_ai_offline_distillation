from __future__ import annotations

import argparse
import json

from distillation.pipeline import cache_teacher_logits, run_all, train_student


def main() -> None:
    parser = argparse.ArgumentParser(description="Public image offline distillation CLI")
    sub = parser.add_subparsers(dest="command", required=True)

    cache = sub.add_parser("cache-teacher", help="Run public teacher once and save logits.")
    cache.add_argument("--teacher", default="resnet18")
    cache.add_argument("--dataset", default="fake", choices=["fake", "cifar10", "image_folder"])
    cache.add_argument("--samples", type=int, default=128)
    cache.add_argument("--batch-size", type=int, default=16)
    cache.add_argument("--device", default="cpu")

    train = sub.add_parser("train-student", help="Train student from saved teacher logits.")
    train.add_argument("--epochs", type=int, default=2)
    train.add_argument("--batch-size", type=int, default=16)
    train.add_argument("--learning-rate", type=float, default=1e-3)
    train.add_argument("--temperature", type=float, default=3.0)
    train.add_argument("--device", default="cpu")

    all_cmd = sub.add_parser("run-all", help="Cache teacher logits and train student.")
    all_cmd.add_argument("--teacher", default="resnet18")
    all_cmd.add_argument("--dataset", default="fake", choices=["fake", "cifar10", "image_folder"])
    all_cmd.add_argument("--samples", type=int, default=128)
    all_cmd.add_argument("--batch-size", type=int, default=16)
    all_cmd.add_argument("--epochs", type=int, default=2)
    all_cmd.add_argument("--learning-rate", type=float, default=1e-3)
    all_cmd.add_argument("--temperature", type=float, default=3.0)
    all_cmd.add_argument("--device", default="cpu")

    args = parser.parse_args()
    if args.command == "cache-teacher":
        result = cache_teacher_logits(
            teacher=args.teacher,
            dataset=args.dataset,
            samples=args.samples,
            batch_size=args.batch_size,
            device=args.device,
        )
    elif args.command == "train-student":
        result = train_student(
            epochs=args.epochs,
            batch_size=args.batch_size,
            learning_rate=args.learning_rate,
            temperature=args.temperature,
            device=args.device,
        )
    else:
        result = run_all(
            teacher=args.teacher,
            dataset=args.dataset,
            samples=args.samples,
            batch_size=args.batch_size,
            epochs=args.epochs,
            learning_rate=args.learning_rate,
            temperature=args.temperature,
            device=args.device,
        )
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
