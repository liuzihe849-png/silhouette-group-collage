# Seam lettering design system

Treat the seam phrase as a visual subject, not as a caption. Select one family from the five reference assets under `assets/design-system/typography-reference/` after diagnosing the photograph's energy, palette, and available seam width.

The PNG assets are visual targets. The bundled OFL fonts and `scripts/render_seam_phrase.py` provide the deterministic final lettering layer. Match the reference crop's stroke behaviour and energy through family selection and controlled word-level placement; do not ask image generation to write the final phrase.

## T1: tall dry brush

Reference: `01-tall-dry-brush.png`

- Character: tall, compressed, energetic brush script with long ascenders and descenders.
- Best for: expansive landscape, winter horizon, travel memory, celebratory panoramic groups.
- Phrase: 3–6 words; allow the line to span 72–94% of the canvas width.
- Treatment: one dark ink colour on a bright or pale paper field; strong vertical stroke rhythm; slight dry-brush breakup; no outline.
- Avoid: overly round letters, short timid sizing, smooth calligraphy, or equal word heights.

## T2: casual dry script

Reference: `02-casual-dry-script.png`

- Character: low-contrast diary handwriting with moderate slant, open counters, and naturally uneven spacing.
- Best for: quiet indoor gatherings, intimate friendship, soft winter or evening scenes.
- Phrase: 3–6 words on one relaxed line.
- Treatment: dark brown or charcoal ink on a quiet pale field; restrained scale changes; subtle baseline drift; dry matte edges.
- Avoid: bold display scale, decorative swashes, rigid digital baseline, or a glossy smooth stroke.

## T3: chunky rounded marker

Reference: `03-chunky-rounded-marker.png`

- Character: upright, heavy, rounded handmade marker with irregular character widths and soft blunt terminals.
- Best for: pets, snow, close groups, humorous or comforting scenes, compact phrases.
- Phrase: 3–5 words; keep counters open and punctuation visible.
- Treatment: warm cream ink on a dark saturated paper field; small word-level size differences; slightly uneven vertical alignment.
- Avoid: geometric bubble type, perfect circles, thin strokes, or excessively playful multicolour letters.

## T4: bold motion brush

Reference: `04-bold-motion-brush.png`

- Character: broad italic brush lettering with long connected strokes, strong directional energy, and optional short motion marks.
- Best for: walking, running, dancing, linked gestures, playful outdoor group movement.
- Phrase: 3–6 words; emphasize the action or rhythm word.
- Treatment: cream ink at large seam scale, optional subtle same-palette registration offset, one tail or pair of motion marks.
- Avoid: heavy contrasting outline, drop shadow, uniform word size, or motion marks scattered around every word.

## T5: wide diary brush

Reference: `05-wide-diary-brush.png`

- Character: wide, loose, human brush script with changing pressure, generous word spacing, and a fast handwritten finish.
- Best for: teams, reunions, summer travel, candid groups, upbeat shared memories.
- Phrase: 3–6 words; let one emotional word become 8–16% larger.
- Treatment: warm cream or off-white across the seam, minor rotation per word, one terminal flick or small emphasis marks.
- Avoid: narrow condensed type, formal calligraphy, exact repetition of letterforms, or a computer-perfect baseline.

## Selection order

1. Choose by scene energy: quiet → T2/T3; expansive → T1; motion → T4; candid team/travel → T5.
2. Confirm the family remains readable against both sides of the seam.
3. Keep the phrase to one line when possible; reduce phrase length before reducing it to caption size.
4. Vary scale, tilt, baseline, and spacing by word within the selected family. Do not mix unrelated families.
5. Use no more than one optional underline, tail, registration offset, or pair of motion marks.
6. Compare the result to its reference crop. Reject it if the stroke weight, width, energy, or handmade material character has drifted into generic system typography.
7. Require contrast ratio at least 3.0 and keep the exact phrase as one cohesive line inside a calm seam band. If T1, T2, or T5 becomes too thin, switch to T3 or T4 before adding any outline.

## Typography quality gate

Confirm all answers are yes:

1. Was one named family selected for a scene-specific reason?
2. Does the phrase span enough of the seam to act as a compositional bridge?
3. Are word-level changes intentional but still coherent?
4. Are spelling and punctuation exact?
5. Does the ink feel printed or hand-painted on paper rather than digitally typeset?
6. Is the lettering free of thick outlines, glossy effects, mechanical baselines, and generic default-font character?
7. Did `render_seam_phrase.py` report `spelling_locked` and `readability_gate_passed` with contrast at least 3.0?
