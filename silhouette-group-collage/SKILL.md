---
name: silhouette-group-collage
description: Transform user-supplied group photos into vertical diptych silhouette collages using Human Cutout Engine preprocessing, reciprocal positive-negative masks, pixel-locked original people and necessary foreground context, tactile paper fields, preserved film texture, scene-matched handwriting, and sparse handmade stars. Use when the user asks for 剪影群像风格, 群像剪影拼贴, 正负形镜空, 上下双联画, youth-memory group artwork, handmade group poster, indie album collage, or a group photo shown once as opaque silhouettes and once through matching photo cutouts without changing faces or bodies.
---

# Silhouette Group Collage

Create an image edit from a supplied group photograph. Preserve every photographed person as protected source pixels while rebuilding the page as a tactile two-panel composition. Treat the reciprocal silhouette exchange as the defining feature. Never ask a generative model to recreate a visible person. Preserve source texture, then use scene-matched handwriting and handmade stars as secondary structure.

## Required preprocessing dependency

Invoke `$human-cutout-engine` before art direction. Treat its reviewed source-resolution Alpha and transparent RGBA as the only person-boundary and protected-pixel source for this workflow. Read `references/human-cutout-handoff.md` and pass its deterministic handoff validator before composing either panel. Do not continue with prompt-estimated, depth-only, or newly generated person boundaries when the handoff fails.

## Workflow

1. Inspect every supplied reference and source photo before prompting.
2. Count all people explicitly from left to right. Record body count, foreground/background scale, pose, clothing anchors, held objects, interactions, environmental anchors, and protected person regions. Recheck the count before generation; never infer it from a casual first glance.
3. Invoke `$human-cutout-engine` on the unchanged source. For groups, overlaps, edge crops, small background people, or foreground occlusion, prefer a manually accepted phase-2 candidate. Preserve the smallest coherent foreground segment needed to maintain the group's original occlusion relationship and future silhouette.
4. Validate the selected source-resolution Alpha, transparent RGBA, and manifest with `scripts/validate_cutout_handoff.py`. Stop if dimensions, RGB lock, Alpha lock, subject coverage, or available count metadata fail. Inspect the checkerboard preview at 200% before continuing.
5. Estimate how much of the source frame is occupied by the accepted subject layer and choose an adaptive layout from `references/adaptive-layout.md`. Accept every source photo, including close-up selfies with 80–90% subject occupancy. Occupancy changes the layout mode; it never disqualifies the photo.
6. Study the transferable gold-standard recipes in `references/gold-standard-system.md` and the non-person assets under `assets/design-system/`. Use them as a quality floor, not as a fixed template.
7. Choose one group mask family from `references/style-system.md`. Use a connected paper-doll chain for a horizontal group and separate related silhouettes for staggered, close-up, edge-cropped, or deep-space groups.
8. Run the art-direction preflight in `references/art-direction-qc.md`. Decide crop, silhouette fidelity, colour, one named lettering family from `references/typography-system.md`, texture hierarchy, and decoration rhythm before generating anything. Read `references/color-system.md`, then run `scripts/select_scene_palette.py` on the source to produce Echo, Counterpoint, and Atmosphere candidates from the bundled heritage token system. Do not fall back to a default template colour or font.
9. When the user does not specify dimensions, set the output width equal to the source pixel width and derive the height from the two-panel composition; do not default to 9:16. Preserve the source photograph's aspect ratio inside each photo panel whenever practical. Use 4:5, 2:3, 9:16, or exact pixel dimensions only when the user requests them; use 9:16 specifically for explicit phone-wallpaper or mobile-wallpaper requests. Repeat the same source scene across the upper and lower halves, then invert figure and ground:
   - Panel A: show most of the photo and cover selected areas with opaque accent shapes.
   - Panel B: fill most of the panel with a flat paper colour and reveal the same photo through apertures matching Panel A's shapes and positions.
