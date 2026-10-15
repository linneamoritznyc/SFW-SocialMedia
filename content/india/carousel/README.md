# India carousel

Six slides, 1080 x 1350, for the Accelerator Workshop on the Save Soil farm at
Coimbatore. Built 21 September 2026. Replaces the five-slide invitation post
that lived in `variants/india/post1-slide-*.html`.

| File | What it is |
| :-- | :-- |
| `slide-N.html` | the source. Edit the words here |
| `slide-N.png` | 1080 x 1350, the slide to post |
| `_carousel.css` | frame, colours and the two type sizes, shared by all six |
| `render.js` | rebuilds the PNGs and runs the four checks below |
| `caption.md` | the caption, with the photo credits at the end |

```
node content/india/carousel/render.js
```

## The rules these slides follow

- Two fonts: Montserrat 700 for headlines, Source Sans 3 for body.
- Two sizes: headline 88px (110px on the cover), body 46px. The gold last
  line on slide 6 is 54px Montserrat 700.
- All text inside the central 1080 x 1080 square, y 135 to 1215, so the 1:1
  grid crop loses nothing. The cover logo sits inside it too.
- No slide counters, no eyebrow labels, no uppercase labels, no rules, bars or
  decorative lines, no photo credit on any slide. Credits go in the caption.
- One swipe cue in the whole carousel: the cream arrow on slide 1.
- Slides 2 to 5 carry a 24px strip of the next slide's left edge at the right.

`render.js` fails if any of that slips, and prints a table of the four checks
per slide.

## The run

| | Slide | Ground | Peek at the right edge |
| :-- | :-- | :-- | :-- |
| 1 | Come to India with us | full-bleed photo, terraced fields | the arrow, not a peek |
| 2 | Ten days on the Save Soil farm | cream | slide 3, cream |
| 3 | Build compost that works | cream | slide 4, photo above cream |
| 4 | Brew the liquids | photo top half, cream below | slide 5, cream |
| 5 | Look at it all under a microscope | cream | slide 6, deep green |
| 6 | Your people are here | deep green | none, last slide |

## Two things to know

1. **The peek is invisible where cream meets cream.** Slide 2 peeks at slide
   3 and slide 4 peeks at slide 5; both neighbours are cream, so the strip is
   there in the file and shows nothing. The strips on 3 and 5 do their job.
   If every slide should move the eye, one of the cream neighbours needs a
   photo or a different ground.
2. **The photographs are Unsplash, not workshop pictures.** Terraced fields on
   the cover, hills and fields at Coimbatore on slide 4. Neither is presented
   as the Save Soil farm. Rows and photo page links are in
   `assets/india-free-images/CREDITS.md`.

## Colour

Organic Cream `#F4F1EA`, Soil Brown `#4F3433`, ink `#333130`, deep green
`#22371F`, Harvest Gold `#C9A227` on the last line of slide 6 only. Values
copied from `variants/_tokens.css`.
