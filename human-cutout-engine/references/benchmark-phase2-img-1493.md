# Phase 2 benchmark: IMG_1493

## Goal

Create one mask per each of the six overlapping people and retain the source pixels. Remove detached plants, posts, and ground residue, while keeping limited rope segments where the foreground rope crosses the group and helps preserve the original visual continuity.

## Detector comparison

### Grounding DINO Tiny

- Detected five boxes at the tested thresholds.
- Several boxes merged adjacent people instead of defining one person each.
- Count gate failed: expected six, detected five.
- Verdict: rejected for this overlap-heavy photo.

### DETR ResNet-50 probe

- Returned many duplicate and group-spanning person boxes.
- NMS could force a count of six but did not yield six trustworthy individual boxes.
- Verdict: rejected rather than tuning the count artificially.

### Mask R-CNN ResNet-50 FPN v2

- At person confidence `0.9`, detected exactly six high-confidence boxes.
- Count gate passed and left-to-right instance records were generated.
- Instance masks were strong enough to define a coarse semantic support, although their raw soft edges were too broad for final delivery.
- Verdict: selected as the phase-2 detector and support mask.

## Refinement comparison

- SAM2.1 Hiera Small received the six Mask R-CNN boxes, but overlapping people produced excessive internal holes. It remains an optional comparison path.
- The selected refinement multiplies the source-resolution BiRefNet HR alpha by a Mask R-CNN semantic support thresholded at `0.2`, with a two-pixel safety radius.
- This preserves hair, faces, fingers, shoes, hats, the phone, and clothing better than a hard `0.5` instance threshold while removing most plants, ground, posts, and rope.

## Result

- Source size preserved: 1178 x 1165.
- Detected people: 6 of 6.
- RGB pixel lock: passed.
- Runtime on Apple MPS after weights were cached: roughly 3 seconds for Mask R-CNN plus the previously generated BiRefNet HR alpha.
- A few short queue-rope segments remain where the real foreground rope intersects feet and the long skirt. This is now intentional context retention rather than an automatic failure.

## Decision

The instance-count, protected-pixel, and group-continuity portions pass on this benchmark. Select the phase-2 retained-context output over the phase-2.1 rope-deletion output. Keep the phase experimental until it passes additional difficult photos; do not connect it to `silhouette-group-collage` or publish it as the production default yet.
