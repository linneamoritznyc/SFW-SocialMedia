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
SOURCES = ("Instagram collab: @tidia.diallo.1 (from Boubacar's reply to Allison) [VERIFY]. Sources: Impact story sheet, Boubacar Tidiane Diallo: https://docs.google.com/spreadsheets/d/10UHLwzJLBQAsmJqmg4hiCQRjBKXPAx7UnOudU-Vsg5U/edit; "
           "YouTube: https://www.youtube.com/@boubacartidianediallo; Facebook: https://www.facebook.com/btidja; "
           "Photos: sent by Boubacar to Stephanie on WhatsApp, 17 August 2026. "
           "[TAG @Stephanie] Send Boubacar the final caption and slides to approve before posting, and confirm he studied on a scholarship.")
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


def instagram():
    d = Deck(name="01-10-2026-thu-ig-soil-regenerators-boubacar")

    # 1 Soil Regenerators in the wild
    s = cream(d, "Template 1, scrapbook. " + SOURCES + " Photo: assets/photo/boubacar/boubacar-raincoat-seedlings-cropped-2x.jpg, "
                 "cropped from the phone screenshot of his Facebook post of 17 July 2024 (status bar, Facebook header and buttons removed) "
                 "and upscaled 2x. [PHOTO NEEDED: the original file from Boubacar]." + CUTS)
    print_(s, B + "boubacar-raincoat-seedlings-cropped-2x.jpg", 200, 150, 680, 820, 0.5, 0.25)
    rrect(s, 60, 60, 620, 72, DEEP, radius=36)
    text(s, 60, 60, 620, 72, "Soil Regenerators in the wild", 28, GLOW, HEAD, True, align="c", anchor="m")
    rect(s, 60, 1030, 960, 250, DEEP, shadow=True)
    sb.tape(s, 110, 1030, 170, 50, -28); sb.tape(s, 970, 1030, 170, 50, 28)
    npt = 60 if text_width("Boubacar Tidiane Diallo,", 60) < 820 else 54
    text(s, 110, 1070, 760, 180, "Boubacar Tidiane Diallo, Guinea", npt, CREAM, HEAD, True, spacing=1.05, anchor="m")
    logo(s, 900, 1170, 90, white=True)
    paper(s, "coffee-cherries-branch", 930, 900, 300, -10)
    paper(s, "leaf-sprig-paper", 130, 260, 200, -20)

    # 2 quote
    s = cream(d, "Quote slide. No microscope photo: Boubacar wrote (reply to Allison) that he does not have a microscope yet, "
                 "and that he sees healthier soil as more earthworms, mushrooms and active decomposition. The cut-paper earthworm, "
                 "mushroom and seedling show those signs. [PHOTO NEEDED: Boubacar on his farm or his mulched soil, which he says he will send]." + CUTS)
    quote_marks(s, 60, 60)
    block(s, 90, 330, 900, "“Today, I ask a different question: What does the soil food web need to thrive?”", 62, DEEP, HEAD, True, 1.1)
    paper(s, "earthworm-paper", 250, 1080, 300, 6)
    paper(s, "mushroom-paper", 600, 1060, 220, -4)
    paper(s, "happy-seedling", 850, 1070, 220, 0)
    paper(s, "leaf-sprig-paper", 980, 820, 170, 25)

    # 3 how he feeds his soil
    s = cream(d, "Photo slide. Main photo: assets/photo/boubacar/boubacar-compost-pile.jpeg (WhatsApp, 17 Aug 2026). Small print: "
                 "assets/photo/boubacar/still-biochar-kiln-smoke-73s.png, from assets/video/boubacar/making-biochar-in-barrel-kiln.mp4 "
                 "(WhatsApp Video 2026-08-17 at 13.46.34) at 1:13." + CUTS)
    print_(s, B + "boubacar-compost-pile.jpeg", 110, 110, 560, 700, 0.5, 0.45)
    print_(s, B + "still-biochar-kiln-smoke-73s.png", 720, 330, 260, 400, 0.5, 0.4)
    paper(s, "earthworm-paper", 850, 190, 200, 10)
    text_box(s, "How he feeds his soil:", "compost, vermicompost, activated biochar, permanent mulch, and cover crops.", 880, 390)
    paper(s, "leaf-sprig-paper", 990, 880, 170, 25)

    # 4 what he grows together
    s = cream(d, "Photo slide. Photo: assets/photo/boubacar/planting-seedling-in-agroforest.jpeg (WhatsApp, 17 Aug 2026). "
                 "[PHOTO NEEDED: coffee growing between cacao, banana and citrus, a still from his YouTube channel]. "
                 "Cut-paper crops: coffee, cacao, banana, citrus, pineapple." + CUTS)
    print_(s, B + "planting-seedling-in-agroforest.jpeg", 110, 110, 520, 690, 0.5, 0.45)
    paper(s, "coffee-cherries-branch", 850, 210, 280, 8)
    paper(s, "cacao-pod", 840, 470, 170, -15)
    paper(s, "banana-bunch", 850, 700, 240, 6)
    text_box(s, "What he grows together:", "coffee, cacao, bananas, citrus, and pineapple, in a syntropic agroforestry system.", 880, 390)
    paper(s, "citrus-orange", 900, 820, 150, -8)
    paper(s, "pineapple", 985, 1230, 150, 10)

    # 5 what he's seeing
    s = cream(d, "Photo slide. Photo: assets/photo/boubacar/still-young-plants-buckets-29s.png, from "
                 "assets/video/boubacar/watering-young-plants-in-buckets.mp4 (WhatsApp Video 2026-08-17 at 13.45.52) at 0:29. "
                 "Low resolution (478 x 850 video). [PHOTO NEEDED: earthworms in his soil, a still from his YouTube channel]." + CUTS)
    print_(s, B + "still-young-plants-buckets-29s.png", 110, 110, 480, 700, 0.5, 0.5)
    paper(s, "earthworm-paper", 820, 260, 300, -6)
    paper(s, "happy-seedling", 780, 560, 200, 0)
    paper(s, "mushroom-paper", 900, 740, 180, 8)
    text_box(s, "What he's seeing:", "more earthworms, better soil structure, better moisture, and stronger young plants.", 880, 390)

    # 6 quote and follow
    s = cream(d, "Quote slide. Photo: assets/photo/boubacar/group-of-five-farmers.jpeg (WhatsApp, 17 Aug 2026). "
                 "Confirm with Boubacar where and when it was taken, and that it shows him with farmers at Gnaly [VERIFY]." + CUTS)
    quote_marks(s, 60, 40, 260)
    y = block(s, 90, 260, 900, "“I am cultivating the life that makes healthy agriculture possible.”", 58, DEEP, HEAD, True, 1.1)
    print_(s, B + "group-of-five-farmers.jpeg", 150, y + 60, 780, 420, 0.5, 0.5)
    t = "Follow him on YouTube: @boubacartidianediallo"
    rrect(s, 60, 1190, 960, 76, GREEN, radius=38)
    text(s, 60, 1190, 960, 76, t, 26, CREAM, HEAD, True, align="c", anchor="m")
    paper(s, "coffee-cherries-branch", 980, y + 80, 200, 20)
    paper(s, "happy-seedling", 110, y + 400, 150, -6)
    logo(s, 1080 - 50 - 110, 50, 110, white=False)
    save(d, "01-10-2026-thu-ig-soil-regenerators-boubacar.pptx")


def linkedin():
    d = Deck(1200, 627, name="01-10-2026-thu-li-boubacar")
    s = d.slide(CREAM, "LinkedIn image. " + SOURCES + " Photo: assets/photo/boubacar/boubacar-compost-pile.jpeg, cropped to landscape: "
                       "compost pile in the lower half, tree canopy above. The WhatsApp file is 810 x 1080, so this crop is upscaled about 1.5x; "
                       "ask Boubacar for the original. No text on the photo.", counter=False)
    p = crop(B + "boubacar-compost-pile.jpeg", 1200, 627, 0.5, 0.28)
    s.shapes.add_picture(p, 0, 0, Emu(1200 * PX), Emu(627 * PX))
    logo(s, 1200 - 30 - 90, 627 - 30 - 81, 90, white=False)
    save(d, "01-10-2026-thu-li-boubacar.pptx")


if __name__ == "__main__":
    instagram(); linkedin()
