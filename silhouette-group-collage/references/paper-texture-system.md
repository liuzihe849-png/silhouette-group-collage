# Heirloom paper texture system

Read this file after colour selection and before rendering any opaque silhouette or large paper field. Paper material is selected independently from colour; one generic noise tile must not be reused mechanically across every artwork.

## Reference-derived parents

The supplied references establish two parent structures:

1. **Fine linen paper** — low contrast, warm matte stock, fine horizontal fibres, tiny paper grain, and faint vertical or horizontal fold memory. Use when quiet space, pale paper, or restrained archival softness matters.
2. **Field fibre paper** — visibly uneven dye, mixed coarse fibres, pale and dark paper flecks, sparse scratches, and a drier printed surface. Use when the colour block needs stronger physical presence.

The reusable assets are original deterministic neutral tiles derived from those material traits. They contain no stars, words, people, landscape pixels, or copied fragments from the references.

## Five profiles

- **heirloom-linen** — the quietest profile; fine horizontal fibres and restrained folds for linen, very-light paper, studio, and generous negative space.
- **field-fibre** — coarse mixed fibres and uneven dye for grass, garden, earthy midtones, and outdoor diary scenes.
- **hearth-smoke-stock** — balanced fine/coarse grain for smoke colours, blue-gray, snow, neutral city, and soft interior scenes.
- **sun-faded-stock** — moderate fibres, faded density drift, and small flecks for yellow, orange, sea travel, summer, and sunset.
- **winter-wool-stock** — dense matte fibres and brighter flecks that remain visible after tinting dark red, plum, pine, or night colours.

Profile definitions and gates live in `assets/design-system/paper-texture-profiles.json`. Neutral assets live under `assets/design-system/paper-textures/system/`.

## Selection order

1. Choose the scene colour token first with `select_scene_palette.py`.
2. Accept the suggested texture profile only after checking the full-page colour value and scene:
   - very-light or linen → `heirloom-linen`;
   - dark, dark-mid, or mid-dark → `winter-wool-stock`;
   - green or grass/garden → `field-fibre`;
   - yellow/orange or sunset → `sun-faded-stock`;
   - smoke, blue-gray, snow, or city neutral → `hearth-smoke-stock`.
3. Render with `apply_paper_texture.py --profile PROFILE` using the exact final mask.
4. Require both `texture_gate_passed: true` and `profile_gate_passed: true`.
5. Inspect at 100% and 200%. The texture must be visible in the silhouette and broad field, but cannot obscure the hand-cut contour.

## Material hierarchy

- Keep photographic grain and focus untouched inside photo regions and protected people.
- Apply paper material only inside opaque paper masks.
- Use the same selected profile for the reciprocal silhouette and its matching broad field unless a deliberate material contrast is recorded.
- Do not place texture as a semi-transparent filter over the whole artwork.
- Do not introduce stars, lettering, black outlines, photographed grass, or copied landscape fragments into a reusable tile.
- Do not make a dark paper smooth: use `winter-wool-stock` so fibre highlights survive tinting.
- Do not make a light paper dirty: use `heirloom-linen` and keep coarse flecks restrained.

## Failure conditions

Reject the material when it looks like flat vector colour, generic monochrome noise, concrete, fabric, leather, a photographic landscape crop, repeated decorations, or heavy grunge. Also reject obvious tile seams, repeated fold lines, crushed dark fibres, and universal texture applied across faces or clothing.
