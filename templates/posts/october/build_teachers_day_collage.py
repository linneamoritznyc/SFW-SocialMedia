"""World Teachers' Day (5 Oct 2026), collage version: same 10 slides, people and words as option 4, restyled after
Linnea's leaf-frame reference. Cream paper cards taped onto a soft gradient that runs brown -> tan -> sage across the
carousel (each slide starts where the last one ended, so the swipe is one long colour change), the paper-cut
microscope, pressed flowers from Unsplash (cut out), and white line-art plants. No dark green background.

python3 templates/posts/october/build_teachers_day_collage.py
Unsplash credits: assets/unsplash-flowers/CREDITS.md; photographers are named in small text on the slides that use them.
"""
import os
from pptx.util import Emu
from pptx.oxml.ns import qn
from lxml import etree
from lib import Deck, rect, text, crop, Tilt, PX, HEAD, BODY
from build_oct_01_10 import logo, pic, save
from build_teachers_day_v2 import portrait, para
from build_teachers_day_options import MENTORS, unicodedata, mentor_text

W, H = 1080, 1350
GREEN, CREAM, BROWN, TAN, SAGE, INK = "31662F", "F3F1EA", "4C3634", "C09D7F", "B1BCB1", "333130"
PAPER = "FBF8F1"
FL = "assets/unsplash-flowers/"
LINE = "assets/collage/white-line/"
MICRO = "assets/collage/cutouts/microscope-paper-1.png"
NOTE = (" Mentor photos: Linnea's Drive folder (5 Oct 2026). Pressed flowers and meadow: Unsplash, credits in "
        "assets/unsplash-flowers/CREDITS.md. Microscope and line art: SFW collage pieces (assets/collage/).")

# gradient stops along the whole carousel (slide 1 left edge -> slide 10 right edge)
STOPS = ["4C3634", "7E6352", "C09D7F", "B9AE98", "B1BCB1", "9DA89C", "C09D7F", "8E705E", "6A4E45", "4C3634", "4C3634"]


def mix(a, b, t):
    a = [int(a[i:i + 2], 16) for i in (0, 2, 4)]; b = [int(b[i:i + 2], 16) for i in (0, 2, 4)]
    return "".join(f"{round(x + (y - x) * t):02X}" for x, y in zip(a, b))


def gradient(s, c1, c2, angle=0, x=0, y=0, w=W, h=H, a1=None, a2=None):
    """Rectangle with a two-stop linear gradient (angle 0 = left to right, 90 = top to bottom). a1/a2: opacity 0-100."""
    r = rect(s, x, y, w, h, c1)
    sp = r._element.spPr
    for tag in ("a:solidFill",):
        old = sp.find(qn(tag))
        if old is not None: sp.remove(old)
    g = etree.SubElement(sp, qn("a:gradFill")); g.set("rotWithShape", "1")
    lst = etree.SubElement(g, qn("a:gsLst"))
    for pos, c, a in ((0, c1, a1), (100000, c2, a2)):
        gs = etree.SubElement(lst, qn("a:gs")); gs.set("pos", str(pos))
        clr = etree.SubElement(gs, qn("a:srgbClr")); clr.set("val", c)
        if a is not None: etree.SubElement(clr, qn("a:alpha")).set("val", str(int(a * 1000)))
    lin = etree.SubElement(g, qn("a:lin")); lin.set("ang", str(int(angle * 60000))); lin.set("scaled", "0")
    ln = sp.find(qn("a:ln"))                      # gradFill must come before a:ln
    if ln is not None: sp.remove(ln); sp.append(ln)
    return r


def background(s, i):
    gradient(s, STOPS[i], STOPS[i + 1], angle=0)


def tape(s, cx, cy, deg, w=150, h=44):
    rect(s, cx - w / 2, cy - h / 2, w, h, "DCE5C8", alpha=72, tl=Tilt(cx, cy, deg))


def card(s, x, y, w, h):
    rect(s, x, y, w, h, PAPER)
    tape(s, x + 40, y + 8, -32); tape(s, x + w - 40, y + 8, 32)


