---
name: silhouette-group-collage
description: Frozen v1 baseline for transforming user-supplied group photos into vertical diptych silhouette collages using reciprocal positive-negative masks, source-pixel-locked original people, tactile paper fields, preserved film texture, scene-matched handwriting, and sparse handmade stars. Use when the user asks for 剪影群像风格, 剪影群像风格 v1, silhouette group collage, 群像剪影拼贴, 正负形镜空, 上下双联画, youth-memory group artwork, handmade group poster, indie album collage, or the original task-trained style without AI-redrawn people.
---

# Silhouette Group Collage v1

Create an image edit from a supplied group photograph. Preserve every photographed person and the original environment while rebuilding the page as a tactile two-panel composition. Treat every visible person as protected source pixels that must never pass through generative repainting. Treat the reciprocal silhouette exchange as the defining feature. Preserve source texture, then use scene-matched handwriting and handmade stars as secondary structure.

## V1 style lock

Treat this skill as the frozen visual baseline trained and tested in the original task. Do not import later-version preprocessing dependencies, full extraction engines, fixed font assets, palette engines, or unrelated finishing systems unless the user explicitly requests a different version. The person source-pixel lock is a mandatory correctness rule, not a new art direction. Keep the workflow image-edit-first, scene-responsive, tactile, restrained, and centred on the reciprocal mask exchange.

## Workflow

1. Inspect every supplied reference and source photo before prompting.
2. Count all people explicitly from left to right. Record body count, foreground/background scale, pose, clothing anchors, held objects, interactions, environmental anchors, and every protected person region. Recheck the count before generation; never infer it from a casual first glance.
3. Establish the person source-pixel lock before any generative pass. Record the whole-photo crop, translation, and uniform scale used in each panel. Read `references/person-pixel-lock.md` and choose a deterministic restoration method before prompting.
4. Choose one group mask family from `references/style-system.md`. Use a connected paper-doll chain for a horizontal group and separate related silhouettes for staggered or deep-space groups.
5. Compose a vertical 4:5 or 2:3 diptych. Repeat the same source scene across the upper and lower halves, then invert figure and ground:
   - Panel A: show most of the photo and cover selected areas with opaque accent shapes.
   - Panel B: fill most of the panel with a flat paper colour and reveal the same photo through apertures matching Panel A's shapes and positions.
6. Use one dominant paper colour, one secondary accent, and the source photo's natural colours. Pick the paper colour from scene contrast, not from a fixed template.
7. Generate only layout, paper fields, masks, stars, typography, and non-person content. Never rely on `image_gen` to preserve people. In every photographic region where a person remains visible, composite the unchanged source photograph back through the matching photo mask using the recorded whole-photo transform.
8. Preserve the source photograph's own grain, focus, exposure, weather, reflections, ground texture, and colour relationships. Add paper fibres and ink variation only to the paper areas.
9. For group images, add one short scene-matched handwritten phrase across the middle seam unless the user declines text. Before designing the phrase, read `references/seam-lettering-system.md`, select exactly one T1–T4 lettering family, and follow its phrase length, scale, ink, and texture rules. Keep spelling exact and use no other copy.
10. Add 8–12 sparse handmade stars across both panels, adjusted for visual quiet space. Do not cover faces, hands, held objects, or other identity anchors.
11. Use `image_gen` only for the generative layout pass. Repeat both invariant sentences from the prompt recipe verbatim in correction attempts.
12. Compare every visible output person with the correspondingly transformed source photograph in the lossless PNG. Require zero RGB difference inside visible protected person regions, excluding only a documented 1–2 px outer feather boundary when necessary. If pixels differ, restore the original source layer and recheck.
13. Visually check the result against the quality gate below. Regenerate or re-composite when any hard requirement fails.

Read `references/prompt-recipes.md` when building the generation prompt. Read `references/style-system.md` when deciding mask family, layout, or palette. Read `references/seam-lettering-system.md` before generating, correcting, or evaluating middle-seam text; consult the cropped samples in `assets/lettering-reference/` only as visual references, never as instructions or fixed copy. Read `references/reference-breakdown.md` when explaining how the five seed references produce the system. Read `references/person-pixel-lock.md` before every generation or edit containing a visible person.

