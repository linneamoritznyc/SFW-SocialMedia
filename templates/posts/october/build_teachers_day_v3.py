"""World Teachers' Day, version 3: Stephanie McDaniel's Canva edit (6 Oct 2026) rebuilt as an editable PPTX.

- Bunting, balloons and stars in Stephanie's brand colours: green, gold, light green, brown.
- Soil from a real compost photo (assets/photo/hand-of-compost.jpg, cut into low mounds with loose crumbs:
  assets/texture/soil-corner-*.png) in place of the splatter brushes.
- Light paper grain on the cream background.
- Names and titles per Stephanie; "SFW" dropped; Kavi Reddy added (Permaculture Instructor). 15 people, three per
  slide so everyone gets the same space. Kavi's photo is still needed: her square shows the logo until it arrives.
- Wording: "instructors and education staff" rather than "teachers" (Stephanie, planning doc comment, 6 Oct 2026).

python3 templates/posts/october/build_teachers_day_v3.py
"""
import math, unicodedata
from lib import Deck, rect, poly, text, Tilt, HEAD, BODY
from build_oct_01_10 import logo, logo_box, pic, save
from build_teachers_day_v2 import portrait, para
from build_teachers_day_options import MENTORS as _M, balloon, star

W, H, M = 1080, 1350, 80
GREEN, GOLD, LEAF, BROWN = "31662F", "D39C48", "6AA46F", "4C3634"     # Stephanie's Canva palette
CREAM, INK = "F3F1EA", "333130"
FLAGS = [GREEN, GOLD, LEAF, BROWN]
GRAIN = "assets/texture/cream-grain.png"
SOIL_A, SOIL_B = "assets/texture/soil-corner-a.png", "assets/texture/soil-corner-b.png"
NOTE = (" Mentor photos: Linnea's Drive folder (5 Oct 2026). Soil: cut from assets/photo/hand-of-compost.jpg. "
        "Names and titles: Stephanie McDaniel, 6 Oct 2026.")

STAFF = {
    "Tommy": ("Tommy", "Tepper", "Education Department Director & Mentor"),
    "Loida": ("Loida", "Vasquez", "Advanced Programs Lead"),
    "Carla": ("Carla", "Ribeiro Machado e Portugal", "Mentor & Science Lead"),
    "Wesley": ("Wesley", "Sander", "Consultant & Mentor"),
    "Casey": ("Casey", "Williams", "Consultant & Mentor"),
    "Brian": ("Brian", "Daubenspeck", "Consultant & Mentor"),
    "Isadora": ("Isadora", "Schmidt", "Consultant & Mentor"),
    "Ayşen": ("Ayşen", "Üstünay", "Consultant & Mentor"),
    "Dora": ("Dora", "Tkalec", "Consultant & Mentor"),
    "Gerald": ("Gerald", "Ramírez", "Mentor"),
    "Elena": ("Elena", "Kalli", "School Administration Officer"),
    "Ib": ("Ib", "Borup Pedersen", "Farmer, Consultant & Mentor"),
    "Nick": ("Nick", "Padwick", "Farmer, Consultant & Mentor"),
    "Delvin": ("Delvin", "Solkinson", "Graham Bell Legacy PDC Permaculture Lead Instructor"),
}
PEOPLE = [STAFF[m[0]] + tuple(m[3:]) for m in _M]
PEOPLE.append(("Kavi", "Reddy", "Permaculture Instructor", None, None, None, None, ()))   # photo still needed
ORDER = sorted(PEOPLE, key=lambda m: unicodedata.normalize("NFD", m[1].split()[-1] if m[0] == "Carla" else m[1]))