def line_art(s, name, x, y, w, alpha_note=""):
    return pic(s, LINE + f"white-{name}-1.png", x, y, w)


def flower(s, name, x, y, w, deg=0):
    return pic(s, FL + f"{name}-cut.png", x, y, w, deg=deg)


def credit(s, t, x=40, y=H - 34, color=CREAM):
    text(s, x, y, 700, 24, t, 13, color, BODY)


ORDER = sorted(MENTORS, key=lambda m: unicodedata.normalize("NFD", m[1].split()[-1] if m[0] == "Carla" else m[1]))
GRID = list(ORDER); _j = next(k for k, m in enumerate(GRID) if m[0] == "Ib"); GRID[_j], GRID[8] = GRID[8], GRID[_j]

# per mentor slide: (white line art: name, x, y, w), (pressed flower: name, x, y, w, deg), microscope corner or None
DECOR = [
    (("tithonia", 200, 1000, 520), ("pressed-red-fern", 860, 60, 200, 12), "br"),
    (("mushroom-cluster", 360, 1060, 460), ("pressed-yellow", -40, 70, 230, -10), None),
    (("coffee-branch", 240, 1010, 520), ("pressed-sprig", 830, 70, 230, 8), "br"),
    (("seedling-roots", 300, 1040, 560), ("pressed-four", -60, 60, 260, -6), None),
    (("orange-branch", 240, 1010, 520), ("pressed-red-fern", 860, 60, 200, 12), "br"),
    (("tithonia", 380, 1000, 480), ("pressed-yellow", -40, 70, 230, -10), None),
    (("mushroom-cluster", 260, 1060, 460), ("pressed-sprig", 830, 70, 230, 8), "br"),
]


def light(c):
    r, g, b = (int(c[i:i + 2], 16) for i in (0, 2, 4))
    return 0.299 * r + 0.587 * g + 0.114 * b > 150


def names(s, m, x, y, w, maxy):
    """Name and role. Name size picked so the longest word fits on one line (no broken words)."""
    from PIL import ImageFont
    f = lambda p: ImageFont.truetype(os.path.expanduser("~/.fonts/Montserrat-Bold.ttf"), int(p * 4 / 3))
    name = f"{'Dr. ' if m[0] == 'Carla' else ''}{m[0]} {m[1]}"
    longest = max((w_ for mm in MENTORS for w_ in (mm[0] + ' ' + mm[1]).split()), key=len)   # same size for everyone
    pt = next((p for p in (38, 34, 31, 28, 26) if f(p).getlength(longest) * 1.15 <= w), 26)  # x1.15: bold is wider
    yy = para(s, x, y, w, name, (pt,), GREEN, HEAD, True, sp=1.0) + 10
    para(s, x, yy, w, m[2], (24,), INK, BODY)


def mentor_slide(d, i, pair, decor):
    s = d.slide(None, "Mentors: " + ", ".join(f"{m[0]} {m[1]}" for m in pair) + "." + NOTE, counter=False)
    background(s, i)
    la, fl, mic = decor
    line_art(s, *la)
    card(s, 90, 100, 900, 1060)
    for k, m in enumerate(pair):
        y = 145 + k * 500
        portrait(s, m[5], m[6], 130, y, 450, 450)
        names(s, m, 615, y + 150, 345, y + 450)
        if k == 0: rect(s, 130, y + 475, 820, 2, TAN, alpha=50)
    flower(s, *fl)
    if mic: pic(s, MICRO, 840, 1030, 230)
    end = mix(STOPS[i], STOPS[i + 1], 0.1 if mic else 0.9)
    logo(s, 40 if mic else W - 40 - 130, H - 140, 130, white=not light(end))
    credit(s, "Pressed flowers: Evie S. and Angèle Kamp on Unsplash", x=(200 if mic else 40), y=H - 34,
           color=INK if light(STOPS[i]) else CREAM)


