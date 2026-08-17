# Person preservation

Use this procedure whenever any person remains visible in the final collage.

## Non-negotiable invariant

`PERSON INVARIANT: every visible person must come directly from the supplied photograph; do not generate, repaint, reconstruct, beautify, relight, or reinterpret any face, hair, skin, hand, body, clothing, footwear, or held object.`

## Protected-layer workflow

1. Invoke `$human-cutout-engine` and accept only a reviewed source-resolution Alpha, protected RGBA, and matching manifest that pass `scripts/validate_cutout_handoff.py`.
2. Include each complete visible person, fine hair, fingers, clothing edges, footwear, held objects, and necessary foreground occluders in the accepted protected subject layer.
3. Keep this RGBA as protected source pixels. Do not send its interior through a generative repaint operation or estimate its boundary again.
4. Build the diptych layout, paper fields, stars, lettering, reciprocal masks, and any non-person environment extension separately.
5. Transform the complete source photograph, Alpha, and RGBA together. In every photographic aperture or visible-photo state, composite the protected subject RGBA back above generated content at the recorded position and scale.
6. Feather only the outer mask edge when necessary. Do not blur, recolour, sharpen, denoise, or relight the person interior.
7. Compare source and output person crops at 200% or greater. Inspect eyes, nose, mouth, jaw, hairline, skin marks, fingers, garment details, footwear, held objects, and retained foreground relationships.
8. If any interior detail differs because of synthesis, restore the accepted protected RGBA. Do not request another generative portrait correction.

## Permitted transformations

- Crop or translate the complete source photograph.
- Uniformly scale the complete source photograph when required by the requested canvas.
- Cover a person completely with an opaque paper silhouette in the positive-mask panel.
- Apply paper texture outside protected person regions.

## Forbidden transformations

- Generative outpainting through a face or body.
- Face enhancement, beauty retouching, relighting, skin smoothing, sharpening, denoising, age changes, expression changes, or hairstyle changes.
- Independent resizing, warping, pose correction, anatomy repair, clothing replacement, or hand regeneration.
- Accepting a merely similar identity because the person count and pose look correct.

## Failure handling

If the available tools cannot preserve or restore protected source pixels, state that exact person preservation cannot be guaranteed and stop before final delivery. A structurally successful collage with altered faces fails the skill.
