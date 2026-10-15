# India countdown stories

Five Instagram Stories for the last hours of enrollment on the Accelerator
Workshop in Coimbatore. Post A to D in order; E is the tail card. Rebuilt
20 September 2026.

Each frame is three files:

| File | What it is |
| :-- | :-- |
| `story-x-name.html` | the source. Edit the words here |
| `story-x-name.png` | 1080 x 1920, the frame to post |
| `story-x-name-guides.png` | the same frame with the reserved areas drawn in. Planning only, never post this one |

`_story.css` holds the frame and the type scale. `prepare.py` makes the two
things CSS cannot: the knockout wordmarks and the hand cut crops.
`render.js` rebuilds the PNGs and fails if anything is drawn where a sticker
or the Instagram interface goes.

```
python3 content/india/countdown-stories/prepare.py   # crops and wordmarks
node    content/india/countdown-stories/render.js    # the ten PNGs
```

---

## The layout

A hard split. The top 45 percent, 0 to 864, is the photograph at full colour
with no scrim on it. The bottom 55 percent, 864 to 1920, is one flat brand
colour with no gradient and no transparency. They meet on a straight edge.
All type sits inside the solid block, left aligned, 90px margins, starting at
904 and ending at 1500, which leaves the bottom 420px empty for the stickers.

Fixed type: eyebrow 30px letterspaced caps, headline 88px Montserrat 700 at
1.1, body 38px Source Sans 3 at 1.5 with each fact on its own line, partner
line and credit 22px. Two frames break the headline size, and only the
headline: C and D carry the most words and would otherwise push type into the
sticker band, so their headlines are 76 and 70.

Three colour pairs, and nothing else:

| Block | Text | Eyebrow | Frames |
| :-- | :-- | :-- | :-- |
| deep green `#22371F` | Organic Cream `#F4F1EA` | Harvest Gold `#C9A227` | A, D, G |
| Soil Brown `#4F3433` | Organic Cream `#F4F1EA` | Natural Tan `#C89B7B` | B, F |
| Organic Cream `#F4F1EA` | Soil Brown `#4F3433` | Food Web Green `#156826` | C, E |

Legacy Purple is memorial content only and appears nowhere.

## The frames

| | Says | Pair | Photograph |
| :-- | :-- | :-- | :-- |
| **A** | Enrollment closes tonight | deep green | Navi, the Velliangiri Hills |
| **B** | What you do in 10 days | Soil Brown | Nitish Surelia, the peak under cloud |
| **C** | The schedule | Organic Cream | Cymatics, light through storm cloud |
| **D** | $5,000, everything on site included | deep green | Ranjini Hemanth, the terraces |
| **E** | These dates do not work? | Organic Cream | Gowtham AGM, sunset |
| **F** | Enrollment extended | Soil Brown | Remi Clinton, misty farmland |
| **G** | Still time to enroll | deep green | Div, sunrise over the ridge |

A, B, C, D, F and G link to
`school.soilfoodweb.com/courses/india-workshop-2026`. E links to
`school.soilfoodweb.com/pages/workshop-interest` and is the only frame that
does not point at the workshop page.

**F and G are extended-deadline alternates for A**, for when the closing time
moves. Never post one alongside A. Neither prints a date: the countdown
sticker carries the new closing time and stays right as the hours pass. To
print it instead, replace the line marked `data-field="note"` and re-render.

## The build

```
python3 content/india/countdown-stories/prepare.py   # crops and wordmarks
node    content/india/countdown-stories/render.js    # the PNGs, with the audit
```

`prepare.py` cuts each 1080 x 864 crop by hand, with its box and its reason,
and makes the cream and Soil Brown knockouts of the wordmark.

`render.js` refuses to finish unless every frame passes four checks: every
line of type sits inside the solid block between 864 and 1500, every text
colour is the one its pair allows, the last body line clears the fine print,
and the mark sits on the photograph below the interface band. It prints what
it measured for each frame.

## The facts, and where they come from

Everything on these frames is on the live enrollment page at
`school.soilfoodweb.com/courses/india-workshop-2026`: the dates, the ten
days, the week one and week two agendas, the $5,000 and $5,500 rates, the 13
nights and meals at the Isha Yoga Center, the daily shuttle to the farm, the
payment plans, and the resident rate by email. The partner credit reads
**Isha Outreach**, which is how that page credits the collaboration, and it
matches `content/calendar.json` and `drafts/2026-10-16-india-four-events.md`.

The hours remaining are not written on any frame, on purpose. The countdown
sticker carries that and stays right as the hours pass.

No photograph here is a workshop photograph and nothing on these frames
suggests otherwise. See `assets/india-free-images/README.md`.
