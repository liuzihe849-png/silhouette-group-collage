# Person pixel lock

Use this procedure whenever any photographed person remains visible in the final collage.

## Non-negotiable invariant

`PERSON INVARIANT: every visible person must come directly from the supplied photograph as protected source pixels; never generate, repaint, reconstruct, beautify, relight, or reinterpret a person.`

## Low-detail face safety gate

Inspect every visible face at 200% before any generative pass. Mark the gate as failed when any condition applies:

- the shorter face dimension will be below 48 source pixels after the planned whole-photo crop and uniform scale;
- focus blur, motion blur, compression, occlusion, low contrast, or distance prevents the eyes, nose, and mouth from being distinguished as separate source features;
- a protected facial interior cannot be defined confidently without asking a model to infer missing detail.

When one face fails, or when the assessment is uncertain, switch the entire job to strict whole-person pixel lock for all visible people. Preserve the original blur rather than trying to repair it. The model may generate only paper fields, reciprocal masks, stars, lettering, and non-person content. Do not generate, enhance, sharpen, denoise, beautify, relight, reconstruct, or replace any visible part of any person.

## Protected-person workflow

1. Mark every visible person before generation, including face, hair, skin, body, hands, clothing, footwear, held objects, and identity-bearing details.
2. Record the whole-photo crop, translation, and uniform scale used to place the photograph in each panel.
3. Keep protected person interiors out of generative repaint operations. Generate paper fields, masks, stars, lettering, and non-person content separately.
4. Composite the unchanged original photograph back through every visible photographic mask using the recorded whole-photo transform. Do not independently warp or resize a person.
5. Feather only the outside of a protected boundary when necessary. Keep a documented 1–2 px feather band outside the comparison interior.
6. Save a lossless PNG and compare each visible protected region with the correspondingly transformed source photograph.
7. Require zero RGB difference inside each protected interior. Record person count, transform, comparison region, differing-pixel count, and maximum RGB difference.
8. If any protected interior pixel differs, restore the original source layer and repeat the comparison. Do not request another generative portrait or body correction.
9. If deterministic whole-person compositing or zero-RGB-difference verification is unavailable, stop before formal delivery. A layout preview must be explicitly labelled non-final and not pixel locked.

## Permitted transformations

- Crop, translate, or uniformly scale the complete source photograph.
- Cover a person completely with an opaque paper silhouette in the positive-mask panel.
- Feather only the outside edge of a protected mask.

## Forbidden transformations

- Generative inpainting or outpainting through any visible part of a person.
- Face or body enhancement, beauty retouching, relighting, skin smoothing, sharpening, denoising, age changes, expression changes, clothing reconstruction, or hand reconstruction.
- Treating a blurred, small, compressed, occluded, or low-contrast face as permission to invent clearer facial detail.
- Independent person resizing, warping, pose correction, hairstyle changes, or replacement with a merely similar identity.
- Claiming preservation from prompt wording or visual resemblance without pixel-comparison evidence.

## Failure handling

If the available tools cannot restore and compare protected source pixels, state that exact person preservation cannot be guaranteed and stop before formal delivery. A visually successful collage with altered person pixels fails this skill. Never promote a generative draft to the formal lossless deliverable.
