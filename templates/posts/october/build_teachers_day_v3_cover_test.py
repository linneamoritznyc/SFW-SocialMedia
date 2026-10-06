"""World Teachers' Day v3: one test cover with Replicate cut-paper art (6 Oct 2026, Linnea: "make only 1 slide").
The soil strip (assets/collage/cutouts/soil-strip-seedlings.png) was made with tools/slide_art_generate.py.

python3 templates/posts/october/build_teachers_day_v3_cover_test.py
"""
from lib import Deck, text
from build_oct_01_10 import logo, pic, save
from build_teachers_day_options import balloon, star
from build_teachers_day_v3 import base, bunting, GREEN, GOLD, LEAF, BROWN, INK, W, H, M, NOTE

STRIP = "assets/collage/cutouts/soil-strip-seedlings.png"     # 2048 x 809
d = Deck(name="05-10-2026-mon-ig-teachers-day-v3-cover-test")
s = base(d, "Test cover: cut-paper soil strip made with Replicate (flux-2-pro, style-reference.png)." + NOTE)
bunting(s, y=40, n=9)
star(s, 330, 248, 34, GOLD); star(s, W - 330, 248, 34, GOLD)
text(s, M, 225, W - 2 * M, 50, "OCTOBER 5", 26, GREEN, HEAD := "Montserrat", True, track=4, align="c")
text(s, M, 285, W - 2 * M, 240, "Happy World Teachers' Day", 76, GREEN, "Montserrat", True, spacing=1.0, align="c")
text(s, (W - 680) / 2, 545, 680, 90, "Thank you to our instructors and education staff.", 30, INK, "Source Sans 3",
     spacing=1.15, align="c")
sh = 1080 * 809 / 2048; top = H - sh + 10
for side in (-1, 1):                       # balloons tied into the soil
    bx = 150 if side < 0 else W - 150
    for dx, t, w, c in [(-40, 640, 125, GREEN), (45, 590, 135, GOLD), (0, 720, 115, LEAF)]:
        balloon(s, bx + side * dx, t, w, c, top + 60)
logo(s, (W - 260) / 2, 660, 260, white=False)
text(s, M, 905, W - 2 * M, 40, "Swipe →", 24, BROWN, "Montserrat", True, align="c")
pic(s, STRIP, 0, top, W)
save(d, "05-10-2026-mon-ig-teachers-day-v3-cover-test.pptx")
