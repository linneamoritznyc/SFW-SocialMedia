"""Soil Regenerators in the wild: Boubacar Tidiane Diallo, Guinea-Conakry (Thu 1 Oct 2026). Instagram carousel and LinkedIn image.

python3 build_boubacar.py
Scrapbook style on cream paper: straight taped prints of Boubacar's own photos, cut-paper pieces (objects only, never his
face or his farm), slide text exactly as in the brief. Every element is a separate editable object.
"""
import os
from pptx.util import Emu
from lib import Deck, rect, rrect, text, crop, _place, ROOT, PX, DEEP, GREEN, CREAM, GLOW, INK, FAINT, GOLD, HEAD, BODY
import scrapbook as sb
from build_oct_01_10 import GRAIN, cream, block, n_lines, lh, logo, logo_br, text_width, save, CUT, paper as _paper

B = "assets/photo/boubacar/"
CUTS = " Cut-paper pieces are objects only (flux-2-pro); nothing generated shows Boubacar or his farm."


def paper(s, name, cx, cy, w, deg=0):
    return _paper(s, name, cx, cy, w, deg)


def print_(s, rel, x, y, w, h, fx=0.5, fy=0.5, tapes=True):
    """Straight paper print (no tilt) of a real photo, w x h photo area."""
    b = 18
    rect(s, x - b, y - b, w + 2 * b, h + 2 * b, sb.PAPER, shadow=True)
    p = crop(rel, int(w), int(h), fx, fy)
    s.shapes.add_picture(p, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    if tapes:
        sb.tape(s, x + 30, y - 8, 160, 48, -30); sb.tape(s, x + w - 30, y - 8, 160, 48, 30)


def text_box(s, head, body, y, h):
    """Cream text box with the headline in Food Web Green and the rest in Deep Green."""
    rect(s, 60, y, 960, h, sb.PAPER, shadow=True)
    text(s, 100, y + 30, 880, 70, head, 46, GREEN, HEAD, True, anchor="m")
    text(s, 100, y + 110, 880, h - 130, body, 38, DEEP, BODY, False, spacing=1.15)


def quote_marks(s, x, y, pt=300):
    text(s, x, y, 400, pt * 1.1, "“", pt, GOLD, HEAD, True, spacing=0.8)


SOURCES = ("Call to action: his YouTube channel (his Instagram @tidia.diallo.1 is private). Sources: Impact story sheet, Boubacar Tidiane Diallo: "
           "https://docs.google.com/spreadsheets/d/10UHLwzJLBQAsmJqmg4hiCQRjBKXPAx7UnOudU-Vsg5U/edit; Email from Boubacar to Allison, "
           "30 September 2026; Instagram: https://www.instagram.com/tidia.diallo.1/; YouTube: https://www.youtube.com/@boubacartidianediallo; "
           "Facebook: https://www.facebook.com/btidja; Photos: sent by Boubacar to Stephanie on WhatsApp, 17 August 2026, and to Allison, "
           "September 2026. [TAG @Stephanie] Send Boubacar the final caption and slides to approve before posting, and confirm he studied on a scholarship.")


HIS = (" New slide: the caption is Boubacar's own words, quoted from his email to Allison, 30 September 2026. "
       "Include it in the text he approves.")


def caption(s, t, y=None, h=None, pt=32):
    """His words on a straight paper strip, sized to the measured text and ending 50 px above the bottom edge."""
    n = n_lines(t, pt, 880 * 0.95)
    h = n * lh(pt, 1.12) + 60
    y = 1300 - h
    rect(s, 60, y, 960, h, sb.PAPER, shadow=True)
    text(s, 100, y + 30, 880, h - 60, t, pt, DEEP, HEAD, True, anchor="m", spacing=1.12)


def instagram():
    d = Deck(name="01-10-2026-thu-ig-soil-regenerators-boubacar")

    # 1 Soil Regenerators in the wild
    s = cream(d, "Template 1, scrapbook. " + SOURCES + " Photo: assets/photo/boubacar/boubacar-portrait-bananas.jpg. "
                 "Guinea flag sticker: vertical red, yellow and green bands, drawn as shapes." + CUTS)
    print_(s, B + "boubacar-portrait-bananas.jpg", 200, 150, 680, 820, 0.5, 0.3)
    rrect(s, 60, 60, 700, 72, DEEP, radius=36)
    text(s, 60, 60, 700, 72, "Happy International Coffee Day", 28, GLOW, HEAD, True, align="c", anchor="m")
    rect(s, 60, 1030, 960, 250, DEEP, shadow=True)
    sb.tape(s, 110, 1030, 170, 50, -28); sb.tape(s, 970, 1030, 170, 50, 28)
    text(s, 110, 1070, 770, 180, "Boubacar Tidiane\nDiallo, Guinea-Conakry", 46, CREAM, HEAD, True, spacing=1.05, anchor="m")
    logo(s, 900, 1170, 90, white=True)
    sb.guinea_flag(s, 930, 200, 190, 8)
    paper(s, "coffee-cherries-branch", 930, 880, 290, -10)
    paper(s, "coffee-cup-paper", 120, 880, 210, -6)
    paper(s, "leaf-sprig-paper", 130, 260, 190, -20)

    # 2 Gnaly (new): the farm
    s = cream(d, "Photo wall: assets/photo/boubacar/farm-overview-with-tanks.jpeg, man-by-water-tanks.jpeg, "
                 "young-tree-with-pineapples.jpg (WhatsApp, 17 Aug 2026, and Allison, Sep 2026). Caption: farm name and region from "
                 "his email signature (30 Sep 2026)." + CUTS)
    print_(s, B + "farm-overview-with-tanks.jpeg", 90, 110, 440, 560, 0.5, 0.5)
    print_(s, B + "young-tree-with-pineapples.jpg", 580, 110, 410, 330, 0.5, 0.55)
    print_(s, B + "man-by-water-tanks.jpeg", 580, 500, 410, 420, 0.4, 0.5)
    sb.guinea_flag(s, 250, 800, 170, -6)
    paper(s, "pineapple", 440, 830, 140, 8)
    caption(s, "Gnaly Coffee & AgroÉcole Bio, Fouta Djallon, Guinea-Conakry", 1000, 170)
    paper(s, "coffee-beans-paper", 960, 1030, 160, 10)
    paper(s, "banana-bunch", 470, 1030, 170, -8)

    # 3 quote (was 2): his face with coffee seedlings
    s = cream(d, "Quote slide. Photo: assets/photo/boubacar/vegetable-beds-by-building.jpeg (Boubacar in his vegetable beds, WhatsApp, "
                 "17 Aug 2026), cropped to remove a blurred fingertip at the bottom." + CUTS)
    quote_marks(s, 60, 40, 260)
    y = block(s, 90, 250, 900, "“Today, I ask a different question: What does the soil food web need to thrive?”", 56, DEEP, HEAD, True, 1.1)
    print_(s, B + "vegetable-beds-by-building.jpeg", 250, y + 70, 580, 1260 - (y + 70), 0.6, 0.25)
    paper(s, "happy-seedling", 120, 1180, 170, -6)
    paper(s, "mushroom-paper", 970, 1190, 160, -4)
    paper(s, "coffee-cherries-branch", 960, y + 140, 200, 20)

    # 4 how he feeds his soil
    s = cream(d, "Photo slide. Main: assets/photo/boubacar/boubacar-compost-pile.jpeg (WhatsApp, 17 Aug 2026). Inset: "
                 "assets/photo/boubacar/still-biochar-kiln-smoke-73s.png, from assets/video/boubacar/making-biochar-in-barrel-kiln.mp4 "
                 "(WhatsApp Video 2026-08-17 at 13.46.34) at 1:13." + CUTS)
    print_(s, B + "boubacar-compost-pile.jpeg", 110, 110, 560, 680, 0.5, 0.45)
    print_(s, B + "still-biochar-kiln-smoke-73s.png", 720, 330, 260, 400, 0.5, 0.4)
    paper(s, "tithonia-flower", 860, 190, 200, 10)
    text_box(s, "How he feeds his soil:",
             "living groundcover, mulch from his farm and the forest, and compost with biochar activated with fish hydrolysate and compost tea.",
             860, 430)

    # 5 compost and mulch at work (new)
    s = cream(d, "Photo wall: assets/photo/boubacar/carrying-mulch.jpg (cropped from a phone screenshot), "
                 "still-biochar-charcoal-16s.png (making-biochar-in-barrel-kiln.mp4 at 0:16), barrel-brew-under-shelter.jpeg." + HIS + CUTS)
    print_(s, B + "carrying-mulch.jpg", 90, 110, 400, 700, 0.5, 0.5)
    print_(s, B + "still-biochar-charcoal-16s.png", 560, 110, 420, 330, 0.5, 0.5)
    print_(s, B + "barrel-brew-under-shelter.jpeg", 560, 500, 420, 430, 0.5, 0.35)
    paper(s, "tithonia-flower", 470, 880, 180, -8)
    caption(s, "“I apply compost regularly around young trees and whenever I add new mulch.”", 1010, 220)
    paper(s, "leaf-sprig-paper", 1000, 960, 150, 20)

    # 6 what he grows together
    s = cream(d, "Photo slide. Main: assets/photo/boubacar/planting-seedling-in-agroforest.jpeg (planting a coffee seedling, WhatsApp, 17 Aug 2026). Inset: assets/photo/boubacar/banana-bunch.jpg. "
                 "Stickers: coffee, cacao, cocoa beans, orange, pineapple." + CUTS)
    print_(s, B + "planting-seedling-in-agroforest.jpeg", 110, 110, 540, 700, 0.45, 0.45)
    print_(s, B + "banana-bunch.jpg", 720, 390, 270, 360, 0.5, 0.35)
    paper(s, "coffee-cherries-branch", 860, 200, 260, 8)
    paper(s, "cacao-pod", 95, 800, 130, -15)
    text_box(s, "What he grows together:", "coffee, cacao, bananas, citrus, and pineapple.", 900, 300)
    paper(s, "citrus-orange", 985, 810, 140, -8)
    paper(s, "pineapple", 985, 1230, 150, 10)
    paper(s, "cocoa-beans", 150, 1250, 190, -6)
    paper(s, "coffee-cup-paper", 780, 1255, 140, 4)

    # 7 harvest (new)
    s = cream(d, "Photo wall: assets/photo/boubacar/buckets-of-tubers.jpg, young-tree-yellow-new-leaves.jpg, "
                 "man-with-harvested-tubers.jpeg (confirm who is in it [VERIFY])." + HIS + CUTS)
    print_(s, B + "buckets-of-tubers.jpg", 90, 110, 520, 600, 0.5, 0.5)
    print_(s, B + "young-tree-yellow-new-leaves.jpg", 670, 110, 320, 420, 0.5, 0.45)
    print_(s, B + "man-with-harvested-tubers.jpeg", 670, 590, 320, 330, 0.5, 0.5)
    paper(s, "banana-bunch", 130, 800, 180, -10)
    paper(s, "cocoa-beans", 480, 800, 170, 8)
    caption(s, "“My compost includes plant residues, animal manure when available, biochar activated with fish hydrolysate and "
               "compost tea, and local organic materials.”", 990, 290)

    # 8 what he's seeing
    s = cream(d, "Photo slide. Main: assets/photo/boubacar/millipede-leaf-litter.jpg (active decomposition). Inset: "
                 "assets/photo/boubacar/boubacar-hand-compost-worm.jpg (earthworm)." + CUTS)
    print_(s, B + "millipede-leaf-litter.jpg", 110, 110, 540, 700, 0.5, 0.35)
    print_(s, B + "boubacar-hand-compost-worm.jpg", 720, 330, 270, 400, 0.4, 0.5)
    paper(s, "mushroom-paper", 860, 190, 170, 8)
    paper(s, "happy-seedling", 690, 830, 150, -6)
    text_box(s, "What he's seeing:", "more earthworms, more mushrooms, active decomposition, and better soil structure.", 900, 360)

    # 9 life in his soil (new)
    s = cream(d, "Photo wall: assets/photo/boubacar/caterpillar-on-leaf.jpg, yellow-caterpillar-on-stem.jpg, "
                 "still-young-plants-buckets-29s.png (watering-young-plants-in-buckets.mp4 at 0:29)." + HIS + CUTS)
    print_(s, B + "yellow-caterpillar-on-stem.jpg", 90, 110, 440, 620, 0.35, 0.4)
    print_(s, B + "caterpillar-on-leaf.jpg", 590, 110, 400, 330, 0.5, 0.35)
    print_(s, B + "still-young-plants-buckets-29s.png", 590, 500, 400, 420, 0.5, 0.55)
    paper(s, "mushroom-paper", 460, 850, 150, 6)
    paper(s, "tithonia-flower", 130, 850, 170, -10)
    caption(s, "“I can already see signs of healthier soil in the field, including more earthworms, mushrooms, and active decomposition.”",
            1000, 270)

    # 10 community (new)
    s = cream(d, "Photo wall: assets/photo/boubacar/group-of-five-farmers.jpeg, two-men-at-shade-house.jpeg, shade-house.jpg "
                 "(cropped from a phone screenshot). Confirm where and when these were taken and who is in them [VERIFY]." + HIS + CUTS)
    print_(s, B + "group-of-five-farmers.jpeg", 90, 110, 900, 470, 0.5, 0.5)
    print_(s, B + "two-men-at-shade-house.jpeg", 90, 650, 430, 310, 0.5, 0.35)
    print_(s, B + "shade-house.jpg", 570, 650, 420, 310, 0.5, 0.5)
    sb.guinea_flag(s, 960, 110, 150, 10)
    caption(s, "“Your training changed the way I see agriculture. I now believe that agriculture is biology, not chemical fertilizer.”",
            1070, 220)

    # 11 quote and follow
    s = cream(d, "Quote slide. Photo: assets/photo/boubacar/young-coffee-plant.jpg." + CUTS)
    quote_marks(s, 60, 30, 240)
    y = block(s, 90, 230, 900, "“My dream is to restore degraded land in the Fouta Djallon and help my community learn living-soil practices.”",
              50, DEEP, HEAD, True, 1.1)
    print_(s, B + "young-coffee-plant.jpg", 290, y + 60, 500, 1150 - (y + 60), 0.5, 0.5)
    rrect(s, 60, 1190, 960, 76, GREEN, radius=38)
    text(s, 60, 1190, 960, 76, "Subscribe on YouTube: @boubacartidianediallo", 26, CREAM, HEAD, True, align="c", anchor="m")
    paper(s, "coffee-cup-paper", 150, 1000, 200, -6)
    paper(s, "coffee-beans-paper", 930, 1000, 170, 20)
    sb.guinea_flag(s, 960, 700, 130, 6)
    logo(s, 1080 - 50 - 110, 50, 110, white=False)
    # Stephanie: logo on the first and last slide, soilfoodweb.com small on the rest
    for sl in list(d.prs.slides)[1:-1]:
        text(sl, 0, 1350 - 44, 1080, 34, "soilfoodweb.com", 17, DEEP, HEAD, True, align="c", anchor="m")
    save(d, "01-10-2026-thu-ig-soil-regenerators-boubacar.pptx")


def linkedin():
    """Cover image for the LinkedIn post: scrapbook page, one taped photo, cut-paper crops, flag and logo."""
    d = Deck(1200, 627, name="01-10-2026-thu-li-boubacar")
    s = d.slide(CREAM, "LinkedIn cover image. " + SOURCES + " Photo: assets/photo/boubacar/boubacar-portrait-bananas.jpg. "
                       "Words are the same as the Instagram cover. Guinea flag drawn as shapes; crops are cut-paper pieces." + CUTS,
                counter=False)
    grain = crop(GRAIN, 1200, 627, 0.5, 0.5)
    s.shapes.add_picture(grain, 0, 0, Emu(1200 * PX), Emu(627 * PX))
    print_(s, B + "boubacar-portrait-bananas.jpg", 90, 70, 400, 480, 0.5, 0.32)
    rrect(s, 560, 90, 520, 60, DEEP, radius=30)
    text(s, 560, 90, 520, 60, "Happy International Coffee Day", 22, GLOW, HEAD, True, align="c", anchor="m")
    text(s, 560, 190, 620, 180, "Boubacar Tidiane\nDiallo, Guinea-Conakry", 38, DEEP, HEAD, True, spacing=1.05, anchor="t")
    sb.guinea_flag(s, 640, 440, 110, -6)
    paper(s, "coffee-cherries-branch", 1120, 420, 130, 14)
    paper(s, "coffee-cup-paper", 800, 470, 150, 4)
    paper(s, "cocoa-beans", 960, 490, 150, -10)
    paper(s, "pineapple", 70, 520, 120, -10)
    paper(s, "tithonia-flower", 520, 520, 120, 12)
    paper(s, "leaf-sprig-paper", 80, 90, 120, -24)
    logo(s, 1200 - 30 - 100, 627 - 30 - 90, 100, white=False)
    save(d, "01-10-2026-thu-li-boubacar.pptx")


if __name__ == "__main__":
    instagram(); linkedin()
