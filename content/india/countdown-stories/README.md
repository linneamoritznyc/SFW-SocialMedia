# India countdown stories

A run of four Instagram Stories for the last hours of enrollment on the
Accelerator Workshop in Coimbatore, plus a fifth tail card. Post 1 to 4 in
order, a few minutes apart. Built 20 September 2026.

Each frame is three files:

| File | What it is |
| :-- | :-- |
| `story-N-name.html` | the source. Edit the words here |
| `story-N-name.png` | 1080 x 1920, the frame to post |
| `story-N-name-guides.png` | the same frame with the reserved areas drawn in. Planning only, never post this one |

`_story.css` holds the frame, the colours and the type scale for all five.
`render.js` rebuilds the PNGs and fails if anything has been drawn where a
sticker or the Instagram interface goes.

```
node content/india/countdown-stories/render.js
```

---

## The run

Every frame carries the wordmark on a cream rectangle at the top, and the
Velliangiri Hills photograph from the lower half down to the bottom edge.

| | Frame | Carries | Stickers to add |
| :-- | :-- | :-- | :-- |
| 1 | **Closing** | Last hours to enroll / Enrollment closes tonight, in gold, and the standing facts | countdown **and** link |
| 2 | **Why attend** | Learn with your hands in the pile / 10 days on the Save Soil farm with the Soil Food Web team | countdown and link |
| 3 | **What you will learn** | Week 1 and Week 2 | countdown and link |
| 4 | **More info** | Payment plans available / India residents: email us for local pricing | countdown and link |
| 5 | **After the run** | Can't make these dates? / Join the list for future workshops | link only |

Frames 1 to 4 link to `school.soilfoodweb.com/courses/india-workshop-2026`.
Frame 5 links to `school.soilfoodweb.com/pages/workshop-interest` and is the
only one that does not point at the workshop page: it is for the people these
dates do not fit. Post it after the deadline passes, or alongside frame 4 if
you want it in the same run.

Frames 1 and 3 repeat the standing facts as a strip, so anyone who joins the
run halfway still gets where, when and how long: Coimbatore, India · Oct 19 to
30 · 10 days. The partner line runs along the bottom of all five: *with the
Isha Foundation and the Conscious Planet Save Soil movement*.

The countdown zone is reserved on all five. If you skip the countdown sticker
on 2 to 5, that is 700 x 300 of free space and nothing needs re-rendering.

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

All readable content sits between y 250 and y 1103, which leaves at least 17px
of air above the countdown box.

---

## Colour

Deep green `#22371F` is the field. Organic Cream `#F4F1EA` is a shape and never
the page. Glow `#DBE6A7` is the accent. Montserrat for headings, Source Sans 3
for body. Values are copied from `variants/_tokens.css`.

Harvest Gold `#C9A227` appears on frame 1 only, on the deadline line, which is
the rule you set. `variants/README.md` reserves gold for donate calls in the
Field Notes series; these are not Field Notes and the gold is doing one job
here. If Stephanie wants that rule held everywhere, the headline goes cream and
nothing else changes.

---

## Photographs

Every frame works with no photograph, which is why they can post today.

All five use `navi-EkQEfFhmhrg-unsplash.jpg`, the Velliangiri Hills at
Coimbatore. To swap it, point the `.photo` block at another file in
`assets/india-free-images/`, add that file's row to `CREDITS.md`, then re-run
`render.js`. The scrim over the picture is near solid where the words are and
opens up below them, which is where the stickers go.

No photographer credit is printed on the frames. Unsplash asks for a credit
rather than requiring one, and the decision here is not to carry one. The
credit still belongs in `CREDITS.md`.

Upload pictures here, in the browser:
<https://github.com/linneamoritznyc/SFW-SocialMedia/upload/claude/upbeat-babbage-ggergv/assets/india-free-images>

Unsplash pictures are not workshop photographs and nothing here may suggest they
are. See `assets/india-free-images/README.md`.

---

## What is on these frames, and what is not

Only the facts supplied for this deadline: the name in full, the place, the
dates, the ten days, the two weeks' content, payment plans, local pricing for
India residents, and the interest list. No price, no attendance number, no
claim about results. The section labels (Why attend, What you will learn, More
info) in the file names and the field labels (Where, When, How long) are
structure, not claims.

The hours remaining are not written on any frame, on purpose. The countdown
sticker carries that and stays right as the hours pass; typed-in text does not.

Two notes for the record, nothing to action:

1. The partner line says **Isha Foundation**, as supplied.
   `content/calendar.json` and `drafts/2026-10-16-india-four-events.md` both say
   *Isha Outreach*, which is the outreach arm of the same organisation. The
   frames follow what was supplied for this post.
2. The dates follow `content/calendar.json`, 19 to 30 October 2026, marked
   verified against the live enrollment page and checked 11 September 2026.
   Copy deck DECISION 12 records a date conflict elsewhere on the old site.
