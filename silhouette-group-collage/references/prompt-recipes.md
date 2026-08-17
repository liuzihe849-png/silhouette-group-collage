# Prompt recipes

## Master edit prompt

Replace bracketed variables. Keep the invariant sentence unchanged.

```text
Transform the supplied group photograph into a native vertical [4:5 / 2:3 / 9:16] two-panel editorial paper collage. Preserve exactly [person count] people in their original left-to-right order, depth scale, poses, clothing, interactions, held objects, environmental anchors, and source-photo texture. For 9:16, compose the artwork directly on the tall canvas; do not blur, mirror, stretch, or generatively extend the source photograph merely to fill height.

PERSON INVARIANT: every visible person must come directly from the supplied photograph; do not generate, repaint, reconstruct, beautify, relight, or reinterpret any face, hair, skin, hand, body, clothing, footwear, or held object.

LAYOUT INVARIANT: the complete source photograph and every reciprocal person mask share the same scale, translation, crop, and inset transform. Never resize, crop, or reposition a mask independently from the photograph. Accept the source at any person occupancy; select environment-led, balanced-group, or portrait-dense layout rather than refusing the photo.

EDGE INVARIANT: build one contour-tight design mask from instance segmentation and alpha matting, using depth only as auxiliary overlap evidence. Cover at least 99.5% of the protected person region while limiting excess mask area to 8% for separate silhouettes or 15% for intentional connected clusters. Add only a 1–3 output-pixel safety edge and reuse the exact same design mask in both panels.

Build a reciprocal positive-negative mask composition from one continuous source image. In the upper panel, retain the photograph and cover every selected person completely with opaque [dominant colour] silhouettes, including every visible face, hair edge, neck, hand, body, garment, shoe, phone, and held object. In the lower panel, reverse figure and ground: use a broad flat [dominant colour / complementary paper colour] field and reveal the same photograph through apertures with matching silhouettes, scale, and positions. The same masks must visibly change from solid covers to photographic windows between panels. Preserve count-defining negative spaces between heads, shoulders, raised arms, lifted legs, phones, joined hands, and companion objects. A connected silhouette must follow the group like a paper-doll chain; it must not become a convex hull, rectangular slab, giant flower blob, saw-tooth band, or broad envelope filled with accidental background. If the colour mass is too large, use separate mask islands or uniformly inset the full photograph and every mask together; never shrink a mask alone.

Art direction: handmade cut-paper editorial collage, indie album artwork, youthful photo diary, imperfect scissor-cut contours, asymmetrical spacing, scanned uncoated paper, visible paper fibres, restrained dust, uneven ink density, slight registration drift, matte surface. Preserve the source photo's own grain, focus, exposure, motion blur, weather, and colour cast inside all photographic regions. Add 8–12 sparse handmade [secondary accent] stars in three size tiers with irregular spacing. Place the exact scene-matched phrase "[phrase]" in [brush diary / chunky marker / loose pencil] handwriting across the middle seam, spelled exactly. Make the phrase a visible compositional bridge spanning roughly 62–90% of the canvas width. Use controlled word-to-word variation: at most two related handwriting faces, scale variation, slight -4° to +4° rotation, irregular baseline, and one optional underline or motion mark. Do not render a tiny uniform digital caption.

INVARIANT: this is one photograph shown in two reciprocal mask states, not a scrapbook grid and not a collection of unrelated images.

Build the paper layout and non-person content separately, then restore the protected original person pixels in every visible photographic state. If the workflow cannot restore original person pixels, stop instead of delivering generated faces.

Avoid generic sticker collage, extra photos, invented people or objects, glossy 3D, smooth gradients, polished vector geometry, perfect symmetry, thin contrasting mask outlines, thick sticker outlines, excessive decorations, tiny centred text, one unchanged font across unrelated images, arbitrary default colours, anatomy changes, and loss of subject identity.
```

## Mandatory pre-prompt decisions

Write these decisions before calling an image tool:

