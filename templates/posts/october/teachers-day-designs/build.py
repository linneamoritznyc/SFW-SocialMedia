"""World Teachers' Day: ten new designs for one two-person slide (Loida Vasquez and Casey Williams), drawn from scratch
in HTML and CSS and rendered to 1080 x 1350 PNG with Playwright (6 Oct 2026). Brand fonts (Montserrat, Source Sans 3),
brand colours, the new logo with flowers. Both people always get the same space. Words exactly as approved.

python3 templates/posts/october/teachers-day-designs/build.py   -> renders/october/teachers-day-designs/design-01..10.png
"""
import os, subprocess, json
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "renders", "october", "teachers-day-designs"); os.makedirs(OUT, exist_ok=True)
A = lambda p: "file://" + os.path.join(ROOT, p)

LOIDA = dict(name="Loida Vasquez", first="Loida", last="Vasquez", title="Advanced Programs Lead &amp; Mentor",
             photo=A("renders/.tmp/zoom-loida-teaching-3.jpg"), pos="50% 30%")
CASEY = dict(name="Casey Williams", first="Casey", last="Williams", title="Mentor &amp; Consultant",
             photo=A("assets/mentors-teachers-day/casey-williams.jpg"), pos="50% 30%")
P = [LOIDA, CASEY]
LOGO, LOGO_W = A("assets/logo/foundation-logo-color.png"), A("assets/logo/foundation-logo-white.png")
SCRATCH, SOIL = A("assets/texture/scratched-paper.png"), A("assets/collage/cutouts/soil-flatlay-border.png")
COMPOST = A("assets/photo/hand-of-compost.jpg")
FERN, SPRIG, YELLOW, FOUR = (A(f"assets/unsplash-flowers/{n}-cut.png") for n in ("pressed-red-fern", "pressed-sprig", "pressed-yellow", "pressed-four"))
LINE = lambda n: A(f"assets/collage/white-line/white-{n}-1.png")

BASE = f"""
@font-face {{ font-family: Montserrat; src: url({A('assets/font/montserrat-latin-variable.woff2')}); font-weight: 100 900; }}
@font-face {{ font-family: 'Source Sans 3'; src: url({A('assets/font/source-sans-3-latin-400-normal.woff2')}); font-weight: 400; }}
@font-face {{ font-family: 'Source Sans 3'; src: url({A('assets/font/source-sans-3-latin-600-normal.woff2')}); font-weight: 600; }}
:root {{ --green:#31662F; --leaf:#6AA46F; --gold:#D39C48; --brown:#4C3634; --tan:#C09D7F; --sage:#B1BCB1;
        --cream:#F3F1EA; --ink:#333130; --purple:#654D76; --blue:#4B7FB4; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1350px; overflow:hidden; }}
body {{ position:relative; background:var(--cream); font-family:'Source Sans 3', sans-serif; color:var(--ink); }}
.abs {{ position:absolute; }}
.name {{ font-family:Montserrat; font-weight:700; color:var(--green); line-height:1.02; }}
.title {{ font-family:'Source Sans 3'; font-weight:400; color:var(--ink); }}
.eyebrow {{ font-family:Montserrat; font-weight:700; letter-spacing:.18em; text-transform:uppercase; }}
.photo {{ background-size:cover; }}
"""

def page(css, body): return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{body}</body></html>"
def bg(p): return f"background-image:url({p['photo']}); background-position:{p['pos']};"

D = {}

# 1  Split frame: each person gets a full-bleed half; names on cream torn-paper labels across the seam.
D[1] = page("""
.half { left:0; width:1080px; height:675px; background-size:cover; }
.half::after { content:''; position:absolute; inset:0; background:linear-gradient(180deg, rgba(49,102,47,0) 55%, rgba(49,102,47,.55)); }
.label { background:var(--cream); padding:26px 36px 24px; clip-path:polygon(0 6%, 3% 0, 30% 4%, 55% 0, 80% 5%, 100% 1%, 98% 50%, 100% 96%, 70% 100%, 40% 95%, 12% 100%, 0 94%, 2% 50%);
  box-shadow:0 10px 30px rgba(0,0,0,.25); }
.label .name { font-size:50px; } .label .title { font-size:27px; margin-top:6px; }
""", f"""
<div class='abs half' style='top:0; {bg(LOIDA)}'></div>
<div class='abs half' style='top:675px; {bg(CASEY)}'></div>
<div class='abs label' style='left:56px; top:500px; transform:rotate(-1.5deg)'><div class='name'>{LOIDA['name']}</div><div class='title'>{LOIDA['title']}</div></div>
<div class='abs label' style='right:56px; top:1170px; transform:rotate(1.2deg)'><div class='name'>{CASEY['name']}</div><div class='title'>{CASEY['title']}</div></div>
<img class='abs' src='{LOGO_W}' style='right:40px; top:36px; width:150px'>
""")

