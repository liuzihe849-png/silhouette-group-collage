---
name: human-cutout-engine
description: Extract people and compositionally necessary foreground occluders from user-supplied photos into source-resolution soft alpha masks and transparent RGBA PNGs while preserving retained RGB pixels exactly. Use for 人像抠图, 群像抠图, 人物透明底 PNG, alpha mask, matting, background removal, protected-person compositing, or as a deterministic preprocessing step before collage and image-generation skills. Retain foreground objects when deleting them would damage group continuity or the future silhouette.
---

# Human Cutout Engine

Produce deterministic cutout assets before any generative editing. Phase 1 outputs a union matte candidate. Experimental phase 2 detects and records each person separately, then constrains the BiRefNet HR matte with those instance masks. Preserve foreground props that visibly occlude or connect the group when removing them would damage compositional continuity. Do not alter the source image or call an image generator.

## Workflow

1. Inspect the source and count visible people. Record hair, hands, shoes, held objects, overlaps, edge crops, foreground occluders, and background regions likely to confuse a matting model.
2. Read `references/backends.md` and `references/benchmark-img-1493.md`, then select a backend:
   - Prefer `birefnet-hr` as the strongest phase-1 candidate, not as an automatically accepted final matte.
   - Use `birefnet-portrait` as a faster comparison candidate.
   - Use `rembg-u2net-human` only as a lightweight baseline.
3. Run `python scripts/extract_people.py SOURCE --output-dir OUTPUT --backend birefnet-hr`.
4. Inspect `alpha.png`, `people-rgba.png`, `checker-preview.png`, and `manifest.json` at 200% zoom.
5. Reject the result if any person, limb, hair edge, footwear, phone, or held object is missing; if obvious background remains; or if gaps between people collapse.
6. Compare candidate runs with `python scripts/compare_cutouts.py SOURCE --run hr=OUTPUT_HR --run baseline=OUTPUT_BASELINE --output comparison.png`.
7. Do not connect this skill to a downstream visual skill until a real-photo comparison passes manual review.

## Experimental phase 2

Read `references/benchmark-phase2-img-1493.md` before running this stage.

1. Generate the accepted BiRefNet HR phase-1 alpha first.
2. Run `python scripts/extract_person_instances.py SOURCE --output-dir OUTPUT --birefnet-alpha PHASE1_ALPHA --expected-count COUNT`.
3. Require `count_gate_passed: true` and inspect every file under `instances/` rather than judging only the union preview.
4. Prefer the default Mask R-CNN detector masks as the instance support. The tested Grounding DINO boxes merged overlapping people, and SAM2 introduced holes in this benchmark; both remain comparison paths, not defaults.
5. Review `refined-checker-preview.png` for thin objects. Remove detached background residue, but retain real foreground objects where they cross, frame, support, or visually connect the people. Do not optimize for a context-free person-only matte at the expense of group wholeness.
6. Build the audit sheet with `python scripts/compare_phase2.py --source SOURCE --phase1 PHASE1_PREVIEW --phase2-dir OUTPUT --output COMPARISON`.
7. Hand phase 2 to `silhouette-group-collage` only after count, RGB lock, subject-layer continuity, detached-background-residue, and 200% manual-review gates pass. Keep failed or unreviewed candidates disconnected.

## Diagnostic phase 2.1: optional foreground removal

Read `references/benchmark-phase2.1-img-1493.md` when a thin foreground object such as a rope or rail remains across the people.

