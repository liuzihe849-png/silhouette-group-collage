# Adaptive layout for every source photo

Never reject a source because people occupy too much or too little of the frame. Person occupancy selects a layout strategy; it is not an admission threshold.

## Coupled-transform invariant

`LAYOUT INVARIANT: the complete source photograph and every reciprocal person mask share the same scale, translation, crop, and inset transform. Never resize, crop, or reposition a mask independently from the photograph.`

If a colour block becomes too large, change panel composition, group masks, or the coupled photo-plus-mask scale. Never expose part of a person to reduce colour area.

## Estimate occupancy

Estimate the union of all visible person regions as a percentage of the source frame. Use a segmentation mask when available; otherwise make a careful visual estimate. The ranges below are routing guidance, not refusal rules.

### Mode A: environment-led

Typical source occupancy: about 5–35%.

- Let the photograph occupy most of the photo panel.
- Preserve landscape, architecture, water, snow, road, sky, room, or other meaningful environment.
- Aim for people to occupy roughly 18–32% of a single output panel when the source naturally supports it.
- Use a horizontal paper-doll chain or separate related silhouettes according to depth.

### Mode B: balanced group

Typical source occupancy: about 35–60%.

- Keep the entire source photograph intact and uniformly scale it within the panel when more breathing room is needed.
- Use a visible paper margin or asymmetrical photo window instead of blurring or extending the photo.
- Prefer separate silhouettes or two to three logical clusters when one connected mass would become heavy.
- Aim for roughly 22–38% person occupancy in a single output panel when achievable without making identity anchors too small.

### Mode C: portrait-dense or selfie

Typical source occupancy: about 60–95%, including edge-cropped faces and bodies.

- Accept and process the photo.
- Uniformly reduce the complete photograph and all masks together into a large hand-cut photo window on paper. Paper becomes the quiet environment when the source contains little environmental context.
- Use individual silhouettes or small touching clusters. Do not merge separated heads into one broad slab.
- Preserve source-edge crops intentionally; never invent missing heads, shoulders, arms, or bodies.
- Keep each opaque silhouette large enough to cover its complete visible source region. If the combined colour mass is heavy, distribute the masks as separate islands and increase surrounding paper space.
- Target approximately 25–45% person occupancy in a single output panel after the coupled inset transform. Treat this as a soft composition target, never as permission to cut a mask.

## Priority order when constraints conflict

1. Complete person coverage and protected source pixels.
2. Coupled photo-and-mask geometry.
3. Recognisable reciprocal mask exchange.
4. Person count, pose rhythm, interactions, and objects.
5. Overall colour-field proportion.
6. Typography and decoration.

Higher priorities may never be sacrificed to satisfy lower priorities.

## Coverage test

For each opaque state, compare the intended person mask `P` with the final colour mask `C` after both use the same transform.

- Required coverage: `area(P ∩ C) / area(P) >= 0.995`.
- Preferred coverage: `1.000`.
- Default excess ratio: `area(C - P) / area(P) <= 0.08` for separate silhouettes and up to `0.15` for intentional connected clusters.
- Expand only the affected contour segment by a 1–3 output-pixel hand-cut safety margin when uncertain.
- Never erode the colour mask to satisfy a maximum-area rule.

Use `scripts/check_mask_coverage.py` when deterministic masks are available. Any exposed facial or body fragment fails visually even if the numerical threshold passes.
