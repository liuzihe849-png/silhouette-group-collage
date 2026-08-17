#!/usr/bin/env python3
"""Extract a source-resolution people alpha matte without changing RGB pixels."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageDraw


MODEL_IDS = {
    "birefnet-hr": "ZhengPeng7/BiRefNet_HR-matting",
    "birefnet-portrait": "ZhengPeng7/BiRefNet-portrait",
    "rembg-u2net-human": "u2net_human_seg",
}

MODEL_REVISIONS = {
    "birefnet-hr": "5d6b6f8adcb5b417c871b1d84ceaae9871355b7f",
    "birefnet-portrait": "ecdeb6240ef23557dbd48ff27c59c1a88cbcb755",
    "rembg-u2net-human": "rembg-md5-pinned",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--backend", choices=MODEL_IDS, default="birefnet-hr")
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


def run_birefnet(image: Image.Image, backend: str, requested_device: str) -> tuple[Image.Image, str]:
    import torch
    from torchvision import transforms
    from transformers import AutoModelForImageSegmentation

    model_id = MODEL_IDS[backend]
    device = choose_device(requested_device)
    size = 2048 if backend == "birefnet-hr" else 1024
    model = AutoModelForImageSegmentation.from_pretrained(
        model_id,
        revision=MODEL_REVISIONS[backend],
        trust_remote_code=True,
    )
    model.to(device)
    model.eval()
    model_dtype = next(model.parameters()).dtype

    transform = transforms.Compose(
        [
            transforms.Resize((size, size)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225]),
        ]
    )
    tensor = transform(image).unsqueeze(0).to(device=device, dtype=model_dtype)
    with torch.inference_mode():
        output = model(tensor)
        logits = output[-1] if isinstance(output, (list, tuple)) else output
        alpha = logits.sigmoid().float().cpu()[0].squeeze().numpy()
    matte = Image.fromarray(np.clip(alpha * 255.0, 0, 255).astype(np.uint8), "L")
    return matte.resize(image.size, Image.Resampling.LANCZOS), device


def run_rembg(image: Image.Image) -> tuple[Image.Image, str]:
    from io import BytesIO

    from rembg import new_session, remove

    payload = BytesIO()
    image.save(payload, format="PNG")
    session = new_session(MODEL_IDS["rembg-u2net-human"])
    result = remove(payload.getvalue(), session=session, only_mask=True, post_process_mask=False)
    matte = Image.open(BytesIO(result)).convert("L")
    return matte.resize(image.size, Image.Resampling.LANCZOS), "onnxruntime-cpu"


def alpha_stats(alpha: np.ndarray) -> dict[str, Any]:
    normalized = alpha.astype(np.float32) / 255.0
    foreground = normalized >= 0.5
    ys, xs = np.nonzero(foreground)
    bbox = None if len(xs) == 0 else [int(xs.min()), int(ys.min()), int(xs.max()) + 1, int(ys.max()) + 1]
    border = np.concatenate((foreground[0], foreground[-1], foreground[:, 0], foreground[:, -1]))
    return {
        "foreground_fraction_at_0_5": round(float(foreground.mean()), 6),
        "soft_edge_fraction_0_05_to_0_95": round(float(((normalized > 0.05) & (normalized < 0.95)).mean()), 6),
        "mean_alpha": round(float(normalized.mean()), 6),
        "bbox_xyxy": bbox,
        "touches_source_border": bool(border.any()),
        "alpha_min": int(alpha.min()),
        "alpha_max": int(alpha.max()),
    }


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


def main() -> None:
    args = parse_args()
    if not args.source.is_file():
        raise SystemExit(f"Source does not exist: {args.source}")
    args.output_dir.mkdir(parents=True, exist_ok=True)

    source_bytes = args.source.read_bytes()
    source = Image.open(args.source).convert("RGB")
    started = time.perf_counter()
    if args.backend.startswith("birefnet"):
        matte, device = run_birefnet(source, args.backend, args.device)
    else:
        matte, device = run_rembg(source)
    runtime_seconds = time.perf_counter() - started

    alpha_array = np.asarray(matte, dtype=np.uint8)
    rgb_array = np.asarray(source, dtype=np.uint8)
    rgba_array = np.dstack((rgb_array, alpha_array))
    rgba = Image.fromarray(rgba_array, "RGBA")

    alpha_path = args.output_dir / "alpha.png"
    rgba_path = args.output_dir / "people-rgba.png"
    preview_path = args.output_dir / "checker-preview.png"
    manifest_path = args.output_dir / "manifest.json"
    matte.save(alpha_path)
    rgba.save(rgba_path)
    checker_preview(rgba).save(preview_path)

    roundtrip = np.asarray(Image.open(rgba_path).convert("RGBA"), dtype=np.uint8)
    rgb_lock = bool(np.array_equal(roundtrip[:, :, :3], rgb_array))
    manifest = {
        "phase": 1,
        "source": str(args.source.resolve()),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "width": source.width,
        "height": source.height,
        "backend": args.backend,
        "model": MODEL_IDS[args.backend],
        "model_revision": MODEL_REVISIONS[args.backend],
        "device": device,
        "runtime_seconds": round(runtime_seconds, 3),
        "platform": platform.platform(),
        "rgb_lock_passed": rgb_lock,
        "alpha": alpha_stats(alpha_array),
        "manual_review_required": True,
        "files": {"alpha": alpha_path.name, "rgba": rgba_path.name, "preview": preview_path.name},
    }
    manifest_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if not rgb_lock:
        raise SystemExit("RGB pixel lock failed")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