1. Do not run this stage by default. A foreground rope, railing, table edge, chair, prop, or branch may belong to the subject layer when it establishes the original occlusion relationship or strengthens the future silhouette.
2. Run this diagnostic only after an explicit aesthetic decision that the object is harmful residue rather than meaningful foreground context.
3. Treat open-vocabulary detections only as candidate regions. Never subtract a broad text-detection box from the person Alpha.
4. Inspect all three SAM2 candidate masks for each region and approve the variant that isolates the occluder without selecting body or clothing.
5. Run `python scripts/remove_foreground_occluders.py SOURCE --input-alpha INPUT_ALPHA --output-dir OUTPUT --box X0,Y0,X1,Y1 --variant-index INDEX --confirm-remove-foreground-occluders` with one `--box` per approved region.
6. Require both `rgb_lock_passed: true` and `removal_gate_passed: true`. The default gate fails when approved masks remove more than 3% of the input subject foreground.
7. Compare the retained-context and removed-context versions. Reject removal when transparent gaps weaken anatomy, pose readability, group rhythm, or silhouette continuity, even if the negative-object Mask is technically accurate.
8. Keep this stage manual-review-only. Do not auto-select a SAM2 variant or silently apply a detected negative object.

## Foreground occlusion decision

Apply this order before deleting any foreground object:

1. Keep the object where it visibly crosses, supports, frames, or connects a person or the group.
2. Keep the smallest coherent local segment needed to preserve the original occlusion relationship; do not retain unrelated extensions across the whole frame.
3. Remove only detached residue that does not contribute to anatomy, pose readability, group rhythm, or the future filled silhouette.
4. Judge the retained subject as the combined `people + necessary foreground context` layer. Do not require a clinically context-free person-only matte.
5. Use the retained Alpha directly when building the later silhouette so the positive and negative shapes preserve the same visual whole.

## Output contract

- `alpha.png`: source-resolution 8-bit soft alpha mask.
- `people-rgba.png`: source RGB pixels with the predicted alpha channel; RGB values must remain byte-identical to the source conversion.
- `checker-preview.png`: transparent cutout over a checkerboard for visual inspection.
- `manifest.json`: source hash, backend, model, dimensions, mask statistics, bounding box, and RGB-lock result.

Experimental phase-2 additions:

- `instances/person-NN-mask.png` and `instances/person-NN-rgba.png`: one auditable instance per detected person.
- `detections.png`: labeled person boxes and confidence scores.
- `union-instance-alpha.png`: union of the individual instance supports.
- `refined-alpha.png` and `refined-people-rgba.png`: BiRefNet HR alpha constrained by the instance support.
- `instances.json`: detector/segmenter IDs, thresholds, count gate, timing, instance records, and RGB lock.

Experimental phase-2.1 additions:

- `candidates/object-NN-variant-N.png`: all SAM2 candidate masks for review.
- `occluder-mask.png`: union of only the approved negative-object candidates.
- `cleaned-alpha.png` and `cleaned-people-rgba.png`: source RGB with approved occluders subtracted from Alpha.
- `occluder-manifest.json`: boxes, variants, scores, removal fraction, safety gate, and RGB lock.

## Hard requirements

- Preserve source width and height.
- Preserve original RGB pixels exactly; change only the alpha channel.
- Retain soft transparency around hair and semitransparent boundaries.
- Never repair missing anatomy with generation, dilation, painting, or content-aware fill.
- Preserve real occlusion relationships. Treat a foreground prop as part of the subject layer when deleting it fragments visible bodies or weakens the future silhouette.
- Prefer a coherent group-plus-context contour over a clinically isolated but visually broken person-only cutout.
- Never convert the final matte into a broad convex hull or bounding blob.
- Treat model output as a candidate requiring visual review, not as guaranteed truth.
- Keep model weights outside the skill folder and download them only when the selected backend is run.
- Keep phase 1 independent from `silhouette-group-collage`.

## Quality gate

Confirm all answers are yes before accepting a run:

1. Are the output dimensions identical to the source?
2. Does `manifest.json` report `rgb_lock_passed: true`?
3. Are all visible people included?
4. Are hair, fingers, shoes, phones, and major held objects retained?
5. Are detached plants, walls, sky, ground, and shadows excluded while meaningful foreground occluders remain where needed?
6. Are count-defining gaps and overlaps still readable?
7. Does the Alpha edge look natural at 200% without a large halo?
8. Does the subject layer remain visually whole enough to become an attractive filled silhouette?

## Delivery

Return the four output files, the chosen backend, runtime/device, quantitative mask statistics, and a concise manual review. State explicitly when the result is experimental or fails any quality gate.
