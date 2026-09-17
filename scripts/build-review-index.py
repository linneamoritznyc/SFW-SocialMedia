import os, re, struct, html, json

ROOT = "/home/user/SFW-SocialMedia"
PNG  = os.path.join(ROOT, "review/png")

def dims(p):
    d = open(p,'rb').read(33)
    return struct.unpack('>II', d[16:24])

SETS = [
  ("Field Notes: Sandra Niggemeyer",
   "variants_", "Twenty-seven directions for the same graduate story. Pick the ones worth keeping.",
   lambda n: n.startswith("variants_") and n.count("_")==1),
  ("UMass Amherst community post",
   "variants_umass_", "Carousel (4:5), three story frames (9:16), two square alternates.", None),
  ("Scholarship announcement",
   "variants_scholarships_", "Seven slides. Every unknown is a dashed placeholder. Consent email is in captions.md.", None),
  ("India tour",
   "variants_india_", "Post 1 invitation, post 2 rice-wheat science, post 3 story and attendees.", None),
  ("Reusable templates",
   "templates_", "Swap the marked fields. Rules are written into the HTML comments.", None),
  ("Motion frames (still)",
   "motion_", "These are animated HTML. The PNG is one frame. Screen-record the HTML at 1080x1920.", None),
]

files = sorted(os.listdir(PNG))
used = set()
groups = []
for title, prefix, note, test in SETS:
    if test:
        m = [f for f in files if test(f[:-4]) and f not in used]
    else:
        m = [f for f in files if f.startswith(prefix) and f not in used]
    used.update(m)
    if m: groups.append((title, note, m))

def label(n):
    n = n[:-4]
    for p in ("variants_umass_","variants_scholarships_","variants_india_","variants_","templates_","motion_"):
        if n.startswith(p): n = n[len(p):]; break
    return n.replace("-", " ")

cards = []
total = 0
for title, note, m in groups:
    items = []
    for f in m:
        w,h = dims(os.path.join(PNG,f))
        ratio = {(1080,1080):"1:1", (1080,1350):"4:5", (1080,1920):"9:16"}.get((w,h), f"{w}x{h}")
        items.append(f'''<figure class="card">
      <a href="png/{f}" download><img src="png/{f}" alt="{html.escape(label(f))}" loading="lazy"></a>
      <figcaption><span class="nm">{html.escape(label(f))}</span><span class="rt">{ratio}</span></figcaption>
    </figure>''')
        total += 1
    cards.append(f'''<section>
    <h2>{html.escape(title)} <span class="ct">{len(m)}</span></h2>
    <p class="note">{html.escape(note)}</p>
    <div class="grid">
    {"".join(items)}
    </div>
  </section>''')

page = f'''<!doctype html>
<meta charset="utf-8">
<title>Soil Food Web Foundation — social assets for review</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
:root{{--green:#156826;--moss:#22371F;--panel:#F4F1EA;--ink:#333130;--soil:#4F3433;--sage:#A7B097;--line:#DED8CC}}
*{{box-sizing:border-box}}
body{{margin:0;background:#fff;color:var(--ink);
  font:16px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}}
header{{background:var(--panel);border-bottom:1px solid var(--line);padding:40px 32px 32px}}
header h1{{margin:0 0 8px;font-size:30px;line-height:1.15;color:var(--moss);font-weight:700;letter-spacing:-.01em}}
header p{{margin:0 0 4px;max-width:62ch;color:var(--soil)}}
header .meta{{margin-top:18px;font-size:14px;color:#6b6560}}
main{{padding:0 32px 80px}}
section{{padding:44px 0 8px;border-bottom:1px solid var(--line)}}
section:last-child{{border-bottom:0}}
h2{{margin:0 0 4px;font-size:21px;color:var(--green);font-weight:700}}
.ct{{font-size:13px;color:#8a837c;font-weight:400;margin-left:6px}}
.note{{margin:0 0 22px;font-size:14px;color:#6b6560;max-width:70ch}}
.grid{{display:grid;gap:22px;grid-template-columns:repeat(auto-fill,minmax(230px,1fr))}}
.card{{margin:0}}
.card a{{display:block;border:1px solid var(--line);background:var(--panel);overflow:hidden}}
.card a:hover{{border-color:var(--green)}}
.card img{{display:block;width:100%;height:auto}}
figcaption{{display:flex;justify-content:space-between;gap:8px;padding-top:7px;font-size:13px}}
.nm{{color:var(--ink)}} .rt{{color:#8a837c;font-variant-numeric:tabular-nums}}
footer{{padding:32px;background:var(--panel);border-top:1px solid var(--line);font-size:14px;color:#6b6560}}
footer b{{color:var(--soil)}}
@media(max-width:640px){{header,main{{padding-left:18px;padding-right:18px}}}}
</style>
<header>
  <h1>Social assets for review</h1>
  <p>Every visual piece built so far, rendered at full export size. Click any image to download the PNG.
     Captions, hashtags and the evidence rung for each piece live in the <code>captions.md</code> file
     inside that set's folder.</p>
  <p class="meta">{total} images &middot; 1080px wide &middot; safe-zone guides removed &middot; generated 17 September 2026</p>
</header>
<main>
{"".join(cards)}
</main>
<footer>
  <p><b>Before anything is scheduled:</b> every dashed box is a placeholder for something we do not yet hold,
     and every name on a graphic needs written consent. Nothing here is approved copy.</p>
</footer>
'''
open(os.path.join(ROOT,"review/index.html"),"w").write(page)
print("wrote review/index.html with", total, "images in", len(groups), "sets")
