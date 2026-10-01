"""Boubacar seamless carousel, "Photo strip" (after the Will Khoury reference in 'inspiration carousel slides instagram/').
Top: one continuous strip of Boubacar's photos, full bleed, darkened with a flat Deep Green tint (no gradients), with the
strip's photo edges offset from the slide edges. On top: white-framed photos, one per slide plus one straddling every seam.
Bottom: one continuous cream band with black text in the same place on every slide. Brand colours and fonts only.

python3 build_boubacar_strip.py  ->  01-10-2026-thu-ig-soil-regenerators-boubacar-strip.pptx
"""
import os
from PIL import Image, ImageFilter, ImageOps
from pptx.util import Emu
from lib import Deck, rect, text, crop, ROOT, PX
from build_oct_01_10 import logo, save
from build_boubacar import B, SOURCES
from build_boubacar_panorama import nlines, lh, HEADF, BODYF, VOICE

N, SW, SH = 11, 1080, 1350
STRIP_H = 860                       # photo strip y 0..860, cream band 860..1350
DEEP, CREAM, GREEN, BLACK, BROWN = (0x22, 0x37, 0x1F), "F3F1EA", "31662F", "111111", "4C3634"
OUT_DIR = os.path.join(ROOT, "assets/collage/boubacar-strip")
MAIN = (90, 90, 470, 640)           # framed main photo: x, y, w, h (same on every slide)
SEAM = (330, 420, 330)              # seam photo: width, height, top y (centred on the seam)
TEXT = (80, 905, 920, 330)          # text block in the cream band

BACKDROP = [  # only the large originals (1536 x 2048 or more), so the strip stays sharp
    "agroforestry-understory.jpg", "young-tree-with-pineapples.jpg", "banana-bunch.jpg", "boubacar-portrait-bananas.jpg",
    "young-tree-yellow-new-leaves.jpg", "buckets-of-tubers.jpg", "young-coffee-plant.jpg", "millipede-leaf-litter.jpg",
    "agroforestry-understory.jpg", "yellow-caterpillar-on-stem.jpg", "young-tree-with-pineapples.jpg", "young-coffee-plant.jpg"]


def strip():
    """12 backdrop panels, each one slide wide but offset half a slide, so photo edges never sit on a slide edge."""
    W = N * SW
    im = Image.new("RGB", (W, SH), tuple(int(CREAM[i:i + 2], 16) for i in (0, 2, 4)))
    for k, name in enumerate(BACKDROP):
        x0 = -SW // 2 + k * SW
        p = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, B + name))).convert("RGB")
        p = ImageOps.fit(p, (SW, STRIP_H), Image.LANCZOS, centering=(0.5, 0.5))
        p = Image.blend(p, Image.new("RGB", p.size, DEEP), 0.62)          # flat tint, the same everywhere
        im.paste(p, (x0, 0))
    os.makedirs(OUT_DIR, exist_ok=True); im.save(os.path.join(OUT_DIR, "panorama-full.jpg"), quality=90)
    for i in range(N):
        im.crop((i * SW, 0, (i + 1) * SW, SH)).save(os.path.join(OUT_DIR, f"slide-{i + 1:02d}.jpg"), quality=92)


