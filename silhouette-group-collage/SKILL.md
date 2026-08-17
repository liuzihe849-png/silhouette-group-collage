---
name: silhouette-group-collage-v1
description: Frozen v1 baseline for transforming user-supplied group photos into vertical diptych silhouette collages using reciprocal positive-negative masks, source-pixel-locked original faces, tactile paper fields, preserved film texture, scene-matched handwriting, and sparse handmade stars. Use when the user asks for 剪影群像风格 v1, 群像剪影拼贴, 正负形镜空, 上下双联画, youth-memory group artwork, handmade group poster, indie album collage, or the original task-trained style without AI-redrawn faces.
---

# Silhouette Group Collage v1

Create an image edit from a supplied group photograph. Preserve every photographed person and the original environment while rebuilding the page as a tactile two-panel composition. Treat every visible face as protected source pixels that must never pass through generative repainting. Treat the reciprocal silhouette exchange as the defining feature. Preserve source texture, then use scene-matched handwriting and handmade stars as secondary structure.

## V1 style lock

Treat this skill as the frozen visual baseline trained and tested in the original task. Do not import later-version preprocessing dependencies, full-person extraction engines, fixed font assets, palette engines, or unrelated finishing systems unless the user explicitly requests a different version. The face source-pixel lock is a mandatory correctness repair to v1, not an optional later-version feature. Keep the workflow image-edit-first, scene-responsive, tactile, restrained, and centred on the reciprocal mask exchange.

## Workflow

1. Inspect every supplied reference and source photo before prompting.
2. Count all people explicitly from left to right. Record body count, foreground/background scale, pose, clothing anchors, held objects, interactions, environmental anchors, and every visible face-lock region. Recheck the count before generation; never infer it from a casual first glance.
3. Establish the face source-pixel lock before any generative pass. Protect each visible face together with its ears, hairline, facial hair, glasses, and identity-bearing near-face details. Record the source crop and the whole-photo crop, translation, and uniform scale used in each panel. Read `references/face-preservation.md` and choose a deterministic restoration method before prompting.
4. Choose one group mask family from `references/style-system.md`. Use a connected paper-doll chain for a horizontal group and separate related silhouettes for staggered or deep-space groups.
5. Compose a vertical 4:5 or 2:3 diptych. Repeat the same source scene across the upper and lower halves, then invert figure and ground:
   - Panel A: show most of the photo and cover selected areas with opaque accent shapes.
   - Panel B: fill most of the panel with a flat paper colour and reveal the same photo through apertures matching Panel A's shapes and positions.
6. Use one dominant paper colour, one secondary accent, and the source photo's natural colours. Pick the paper colour from scene contrast, not from a fixed template.
7. Generate only the layout, paper fields, masks, stars, typography, and non-face content. Never rely on `image_gen` to preserve a face. When a face is visible, composite the protected source-face region back above generated content using the recorded whole-photo transform. Feather only the outer boundary; do not alter the protected interior.
8. Preserve the source photograph's own grain, focus, exposure, weather, reflections, ground texture, and colour relationships. Add paper fibres and ink variation only to the paper areas.
9. For group images, add one short scene-matched handwritten phrase across the middle seam unless the user declines text. Keep spelling exact and use no other copy.
10. Add 8–12 sparse handmade stars across both panels, adjusted for visual quiet space. Do not cover faces, hands, held objects, or other identity anchors.
11. Use `image_gen` only for the generative layout pass. Repeat both invariant sentences from the prompt recipe verbatim in correction attempts.
12. Compare every visible output face with the correspondingly transformed source crop at 200% or greater in the lossless PNG. Confirm that the protected interior has zero RGB difference; exclude only a documented 1–2 px feather boundary when necessary. If the pixels differ, restore the source-face layer and recheck. Never claim a face lock without comparison evidence.
13. Visually check the result against the quality gate below. Regenerate or re-composite when any hard requirement fails.

Read `references/prompt-recipes.md` when building the generation prompt. Read `references/style-system.md` when deciding mask family, layout, palette, or typography. Read `references/reference-breakdown.md` when explaining how the five seed references produce the system.
Read `references/face-preservation.md` before every generation or edit containing a visible face.

