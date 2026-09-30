"""Three LinkedIn cover options for the Boubacar post (1200 x 627), in the trifold's visual language:
deep colour panels with a top-to-bottom gradient, tracked uppercase eyebrows, Montserrat headlines,
EB Garamond for the quieter lines, photos cut with a soft curve. No stickers.

python3 build_boubacar_li_options.py  ->  01-10-2026-thu-li-boubacar-option-{a-green,b-blue,c-soil}.pptx
"""
import math, os
from lxml import etree
from pptx.util import Emu
from lib import Deck, rect, text, crop, poly, _place, PX, ROOT, CREAM, GLOW, HEAD
from build_oct_01_10 import logo, save, text_width
from build_boubacar import B, SOURCES

A = "http://schemas.openxmlformats.org/drawingml/2006/main"
SERIF = "EB Garamond"
W, H = 1200, 627
QUOTE = "“Today, I ask a different question: What does the soil food web need to thrive?”"
NOTE = (" Trifold style: gradient panel, tracked eyebrow, Montserrat headline, EB Garamond serif. EB Garamond is in the repo "
        "(assets/font) and in Canva. No stickers. ")


def grad_rect(s, x, y, w, h, c1, c2, ang=90):
    """Rectangle with a linear gradient from c1 to c2 (ang 90 = top to bottom)."""
    r = rect(s, x, y, w, h, c1)
    sp = r._element.spPr
    for e in sp.findall("{%s}solidFill" % A): sp.remove(e)
    g = etree.Element("{%s}gradFill" % A, rotWithShape="1"); lst = etree.SubElement(g, "{%s}gsLst" % A)
    for pos, c in ((0, c1), (100000, c2)):
        gs = etree.SubElement(lst, "{%s}gs" % A, pos=str(pos)); etree.SubElement(gs, "{%s}srgbClr" % A, val=c)
    etree.SubElement(g, "{%s}lin" % A, ang=str(ang * 60000), scaled="0")
    sp.insert(list(sp).index(sp.find("{%s}prstGeom" % A)) + 1, g)
    return r


