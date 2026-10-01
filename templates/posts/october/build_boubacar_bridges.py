"""Boubacar seamless carousel, "Bridges": no colour fades.
Flat cream canvas; big hard-edged brand-colour shapes and photos sit ON the seams, half on one slide and half on the
next, so each swipe completes the image you just saw half of. One continuous brown hyphae line runs the whole length.
Text in black straight on the cream, same position on every slide. Brand colours and fonts only.
References: plannthat.com/seamless-instagram-carousel-guide, pstr.app/seamless-carousel (place elements across seams).

python3 build_boubacar_bridges.py  ->  01-10-2026-thu-ig-soil-regenerators-boubacar-bridges.pptx
"""
import math, os, random
from PIL import Image, ImageDraw, ImageFilter
from pptx.util import Emu
from lib import Deck, rect, text, crop, ROOT, PX
from build_oct_01_10 import logo, save
from build_boubacar import B, SOURCES
from build_boubacar_panorama import nlines, lh, HEADF, BODYF, VOICE

N, SW, SH = 11, 1080, 1350
CREAM, GREEN, BROWN, TAN, SAGE, BLACK = "F3F1EA", "31662F", "4C3634", "C09D7F", "B1BCB1", "111111"
RGB = lambda h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
BG_DIR = os.path.join(ROOT, "assets/collage/boubacar-bridges")
MAIN = (190, 110, 480, 640)          # x, y, w, h of the main photo, same on every slide
BRIDGE = (180, 400, 330)             # half-width on each side of the seam, height, top y
TEXT = (80, 830, 920, 380)           # text block, same on every slide


def background():
    """Flat shapes on the seams + one continuous hyphae line. Saved as one panorama and 11 slices."""
    W = N * SW; random.seed(5)
    im = Image.new("RGB", (W, SH), RGB(CREAM)); d = ImageDraw.Draw(im)
    cols = [GREEN, TAN, SAGE]
    for i in range(1, N):                                    # one big flat shape centred on each seam, behind the bridge photo
        cx = i * SW; c = RGB(cols[(i - 1) % 3]); r = 300
        d.ellipse([cx - r, 230 - r * 0.15, cx + r, 230 + r * 1.75], fill=c)
    line = Image.new("RGBA", (W, SH), (0, 0, 0, 0)); L = ImageDraw.Draw(line)
    col = RGB(BROWN) + (255,)

    def seg(x, y, nx, ny, w):
        L.line([(x, y), (nx, ny)], fill=col, width=max(1, int(w))); r = w / 2; L.ellipse([nx - r, ny - r, nx + r, ny + r], fill=col)

    def twig(x, y, a, w, depth):
        if depth == 0 or w < 1.2: return
        for _ in range(random.randint(3, 6)):
            a += random.uniform(-0.3, 0.3); s = random.uniform(10, 18); nx, ny = x + math.cos(a) * s, y + math.sin(a) * s
            if 800 < ny < 1300 and not (60 < (nx % SW) < 1020): return      # never into the text area
            seg(x, y, nx, ny, w); x, y = nx, ny; w *= 0.93
        for _ in range(2): twig(x, y, a + random.uniform(-0.9, 0.9), w * 0.65, depth - 1)

    x, y = 0, 790
    while x < W:                                             # the main thread, between photos and text on every slide
        nx = x + 14; ny = 790 + 16 * math.sin(nx / 210) + 7 * math.sin(nx / 67)
        seg(x, y, nx, ny, 9); x, y = nx, ny
        if random.random() < 0.035:
            twig(x, y, -math.pi / 2 + random.uniform(-0.8, 0.8), 5, 4)
    im = im.convert("RGBA"); im.alpha_composite(line.filter(ImageFilter.GaussianBlur(0.7))); im = im.convert("RGB")
    os.makedirs(BG_DIR, exist_ok=True); im.save(os.path.join(BG_DIR, "panorama-full.jpg"), quality=90)
    for i in range(N):
        im.crop((i * SW, 0, (i + 1) * SW, SH)).save(os.path.join(BG_DIR, f"slide-{i + 1:02d}.jpg"), quality=92)


