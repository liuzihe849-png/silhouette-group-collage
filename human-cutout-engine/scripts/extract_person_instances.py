#!/usr/bin/env python3
"""Detect each person, segment each instance, and constrain a soft union alpha."""

from __future__ import annotations

import argparse
import hashlib
import json
import platform
import time
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter


DETECTOR_ID = "IDEA-Research/grounding-dino-tiny"
INSTANCE_DETECTOR_ID = "torchvision/maskrcnn_resnet50_fpn_v2_coco"
SEGMENTER_ID = "facebook/sam2.1-hiera-small"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--birefnet-alpha", type=Path)
    parser.add_argument("--expected-count", type=int)
    parser.add_argument("--detector", choices=("maskrcnn", "grounding-dino"), default="maskrcnn")
    parser.add_argument("--instance-segmenter", choices=("detector-mask", "sam2"), default="detector-mask")
    parser.add_argument("--person-score-threshold", type=float, default=0.9)
    parser.add_argument("--box-threshold", type=float, default=0.28)
    parser.add_argument("--text-threshold", type=float, default=0.22)
    parser.add_argument("--nms-iou", type=float, default=0.55)
    parser.add_argument("--instance-support-threshold", type=float, default=0.2)
    parser.add_argument("--constraint-radius", type=int, default=2)
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


def box_iou(a: np.ndarray, b: np.ndarray) -> float:
    x0, y0 = np.maximum(a[:2], b[:2])
    x1, y1 = np.minimum(a[2:], b[2:])
    intersection = max(0.0, float(x1 - x0)) * max(0.0, float(y1 - y0))
    area_a = max(0.0, float(a[2] - a[0])) * max(0.0, float(a[3] - a[1]))
    area_b = max(0.0, float(b[2] - b[0])) * max(0.0, float(b[3] - b[1]))
    return intersection / max(area_a + area_b - intersection, 1e-9)


def nms(boxes: np.ndarray, scores: np.ndarray, threshold: float) -> list[int]:
    order = list(np.argsort(scores)[::-1])
    keep: list[int] = []
    while order:
        current = order.pop(0)
        keep.append(int(current))
        order = [idx for idx in order if box_iou(boxes[current], boxes[idx]) <= threshold]
    return keep


def move_inputs(inputs, device: str):
    return {key: value.to(device) if hasattr(value, "to") else value for key, value in inputs.items()}


def detect_people(image: Image.Image, device: str, box_threshold: float, text_threshold: float, nms_iou: float):
    import torch
    from transformers import AutoModelForZeroShotObjectDetection, AutoProcessor

    processor = AutoProcessor.from_pretrained(DETECTOR_ID)
    model = AutoModelForZeroShotObjectDetection.from_pretrained(DETECTOR_ID).to(device).eval()
    text_labels = [["person"]]
    inputs = processor(images=image, text=text_labels, return_tensors="pt")
    inputs = move_inputs(inputs, device)
    with torch.inference_mode():
        outputs = model(**inputs)
    result = processor.post_process_grounded_object_detection(
        outputs,
        inputs["input_ids"],
        threshold=box_threshold,
        text_threshold=text_threshold,
        target_sizes=[image.size[::-1]],
        text_labels=text_labels,
    )[0]
    boxes = result["boxes"].detach().float().cpu().numpy()
    scores = result["scores"].detach().float().cpu().numpy()
    if boxes.size == 0:
        return np.empty((0, 4), dtype=np.float32), np.empty((0,), dtype=np.float32)
    selected = nms(boxes, scores, nms_iou)
    boxes, scores = boxes[selected], scores[selected]
    # Stable human-readable instance ids: left-to-right by box center.
    order = np.argsort((boxes[:, 0] + boxes[:, 2]) / 2.0)
    return boxes[order], scores[order]


def detect_people_maskrcnn(image: Image.Image, device: str, score_threshold: float):
    import torch
    from torchvision.models.detection import MaskRCNN_ResNet50_FPN_V2_Weights, maskrcnn_resnet50_fpn_v2

    weights = MaskRCNN_ResNet50_FPN_V2_Weights.DEFAULT
    model = maskrcnn_resnet50_fpn_v2(weights=weights).to(device).eval()
    tensor = weights.transforms()(image).to(device)
    with torch.inference_mode():
        result = model([tensor])[0]
    keep = (result["labels"] == 1) & (result["scores"] >= score_threshold)
    boxes = result["boxes"][keep].detach().float().cpu().numpy()
    scores = result["scores"][keep].detach().float().cpu().numpy()
    masks = result["masks"][keep, 0].detach().float().cpu().numpy()
    if boxes.size == 0:
        return (
            np.empty((0, 4), dtype=np.float32),
            np.empty((0,), dtype=np.float32),
            np.empty((0, image.height, image.width), dtype=np.float32),
        )
    order = np.argsort((boxes[:, 0] + boxes[:, 2]) / 2.0)
    return boxes[order], scores[order], masks[order]


