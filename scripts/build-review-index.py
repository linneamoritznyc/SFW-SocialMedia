"""Builds review/index.html plus one index per set folder."""
import os, struct, html

ROOT = "/home/user/SFW-SocialMedia"
REV  = os.path.join(ROOT, "review")

SETS = [
 ("1-graduate-celebration", "Graduate celebration: Sandra Niggemeyer",
  "Her field trial in Van, Texas. Twenty years fallow, three plots, one season. "
  "Start-here holds the six worth posting; more-options holds the other twenty-one "
  "if you want a different angle.", "captions-field-notes.md",
  ["start-here", "more-options"]),
 ("2-umass-amherst", "UMass Amherst community post",
  "Five carousel slides at 4:5, three story frames at 9:16, two square alternates. "
  "No partnership with UMass is claimed anywhere.", "captions-umass.md", None),
 ("3-scholarships", "Scholarship announcement",
  "Seven slides at 4:5. Every dashed box is a name, number or face we do not have yet. "
  "The consent email to send each recipient is at the bottom of the captions file.",
  "captions-scholarships.md", None),
 ("4-india-tour", "India tour",
  "Three posts: the invitation carousel, the rice-wheat science carousel, and a story "
  "frame with an attendees card. Dates still disagree across our own materials.",
  "captions-india.md", None),
 ("5-templates", "Reusable templates",
  "Myth, checklist and microbe layouts. Swap the marked fields and the layout holds. "
  "Not posts, tooling.", None, None),
 ("7-quote-cards", "Quote cards",
  "Lines from the phrase bank, set as cards. These are finished posts, not drafts.",
  None, None),
 ("6-motion-stills", "Motion pieces (still frames)",
  "One frame each from four animated HTML pages at 9:16. These are not finished posts. "
  "The animation lives in motion/ in the repo and has to be screen-recorded.", None, None),
]

RATIO = {(1080,1080):"1:1", (1080,1350):"4:5", (1080,1920):"9:16"}

def dims(p):
    return struct.unpack('>II', open(p,'rb').read(33)[16:24])

def label(f):
    return f[:-4].replace("-", " ")

CSS = """
:root{--green:#156826;--moss:#22371F;--panel:#F4F1EA;--ink:#333130;--soil:#4F3433;--line:#DED8CC}
*{box-sizing:border-box}
body{margin:0;background:#fff;color:var(--ink);
 font:16px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
header{background:var(--panel);border-bottom:1px solid var(--line);padding:38px 32px 30px}
h1{margin:0 0 10px;font-size:29px;line-height:1.15;color:var(--moss);letter-spacing:-.01em}
header p{margin:0;max-width:64ch;color:var(--soil)}
.meta{margin-top:16px;font-size:14px;color:#6b6560}
a.back{display:inline-block;margin-bottom:14px;font-size:14px;color:var(--green)}
main{padding:0 32px 72px}
section{padding:38px 0 6px;border-bottom:1px solid var(--line)}
section:last-child{border-bottom:0}
h2{margin:0 0 5px;font-size:20px;color:var(--green)}
.ct{font-size:13px;color:#8a837c;font-weight:400;margin-left:6px}
.note{margin:0 0 20px;font-size:14px;color:#6b6560;max-width:72ch}
.grid{display:grid;gap:22px;grid-template-columns:repeat(auto-fill,minmax(225px,1fr))}
figure{margin:0}
figure a{display:block;border:1px solid var(--line);background:var(--panel)}
figure a:hover{border-color:var(--green)}
img{display:block;width:100%;height:auto}
figcaption{display:flex;justify-content:space-between;gap:8px;padding-top:7px;font-size:13px}
.rt{color:#8a837c;font-variant-numeric:tabular-nums}
.setlist{display:grid;gap:18px;grid-template-columns:repeat(auto-fill,minmax(310px,1fr));padding:34px 0 0}
.set{border:1px solid var(--line);padding:20px 22px 22px;text-decoration:none;color:inherit;display:block}
.set:hover{border-color:var(--green);background:var(--panel)}
.set h3{margin:0 0 6px;font-size:18px;color:var(--green)}
.set p{margin:0;font-size:14px;color:#6b6560}
.set .n{display:block;margin-top:12px;font-size:13px;color:#8a837c}
footer{padding:30px 32px;background:var(--panel);border-top:1px solid var(--line);
 font-size:14px;color:#6b6560}
footer b{color:var(--soil)}
@media(max-width:640px){header,main,footer{padding-left:18px;padding-right:18px}}
"""

