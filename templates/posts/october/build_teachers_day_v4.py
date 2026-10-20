"""World Teachers' Day, version 4: Stephanie McDaniel's layout and feedback, soil version B (Linnea, 6 Oct 2026).

Stephanie's feedback, all applied:
- her bunting colours; balloons in the brand palette (docs/brand-colors.md)
- the new logo with flowers (assets/logo/, Final Oct 2026)
- names checked: Tepper, Schmidt, Sander, Pedersen, Ramírez, Üstünay
- titles: Carla "Mentor & Science Lead"; Tommy "Education Department Director & Mentor"; no "SFW"; titles as in her Canva
- how long each person has been on the team, on a highlighter stroke ("highlights")
- texture: scratched paper after her Dora and Ayşen slide; real soil, kept off the staff photos
- Kavi Reddy added (Permaculture Instructor); "instructors and education staff" rather than "teachers"
- two people per slide, as in her Canva

The soil strip (Replicate flat-lay, assets/collage/cutouts/soil-flatlay-border.png) runs along the bottom of every slide,
mirrored on every other slide so the strip joins up across the swipe.

python3 templates/posts/october/build_teachers_day_v4.py
"""
from PIL import ImageFont
import os
from lib import Deck, rect, text, Tilt
from build_oct_01_10 import logo, logo_box, pic, save
from build_teachers_day_v2 import portrait, para
from build_teachers_day_options import balloon, star
from build_teachers_day_v3 import base, bunting, ORDER as _ORDER, GREEN, GOLD, BROWN, INK, W, H, M, NOTE

TAN, PURPLE, BLUE, SAGE = "C09D7F", "654D76", "4B7FB4", "B1BCB1"
SOIL = "assets/collage/cutouts/soil-flatlay-border.png"      # 2048 x 989, soil dense from row ~590
SOIL_TOP = 1185                                               # where the soil starts on every slide

TITLES = {"Loida": "Advanced Programs Lead & Mentor"}          # as in Stephanie's Canva
ORDER = [m[:2] + (TITLES.get(m[0], m[2]),) + m[3:] for m in _ORDER]

# Start years. Sourced: Loida (first employee, 19 Feb 2019) and Carla (joined June 2019), all-hands notes 17 Sep 2026;
# Wesley (mentor since June 2020), his team page bio. Everyone else: blank until we have the Team Directory.
SINCE = {"Loida": 2019, "Carla": 2019, "Wesley": 2020}


def soil(s, i):
    sh = pic(s, SOIL, 0, SOIL_TOP - 0.40 * 1080 * 989 / 2048, W)
    if i % 2: sh._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm").set("flipH", "1")


def since(s, x, y, who):
    label = f"On the team since {SINCE[who]}" if who in SINCE else "On the team since ____"
    w = ImageFont.truetype(os.path.expanduser("~/.fonts/Montserrat-Bold.ttf"), 27).getlength(label) * 1.12
    rect(s, x - 8, y - 2, w + 16, 34, GOLD, alpha=42, tl=Tilt(x + w / 2, y + 15, -1.5))     # highlighter stroke
    text(s, x, y, w + 10, 32, label, 20, BROWN, "Montserrat", True)


def person(s, m, y, cell=470):
    if m[5]: portrait(s, m[5], m[6], 80, y, cell, cell)
    else: logo_box(s, 80, y, cell, cell)
    name = f"{'Dr. ' if m[0] == 'Carla' else ''}{m[0]} {m[1]}"
    yy = para(s, 595, y + cell / 2 - 70, 420, name, (44, 40, 36, 32), GREEN, "Montserrat", True, sp=1.0, maxh=170) + 12
    para(s, 595, yy, 420, m[2], (26, 24), INK, "Source Sans 3", maxh=120)   # no "on the team since" (Linnea)


def bouquet(s, side, top_y, tie_y):
    bx = 150 if side < 0 else W - 150
    cols = [GREEN, PURPLE, SAGE] if side < 0 else [GOLD, BLUE, TAN]
    for (dx, t, w), c in zip([(-40, 0, 125), (45, -50, 135), (0, 80, 115)], cols):
        balloon(s, bx + side * dx, top_y + t, w, c, tie_y)


def build():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-v4")

    s = base(d, "Cover." + NOTE)
    bunting(s, y=40, n=9)
    star(s, 330, 248, 34, GOLD); star(s, W - 330, 248, 34, GOLD)
    text(s, M, 225, W - 2 * M, 50, "OCTOBER 5", 26, GREEN, "Montserrat", True, track=4, align="c")
    text(s, M, 285, W - 2 * M, 240, "Happy World Teachers' Day", 76, GREEN, "Montserrat", True, spacing=1.0, align="c")
    text(s, (W - 680) / 2, 545, 680, 90, "Thank you to our instructors and education staff.", 30, INK, "Source Sans 3",
         spacing=1.15, align="c")
    bouquet(s, -1, 640, SOIL_TOP + 30); bouquet(s, 1, 640, SOIL_TOP + 30)
    logo(s, (W - 270) / 2, 690, 270, white=False)
    text(s, M, 960, W - 2 * M, 40, "Swipe →", 24, BROWN, "Montserrat", True, align="c")
    soil(s, 0)

    pairs = [ORDER[k:k + 2] for k in range(0, len(ORDER), 2)]
    for i, pair in enumerate(pairs, start=1):
        s = base(d, "People: " + ", ".join(f"{m[0]} {m[1]}" for m in pair) + "." + NOTE)
        bunting(s)
        person(s, pair[0], 190)
        if len(pair) == 2:
            person(s, pair[1], 700)
        else:                                  # last person: same size as everyone, the thank-you sits beside them
            text(s, 80, 760, 920, 180, "Thank you to all our instructors and education staff.", 40, GREEN, "Montserrat",
                 True, spacing=1.05)
        logo(s, W - 40 - 120, 1040, 120, white=False)
        soil(s, i)

    # everyone: title row, then 5 x 3 same-size squares
    s = base(d, "Everyone in one grid." + NOTE)
    bunting(s)
    text(s, 48, 190, 760, 120, "Happy World Teachers' Day", 44, GREEN, "Montserrat", True, spacing=1.0)
    logo(s, W - 48 - 140, 175, 140, white=False)
    n, gap, cap = 5, 10, 32
    cell = (W - 96 - (n - 1) * gap) / n
    for i, m in enumerate(ORDER):
        x = 48 + (i % n) * (cell + gap); y = 350 + (i // n) * (cell + cap + 14)
        if m[5]: portrait(s, m[5], m[6], x, y, cell, cell)
        else: logo_box(s, x, y, cell, cell)
        last = m[1].split()[-1] if m[0] == "Carla" else m[1]
        text(s, x, y + cell + 5, cell, cap - 5, f"{m[0]} {last}", 15, INK, "Source Sans 3")
    soil(s, len(pairs) + 1)
    save(d, "05-10-2026-mon-ig-teachers-day-v4.pptx")


if __name__ == "__main__":
    build()