```text
Source diagnosis: [group geometry], [energy], [environmental anchor], [quiet zones]
Person occupancy: [estimated percentage]
Adaptive layout: [environment-led / balanced group / portrait-dense] with coupled photo-plus-mask transform
Mask family: [family] because [pose/spacing reason]
Palette candidates:
1. Echo: [dominant / accent / neutral]
2. Counterpoint: [dominant / accent / neutral]
3. Atmosphere: [dominant / accent / neutral]
Chosen palette: [candidate] because [contrast + mood + source anchor]
Phrase: "[exact 3–6 word phrase]"
Lettering: [brush diary / chunky marker / loose pencil], key word [word], controlled word-level variation
Person lock: [deterministic mask/composite method]
Coverage check: [target 100%, required >=99.5%]
Excess check: [<=8% separate / <=15% connected]
```

Do not generate until every line is resolved.

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

### Mask became a giant blob

```text
Discard the enclosing blob, convex hull, saw-tooth slab, or broad group envelope. Retrace the paper-doll rhythm of the actual people. Preserve every head peak, shoulder break, extended arm, lifted leg, phone, joined hand, companion object, and large negative gap. Use only narrow bridges where bodies genuinely touch. Keep accidental background leakage out of the lower apertures. Do not add a contrasting outline around the mask.
```

### Mask leaves part of a person exposed

```text
Restore complete opaque coverage of every selected person, including visible face, mouth, hair, ear, neck, hand, body, clothing, footwear, phone, and held object. Expand or correct the mask outward; never erode or independently shrink it to reduce colour area. Keep the photograph and mask on the same coupled transform. If the colour mass remains heavy, uniformly inset the complete source photograph and all masks together or divide the group into separate related silhouette islands. Required deterministic coverage is at least 99.5%, with 100% preferred.
```

### Mask is complete but looks swollen

```text
Return to the source-resolution person alpha and remove broad dilation. Refine only the local 6–16 pixel uncertain boundary band using instance segmentation, alpha matting, visible colour edges, and depth discontinuity as auxiliary evidence. Add only a 1–3 output-pixel safety edge. Keep coverage at least 99.5% while reducing area(C-P)/area(P) to 8% or less for separate silhouettes, or 15% or less for intentional connected clusters. Reuse the corrected exact mask in both reciprocal states.
```

### Typography looks generic

```text
Remove the tiny uniform caption and rebuild the exact phrase as a major seam element spanning 62–90% of the canvas width. Choose one scene-matched handwriting family. Vary scale, tilt, baseline, spacing, and stroke density by word within a coherent range; use at most two related handwriting faces and one optional underline or motion mark. Keep spelling exact. Do not use a default sans/serif font or identical treatment from another image.
```

### Palette feels arbitrary or ugly

```text
Return to the source and compare three palette candidates: one echoing a distinctive garment/object, one muted complementary counterpoint to the environment, and one matching the scene's emotional temperature. Choose the strongest silhouette-to-photo contrast with restrained saturation. Use one dominant paper colour, one supporting accent, and cream or charcoal. Do not reuse a default teal, vermilion, magenta, or beige template.
```

### Subject is damaged

```text
Restore the source identity, body count, anatomy, pose, clothing, landmark geometry, and spatial relationships. Simplify the mask rather than altering the subject. Keep at least one unobstructed photographic view of every essential anchor.
```

### Face or person details changed

```text
Do not attempt another generative portrait correction. Restore the protected person regions directly from the supplied source photograph, including original face, eyes, nose, mouth, hair, skin, hands, body, clothing, footwear, and held objects. Keep the generated paper, mask, environment, stars, and typography outside those protected regions unchanged. PERSON INVARIANT: every visible person must come directly from the supplied photograph; do not generate, repaint, reconstruct, beautify, relight, or reinterpret any face, hair, skin, hand, body, clothing, footwear, or held object.
```

### Person count or depth is wrong

```text
Return to the source and recount every person from left to right. Restore the exact count, order, scale, pose, clothing, interactions, held objects, and foreground/background depth. Do not enlarge distant people or merge separated figures. Preserve the invariant sentence.
```

### Texture, stars, or text is missing

```text
Restore the source photograph's original grain, focus, exposure, colour cast, weather, ground and background texture inside all photo regions. Add 8–12 sparse handmade stars across both panels. Add one clearly readable scene-matched lowercase handwritten phrase across the middle seam, spelled exactly as supplied. Keep all three elements subordinate to the reciprocal silhouettes.
```