10. Apply one coupled transform to the complete source photograph, accepted Alpha, and protected RGBA. Scale, translate, crop, or inset them together. Never shrink, crop, reshape, or reposition a mask independently to satisfy a colour-area target.
11. Build the tight design mask from the transformed accepted Alpha using `references/edge-refinement.md`. Do not re-segment or ask a generator to infer the people. Add only a 1–3 output-pixel hand-cut safety edge and retain necessary foreground occluders already accepted in the subject layer.
12. Preserve count-defining negative space inside and around the group. A connected silhouette is a paper-doll chain following bodies, raised arms, lifted legs, phones, companions, necessary foreground context, and major gaps; it is never a convex hull, bounding blob, rectangular slab, or giant flower covering the whole group.
13. Use the exact same design mask for both reciprocal states. Cover 100% of every accepted subject pixel in the opaque state. Maintain at least 99.5% measured coverage and limit excess mask area using `scripts/check_mask_coverage.py`; full coverage never licenses a bulky halo.
14. Use one dominant paper colour, one secondary accent, and the source photo's natural colours. Build and compare at least three scene-derived palette candidates before selecting one. The three candidates must use different token IDs and roles from `assets/design-system/color-system.json`; require seam-text contrast of at least 3.0 and reject any dominant listed as an avoid colour for the diagnosed scene. Pick for contrast, emotional fit, and clothing/environment harmony, never from a fixed template or automatic score alone.
15. Lock the transformed Human Cutout Engine RGBA before generation. Keep all accepted people and necessary foreground context as protected source pixels. A uniform transform applied to the complete source package is allowed; isolated generative reconstruction is not.
16. Generate only a person-free layout/background pass with reserved paper masks and a calm empty seam band. Do not ask `image_gen` to render the final phrase or final paper material. Composite the protected RGBA through the accepted reciprocal mask at its recorded transform.
17. Read `references/paper-texture-system.md`, accept or revise the profile suggested by the palette manifest, then build every opaque paper field and every opaque person silhouette with `scripts/apply_paper_texture.py --profile PROFILE`. Flat colour is only a temporary layout guide. Require both texture and profile gates to pass before continuing.
18. Preserve the source photograph's own grain, focus, exposure, weather, reflections, ground texture, and colour relationships. Apply paper fibres only inside paper masks. Verify both photo texture and paper texture at 100% and 200% zoom.
   Use exactly one quiet paper profile. Reject cloud-like tonal patches, artificial fold shadows, cloth weave, glossy noise, repeated tile seams, or stars baked into the material texture.
   Read `references/torn-paper-seam.md` and add one restrained, deterministic torn-paper edge where the broad colour field meets the photo collage. Reuse the same edge path for corresponding reciprocal seams. Never apply this effect to the protected person Alpha.
19. For group images, add one short scene-matched handwritten phrase across the middle seam unless the user declines text. Select one named family from `references/typography-system.md`, then render the exact phrase as a separate transparent layer with `scripts/render_seam_phrase.py`. Require its spelling, contrast, scale, and readability manifest to pass. Never accept image-generated final lettering.
20. Add 8–12 sparse handmade stars across both panels with three size tiers and irregular spacing after paper and lettering are complete. Do not bake decorations into the paper texture or cover identity anchors.
21. Generate or edit with `image_gen` only for non-person, non-lettering layout content. Repeat both invariant sentences from the prompt recipe verbatim in correction attempts.
22. Compare every visible person and retained foreground occluder against the source at face-level zoom. Reject any output with changed facial structure, eyes, nose, mouth, skin texture, hairstyle, body, clothing, hands, held objects, or broken occlusion continuity. Restore the accepted protected RGBA rather than prompting another portrait redraw.
23. Run the visual failure gate in `references/art-direction-qc.md`. Reject the render before delivery if the handoff is unverified, the mask becomes a giant blob, any accepted subject pixel is exposed, any paper region remains a smooth flat fill, texture manifests fail, the final lettering was generated or is hard to read, the palette feels arbitrary, or the paper/film texture disappears.

Read `references/prompt-recipes.md` when building the generation prompt. Read `references/style-system.md` when deciding mask family, layout, palette, or typography. Read `references/reference-breakdown.md` when explaining how the five seed references produce the system.
Read `references/person-preservation.md` before every generation or edit that contains a visible person.
Read `references/art-direction-qc.md` before every render and again during final review.
Read `references/adaptive-layout.md` before choosing crop, scale, panel placement, or mask grouping.
Read `references/edge-refinement.md` before building or correcting any person silhouette.
Read `references/torn-paper-seam.md` before constructing the paper-photo boundary.
Read `references/gold-standard-system.md` before choosing a final art direction.
Read `references/human-cutout-handoff.md` before extracting, validating, transforming, or compositing the protected subject layer.
Read `references/typography-system.md` before choosing, generating, or compositing the seam phrase.
Read `references/deterministic-finishing.md` before rendering any paper field, opaque silhouette, seam phrase, or decoration.
Read `references/color-system.md` before selecting, extending, or applying any paper, ink, lettering, or decoration colour.
Read `references/paper-texture-system.md` after colour selection and before rendering any opaque silhouette or broad paper field.

## Person pixel lock

- Treat every visible person as a protected source region, not as generative subject matter.
- Source every protected region from the accepted Human Cutout Engine Alpha and RGBA handoff. Do not redraw or estimate the people boundary later in the workflow.
- Do not use text prompting alone as proof of identity preservation. Prompts can guide masks and layout, but they cannot guarantee unchanged facial pixels.
- Preserve the original person layer through masking and compositing. AI-generated content may touch the outside edge of the cutout but must not replace pixels inside it.
- Allow only whole-photo crop, translation, or uniform scaling needed for layout. Never beautify, relight, sharpen, restyle, synthesize, or independently resize faces or bodies.
- When an opaque paper silhouette covers a person, no original person pixels need to remain visible in that state. In every photographic aperture or visible-photo state, restore the original person pixels.
- If deterministic person restoration is unavailable, stop and report that exact identity preservation cannot be guaranteed. Do not deliver a generatively reconstructed face as a final result.

## Hard requirements

