"""World Teachers' Day: ten designs for the Loida and Casey slide where the photos, text and logo stay exactly where
Stephanie put them (two 515 px squares on the left, name and title on the right, logo bottom right). Only the
surroundings change: background, top decoration, textures, light, colour (Linnea, 6 Oct 2026).

python3 templates/posts/october/teachers-day-designs-2/build.py -> renders/october/teachers-day-designs-2/design-01..10.png
"""
import os, subprocess, json, random, math
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(ROOT, "renders", "october", "teachers-day-designs-2"); os.makedirs(OUT, exist_ok=True)
A = lambda p: "file://" + os.path.join(ROOT, p)
LOIDA = A("renders/.tmp/zoom-loida-teaching-3.jpg"); CASEY = A("assets/mentors-teachers-day/casey-williams.jpg")
LOGO = A("assets/logo/foundation-logo-color.png")
SCRATCH, SOIL, COMPOST = A("assets/texture/scratched-paper.png"), A("assets/collage/cutouts/soil-flatlay-border.png"), A("assets/photo/hand-of-compost.jpg")
PRESSED = [A(f"assets/unsplash-flowers/{n}-cut.png") for n in ("pressed-red-fern", "pressed-sprig", "pressed-yellow", "pressed-four")]

BASE = f"""
@font-face {{ font-family: Montserrat; src: url({A('assets/font/montserrat-latin-variable.woff2')}); font-weight: 100 900; }}
@font-face {{ font-family: 'Source Sans 3'; src: url({A('assets/font/source-sans-3-latin-400-normal.woff2')}); font-weight: 400; }}
:root {{ --green:#31662F; --leaf:#6AA46F; --gold:#D39C48; --brown:#4C3634; --tan:#C09D7F; --sage:#B1BCB1;
        --cream:#F3F1EA; --ink:#333130; --purple:#654D76; --blue:#4B7FB4; }}
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:1080px; height:1350px; overflow:hidden; }}
body {{ position:relative; background:var(--cream); }}
.abs {{ position:absolute; }}
/* the fixed layer: identical on every design */
.ph {{ position:absolute; left:62px; width:515px; height:515px; background-size:cover; background-position:50% 30%; z-index:5; }}
.who {{ position:absolute; left:618px; width:420px; z-index:5; }}
.who .n {{ font-family:Montserrat; font-weight:700; font-size:52px; line-height:1.04; color:var(--green); }}
.who .t {{ font-family:'Source Sans 3'; font-size:31px; line-height:1.45; color:var(--ink); margin-top:14px; }}
.logo {{ position:absolute; left:892px; top:1178px; width:150px; z-index:6; }}
"""
FIXED = f"""
<div class='ph' style='top:180px; background-image:url({LOIDA})'></div>
<div class='ph' style='top:742px; background-image:url({CASEY})'></div>
<div class='who' style='top:352px'><div class='n'>Loida<br>Vasquez</div><div class='t'>Advanced Programs Lead &amp;<br>Mentor</div></div>
<div class='who' style='top:925px'><div class='n'>Casey<br>Williams</div><div class='t'>Mentor &amp; Consultant</div></div>
<img class='logo' src='{LOGO}'>
"""
def page(css, deco): return f"<!doctype html><html><head><meta charset='utf-8'><style>{BASE}{css}</style></head><body>{deco}{FIXED}</body></html>"
def scratch(op=1): return f"<div class='abs' style='inset:0; background:url({SCRATCH}); background-size:cover; opacity:{op}'></div>"

def garland():
    """Pressed flowers and leaves hanging from a twine across the top."""
    random.seed(3); out = ["<svg class='abs' style='left:0; top:0' width='1080' height='200'><path d='M -10 40 Q 540 140 1090 40' stroke='#8a6d55' stroke-width='3' fill='none'/></svg>"]
    for i in range(9):
        x = 40 + i * 120; y = 40 + 100 * (1 - ((x - 540) / 550) ** 2) * .5 * 2 - 6
        img = PRESSED[i % 4]; rot = random.uniform(-25, 25) + 180 * 0
        out.append(f"<img class='abs' src='{img}' style='left:{x-40}px; top:{y-8}px; width:{random.randint(95,130)}px; transform:rotate({rot}deg); transform-origin:50% 0'>")
    return "".join(out)