# 2  Soil-dark: brown ground with grain, round portraits ringed in gold, cream type, white line-art plants.
D[2] = page(f"""
body {{ background:radial-gradient(120% 80% at 50% 10%, #6b4d45, var(--brown) 60%, #2f2120); }}
.grain {{ inset:0; background:url({SCRATCH}); background-size:cover; opacity:.35; mix-blend-mode:screen; }}
.circle {{ width:400px; height:400px; border-radius:50%; background-size:cover; box-shadow:0 0 0 10px var(--gold), 0 0 0 22px rgba(211,156,72,.25); }}
.n {{ color:var(--cream); }} .t {{ color:#E9DCC9; }}
""", f"""
<div class='abs grain'></div>
<img class='abs' src='{LINE("tithonia")}' style='left:-90px; bottom:-40px; width:440px; opacity:.55'>
<img class='abs' src='{LINE("mushroom-cluster")}' style='right:-60px; top:-20px; width:360px; opacity:.45'>
<div class='abs eyebrow' style='left:0; right:0; top:70px; text-align:center; color:var(--gold); font-size:24px'>World Teachers' Day</div>
<div class='abs circle' style='left:100px; top:170px; {bg(LOIDA)}'></div>
<div class='abs' style='left:560px; top:270px; width:440px'><div class='name n' style='font-size:52px'>{LOIDA['name']}</div><div class='title t' style='font-size:28px; margin-top:12px'>{LOIDA['title']}</div></div>
<div class='abs circle' style='right:100px; top:690px; {bg(CASEY)}'></div>
<div class='abs' style='left:90px; top:800px; width:420px; text-align:right'><div class='name n' style='font-size:52px'>{CASEY['name']}</div><div class='title t' style='font-size:28px; margin-top:12px'>{CASEY['title']}</div></div>
<img class='abs' src='{LOGO_W}' style='left:470px; bottom:50px; width:140px'>
""")

# 3  Two tall portrait columns, full bleed, fading into green at the bottom where the names sit.
D[3] = page("""
.col { top:0; width:540px; height:1350px; background-size:cover; }
.col::after { content:''; position:absolute; inset:0; background:linear-gradient(180deg, rgba(49,102,47,0) 45%, rgba(49,102,47,.92) 82%); }
.cap { bottom:110px; width:540px; padding:0 40px; }
.cap .name { color:var(--cream); font-size:50px; } .cap .title { color:#E6EFE1; font-size:26px; margin-top:10px; }
""", f"""
<div class='abs col' style='left:0; {bg(LOIDA)}'></div>
<div class='abs col' style='left:540px; {bg(CASEY)}'></div>
<div class='abs' style='left:538px; top:0; width:4px; height:1350px; background:var(--cream)'></div>
<div class='abs cap' style='left:0'><div class='name'>Loida<br>Vasquez</div><div class='title'>{LOIDA['title']}</div></div>
<div class='abs cap' style='left:540px'><div class='name'>Casey<br>Williams</div><div class='title'>{CASEY['title']}</div></div>
<div class='abs' style='left:0; right:0; top:0; height:150px; background:linear-gradient(180deg, rgba(243,241,234,.95), rgba(243,241,234,0))'></div>
<img class='abs' src='{LOGO}' style='left:465px; top:22px; width:150px; background:rgba(243,241,234,.9); border-radius:50%; padding:8px'>
""")