def place(s, path, x, y, w, h):
    s.shapes.add_picture(path, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def framed(s, rel, x, y, w, h, fx=0.5, fy=0.5):
    rect(s, x - 10, y - 10, w + 20, h + 20, "FFFFFF", shadow=True)
    place(s, crop(rel, int(w), int(h), fx, fy), x, y, w, h)


def bridge_halves(rel, fx=0.5, fy=0.5):
    """Crop a photo to the bridge size and split it at the seam. Returns (left half path, right half path)."""
    hw, h, _ = BRIDGE
    full = Image.open(crop(rel, 2 * hw, h, fx, fy))
    base = os.path.join(BG_DIR, "tmp-" + os.path.basename(rel).rsplit(".", 1)[0])
    full.crop((0, 0, hw, h)).save(base + "-L.jpg", quality=92); full.crop((hw, 0, 2 * hw, h)).save(base + "-R.jpg", quality=92)
    return base + "-L.jpg", base + "-R.jpg"


def words(s, body, head=None, voice=False):
    x, y0, w, hmax = TEXT
    bfont = VOICE if voice else BODYF
    for hpt, bpt in ((52, 52), (50, 48), (48, 46), (46, 42), (44, 40), (42, 38), (40, 36), (38, 34), (36, 32)):
        hh = nlines(head, hpt, w * 0.96, HEADF) * lh(hpt, 1.05) + 16 if head else 0
        bh = nlines(body, bpt, w * 0.96, bfont) * lh(bpt, 1.15)
        if hh + bh <= hmax: break
    y = y0
    if head:
        text(s, x, y, w, hh, head, hpt, BLACK, HEADF, True, spacing=1.05); y += hh
    text(s, x, y, w, bh + 10, body, bpt, BLACK, bfont, False, italic=voice, spacing=1.15)


def footer(s, t="soilfoodweb.com"):
    text(s, 0, SH - 80, SW, 44, t, 22, BROWN, HEADF, True, align="c", anchor="m")


SLIDES = [
    # main photo, focus, heading, body, voice, bridge photo to the NEXT slide, its focus
    ("boubacar-portrait-bananas-closer.jpg", (0.5, 0.35), "Boubacar Tidiane Diallo",
     "Guinea-Conakry\nGraduated from the Soil Food Web School in July 2026", False, "young-tree-with-pineapples.jpg", (0.5, 0.55)),
    ("farm-overview-with-tanks.jpeg", (0.5, 0.5), "When he started, the land was worn out.",
     "The soil at Gnaly Coffee & AgroÉcole Bio, in the Fouta Djallon highlands of Guinea-Conakry, had been degraded and poorly "
     "managed for years.", False, "man-by-water-tanks.jpeg", (0.4, 0.5)),
    ("vegetable-beds-by-building.jpeg", (0.6, 0.25), "So he changed the question:",
     "“Today, I ask a different question: What does the soil food web need to thrive?”", True, "still-biochar-kiln-smoke-73s.png", (0.5, 0.4)),
    ("boubacar-compost-pile.jpeg", (0.5, 0.45), "How he feeds his soil:",
     "living groundcover, mulch from his farm and the forest, and compost with biochar activated with fish hydrolysate and compost tea.",
     False, "still-biochar-charcoal-16s.png", (0.5, 0.5)),
    ("carrying-mulch.jpg", (0.5, 0.5), None, "“I apply compost regularly around young trees and whenever I add new mulch.”", True,
     "banana-bunch.jpg", (0.5, 0.4)),
    ("planting-seedling-in-agroforest.jpeg", (0.45, 0.45), "What he grows together:", "coffee, cacao, bananas, citrus, and pineapple.",
     False, "barrel-brew-under-shelter.jpeg", (0.5, 0.35)),
    ("buckets-of-tubers.jpg", (0.5, 0.5), None,
     "“My compost includes plant residues, animal manure when available, biochar activated with fish hydrolysate and compost tea, "
     "and local organic materials.”", True, "boubacar-hand-compost-worm.jpg", (0.4, 0.5)),
    ("millipede-leaf-litter.jpg", (0.5, 0.35), "What he's seeing:",
     "more earthworms, more mushrooms, active decomposition, and better soil structure.", False, "caterpillar-on-leaf.jpg", (0.5, 0.35)),
    ("yellow-caterpillar-on-stem.jpg", (0.35, 0.4), None,
     "“I can already see signs of healthier soil in the field, including more earthworms, mushrooms, and active decomposition.”",
     True, "two-men-at-shade-house.jpeg", (0.5, 0.35)),
    ("group-of-five-farmers.jpeg", (0.42, 0.5), None,
     "“Your training changed the way I see agriculture. I now believe that agriculture is biology, not chemical fertilizer.”", True,
     "young-tree-yellow-new-leaves.jpg", (0.5, 0.45)),
    ("young-coffee-plant.jpg", (0.5, 0.5), None,
     "“My dream is to restore degraded land in the Fouta Djallon and help my community learn living-soil practices.”", True, None, None),
]


def build():
    background()
    d = Deck(name="01-10-2026-thu-ig-soil-regenerators-boubacar-bridges")
    hw, bh, by = BRIDGE
    halves = [bridge_halves(B + sl[5], *sl[6]) if sl[5] else None for sl in SLIDES]
    for i, (photo, focus, head, body, voice, bphoto, _) in enumerate(SLIDES, 1):
        note = ("Bridges seamless carousel (no fades): photos straddle the seams. Background assets/collage/boubacar-bridges/ (drawn by "
                f"code, brand colours). Main photo: {photo}." + (f" Bridge to next slide: {bphoto}." if bphoto else "")
                + (" " + SOURCES if i == 1 else "") + (" His words from his email to Allison, 30 Sep 2026." if voice else ""))
        s = d.slide(None, note, counter=False)
        place(s, os.path.join(BG_DIR, f"slide-{i:02d}.jpg"), 0, 0, SW, SH)
        if i > 1 and halves[i - 2]:                  # right half of the previous bridge, at this slide's left edge
            rect(s, -10, by - 10, hw + 10, bh + 20, "FFFFFF", shadow=True)
            place(s, halves[i - 2][1], 0, by, hw, bh)
        if halves[i - 1]:                            # left half of the next bridge, at this slide's right edge
            rect(s, SW - hw, by - 10, hw + 10, bh + 20, "FFFFFF", shadow=True)
            place(s, halves[i - 1][0], SW - hw, by, hw, bh)
        x, y, w, h = MAIN
        framed(s, B + photo, x, y, w, h, *focus)
        words(s, body, head, voice)
        if i == 1:
            logo(s, SW - 40 - 150, 25, 150, white=False)
            text(s, 80, 40, 700, 50, "HAPPY INTERNATIONAL COFFEE DAY", 22, GREEN, HEADF, True, track=3)
        elif i == N:
            logo(s, SW - 40 - 150, 25, 150, white=False)
            footer(s, "Subscribe on YouTube: @boubacartidianediallo")
        else:
            footer(s)
    save(d, "01-10-2026-thu-ig-soil-regenerators-boubacar-bridges.pptx")


if __name__ == "__main__":
    build()