def paper_flags():
    random.seed(5); out = ["<svg class='abs' style='left:0; top:0' width='1080' height='200'><path d='M -10 30 Q 540 110 1090 30' stroke='#4C3634' stroke-width='3' fill='none'/></svg>"]
    cols = ["#31662F", "#D39C48", "#B1BCB1", "#4C3634", "#C09D7F", "#654D76"]
    for i in range(10):
        cx = 54 + i * 108; top = 30 + 80 * (1 - ((cx - 540) / 550) ** 2) - 4
        c = cols[i % len(cols)]
        out.append(f"<div class='abs' style='left:{cx-46}px; top:{top}px; width:92px; height:110px; background:{c}; "
                   f"clip-path:polygon(0 0, 100% 0, 52% 100%, 46% 96%); transform:rotate({random.uniform(-4,4)}deg)'>"
                   f"<div style='position:absolute; inset:0; background:url({SCRATCH}); background-size:600px; opacity:.55; mix-blend-mode:screen'></div></div>")
    return "".join(out)

D = {}
D[1] = page("", scratch() + garland() + f"<img class='abs' src='{SOIL}' style='left:0; top:1110px; width:1080px'>")
D[2] = page(".leak { inset:0; background:radial-gradient(60% 45% at 100% 0%, rgba(245,190,110,.75), rgba(245,190,110,0) 70%), radial-gradient(40% 30% at 0% 100%, rgba(211,156,72,.35), rgba(211,156,72,0) 70%); }",
            scratch(.8) + "<div class='abs leak'></div>"
            + "".join(f"<div class='abs' style='left:{x}px; top:{y}px; width:{s}px; height:{s}px; background:var(--gold); clip-path:polygon(50% 0, 60% 40%, 100% 50%, 60% 60%, 50% 100%, 40% 60%, 0 50%, 40% 40%)'></div>"
                      for x, y, s in [(620, 300, 34), (990, 520, 24), (640, 860, 26), (1000, 1080, 34), (600, 640, 18)]))
D[3] = page(f".ombre {{ inset:0; background:linear-gradient(180deg, var(--cream) 0%, var(--cream) 55%, #E3D3BF 72%, var(--tan) 86%, #8b6a55 100%); }}"
            f".dirt {{ left:0; right:0; bottom:0; height:420px; background:url({COMPOST}) 0 0 / 1600px auto; -webkit-mask-image:linear-gradient(0deg, #000 10%, transparent 95%); opacity:.9; }}",
            "<div class='abs ombre'></div><div class='abs dirt'></div>" + scratch(.5))
D[4] = page(".dots { right:0; bottom:0; width:1080px; height:1350px; background-image:radial-gradient(var(--green) 30%, transparent 32%); background-size:20px 20px;"
            " -webkit-mask-image:radial-gradient(120% 90% at 100% 100%, rgba(0,0,0,.55), transparent 60%); }",
            "<div class='abs' style='inset:0; background:linear-gradient(160deg, #EEF0EA, #DDE3DA)'></div><div class='abs dots'></div>" + scratch(.6))
D[5] = page(".strip { left:-40px; width:1160px; }",
            "<div class='abs' style='inset:0; background:#EFE7DA'></div>"
            "<div class='abs strip' style='top:110px; height:340px; background:var(--sage); opacity:.55; transform:rotate(-3deg); clip-path:polygon(0 4%, 20% 0, 45% 6%, 70% 1%, 100% 5%, 100% 95%, 75% 100%, 50% 94%, 25% 100%, 0 96%)'></div>"
            "<div class='abs strip' style='top:640px; height:380px; background:var(--tan); opacity:.45; transform:rotate(2deg); clip-path:polygon(0 3%, 30% 0, 60% 5%, 100% 0, 100% 97%, 65% 100%, 35% 95%, 0 100%)'></div>"
            "<div class='abs strip' style='top:1180px; height:260px; background:var(--leaf); opacity:.35; transform:rotate(-2deg); clip-path:polygon(0 8%, 35% 0, 70% 7%, 100% 2%, 100% 100%, 0 100%)'></div>" + scratch(.7))
