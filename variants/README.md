# Field Notes, seven visual directions

Seven standalone 1080 by 1080 HTML files, all showing the same trial so they can
be compared like with like. Open `index.html` to see them all on one page and
screenshot it whole. Open any numbered file on its own to see it at full size.

The trial in all seven: Sandra Niggemeyer, Van, Texas, 2026 season. Butternut
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

## The seven directions

### 1. Number first

**What it is good for.** The scroll stopper. One statistic at 320px filling the
frame, with the two numbers that keep it honest sitting on a cream plate
underneath. Works when the trial has one finding big enough to carry a whole
post, which is not every trial.

**Pillar.** Community Voice. The number does the work, so it reads as evidence
rather than as a congratulation.

**Watch for.** It is the easiest of the seven to make dishonest. The control
plot gained 14% on its own, and that number has to stay on the card. A 46% with
nothing beside it implies the compost did all of it.

**Time to update.** About 5 minutes. Swap four numbers, a name, a place and the
source line.

### 2. Portrait led

**What it is good for.** The only direction that makes the post about a person
rather than a result. It is what most organisations would reach for first, and it
is the one this one currently cannot do.

**Pillar.** Community Voice.

**Watch for.** It ships blocked on purpose. The frame holds a dashed placeholder
listing the three conditions, which follows the house convention of a visible
dashed box rather than filler. Do not put a stock face in it. Do not put a
mentor's face in it either.

**Time to update.** About 10 minutes once the photograph exists, plus however
long consent takes. Budget the consent request as the long pole, not the design.

### 3. Data card

**What it is good for.** LinkedIn, and anywhere the audience is a practitioner
who wants the actual numbers. Two small bar charts, drawn in plain HTML, no
library.

**Pillar.** Community Voice, though it reads as Science Explained and can be
scheduled as either.

**The chart rules, so a Canva rebuild keeps them.**

- One measure per chart. Percent and ounces never share an axis. Two measures
  means two charts.
- Every bar starts at zero. Never trim the baseline to make a difference look
  bigger.
- One colour for every bar in a chart. Length carries the magnitude and the
  label carries the identity, so no legend is needed and colour blindness cannot
  break it. Do not colour-code the plots.
- Every bar is labelled with its own value.

**Bar arithmetic for the next graduate.** Pick a round number above the largest
value and use it as the full width. Organic matter here: largest is 46, round up
to 50, so each bar's width is `value / 50 × 100%`. That gives 92%, 28% and 2%.
Harvest: largest is 35, round up to 40, so 87.5%, 75% and 47.5%. Keep the same
ceiling for every bar within one chart or the comparison is a lie.

**Time to update.** About 15 minutes. The bar widths are the fiddly part and the
only place in the set where you can make an arithmetic mistake that looks fine.

### 4. Field photograph

**What it is good for.** Instagram feed and the top of a carousel. Full bleed,
one line, nothing else.

**Pillar.** Community Voice.

**Watch for.** The weakest evidence in the set until a real plot photograph
arrives, because a library photograph of somebody else's hands proves nothing
about Sandra's ground. The stand-in is named in the card's own source line so
that nobody can forget. Strategy guidance already says field photos and data
graphics beat stock; a Foundation library photo standing in for a specific claim
is the same trap one step removed.

**Time to update.** About 5 minutes to set. Getting a usable photograph from the
graduate is the actual cost, and that is a request, not a design task.

### 5. Quote card

**What it is good for.** Shipping this week. It needs no photograph of anyone,
so it carries no consent blocker on the image, and it is the only direction that
puts the graduate's own thinking in front of her results.

**Pillar.** Community Voice, reads as The Bigger Picture.

**Watch for.** The sentence has to be hers and has to be quoted accurately.
Sandra's is "soil biology rebuilds the ground before it rebuilds the yield",
which is unusually good. Most reports will not hand you one that clean, and a
tidied-up paraphrase in quotation marks is not a quote. If there is no sentence,
this direction does not run.

**Time to update.** About 5 minutes to set, plus perhaps 15 minutes reading the
report to find a sentence worth setting.

### 6. The honest ledger

*Not on the brief. Added because the series promise asked for it.*

**What it is good for.** The post that earns the series its credibility. Three
plots, three measures, and the three things that went wrong, all on one card.
The tea plot gained 1% organic matter and carried the fewest squash bugs. The
control gained 14% on water alone. Neither fact is convenient and both are on the
card.

**Pillar.** Community Voice. This is the one that delivers "we publish what the
trial found, including when the results disappoint" rather than just claiming it.

**Watch for.** It is a table, not a chart, because percent, ounces and a pest
count share no axis. Do not let anyone redraw it as a single graph. It is also
the densest of the seven and the least suited to a phone glance, so it belongs
mid carousel rather than as slide one.

**Time to update.** About 20 minutes, and it is the only one that needs the whole
report rather than the summary. You need every result and every failure, and
Carla should science-check the takeaway before it goes to Stephanie.

### 7. Specimen sheet

*Not on the brief. Added because her own report already solved the layout.*

**What it is good for.** Turning the structure of a field trial into the design
itself. Three plates on a pale green ground, labelled A1, B and C1, which are
Sandra's own labels from page 16. It reads as a specimen case rather than a
social graphic, which is the register the brand is already in.

**Pillar.** Community Voice, reads as Science Explained.

**Watch for.** The plate labels belong to the graduate, not to us. If the next
report labels its plots 1, 2 and 3, the card says 1, 2 and 3. Inventing tidier
labels would be inventing data. This is also the direction that most wants the
real page 16 photograph sitting beside it in a carousel.

**Time to update.** About 15 minutes, and it needs the graduate's own plot
labels, which means opening the report rather than working from the summary.

---

## What I would put in front of Stephanie

Three, not seven: **5 the quote card**, because it can run this week with no
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
