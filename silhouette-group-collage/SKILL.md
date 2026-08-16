---
name: silhouette-group-collage
description: Transform user-supplied group photos into vertical diptych silhouette collages using reciprocal positive-negative masks, pixel-locked original people, tactile paper fields, preserved film texture, scene-matched handwriting, and sparse handmade stars. Use when the user asks for 剪影群像风格, 群像剪影拼贴, 正负形镜空, 上下双联画, youth-memory group artwork, handmade group poster, indie album collage, or a group photo shown once as opaque silhouettes and once through matching photo cutouts without changing faces or bodies.
---

# Silhouette Group Collage

Create an image edit from a supplied group photograph. Preserve every photographed person as protected source pixels while rebuilding the page as a tactile two-panel composition. Treat the reciprocal silhouette exchange as the defining feature. Never ask a generative model to recreate a visible person. Preserve source texture, then use scene-matched handwriting and handmade stars as secondary structure.

## Workflow

1. Inspect every supplied reference and source photo before prompting.
2. Count all people explicitly from left to right. Record body count, foreground/background scale, pose, clothing anchors, held objects, interactions, environmental anchors, and protected person regions. Recheck the count before generation; never infer it from a casual first glance.
3. Choose one group mask family from `references/style-system.md`. Use a connected paper-doll chain for a horizontal group and separate related silhouettes for staggered or deep-space groups.
4. Run the art-direction preflight in `references/art-direction-qc.md`. Decide crop, silhouette fidelity, colour, lettering family, texture hierarchy, and decoration rhythm before generating anything. Do not fall back to a default template colour or font.
5. Compose a vertical 4:5, 2:3, or 9:16 diptych. Use 9:16 for phone wallpaper requests. Repeat the same source scene across the upper and lower halves, then invert figure and ground:
   - Panel A: show most of the photo and cover selected areas with opaque accent shapes.
   - Panel B: fill most of the panel with a flat paper colour and reveal the same photo through apertures matching Panel A's shapes and positions.
6. Preserve count-defining negative space inside and around the group. A connected silhouette is a paper-doll chain following bodies, raised arms, lifted legs, phones, companions, and major gaps; it is never a convex hull, bounding blob, rectangular slab, or giant flower covering the whole group.
7. Use one dominant paper colour, one secondary accent, and the source photo's natural colours. Build and compare at least three scene-derived palette candidates before selecting one. Pick for contrast, emotional fit, and clothing/environment harmony, never from a fixed template.
8. Lock every visible person before generation. Keep faces, hair, skin, bodies, hands, clothing, footwear, and held objects from the source photograph as protected pixels. A uniform transform applied to the complete source photo is allowed; isolated generative reconstruction of a person is not.
9. Generate only the paper fields, masks, non-person environment extensions, stars, and typography. If the tool may redraw people, generate a person-free layout/background pass and composite the original protected person regions back afterward at the recorded scale and position.
10. Preserve the source photograph's own grain, focus, exposure, weather, reflections, ground texture, and colour relationships. Add paper fibres and ink variation only to the paper areas. Verify both photo texture and paper texture at 200% zoom.
11. For group images, add one short scene-matched handwritten phrase across the middle seam unless the user declines text. Treat it as a major compositional bridge, not a tiny caption. Keep spelling exact and use no other copy. Follow the controlled handwriting variation in `references/art-direction-qc.md`.
12. Add 8–12 sparse handmade stars across both panels with three size tiers and irregular spacing. Do not cover faces, hands, held objects, or other identity anchors.
13. Generate or edit with `image_gen` only for non-person content. Repeat both invariant sentences from the prompt recipe verbatim in correction attempts.
14. Compare every visible person against the source at face-level zoom. Reject any output with changed facial structure, eyes, nose, mouth, skin texture, hairstyle, body, clothing, hands, or held objects. Restore the protected source-person layer rather than prompting another portrait redraw.
15. Run the visual failure gate in `references/art-direction-qc.md`. Reject the render before delivery if the mask becomes a giant blob, the lettering looks like a default font, the palette feels arbitrary, the people are too small, or the paper/film texture disappears.

Read `references/prompt-recipes.md` when building the generation prompt. Read `references/style-system.md` when deciding mask family, layout, palette, or typography. Read `references/reference-breakdown.md` when explaining how the five seed references produce the system.
Read `references/person-preservation.md` before every generation or edit that contains a visible person.
Read `references/art-direction-qc.md` before every render and again during final review.