# 4  Kraft-paper scrapbook: two prints, masking tape, label-maker style name strips, pressed flowers.
D[4] = page(f"""
body {{ background:#C9AE8E; }}
.kraft {{ inset:0; background:url({SCRATCH}); background-size:cover; opacity:.6; mix-blend-mode:multiply; }}
.print {{ background:#FCFBF7; padding:18px 18px 90px; box-shadow:0 14px 30px rgba(60,40,30,.35); }}
.print .ph {{ width:430px; height:430px; background-size:cover; }}
.tape {{ width:160px; height:46px; background:rgba(230,236,214,.8); }}
.strip {{ background:var(--brown); color:var(--cream); font-family:Montserrat; font-weight:700; padding:10px 18px; display:inline-block; }}
.strip2 {{ background:var(--cream); color:var(--ink); padding:8px 16px; display:inline-block; font-size:24px; margin-top:8px; }}
""", f"""
<div class='abs kraft'></div>
<img class='abs' src='{FERN}' style='right:40px; top:40px; width:220px; transform:rotate(18deg)'>
<img class='abs' src='{YELLOW}' style='right:30px; bottom:20px; width:240px; transform:rotate(-12deg)'>
<div class='abs print' style='left:70px; top:120px; transform:rotate(-3deg)'><div class='ph' style='{bg(LOIDA)}'></div></div>
<div class='abs tape' style='left:220px; top:100px; transform:rotate(-8deg)'></div>
<div class='abs' style='left:560px; top:330px'><div class='strip' style='font-size:40px'>{LOIDA['name']}</div><br><div class='strip2'>{LOIDA['title']}</div></div>
<div class='abs print' style='right:70px; top:700px; transform:rotate(2.5deg)'><div class='ph' style='{bg(CASEY)}'></div></div>
<div class='abs tape' style='right:220px; top:680px; transform:rotate(6deg)'></div>
<div class='abs' style='left:90px; top:900px'><div class='strip' style='font-size:40px'>{CASEY['name']}</div><br><div class='strip2'>{CASEY['title']}</div></div>
<img class='abs' src='{LOGO}' style='left:90px; top:1150px; width:140px'>
""")

# 5  Editorial: big offset photos, names set sideways along the photo edge, thin rules, lots of air.
D[5] = page("""
.ph { width:560px; height:560px; background-size:cover; }
.side { transform-origin:left top; transform:rotate(-90deg); white-space:nowrap; }
.rule { height:2px; background:var(--green); }
""", f"""
<div class='abs eyebrow' style='left:80px; top:70px; font-size:22px; color:var(--brown)'>World Teachers' Day · October 5</div>
<div class='abs rule' style='left:80px; top:115px; width:920px'></div>
<div class='abs ph' style='left:80px; top:160px; {bg(LOIDA)}'></div>
<div class='abs side' style='left:672px; top:715px'><span class='name' style='font-size:58px'>{LOIDA['name']}</span></div>
<div class='abs title' style='left:740px; top:620px; width:300px; font-size:27px'>{LOIDA['title']}</div>
<div class='abs ph' style='left:440px; top:735px; {bg(CASEY)}'></div>
<div class='abs side' style='left:350px; top:1290px'><span class='name' style='font-size:58px'>{CASEY['name']}</span></div>
<div class='abs title' style='left:80px; top:760px; width:300px; font-size:27px'>{CASEY['title']}</div>
<img class='abs' src='{LOGO}' style='left:80px; top:1140px; width:150px'>
""")

# 6  Arch windows on sage with a soil band: two arches side by side, names underneath.
D[6] = page(f"""
body {{ background:linear-gradient(180deg, #DCE3DA, var(--sage)); }}
.arch {{ width:440px; height:620px; border-radius:220px 220px 0 0; background-size:cover; border:10px solid var(--cream); }}
.cap {{ width:440px; text-align:center; }}
""", f"""
<div class='abs eyebrow' style='left:0; right:0; top:80px; text-align:center; font-size:24px; color:var(--green)'>World Teachers' Day</div>
<div class='abs arch' style='left:70px; top:150px; {bg(LOIDA)}'></div>
<div class='abs arch' style='right:70px; top:150px; {bg(CASEY)}'></div>
<div class='abs cap' style='left:70px; top:810px'><div class='name' style='font-size:46px'>Loida<br>Vasquez</div><div class='title' style='font-size:26px; margin-top:12px'>{LOIDA['title']}</div></div>
<div class='abs cap' style='right:70px; top:810px'><div class='name' style='font-size:46px'>Casey<br>Williams</div><div class='title' style='font-size:26px; margin-top:12px'>{CASEY['title']}</div></div>
<img class='abs' src='{SOIL}' style='left:0; bottom:-150px; width:1080px'>
<img class='abs' src='{LOGO}' style='left:470px; top:1035px; width:140px'>
""")

