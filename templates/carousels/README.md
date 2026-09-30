# Carousel templates (PPTX)

1080 x 1350, colours and fonts from `variants/_tokens.css` (Montserrat, EB Garamond, Source Sans 3; install them before opening).
Every content text box starts with `[COPY: Allison]`. Fixed labels (series name, "Save this", handle) do not.
Photo, diagram and icon boxes are marked `[PHOTO]`, `[DIAGRAM]`, `[ICON]`. Speaker notes on each slide carry the rule for that slide.

| File | Slides |
| :-- | :-- |
| soil-regenerators-in-the-wild.pptx | 5 |
| field-notes.pptx | 6 |
| did-you-know.pptx | 5 |
| numbered-checklist.pptx | 7 |

Rebuild: `pip install python-pptx && python3 build.py`.
Rules kept: every number needs a source line, no invented facts (placeholders describe the shape, not a claim),
Harvest Gold `#C9A227` only on the graduate result number and the checklist "Save this" label.

## Dated posts (`posts/`)

One PPTX per post, named `DD-MM-YYYY-day-slug.pptx` (day first, so the earliest date in a month sorts to the top; it does not sort across months). The date and post name are also in each file's title and at the top of every slide's speaker notes.
Change `START` in `build.py` to move the whole two-week plan, then run `python3 build.py`.

| Date | Post |
| :-- | :-- |
| Mon 5 Oct 2026 | World Teachers' Day: five mentors (`build_week1.py`) |
| Tue 6 Oct 2026 | Dr. Carla Portugal (`build_week1.py`) |
| Wed 7 Oct 2026 | Soil Regenerators in the wild #1 |
| Fri 9 Oct 2026 | Numbered checklist |
| Mon 12 Oct 2026 | Field Notes |
| Wed 14 Oct 2026 | Soil Regenerators in the wild #2 |
| Fri 16 Oct 2026 | Did you know #2 |
