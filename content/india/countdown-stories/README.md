# India countdown stories

Five Instagram Story options for the last hours of enrollment on the
Accelerator Workshop in Coimbatore. Built 20 September 2026.

Each option is three files:

| File | What it is |
| :-- | :-- |
| `story-x.html` | the source. Edit the words here |
| `story-x.png` | 1080 x 1920, the frame to post |
| `story-x-guides.png` | the same frame with the reserved areas drawn in. Planning only, never post this one |

`_story.css` holds the frame, the colours and the type scale for all five.
`render.js` rebuilds the PNGs and refuses to finish if anything has been drawn
where a sticker or the Instagram interface goes.

```
node content/india/countdown-stories/render.js
```

---

## The five

| | Says | Link sticker |
| :-- | :-- | :-- |
| **A** | Last hours to enroll / Accelerator Workshop, Coimbatore, India, Oct 19 to 30 | `school.soilfoodweb.com/courses/india-workshop-2026` |
| **B** | Enrollment closes tonight / 10 days on the Save Soil farm with the Soil Food Web team | same |
| **C** | Week 1 and Week 2, what the days contain | same |
| **D** | Learn with your hands in the pile / payment plans, and local pricing for India residents | same |
| **E** | Can't make these dates? / Join the list for future workshops | `school.soilfoodweb.com/pages/workshop-interest` |

Both addresses are on `school.soilfoodweb.com` and both are recorded in
`content/calendar.json` and `docs/link-map.md`. E deliberately does not link to
the workshop page: it is for the people that set of dates does not fit.

The partner line, on all five where it fits: *with the Isha Foundation and the
Conscious Planet Save Soil movement*.

---

## The reserved areas

The numbers are the same in `_story.css` and in `render.js`, and the guides PNG
shows them.

| Area | Box | Who fills it |
| :-- | :-- | :-- |
| Instagram interface, top | 1080 x 250 at the top | nobody. Kept clear |
| Instagram interface, bottom | 1080 x 250 at the bottom | nobody. Kept clear |
| Countdown sticker | 700 x 300 at x 190, y 1120 | you, in the Instagram app |
| Link sticker | 640 x 160 at x 220, y 1490 | you, in the Instagram app |

All readable content sits between y 250 and y 1100. The lowest line of text on
any of the five ends at 1100, which leaves 20px of air above the countdown box.

---

## Colour

Deep green `#22371F` is the field. Organic Cream `#F4F1EA` is a shape and never
the page. Glow `#DBE6A7` is the small accent. Montserrat for headings, Source
Sans 3 for body. Values are copied from `variants/_tokens.css`.

**Harvest Gold `#C9A227` appears on A and B only, on the deadline line.** Note
for Stephanie: `variants/README.md` records gold as reserved for donate calls
and says gold in a Field Notes graphic is a bug. These are not Field Notes, and
the gold here is doing the job you asked of it, marking the deadline and
nothing else. If she wants that rule held everywhere, the two headlines go cream
and nothing else changes.

---

## Photographs

Every frame works with no photograph, which is why they can post today.

To add one: uncomment the `.photo` block at the top of a story file, point it at
a file in `assets/india-free-images/`, uncomment the `.credit` line at the
bottom and put the photographer's name in it, add the row to
`assets/india-free-images/CREDITS.md`, then re-run `render.js`. A dark green
wash sits over the picture so the type keeps its contrast.

Unsplash pictures are not workshop photographs and nothing here may suggest they
are. See `assets/india-free-images/README.md`.

---

## What is on these frames, and what is not

Only the facts supplied for this deadline: the name in full, the place, the
dates, the ten days, the two weeks' content, payment plans, local pricing for
India residents, and the interest list. No price, no attendance number, no
claim about results.

Two things to check before posting:

1. **"Isha Foundation" or "Isha Outreach".** The partner line here says Isha
   Foundation, as supplied. `content/calendar.json` and the four-events draft
   both say *Isha Outreach*. One of the two is wrong and it is a partner's own
   name, so it is worth thirty seconds with Evan.
2. **The dates.** `content/calendar.json` has 19 to 30 October 2026 marked
   verified against the live enrollment page, checked 11 September 2026. Copy
   deck DECISION 12 records a date conflict elsewhere on the old site, in the
   footer, the FAQ and the inclusions list. The frames follow calendar.json.

The hours remaining are not written on any frame, on purpose. The countdown
sticker carries that and stays right as the hours pass; typed-in text does not.
