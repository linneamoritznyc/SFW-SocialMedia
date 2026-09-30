"""Soil Regenerators in the wild: Boubacar Tidiane Diallo, Guinea (Thu 1 Oct 2026). Instagram carousel and LinkedIn image.

python3 build_boubacar.py
Scrapbook style on cream paper: straight taped prints of Boubacar's own photos, cut-paper pieces (objects only, never his
face or his farm), slide text exactly as in the brief. Every element is a separate editable object.
"""
import os
from pptx.util import Emu
from lib import Deck, rect, rrect, text, crop, _place, ROOT, PX, DEEP, GREEN, CREAM, GLOW, INK, FAINT, GOLD, HEAD, BODY
import scrapbook as sb
from build_oct_01_10 import cream, block, n_lines, lh, logo, logo_br, text_width, save, CUT, paper as _paper

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


SOURCES = ("Instagram collab: @tidia.diallo.1. Sources: Impact story sheet, Boubacar Tidiane Diallo: "
           "https://docs.google.com/spreadsheets/d/10UHLwzJLBQAsmJqmg4hiCQRjBKXPAx7UnOudU-Vsg5U/edit; Email from Boubacar to Allison, "
           "30 September 2026; Instagram: https://www.instagram.com/tidia.diallo.1/; YouTube: https://www.youtube.com/@boubacartidianediallo; "
           "Facebook: https://www.facebook.com/btidja; Photos: sent by Boubacar to Stephanie on WhatsApp, 17 August 2026, and to Allison, "
           "September 2026. [TAG @Stephanie] Send Boubacar the final caption and slides to approve before posting, and confirm he studied on a scholarship.")


