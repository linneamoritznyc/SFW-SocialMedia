# Field Notes, twenty seven visual directions

Twenty seven standalone HTML files, twenty five of them 1080 by 1080, all showing the same trial so they can
be compared like with like. Open `index.html` to see them all on one page and
screenshot it whole. Open any numbered file on its own to see it at full size.

The trial in all of them: Sandra Niggemeyer, Van, Texas, 2026 season. Butternut
squash on clay and sand that sat fallow for twenty years. Three plots.

Built 17 September 2026 for the Thursday Field Notes series, Community Voice
pillar. The output of this folder is a visual reference a human rebuilds in
Canva, not a publishing step.

---

## Read this before you pick one

**1. The current graduate graphic is purple, and purple is not available.**
Legacy Purple `#6B4C7A` is reserved for Dr. Elaine Ingham memorial content, with
no exceptions. The existing graduate template breaks that rule. All seven
directions here are green and cream instead. Harvest Gold `#C9A227` (donate calls
only) and Green Legacy `#59A66C` (decorative, fails contrast, never text) are
also absent from every file. If you find any of the three in a Field Notes
graphic, it is a bug.

**2. Consent is not currently being obtained, and two of these need it.**
The 8 September notes record consent as required and missing. Direction 2 cannot
run at all until the graduate says yes in writing and gives a handle to tag.
Nothing here should name a person before that either. Direction 5, the quote
card, is the only one that needs no photograph of anybody, which is why it is the
safest thing to ship first.

**3. There is no photograph of Sandra's plot in this repository.**
Direction 4 uses `assets/photo/red-soil-hand.jpg` from the Foundation library as
a stand-in and says so in its own source line. The picture this series actually
wants is page 16 of her report: three sheets of brown paper labelled A1, B and C1
with the squash from each plot laid out. Direction 7 is built to be the design
equivalent of that page until the page itself is cleared.

**4. The harvest is measured in ounces and that is a small sample.**
Thirty five ounces against nineteen is a real difference and roughly two pounds
against one. Turning it into "84 percent more squash" would be overclaiming from
a single unreplicated season. Every direction that shows the harvest shows the
ounces and says the sample is small.

**5. One thing to rule on.** The series label reads FIELD NOTES in uppercase.
The copy deck says sentence case for headings. An eyebrow is a label rather than
a heading, and the stylesheet lists eyebrows as a use of Food Web Green, so this
is probably fine. Stephanie should say either way, because it appears in all
seven.

---

## The six swappable fields

Identical in all seven files, marked in the markup with `data-field`, and listed
in a comment block at the top of every file in the same order.

| Field | In Sandra's post | Where it comes from |
| :-- | :-- | :-- |
| `hero-number` | 46% | The headline finding of the trial |
| `place` | Van, Texas | Carla's announcement |
| `headshot` | empty | The graduate, after consent. Directory application if one exists |
| `test-question` | Can soil biology rebuild ground that sat fallow for twenty years? | What the trial set out to answer |
| `soil-result` | 46% / 14% / 1% organic matter gained | The report |
| `crop-result` | 35 oz / 30 oz / 19 oz squash | The report |

Two identity fields travel with them and are marked the same way: `name` and
`season`.

Every number also needs its source line. That is a brand rule, not a nicety: no
unattributed percentages. The line names the graduate's report and the year.

---

## The eighteen directions

Grouped by what they are for. Time to update is for the next graduate, once the
report has been read.

### Lead with a number

| # | Direction | Good for | Time |
| :-- | :-- | :-- | :-- |
| 1 | **Number first** | The scroll stopper. Deep green, statistic at 320px, microscopy drifting behind. Needs one finding big enough to carry a post | 5 min |
| 9 | **Statement** | Her conclusion at 104px on glow green, no photograph at all. Cheapest to make, travels well as a repost | 4 min |
| 16 | **Graduate announcement** | The celebration card proper, the direct replacement for the purple one | 8 min |

### Lead with the data

| # | Direction | Good for | Time |
| :-- | :-- | :-- | :-- |
| 3 | **Data card** | LinkedIn and practitioners who want the numbers. Two charts, one measure each | 15 min |
| 6 | **The honest ledger** | The post that earns the series its credibility. Every result and every failure | 20 min |
| 7 | **Specimen sheet** | Her own plate labels, A1, B and C1, each carrying a real organism | 15 min |
| 8 | **Split, control against compost** | Two photographs, one number each, a hard line between. Reads instantly at thumbnail size | 8 min |
| 11 | **Expected against happened** | Sets up the assumption, then breaks it. The most shareable structure in the set | 12 min |
| 14 | **The season** | What happened in order, with the failures marked. Good mid carousel | 12 min |

### Lead with a picture

| # | Direction | Good for | Time |
| :-- | :-- | :-- | :-- |
| 2 | **Portrait led** | The only one that makes the post about a person. Ships blocked on consent | 10 min + consent |
| 4 | **Field photograph** | Instagram feed, top of a carousel. Full bleed, one line | 5 min |
| 10 | **Carousel opener** | Built to be slide one and nothing else. Centred question, swipe prompt | 5 min |
| 13 | **Cover** | Masthead and issue number. Treats the series as a publication, which helps it feel like one | 10 min |
| 15 | **Microscopy hero** | The organism as the subject. The one picture type no other soil account has | 8 min |

### Lead with the writing

