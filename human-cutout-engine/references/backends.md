# Phase 1 backend selection

## Preferred: BiRefNet HR Matting

- Model: `ZhengPeng7/BiRefNet_HR-matting`
- Purpose: 2048-pixel high-resolution soft alpha matting.
- License: MIT on the official model card and code repository.
- Use as the strongest phase-1 candidate when edge fidelity matters. It can still retain salient non-person objects and must pass manual review.
- Cost: about 0.2B parameters; first use downloads a large checkpoint and uses substantial memory.

Install in an isolated environment:

```bash
python3 -m venv .venv
.venv/bin/pip install torch torchvision transformers pillow numpy safetensors einops kornia timm
```

## Comparison: BiRefNet Portrait

- Model: `ZhengPeng7/BiRefNet-portrait`
- Purpose: portrait-specific 1024-pixel soft alpha matting.
- Use as the main comparison against HR Matting.

## Lightweight baseline: rembg U2Net Human

- Runtime: `rembg`
- Model: `u2net_human_seg`
- Purpose: fast human segmentation baseline.
- Install: `.venv/bin/pip install "rembg[cpu]"`
- Do not confuse the MIT license of the `rembg` runner with the license of every optional model it can download.

## Experimental instance stage

- Default detector and coarse instance support: torchvision Mask R-CNN ResNet-50 FPN v2 with COCO weights.
- Edge refiner: BiRefNet HR Matting, restricted by the instance support rather than used as an unconstrained person detector.
- Tested comparison: Grounding DINO Tiny plus SAM2.1 Hiera Small. On `IMG_1493`, Grounding DINO merged overlapping people into five boxes and SAM2 produced excessive holes. Keep this path optional until a future benchmark improves it.
- Mask R-CNN is BSD-licensed through torchvision; SAM2.1 is Apache-2.0. Re-check all licenses before a commercial public release.
- The model checkpoint remains outside the skill folder under the standard PyTorch cache.

## Model safety

- Pin model IDs and record them in `manifest.json`.
- Do not bundle checkpoints in the public skill repository.
- Do not default to BRIA RMBG weights for a commercial workflow without a separate commercial license review.
- Re-check model-card licenses before publishing a commercial release.
