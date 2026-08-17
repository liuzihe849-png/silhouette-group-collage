#!/usr/bin/env python3
"""Remove manually approved foreground-occluder masks from a people alpha."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw


MODEL_ID = "facebook/sam2.1-hiera-small"


def parse_box(value: str) -> list[float]:
    parts = value.split(",")
    if len(parts) != 4:
        raise argparse.ArgumentTypeError("box must be x0,y0,x1,y1")
    try:
        box = [float(part) for part in parts]
    except ValueError as exc:
        raise argparse.ArgumentTypeError("box coordinates must be numbers") from exc
    if box[2] <= box[0] or box[3] <= box[1]:
        raise argparse.ArgumentTypeError("box must have positive width and height")
    return box


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--input-alpha", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--box", type=parse_box, action="append", required=True)
    parser.add_argument(
        "--variant-index",
        type=int,
        default=1,
        help="Zero-based SAM2 multimask candidate selected after visual review (default: 1).",
    )
    parser.add_argument("--mask-threshold", type=float, default=0.5)
    parser.add_argument("--max-removed-person-fraction", type=float, default=0.03)
    parser.add_argument(
        "--confirm-remove-foreground-occluders",
        action="store_true",
        help="Required acknowledgement: removal may break group continuity and is not the default workflow.",
    )
    parser.add_argument("--device", choices=("auto", "mps", "cuda", "cpu"), default="auto")
    return parser.parse_args()


def choose_device(requested: str) -> str:
    import torch

    if requested != "auto":
        return requested
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


def checker_preview(rgba: Image.Image) -> Image.Image:
    width, height = rgba.size
    tile = max(12, min(width, height) // 36)
    bg = Image.new("RGB", rgba.size, "#dedbd2")
    draw = ImageDraw.Draw(bg)
    for y in range(0, height, tile):
        for x in range(0, width, tile):
            if ((x // tile) + (y // tile)) % 2:
                draw.rectangle((x, y, x + tile - 1, y + tile - 1), fill="#b9b6ae")
    bg.paste(rgba, mask=rgba.getchannel("A"))
    return bg


def sam2_variants(image: Image.Image, boxes: list[list[float]], device: str):
    import torch
    from transformers import Sam2Model, Sam2Processor

    processor = Sam2Processor.from_pretrained(MODEL_ID)
    model = Sam2Model.from_pretrained(MODEL_ID).to(device).eval()
    inputs = processor(images=image, input_boxes=[boxes], return_tensors="pt")
    inputs = {key: value.to(device) if hasattr(value, "to") else value for key, value in inputs.items()}
    with torch.inference_mode():
        outputs = model(**inputs, multimask_output=True)
    masks = processor.post_process_masks(
        outputs.pred_masks.detach().float().cpu(),
        inputs["original_sizes"].detach().cpu(),
        binarize=False,
    )[0]
    probabilities = torch.sigmoid(masks).numpy()
    scores = outputs.iou_scores.detach().float().cpu()[0].numpy()
    return probabilities, scores


def make_rgba(rgb: np.ndarray, alpha: np.ndarray) -> Image.Image:
    return Image.fromarray(np.dstack((rgb, alpha.astype(np.uint8))), "RGBA")


def main() -> None:
    args = parse_args()
    if not args.source.is_file() or not args.input_alpha.is_file():
        raise SystemExit("source and input alpha must exist")
    if args.variant_index < 0 or args.variant_index > 2:
        raise SystemExit("--variant-index must be 0, 1, or 2")
    if not args.confirm_remove_foreground_occluders:
        raise SystemExit(
            "Foreground occluders are retained by default. Re-run with "
            "--confirm-remove-foreground-occluders only after an explicit aesthetic decision."
        )
    if not 0.0 < args.mask_threshold < 1.0:
        raise SystemExit("--mask-threshold must be between 0 and 1")

    args.output_dir.mkdir(parents=True, exist_ok=True)
    candidates_dir = args.output_dir / "candidates"
    candidates_dir.mkdir(exist_ok=True)
    source_bytes = args.source.read_bytes()
    source = Image.open(args.source).convert("RGB")
    alpha_image = Image.open(args.input_alpha).convert("L")
    if alpha_image.size != source.size:
        raise SystemExit("input alpha dimensions do not match source")
    rgb = np.asarray(source, dtype=np.uint8)
    input_alpha = np.asarray(alpha_image, dtype=np.uint8)
    device = choose_device(args.device)

    started = time.perf_counter()
    variants, scores = sam2_variants(source, args.box, device)
    runtime_seconds = time.perf_counter() - started
    if variants.shape[0] != len(args.box):
        raise SystemExit("SAM2 returned an unexpected object count")

    selected_binary = []
    objects = []
    for object_index in range(variants.shape[0]):
        variant_records = []
        for variant_index in range(variants.shape[1]):
            probability = variants[object_index, variant_index]
            alpha = np.clip(probability * 255.0, 0, 255).astype(np.uint8)
            path = candidates_dir / f"object-{object_index + 1:02d}-variant-{variant_index + 1}.png"
            Image.fromarray(alpha, "L").save(path)
            variant_records.append(
                {
                    "variant_index": variant_index,
                    "iou_score": round(float(scores[object_index, variant_index]), 6),
                    "foreground_fraction": round(float((probability >= args.mask_threshold).mean()), 8),
                    "mask": str(path.relative_to(args.output_dir)),
                }
            )
        chosen = variants[object_index, args.variant_index] >= args.mask_threshold
        selected_binary.append(chosen)
        objects.append(
            {
                "object_index": object_index,
                "approved_box_xyxy": [round(value, 2) for value in args.box[object_index]],
                "selected_variant_index": args.variant_index,
                "variants": variant_records,
            }
        )

    occluder = np.logical_or.reduce(selected_binary)
    # Subtract only SAM2-confirmed occluder pixels. Never synthesize hidden person pixels.
    cleaned_alpha = np.where(occluder, 0, input_alpha).astype(np.uint8)
    occluder_alpha = (occluder * 255).astype(np.uint8)
    Image.fromarray(occluder_alpha, "L").save(args.output_dir / "occluder-mask.png")
    Image.fromarray(cleaned_alpha, "L").save(args.output_dir / "cleaned-alpha.png")
    rgba = make_rgba(rgb, cleaned_alpha)
    rgba_path = args.output_dir / "cleaned-people-rgba.png"
    rgba.save(rgba_path)
    checker_preview(rgba).save(args.output_dir / "cleaned-checker-preview.png")

    roundtrip = np.asarray(Image.open(rgba_path).convert("RGBA"), dtype=np.uint8)
    rgb_lock = bool(np.array_equal(roundtrip[:, :, :3], rgb))
    removed = (input_alpha >= 128) & occluder
    input_foreground = input_alpha >= 128
    removed_person_fraction = float(removed.sum() / max(int(input_foreground.sum()), 1))
    removal_gate_passed = removed_person_fraction <= args.max_removed_person_fraction
    manifest = {
        "phase": "2.1",
        "experimental": True,
        "aesthetic_default": False,
        "explicit_removal_confirmation": True,
        "source": str(args.source.resolve()),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "input_alpha": str(args.input_alpha.resolve()),
        "width": source.width,
        "height": source.height,
        "model": MODEL_ID,
        "device": device,
        "runtime_seconds": round(runtime_seconds, 3),
        "platform": platform.platform(),
        "mask_threshold": args.mask_threshold,
        "rgb_lock_passed": rgb_lock,
        "occluder_fraction": round(float(occluder.mean()), 8),
        "removed_foreground_fraction": round(float(removed.mean()), 8),
        "removed_fraction_of_input_foreground": round(removed_person_fraction, 8),
        "max_removed_person_fraction": args.max_removed_person_fraction,
        "removal_gate_passed": removal_gate_passed,
        "objects": objects,
        "manual_candidate_review_required": True,
        "hidden_anatomy_reconstructed": False,
    }
    (args.output_dir / "occluder-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if not rgb_lock:
        raise SystemExit("RGB pixel lock failed")
    if not removal_gate_passed:
        raise SystemExit(
            f"Removal safety gate failed: {removed_person_fraction:.4f} exceeds "
            f"{args.max_removed_person_fraction:.4f}"
        )
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