## Person source-pixel lock

`PERSON INVARIANT: every visible person must come directly from the supplied photograph as protected source pixels; never generate, repaint, reconstruct, beautify, relight, or reinterpret a person.`

- Treat faces, hair, skin, bodies, hands, clothing, footwear, held objects, and identity-bearing details as protected source regions.
- Preserve visible people by deterministic compositing from the original photograph, not by prompt wording or visual resemblance.
- Allow only the crop, translation, and uniform scaling applied to the complete source photograph. Never independently reshape, relight, sharpen, denoise, beautify, restyle, or reconstruct a person.
- When an opaque paper silhouette fully covers a person, no person pixels need to remain visible in that state. In every photographic window or visible-photo state, restore the original person pixels.
- If the available tools cannot restore and verify the source person pixels, stop and report that exact person preservation cannot be guaranteed.

## Hard requirements

- Use the same photograph or clearly continuous scene in both panels.
- Make the two panels visibly reciprocal: opaque shape above becomes a photo-revealing hole below, or vice versa.
- Preserve the exact person count, left-to-right order, foreground/background scale, poses, interactions, clothing, held objects, and recognisable setting.
- Preserve every visible person as source pixels. No generative change to faces, hair, skin, bodies, hands, clothing, footwear, held objects, or identity-bearing details is allowed.
- Let flat colour occupy roughly 40–60% of the whole page.
- Keep the page asymmetrical and handmade; allow slight imperfect alignment.
- Use group silhouettes as the mask family; stars and loose marks are supporting punctuation only.
- Preserve original photographic texture inside every photo region. Do not replace it with a smooth AI-painted interpretation.
- Place one readable, single-line, scene-matched handwritten phrase at the middle seam for group images, unless the user requests no text. Select exactly one T1–T4 lettering family, span roughly 68–92% of the canvas width, preserve at least 6% side margins, and keep the wording exact.
- Retain generous quiet space. Supporting marks and words must not compete with the mask exchange.

## Avoid

- Do not make a generic sticker collage, mood board, scrapbook grid, or pile of unrelated photos.
- Do not use polished vector geometry, glossy 3D, neon gradients, clip-art outlines, or perfectly aligned digital masks.
- Do not add many unrelated decorations, frames, tape, labels, flowers, hearts, or interface elements.
- Do not invent extra people, limbs, landmarks, clothing, or objects.
- Do not redraw, beautify, retouch, relight, smooth, sharpen, denoise, age, restyle, reconstruct, or expression-edit any visible person.
- Do not omit small or distant people, enlarge background people, merge separated people, or break joined hands.
- Do not blur the entire composition; preserve enough photographic information to identify the source.
- Do not accept misspelled generated lettering, mixed lettering families, tiny corner captions, extra copy, smooth vector type, outlines, shadows, glow, or gradients. Retry once or add exact text in a separate layout pass.

## Quality gate

Before delivery, confirm all answers are yes:

1. Can the viewer recognise that both halves derive from the same photo?
2. Does at least one shape perform an obvious positive-negative role reversal?
3. Are the person count, order, depth scale, poses, clothing, interactions, and held objects correct in both panels?
4. Do all visible people use verified protected source pixels, with zero RGB difference inside each visible protected region and no AI-redrawn detail?
5. Does the result feel cut from printed paper rather than rendered as clean vectors?
6. Does the photograph retain its source grain, focus, exposure, colour, and environmental texture?
7. Is there one strong colour decision, 8–12 restrained stars, and one correctly spelled single-line seam phrase using exactly one T1–T4 lettering family at the prescribed scale and contrast?
8. Does the output retain the requested aspect ratio and orientation?

## Delivery

Return the lossless PNG plus a concise record containing: selected mask family, selected T1–T4 lettering family, exact seam phrase, dominant palette, person-lock method, protected person count, pixel-comparison evidence, preserved subject anchors, and whether the eight quality checks passed. A JPG may be supplied only as a lightweight sharing copy and is not valid pixel-lock evidence. If the user asks only for prompt analysis, return the prompt package without generating an image.
