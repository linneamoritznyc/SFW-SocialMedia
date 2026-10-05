"""World Teachers' Day (5 Oct 2026): three more options, 2 slides each. No AI art and no paper-cut flowers: real
photos, drawn shapes (bunting, confetti), brand colours on cream.

1 Photo: the mentors' workshop group photo full bleed, then all fourteen faces.
2 Bunting: drawn bunting and confetti over the title with a row of faces, then all fourteen faces.
3 Grid cover: the title above the grid of all fourteen, then a thank-you slide with every name.

python3 templates/posts/october/build_teachers_day_options.py
"""
import math, random, unicodedata
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from lib import Deck, rect, poly, text, crop, PX, HEAD, BODY
from build_oct_01_10 import logo, save
from build_teachers_day_v2 import MENTORS, portrait, GARA

# Names and roles exactly as Linnea gave them (team page, 5 Oct 2026). Elina Psara, Caterina Capri, Laura Campos and
# Nora Levay are not on the team now (Linnea, 5 Oct 2026), so they are not in the post.
SITE = {
    "Tommy": ("Tommy", "Tapper", "Instructor"),
    "Loida": ("Loida", "Vasquez", "Advanced Programs Lead"),
    "Carla": ("Carla", "Ribeiro Machado e Portugal", "SFW Mentor"),
    "Wesley": ("Wesley", "Sander", "SFW Consultant & Mentor"),
    "Casey": ("Casey", "Williams", "SFW Consultant & Mentor"),
    "Brian": ("Brian", "Daubenspeck", "SFW Consultant & Mentor"),
    "Isadora": ("Isadora", "Shmidt", "SFW Consultant & Mentor"),
    "Aysen": ("Ayşen", "Üstünay", "SFW Consultant & Mentor"),
    "Dora": ("Dora", "Tkalec", "SFW Consultant & Mentor"),
    "Gerald": ("Gerald", "Ramírez", "SFW Mentor"),
    "Elena": ("Elena", "Kalli", "School Administration Officer"),
    "Ib": ("Ib", "Borup Pedersen", "Farmer, SFW Consultant & Mentor"),
    "Nick": ("Nick", "Padwick", "Farmer, SFW Consultant & Mentor"),
    "Delvin": ("Delvin", "Solkinson", "SFW Permaculture Lead"),
}
MENTORS = [SITE[m[0]] + tuple(m[3:]) for m in MENTORS]
DR = {"Carla", "Elina", "Caterina", "Nora"}

GREEN, CREAM, BROWN, TAN, SAGE, GOLD, BLACK = "31662F", "F3F1EA", "4C3634", "C09D7F", "B1BCB1", "D39C48", "333130"
W, H, M = 1080, 1350, 80
GROUP = "assets/mentors-teachers-day/group-mentors-workshop.jpg"
NOTE = (" Mentor photos: Linnea's Drive folder (5 Oct 2026) and assets/mentors-teachers-day/; written consent per the "
        "folder README.")


def dot(s, x, y, d, color):
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(d * PX)), Emu(int(d * PX)))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(color); sh.line.fill.background(); sh.shadow.inherit = False


