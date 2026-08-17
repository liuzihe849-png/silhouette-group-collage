# Tight silhouette edge refinement

The silhouette must fully cover the selected person while staying visually close to the true source boundary. Depth is useful but is not the primary extraction method.

## Evidence priority

Use boundary evidence in this order:

1. Instance-level person or object segmentation.
2. Alpha matting for hair, fingers, fabric fringe, phones, shoes, and translucent edges.
3. Source colour and luminance edges inside a narrow uncertain band.
4. Depth discontinuity to resolve person-background and foreground-background overlap.
5. Manual contour correction when automated evidence conflicts.

Do not treat a smooth depth map as an exact hair or clothing boundary. It often merges nearby faces, hands, phones, dark clothing, and background foliage.

## Single design-mask workflow

1. Start from the reviewed source-resolution Alpha produced by `$human-cutout-engine`; include every visible person, protected held object, and necessary foreground occluder.
2. Keep people separate until interaction and depth order are verified. Merge only genuinely touching people or deliberate small clusters.
3. Define an uncertain edge band roughly 6–16 source pixels wide around the accepted mask only when manual review identifies a local defect. Refine only this band using matting, colour edges, and depth discontinuity; never re-estimate the full subject boundary.
4. Preserve intentional holes and negative spaces between arms, legs, torsos, phones, and neighbouring people.
5. Convert the refined alpha into one binary design mask after the final coupled photo transform is known.
6. Add a final outward safety edge of 1–3 pixels at output size, or at most 0.3% of the output short edge, whichever is smaller. Use a round or hand-cut contour, never a coarse block filter.
7. Use this exact same design mask for the opaque upper state and photographic lower aperture. Do not create separate expanded and tight reciprocal shapes.

## Quantitative checks

Compare protected person mask `P` with design colour mask `C`:

- coverage: `area(P ∩ C) / area(P) >= 0.995`, preferably `1.000`;
- maximum excess ratio: `area(C - P) / area(P) <= 0.08` for separate silhouettes;
- maximum excess ratio: up to `0.15` for a connected cluster with intentional narrow bridges;
- no isolated colour islands unless they correspond to a source-visible object or a deliberate star outside the mask system.

Treat these as diagnostics. Face-level visual review overrides a numerical pass. A visible exposed fragment or a bulky halo fails immediately.

## Failure correction

- **Person exposed:** restore the missing local contour or expand only the affected edge segment.
- **Mask looks swollen:** return to the refined alpha; remove broad dilation and inspect excess ratio.
- **Adjacent people merged:** restore the source negative gap or split them into separate silhouette islands.
- **Hair or fingers look blocky:** refine the local edge band with matting and colour evidence; do not expand the entire mask.
- **Depth boundary conflicts with source pixels:** trust instance mask, matting, and visible source edge before depth.
