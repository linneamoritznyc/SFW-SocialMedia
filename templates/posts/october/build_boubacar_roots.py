"""Boubacar carousel, second style: the 'root network' look of the LinkedIn option E card.
Alternating gold, green and brown grounds with a pale root network, arch-framed photos, Roboto headlines,
Times New Roman in cream bands, no stickers. Same 11 slides and words as the scrapbook version.

python3 build_boubacar_roots.py  ->  01-10-2026-thu-ig-soil-regenerators-boubacar-roots.pptx
"""
import os
from PIL import ImageFont
from lxml import etree
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE
from lib import Deck, rect, rrect, text, crop, ROOT, PX
from build_oct_01_10 import logo, save
from build_boubacar import B, SOURCES

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
W, H = 1080, 1350
SANS, SERIF = "Montserrat", "EB Garamond"   # starred brand fonts in Canva
THEMES = {  # ground, roots, headline, accent (eyebrow + rule), band, band text, logo white?
    "gold": ("D9A13E", "root-network-gold-portrait.png", "1E1412", "1E1412", "F6E3C2", "1E1412", False),
    "green": ("31662F", "root-network-green-portrait.png", "F4F1EA", "DBE6A7", "E4E6CF", "22371F", True),
    "brown": ("4C3634", "root-network-brown-portrait.png", "F4F1EA", "E8CDB8", "F1E4D6", "3A2524", True),
}
_F = {}


def width(t, pt, font):
    path = {SANS: "~/.fonts/Montserrat-Regular.ttf", SERIF: "~/.fonts/EBGaramond-Regular.ttf"}[font]
    key = (font, pt)
    if key not in _F: _F[key] = ImageFont.truetype(os.path.expanduser(path), int(pt * 1.3333))
    return _F[key].getlength(t)


def lines(t, pt, w, font):
    n = 0
    for para in t.split("\n"):
        n += 1; cur = ""
        for word in para.split(" "):
            trial = (cur + " " + word).strip()
            if cur and width(trial, pt, font) > w: n += 1; cur = word
            else: cur = trial
    return n


def lh(pt, sp): return pt * 1.3333 * 1.17 * sp


def block(s, x, y, w, t, pt, color, font, sp=1.1):
    h = lines(t, pt, w * 0.97, font) * lh(pt, sp)
    text(s, x, y, w, h + 12, t, pt, color, font, False, spacing=sp)
    return y + h


def slide(d, theme, note):
    g, roots, *_ = THEMES[theme]
    s = d.slide(g, note, counter=False)
    rect(s, 0, 0, W, H, g)
    s.shapes.add_picture(os.path.join(ROOT, "assets/collage", roots), 0, 0, Emu(W * PX), Emu(H * PX))
    return s


def arch(s, rel, x, y, w, h, fx=0.5, fy=0.5, frame="F6E3C2"):
    """Main photo: a straight rectangle with a cream frame (arches removed on request)."""
    framed(s, rel, x, y, w, h, fx, fy, frame)