def place(s, path, x, y, w, h):
    s.shapes.add_picture(path, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def framed(s, rel, x, y, w, h, fx=0.5, fy=0.5):
    rect(s, x - 8, y - 8, w + 16, h + 16, "FFFFFF", shadow=True)
    place(s, crop(rel, int(w), int(h), fx, fy), x, y, w, h)


def seam_halves(rel, fx, fy):
    w, h, _ = SEAM
    full = Image.open(crop(rel, w, h, fx, fy)); base = os.path.join(OUT_DIR, "tmp-" + os.path.basename(rel).rsplit(".", 1)[0])
    full.crop((0, 0, w // 2, h)).save(base + "-L.jpg", quality=92); full.crop((w // 2, 0, w, h)).save(base + "-R.jpg", quality=92)
    return base + "-L.jpg", base + "-R.jpg"


def words(s, body, head=None, voice=False):
    x, y0, w, hmax = TEXT
    bfont = VOICE if voice else BODYF
    for hpt, bpt in ((48, 46), (46, 42), (44, 40), (42, 38), (40, 36), (38, 34), (36, 32), (34, 30)):
        hh = nlines(head, hpt, w * 0.96, HEADF) * lh(hpt, 1.05) + 14 if head else 0
        bh = nlines(body, bpt, w * 0.96, bfont) * lh(bpt, 1.15)
        if hh + bh <= hmax: break
    y = y0
    if head:
        text(s, x, y, w, hh, head, hpt, BLACK, HEADF, True, spacing=1.05); y += hh
    text(s, x, y, w, bh + 10, body, bpt, BLACK, bfont, False, italic=voice, spacing=1.15)


SLIDES = [  # main photo, focus, heading, body, voice, seam photo to the NEXT slide, focus
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
    strip()
    d = Deck(name="01-10-2026-thu-ig-soil-regenerators-boubacar-strip")
    sw, sh, sy = SEAM
    SPLIT = {1, 4, 7, 10}             # only these seams carry a split photo; elsewhere the second photo sits whole on its slide
    halves = [seam_halves(B + sl[5], *sl[6]) if sl[5] and i in SPLIT else None for i, sl in enumerate(SLIDES, 1)]
    for i, (photo, focus, head, body, voice, sphoto, _) in enumerate(SLIDES, 1):
        note = ("Photo-strip seamless carousel (after the Will Khoury reference). Backdrop assets/collage/boubacar-strip/ "
                f"(his photos, flat Deep Green tint). Main photo: {photo}." + (f" Seam photo to next slide: {sphoto}." if sphoto else "")
                + (" " + SOURCES if i == 1 else "") + (" His words from his email to Allison, 30 Sep 2026." if voice else ""))
        s = d.slide(None, note, counter=False)
        place(s, os.path.join(OUT_DIR, f"slide-{i:02d}.jpg"), 0, 0, SW, SH)
        if i > 1 and halves[i - 2]:
            rect(s, -8, sy - 8, sw // 2 + 8, sh + 16, "FFFFFF", shadow=True); place(s, halves[i - 2][1], 0, sy, sw // 2, sh)
        if halves[i - 1]:
            rect(s, SW - sw // 2, sy - 8, sw // 2 + 8, sh + 16, "FFFFFF", shadow=True); place(s, halves[i - 1][0], SW - sw // 2, sy, sw // 2, sh)
        framed(s, B + photo, *MAIN, *focus)
        if sphoto and i not in SPLIT and not (i == 1 or i == N):     # second photo whole, in the right column
            framed(s, B + sphoto, 640, 300 if (i - 1) not in SPLIT else 380, 350, 340, *SLIDES[i - 1][6])
        words(s, body, head, voice)
        if i == 1:
            logo(s, 615, 100, 200, white=True)
            text(s, 615, 320, 295, 160, "Happy\nInternational\nCoffee Day", 28, "F3F1EA", HEADF, True, spacing=1.1)
        elif i == N:
            logo(s, SW - 60 - 170, 120, 170, white=True)
            text(s, 0, SH - 80, SW, 44, "Subscribe on YouTube: @boubacartidianediallo", 22, BROWN, HEADF, True, align="c", anchor="m")
        else:
            text(s, 0, SH - 80, SW, 44, "soilfoodweb.com", 22, BROWN, HEADF, True, align="c", anchor="m")
    save(d, "01-10-2026-thu-ig-soil-regenerators-boubacar-strip.pptx")


if __name__ == "__main__":
    build()


def linkedin():
    """LinkedIn image (1200 x 627) in the same photo-strip style: tinted sharp backdrop, white-framed photos, cream band."""
    W, H, BAND = 1200, 627, 440
    bg = Image.new("RGB", (W, H), tuple(int(CREAM[i:i + 2], 16) for i in (0, 2, 4)))
    for k, name in enumerate(["young-tree-with-pineapples.jpg", "agroforestry-understory.jpg"]):
        p = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, B + name))).convert("RGB")
        p = ImageOps.fit(p, (W // 2 + 1, BAND), Image.LANCZOS)
        bg.paste(Image.blend(p, Image.new("RGB", p.size, DEEP), 0.62), (k * W // 2, 0))
    path = os.path.join(OUT_DIR, "linkedin-backdrop.jpg"); bg.save(path, quality=92)
    d = Deck(W, H, name="01-10-2026-thu-li-boubacar-strip")
    s = d.slide(None, "LinkedIn image, photo-strip style (matches the Instagram carousel). " + SOURCES +
                " Photos: boubacar-portrait-bananas-closer.jpg, vegetable-beds-by-building.jpeg, young-coffee-plant.jpg.", counter=False)
    place(s, path, 0, 0, W, H)
    framed(s, B + "boubacar-portrait-bananas-closer.jpg", 60, 40, 280, 370, 0.5, 0.33)
    framed(s, B + "vegetable-beds-by-building.jpeg", 375, 95, 230, 290, 0.6, 0.25)
    framed(s, B + "young-coffee-plant.jpg", 640, 60, 230, 300, 0.5, 0.5)
    logo(s, W - 50 - 170, 60, 170, white=True)
    text(s, 60, BAND + 28, 1000, 30, "HAPPY INTERNATIONAL COFFEE DAY", 18, GREEN, HEADF, True, track=3)
    text(s, 60, BAND + 48, 1080, 56, "Boubacar Tidiane Diallo", 42, BLACK, HEADF, True)
    text(s, 60, BAND + 116, 1080, 36, "Gnaly Coffee & AgroÉcole Bio, Fouta Djallon, Guinea-Conakry", 24, BLACK, BODYF, False)
    save(d, "01-10-2026-thu-li-boubacar-strip.pptx")


if __name__ == "__main__":
    linkedin()