FOOT = ("<footer><p><b>Before anything is scheduled:</b> every dashed box is a "
        "placeholder for an asset or a fact we do not hold yet, every name or face "
        "on a graphic needs written consent first, and none of the copy is approved."
        "</p></footer>")

def figures(folder, files):
    out = []
    for f in files:
        w, h = dims(os.path.join(folder, f))
        r = RATIO.get((w, h), f"{w}x{h}")
        out.append(f'<figure><a href="{f}" download><img src="{f}" loading="lazy" '
                   f'alt="{html.escape(label(f))}"></a><figcaption>'
                   f'<span>{html.escape(label(f))}</span><span class="rt">{r}</span>'
                   f'</figcaption></figure>')
    return "".join(out)

total = 0
tiles = []
for slug, title, note, cap, subs in SETS:
    d = os.path.join(REV, slug)
    if not os.path.isdir(d):
        continue
    blocks, count = [], 0
    if subs:
        for sub in subs:
            sd = os.path.join(d, sub)
            if not os.path.isdir(sd):
                continue
            fs = sorted(x for x in os.listdir(sd) if x.endswith(".png"))
            count += len(fs)
            heading = ("Start here" if sub == "start-here" else "More options")
            sub_note = ("The six worth putting in front of people."
                        if sub == "start-here"
                        else "Same story, other angles. Only if none of the six land.")
            blocks.append(f'<section><h2>{heading}<span class="ct">{len(fs)}</span></h2>'
                          f'<p class="note">{sub_note}</p><div class="grid">'
                          + "".join(
                              f'<figure><a href="{sub}/{f}" download>'
                              f'<img src="{sub}/{f}" loading="lazy" alt="{html.escape(label(f))}">'
                              f'</a><figcaption><span>{html.escape(label(f))}</span>'
                              f'<span class="rt">{RATIO.get(dims(os.path.join(sd,f)), "")}</span>'
                              f'</figcaption></figure>' for f in fs)
                          + '</div></section>')
    else:
        fs = sorted(x for x in os.listdir(d) if x.endswith(".png"))
        count = len(fs)
        blocks.append(f'<section><div class="grid">{figures(d, fs)}</div></section>')
    total += count
    caplink = (f'<p class="meta">Captions, hashtags and sources: '
               f'<a href="../{cap}">{cap}</a></p>' if cap else "")
    open(os.path.join(d, "index.html"), "w").write(
        f'<!doctype html><meta charset="utf-8"><title>{html.escape(title)}</title>'
        f'<meta name="viewport" content="width=device-width,initial-scale=1">'
        f'<style>{CSS}</style><header><a class="back" href="../index.html">'
        f'&larr; all sets</a><h1>{html.escape(title)}</h1><p>{html.escape(note)}</p>'
        f'{caplink}<p class="meta">{count} images &middot; click any to download</p>'
        f'</header><main>{"".join(blocks)}</main>{FOOT}')
    tiles.append(f'<a class="set" href="{slug}/index.html"><h3>{html.escape(title)}</h3>'
                 f'<p>{html.escape(note.split(".")[0])}.</p>'
                 f'<span class="n">{count} images</span></a>')

open(os.path.join(REV, "index.html"), "w").write(
    '<!doctype html><meta charset="utf-8">'
    '<title>Soil Food Web Foundation — social assets for review</title>'
    '<meta name="viewport" content="width=device-width,initial-scale=1">'
    f'<style>{CSS}</style><header><h1>Social assets for review</h1>'
    '<p>Six sets of draft social posts, rendered at full export size. Open a set, '
    'then click any image to download the PNG. Captions, hashtags and the source '
    'behind every number are in the captions file linked inside each set.</p>'
    f'<p class="meta">{total} images &middot; all 1080px wide &middot; '
    'generated 17 September 2026</p></header>'
    f'<main><div class="setlist">{"".join(tiles)}</div></main>{FOOT}')

print(f"{total} images across {len(tiles)} sets")