def framed(s, rel, x, y, w, h, fx=0.5, fy=0.5, frame="F6E3C2"):
    rect(s, x - 10, y - 10, w + 20, h + 20, frame, shadow=True)
    s.shapes.add_picture(crop(rel, int(w), int(h), fx, fy), Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def eyebrow(s, theme, y, t, x=80):
    _, _, head, acc, *_ = THEMES[theme]
    rect(s, x, y, 300, 6, acc)
    text(s, x, y + 16, 900, 50, t, 32, acc, SANS, False)


def band(s, theme, y, t, pt=30, head=None, hpt=40):
    """Cream band across the slide: optional Roboto headline, then Times New Roman text. Sized to the text."""
    _, _, _, _, bg, fg, _ = THEMES[theme]
    tw = 900
    hh = lines(head, hpt, tw * 0.97, SANS) * lh(hpt, 1.05) + 14 if head else 0
    th = lines(t, pt, tw * 0.97, SERIF) * lh(pt, 1.15)
    h = hh + th + 70
    rect(s, 0, y, W, h, bg, alpha=88)
    yy = y + 35
    if head:
        text(s, 90, yy, tw, hh, head, hpt, fg, SANS, True, spacing=1.05); yy += hh
    text(s, 90, yy, tw, th + 10, t, pt, fg, SERIF, False, spacing=1.15)
    return y + h


def quote(s, theme, t, y=150, pt=50):
    _, _, head, acc, *_ = THEMES[theme]
    text(s, 70, y - 110, 200, 200, "“", 150, acc, SERIF, False, spacing=0.8)
    return block(s, 90, y + 40, 900, t, pt, head, SERIF, 1.12)


def logo_for(s, theme, x=W - 60 - 130, y=H - 50 - 117, w=130):
    logo(s, x, y, w, white=THEMES[theme][6])


def build():
    d = Deck(name="01-10-2026-thu-ig-soil-regenerators-boubacar-roots")
    NOTE = " Root-network style (as the LinkedIn option E card). Fonts: Montserrat and EB Garamond (brand). Same words as the scrapbook version."

    # 1 cover, gold
    s = slide(d, "gold", "Cover." + NOTE + " " + SOURCES + " Photo: boubacar-portrait-bananas-closer.jpg.")
    logo(s, 60, 50, 170, white=False)
    arch(s, B + "boubacar-portrait-bananas-closer.jpg", 420, 70, 560, 800, 0.5, 0.35)
    eyebrow(s, "gold", 930, "Happy International Coffee Day")
    text(s, 80, 1005, 940, 200, "Boubacar Tidiane Diallo,\nGuinea-Conakry", 52, "1E1412", SANS, False, spacing=0.98)

    # 2 Gnaly, green
    s = slide(d, "green", "Gnaly." + NOTE + " Photos: farm-overview-with-tanks.jpeg, young-tree-with-pineapples.jpg, man-by-water-tanks.jpeg.")
    arch(s, B + "farm-overview-with-tanks.jpeg", 80, 90, 460, 700, 0.5, 0.5, "E4E6CF")
    framed(s, B + "young-tree-with-pineapples.jpg", 610, 110, 390, 300, 0.5, 0.55, "E4E6CF")
    framed(s, B + "man-by-water-tanks.jpeg", 610, 470, 390, 320, 0.4, 0.5, "E4E6CF")
    band(s, "green", 880, "Fouta Djallon, Guinea-Conakry", 42, "Gnaly Coffee & AgroÉcole Bio", 52)

    # 3 the question, brown
    s = slide(d, "brown", "Quote." + NOTE + " Photo: vegetable-beds-by-building.jpeg.")
    y = quote(s, "brown", "“Today, I ask a different question: What does the soil food web need to thrive?”", 150, 60)
    arch(s, B + "vegetable-beds-by-building.jpeg", 300, y + 80, 480, 1260 - (y + 80), 0.6, 0.25, "F1E4D6")

    # 4 how he feeds his soil, gold
    s = slide(d, "gold", "Method." + NOTE + " Photos: boubacar-compost-pile.jpeg; still-biochar-kiln-smoke-73s.png (making-biochar-in-barrel-kiln.mp4 at 1:13).")
    arch(s, B + "boubacar-compost-pile.jpeg", 80, 80, 560, 700, 0.5, 0.45)
    framed(s, B + "still-biochar-kiln-smoke-73s.png", 700, 300, 300, 440, 0.5, 0.4)
    band(s, "gold", 850, "living groundcover, mulch from his farm and the forest, and compost with biochar activated with fish hydrolysate and compost tea.",
         38, "How he feeds his soil:", 46)

    # 5 compost and mulch at work, green
    s = slide(d, "green", "His words (email to Allison, 30 Sep 2026)." + NOTE + " Photos: carrying-mulch.jpg, still-biochar-charcoal-16s.png, barrel-brew-under-shelter.jpeg.")
    arch(s, B + "carrying-mulch.jpg", 80, 80, 440, 760, 0.5, 0.5, "E4E6CF")
    framed(s, B + "still-biochar-charcoal-16s.png", 590, 100, 410, 330, 0.5, 0.5, "E4E6CF")
    framed(s, B + "barrel-brew-under-shelter.jpeg", 590, 490, 410, 350, 0.5, 0.35, "E4E6CF")
    band(s, "green", 930, "“I apply compost regularly around young trees and whenever I add new mulch.”", 44)

    # 6 what he grows together, brown
    s = slide(d, "brown", "Crops." + NOTE + " Photos: planting-seedling-in-agroforest.jpeg, banana-bunch.jpg.")
    arch(s, B + "planting-seedling-in-agroforest.jpeg", 80, 80, 560, 740, 0.45, 0.45, "F1E4D6")
    framed(s, B + "banana-bunch.jpg", 700, 320, 300, 440, 0.5, 0.35, "F1E4D6")
    band(s, "brown", 900, "coffee, cacao, bananas, citrus, and pineapple.", 42, "What he grows together:", 50)

    # 7 harvest, gold
    s = slide(d, "gold", "His words (email to Allison, 30 Sep 2026)." + NOTE + " Photos: buckets-of-tubers.jpg, young-tree-yellow-new-leaves.jpg, man-with-harvested-tubers.jpeg [VERIFY who].")
    arch(s, B + "buckets-of-tubers.jpg", 80, 80, 520, 680, 0.5, 0.5)
    framed(s, B + "young-tree-yellow-new-leaves.jpg", 660, 100, 340, 300, 0.5, 0.45)
    framed(s, B + "man-with-harvested-tubers.jpeg", 660, 460, 340, 300, 0.5, 0.5)
    band(s, "gold", 850, "“My compost includes plant residues, animal manure when available, biochar activated with fish hydrolysate and compost tea, and local organic materials.”", 40)

    # 8 what he's seeing, green
    s = slide(d, "green", "Results." + NOTE + " Photos: millipede-leaf-litter.jpg, boubacar-hand-compost-worm.jpg.")
    arch(s, B + "millipede-leaf-litter.jpg", 80, 80, 560, 740, 0.5, 0.35, "E4E6CF")
    framed(s, B + "boubacar-hand-compost-worm.jpg", 700, 320, 300, 440, 0.4, 0.5, "E4E6CF")
    band(s, "green", 890, "more earthworms, more mushrooms, active decomposition, and better soil structure.", 40, "What he's seeing:", 50)

    # 9 life in his soil, brown
    s = slide(d, "brown", "His words (email to Allison, 30 Sep 2026)." + NOTE + " Photos: yellow-caterpillar-on-stem.jpg, caterpillar-on-leaf.jpg, still-young-plants-buckets-29s.png.")
    arch(s, B + "yellow-caterpillar-on-stem.jpg", 80, 80, 460, 740, 0.35, 0.4, "F1E4D6")
    framed(s, B + "caterpillar-on-leaf.jpg", 600, 100, 400, 320, 0.5, 0.35, "F1E4D6")
    framed(s, B + "still-young-plants-buckets-29s.png", 600, 480, 400, 340, 0.5, 0.55, "F1E4D6")
    band(s, "brown", 900, "“I can already see signs of healthier soil in the field, including more earthworms, mushrooms, and active decomposition.”", 42)

    # 10 community, gold
    s = slide(d, "gold", "His words (email to Allison, 30 Sep 2026)." + NOTE + " Photos: group-of-five-farmers.jpeg, two-men-at-shade-house.jpeg, shade-house.jpg [VERIFY who, where, when].")
    framed(s, B + "group-of-five-farmers.jpeg", 80, 80, 920, 480, 0.5, 0.5)
    framed(s, B + "two-men-at-shade-house.jpeg", 80, 620, 440, 300, 0.5, 0.35)
    framed(s, B + "shade-house.jpg", 560, 620, 440, 300, 0.5, 0.5)
    band(s, "gold", 990, "“Your training changed the way I see agriculture. I now believe that agriculture is biology, not chemical fertilizer.”", 42)

    # 11 dream and call, green
    s = slide(d, "green", "Closing quote and call to action (YouTube)." + NOTE + " Photo: young-coffee-plant.jpg.")
    y = quote(s, "green", "“My dream is to restore degraded land in the Fouta Djallon and help my community learn living-soil practices.”", 130, 52)
    arch(s, B + "young-coffee-plant.jpg", 330, y + 70, 420, 1140 - (y + 70), 0.5, 0.5, "E4E6CF")
    rect(s, 0, 1175, W, 90, "E4E6CF", alpha=92)
    text(s, 0, 1175, W, 90, "Subscribe on YouTube: @boubacartidianediallo", 28, "22371F", SANS, True, align="c", anchor="m")
    logo(s, W - 60 - 110, 40, 110, white=True)

    # Stephanie: logo on the first and last slide, soilfoodweb.com small on the rest
    foot = {"gold": "1E1412", "green": "F4F1EA", "brown": "F4F1EA"}
    order = ["gold", "green", "brown", "gold", "green", "brown", "gold", "green", "brown", "gold", "green"]
    for i, sl in enumerate(list(d.prs.slides)[1:-1], 1):
        text(sl, 0, H - 58, W, 44, "soilfoodweb.com", 26, foot[order[i]], SANS, False, align="c", anchor="m")
    save(d, "01-10-2026-thu-ig-soil-regenerators-boubacar-roots.pptx")


if __name__ == "__main__":
    build()