def segment_instances(image: Image.Image, boxes: np.ndarray, device: str):
    import torch
    from transformers import Sam2Model, Sam2Processor

    processor = Sam2Processor.from_pretrained(SEGMENTER_ID)
    model = Sam2Model.from_pretrained(SEGMENTER_ID).to(device).eval()
    input_boxes = [[box.tolist() for box in boxes]]
    inputs = processor(images=image, input_boxes=input_boxes, return_tensors="pt")
    inputs = move_inputs(inputs, device)
    with torch.inference_mode():
        outputs = model(**inputs, multimask_output=True)
    masks = processor.post_process_masks(
        outputs.pred_masks.detach().float().cpu(),
        inputs["original_sizes"].detach().cpu(),
        binarize=False,
    )[0]
    scores = outputs.iou_scores.detach().float().cpu()[0]
    if masks.ndim == 3:
        masks = masks[:, None, :, :]
    selected_masks = []
    selected_scores = []
    for index in range(masks.shape[0]):
        best = int(torch.argmax(scores[index]).item())
        logits = masks[index, best]
        selected_masks.append(torch.sigmoid(logits).numpy())
        selected_scores.append(float(scores[index, best].item()))
    return np.stack(selected_masks), selected_scores


def make_rgba(rgb: np.ndarray, alpha: np.ndarray) -> Image.Image:
    return Image.fromarray(np.dstack((rgb, alpha.astype(np.uint8))), "RGBA")


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


def draw_detection_overlay(image: Image.Image, boxes: np.ndarray, scores: np.ndarray) -> Image.Image:
    overlay = image.copy()
    draw = ImageDraw.Draw(overlay)
    colors = ["#ff3b30", "#ff9500", "#ffcc00", "#34c759", "#007aff", "#af52de", "#ff2d55"]
    for index, (box, score) in enumerate(zip(boxes, scores), start=1):
        color = colors[(index - 1) % len(colors)]
        draw.rectangle(tuple(float(v) for v in box), outline=color, width=4)
        draw.text((float(box[0]) + 4, float(box[1]) + 4), f"P{index} {score:.3f}", fill=color, stroke_width=2, stroke_fill="white")
    return overlay


