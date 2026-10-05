"""World Teachers' Day (5 Oct 2026): three more options, 2 slides each. No AI art and no paper-cut flowers: real
photos, drawn shapes (bunting, confetti), brand colours on cream.

1 Photo: the mentors' workshop group photo full bleed, then all fourteen faces.
2 Bunting: drawn bunting and confetti over the title with a row of faces, then all fourteen faces.
3 Grid cover: the title above the grid of all fourteen, then a thank-you slide with every name.

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


def faces(s, y0, color=GREEN, fill_cells=True):
    """All fourteen mentors as a 4 x 4 grid of square photos, name on a cream strip inside each square.
    The two spare cells hold a thank-you note and the logo, so the grid is complete."""
    n, gap = 4, 8
    cell = (W - 2 * 48 - (n - 1) * gap) / n
    for i in range(16):
        x = 48 + (i % n) * (cell + gap); y = y0 + (i // n) * (cell + gap)
        if i < len(MENTORS):
            m = MENTORS[i]
            portrait(s, m[5], m[6], x, y, cell, cell)
            rect(s, x, y + cell - 44, cell, 44, CREAM, alpha=88)
            text(s, x + 6, y + cell - 44, cell - 12, 44, f"{m[0]} {m[1]}", 15, GREEN, HEAD, True, align="c", anchor="m")
        elif i == 14 and fill_cells:
            rect(s, x, y, cell, cell, GREEN)
            text(s, x + 18, y, cell - 36, cell, "Thank you, mentors!", 24, CREAM, HEAD, True, align="c", anchor="m", spacing=1.05)
        elif i == 15 and fill_cells:
            rect(s, x, y, cell, cell, TAN)
            logo(s, x + (cell - 140) / 2, y + (cell - 140 * 668 / 743) / 2, 140, white=True)


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
    bunting(s)
    confetti(s, 26, (40, 200, W - 60, 300), 3)
    text(s, M, 330, W - 2 * M, 40, "OCTOBER 5", 24, GREEN, HEAD, True, track=4, align="c")
    text(s, M, 380, W - 2 * M, 240, "Happy World Teachers' Day", 76, GREEN, HEAD, True, spacing=1.0, align="c")
    text(s, M, 620, W - 2 * M, 100, "Thank you to the mentors who teach our students to see soil.", 30, BLACK, BODY, spacing=1.15, align="c")
    confetti(s, 30, (40, 780, W - 60, 980), 21)                 # no faces on the cover: nobody is singled out
    text(s, M, 1030, W - 2 * M, 40, "Swipe to meet all fourteen →", 22, BROWN, HEAD, True, align="c")
    logo(s, (W - 100) / 2, H - 60 - 100 * 668 / 743, 100, white=False)
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


def option4():
    """7 slides: bunting cover, four slides with four mentors each (square photos, name, role, one line), the grid of
    all fourteen, and a bunting thank-you."""
    d = Deck(name="05-10-2026-mon-ig-teachers-day-option-4-seven-slides")
    s = d.slide(CREAM, "Slide 1: bunting cover." + NOTE, counter=False)
    bunting(s); confetti(s, 26, (40, 200, W - 60, 300), 3)
    text(s, M, 330, W - 2 * M, 40, "OCTOBER 5", 24, GREEN, HEAD, True, track=4, align="c")
    text(s, M, 380, W - 2 * M, 240, "Happy World Teachers' Day", 76, GREEN, HEAD, True, spacing=1.0, align="c")
    text(s, M, 620, W - 2 * M, 100, "Meet the mentors who teach our students to see soil.", 30, BLACK, BODY, spacing=1.15, align="c")
    confetti(s, 30, (40, 780, W - 60, 980), 21)                 # no faces on the cover: nobody is singled out
    text(s, M, 1030, W - 2 * M, 40, "Swipe to meet all fourteen →", 22, BROWN, HEAD, True, align="c")
    logo(s, (W - 100) / 2, H - 60 - 100 * 668 / 743, 100, white=False)
    for k in range(0, len(MENTORS), 4):                     # four mentors per slide (2 x 2); the last slide's
        group = MENTORS[k:k + 4]                               # two spare cells hold the thank-you and the logo
        s = d.slide(CREAM, "Mentors: " + ", ".join(f"{m[0]} {m[1]}" for m in group) + ". About lines: drafts from the "
                    "team notes; confirm with each mentor (05-10-2026-mon-ig-teachers-day-mentors.md)." + NOTE, counter=False)
        bunting(s, y=20, n=11)
        cell, gx, top, rowh = 440, 48, 175, 590
        for i in range(4):
            x = gx + (i % 2) * (cell + 104); y = top + (i // 2) * rowh
            if i < len(group):
                m = group[i]
                portrait(s, m[5], m[6], x, y, cell, cell)
                yy = para(s, x, y + cell + 14, cell, f"{'Dr. ' if m[1] == 'Portugal' else ''}{m[0]} {m[1]}", (26, 23, 21),
                          GREEN, HEAD, True, sp=1.0) + 2
                yy = para(s, x, yy, cell, m[2].replace("AP ", "Advanced Programs "), (16,), BLACK, BODY) + 6
                line = f"“{m[4]}”" if m[4] else m[3]
                if line: para(s, x, yy, cell, line, (15, 14, 13), GREEN, BODY, maxh=y + rowh - 10 - yy)
            elif i == len(group):
                rect(s, x, y, cell, cell, GREEN)
                text(s, x + 30, y, cell - 60, cell, "Thank you, mentors!", 40, CREAM, HEAD, True, align="c", anchor="m", spacing=1.05)
            else:
                rect(s, x, y, cell, cell, TAN)
                logo(s, x + (cell - 220) / 2, y + (cell - 220 * 668 / 743) / 2, 220, white=True)
    s = d.slide(CREAM, "All fourteen in a grid." + NOTE, counter=False)
    bunting(s, y=20, n=11)
    faces(s, 230)
    s = d.slide(CREAM, "Thank you, with bunting and confetti.", counter=False)
    bunting(s); confetti(s, 30, (40, 200, W - 60, 320), 11)
    text(s, M, 380, W - 2 * M, 260, "Thank you to every mentor who teaches our students to see soil.", 56, GREEN, HEAD,
         True, spacing=1.05, align="c")
    text(s, M, 800, W - 2 * M, 100, "Tag a teacher who helped you see soil differently.", 30, BLACK, BODY,
         align="c")
    confetti(s, 16, (40, 900, W - 60, 1050), 13)
    logo(s, (W - 140) / 2, H - 80 - 140 * 668 / 743, 140, white=False)
    save(d, "05-10-2026-mon-ig-teachers-day-option-4-seven-slides.pptx")


if __name__ == "__main__":
    option1(); option2(); option3(); option4()
