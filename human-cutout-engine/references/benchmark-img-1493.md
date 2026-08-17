# Phase 1 benchmark: IMG_1493

Source: six overlapping people outdoors, one edge-cropped subject, raised legs, hats, fingers, a phone, black queue ropes, posts, and dense plants.

## Results

### BiRefNet HR Matting

- Best retention of all six people, hair, fingers, footwear, phone, and long skirt.
- Preserved source RGB pixels exactly.
- False positives: black queue ropes, small post fragments, and translucent ground/edge residue.
- Verdict: strongest candidate, but fails clean person-only extraction on this test.

### BiRefNet Portrait

- Preserved all six people and major identity anchors.
- Retained more queue-post structure and produced a harder matte than HR Matting.
- Verdict: does not improve the principal false-positive failure.

### rembg U2Net Human

- Excluded more of the queue barrier.
- Lost major limbs, footwear, lower bodies, and much of the right subject.
- Verdict: unacceptable for protected-person compositing.

## Phase 1 decision

Do not connect any tested backend directly to `silhouette-group-collage`. BiRefNet HR Matting is the best alpha refiner, but it needs an instance-level person constraint before it can become a reliable people-only mask. The next experimental stage should obtain per-person masks first, then use BiRefNet only to refine edges within those masks.