def brush(x, y, w, h, seed):
    random.seed(seed); lines = []
    for k in range(40):
        yy = random.gauss(h / 2, h * .18); a = random.uniform(.25, .6); sw = random.uniform(3, 8)
        lines.append(f"<path d='M {random.uniform(0,30):.0f} {yy:.0f} C {w*.3:.0f} {yy+random.uniform(-6,6):.0f}, {w*.7:.0f} {yy+random.uniform(-6,6):.0f}, {w-random.uniform(0,40):.0f} {yy+random.uniform(-4,4):.0f}' stroke='#D39C48' stroke-opacity='{a:.2f}' stroke-width='{sw:.1f}' fill='none' stroke-linecap='round'/>")
    return f"<svg class='abs' style='left:{x}px; top:{y}px' width='{w}' height='{h}'>{''.join(lines)}</svg>"
D[6] = page("", scratch() + brush(590, 330, 460, 260, 1) + brush(590, 905, 460, 230, 2))
D[7] = page(".blob { border-radius:50%; filter:blur(110px); }",
            "<div class='abs blob' style='left:-200px; top:-160px; width:700px; height:600px; background:var(--leaf); opacity:.55'></div>"
            "<div class='abs blob' style='right:-220px; top:420px; width:620px; height:620px; background:var(--gold); opacity:.5'></div>"
            "<div class='abs blob' style='left:200px; bottom:-260px; width:760px; height:520px; background:var(--purple); opacity:.35'></div>")
def green_line(name, x, y, w, op):
    return f"<img class='abs' src='{A(f'assets/collage/cutouts/line-{name}-1.png')}' style='left:{x}px; top:{y}px; width:{w}px; opacity:{op}; filter:sepia(1) hue-rotate(50deg) saturate(2.5) brightness(.9)'>"
D[8] = page("", scratch(.8) + green_line("tithonia", 760, 20, 360, .45) + green_line("seedling-roots", 600, 1090, 480, .35) + green_line("mushroom-cluster", 830, 600, 260, .35))
def terrazzo():
    random.seed(8); cols = ["#31662F", "#D39C48", "#B1BCB1", "#C09D7F", "#654D76", "#4C3634"]; out = []
    for _ in range(170):
        x, y, r = random.uniform(0, 1080), random.uniform(0, 1350), random.uniform(8, 20)
        pts = " ".join(f"{x + r*random.uniform(.5,1.2)*math.cos(a):.0f},{y + r*random.uniform(.5,1.2)*math.sin(a):.0f}" for a in [i * math.pi / 3 for i in range(6)])
        out.append(f"<polygon points='{pts}' fill='{random.choice(cols)}' fill-opacity='.28'/>")
    return f"<svg class='abs' style='left:0; top:0' width='1080' height='1350'>{''.join(out)}</svg>"
D[9] = page(".frame { inset:22px; border:14px solid var(--green); border-radius:28px; }", terrazzo() + scratch(.5) + "<div class='abs frame'></div>")
D[10] = page("", scratch() + paper_flags()
             + f"<img class='abs' src='{PRESSED[0]}' style='left:-30px; top:1130px; width:240px; transform:rotate(-20deg)'>"
             + f"<img class='abs' src='{PRESSED[3]}' style='left:600px; top:1210px; width:220px; transform:rotate(8deg)'>")

files = []
for k, html in D.items():
    p = os.path.join(OUT, f"design-{k:02d}.html"); open(p, "w").write(html); files.append(p)
js = os.path.join(OUT, "render.js")
open(js, "w").write("""const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => { const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of %s) { await p.goto('file://' + f); await p.waitForTimeout(400); await p.screenshot({ path: f.replace('.html', '.png') }); }
  await b.close(); })();""" % json.dumps(files))
subprocess.run(["node", js], check=True)
from PIL import Image
sheet = Image.new("RGB", (5 * 432 + 6 * 12, 2 * 540 + 3 * 12), (60, 60, 60))
for i, f in enumerate(files):
    sheet.paste(Image.open(f.replace(".html", ".png")).convert("RGB").resize((432, 540)), (12 + (i % 5) * 444, 12 + (i // 5) * 552))
sheet.save(os.path.join(OUT, "contact.png")); print("ok")