def photo(s, rel, x, y, w, h, fx=0.5, fy=0.5):
    p = crop(rel, int(w), int(h), fx, fy)
    return s.shapes.add_picture(p, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def curve_edge(s, x0, color, side="left", bulge=60, n=40):
    """Colour shape whose inner edge is a soft curve, laid over a photo edge (like the trifold's curved crops).
    side='left': fills x < curve; the curve runs from x0 at top and bottom to x0 + bulge in the middle."""
    pts = []
    for i in range(n + 1):
        t = i / n; y = t * H
        cx = x0 + bulge * math.sin(math.pi * t)
        pts.append((cx, y))
    if side == "left":
        pts = [(0, H), (0, 0)] + pts
    else:
        pts = [(W, H), (W, 0)] + pts
    return poly(s, pts, color)


def eyebrow(s, x, y, t, color=GLOW, pt=15):
    text(s, x, y, 600, 30, t.upper(), pt, color, HEAD, True, track=3)


def option_a():
    """Food Web Green panel on the left, the portrait on the right behind a curved green edge."""
    d = Deck(W, H, name="01-10-2026-thu-li-boubacar-option-a-green")
    s = d.slide("156826", "Option A, green." + NOTE + SOURCES, counter=False)
    photo(s, B + "boubacar-portrait-bananas.jpg", 560, 0, 640, H, 0.5, 0.42)
    grad_rect(s, 0, 0, 640, H, "156826", "22371F")
    curve_edge(s, 600, "1A4F24", "left", 70)
    eyebrow(s, 70, 80, "Happy International Coffee Day")
    rect(s, 70, 118, 60, 3, GLOW)
    text(s, 70, 140, 600, 150, "Boubacar Tidiane\nDiallo", 44, CREAM, HEAD, True, spacing=1.02)
    text(s, 70, 290, 540, 50, "Guinea-Conakry", 30, GLOW, SERIF, False, italic=True)
    text(s, 70, 370, 500, 130, QUOTE, 22, CREAM, SERIF, False, italic=True, spacing=1.2, alpha=92)
    logo(s, 70, H - 40 - 72, 80, white=True)
    save(d, "01-10-2026-thu-li-boubacar-option-a-green.pptx")


def editorial(name, label, c1, c2, edge, soft):
    """Option B layout (photo left with a curved edge, quote in large serif) in a given colour."""
    d = Deck(W, H, name=name)
    s = d.slide(c1, label + NOTE + "Photo: assets/photo/boubacar/vegetable-beds-by-building.jpeg. " + SOURCES, counter=False)
    grad_rect(s, 0, 0, W, H, c1, c2)
    photo(s, B + "vegetable-beds-by-building.jpeg", 0, 0, 520, H, 0.6, 0.3)
    curve_edge(s, 520, edge, "right", -60)
    eyebrow(s, 560, 70, "Happy International Coffee Day", soft)
    rect(s, 560, 108, 60, 3, soft)
    text(s, 560, 140, 590, 260, QUOTE, 34, CREAM, SERIF, False, italic=True, spacing=1.15)
    text(s, 560, 430, 580, 44, "Boubacar Tidiane Diallo", 28, CREAM, HEAD, True)
    text(s, 560, 474, 580, 40, "Gnaly Coffee & AgroÉcole Bio, Guinea-Conakry", 22, soft, SERIF, False)
    logo(s, W - 40 - 80, H - 40 - 72, 80, white=True)
    save(d, name + ".pptx")


def option_b():
    editorial("01-10-2026-thu-li-boubacar-option-b-blue", "Option B, blue.", "3780B8", "1F4E73", "2E6A9C", "DCEBF7")


def option_b_green():
    editorial("01-10-2026-thu-li-boubacar-option-b-green", "Option B layout, green.", "156826", "22371F", "1A5A25", GLOW)


def option_b_brown():
    editorial("01-10-2026-thu-li-boubacar-option-b-brown", "Option B layout, soil brown.", "5A3B39", "3A2524", "4E3331", "E8CDB8")


def option_c():
    """Soil brown: full-bleed photo with a deep brown gradient from the left, type over it."""
    d = Deck(W, H, name="01-10-2026-thu-li-boubacar-option-c-soil")
    s = d.slide("4F3433", "Option C, soil brown." + NOTE + SOURCES, counter=False)
    photo(s, B + "boubacar-portrait-bananas.jpg", 520, 0, 680, H, 0.5, 0.45)
    # brown panel on the left that fades into the photo
    rect(s, 0, 0, 560, H, "3A2524")
    r = grad_rect(s, 560, 0, 260, H, "3A2524", "3A2524", 0)
    gs = r._element.spPr.find(".//{%s}gsLst" % A).findall("{%s}gs" % A)
    etree.SubElement(gs[1].find("{%s}srgbClr" % A), "{%s}alpha" % A, val="0")
    eyebrow(s, 70, 90, "Happy International Coffee Day", "E8CDB8")
    rect(s, 70, 128, 60, 3, "C89B7B")
    text(s, 70, 150, 600, 150, "Boubacar Tidiane\nDiallo", 44, CREAM, HEAD, True, spacing=1.02)
    text(s, 70, 300, 520, 50, "Guinea-Conakry", 30, "E8CDB8", SERIF, False, italic=True)
    text(s, 70, 370, 470, 60, "Gnaly Coffee & AgroÉcole Bio, Fouta Djallon", 20, CREAM, SERIF, False, alpha=85)
    logo(s, 70, H - 40 - 72, 80, white=True)
    save(d, "01-10-2026-thu-li-boubacar-option-c-soil.pptx")




def option_d():
    """Freestyle: cream field-journal page. Big serif pull quote from his email, two photos stacked on a Deep Green
    column, thin gold rules, one cut-paper coffee branch as the only ornament."""
    from build_oct_01_10 import GRAIN, CUT
    import scrapbook as sb
    d = Deck(W, H, name="01-10-2026-thu-li-boubacar-option-d-journal")
    s = d.slide(CREAM, "Option D, freestyle field journal." + NOTE + "Quote from Boubacar's email to Allison, 30 Sep 2026. Photos: "
                "planting-seedling-in-agroforest.jpeg and boubacar-hand-compost-worm.jpg. " + SOURCES, counter=False)
    s.shapes.add_picture(crop(GRAIN, W, H), 0, 0, Emu(W * PX), Emu(H * PX))
    rect(s, 760, 0, 440, H, "22371F")
    photo(s, B + "planting-seedling-in-agroforest.jpeg", 800, 40, 360, 330, 0.45, 0.45)
    photo(s, B + "boubacar-hand-compost-worm.jpg", 800, 390, 360, 197, 0.4, 0.55)
    eyebrow(s, 70, 64, "Happy International Coffee Day", "156826")
    rect(s, 70, 102, 60, 3, "C9A227")
    text(s, 62, 118, 120, 150, "“", 140, "C9A227", SERIF, False, spacing=0.8)
    text(s, 70, 200, 640, 200, "I now believe that agriculture is biology, not chemical fertilizer.”", 42, "22371F", SERIF, False,
         italic=True, spacing=1.1)
    rect(s, 70, 450, 640, 1.5, "C9A227")
    text(s, 70, 470, 640, 40, "Boubacar Tidiane Diallo", 26, "22371F", HEAD, True)
    text(s, 70, 508, 680, 34, "Gnaly Coffee & AgroÉcole Bio, Fouta Djallon, Guinea-Conakry", 18, "4F3433", SERIF, False)
    sb.cutout(s, CUT + "coffee-cherries-branch-1.png", 700, 120, 120, 20)
    logo(s, 650, H - 24 - 60, 66, white=False)
    save(d, "01-10-2026-thu-li-boubacar-option-d-journal.pptx")




def option_e():
    """Freestyle, after the Eric Feiler welcome card: warm gold with a pale root network, logo top left, black rule,
    big Roboto name, a cream band in Times New Roman, and Boubacar cut out on the right with a soft cream glow."""
    from PIL import Image as PImage
    d = Deck(W, H, name="01-10-2026-thu-li-boubacar-option-e-gold-roots")
    s = d.slide("D9A13E", "Option E, gold roots (style of the SFW 'Welcome Eric Feiler' card). Fonts: Roboto and Times New Roman, as on "
                "that card. Cutout: assets/photo/boubacar/boubacar-portrait-cutout.png, his own photo with the background removed "
                "locally (rembg); nothing generated. Root network: assets/collage/root-network-gold.png, drawn by code. " + SOURCES,
                counter=False)
    rect(s, 0, 0, W, H, "D9A13E")
    s.shapes.add_picture(os.path.join(ROOT, "assets/collage/root-network-gold.png"), 0, 0, Emu(W * PX), Emu(H * PX))
    rect(s, 0, 430, 860, 130, "F6E3C2", alpha=78)
    # cutout: scaled so his waist sits at the bottom edge
    cw, ch = PImage.open(os.path.join(ROOT, B + "boubacar-portrait-cutout.png")).size
    h = 1180; w = h * cw / ch; x = 1200 - w + 20; y = 20
    gw, gh = PImage.open(os.path.join(ROOT, B + "boubacar-portrait-cutout-glow.png")).size
    k = h / ch
    s.shapes.add_picture(os.path.join(ROOT, B + "boubacar-portrait-cutout-glow.png"), Emu(int((x - 40 * k) * PX)), Emu(int((y - 40 * k) * PX)),
                         Emu(int(gw * k * PX)), Emu(int(gh * k * PX)))
    s.shapes.add_picture(os.path.join(ROOT, B + "boubacar-portrait-cutout.png"), Emu(int(x * PX)), Emu(int(y * PX)),
                         Emu(int(w * PX)), Emu(int(h * PX)))
    logo(s, 40, 30, 150, white=False)
    rect(s, 90, 190, 330, 6, "1E1412")
    text(s, 90, 208, 700, 40, "Happy International Coffee Day", 24, "1E1412", "Roboto", False)
    text(s, 86, 250, 760, 170, "Boubacar Tidiane\nDiallo", 58, "1E1412", "Roboto", False, spacing=0.95)
    text(s, 90, 446, 740, 110, "Gnaly Coffee & AgroÉcole Bio\nFouta Djallon, Guinea-Conakry", 28, "1E1412", "Times New Roman", False,
         spacing=1.15)
    save(d, "01-10-2026-thu-li-boubacar-option-e-gold-roots.pptx")


if __name__ == "__main__":
    option_a(); option_b(); option_c(); option_b_green(); option_b_brown(); option_d(); option_e()