def bunting(s, y=40, n=9):
    """String across the top with triangle flags in brand colours (drawn shapes, editable)."""
    cols = [GREEN, TAN, SAGE, BROWN]   # brand palette; gold is for donate and warnings only
    pts = [(x, y + 40 * math.sin(math.pi * x / W)) for x in range(-20, W + 40, 20)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        poly(s, [(x0, y0), (x1, y1), (x1, y1 + 3), (x0, y0 + 3)], BROWN)
    step = W / n
    for i in range(n):
        cx = step * (i + 0.5); top = y + 40 * math.sin(math.pi * cx / W)
        poly(s, [(cx - 44, top), (cx + 44, top), (cx, top + 100)], cols[i % len(cols)])


def confetti(s, n, box, seed):
    random.seed(seed)
    x0, y0, x1, y1 = box
    for _ in range(n):
        dot(s, random.uniform(x0, x1), random.uniform(y0, y1), random.uniform(9, 20),
            random.choice([GREEN, TAN, SAGE, BROWN]))


def balloon(s, cx, top, w, color, string_to):
    """A drawn balloon (PowerPoint shapes, editable): body, shine, knot and a wavy string."""
    h = w * 1.22
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int((cx - w / 2) * PX)), Emu(int(top * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(color); sh.line.fill.background(); sh.shadow.inherit = False
    rect(s, cx - w * 0.28, top + h * 0.16, w * 0.12, h * 0.2, CREAM, alpha=45, kind=MSO_SHAPE.OVAL)
    poly(s, [(cx - 9, top + h + 10), (cx + 9, top + h + 10), (cx, top + h - 4)], color)
    pts = [(cx + 10 * math.sin(t / 30), top + h + 10 + t) for t in range(0, int(string_to - top - h - 10), 6)]
    for (x0, y0), (x1, y1) in zip(pts, pts[1:]):
        poly(s, [(x0, y0), (x1, y1), (x1 + 2, y1), (x0 + 2, y0)], BROWN)


def bouquet(s, side):
    """Three balloons in a loose cluster at the bottom left (side=-1) or right (side=1), strings to the bottom edge."""
    base = 210 if side < 0 else W - 210
    for dx, top, w, c in [(-70, 820, 150, GREEN), (60, 760, 160, TAN), (0, 930, 140, SAGE)]:
        balloon(s, base + side * dx, top, w, c, H + 10)


def star(s, cx, cy, d, color):
    sh = s.shapes.add_shape(MSO_SHAPE.STAR_5_POINT, Emu(int((cx - d / 2) * PX)), Emu(int((cy - d / 2) * PX)),
                            Emu(int(d * PX)), Emu(int(d * PX)))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(color); sh.line.fill.background(); sh.shadow.inherit = False


def party(s, title, sub, foot):
    """Cover and closing layout: bunting, stars by the date, title, two balloon bouquets and a big logo between them."""
    bunting(s)
    star(s, 330, 278, 34, TAN); star(s, W - 330, 278, 34, TAN)
    text(s, M, 255, W - 2 * M, 50, "OCTOBER 5", 26, GREEN, HEAD, True, track=4, align="c")
    pt = 76 if len(title) < 30 else 56
    text(s, M, 320, W - 2 * M, 280, title, pt, GREEN, HEAD, True, spacing=1.0, align="c")
    if sub: text(s, M, 600, W - 2 * M, 100, sub, 30, BLACK, BODY, spacing=1.15, align="c")
    bouquet(s, -1); bouquet(s, 1)
    lw = 300
    logo(s, (W - lw) / 2, 760, lw, white=False)
    text(s, M, 1120, W - 2 * M, 40, foot, 24, BROWN, HEAD, True, align="c")


def faces(s, y0, color=GREEN, fill_cells=True, people=None, with_logo=False):
    """All mentors as a regular grid of same-size square photos. The title takes the first two cells of the top row
    (plain text, no box). with_logo: names as plain captions under each photo (no box) and the logo under the title;
    otherwise names sit on a cream strip inside each photo."""
    people = people or MENTORS
    n = 5 if len(people) > 14 else 4
    if with_logo:
        cell, gap, cap = 225, 12, 36
        x0 = (W - n * cell - (n - 1) * gap) / 2; rowh = cell + cap + 14
        text(s, x0, y0 + 4, 2 * cell + gap, 110, "Happy World Teachers' Day", 40, GREEN, HEAD, True, spacing=1.0)
        lw = 140; logo(s, x0, y0 + cell + cap - lw * 668 / 743, lw, white=False)
        for i, m in enumerate(people):
            c = i + 2; x = x0 + (c % n) * (cell + gap); y = y0 + (c // n) * rowh
            portrait(s, m[5], m[6], x, y, cell, cell)
            last = m[1].split()[-1] if m[0] == "Carla" else m[1]
            text(s, x, y + cell + 6, cell, cap - 6, f"{m[0]} {last}", 18, BLACK, BODY)
        return
    gap = 8
    cell = (W - 2 * 48 - (n - 1) * gap) / n
    text(s, 48 + 4, y0, 2 * cell + gap - 8, cell, "Happy World Teachers' Day", 34 if n == 5 else 40, GREEN, HEAD, True,
         anchor="m", spacing=1.0)
    for i, m in enumerate(people):
        c = i + 2; x = 48 + (c % n) * (cell + gap); y = y0 + (c // n) * (cell + gap)
        portrait(s, m[5], m[6], x, y, cell, cell)
        rect(s, x, y + cell - 36, cell, 36, CREAM, alpha=88)
        last = m[1].split()[-1] if m[0] == "Carla" else m[1]
        text(s, x + 4, y + cell - 36, cell - 8, 36, f"{m[0]} {last}", 12 if n == 5 else 15, GREEN, HEAD, True,
             align="c", anchor="m")


def option1():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-1-photo")
    s = d.slide(CREAM, "Option 1, slide 1: mentors' workshop group photo (assets/mentors-teachers-day/group-mentors-workshop.jpg)."
                + NOTE, counter=False)
    s.shapes.add_picture(crop(GROUP, 1080, 780, 0.5, 0.55), 0, 0, Emu(W * PX), Emu(780 * PX))
    text(s, M, 820, W - 2 * M, 40, "OCTOBER 5", 22, GREEN, HEAD, True, track=4)
    text(s, M, 865, W - 2 * M, 200, "Happy World Teachers' Day", 60, GREEN, HEAD, True, spacing=1.0)
    text(s, M, 1080, W - 2 * M - 150, 100, "Thank you to the mentors who teach our students to see soil.", 28, BLACK, BODY, spacing=1.15)
    logo(s, W - M - 100, H - 70 - 100 * 668 / 743, 100, white=False)
    s = d.slide(CREAM, "Option 1, slide 2: all fourteen mentors." + NOTE, counter=False)
    text(s, M, 120, W - 2 * M, 40, "OUR MENTORS", 22, GREEN, HEAD, True, track=4)
    faces(s, 230)
    text(s, M, H - 70, 400, 30, "soilfoodweb.com", 18, GREEN, HEAD, True)
    save(d, "05-10-2026-mon-ig-teachers-day-option-1-photo.pptx")


def option2():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-2-bunting")
    s = d.slide(CREAM, "Option 2, slide 1: drawn bunting and confetti (PowerPoint shapes)." + NOTE, counter=False)
    party(s, "Happy World Teachers' Day", "Thank you to the mentors who teach our students to see soil.",
          "Swipe to meet all fourteen →")
    s = d.slide(CREAM, "Option 2, slide 2: all fourteen mentors." + NOTE, counter=False)
    bunting(s, y=20, n=11)
    faces(s, 230)
    text(s, M, H - 60, 400, 30, "soilfoodweb.com", 18, GREEN, HEAD, True)
    save(d, "05-10-2026-mon-ig-teachers-day-option-2-bunting.pptx")


def option3():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-3-wreath")
    s = d.slide(CREAM, "Option 3, slide 1: title above a 4 x 4 grid of the fourteen mentors." + NOTE, counter=False)
    text(s, 48, 60, W - 96, 40, "OCTOBER 5", 22, GREEN, HEAD, True, track=4)
    text(s, 48, 105, W - 96, 120, "Happy World Teachers' Day", 48, GREEN, HEAD, True, spacing=1.0)
    faces(s, 230)
    s = d.slide(CREAM, "Option 3, slide 2: every mentor by name and role.", counter=False)
    text(s, M, 110, W - 2 * M, 200, "Thank you to every mentor on our team.", 52, GREEN, HEAD, True, spacing=1.05)
    rect(s, M, 300, 120, 4, TAN)
    for i, m in enumerate(MENTORS):
        x = M + (i // 7) * 470; y = 350 + (i % 7) * 110
        text(s, x, y, 450, 40, f"{m[0]} {m[1]}", 26, BLACK, HEAD, True)
        text(s, x, y + 40, 450, 34, m[2].replace("AP ", "Advanced Programs "), 18, GREEN, BODY)
    logo(s, W - M - 100, H - 60 - 100 * 668 / 743, 100, white=False)
    save(d, "05-10-2026-mon-ig-teachers-day-option-3-wreath.pptx")


from build_teachers_day_v2 import para


def mentor_text(s, m, x, y, w, maxh, big=False):
    """Name and role only, from the team page, the same for every mentor (no drafted quotes or fun facts)."""
    name = f"{'Dr. ' if m[0] in DR else ''}{m[0]} {m[1]}"
    yy = para(s, x, y, w, name, (40, 36, 32) if big else (26, 23, 21), GREEN, HEAD, True, sp=1.0) + (12 if big else 2)
    para(s, x, yy, w, m[2], (26,) if big else (16,), BLACK, BODY)


def option4():
    """10 slides, every mentor treated the same: bunting cover, seven slides with two mentors each (same layout, same
    size, alphabetical by surname so nobody comes first), the grid of all fourteen, and a plain closing slide."""
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-4-ten-slides")
    s = d.slide(CREAM, "Slide 1: bunting, balloons and stars (PowerPoint shapes), big logo." + NOTE, counter=False)
    party(s, "Happy World Teachers' Day", "Meet our fourteen mentors.", "Swipe →")
    abc = sorted(MENTORS, key=lambda m: unicodedata.normalize("NFD", m[1].split()[-1] if m[0] == "Carla" else m[1]))
    for k in range(0, len(abc), 2):
        group = abc[k:k + 2]
        s = d.slide(CREAM, "Mentors: " + ", ".join(f"{m[0]} {m[1]}" for m in group) + ". About lines: drafts from the "
                    "team notes; confirm with each mentor (05-10-2026-mon-ig-teachers-day-mentors.md)." + NOTE, counter=False)
        bunting(s, y=20, n=11)
        cell, top, rowh = 520, 180, 565
        for i, m in enumerate(group):
            y = top + i * rowh
            portrait(s, m[5], m[6], 60, y, cell, cell)
            mentor_text(s, m, 60 + cell + 36, y + cell / 2 - 90, W - 60 - (60 + cell + 36), y + cell, big=True)
    s = d.slide(CREAM, "All fourteen in a grid, alphabetical." + NOTE, counter=False)
    bunting(s, y=20, n=11)
    faces(s, 185, people=abc, with_logo=True)
    s = d.slide(CREAM, "Closing: bunting, balloons and a big logo. Line to confirm with Linnea.", counter=False)
    party(s, "Happy World Teachers' Day", "", "soilfoodweb.com")
    save(d, "05-10-2026-mon-ig-teachers-day-option-4-ten-slides.pptx")


if __name__ == "__main__":
    option1(); option2(); option3(); option4()