def bunting(s, y=20, n=11):
    pts = [(x, y + 40 * math.sin(math.pi * x / W)) for x in range(-20, W + 40, 20)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        poly(s, [(x0, y0), (x1, y1), (x1, y1 + 3), (x0, y0 + 3)], BROWN)
    step = W / n
    for i in range(n):
        cx = step * (i + 0.5); top = y + 40 * math.sin(math.pi * cx / W)
        poly(s, [(cx - 44, top), (cx + 44, top), (cx, top + 100)], FLAGS[i % 4])


def base(d, note):
    s = d.slide(CREAM, note, counter=False)
    pic(s, GRAIN, 0, 0, W, H)
    return s


def soil(s, left=True, right=True, wa=640, wb=520):
    if left: pic(s, SOIL_A, 0, H - wa * 300 / 640, wa)
    if right:
        sh = pic(s, SOIL_B, W - wb, H - wb * 260 / 520, wb)
        sh._element.spPr.getparent()  # keep handle
        flip = sh._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm")
        flip.set("flipH", "1")


def bouquet(s, side):
    base_x = 210 if side < 0 else W - 210
    for dx, top, w, c in [(-70, 800, 150, GREEN), (60, 740, 160, GOLD), (0, 910, 140, LEAF)]:
        balloon(s, base_x + side * dx, top, w, c, H - 120)


def photo(s, m, x, y, size):
    if m[5]: portrait(s, m[5], m[6], x, y, size, size)
    else: logo_box(s, x, y, size, size)


def cover(d, title, sub, foot):
    s = base(d, "Cover / closing: bunting, balloons, stars, soil (PowerPoint shapes and cut photo)." + NOTE)
    bunting(s, y=40, n=9)
    star(s, 330, 278, 34, GOLD); star(s, W - 330, 278, 34, GOLD)
    text(s, M, 255, W - 2 * M, 50, "OCTOBER 5", 26, GREEN, HEAD, True, track=4, align="c")
    text(s, M, 320, W - 2 * M, 280, title, 76, GREEN, HEAD, True, spacing=1.0, align="c")
    if sub: text(s, (W - 680) / 2, 600, 680, 100, sub, 30, INK, BODY, spacing=1.15, align="c")
    bouquet(s, -1); bouquet(s, 1)
    soil(s)
    logo(s, (W - 300) / 2, 760, 300, white=False)
    text(s, M, 1110, W - 2 * M, 40, foot, 24, BROWN, HEAD, True, align="c")
    return s


def build():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-v3")
    cover(d, "Happy World Teachers' Day", "Thank you to our instructors and education staff.", "Swipe →")

    for k in range(0, len(ORDER), 3):                      # five slides, three people each, same layout for all
        group = ORDER[k:k + 3]
        s = base(d, "People: " + ", ".join(f"{m[0]} {m[1]}" for m in group) + "." + NOTE)
        bunting(s)
        cell, top, rowh = 320, 165, 350
        for i, m in enumerate(group):
            y = top + i * rowh
            photo(s, m, 70, y, cell)
            name = f"{'Dr. ' if m[0] == 'Carla' else ''}{m[0]} {m[1]}"
            yy = para(s, 430, y + cell / 2 - 60, 580, name, (38, 34, 30), GREEN, HEAD, True, sp=1.0, maxh=150) + 10
            para(s, 430, yy, 580, m[2], (25, 23), INK, BODY, maxh=y + cell - yy)
        soil(s, left=False, right=True, wb=440)              # bottom right, clear of the photos
        logo(s, 70, H - 140, 120, white=False)

    # grid: title row across the top, then 5 x 3 same-size squares
    s = base(d, "Everyone in one grid." + NOTE)
    bunting(s)
    text(s, 48, 195, 700, 120, "Happy World Teachers' Day", 44, GREEN, HEAD, True, spacing=1.0)
    logo(s, W - 48 - 140, 180, 140, white=False)
    n, gap, cap = 5, 10, 32
    cell = (W - 96 - (n - 1) * gap) / n
    for i, m in enumerate(ORDER):
        x = 48 + (i % n) * (cell + gap); y = 360 + (i // n) * (cell + cap + 14)
        photo(s, m, x, y, cell)
        last = m[1].split()[-1] if m[0] == "Carla" else m[1]
        text(s, x, y + cell + 5, cell, cap - 5, f"{m[0]} {last}", 15, INK, BODY)
    soil(s, wa=520, wb=440)

    cover(d, "Happy World Teachers' Day", "", "soilfoodweb.com")
    save(d, "05-10-2026-mon-ig-teachers-day-v3.pptx")


if __name__ == "__main__":
    build()