def build():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-collage")

    # 1 cover: meadow photo, brown gradient from the bottom, cream card with the title, microscope, line art
    s = d.slide(None, "Cover: meadow photo (Annie Spratt, Unsplash) under a brown gradient; cream card." + NOTE, counter=False)
    s.shapes.add_picture(crop(FL + "meadow-poppies.jpg", 1080, 1350, 0.5, 0.5), 0, 0, Emu(W * PX), Emu(H * PX))
    gradient(s, BROWN, BROWN, angle=90, a1=15, a2=92)
    line_art(s, "tithonia", -110, 760, 420)
    card(s, 110, 250, 860, 640)
    text(s, 150, 320, 780, 40, "OCTOBER 5", 24, BROWN, HEAD, True, track=4, align="c")
    text(s, 150, 380, 780, 260, "Happy World Teachers' Day", 78, GREEN, HEAD, True, spacing=1.0, align="c")
    text(s, 220, 660, 640, 100, "Thank you to everyone who teaches and mentors our students.", 30, INK, BODY,
         spacing=1.15, align="c")
    flower(s, "pressed-red-fern", 40, 140, 230, -14)
    pic(s, MICRO, 760, 760, 280)
    logo(s, (W - 230) / 2, 1020, 230, white=True)
    text(s, 0, 1250, W, 40, "Swipe →", 24, CREAM, HEAD, True, align="c")
    credit(s, "Meadow: Annie Spratt on Unsplash. Pressed flowers: Evie S. on Unsplash", y=H - 34)

    # 2-8 two mentors each
    for k in range(7):
        mentor_slide(d, k + 1, ORDER[2 * k:2 * k + 2], DECOR[k])

    # 9 grid on a card
    s = d.slide(None, "All fourteen on one card." + NOTE, counter=False)
    background(s, 8)
    line_art(s, "seedling-roots", 640, 980, 520)
    card(s, 40, 90, 1000, 1170)
    cell, gap, cap = 210, 12, 34
    x0 = (W - 4 * cell - 3 * gap) / 2; y0 = 140; rowh = cell + cap + 12
    text(s, x0, y0 + 4, 2 * cell + gap, 110, "Happy World Teachers' Day", 38, GREEN, HEAD, True, spacing=1.0)
    lw = 130; logo(s, x0, y0 + cell + cap - lw * 668 / 743, lw, white=False)
    for i, m in enumerate(GRID):
        c = i + 2; x = x0 + (c % 4) * (cell + gap); y = y0 + (c // 4) * rowh
        portrait(s, m[5], m[6], x, y, cell, cell)
        last = m[1].split()[-1] if m[0] == "Carla" else m[1]
        text(s, x, y + cell + 5, cell, cap - 5, f"{m[0]} {last}", 17, INK, BODY)
    flower(s, "pressed-sprig", 840, 30, 220, 10)
    pic(s, MICRO, 40, 1150, 190)
    credit(s, "Pressed flowers: Evie S. on Unsplash", x=250, y=H - 34)

    # 10 closing: dried flowers photo, gradient, big logo
    s = d.slide(None, "Closing: dried flowers (Katsia Jazwinska, Unsplash) under a brown gradient; big logo." + NOTE,
                counter=False)
    s.shapes.add_picture(crop(FL + "dried-row.jpg", 1080, 1350, 0.5, 0.5), 0, 0, Emu(W * PX), Emu(H * PX))
    gradient(s, BROWN, BROWN, angle=90, a1=92, a2=35)
    line_art(s, "mushroom-cluster", 720, 60, 420)
    text(s, 80, 230, 920, 50, "OCTOBER 5", 26, CREAM, HEAD, True, track=4, align="c")
    text(s, 80, 290, 920, 260, "Happy World Teachers' Day", 80, CREAM, HEAD, True, spacing=1.0, align="c")
    logo(s, (W - 320) / 2, 600, 320, white=True)
    pic(s, MICRO, 60, 980, 260)
    text(s, 0, 1200, W, 40, "soilfoodweb.com", 26, CREAM, HEAD, True, align="c")
    credit(s, "Dried flowers: Katsia Jazwinska on Unsplash", y=H - 34)

    save(d, "05-10-2026-mon-ig-teachers-day-collage.pptx")


if __name__ == "__main__":
    build()
