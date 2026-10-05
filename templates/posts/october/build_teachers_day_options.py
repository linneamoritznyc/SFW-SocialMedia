"""World Teachers' Day (5 Oct 2026): three more options, 2 slides each. No AI art and no paper-cut flowers: real
photos, drawn shapes (bunting, confetti), brand colours on cream.

1 Photo: the mentors' workshop group photo full bleed, then all fourteen faces.
2 Bunting: drawn bunting and confetti over the title with a row of faces, then all fourteen faces.
3 Wreath: the fourteen faces in a ring around the title, then a thank-you slide with every name.

python3 templates/posts/october/build_teachers_day_options.py
"""
import math, random
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE
from pptx.dml.color import RGBColor
from lib import Deck, rect, poly, text, crop, PX, HEAD, BODY
from build_oct_01_10 import logo, save
from build_teachers_day_v2 import MENTORS, portrait, GARA

GREEN, CREAM, BROWN, TAN, SAGE, GOLD, BLACK = "31662F", "F3F1EA", "4C3634", "C09D7F", "B1BCB1", "D39C48", "1A1A1A"
W, H, M = 1080, 1350, 80
GROUP = "assets/mentors-teachers-day/group-mentors-workshop.jpg"
NOTE = (" Mentor photos: Linnea's Drive folder (5 Oct 2026) and assets/mentors-teachers-day/; written consent per the "
        "folder README.")


def dot(s, x, y, d, color):
    sh = s.shapes.add_shape(MSO_SHAPE.OVAL, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(d * PX)), Emu(int(d * PX)))
    sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(color); sh.line.fill.background(); sh.shadow.inherit = False


def bunting(s, y=40, n=9):
    """String across the top with triangle flags in brand colours (drawn shapes, editable)."""
    cols = [GREEN, TAN, SAGE, BROWN, GOLD]
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
            random.choice([GREEN, TAN, SAGE, BROWN, GOLD]))


def faces(s, y0, cols=4, d=196, gap=45, color=GREEN):
    for i, m in enumerate(MENTORS):
        row = i // cols; n_in = min(cols, len(MENTORS) - row * cols)
        x0 = (W - (n_in * d + (n_in - 1) * gap)) / 2
        x = x0 + (i % cols) * (d + gap); y = y0 + row * (d + 94)
        portrait(s, m[5], m[6], x, y, d, d, round_=True)
        text(s, x - 24, y + d + 8, d + 48, 30, f"{m[0]} {m[1]}", 17, color, HEAD, True, align="c")


def option1():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-1-photo")
    s = d.slide(CREAM, "Option 1, slide 1: mentors' workshop group photo (assets/mentors-teachers-day/group-mentors-workshop.jpg)."
                + NOTE, counter=False)
    s.shapes.add_picture(crop(GROUP, 1080, 780, 0.5, 0.55), 0, 0, Emu(W * PX), Emu(780 * PX))
    text(s, M, 820, W - 2 * M, 40, "OCTOBER 5", 22, GREEN, HEAD, True, track=4)
    text(s, M, 865, W - 2 * M, 200, "Happy World Teachers' Day", 60, GREEN, HEAD, True, spacing=1.0)
    text(s, M, 1080, W - 2 * M - 150, 100, "Thank you to the mentors who teach our students to see soil.", 28, BLACK, GARA,
         italic=True, spacing=1.15)
    logo(s, W - M - 100, H - 70 - 100 * 668 / 743, 100, white=False)
    s = d.slide(CREAM, "Option 1, slide 2: all fourteen mentors." + NOTE, counter=False)
    text(s, M, 70, W - 2 * M, 40, "OUR MENTORS", 22, GREEN, HEAD, True, track=4)
    faces(s, 140)
    text(s, M, H - 70, 400, 30, "soilfoodweb.com", 18, GREEN, HEAD, True)
    save(d, "05-10-2026-mon-ig-teachers-day-option-1-photo.pptx")


