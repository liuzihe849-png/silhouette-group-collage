# Human Cutout Engine handoff

Use `$human-cutout-engine` as the required person-extraction stage before building a reciprocal collage.

## Required inputs

Accept one reviewed Human Cutout Engine candidate containing:

- the unchanged source photograph;
- a source-resolution soft Alpha mask;
- a transparent RGBA cutout whose RGB channels are byte-identical to the source;
- the matching `manifest.json` or `instances.json`;
- a checkerboard preview reviewed at 200%.

Prefer the reviewed phase-2 `refined-alpha.png` and `refined-people-rgba.png` for groups, overlaps, edge crops, small background people, and foreground occlusion. Accept phase 1 only when every visible person and protected object passes manual review.

## Acceptance gate

Before art direction, run:

```bash
python scripts/validate_cutout_handoff.py \
  --source SOURCE \
  --alpha HUMAN_ALPHA \
  --rgba HUMAN_RGBA \
  --manifest HUMAN_MANIFEST \
  --expected-count COUNT
```

Continue only when the report confirms:

- identical source, Alpha, and RGBA dimensions;
- exact source-to-RGBA RGB lock;
- exact Alpha-to-RGBA Alpha agreement;
- non-empty subject coverage;
- `rgb_lock_passed: true` in the manifest;
- `count_gate_passed: true` and matching counts when instance metadata exists.

The numerical gate does not replace visual review. Reject missing hair, fingers, shoes, phones, held objects, companions, or count-defining gaps.

## Foreground occlusion policy

Treat the accepted subject as `people + necessary foreground context`.

- Retain the smallest coherent portion of a rope, railing, table, chair, branch, prop, pet, or other object that visibly crosses, supports, frames, or connects the people.
- Remove detached background residue that does not contribute to body continuity, pose readability, group rhythm, or the future silhouette.
- Do not require a clinically context-free people-only matte.
- Do not run optional foreground removal unless the object is aesthetically harmful and the user or art-direction review explicitly approves removal.

## Coupled reciprocal use

Derive all downstream person geometry from the accepted Alpha:

1. Preserve the soft Alpha and RGBA as the protected photographic subject layer.
2. Transform the complete photograph, Alpha, and RGBA together with one crop, translation, and uniform scale.
3. Convert the transformed Alpha into one tight design mask, adding only the allowed 1–3 output-pixel hand-cut safety edge.
4. Use that exact design mask as the opaque shape in one panel and the photographic aperture in the other.
5. Composite the transformed protected RGBA back into every visible-photo state without generative repainting.

Never ask image generation to estimate the people boundary again after the handoff passes.
