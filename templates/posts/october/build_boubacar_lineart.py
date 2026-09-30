"""Boubacar carousel, third version: realistic botanical line drawings (Stephanie's direction) and a clearer story.

Arc: cover, the hook (before, then his question), the land, what he feeds the soil, how, his compost, what grows,
what's changing, life returning, passing it on, the dream. A small numbered chapter label runs through every slide.
Cream paper, photos in thin line frames, line art in Deep Green, brand fonts (Montserrat, Source Sans 3,
EB Garamond italic for his words). Logo on the first and last slide, soilfoodweb.com on the others.

python3 build_boubacar_lineart.py  ->  01-10-2026-thu-ig-soil-regenerators-boubacar-lineart.pptx
"""
import os
from pptx.util import Emu
from lib import Deck, rect, rrect, text, crop, DEEP, GREEN, INK, GOLD, CREAM, HEAD, BODY, PX, ROOT
from build_oct_01_10 import cream, n_lines, lh, logo, save, CUT
from build_boubacar import B, SOURCES
import scrapbook as sb

W, H = 1080, 1350
GARA = "EB Garamond"
LINE = CUT + "line-{}-1.png"
NOTE = (" Line-art version: realistic botanical line drawings made with flux-2-pro (no style reference, objects only, "
        "never Boubacar or his farm), recoloured Deep Green. ")


def art(s, name, cx, cy, w, deg=0):
    p = LINE.format(name)
    if os.path.exists(os.path.join(ROOT, p)):
        return sb.cutout(s, p, cx, cy, w, deg)
    print("missing line art:", name)