# 7  Blurry brand gradient with frosted-glass cards.
D[7] = page("""
body { background:#E9E4D8; }
.blob { border-radius:50%; filter:blur(90px); opacity:.85; }
.glass { width:940px; height:520px; background:rgba(255,255,255,.42); border:1.5px solid rgba(255,255,255,.75); border-radius:36px;
  backdrop-filter:blur(18px); box-shadow:0 20px 50px rgba(76,54,52,.18); }
.ph { width:440px; height:440px; border-radius:24px; background-size:cover; }
""", f"""
<div class='abs blob' style='left:-120px; top:80px; width:620px; height:620px; background:var(--leaf)'></div>
<div class='abs blob' style='right:-160px; top:360px; width:640px; height:640px; background:var(--gold)'></div>
<div class='abs blob' style='left:120px; bottom:-200px; width:700px; height:600px; background:var(--purple); opacity:.55'></div>
<div class='abs glass' style='left:70px; top:110px'></div>
<div class='abs ph' style='left:110px; top:150px; {bg(LOIDA)}'></div>
<div class='abs' style='left:590px; top:300px; width:390px'><div class='name' style='font-size:48px'>{LOIDA['name']}</div><div class='title' style='font-size:27px; margin-top:12px'>{LOIDA['title']}</div></div>
<div class='abs glass' style='left:70px; top:680px'></div>
<div class='abs ph' style='left:110px; top:720px; {bg(CASEY)}'></div>
<div class='abs' style='left:590px; top:870px; width:390px'><div class='name' style='font-size:48px'>{CASEY['name']}</div><div class='title' style='font-size:27px; margin-top:12px'>{CASEY['title']}</div></div>
<img class='abs' src='{LOGO}' style='left:470px; top:24px; width:120px'>
""")

# 8  Green duotone photos with halftone dots and bold type.
D[8] = page("""
.duo { width:500px; height:560px; background-size:cover; filter:grayscale(1) contrast(1.1); }
.tint { width:500px; height:560px; background:var(--green); mix-blend-mode:screen; }
.tint2 { width:500px; height:560px; background:var(--cream); mix-blend-mode:multiply; }
.dots { width:500px; height:560px; background-image:radial-gradient(var(--green) 28%, transparent 30%); background-size:16px 16px;
  -webkit-mask-image:linear-gradient(0deg, #000, transparent 60%); }
""", f"""
<div class='abs duo' style='left:60px; top:80px; {bg(LOIDA)}'></div><div class='abs tint' style='left:60px; top:80px'></div><div class='abs dots' style='left:60px; top:80px'></div>
<div class='abs duo' style='left:520px; top:710px; {bg(CASEY)}'></div><div class='abs tint' style='left:520px; top:710px'></div><div class='abs dots' style='left:520px; top:710px'></div>
<div class='abs' style='left:600px; top:250px; width:420px'><div class='name' style='font-size:60px'>Loida<br>Vasquez</div><div class='title' style='font-size:28px; margin-top:14px'>{LOIDA['title']}</div></div>
<div class='abs' style='left:60px; top:880px; width:420px'><div class='name' style='font-size:60px'>Casey<br>Williams</div><div class='title' style='font-size:28px; margin-top:14px'>{CASEY['title']}</div></div>
<div class='abs' style='left:60px; top:660px; width:420px; height:14px; background:var(--gold)'></div>
<img class='abs' src='{LOGO}' style='left:60px; top:1160px; width:130px'>
""")