- Use the same photograph or clearly continuous scene in both panels.
- Require a passing Human Cutout Engine handoff before constructing either panel.
- Make the two panels visibly reciprocal: opaque shape above becomes a photo-revealing hole below, or vice versa.
- Preserve the exact person count, left-to-right order, foreground/background scale, poses, interactions, clothing, held objects, and recognisable setting.
- Preserve every visible person's original facial and body pixels. No generative face, hair, skin, hand, body, clothing, footwear, or held-object reconstruction is allowed.
- Accept close-up and face-dominant photos. Adapt the whole-photo layout rather than refusing the source.
- Keep source photo and all reciprocal masks on one coupled transform. If a large group needs reduction, uniformly reduce the complete photo and its masks together.
- Cover every selected person completely in the opaque state. Never expose partial faces, mouths, hair, hands, bodies, clothing, footwear, phones, or held objects.
- Keep the design mask tight. Default safety expansion is only 1–3 pixels at final output size, or at most 0.3% of the short edge. Use depth only to refine uncertain overlaps, not to replace instance segmentation or matting.
- Let flat colour occupy roughly 40–60% of the whole page.
- Select the dominant, ink, and supporting accent from the scene-adaptive heritage colour system. Record three different scene-derived candidates, the chosen token IDs, exact hex values, scene route, and a text contrast ratio of at least 3.0.
- Keep the page asymmetrical and handmade; allow slight imperfect alignment.
- Use group silhouettes as the mask family; stars and loose marks are supporting punctuation only.
- Preserve count-defining gaps. Do not replace a group with one enclosing polygon, convex hull, saw-tooth slab, or near-rectangular mass.
- Preserve original photographic texture inside every photo region. Do not replace it with a smooth AI-painted interpretation.
- Render all opaque paper fields and silhouettes from one selected reference-derived paper profile with passing deterministic texture and profile manifests; smooth flat digital fills and arbitrary universal noise fail.
- Place one readable, scene-matched handwritten phrase at the middle seam for group images, unless the user requests no text. It should usually span 62–90% of the canvas width with controlled word-to-word changes in scale, tilt, baseline, and lettering face.
- Render the exact phrase as a separate transparent layer with a bundled OFL font. Require contrast ratio at least 3.0 and a passing readability manifest; image-generated final text fails.
- Retain generous quiet space. Supporting marks and words must not compete with the mask exchange.
- When the user does not request a size, keep the output width equal to the source pixel width and do not force a preset aspect ratio or 9:16 canvas.

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
- Do not use any image-generated lettering as final copy, even when it is spelled correctly.
- Do not use tiny centred captions, one unchanged digital font across every image, or identical word sizing and baseline.
- Do not use an arbitrary high-saturation default colour when it is unrelated to the source scene.
- Do not refuse a photo solely because people occupy most of the frame.
- Do not shrink or crop a mask independently to reduce colour coverage.
- Do not broadly dilate, inflate, or feather a person mask merely to pass the coverage test.

## Quality gate

Before delivery, confirm all answers are yes:

1. Did the Human Cutout Engine handoff pass dimensions, RGB lock, Alpha lock, count metadata when available, and 200% manual review?
2. Can the viewer recognise that both halves derive from the same photo?
3. Does at least one shape perform an obvious positive-negative role reversal?
4. Are the person count, order, depth scale, poses, clothing, interactions, held objects, and retained foreground relationships correct in both panels?
5. Does every opaque silhouette fully cover its accepted subject layer with no exposed face, mouth, hair, hand, body, clothing, footwear, phone, held object, or necessary foreground segment while remaining tight to the true contour?
6. Do all visible people use the protected source pixels, with no generated change to faces, hair, skin, bodies, hands, clothing, footwear, or held objects?
7. Do all paper fields and opaque silhouettes use the selected reference-derived profile with both texture and profile gates passing instead of smooth digital fills or universal noise?
8. Does the photograph retain its source grain, focus, exposure, colour, and environmental texture?
9. Is there one strong scene-derived colour decision selected from three different token candidates, with a recorded scene route and ink contrast of at least 3.0, plus 8–12 restrained stars with scale rhythm and one correctly spelled scene-matched phrase that visibly binds the seam?
10. Was the exact phrase rendered separately with a bundled font, a contrast ratio of at least 3.0, cohesive spacing, and a passing readability manifest?
11. Did the selected adaptive layout create useful paper/environment space without independently shrinking the mask?
12. Does the output retain the requested geometry, or the source pixel width when no geometry was requested, without silently forcing 9:16?

## Delivery

Return the generated image plus a concise record containing: Human Cutout Engine candidate paths and handoff result, source subject-occupancy estimate, output geometry mode, adaptive layout mode, selected gold-standard recipe, selected mask family, edge-refinement method, retained foreground context, palette-manifest path, three palette candidate token IDs, chosen paper/ink/accent tokens and exact hex values, scene route, selected paper profile and reference parent, texture/profile gate results, text contrast, named typography family with reference asset and phrase, protected person-layer method, mask coverage and excess-area results, preserved subject anchors, and whether the twelve quality checks passed. If the user asks only for prompt analysis, return the prompt package without generating an image.
