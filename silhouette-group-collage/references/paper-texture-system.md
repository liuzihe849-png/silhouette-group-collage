# Five quiet paper texture system

The paper field must feel scanned and tactile without competing with the photograph, silhouettes, or seam phrase. The five assets below are procedural, tintable reconstructions of the supplied material references. They contain no copied reference pixels and no decorative stars.

## Profiles

- **soft-fibre-paper** — fine, randomly oriented short paper fibres with gentle micro-grain. Default for blue, blue-gray, smoke, snow, and quiet diary scenes.
- **fine-matte-grain** — close, even, non-glossy paper tooth. Use for red, plum, green, teal, and large fields where the colour should remain visually calm.
- **sparse-light-fleck** — a mostly clean field with a few pale paper crumbs and short pale scratches. Use for warm, light, yellow, orange, and softly aged layouts.
- **sparse-dark-fleck** — the cleanest field, punctuated by very sparse dark ink flecks. Use for linen, butter-yellow, minimal layouts, and generous negative space.
- **medium-light-fleck** — restrained but clearly visible pale paper dust with varied fleck sizes. Use for sea, sky, summer, travel, or when a little more analogue wear is useful.

## Selection

1. Start with the profile suggested by `scripts/select_scene_palette.py`.
2. Compare it with one quieter neighbouring profile at final output size.
3. Prefer `soft-fibre-paper` or `fine-matte-grain` when the group already occupies much of the frame.
4. Use the three fleck profiles only when their particle direction supports the scene; never stack profiles.
5. Keep all profiles subordinate to protected source pixels and the reciprocal silhouette structure.

## Non-negotiable visual rules

- No cloud-like light/dark patches or broad mottled stains.
- No artificial folds, crease shadows, fabric weave, canvas pattern, or wool texture.
- No glossy digital noise, embossed grain, gradients, or repeated tile seams.
- No star, doodle, or lettering baked into a paper texture. Decorations are separate layers.
- Do not turn the paper field into a distressed overlay. The material is quiet; the silhouettes and phrase carry the graphic emphasis.

## Deterministic use

Build assets with:

```bash
python3 scripts/build_paper_texture_library.py
```

Tint one selected profile with:

```bash
python3 scripts/apply_paper_texture.py \
  --profile fine-matte-grain \
  --colour '#C9543F' \
  --width 1080 \
  --height 960 \
  --output outputs/paper-field.png
```

The output manifest must report both `profile_gate_passed: true` and `texture_gate_passed: true`. Inspect at 100% and 200% zoom; if the profile reads as a filter before it reads as paper, choose a quieter profile or reduce strength.