## Face source-pixel lock

`FACE INVARIANT: every visible face must come directly from the supplied photograph as protected source pixels; never generate, repaint, reconstruct, beautify, relight, or reinterpret a face.`

- Treat every visible face as a protected source region, not as generative subject matter.
- Do not use text prompting alone as proof of identity preservation. A prompt can guide masks and layout but cannot guarantee unchanged facial pixels.
- Preserve face pixels through masking and deterministic compositing. AI-generated content may touch the outside boundary but must not replace pixels inside the protected region.
- Allow only the crop, translation, and uniform scaling applied to the complete source photograph. Never independently resize, warp, relight, sharpen, denoise, beautify, age, restyle, reconstruct, or expression-edit a face.
- When an opaque paper silhouette fully covers a face, no face pixels need to remain visible in that state. In every photographic aperture or visible-photo state, restore the original face pixels.
- If the available tools cannot restore and verify the source face pixels, stop and report that exact face preservation cannot be guaranteed. Do not deliver a generatively reconstructed face.

## Hard requirements

- Use the same photograph or clearly continuous scene in both panels.
- Make the two panels visibly reciprocal: opaque shape above becomes a photo-revealing hole below, or vice versa.
- Preserve the exact person count, left-to-right order, foreground/background scale, poses, interactions, clothing, held objects, and recognisable setting.
- Preserve every visible face as source pixels. No generative change to facial structure, eyes, nose, mouth, skin texture, expression, ears, hairline, facial hair, glasses, or identity-bearing near-face details is allowed.
- Let flat colour occupy roughly 40–60% of the whole page.
- Keep the page asymmetrical and handmade; allow slight imperfect alignment.
- Use group silhouettes as the mask family; stars and loose marks are supporting punctuation only.
- Preserve original photographic texture inside every photo region. Do not replace it with a smooth AI-painted interpretation.
- Place one readable, scene-matched handwritten phrase at the middle seam for group images, unless the user requests no text.
- Retain generous quiet space. Supporting marks and words must not compete with the mask exchange.

## Avoid

- Do not make a generic sticker collage, mood board, scrapbook grid, or pile of unrelated photos.
- Do not use polished vector geometry, glossy 3D, neon gradients, clip-art outlines, or perfectly aligned digital masks.
- Do not add many unrelated decorations, frames, tape, labels, flowers, hearts, or interface elements.
- Do not invent extra people, limbs, landmarks, clothing, or objects.
- Do not redraw, beautify, retouch, relight, smooth, sharpen, denoise, age, de-age, restyle, reconstruct, or expression-edit any visible face.
- Do not omit small or distant people, enlarge background people, merge separated people, or break joined hands.
- Do not blur the entire composition; preserve enough photographic information to identify the source.
- Do not accept misspelled generated lettering. Retry once or add exact text in a separate layout pass.

## Quality gate

Before delivery, confirm all answers are yes:

1. Can the viewer recognise that both halves derive from the same photo?
2. Does at least one shape perform an obvious positive-negative role reversal?
3. Are the person count, order, depth scale, poses, clothing, interactions, and held objects correct in both panels?
4. Do all visible faces use verified protected source pixels, with zero RGB difference inside each transformed face-lock region and no AI-redrawn facial detail?
5. Does the result feel cut from printed paper rather than rendered as clean vectors?
6. Does the photograph retain its source grain, focus, exposure, colour, and environmental texture?
7. Is there one strong colour decision, 8–12 restrained stars, and one correctly spelled scene-matched phrase at the seam?
8. Does the output retain the requested aspect ratio and orientation?

## Delivery

Return the lossless PNG plus a concise record containing: selected mask family, dominant palette, face-lock method, protected face count, pixel-comparison evidence, preserved subject anchors, and whether the eight quality checks passed. A JPG may be supplied only as a lightweight sharing copy and is not valid face-lock evidence. If the user asks only for prompt analysis, return the prompt package without generating an image.