def instagram():
    d = Deck(name="01-10-2026-thu-ig-soil-regenerators-boubacar")

    # 1 Soil Regenerators in the wild
    s = cream(d, "Template 1, scrapbook. " + SOURCES + " Photo: assets/photo/boubacar/boubacar-portrait-bananas.jpg." + CUTS)
    print_(s, B + "boubacar-portrait-bananas.jpg", 200, 150, 680, 820, 0.5, 0.3)
    rrect(s, 60, 60, 620, 72, DEEP, radius=36)
    text(s, 60, 60, 620, 72, "Soil Regenerators in the wild", 28, GLOW, HEAD, True, align="c", anchor="m")
    rect(s, 60, 1030, 960, 250, DEEP, shadow=True)
    sb.tape(s, 110, 1030, 170, 50, -28); sb.tape(s, 970, 1030, 170, 50, 28)
    text(s, 110, 1070, 760, 180, "Boubacar Tidiane Diallo, Guinea", 60, CREAM, HEAD, True, spacing=1.05, anchor="m")
    logo(s, 900, 1170, 90, white=True)
    paper(s, "coffee-cherries-branch", 930, 900, 300, -10)
    paper(s, "leaf-sprig-paper", 130, 260, 200, -20)

    # 2 quote, with his covered soil
    s = cream(d, "Quote slide. Photo: assets/photo/boubacar/boubacar-field-mulch.jpg (his covered soil). Confirm the man in the green "
                 "shirt is Boubacar [VERIFY]." + CUTS)
    quote_marks(s, 60, 40, 260)
    y = block(s, 90, 250, 900, "“Today, I ask a different question: What does the soil food web need to thrive?”", 56, DEEP, HEAD, True, 1.1)
    print_(s, B + "boubacar-field-mulch.jpg", 250, y + 70, 580, 1250 - (y + 70), 0.5, 0.62)
    paper(s, "earthworm-paper", 150, 1180, 200, 6)
    paper(s, "mushroom-paper", 950, 1180, 170, -4)

    # 3 how he feeds his soil
    s = cream(d, "Photo slide. Main: assets/photo/boubacar/boubacar-compost-pile.jpeg (WhatsApp, 17 Aug 2026). Inset: "
                 "assets/photo/boubacar/still-biochar-kiln-smoke-73s.png, from assets/video/boubacar/making-biochar-in-barrel-kiln.mp4 "
                 "(WhatsApp Video 2026-08-17 at 13.46.34) at 1:13. The hand-with-worm photo moved to slide 5 (earthworms)." + CUTS)
    print_(s, B + "boubacar-compost-pile.jpeg", 110, 110, 560, 680, 0.5, 0.45)
    print_(s, B + "still-biochar-kiln-smoke-73s.png", 720, 330, 260, 400, 0.5, 0.4)
    paper(s, "leaf-sprig-paper", 860, 190, 200, 10)
    text_box(s, "How he feeds his soil:",
             "living groundcover, mulch from his farm and the forest, and compost with biochar activated with fish hydrolysate and compost tea.",
             860, 430)

    # 4 what he grows together
    s = cream(d, "Photo slide. Main: assets/photo/boubacar/agroforestry-understory.jpg. Inset: assets/photo/boubacar/banana-bunch.jpg. "
                 "Cut-paper crops: coffee, cacao, citrus, pineapple." + CUTS)
    print_(s, B + "agroforestry-understory.jpg", 110, 110, 540, 700, 0.5, 0.45)
    print_(s, B + "banana-bunch.jpg", 720, 390, 270, 360, 0.5, 0.35)
    paper(s, "coffee-cherries-branch", 860, 200, 260, 8)
    paper(s, "cacao-pod", 95, 800, 130, -15)
    text_box(s, "What he grows together:", "coffee, cacao, bananas, citrus, and pineapple.", 900, 300)
    paper(s, "citrus-orange", 985, 810, 140, -8)
    paper(s, "pineapple", 985, 1230, 150, 10)

    # 5 what he's seeing
    s = cream(d, "Photo slide. Main: assets/photo/boubacar/millipede-leaf-litter.jpg (active decomposition). Inset: "
                 "assets/photo/boubacar/boubacar-hand-compost-worm.jpg (earthworm)." + CUTS)
    print_(s, B + "millipede-leaf-litter.jpg", 110, 110, 540, 700, 0.5, 0.35)
    print_(s, B + "boubacar-hand-compost-worm.jpg", 720, 330, 270, 400, 0.4, 0.5)
    paper(s, "mushroom-paper", 860, 190, 170, 8)
    paper(s, "earthworm-paper", 700, 830, 170, -6)
    text_box(s, "What he's seeing:", "more earthworms, more mushrooms, active decomposition, and better soil structure.", 900, 360)

    # 6 quote and follow
    s = cream(d, "Quote slide. Photo: assets/photo/boubacar/young-coffee-plant.jpg (sharper than the groundcover photo)." + CUTS)
    quote_marks(s, 60, 30, 240)
    y = block(s, 90, 230, 900, "“My dream is to restore degraded land in the Fouta Djallon and help my community learn living-soil practices.”",
              50, DEEP, HEAD, True, 1.1)
    print_(s, B + "young-coffee-plant.jpg", 290, y + 60, 500, 1150 - (y + 60), 0.5, 0.5)
    rrect(s, 190, 1190, 700, 76, GREEN, radius=38)
    text(s, 190, 1190, 700, 76, "Follow him: @tidia.diallo.1", 30, CREAM, HEAD, True, align="c", anchor="m")
    paper(s, "happy-seedling", 150, 1000, 180, -6)
    paper(s, "leaf-sprig-paper", 930, 980, 190, 20)
    logo(s, 1080 - 50 - 110, 50, 110, white=False)
    save(d, "01-10-2026-thu-ig-soil-regenerators-boubacar.pptx")


def linkedin():
    d = Deck(1200, 627, name="01-10-2026-thu-li-boubacar")
    s = d.slide(CREAM, "LinkedIn image. " + SOURCES + " Photo: assets/photo/boubacar/boubacar-portrait-bananas.jpg, cropped to landscape. The mulched-field photo was the first "
                       "choice, but it is portrait and any landscape crop cut off his head. No text on the photo.",
                counter=False)
    p = crop(B + "boubacar-portrait-bananas.jpg", 1200, 627, 0.5, 0.52)
    s.shapes.add_picture(p, 0, 0, Emu(1200 * PX), Emu(627 * PX))
    logo(s, 1200 - 30 - 90, 627 - 30 - 81, 90, white=False)
    save(d, "01-10-2026-thu-li-boubacar.pptx")


if __name__ == "__main__":
    instagram(); linkedin()
