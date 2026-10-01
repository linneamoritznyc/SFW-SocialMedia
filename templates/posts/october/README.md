# October 2026 posts

`python3 build_october.py` rebuilds everything: 9 template masters in `_templates/`, 27 posts here, and `PHOTO-PLACEHOLDERS.md`.
Templates and helpers live in `lib.py`; the post list is in `build_october.py`.

Decisions made while building (change them in `lib.py`):
- Sizes are real points on an 11.25 in wide slide, exactly as in the spec.
- Logo placeholder sits bottom right on covers and closing slides. Left off: trading-card slides (the card fan and cards fill the space), the two-photo mentor cover, story/reel caption cards.
- On cream backgrounds the logo outline is Deep Green, because a Cream outline would be invisible.
- Gold is used only on donate slides and the compost warning icons. The underwear "Still whole?" badge is Soil Brown so it is not gold.
- Reel caption cards (6B) have no page background. Cream text is invisible on a white page: remove the page background in Canva or export PNG with transparent background.
- Numbers on big-number slides carry a "Source: [COPY: Allison]" line.
- Card texture uses PowerPoint's diagonal pattern fill, not exact 2 px / 18 px lines.

## Brand fonts (the three starred fonts in Canva)
- **Montserrat**: headings, labels, names, series and date pills, the soilfoodweb.com line.
- **Source Sans 3**: body text and descriptive lines ("How he feeds his soil: living groundcover, ...").
- **EB Garamond, italic**: the human voice. Quotes from graduates and mentors (Soil Regenerators in the wild), Field Notes observations, pull quotes.
- No other fonts. Emoji show in the system emoji font.

## Logo and website
- Logo on the first and last slide of a carousel.
- soilfoodweb.com, small and centred at the bottom, on every other slide (Stephanie, 30 Sep 2026).
- No slide numbers.

## Seamless carousel (also called panoramic or split carousel)
One extra-wide background cut into equal 1080 x 1350 slices, so the design flows across the edges when you swipe.
- Background: `python3 tools/make_hyphae_panorama.py <out-dir> gold green brown ...` (one colour per slide). Hyphae cross every
  seam; each slide keeps its own colour in the middle and blends into the next one at the edge.
- Layout: one fixed grid on every slide (same photo area, same text card size and position, same footer), so only the
  content changes as you swipe (Stephanie, 30 Sep 2026).
- Example: `build_boubacar_panorama.py`.
