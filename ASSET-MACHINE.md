# Asset machine, a proposal

What to build next in this repository, and what to leave alone. 17 September 2026.

You described three pieces: an inventory of every asset with descriptions, a
slash command that turns a graduation announcement into a finished carousel plus
asset paths, and a status script counting days of scheduled content ahead. Here
is what I would actually build.

## Build: the inventory. It already exists.

`INVENTORY.md` is done, at the repository root. 273 files with path, dimensions,
duration and a description written so that searching for "hands", "compost",
"microscope" or "nematode" lands on the right thing, plus the full colour token
set extracted before `css/site.css` was deleted.

The part worth doing next is not more description, it is **the licence column**.
Seven photographs sit in `assets/photo/openly-licensed/` with an empty credits
register, and two more have stock-library filenames and no recorded licence. The
meeting record says images were pulled from Canva and catalogued into a Drive
folder. Until every file can answer "who took this and under what licence", the
inventory is a picture list rather than an asset library, and a nonprofit under
Google Ad Grant scrutiny cannot afford that gap.

One afternoon of recording licences beats any amount of further tooling.

## Build: the carousel command. This is the one with real leverage.

`/graduate` takes Carla's announcement and the field trial report and returns the
seven slide texts, the caption, the LinkedIn adaptation and the asset paths, with
the six swappable fields filled in.

It earns its place because the work it removes is real and repeats every other
Thursday: reading a long report for six specific fields, writing the same seven
slides in the same order, and adapting to LinkedIn. That is the ninety minutes
`sop/field-notes-series.md` currently describes as manual.

Three things it has to enforce, or it is worse than doing it by hand:

- **No internal acronyms in public copy.** Foundation Courses, not FC. Advanced
  Programs, not AP, which an American reader reads as Advanced Placement.
- **No number without its source line, and no percentage without its control.**
- **No consent, no draft.** It should refuse to produce a portrait direction
  until consent is recorded, and say so.

What it must not do: invent a number, smooth a disappointing result, or write a
quote the graduate did not say.

## Build, smaller than you think: the status script

`scripts/status.js`, counting drafts, approved and posted, and days of scheduled
content ahead of today.

Staying a month ahead is the thing worth protecting, so the number goes on line
one. But the truth is Later already knows the schedule and this script will only
ever know what is in the folders. Build it as a count of the folders, twenty
lines, no date parsing beyond the filename, and accept that it measures the
drafting pipeline rather than the posting calendar. Do not build a Later
integration to close that gap.

## Cut: `/post`, `/week` and `/asset`

Three commands I would not build yet.

**`/asset`** searches `INVENTORY.md` for a matching picture. A person reading a
2,000 word file with Ctrl-F does this in ten seconds, and does it better, because
choosing a photograph is a judgement about whether the picture supports the
claim. That judgement is the entire point of the licence and stand-in flags. Cut
it.

**`/week`** generates a week of drafts and checks that two promotional pillars do
not stack. Stephanie owns promotional content and Linnea owns community and
storytelling, so the stacking check is a conversation between two people, not a
script. Generating a week of drafts also inverts the workflow: the constraint is
not draft volume, it is Stephanie's approval queue. Cut it.

**`/post`** is a general purpose post generator. It would produce plausible soil
science content, which is exactly the thing the account has enough of. The
Foundation's advantage is the field trials, and a general generator dilutes the
one thing that is actually scarce. Build `/graduate` well instead.

## The thing not on your list, which I would build first

**A scholarship recipient command, built the same way as `/graduate`.**

The division of labour gives Linnea community and storytelling content "starting
with graduate announcements and scholarship recipients". Scholarship recipients
are the other half of the beat and have the same shape: a named person, a named
place, a consent requirement, a story that is not a promotion. Every rule in
`sop/field-notes-series.md` transfers, and the second series is where the format
proves it was a format rather than one good post.

## Order

1. Record the licences. One afternoon, no code.
2. `/graduate`, with the three refusals built in.
3. `scripts/status.js`, twenty lines.
4. The scholarship series, reusing `/graduate`'s structure.

Nothing above publishes anything. The output stays text and asset paths that a
person pastes into Canva and Later, and the approval step stays a human reading
it.