def photo(s, rel, x, y, w, h, fx=0.5, fy=0.5):
    """Photo with a thin Deep Green line frame set 14 px outside it."""
    rect(s, x - 14, y - 14, w + 28, h + 28, None, line=DEEP, lw=2)
    s.shapes.add_picture(crop(rel, int(w), int(h), fx, fy), Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def chapter(s, n, t):
    text(s, 80, 70, 900, 36, f"{n:02d}   {t.upper()}", 20, GREEN, HEAD, True, track=3)
    rect(s, 80, 112, 70, 3, GOLD)


def footer(s, swipe=True):
    text(s, 0, H - 62, W, 40, "soilfoodweb.com", 22, DEEP, HEAD, True, align="c", anchor="m")
    if swipe:
        text(s, W - 170, H - 62, 110, 40, "→", 30, GREEN, HEAD, True, align="r", anchor="m")


def para(s, x, y, w, t, pt, font=BODY, color=INK, bold=False, italic=False, sp=1.2):
    h = n_lines(t, pt, w * 0.96, font, bold) * lh(pt, sp)
    text(s, x, y, w, h + 12, t, pt, color, font, bold, italic=italic, spacing=sp)
    return y + h


def heading_body(s, y, head, body, hpt=46, bpt=36):
    y = para(s, 80, y, 920, head, hpt, HEAD, GREEN, True, sp=1.05) + 14
    return para(s, 80, y, 920, body, bpt, BODY, INK)


def his_words(s, y, t, pt=40):
    text(s, 64, y - 58, 120, 120, "“", 110, GOLD, GARA, False, spacing=0.8)
    return para(s, 80, y + 20, 920, t.strip("“”"), pt, GARA, DEEP, False, True, 1.15)


def build():
    d = Deck(name="01-10-2026-thu-ig-soil-regenerators-boubacar-lineart")

    # 1 cover
    s = cream(d, "Cover." + NOTE + SOURCES + " Photo: boubacar-portrait-bananas-closer.jpg.")
    photo(s, B + "boubacar-portrait-bananas-closer.jpg", 420, 90, 580, 820, 0.5, 0.35)
    art(s, "coffee-branch", 220, 600, 380, -12)
    logo(s, 70, 70, 150, white=False)
    text(s, 80, 960, 900, 40, "HAPPY INTERNATIONAL COFFEE DAY", 22, GREEN, HEAD, True, track=3)
    rect(s, 80, 1002, 70, 3, GOLD)
    text(s, 80, 1025, 940, 150, "Boubacar Tidiane\nDiallo", 56, DEEP, HEAD, True, spacing=1.0)
    text(s, 80, 1180, 900, 60, "Guinea-Conakry", 40, GREEN, GARA, False, italic=True)
    text(s, W - 170, H - 62, 110, 40, "→", 30, GREEN, HEAD, True, align="r", anchor="m")

    # 2 the hook
    s = cream(d, "The hook. Setup line from the approved caption ('Back then, he told us, he mostly thought about what nutrients "
                 "his plants needed'), shortened; then his quote. Chapter labels are new, short connective words." + NOTE)
    chapter(s, 2, "The question")
    y = para(s, 80, 190, 920, "He used to ask what nutrients his plants needed.", 40, BODY, INK)
    rect(s, 80, y + 40, 920, 1.5, DEEP)
    y = his_words(s, y + 150, "“Today, I ask a different question: What does the soil food web need to thrive?”", 64)
    art(s, "seedling-roots", 540, 1040, 300, 0)
    footer(s)

    # 3 the land
    s = cream(d, "The land. Photos: farm-overview-with-tanks.jpeg, young-tree-with-pineapples.jpg. Degraded-soil line from the "
                 "approved caption ('When he started, the soil had been degraded and poorly managed for years')." + NOTE)
    chapter(s, 3, "The land")
    photo(s, B + "farm-overview-with-tanks.jpeg", 94, 170, 520, 640, 0.5, 0.5)
    photo(s, B + "young-tree-with-pineapples.jpg", 680, 170, 306, 300, 0.5, 0.55)
    art(s, "banana-plant", 830, 680, 300, 4)
    heading_body(s, 880, "Gnaly Coffee & AgroÉcole Bio",
                 "Fouta Djallon, Guinea-Conakry. When he started, the soil had been degraded and poorly managed for years.", 44, 34)
    footer(s)

    # 4 feeding the soil
    s = cream(d, "Photos: boubacar-compost-pile.jpeg; still-biochar-kiln-smoke-73s.png (making-biochar-in-barrel-kiln.mp4 at 1:13)." + NOTE)
    chapter(s, 4, "Feeding the soil")
    photo(s, B + "boubacar-compost-pile.jpeg", 94, 170, 560, 640, 0.5, 0.45)
    photo(s, B + "still-biochar-kiln-smoke-73s.png", 720, 330, 266, 400, 0.5, 0.4)
    art(s, "tithonia", 860, 230, 220, 10)
    heading_body(s, 880, "How he feeds his soil:",
                 "living groundcover, mulch from his farm and the forest, and compost with biochar activated with fish hydrolysate and compost tea.",
                 44, 32)
    footer(s)

    # 5 in practice
    s = cream(d, "His words (email to Allison, 30 Sep 2026). Photos: carrying-mulch.jpg, young-tree-yellow-new-leaves.jpg." + NOTE)
    chapter(s, 5, "In practice")
    photo(s, B + "carrying-mulch.jpg", 94, 170, 480, 700, 0.5, 0.5)
    photo(s, B + "young-tree-yellow-new-leaves.jpg", 650, 170, 336, 380, 0.5, 0.45)
    art(s, "orange-branch", 820, 740, 300, -8)
    his_words(s, 960, "“I apply compost regularly around young trees and whenever I add new mulch.”", 44)
    footer(s)

    # 6 his compost
    s = cream(d, "His words (email to Allison, 30 Sep 2026). Photos: barrel-brew-under-shelter.jpeg, still-biochar-charcoal-16s.png "
                 "(making-biochar-in-barrel-kiln.mp4 at 0:16)." + NOTE)
    chapter(s, 6, "His compost")
    photo(s, B + "barrel-brew-under-shelter.jpeg", 94, 170, 440, 560, 0.5, 0.35)
    photo(s, B + "still-biochar-charcoal-16s.png", 600, 170, 386, 330, 0.5, 0.5)
    art(s, "compost-pile", 790, 660, 330, 0)
    his_words(s, 850, "“My compost includes plant residues, animal manure when available, biochar activated with fish hydrolysate "
                      "and compost tea, and local organic materials.”", 38)
    footer(s)

    # 7 what grows
    s = cream(d, "Photos: planting-seedling-in-agroforest.jpeg, banana-bunch.jpg." + NOTE)
    chapter(s, 7, "What grows")
    photo(s, B + "planting-seedling-in-agroforest.jpeg", 94, 170, 540, 660, 0.45, 0.45)
    photo(s, B + "banana-bunch.jpg", 700, 170, 286, 380, 0.5, 0.35)
    art(s, "cacao-pod", 760, 700, 200, -10)
    art(s, "pineapple-plant", 930, 720, 210, 6)
    heading_body(s, 900, "What he grows together:", "coffee, cacao, bananas, citrus, and pineapple.", 44, 36)
    art(s, "coffee-branch", 930, 1150, 200, 20)
    footer(s)

    # 8 what's changing
    s = cream(d, "Photos: millipede-leaf-litter.jpg, boubacar-hand-compost-worm.jpg." + NOTE)
    chapter(s, 8, "What's changing")
    photo(s, B + "millipede-leaf-litter.jpg", 94, 170, 540, 660, 0.5, 0.35)
    photo(s, B + "boubacar-hand-compost-worm.jpg", 700, 170, 286, 380, 0.4, 0.5)
    art(s, "earthworm", 820, 680, 260, -6)
    art(s, "mushroom-cluster", 860, 800, 170, 0)
    heading_body(s, 900, "What he's seeing:", "more earthworms, more mushrooms, active decomposition, and better soil structure.", 44, 36)
    footer(s)

    # 9 life returns
    s = cream(d, "His words (email to Allison, 30 Sep 2026). Photos: yellow-caterpillar-on-stem.jpg, caterpillar-on-leaf.jpg." + NOTE)
    chapter(s, 9, "Life returns")
    photo(s, B + "yellow-caterpillar-on-stem.jpg", 94, 170, 480, 660, 0.35, 0.4)
    photo(s, B + "caterpillar-on-leaf.jpg", 650, 170, 336, 330, 0.5, 0.35)
    art(s, "millipede", 810, 690, 300, 0)
    his_words(s, 930, "“I can already see signs of healthier soil in the field, including more earthworms, mushrooms, and active "
                      "decomposition.”", 40)
    footer(s)

    # 10 passing it on
    s = cream(d, "His words (email to Allison, 30 Sep 2026). Photos: group-of-five-farmers.jpeg, two-men-at-shade-house.jpeg "
                 "[VERIFY who, where, when]." + NOTE)
    chapter(s, 10, "Passing it on")
    photo(s, B + "group-of-five-farmers.jpeg", 94, 170, 892, 440, 0.5, 0.5)
    photo(s, B + "two-men-at-shade-house.jpeg", 94, 670, 420, 260, 0.5, 0.35)
    art(s, "seedling-roots", 780, 800, 280, 0)
    his_words(s, 1010, "“Your training changed the way I see agriculture. I now believe that agriculture is biology, not chemical "
                       "fertilizer.”", 38)
    footer(s)

    # 11 the dream
    s = cream(d, "The dream and the call to action (YouTube)." + NOTE + " Photo: young-coffee-plant.jpg.")
    chapter(s, 11, "The dream")
    y = his_words(s, 200, "“My dream is to restore degraded land in the Fouta Djallon and help my community learn living-soil practices.”", 50)
    photo(s, B + "young-coffee-plant.jpg", 94, y + 70, 460, 1150 - (y + 70), 0.5, 0.5)
    art(s, "coffee-branch", 800, y + 250, 360, 10)
    rrect(s, 80, 1190, 920, 80, GREEN, radius=40)
    text(s, 80, 1190, 920, 80, "Subscribe on YouTube: @boubacartidianediallo", 24, CREAM, HEAD, True, align="c", anchor="m")
    logo(s, W - 70 - 120, 50, 120, white=False)

    save(d, "01-10-2026-thu-ig-soil-regenerators-boubacar-lineart.pptx")


if __name__ == "__main__":
    build()