## Person pixel lock

- Treat every visible person as a protected source region, not as generative subject matter.
- Do not use text prompting alone as proof of identity preservation. Prompts can guide masks and layout, but they cannot guarantee unchanged facial pixels.
- Preserve the original person layer through masking and compositing. AI-generated content may touch the outside edge of the cutout but must not replace pixels inside it.
- Allow only whole-photo crop, translation, or uniform scaling needed for layout. Never beautify, relight, sharpen, restyle, synthesize, or independently resize faces or bodies.
- When an opaque paper silhouette covers a person, no original person pixels need to remain visible in that state. In every photographic aperture or visible-photo state, restore the original person pixels.
- If deterministic person restoration is unavailable, stop and report that exact identity preservation cannot be guaranteed. Do not deliver a generatively reconstructed face as a final result.

## Hard requirements

- Use the same photograph or clearly continuous scene in both panels.
- Make the two panels visibly reciprocal: opaque shape above becomes a photo-revealing hole below, or vice versa.
- Preserve the exact person count, left-to-right order, foreground/background scale, poses, interactions, clothing, held objects, and recognisable setting.
- Preserve every visible person's original facial and body pixels. No generative face, hair, skin, hand, body, clothing, footwear, or held-object reconstruction is allowed.
- Let flat colour occupy roughly 40–60% of the whole page.
- Keep the page asymmetrical and handmade; allow slight imperfect alignment.
- Use group silhouettes as the mask family; stars and loose marks are supporting punctuation only.
- Preserve count-defining gaps. Do not replace a group with one enclosing polygon, convex hull, saw-tooth slab, or near-rectangular mass.
- Preserve original photographic texture inside every photo region. Do not replace it with a smooth AI-painted interpretation.
- Place one readable, scene-matched handwritten phrase at the middle seam for group images, unless the user requests no text. It should usually span 62–90% of the canvas width with controlled word-to-word changes in scale, tilt, baseline, and lettering face.
- Retain generous quiet space. Supporting marks and words must not compete with the mask exchange.

## Avoid

- Do not make a generic sticker collage, mood board, scrapbook grid, or pile of unrelated photos.
- Do not use polished vector geometry, glossy 3D, neon gradients, clip-art outlines, or perfectly aligned digital masks.
- Do not add thin contrasting outlines around silhouette edges; separation must come from colour and figure-ground contrast.
- Do not add many unrelated decorations, frames, tape, labels, flowers, hearts, or interface elements.
- Do not invent extra people, limbs, landmarks, clothing, or objects.
- Do not redraw, beautify, age, de-age, relight, smooth, sharpen, restyle, or reinterpret any visible person.
- Do not omit small or distant people, enlarge background people, merge separated people, or break joined hands.
- Do not blur the entire composition; preserve enough photographic information to identify the source.
- Do not accept misspelled generated lettering. Retry once or add exact text in a separate layout pass.
- Do not use tiny centred captions, one unchanged digital font across every image, or identical word sizing and baseline.
- Do not use an arbitrary high-saturation default colour when it is unrelated to the source scene.

## Quality gate

Before delivery, confirm all answers are yes:

1. Can the viewer recognise that both halves derive from the same photo?
2. Does at least one shape perform an obvious positive-negative role reversal?
3. Are the person count, order, depth scale, poses, clothing, interactions, and held objects correct in both panels?
4. Do all visible people use the protected source pixels, with no generated change to faces, hair, skin, bodies, hands, clothing, footwear, or held objects?
5. Does the result feel cut from printed paper rather than rendered as clean vectors?
6. Does the photograph retain its source grain, focus, exposure, colour, and environmental texture?
7. Is there one strong scene-derived colour decision, 8–12 restrained stars with scale rhythm, and one correctly spelled scene-matched phrase that visibly binds the seam?
8. Does the typography show controlled handwritten variation instead of a tiny or uniform digital caption?
9. Are the main figures large enough to make the page feel composed rather than empty, while retaining deliberate quiet space?
10. Does the output retain the requested aspect ratio and orientation?

## Delivery

Return the generated image plus a concise record containing: selected mask family, three palette candidates and the chosen palette, lettering family and phrase, protected person-layer method, preserved subject anchors, and whether the ten quality checks passed. If the user asks only for prompt analysis, return the prompt package without generating an image.
