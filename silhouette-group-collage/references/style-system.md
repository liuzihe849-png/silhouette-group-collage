# Style system

## The shared visual grammar

The references combine six stable choices:

1. **Vertical diptych** — one page split into two related scenes rather than one full-bleed poster.
2. **One source, two states** — the same photo is reused so the viewer can compare presence and absence.
3. **Reciprocal masking** — a solid shape in one panel becomes a window exposing the photo in the other. This is the primary style signature.
4. **Figure-ground play** — positive and negative space exchange roles; the viewer mentally completes missing subjects.
5. **Analogue construction** — rough cut edges, paper fibre, faded consumer film, dust, grain, slight print misregistration, and low-fi scanning.
6. **Youthful restraint** — naive stars and handwriting create intimacy, but never overpower the mask logic.

## Visual hierarchy

Use this priority order:

1. Recognisable source subject or scene.
2. Reciprocal mask exchange.
3. Large flat colour field.
4. Tactile paper and film texture.
5. Sparse visual punctuation.
6. One scene-matched handwritten seam phrase.

Original person pixels override every style choice. Apply paper, film, ink, and registration effects only outside protected visible-person regions. Read `art-direction-qc.md` for the mandatory palette, typography, composition, and rejection process.

If an output feels like a generic scrapbook, reduce levels 5 and 6 before changing levels 1–4.

## Group mask families

### A. Connected paper-doll silhouette

Use for a close couple or tightly clustered group. Trace the bodies as a loose paper-doll chain while retaining every head peak, count-defining gap, raised arm, lifted leg, phone, joined hand, and held object. Join only at real touches or with narrow crude bridges. Never replace the group with a convex hull, rectangular slab, saw-tooth band, or giant enclosing blob. Make the edge look cut by hand. Invert this exact silhouette between panels.

Best for: friendship, youth, group portraits, performance posters, album artwork.

### B. Separate related silhouettes

Use for people separated across a landscape or arranged at different depths. Keep every silhouette separate at its true scale and position. Relate the set through colour and a few thin crude paper bridges, never by enlarging distant people.

Best for: running groups, staggered travel groups, wide environmental portraits.

### C. Horizontal paper-doll chain

Use for people standing or moving in one horizontal line. Simplify the repeated outer contours into one jagged cut-paper band. Keep the actual number of heads, bodies, raised arms, clothing lengths, and significant gaps readable.

Best for: lakeside group portraits, dance lines, friends holding hands.

### D. Group plus companion mask

Use one group silhouette family plus one small matching mask for a thrown snowball, hat, balloon, or another source-visible companion object. Do not invent companion objects.

Best for: celebratory group moments with one airborne or held focal object.

## Layout ratios

- Default canvas: vertical 4:5; use vertical 2:3 for poster-like artwork and native 9:16 for phone wallpapers.
- Panel split: 45:55 or 50:50. A precise half split is allowed, but internal placement should remain asymmetrical.
- Flat colour coverage: 40–60% of the complete page.
- Main group masks: collectively 25–45% of one panel while preserving the source's scale and spacing.
- Quiet space: keep at least one calm region equal to roughly 15% of the page.

For 9:16, make the principal group occupy roughly 62–88% of canvas width and 42–70% of panel height. Reserve 7–12% around the seam for large handwriting overlap. Never fill the extra height with blurred, mirrored, or stretched source pixels.

## Palette recipes

Use one recipe, never all at once:

- Electric emotional: hot magenta `#F70883`, sky blue, grass green, off-white.
- Field diary: sage `#B6C596`, moss green, dusty pink, cream.
- Travel poster: vermilion `#FF4633`, pale blue, warm landscape browns, ivory.
- Youth archive: faded olive `#9CAF6A`, cream `#F4F0D8`, forest green, charcoal.

Sample colours from the source when they are already distinctive. Keep contrast strong enough that apertures read instantly.

Do not select a recipe mechanically. Compare an echo, counterpoint, and atmosphere palette from `art-direction-qc.md`; then choose one and record the reason. Reusing the same dominant colour across unrelated photos is a failure.

## Texture recipe

Describe texture as physical production, not as a filter:

`scanned uncoated paper, visible paper fibres, faded 35mm consumer-film colour, restrained dust and fine grain, slightly uneven ink density, imperfect hand-cut edges, subtle registration drift, matte surface`

Avoid heavy universal noise, fake torn-paper shadows, thick white sticker outlines, and sepia wash.

## Typography

Typography is expected for group images unless the user declines it. Derive one short lowercase phrase from visible action and setting, such as `we ran to the sea`, `we ran toward the sun`, or `together under winter skies`. Place it across the panel seam so it binds the group. Verify spelling exactly. Select brush diary, chunky marker, or loose pencil based on the scene. Span roughly 62–90% of the canvas width and vary word scale, tilt, baseline, spacing, and occasional stroke density within a coherent handwritten family. Use at most two related faces and no additional copy. Tiny centred captions and identical typography across unrelated photos fail.

## Decoration rhythm

Use 8–12 handmade stars in three size tiers rather than evenly scattering identical symbols. Use two decoration colours at most. Put roughly two-thirds in quiet zones and use the rest to guide the eye between panels. Mix filled and outline stars, vary rotation and spacing, and keep them off protected anchors.

## Source-preservation checklist

Before generating, record:

- exact person count and left-to-right order;
- foreground, midground, and background scale;
- pose, raised arms, joined hands, lifted legs, and held objects;
- distinctive clothing colours and silhouettes;
- environmental anchors such as lake, mountain, road, sea, snow, sunset, rocks, or reflections;
- source grain, focus, motion blur, exposure, and colour cast.
- protected pixel regions for every complete visible person, including faces, hair, skin, hands, clothing, footwear, and held objects.