| # | Direction | Good for | Time |
| :-- | :-- | :-- | :-- |
| 5 | **Quote card** | Shipping this week. No photograph of anyone, so no consent blocker on the image | 5 min + reading |
| 12 | **Run your own trial** | The save. Four steps a grower can copy onto their own ground | 15 min, reusable |

### Other formats

| # | Direction | Good for | Time |
| :-- | :-- | :-- | :-- |
| 17 | **Feed post, 4:5** | 1080 x 1350, the tallest crop Instagram allows in feed. If only one format gets built, build this one | 10 min |
| 18 | **Story and reel cover, 9:16** | 1080 x 1920, with the app's interface zones marked so nothing important sits under them | 10 min |


### Built at the phone legibility floor

A 1080 square is about 390px wide in an Instagram feed, so everything in these
frames is seen at roughly 36 percent of the size it is drawn at. The floor,
written at the bottom of `_tokens.css`:

| Drawn at | Seen at | Used for |
| :-- | :-- | :-- |
| 28px | 10px | credit and source lines. Never go under this |
| 34px | 12px | supporting text |
| 40px | 14px | the line people actually read |
| 56px | 20px | sub headings and stat labels |
| 80px | 29px | headlines |
| 160px+ | 58px+ | hero numbers |

**If a layout will not fit at these sizes, cut words, not type.** That is how
every card here was fixed when the type went up.

### Fast to make, one number each

| # | Direction | Good for | Time |
| :-- | :-- | :-- | :-- |
| 19 | **One number** | Nothing but the figure at 440px. The simplest thing in the set | 3 min |
| 21 | **One word** | FALLOW at 210px over dry soil. Built to work as a thumbnail | 4 min |
| 23 | **Four numbers** | The whole season as a 2 by 2 grid. Fastest to read | 6 min |

### Teaching and engagement

| # | Direction | Good for | Time |
| :-- | :-- | :-- | :-- |
| 20 | **Myth and measurement** | What people say, struck through. What she measured, underneath | 8 min |
| 22 | **The mechanism** | Three steps of soil biology. Sits in Science Explained as easily as here | 10 min, reusable |
| 24 | **The question** | Engagement post. One question, one prompt | 4 min |
| 25 | **Carousel end card** | The series promise and the cadence. Reuse unchanged on every post | 0 min after the first |
| 26 | **Three plots, three photographs** | One number on each. Reads at any size | 8 min |
| 27 | **If you change one thing** | Keep a control plot, and why her 14% proves it | 8 min |

### Notes that apply across the set

- **Direction 3, the chart rules.** One measure per chart, percent and ounces never
  share an axis. Every bar starts at zero. One colour per chart: length carries
  magnitude, the label carries identity, so no legend is needed and colour
  blindness cannot break it. To rescale, pick a round ceiling above the largest
  value and set each width to `value / ceiling x 100%`. Keep one ceiling per chart.
- **Direction 6 is a table, not a chart.** Percent, ounces and a pest count share
  no axis. Do not let anyone redraw it as a single graph.
- **Direction 7's plate labels belong to the graduate.** If the next report labels
  its plots 1, 2 and 3, the card says 1, 2 and 3. Tidier labels would be invented
  data.
- **Directions 4, 8, 10, 13 and 17 use library photographs as stand-ins** and say
  so in their own source lines.

## What I would put in front of Stephanie

Three, not twenty seven: **5 the quote card**, because it can run this week with no
consent blocker on the image; **1 number first**, because it is the scroll
stopper and the fastest to repeat; and **6 the honest ledger**, because it is the
one that decides what kind of series this is.

If she wants a single carousel instead of a single card, the order that works is
4 or 7 as the opening frame, then 1, then 3, then 6, then 5 to close.

---

## How these are built

No framework, no build step, no npm. Each file is standalone HTML with its own
styles inline and one shared stylesheet, `_tokens.css`, holding the colour tokens
and the `@font-face` rules.

**Colours** are copied verbatim from the `:root` block of the old `css/site.css`,
which is recorded in full in `INVENTORY.md` at the repository root. Nothing is
invented. There is one shadow value in the brand, `0 2px 12px rgba(79, 52, 51,
0.10)`, and it is the only shadow used here.

**Cream** `#F4F1EA` appears only as a bound rectangle behind a group, never as a
page background, which is what the stylesheet says it is for. Direction 7 uses
`--panel-green` `#E6EADC` in exactly the role its own comment describes: a pale
green ground set behind a group of plates to bind them into one object. This also
matches the meeting record, where beige as a background was rejected by both Evan
and Linnea and the direction was settled as green and light green.

**Type** is the self-hosted Montserrat, Source Sans 3 and EB Garamond in
`assets/font/`. Montserrat carries headings and numbers, Source Sans 3 carries
body and source lines, EB Garamond carries the quote and the serif ledes.

**Note on paths.** These files point at `assets/font/` and `assets/photo/`, not
`fonts/` and `img/`. Those folders were reorganised into `assets/` earlier, and
`css/site.css` has been deleted after its tokens were extracted into
`INVENTORY.md`. If a font or photograph does not load, that is why.

**To render one as an image**, open it in a browser at 100% and screenshot the
square, or use the bundled Chromium:

    /opt/pw-browsers/chromium-1194/chrome-linux/chrome --headless --no-sandbox \
      --force-device-scale-factor=1 --window-size=1080,1180 \
      --screenshot=out.png file:///absolute/path/to/01-number-first.html

Crop to the top 1080 by 1080. Chromium's window height is not the viewport
height, so asking for exactly 1080 gives you a short frame.