# 9  Field-guide specimen sheets: two herbarium cards with pressed flowers, label boxes and fine rules.
D[9] = page(f"""
body {{ background:#E8E1D2; }}
.sheet {{ width:470px; height:1130px; background:#FBF9F3; box-shadow:0 10px 26px rgba(76,54,52,.18); }}
.ph {{ width:410px; height:410px; background-size:cover; }}
.labelbox {{ border:2px solid var(--brown); padding:18px 20px; }}
.small {{ font-family:Montserrat; font-weight:700; font-size:15px; letter-spacing:.16em; color:var(--brown); text-transform:uppercase; }}
""", f"""
<div class='abs sheet' style='left:50px; top:110px'></div><div class='abs sheet' style='right:50px; top:110px'></div>
<div class='abs ph' style='left:80px; top:140px; {bg(LOIDA)}'></div><div class='abs ph' style='right:80px; top:140px; {bg(CASEY)}'></div>
<img class='abs' src='{SPRIG}' style='left:110px; top:590px; width:230px; transform:rotate(-8deg)'>
<img class='abs' src='{FOUR}' style='right:90px; top:600px; width:300px; transform:rotate(5deg)'>
<div class='abs labelbox' style='left:80px; top:900px; width:410px'><div class='name' style='font-size:40px; margin-top:8px'>{LOIDA['name']}</div><div class='title' style='font-size:24px; margin-top:6px'>{LOIDA['title']}</div></div>
<div class='abs labelbox' style='right:80px; top:900px; width:410px'><div class='name' style='font-size:40px; margin-top:8px'>{CASEY['name']}</div><div class='title' style='font-size:24px; margin-top:6px'>{CASEY['title']}</div></div>
<div class='abs eyebrow' style='left:50px; top:52px; font-size:22px; color:var(--brown)'>World Teachers' Day · October 5</div>
<img class='abs' src='{LOGO}' style='right:50px; top:20px; width:90px'>
""")

# 10 Grown from the soil: full-bleed compost, two cream cards on top, warm light from above.
D[10] = page(f"""
body {{ background:url({COMPOST}) 0% 0% / 2400px auto; }}
.shade {{ inset:0; background:linear-gradient(180deg, rgba(243,200,140,.35), rgba(30,20,15,.15) 40%, rgba(30,20,15,.45)); }}
.card {{ width:920px; height:500px; background:var(--cream); border-radius:6px; box-shadow:0 18px 40px rgba(0,0,0,.4); }}
.ph {{ width:420px; height:420px; background-size:cover; }}
""", f"""
<div class='abs shade'></div>
<div class='abs card' style='left:80px; top:120px'></div>
<div class='abs ph' style='left:120px; top:160px; {bg(LOIDA)}'></div>
<div class='abs' style='left:580px; top:300px; width:390px'><div class='name' style='font-size:48px'>{LOIDA['name']}</div><div class='title' style='font-size:27px; margin-top:12px'>{LOIDA['title']}</div></div>
<div class='abs card' style='left:80px; top:680px'></div>
<div class='abs ph' style='left:120px; top:720px; {bg(CASEY)}'></div>
<div class='abs' style='left:580px; top:860px; width:390px'><div class='name' style='font-size:48px'>{CASEY['name']}</div><div class='title' style='font-size:27px; margin-top:12px'>{CASEY['title']}</div></div>
<img class='abs' src='{SPRIG}' style='right:30px; top:610px; width:220px; transform:rotate(12deg)'>
<img class='abs' src='{LOGO_W}' style='left:470px; top:1210px; width:140px'>
""")

files = []
for k, html in D.items():
    p = os.path.join(OUT, f"design-{k:02d}.html"); open(p, "w").write(html); files.append(p)
js = os.path.join(OUT, "render.js")
open(js, "w").write("""
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of %s) { await p.goto('file://' + f); await p.waitForTimeout(400); await p.screenshot({ path: f.replace('.html', '.png') }); }
  await b.close();
})();""" % json.dumps(files))
subprocess.run(["node", js], check=True)
# contact sheet
from PIL import Image
ims = [Image.open(f.replace(".html", ".png")) for f in files]
sheet = Image.new("RGB", (5 * 432 + 6 * 12, 2 * 540 + 3 * 12), (60, 60, 60))
for i, im in enumerate(ims):
    t = im.convert("RGB").resize((432, 540)); sheet.paste(t, (12 + (i % 5) * 444, 12 + (i // 5) * 552))
sheet.save(os.path.join(OUT, "contact.png")); print("ok", len(ims))
