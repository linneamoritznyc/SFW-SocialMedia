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
