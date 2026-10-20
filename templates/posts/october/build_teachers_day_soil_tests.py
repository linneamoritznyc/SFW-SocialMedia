"""World Teachers' Day: four versions of one two-person slide (Loida and Casey), Stephanie's Canva layout, each with a
different soil treatment. Soil never goes over the staff photos.

A  real compost mound bottom right (cut from assets/photo/hand-of-compost.jpg), logo bottom left
B  soil and seedlings flat-lay border along the bottom (Replicate, flux-2-pro, cut out)
C  torn strip of real soil across the bottom, like a pasted paper strip
D  soil crumbs drifting down the top-right corner and a small mound bottom left (both cut from the compost photo)

python3 templates/posts/october/build_teachers_day_soil_tests.py
"""
import random
from PIL import Image, ImageDraw, ImageFilter
from lib import Deck
from build_oct_01_10 import logo, pic, save
from build_teachers_day_v2 import portrait, para
from build_teachers_day_v3 import base, bunting, PEOPLE, GREEN, INK, W, H, NOTE

LOIDA = next(m for m in PEOPLE if m[0] == "Loida")
CASEY = next(m for m in PEOPLE if m[0] == "Casey")
PAIR = [LOIDA[:2] + ("Advanced Programs Lead & Mentor",) + LOIDA[3:], CASEY]   # Loida's title as in Stephanie's Canva
TX = "assets/texture/"


def torn_strip(path, w=1080, h=230, seed=4):
    """Real compost cut into a strip with a torn top edge."""
    random.seed(seed)
    src = Image.open("assets/photo/hand-of-compost.jpg").convert("RGB").crop((0, 0, 1800, 560))
    k = max(h / src.height, w / src.width); t = src.resize((int(src.width * k) + 1, int(src.height * k) + 1)).crop((0, 0, w, h))
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    y = 60; pts = [(0, h)]
    for x in range(0, w + 8, 8):
        y = max(25, min(95, y + random.uniform(-9, 9))); pts.append((x, y))
    pts.append((w, h)); d.polygon(pts, fill=255)
    m = m.filter(ImageFilter.GaussianBlur(1.2))
    out = t.convert("RGBA"); out.putalpha(m); out.save(path, optimize=True)


def crumbs(path, w=420, h=520, seed=9):
    """Crumbs of real compost drifting from the top-right corner: denser at the corner, thinning out."""
    random.seed(seed)
    src = Image.open("assets/photo/hand-of-compost.jpg").convert("RGB").crop((0, 0, 1800, 560)).resize((w, int(w * 560 / 1800)))
    tex = Image.new("RGB", (w, h)); y = 0
    while y < h: tex.paste(src, (0, y)); y += src.height
    m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    for _ in range(520):
        x = w - abs(random.gauss(0, w * 0.35)); yy = abs(random.gauss(0, h * 0.35))
        if not (0 <= x < w and 0 <= yy < h): continue
        r = random.uniform(1.5, 7) * (1 - 0.6 * ((w - x) / w + yy / h) / 2)
        d.ellipse([x - r, yy - r * random.uniform(.6, 1), x + r, yy + r], fill=255)
    out = tex.convert("RGBA"); out.putalpha(m.filter(ImageFilter.GaussianBlur(.5))); out.save(path, optimize=True)


def people(s):
    cell, top = 470, 190
    for i, m in enumerate(PAIR):
        y = top + i * (cell + 40)
        portrait(s, m[5], m[6], 80, y, cell, cell)
        yy = para(s, 595, y + cell / 2 - 70, 420, f"{m[0]} {m[1]}", (44, 40, 36), GREEN, "Montserrat", True, sp=1.0, maxh=130) + 12
        para(s, 595, yy, 420, m[2], (26, 24), INK, "Source Sans 3", maxh=120)


def build():
    torn_strip(TX + "soil-torn-strip.png"); crumbs(TX + "soil-crumbs-corner.png")
    d = Deck(name="05-10-2026-mon-ig-teachers-day-soil-tests")
    for key, note in [("A", "compost mound bottom right"), ("B", "flat-lay soil border (Replicate)"),
                      ("C", "torn soil strip"), ("D", "crumbs top right, small mound bottom left")]:
        s = base(d, f"Version {key}: {note}." + NOTE)
        bunting(s)
        if key == "A":
            pic(s, TX + "soil-corner-b.png", W - 560, H - 560 * 260 / 520, 560).rotation = 0
            sh = s.shapes[-1]; sh._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm").set("flipH", "1")
            people(s); logo(s, 80, H - 150, 120, white=False)
        elif key == "B":
            people(s)
            bw = 1080; bh = bw * 989 / 2048                     # soil starts about 40% down the cut-out
            pic(s, "assets/collage/cutouts/soil-flatlay-border.png", 0, 1185 - 0.40 * bh, bw)
            logo(s, W - 40 - 120, 1040, 120, white=False)
        elif key == "C":
            people(s)
            pic(s, TX + "soil-torn-strip.png", 0, H - 150, W, 150 * 1.0 * 230 / 230)
            logo(s, W - 40 - 125, H - 150 - 120, 125, white=False)
        else:
            pic(s, TX + "soil-crumbs-corner.png", W - 420, 0, 420)
            people(s)
            pic(s, TX + "soil-corner-a.png", 0, H - 380 * 300 / 640, 380)
            logo(s, W - 40 - 120, H - 150, 120, white=False)
    save(d, "05-10-2026-mon-ig-teachers-day-soil-tests.pptx")


if __name__ == "__main__":
    build()
