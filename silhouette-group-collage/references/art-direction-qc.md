# Art direction and rejection gate

Read this file before every render and during final review. The goal is not merely to satisfy the reciprocal-mask formula; the output must also look art-directed.

## 1. Diagnose the source before choosing a style

Record four things:

1. **Group geometry** — tight cluster, horizontal chain, staggered depth, or group plus companion object.
2. **Energy** — still portrait, playful pose, running, celebration, intimate indoor gathering, or travel memory.
3. **Colour anchors** — one distinctive clothing colour, one environmental colour, and one neutral.
4. **Quiet zones** — sky, wall, snow, water, floor, or blank paper areas that can accept lettering and stars.

Make the design respond to these observations. Never select palette, type, or decoration before this diagnosis.

Estimate person occupancy and select environment-led, balanced-group, or portrait-dense mode from `adaptive-layout.md`. This selection never rejects the photo.

## 2. Mask fidelity: preserve the pose, not merely the envelope

A successful silhouette lets the viewer recount the people without seeing faces. Preserve:

- every head peak and shoulder break;
- raised or extended arms;
- lifted legs and footwear;
- phones, joined hands, companion animals, and airborne objects;
- large gaps between people and triangular negative spaces formed by limbs.

For a connected group, use only narrow paper bridges where bodies genuinely touch or visually pass energy to one another. Separate a distant or foreground person when joining them would require a broad artificial slab.

Reject the mask if any of these are true:

- it resembles a rectangle, convex hull, flower blob, or saw-tooth mountain band;
- it leaves any portion of a selected face, hair, neck, hand, body, clothing, footwear, phone, or held object exposed;
- the reciprocal photo aperture contains large accidental areas of grass, wall, road, or sky;
- thin coloured outlines are needed to explain the edge;
- the viewer cannot recover the original pose rhythm from the silhouette alone.

Use a hard binary aperture edge for visible source pixels. If automated segmentation is messy, simplify the hand-cut contour or use a deliberately shaped photo window; never leave translucent halos, background slivers, half-covered faces, or half-cut footwear. A large colour mask is not corrected by shrinking it independently. Use separate mask islands or uniformly inset the complete source photo and all masks together.

## 3. Composition for 9:16 phone wallpaper

Use a native 1080×1920 or equivalent 9:16 canvas. Do not blur, mirror, or stretch the source to fill height.

- Split panels around 46:54 or 50:50; reserve 7–12% of the page around the seam for lettering overlap.
- In environment-led mode, aim for people to occupy roughly 18–32% of one panel while preserving the environmental anchor.
- In balanced mode, use roughly 22–38% when practical.
- In portrait-dense mode, uniformly inset the whole photo and matching masks so people occupy roughly 25–45% of one panel. These are soft targets, never mask-cropping rules.
- Preserve one meaningful environmental anchor in the photo panel: architecture, mountain, lake, sea, snow, table, window, or road.
- Use asymmetry inside each panel, but keep the reciprocal mask transform recognisable.
- Keep roughly 12–20% of the whole page as quiet space for breathing room, text terminals, and sparse marks.

The page should feel full because the photo window, environment/paper field, mask rhythm, and lettering are balanced. The people do not need to dominate the page.

## 4. Scene-derived palette selection

Create three candidates before rendering:

1. **Echo palette** — dominant paper sampled from a distinctive garment or object.
2. **Counterpoint palette** — a muted complementary colour against the dominant environment.
3. **Atmosphere palette** — a paper colour matching the emotional temperature of the scene.

Choose one candidate using these checks:

- silhouette-to-photo contrast is immediately readable;
- the colour supports the scene rather than looking pasted on;
- saturation does not overpower skin, clothing, or the environment;
- cream/ink accent remains legible on both panels;
- the choice differs from the previous image when the sources have different colour stories.

Use one dominant paper colour, one supporting accent, and cream or charcoal. Never default every image to teal, vermilion, magenta, or beige. Avoid pure digital primaries unless the source already contains them and the mood supports them.

## 5. Handwriting system: controlled variation

The seam phrase is a major visual bridge, not metadata. Derive one short phrase from the visible action and setting. Prefer 3–6 words and lowercase unless the scene calls for emphatic capitals.

Select one lettering family per image:

- **brush diary** — fluid thick-thin strokes for movement, travel, friendship, or celebration;
- **chunky marker** — rounded irregular letters for snow, pets, playful groups, or graphic colour fields;
- **loose pencil** — lighter, more intimate lettering for indoor gatherings or quiet memories.

Apply controlled randomness by word, not chaotic letter-by-letter styling:

- use at most two related handwriting faces;
- vary word scale within roughly 0.88–1.16;
- rotate words between about -4° and +4°;
- shift baselines by 1–3% of canvas height;
- vary spacing and occasional stroke density;
- let one key word become the largest word;
- add at most one underline, tail, or pair of motion marks.

The complete phrase should usually span 62–90% of canvas width and 5–11% of canvas height. Keep spelling exact. Reject tiny centred captions, default sans/serif type, identical word sizes, rigid baselines, heavy outlines, or a font treatment reused unchanged across unrelated photos.

## 6. Texture hierarchy

Maintain two distinct material systems:

- **Photo regions:** retain original grain, focus, exposure, colour cast, reflections, weather, and motion blur. Do not apply universal paper noise over protected people.
- **Paper regions:** show scanned uncoated fibres, subtle density variation, matte ink, restrained dust, and slight registration drift at normal viewing size.

Roughness belongs to the physical edge, not to random angular polygons. Avoid smooth flat fills, universal noise, artificial torn-paper drop shadows, thick white sticker borders, and sepia filters.

At 200% zoom, confirm that paper fibres are visible in the paper field while face, hair, skin, hands, clothing, footwear, and held objects remain unchanged source pixels.

## 7. Decoration rhythm

Use 8–12 handmade stars or equivalent loose marks with three size tiers:

- 2–3 large anchors;
- 3–4 medium stars;
- 3–5 tiny punctuation marks.

Use no more than two decoration colours. Place about two-thirds in quiet zones and let the remainder lead the eye between panels. Vary rotation, fill/outline, and spacing. Avoid grids, even distribution, repeated identical symbols, edge collisions, faces, hands, phones, and important clothing details.

## 8. Final rejection gate

Reject and correct the result if any answer is no:

1. Can the people be recounted from the silhouette rhythm?
2. Does every opaque silhouette cover its complete person region with no exposed fragment?
3. Do the positive and negative states use the same recognisable mask and coupled source-photo transform?
4. Did the occupancy-aware layout create environment or paper breathing room without refusing the source?
5. Does the palette clearly belong to this source photo?
6. Does the lettering vary by word while remaining one coherent handwriting family?
7. Are paper fibres visible without damaging the photographic regions?
8. Do the stars have scale and spacing rhythm rather than mechanical scatter?
9. Are all visible people restored from protected source pixels?

Do not deliver a merely functional reciprocal mask when it fails art direction.
