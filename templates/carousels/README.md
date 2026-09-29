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