def option2():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-2-bunting")
    s = d.slide(CREAM, "Option 2, slide 1: drawn bunting and confetti (PowerPoint shapes), five mentor faces." + NOTE, counter=False)
    bunting(s)
    confetti(s, 26, (40, 200, W - 60, 300), 3)
    text(s, M, 330, W - 2 * M, 40, "OCTOBER 5", 24, GREEN, HEAD, True, track=4, align="c")
    text(s, M, 380, W - 2 * M, 240, "Happy World Teachers' Day", 76, GREEN, HEAD, True, spacing=1.0, align="c")
    text(s, M, 620, W - 2 * M, 100, "Thank you to the mentors who teach our students to see soil.", 30, BLACK, GARA,
         italic=True, spacing=1.15, align="c")
    pick = [MENTORS[i] for i in (2, 4, 9, 6, 12)]
    d_ = 170; gap = 20; x0 = (W - (5 * d_ + 4 * gap)) / 2
    for i, m in enumerate(pick):
        portrait(s, m[5], m[6], x0 + i * (d_ + gap), 820, d_, d_, round_=True)
    text(s, M, 1030, W - 2 * M, 40, "Swipe to meet all fourteen →", 22, BROWN, HEAD, True, align="c")
    confetti(s, 14, (40, 1090, W - 60, 1180), 9)
    logo(s, (W - 100) / 2, H - 60 - 100 * 668 / 743, 100, white=False)
    s = d.slide(CREAM, "Option 2, slide 2: all fourteen mentors." + NOTE, counter=False)
    bunting(s, y=20, n=11)
    faces(s, 190, d=186)
    text(s, M, H - 60, 400, 30, "soilfoodweb.com", 18, GREEN, HEAD, True)
    save(d, "05-10-2026-mon-ig-teachers-day-option-2-bunting.pptx")


def option3():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-3-wreath")
    s = d.slide(CREAM, "Option 3, slide 1: the fourteen mentors in a ring around the title." + NOTE, counter=False)
    cx, cy, r, dd = W / 2, 660, 400, 150
    for i, m in enumerate(MENTORS):
        a = -math.pi / 2 + 2 * math.pi * i / len(MENTORS)
        portrait(s, m[5], m[6], cx + r * math.cos(a) - dd / 2, cy + r * math.sin(a) - dd / 2, dd, dd, round_=True)
    text(s, cx - 260, cy - 150, 520, 40, "OCTOBER 5", 22, GREEN, HEAD, True, track=4, align="c")
    text(s, cx - 260, cy - 100, 520, 200, "Happy World Teachers' Day", 50, GREEN, HEAD, True, spacing=1.0, align="c")
    text(s, cx - 230, cy + 90, 460, 90, "To the mentors who teach our students to see soil.", 22, BLACK, GARA,
         italic=True, spacing=1.15, align="c")
    logo(s, (W - 100) / 2, H - 60 - 100 * 668 / 743, 100, white=False)
    s = d.slide(CREAM, "Option 3, slide 2: every mentor by name and role.", counter=False)
    text(s, M, 110, W - 2 * M, 200, "Thank you to every mentor on our team.", 52, GREEN, HEAD, True, spacing=1.05)
    rect(s, M, 300, 120, 4, TAN)
    for i, m in enumerate(MENTORS):
        x = M + (i // 7) * 470; y = 350 + (i % 7) * 110
        text(s, x, y, 450, 40, f"{m[0]} {m[1]}", 26, BLACK, HEAD, True)
        text(s, x, y + 40, 450, 34, m[2].replace("AP ", "Advanced Programs "), 18, GREEN, BODY)
    logo(s, W - M - 100, H - 60 - 100 * 668 / 743, 100, white=False)
    save(d, "05-10-2026-mon-ig-teachers-day-option-3-wreath.pptx")


if __name__ == "__main__":
    option1(); option2(); option3()
