# Heirloom scene colour system

Read this file before selecting any opaque silhouette, paper field, lettering, or star colour. The system converts one four-card reference into a scene-adaptive palette language; it is not a fixed four-colour template.

## Reference anchors

The reference screenshot contains two reliable named hex anchors and two visibly mismatched printed labels. When screenshot text and the visible card disagree, the visible card is the visual authority.

| Token | Working colour | Authority | Role |
| --- | --- | --- | --- |
| Shepherd's Red | `#8E372F` | printed anchor and visible card agree | deep warm dominant |
| Hearth Smoke | `#BFC4B9` | median sampled from the visible pale smoke card | light cool-neutral field |
| Butter Yellow | `#E8D297` | median sampled from the visible yellow card | gentle warm counterpoint |
| Heirloom Linen | `#FFF9F3` | printed anchor | paper light and light ink |

The complete token set lives in `assets/design-system/color-system.json`. Its extensions keep the same heritage-print properties: softened chroma, warm paper bias, low digital purity, and enough light-dark separation for reciprocal masks.

## Mandatory scene-first selection

1. Record the source's environmental family, dominant light level, one clothing/object colour anchor, and one neutral.
2. Run `scripts/select_scene_palette.py SOURCE --scene SCENE --output palette-manifest.json`.
3. Compare the three returned roles:
   - **Echo**: relates to a source garment or object without becoming indistinguishable from it.
   - **Counterpoint**: separates from the environmental hue while remaining muted.
   - **Atmosphere**: supports the emotional temperature and exposure of the scene.
4. Reject any candidate that merges with the main environment, overpowers protected people, or produces seam lettering below 3.0 contrast.
5. Record the selected token ID, exact hex, ink token, contrast ratio, and reason in the delivery manifest.

The selector is a preflight assistant, not an automatic aesthetic verdict. Human review chooses the final candidate.

## Scene routes

- **Snow or winter:** begin with Shepherd's Red, Winter Plum, Saffron Cloth, or Blue Smoke. Do not use near-white as the dominant silhouette against snow.
- **Sea and sky:** begin with Dried Persimmon, Butter Yellow, Saffron Cloth, or Harbor Slate. A blue dominant must visibly separate from the water.
- **Grass and garden:** begin with Shepherd's Red, Brick Rose, Butter Yellow, or Muted Teal. Avoid foliage-matching sage as the main silhouette.
- **Warm interior:** begin with Hearth Smoke, Blue Smoke, Oxblood Wool, or Butter Yellow. Balance wood and firelight instead of merely repeating brown.
- **City neutral:** introduce one softened blue, rose, sage, or yellow against concrete and pale architecture.
- **Night party:** use Winter Plum, Burnt Ochre, Shepherd's Red, or Harbor Slate, but confirm separation from dark clothing.
- **Sunset road:** use Saffron Cloth, Shepherd's Red, Faded Denim, or Winter Plum; avoid merging into dry earth.

These routes are candidate pools, not locked recipes.

## Page ratios and pairings

- Use one dominant paper colour, one ink/lettering colour, and at most one supporting accent.
- Let the dominant paper occupy roughly 40–60% of the complete diptych.
- Use Heirloom Linen on dark papers; use Charcoal Ink or Storm Ink on light papers.
- Use the supporting accent only for 8–12 stars, motion marks, or one small lettering terminal.
- Keep photo colours natural. Do not globally recolour protected people to match the palette.
- Apply every selected paper colour through `scripts/apply_paper_texture.py`; the hex is a dye target, not permission for a smooth digital fill.

## Rejection rules

Reject a palette when any of these are true:

- it is selected from habit rather than the source;
- it duplicates the main environmental hue so closely that the silhouette disappears;
- it uses a pure red, green, blue, cyan, or neon tone with no source justification;
- the lettering contrast is below 3.0;
- all three candidates share the same hue family;
- the same dominant is reused across unrelated photos without a scene-based reason;
- the paper colour is attractive alone but makes the complete page loud, synthetic, or commercially generic.
