# Deterministic paper and lettering finish

Do not ask an image-generation model to produce the final paper texture or final phrase. The model may reserve shapes and seam space, but both visible finishes are deterministic compositing layers.

## Paper layer

1. Read `paper-texture-system.md` and choose one of its five reference-derived neutral profiles after colour selection. The older coloured crops are palette references only because they contain stars or lettering.
2. Run `scripts/apply_paper_texture.py --profile PROFILE` separately for every opaque paper field and every opaque person silhouette, passing the exact final mask for that region.
3. Tint the selected neutral profile to the scene-derived colour. Do not place a semi-transparent texture over a flat digital fill; the script must create the actual coloured paper pixels.
4. Require `texture_gate_passed: true`, `profile_gate_passed: true`, and the profile-specific minimum luma standard deviation in the generated manifest.
5. Inspect at 100% and 200%. The fibres must remain visible at normal size without becoming heavy universal noise.
6. Add stars only after the material layer is complete. Stars, words, shadows, and photographed objects never belong inside a reusable texture tile.

Example:

```bash
python scripts/apply_paper_texture.py \
  --profile fine-matte-grain \
  --colour '#c94b3f' --width 1178 --height 1600 \
  --mask final-paper-mask.png --output final-paper-layer.png
```

## Seam lettering layer

1. Reserve a calm seam band before rendering. Do not place the phrase directly over high-frequency faces, clothing, foliage, or shoreline detail.
2. Run `scripts/render_seam_phrase.py` with the exact approved phrase and one selected T1–T5 family.
3. Composite the resulting transparent PNG after the paper layer. Never use generated lettering as the final copy.
4. Require `spelling_locked: true`, `readability_gate_passed: true`, contrast ratio at least `3.0`, phrase width fraction at least `0.58`, and phrase height fraction at least `0.20` of its reserved seam band.
5. Keep the phrase visually continuous. Word gaps are controlled by the renderer; do not manually scatter isolated words across the full page.
6. If the chosen family fails contrast or scale, choose a stronger ink colour, shorten the phrase, enlarge the seam band, or switch to T3/T4. Never solve readability with a thick white outline or drop shadow.

Example:

```bash
python scripts/render_seam_phrase.py \
  --text 'we found the blue' --family T5 \
  --width 1178 --height 190 \
  --ink '#f4e7c8' --background-colour '#c94b3f' \
  --output seam-phrase.png
```

## Failure conditions

Reject the artwork when any of the following is true:

- a paper field or opaque silhouette is a smooth digital colour;
- the selected texture profile is unrelated to the paper colour value or scene;
- either the profile gate or output texture gate fails;
- texture appears only as a faint optional overlay;
- a texture tile repeats stars, words, or other decorations;
- a paper-photo boundary is perfectly straight, a repeated zigzag, or uses a fake lifted-paper shadow instead of the shared torn-seam mask;
- the final phrase came from image generation;
- words are illegible, misspelled, too thin, scattered, or placed on a busy seam;
- the phrase requires an outline, glow, or shadow to become readable.
