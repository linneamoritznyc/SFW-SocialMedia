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

## The set

Every frame carries the same four things: the eyebrow naming the workshop,
the headline, the facts on their own lines, and the partner credit. Body text
is 32 to 34px and the partner line is 26px, because at 1080 wide the frame is
about 400 physical pixels across and anything smaller cannot be read in the
hand.

| | Layout | Says | Colour family | Photograph |
| :-- | :-- | :-- | :-- | :-- |
| **A** | headline only, very large | Enrollment closes tonight / Coimbatore, India · Oct 19 to 30 | Soil Brown scrim, cream type, **Harvest Gold** headline | Navi, the Velliangiri Hills |
| **B** | headline bottom left, photo open at the top | Learn with your hands in the pile / Coimbatore, India · Oct 19 to 30 | Food Web Green scrim, cream type, **Natural Tan** support | Nitish Surelia, the peak under cloud |
| **C** | two stacked week lines, thin cream rule between | Week 1 and Week 2 | deep green scrim, cream type, **Light Green** labels | Cymatics, light through storm cloud |
| **D** | cream card at bottom left, 55% of the width | Payment plans available / India residents: email us for local pricing | cream card, Soil Brown type, **Education Blue** pricing line | Ranjini Hemanth, the terraces |
| **F** | extended deadline, alternate for A | Enrollment extended | Soil Brown scrim, cream type, **Harvest Gold** headline | Remi Clinton, misty farmland |
| **G** | extended deadline, alternate for A | Still time to enroll | Soil Brown scrim, cream type, **Harvest Gold** headline | Div, sunrise over the ridge |
| **E** | type left, under an open sky | Can't make these dates? / Join the list for future workshops | Natural Tan scrim, Soil Brown type, **Food Web Green** call to action | Gowtham AGM, sunset |

**F and G are extended-deadline alternates for A**, for when the closing time
moves. They carry A's colour family, including Harvest Gold, because they are
the same frame with a new deadline, so never post one alongside A. Neither
prints a date: the countdown sticker carries the new closing time and stays
right as the hours pass. To print the date instead, replace the line marked
`data-field="note"` and re-run `render.js`.

A to D, F and G link to `school.soilfoodweb.com/courses/india-workshop-2026`. E links to
`school.soilfoodweb.com/pages/workshop-interest` and is the only frame that
does not point at the workshop page: it is for the people these dates do not
fit.

Harvest Gold is on A and nowhere else. Legacy Purple #6B4C7A is memorial
content only and appears nowhere. One accent colour per frame.

**Two approved lines are not used in this set:** "Last hours to enroll" and
"10 days on the Save Soil farm with the Soil Food Web team". Both are still
yours; say the word and either one swaps into A or B.

---

## How a frame is built

A full bleed photograph at full colour, then a scrim that is clear across the
top and holds at 85 percent from 55 percent down, then type on the dark part.
The three dark scrims (A, B, C) multiply rather than cover, so the ridge
lines and the cloud survive underneath and the colour reads as a grade rather
than paint. E's Natural Tan sits under dark type, the opposite job, so it
stays a normal scrim. D has no scrim at all: the cream card carries the words,
so the terraces need nothing done to them.

The wordmark is a one colour knockout, 120px, no box: cream on A to D, Soil
Brown on E because that scrim is light. `prepare.py` makes both from the
supplied logo.

The crops are cut by hand in `prepare.py`, each with its box and the reason,
because CSS can only choose one axis when the picture and the frame disagree
this much. The subject sits in the top half of every frame, clear of the type.

---

## The reserved areas

| Area | Box | Who fills it |
| :-- | :-- | :-- |
| Instagram interface, top | 1080 x 250 at the top | nobody. Kept clear |
| Instagram interface, bottom | 1080 x 250 at the bottom | nobody. Kept clear |
| Countdown sticker | 700 x 300 at x 190, y 1120 | you, in the Instagram app |
| Link sticker | 640 x 160 at x 220, y 1490 | you, in the Instagram app |

All type ends at 1100, twenty pixels above the countdown box. `render.js`
checks every text box, the card and the wordmark against all four areas on
every build and exits non zero if anything overlaps.

---

## Contrast, measured off the rendered PNGs

| | Measured | Threshold | |
| :-- | :-- | :-- | :-- |
| A, gold headline on the brown scrim | 5.53:1 | 3:1 large | passes |
| B, tan support on the green scrim | 5.86:1 | 3:1 large | passes |
| C, Light Green labels at 44px | 3.63:1 | 3:1 large | passes |
| D, Education Blue pricing line at 32px | 3.73:1 | 3:1 large | passes |
| E, Food Web Green call to action at 34px | **2.84:1** | 3:1 large | **short** |

Light Green is marked decorative in the brand guide and banned for text; at
44px it is large text, where the threshold is 3:1, which is why it works here
and would not at body size.

Food Web Green on Natural Tan cannot pass: the two colours are 2.78:1 against
each other at best. Deep green #22371F on the same tan measures 5.15:1 and
keeps the family. One line in `story-e-next.html` changes it.

---

## What is on these frames, and what is not

Only the facts supplied for this deadline: the name in full, the place, the
dates, the two weeks' content, payment plans, local pricing for India
residents, and the interest list. No price, no attendance number, no claim
about results. The hours remaining are not written on any frame, on purpose:
the countdown sticker carries that and stays right as the hours pass.

The partner line reads **Isha Foundation**, as supplied.
`content/calendar.json` and `drafts/2026-10-16-india-four-events.md` both say
*Isha Outreach*, the outreach arm of the same organisation. The dates follow
`content/calendar.json`, 19 to 30 October 2026, verified against the live
enrollment page on 11 September 2026.

No photograph here is a workshop photograph and nothing on these frames
suggests otherwise. See `assets/india-free-images/README.md`.
