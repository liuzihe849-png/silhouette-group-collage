# Face preservation

Use this procedure whenever any face remains visible in the final collage.

## Non-negotiable invariant

`FACE INVARIANT: every visible face must come directly from the supplied photograph as protected source pixels; never generate, repaint, reconstruct, beautify, relight, or reinterpret a face.`

## Protected-face workflow

1. Mark each visible face before generation. Include the full face, ears, hairline, facial hair, glasses, and identity-bearing near-face details.
2. Record the source crop and the whole-photo crop, translation, and uniform scale used to place that photograph in each panel.
3. Keep the protected face interiors out of generative repaint operations. Generate paper fields, masks, stars, lettering, and non-face content separately.
4. Composite each protected source-face region above generated content using the recorded whole-photo transform. Do not independently warp or resize a face.
5. Feather only the outer mask boundary when necessary. Keep a documented 1–2 px feather band outside the protected comparison interior.
6. Save a lossless PNG. Compare each output face with the correspondingly transformed source crop at 200% or greater.
7. Require zero RGB difference inside the protected interior. Record the face count, transform, comparison region, differing-pixel count, and maximum RGB difference.
8. If any protected interior pixel differs, restore the original face layer and repeat the comparison. Do not request another generative portrait correction.

## Permitted transformations

- Crop, translate, or uniformly scale the complete source photograph.
- Cover a face completely with an opaque paper silhouette in the positive-mask panel.
- Feather only the outside edge of a protected face mask.

## Forbidden transformations

- Generative inpainting or outpainting through a visible face.
- Face enhancement, beauty retouching, relighting, skin smoothing, sharpening, denoising, age changes, expression changes, or facial reconstruction.
- Independent face resizing, warping, pose correction, hairstyle changes, or replacement with a merely similar identity.
- Claiming preservation from prompt wording or visual resemblance without pixel-comparison evidence.

## Failure handling

If the available tools cannot restore and compare protected source-face pixels, state that exact face preservation cannot be guaranteed and stop before final delivery. A structurally successful collage with altered facial pixels fails the skill.