def main() -> None:
    args = parse_args()
    if not args.source.is_file():
        raise SystemExit(f"Source does not exist: {args.source}")
    if args.constraint_radius < 0 or args.constraint_radius > 3:
        raise SystemExit("--constraint-radius must be between 0 and 3 pixels")
    args.output_dir.mkdir(parents=True, exist_ok=True)
    instances_dir = args.output_dir / "instances"
    instances_dir.mkdir(exist_ok=True)

    source_bytes = args.source.read_bytes()
    source = Image.open(args.source).convert("RGB")
    rgb = np.asarray(source, dtype=np.uint8)
    device = choose_device(args.device)

    started = time.perf_counter()
    if args.detector == "maskrcnn":
        boxes, detector_scores, detector_masks = detect_people_maskrcnn(
            source, device, args.person_score_threshold
        )
        detector_id = INSTANCE_DETECTOR_ID
    else:
        boxes, detector_scores = detect_people(
            source, device, args.box_threshold, args.text_threshold, args.nms_iou
        )
        detector_masks = None
        detector_id = DETECTOR_ID
    detection_seconds = time.perf_counter() - started
    if len(boxes) == 0:
        raise SystemExit("No people detected")

    started = time.perf_counter()
    if args.instance_segmenter == "detector-mask":
        if detector_masks is None:
            raise SystemExit("detector-mask requires --detector maskrcnn")
        instance_probabilities = detector_masks
        instance_scores = [None] * len(boxes)
        segmenter_id = INSTANCE_DETECTOR_ID
    else:
        instance_probabilities, instance_scores = segment_instances(source, boxes, device)
        segmenter_id = SEGMENTER_ID
    segmentation_seconds = time.perf_counter() - started

    records = []
    binary_instances = []
    for index, (box, detector_score, probability, instance_score) in enumerate(
        zip(boxes, detector_scores, instance_probabilities, instance_scores), start=1
    ):
        binary = probability >= 0.5
        binary_instances.append(binary)
        alpha = np.clip(probability * 255.0, 0, 255).astype(np.uint8)
        stem = f"person-{index:02d}"
        mask_path = instances_dir / f"{stem}-mask.png"
        rgba_path = instances_dir / f"{stem}-rgba.png"
        Image.fromarray(alpha, "L").save(mask_path)
        make_rgba(rgb, alpha).save(rgba_path)
        records.append(
            {
                "id": stem,
                "box_xyxy": [round(float(value), 2) for value in box],
                "detector_score": round(float(detector_score), 6),
                "sam_iou_score": None if instance_score is None else round(float(instance_score), 6),
                "foreground_fraction_at_0_5": round(float(binary.mean()), 6),
                "mask": str(mask_path.relative_to(args.output_dir)),
                "rgba": str(rgba_path.relative_to(args.output_dir)),
            }
        )

    union_binary = np.max(instance_probabilities, axis=0) >= args.instance_support_threshold
    union_soft = np.max(instance_probabilities, axis=0)
    union_alpha = np.clip(union_soft * 255.0, 0, 255).astype(np.uint8)
    union_mask_path = args.output_dir / "union-instance-alpha.png"
    union_rgba_path = args.output_dir / "union-instance-rgba.png"
    Image.fromarray(union_alpha, "L").save(union_mask_path)
    union_rgba = make_rgba(rgb, union_alpha)
    union_rgba.save(union_rgba_path)
    checker_preview(union_rgba).save(args.output_dir / "union-checker-preview.png")
    draw_detection_overlay(source, boxes, detector_scores).save(args.output_dir / "detections.png")

    refined = None
    if args.birefnet_alpha:
        if not args.birefnet_alpha.is_file():
            raise SystemExit(f"BiRefNet alpha does not exist: {args.birefnet_alpha}")
        birefnet = Image.open(args.birefnet_alpha).convert("L")
        if birefnet.size != source.size:
            raise SystemExit("BiRefNet alpha dimensions do not match the source")
        constraint = Image.fromarray((union_binary * 255).astype(np.uint8), "L")
        if args.constraint_radius:
            constraint = constraint.filter(ImageFilter.MaxFilter(args.constraint_radius * 2 + 1))
        constraint_array = np.asarray(constraint, dtype=np.float32) / 255.0
        birefnet_array = np.asarray(birefnet, dtype=np.float32) / 255.0
        refined = np.clip(birefnet_array * constraint_array * 255.0, 0, 255).astype(np.uint8)
        Image.fromarray(refined, "L").save(args.output_dir / "refined-alpha.png")
        refined_rgba = make_rgba(rgb, refined)
        refined_rgba.save(args.output_dir / "refined-people-rgba.png")
        checker_preview(refined_rgba).save(args.output_dir / "refined-checker-preview.png")

    count_passed = args.expected_count is None or len(records) == args.expected_count
    roundtrip = np.asarray(Image.open(union_rgba_path).convert("RGBA"), dtype=np.uint8)
    rgb_lock = bool(np.array_equal(roundtrip[:, :, :3], rgb))
    manifest = {
        "phase": 2,
        "experimental": True,
        "source": str(args.source.resolve()),
        "source_sha256": hashlib.sha256(source_bytes).hexdigest(),
        "width": source.width,
        "height": source.height,
        "device": device,
        "detector": detector_id,
        "detector_kind": args.detector,
        "person_score_threshold": args.person_score_threshold if args.detector == "maskrcnn" else None,
        "segmenter": segmenter_id,
        "instance_segmenter_kind": args.instance_segmenter,
        "box_threshold": args.box_threshold,
        "text_threshold": args.text_threshold,
        "nms_iou": args.nms_iou,
        "expected_count": args.expected_count,
        "detected_count": len(records),
        "count_gate_passed": count_passed,
        "rgb_lock_passed": rgb_lock,
        "detection_seconds": round(detection_seconds, 3),
        "segmentation_seconds": round(segmentation_seconds, 3),
        "platform": platform.platform(),
        "constraint_radius_pixels": args.constraint_radius if refined is not None else None,
        "instance_support_threshold": args.instance_support_threshold,
        "instances": records,
        "union_foreground_fraction_at_0_5": round(float(union_binary.mean()), 6),
        "refined_foreground_fraction_at_0_5": None if refined is None else round(float((refined >= 128).mean()), 6),
        "manual_review_required": True,
    }
    (args.output_dir / "instances.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    if not rgb_lock:
        raise SystemExit("RGB pixel lock failed")
    if not count_passed:
        raise SystemExit(f"Count gate failed: expected {args.expected_count}, detected {len(records)}")
    print(json.dumps(manifest, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
