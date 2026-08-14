# Prompt recipes

## Master edit prompt

Replace bracketed variables. Keep the invariant sentence unchanged.

```text
Transform the supplied group photograph into a vertical [4:5 / 2:3] two-panel editorial paper collage. Preserve exactly [person count] people in their original left-to-right order, depth scale, poses, clothing, interactions, held objects, environmental anchors, and source-photo texture.

Build a reciprocal positive-negative mask composition from one continuous source image. In the upper panel, retain the photograph and cover every person with opaque [dominant colour] group silhouettes. In the lower panel, reverse figure and ground: use a broad flat [dominant colour / complementary paper colour] field and reveal the same photograph through apertures with matching silhouettes, scale, and positions. The same masks must visibly change from solid covers to photographic windows between panels.

Art direction: handmade cut-paper editorial collage, indie album artwork, youthful photo diary, imperfect scissor-cut contours, asymmetrical spacing, scanned uncoated paper, visible paper fibres, restrained dust, uneven ink density, slight registration drift, matte surface. Preserve the source photo's own grain, focus, exposure, motion blur, weather, and colour cast inside all photographic regions. Add 8–12 sparse handmade [secondary accent] stars. Place the exact scene-matched phrase "[phrase]" in loose lowercase handwriting across the middle seam, spelled exactly and secondary to the group.

INVARIANT: this is one photograph shown in two reciprocal mask states, not a scrapbook grid and not a collection of unrelated images.

Avoid generic sticker collage, extra photos, invented people or objects, glossy 3D, smooth gradients, polished vector geometry, perfect symmetry, thick sticker outlines, excessive decorations, illegible prominent text, anatomy changes, and loss of subject identity.
```

## Recipe A: organic silhouette / group memory

```text
Use one loose connected silhouette around the complete group. Upper panel: cut the group out from the photograph and place it on warm cream paper with sparse faded olive stars. Lower panel: return to the grassy photograph and cover the group with a matching warm-cream silhouette, allowing only a few intentional gaps. Add fine paper fibres, faded consumer-film colour, subtle photocopy grain, imperfect hand-cut edges, and quiet handwritten caption space. Keep faces, body count, pose, clothing, and group spacing recognisable. Avoid sticker outlines and precise vector tracing.
```

## Recipe B: staggered group in a landscape

```text
Count every person and preserve their true foreground/background scale. Upper panel: retain the landscape photograph and cover each person with a separate related paper silhouette at the same position. Lower panel: fill the panel with the paper colour and use those exact silhouettes as photographic apertures. Keep distant people small, preserve interactions and held objects, retain the source texture, add 8–12 restrained stars, and place one scene-matched handwritten phrase across the middle seam.
```

## Recipe C: horizontal group line

```text
Build one loose paper-doll chain from the complete horizontal group. Preserve the exact body count, order, spacing, raised arms, clothing lengths, and companion objects. Upper panel: overlay the chain on the source photo. Lower panel: turn the same chain into photo apertures inside a broad paper field. Retain lake, mountain, shore, or other horizontal environmental bands. Add 8–12 restrained stars and one readable scene-matched phrase at the seam.
```

## Recipe D: group plus companion object

```text
Use the appropriate group silhouette family plus one small mask for a visible thrown or held object. Preserve the object in both reciprocal states and keep its relationship to the correct person. Never invent a companion object. Retain source photo texture, handmade paper texture, restrained stars, and one exact handwritten seam phrase.
```

## Correction prompts

### Output looks like a generic scrapbook

```text
Remove tape, frames, stickers, extra photos, and unrelated decorations. Rebuild around one photograph repeated in two panels. Make the same mask switch clearly from opaque shape to photo aperture. Preserve the invariant sentence.
```

### Reciprocal effect is weak

```text
Match mask positions and contours more closely across both panels. Increase the flat colour area and make the upper opaque shapes visibly correspond to lower cutout windows. Do not change the subject or crop.
```

### Output looks too digital

```text
Replace perfect vector edges with irregular scissor-cut contours. Add subtle uncoated-paper fibres, uneven ink density, faded consumer-film colour, fine dust, and slight registration drift. Keep grain restrained and the surface matte.
```

### Subject is damaged

```text
Restore the source identity, body count, anatomy, pose, clothing, landmark geometry, and spatial relationships. Simplify the mask rather than altering the subject. Keep at least one unobstructed photographic view of every essential anchor.
```

### Person count or depth is wrong

```text
Return to the source and recount every person from left to right. Restore the exact count, order, scale, pose, clothing, interactions, held objects, and foreground/background depth. Do not enlarge distant people or merge separated figures. Preserve the invariant sentence.
```

### Texture, stars, or text is missing

```text
Restore the source photograph's original grain, focus, exposure, colour cast, weather, ground and background texture inside all photo regions. Add 8–12 sparse handmade stars across both panels. Add one clearly readable scene-matched lowercase handwritten phrase across the middle seam, spelled exactly as supplied. Keep all three elements subordinate to the reciprocal silhouettes.
```
