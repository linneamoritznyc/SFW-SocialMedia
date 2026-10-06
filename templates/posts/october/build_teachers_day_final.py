"""World Teachers' Day, final carousel (Linnea, 6 Oct 2026): Stephanie's layout (two square photos on the left, name and
title on the right, logo bottom right), all fifteen people, two per slide, on the three backgrounds Linnea picked from
the design round, taking turns:

  dark   soil-brown gradient, cream scratches, faint white line-art plants, gold edge on the photos, cream type
  soil   real compost photo full bleed, cream cards under each person, a pressed sprig
  sage   soft sage gradient with the soil and seedlings strip along the bottom

Names and titles as approved (Stephanie's edits); no "SFW", no "on the team since". New logo with flowers.
Kavi Reddy's photo is still needed: her square shows the logo until it arrives.

python3 templates/posts/october/build_teachers_day_final.py
"""
from pptx.util import Emu
from lib import Deck, rect, text, crop, PX
from build_oct_01_10 import logo, logo_box, pic, save
from build_teachers_day_v2 import portrait, para
from build_teachers_day_v4 import ORDER, soil
from build_teachers_day_collage import gradient

W, H, M = 1080, 1350, 80
GREEN, GOLD, BROWN, INK, CREAM = "31662F", "D39C48", "4C3634", "333130", "F3F1EA"
NOTE = (" Photos: Linnea's Drive folder (5 Oct 2026). Compost: assets/photo/hand-of-compost.jpg. Soil strip: Replicate "
        "flat-lay, assets/collage/cutouts/soil-flatlay-border.png. Pressed sprig: Evie S. on Unsplash.")
CELL, X, TX, TW, ROWS = 470, 80, 595, 420, (190, 700)
# one name size for everyone: the largest at which the longest single word still fits on a line (no broken names)
from PIL import ImageFont; import os
_f = lambda p: ImageFont.truetype(os.path.expanduser("~/.fonts/Montserrat-Bold.ttf"), int(p * 4 / 3))
_longest = max((w for m in ORDER for w in (m[0] + " " + m[1]).split()), key=len)
NAME_PT = next(p for p in (44, 40, 38, 36, 34, 32) if _f(p).getlength(_longest) * 1.18 <= TW - 30)


def bg_dark(s):
    gradient(s, "6B4D45", "2F2120", angle=90)
    pic(s, "assets/texture/scratched-paper-on-dark.png", 0, 0, W, H)
    pic(s, "assets/collage/white-line/white-mushroom-cluster-soft.png", 760, -30, 360)
    pic(s, "assets/collage/white-line/white-tithonia-soft.png", -90, 900, 420)


def bg_soil(s):
    s.shapes.add_picture(crop("assets/photo/hand-of-compost.jpg", W, H, 0.0, 0.0), 0, 0, Emu(W * PX), Emu(H * PX))
    gradient(s, "F3C88C", "1E140F", angle=90, a1=25, a2=45)


def bg_sage(s):
    gradient(s, "DCE3DA", "B1BCB1", angle=90)


STYLE = {   # background, name colour, title colour, white logo?
    "dark": (bg_dark, CREAM, "E9DCC9", True),
    "soil": (bg_soil, GREEN, INK, True),
    "sage": (bg_sage, GREEN, INK, False),
}


def person(s, m, y, kind):
    _, nc, tc, _ = STYLE[kind]
    if kind == "soil":                                     # photo on the compost with a cream edge, text on a cream card
        rect(s, X - 10, y - 10, CELL + 20, CELL + 20, CREAM, shadow=True)
        rect(s, TX - 30, y + 60, W - 40 - (TX - 30), CELL - 120, CREAM, shadow=True)
    if kind == "dark": rect(s, X - 8, y - 8, CELL + 16, CELL + 16, GOLD)                             # gold edge
    if m[5]: portrait(s, m[5], m[6], X, y, CELL, CELL)
    else: logo_box(s, X, y, CELL, CELL)
    name = f"{'Dr. ' if m[0] == 'Carla' else ''}{m[0]} {m[1]}"
    yy = para(s, TX, y + CELL / 2 - 70, TW, name, (NAME_PT,), nc, "Montserrat", True, sp=1.0, maxh=170) + 12
    para(s, TX, yy, TW, m[2], (26, 24), tc, "Source Sans 3", maxh=120)


def finish(s, kind, logo_y=1190):
    if kind == "sage": soil(s, 1)
    logo(s, W - 40 - 140, logo_y, 140, white=True if kind == "sage" else STYLE[kind][3])   # sage: white logo on the soil


def build():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-final")

    # cover, dark
    s = d.slide(None, "Cover." + NOTE, counter=False); bg_dark(s)
    text(s, M, 300, W - 2 * M, 50, "OCTOBER 5", 26, GOLD, "Montserrat", True, track=4, align="c")
    text(s, M, 370, W - 2 * M, 260, "Happy World Teachers' Day", 84, CREAM, "Montserrat", True, spacing=1.0, align="c")
    text(s, (W - 700) / 2, 650, 700, 100, "Thank you to our instructors and education staff.", 32, "E9DCC9", "Source Sans 3",
         spacing=1.15, align="c")
    logo(s, (W - 280) / 2, 820, 280, white=True)
    text(s, M, 1150, W - 2 * M, 40, "Swipe →", 26, GOLD, "Montserrat", True, align="c")

    kinds = ["soil", "sage", "dark"]
    pairs = [ORDER[k:k + 2] for k in range(0, len(ORDER), 2)]
    for i, pair in enumerate(pairs):
        kind = kinds[i % 3]
        s = d.slide(None, f"People ({kind} background): " + ", ".join(f"{m[0]} {m[1]}" for m in pair) + "." + NOTE, counter=False)
        STYLE[kind][0](s)
        person(s, pair[0], ROWS[0], kind)
        if len(pair) == 2:
            person(s, pair[1], ROWS[1], kind)
        else:                                   # last person: same size as everyone; the thank-you sits below
            if kind == "soil": rect(s, X - 30, ROWS[1] - 20, W - 2 * (X - 30), 240, CREAM, shadow=True)
            text(s, X, ROWS[1] + 10, W - 2 * X, 200, "Thank you to all our instructors and education staff.", 42,
                 STYLE[kind][1], "Montserrat", True, spacing=1.05)
        if kind == "soil": pic(s, "assets/unsplash-flowers/pressed-sprig-cut.png", 850, 600, 210, deg=12)
        finish(s, kind)

    # everyone, sage
    s = d.slide(None, "Everyone in one grid." + NOTE, counter=False); bg_sage(s)
    text(s, 48, 120, 760, 130, "Happy World Teachers' Day", 48, GREEN, "Montserrat", True, spacing=1.0)
    logo(s, W - 48 - 150, 100, 150, white=False)
    n, gap, cap = 5, 10, 34
    cell = (W - 96 - (n - 1) * gap) / n
    for i, m in enumerate(ORDER):
        x = 48 + (i % n) * (cell + gap); y = 300 + (i // n) * (cell + cap + 16)
        if m[5]: portrait(s, m[5], m[6], x, y, cell, cell)
        else: logo_box(s, x, y, cell, cell)
        last = m[1].split()[-1] if m[0] == "Carla" else m[1]
        text(s, x, y + cell + 6, cell, cap - 4, f"{m[0]} {last}", 16, INK, "Source Sans 3")
    soil(s, 0)
    save(d, "05-10-2026-mon-ig-teachers-day-final.pptx")


if __name__ == "__main__":
    build()
