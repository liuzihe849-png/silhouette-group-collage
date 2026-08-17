# Torn paper collage seam

Add an irregular torn-paper edge where the broad paper field meets the photographic collage. This is a construction detail, not a decorative border.

## Rules

- Apply the tear only to the paper-photo boundary. Never erode, expand, or redraw the Human Cutout Engine person Alpha.
- Reuse one deterministic edge path for corresponding reciprocal boundaries so the diptych still reads as one positive-negative system.
- Keep the amplitude restrained: normally 4–18 output pixels. The tear should read at close view without becoming a saw-tooth band.
- Preserve faces, hands, phones, held objects, lettering, and other identity anchors. Move the seam or locally suppress fibres if it would cross them.
- Use a soft-alpha fringe only for tiny exposed paper fibres. The main aperture remains hard and clean.
- Do not add a white sticker border, bevel, drop shadow, lifted-paper shadow, or repeated zigzag.

## Deterministic mask

```bash
python3 scripts/build_torn_paper_seam.py \
  --width 1080 --height 96 --edge top --seed 849 \
  --output outputs/torn-seam-mask.png
```

Use the generated grayscale mask to composite the selected textured paper field against the photo. Record the `shared_path_key` in the delivery manifest and reuse it wherever the reciprocal boundary corresponds.
