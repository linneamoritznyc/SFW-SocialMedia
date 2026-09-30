"""Cute science scrapbook kit: taped photo prints, paper notes and stickers drawn as native PowerPoint shapes.
Every sticker is a group of editable shapes with a white die-cut outline, so it can be moved or recoloured in Canva."""
import math, os
from PIL import Image
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE
from lib import _place, rect, rrect, oval, text, crop, Tilt, ROOT, PX, DEEP, GREEN, CREAM, GLOW, LIGHT, INK, FAINT, BODY, HEAD

PAPER, WHITE = "FFFDF7", "FFFFFF"
BROWN, BEAN, BEAN_DK = "4F3433", "6B4430", "3E2517"
LEMON, LEMON_IN, LEAF = "E9B824", "FFE48A", "59A66C"
OUT = 6          # die-cut outline width (px)


class _G:
    def __init__(self, grp, s): self.shapes, self._deck = grp.shapes, s._deck


def group(s):
    g = s.shapes.add_group_shape()
    return g, _G(g, s)


def _sh(r, shadow=False):
    """White die-cut edge on a shape; optional soft shadow."""
    r.line.color.rgb = __import__("pptx.dml.color", fromlist=["RGBColor"]).RGBColor.from_string(WHITE)
    r.line.width = Emu(OUT * PX)
    return r


def shape(s, kind, x, y, w, h, fill, deg=0, line=WHITE, lw=OUT, shadow=False):
    r = rect(s, x, y, w, h, fill, kind=kind, line=line, lw=lw, shadow=shadow)
    if deg: r.rotation = deg
    return r


def tape(s, cx, cy, w=150, h=46, deg=-30):
    rect(s, cx - w / 2, cy - h / 2, w, h, GLOW, alpha=70, tl=Tilt(cx, cy, deg))


def polaroid(s, rel, x, y, size, deg=0, credit="", credit_pt=16, fx=0.5, fy=0.5):
    """Square photo on a paper print, credit written in the bottom margin."""
    b, foot = size * 0.04, max(54, size * 0.11)
    fw, fh = size + 2 * b, size + b + foot
    tl = Tilt(x + fw / 2, y + fh / 2, deg)
    rect(s, x, y, fw, fh, PAPER, tl=tl, shadow=True)
    p = s.shapes.add_picture(crop(rel, int(size), int(size), fx, fy), 0, 0, Emu(1), Emu(1))
    _place(p, x + b, y + b, size, size, tl)
    if credit:
        text(s, x + b, y + b + size, size, foot, credit, credit_pt, FAINT, BODY, align="c", anchor="m", tl=tl)
    return x, y, fw, fh


def note(s, x, y, w, h, fill=PAPER, deg=0, tapes=True):
    tl = Tilt(x + w / 2, y + h / 2, deg)
    rect(s, x, y, w, h, fill, tl=tl, shadow=True)
    if tapes:
        tape(s, x + 60, y + 6, 150, 44, -28); tape(s, x + w - 60, y + 6, 150, 44, 28)
    return tl


def pic(s, rel, x, y, w, deg=0):
    p = os.path.join(ROOT, rel); iw, ih = Image.open(p).size; h = w * ih / iw
    sh = s.shapes.add_picture(p, 0, 0, Emu(1), Emu(1)); _place(sh, x, y, w, h); sh.rotation = deg
    return sh


def cutout(s, rel, cx, cy, w, deg=0):
    """Existing cut-paper PNG cutout, trimmed to its visible pixels and centred."""
    p = os.path.join(ROOT, rel)
    im = Image.open(p).convert("RGBA"); im = im.crop(im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox())
    t = os.path.join(ROOT, "renders", ".tmp"); os.makedirs(t, exist_ok=True)
    tp = os.path.join(t, "trim-" + os.path.basename(rel)); im.save(tp)
    h = w * im.height / im.width
    sh = s.shapes.add_picture(tp, 0, 0, Emu(1), Emu(1)); _place(sh, cx - w / 2, cy - h / 2, w, h); sh.rotation = deg
    return sh


def face(g, cx, cy, k, color=BROWN):
    """Two dot eyes and a small smile."""
    e = 7 * k
    oval(g, cx - 16 * k - e / 2, cy - e / 2, e, e, color); oval(g, cx + 16 * k - e / 2, cy - e / 2, e, e, color)
    sm = shape(g, MSO_SHAPE.BLOCK_ARC, cx - 11 * k, cy + 2 * k, 22 * k, 16 * k, color, 180, line=None)
    sm.adjustments[2] = 0.18


# ---------------------------------------------------------------- stickers
def lemon(s, cx, cy, r, deg=0):
    g, G = group(s)
    shape(G, MSO_SHAPE.OVAL, cx + r * 0.45, cy - r * 1.2, r * 0.9, r * 0.45, LEAF, -35)          # leaf
    shape(G, MSO_SHAPE.OVAL, cx - r, cy - r, 2 * r, 2 * r, LEMON, shadow=True)
    ri = r * 0.8
    oval(G, cx - ri, cy - ri, 2 * ri, 2 * ri, LEMON_IN)
    for k in range(4):                                           # segment lines
        rect(G, cx - ri, cy - 3, 2 * ri, 6, WHITE, tl=Tilt(cx, cy, 45 * k))
    oval(G, cx - r * 0.12, cy - r * 0.12, r * 0.24, r * 0.24, WHITE)
    g.rotation = deg
    return g


def cup(s, cx, cy, w, deg=0, happy=True):
    g, G = group(s)
    shape(G, MSO_SHAPE.OVAL, cx - w * 0.55, cy + w * 0.28, w * 1.1, w * 0.26, PAPER, shadow=True)      # saucer
    shape(G, MSO_SHAPE.DONUT, cx + w * 0.26, cy - w * 0.12, w * 0.3, w * 0.3, PAPER)                  # handle
    shape(G, MSO_SHAPE.ROUNDED_RECTANGLE, cx - w * 0.38, cy - w * 0.25, w * 0.76, w * 0.62, PAPER)    # cup
    rect(G, cx - w * 0.38 + OUT / 2, cy + w * 0.12, w * 0.76 - OUT, w * 0.08, GREEN)                  # green band
    shape(G, MSO_SHAPE.OVAL, cx - w * 0.36, cy - w * 0.32, w * 0.72, w * 0.16, BROWN)                 # coffee
    if happy: face(G, cx, cy - w * 0.02, w / 180)
    for i in (-1, 0, 1):                                                                             # steam
        shape(G, MSO_SHAPE.WAVE, cx + i * w * 0.16 - w * 0.03, cy - w * 0.62, w * 0.06, w * 0.24, "D8D2C4", 90, line=None)
    g.rotation = deg
    return g


def beans(s, cx, cy, w, deg=0):
    g, G = group(s)
    for dx, dy, a in ((-0.3, 0.05, -30), (0.05, -0.12, 20), (0.32, 0.12, 70)):
        x, y = cx + dx * w, cy + dy * w
        shape(G, MSO_SHAPE.OVAL, x - w * 0.2, y - w * 0.13, w * 0.4, w * 0.26, BEAN, a, shadow=True)
        rect(G, x - w * 0.15, y - 2.5, w * 0.3, 5, BEAN_DK, tl=Tilt(x, y, a + 8))
    g.rotation = deg
    return g


def seedling(s, cx, cy, h, sad=False, deg=0):
    """cy is the ground line."""
    g, G = group(s)
    leaf = "A7A45C" if sad else LEAF
    rect(G, cx - 4, cy - h * 0.62, 8, h * 0.62, "7FA05A" if not sad else "9C9A5A")                    # stem
    for side in (-1, 1):
        a = side * (115 if sad else 35)
        lx = cx + side * h * (0.2 if not sad else 0.16); ly = cy - h * (0.66 if not sad else 0.5)
        shape(G, MSO_SHAPE.OVAL, lx - h * 0.2, ly - h * 0.1, h * 0.4, h * 0.2, leaf, a + (0 if side > 0 else 180))
    shape(G, MSO_SHAPE.OVAL, cx - h * 0.5, cy - h * 0.1, h, h * 0.3, BROWN, shadow=True)             # soil mound
    if not sad: face(G, cx, cy + h * 0.03, h / 260, CREAM)
    g.rotation = deg
    return g


def bacterium(s, cx, cy, L, deg=0, fill="BFD8A6"):
    """Cute rod-shaped bacterium with a whippy flagellum and a face."""
    g, G = group(s)
    w = L * 0.42
    # flagellum: a thin wave off the tail
    for i in range(3):                                   # flagellum: a wiggly tail of three small arcs
        shape(G, MSO_SHAPE.ARC, cx - L * 0.5 - (i + 1) * L * 0.16, cy - w * 0.14 + (i % 2) * w * 0.02, L * 0.17, w * 0.26,
              None, 180 * (i % 2), line=GREEN, lw=4)
    r = shape(G, MSO_SHAPE.ROUNDED_RECTANGLE, cx - L / 2, cy - w / 2, L, w, fill, shadow=True)
    r.adjustments[0] = 0.5
    face(G, cx + L * 0.12, cy - w * 0.05, L / 220, DEEP)
    g.rotation = deg
    return g


PH = ["D7392E", "E4592B", "EC7B2A", "F1A12E", "F4C430", "D9D23A", "A8C64A", "6FB24F", "3E9F55", "2F8C6C",
      "2C7C8C", "34659E", "4A4F9E", "5B3E8F", "653079"]      # universal indicator, pH 0 to 14


def ph_strip(s, x, y, w, h=90):
    cw = w / 15
    rect(s, x - 14, y - 14, w + 28, h + 70, PAPER, shadow=True)
    for i, c in enumerate(PH):
        rect(s, x + i * cw, y, cw + 1, h, c)
    for v in (0, 7, 14):
        text(s, x + v * cw - 20, y + h + 6, cw + 40, 40, str(v), 24, INK, HEAD, True, align="c")
    return cw


def pointer(s, cx, y, color=DEEP):
    shape(s, MSO_SHAPE.ISOSCELES_TRIANGLE, cx - 16, y, 32, 26, color, 180, line=None)


def thermometer(s, x, y, h, mark=55, top=80, color="D9A521"):
    """Paper thermometer from 0 (bulb) to `top` °C, filled to `mark`, with its label."""
    tube_w = h * 0.12; bulb = tube_w * 2
    t0, t1 = y + h - bulb * 0.6, y           # 0 °C and `top` °C positions
    ty = lambda c: t0 - (t0 - t1) * c / top
    rrect(s, x, y - 10, tube_w, h - bulb * 0.4, PAPER, radius=tube_w / 2, line=DEEP, lw=3)
    rect(s, x + tube_w * 0.3, ty(mark), tube_w * 0.4, t0 - ty(mark) + bulb * 0.2, color)
    oval(s, x + tube_w / 2 - bulb / 2, y + h - bulb, bulb, bulb, color, line=DEEP, lw=3)
    rect(s, x + tube_w + 4, ty(mark) - 2, 36, 5, DEEP)
    return ty(mark)


def mushroom(s, cx, cy, h, deg=0, cap="B98A5E"):
    """cy is the ground line."""
    g, G = group(s)
    shape(G, MSO_SHAPE.ROUNDED_RECTANGLE, cx - h * 0.14, cy - h * 0.55, h * 0.28, h * 0.55, PAPER, shadow=True)
    shape(G, MSO_SHAPE.CHORD, cx - h * 0.45, cy - h * 0.95, h * 0.9, h * 0.8, cap, 0)
    for dx, dy in ((-0.2, -0.78), (0.12, -0.84), (0.25, -0.7)):
        oval(G, cx + dx * h - h * 0.05, cy + dy * h - h * 0.04, h * 0.1, h * 0.08, PAPER)
    face(G, cx, cy - h * 0.3, h / 300)
    g.rotation = deg
    return g


def beetle(s, cx, cy, L, deg=0, fill="2F4A3A"):
    g, G = group(s)
    for side in (-1, 1):                                   # legs
        for k in (-1, 0, 1):
            rect(G, cx + side * L * 0.28 - (L * 0.18 if side < 0 else 0), cy + k * L * 0.18 - 2, L * 0.18, 4, DEEP,
                 tl=Tilt(cx + side * L * 0.3, cy + k * L * 0.18, side * k * 25))
    shape(G, MSO_SHAPE.OVAL, cx - L * 0.14, cy - L * 0.62, L * 0.28, L * 0.24, DEEP)                 # head
    shape(G, MSO_SHAPE.OVAL, cx - L * 0.3, cy - L * 0.45, L * 0.6, L * 0.85, fill, shadow=True)    # shell
    rect(G, cx - 2, cy - L * 0.42, 4, L * 0.8, WHITE)
    for dx, dy in ((-0.14, -0.15), (0.14, -0.05), (-0.12, 0.15), (0.12, 0.22)):
        oval(G, cx + dx * L - L * 0.04, cy + dy * L - L * 0.04, L * 0.08, L * 0.08, GLOW)
    g.rotation = deg
    return g


def bird(s, cx, cy, L, deg=0, fill="8C6A4E"):
    g, G = group(s)
    shape(G, MSO_SHAPE.ISOSCELES_TRIANGLE, cx - L * 0.62, cy - L * 0.12, L * 0.3, L * 0.22, fill, -90)   # tail
    shape(G, MSO_SHAPE.OVAL, cx - L * 0.45, cy - L * 0.28, L * 0.8, L * 0.56, fill, shadow=True)       # body
    oval(G, cx - L * 0.2, cy - L * 0.02, L * 0.42, L * 0.22, "E8D9C0")                                 # breast
    shape(G, MSO_SHAPE.OVAL, cx - L * 0.28, cy - L * 0.2, L * 0.4, L * 0.24, "6E523B", -15)            # wing
    shape(G, MSO_SHAPE.OVAL, cx + L * 0.12, cy - L * 0.52, L * 0.36, L * 0.36, fill)                   # head
    shape(G, MSO_SHAPE.ISOSCELES_TRIANGLE, cx + L * 0.44, cy - L * 0.4, L * 0.16, L * 0.1, "E0A83A", 90, line=None)
    oval(G, cx + L * 0.3, cy - L * 0.42, L * 0.06, L * 0.06, BROWN)
    for dx in (-0.08, 0.08):
        rect(G, cx + dx * L, cy + L * 0.25, 4, L * 0.16, "E0A83A")
    g.rotation = deg
    return g


def flower(s, cx, cy, r, deg=0, petal="F2CF5B", centre="8C6A4E", stem=True):
    g, G = group(s)
    if stem:
        rect(G, cx - 3, cy, 6, r * 2.6, "7FA05A")
        shape(G, MSO_SHAPE.OVAL, cx + 2, cy + r * 1.3, r * 0.9, r * 0.4, LEAF, -30)
    for k in range(6):
        a = math.radians(60 * k)
        px_, py_ = cx + math.cos(a) * r * 0.62, cy + math.sin(a) * r * 0.62
        shape(G, MSO_SHAPE.OVAL, px_ - r * 0.42, py_ - r * 0.28, r * 0.84, r * 0.56, petal, 60 * k, lw=4)
    shape(G, MSO_SHAPE.OVAL, cx - r * 0.38, cy - r * 0.38, r * 0.76, r * 0.76, centre, lw=4)
    g.rotation = deg
    return g


def coins(s, cx, cy, w, deg=0):
    g, G = group(s)
    for i in range(4):
        shape(G, MSO_SHAPE.OVAL, cx - w / 2, cy - i * w * 0.14, w, w * 0.32, "D9A521", lw=4, shadow=(i == 0))
    oval(G, cx - w * 0.3, cy - 3 * w * 0.14 + w * 0.05, w * 0.6, w * 0.2, "E9C45A")
    g.rotation = deg
    return g


def paper_doc(s, cx, cy, w, deg=0):
    g, G = group(s)
    h = w * 1.3
    shape(G, MSO_SHAPE.RECTANGLE, cx - w / 2, cy - h / 2, w, h, WHITE, line="D8D2C4", lw=3, shadow=True)
    rect(G, cx - w * 0.36, cy - h * 0.38, w * 0.72, h * 0.07, GREEN)
    for i in range(6):
        rect(G, cx - w * 0.36, cy - h * 0.2 + i * h * 0.1, w * (0.72 if i % 3 != 2 else 0.5), 5, "B8B2A4")
    g.rotation = deg
    return g


def magnifier(s, cx, cy, r, deg=-35):
    g, G = group(s)
    rect(G, cx - r * 0.12, cy + r * 0.9, r * 0.24, r * 1.1, BROWN, line=WHITE, lw=OUT)
    shape(G, MSO_SHAPE.DONUT, cx - r, cy - r, 2 * r, 2 * r, DEEP, shadow=True)
    oval(G, cx - r * 0.78, cy - r * 0.78, r * 1.56, r * 1.56, "DDEBF2")
    oval(G, cx - r * 0.5, cy - r * 0.55, r * 0.35, r * 0.2, WHITE)
    g.rotation = deg
    return g


def microscope(s, cx, cy, h, deg=0, body="3E6B5A"):
    """cy is the base line."""
    g, G = group(s)
    shape(G, MSO_SHAPE.ROUNDED_RECTANGLE, cx - h * 0.35, cy - h * 0.1, h * 0.7, h * 0.1, body, shadow=True)       # base
    shape(G, MSO_SHAPE.ROUNDED_RECTANGLE, cx + h * 0.05, cy - h * 0.72, h * 0.14, h * 0.64, body)                 # arm
    rect(G, cx - h * 0.28, cy - h * 0.38, h * 0.5, h * 0.05, DEEP)                                               # stage
    shape(G, MSO_SHAPE.ROUNDED_RECTANGLE, cx - h * 0.2, cy - h * 0.95, h * 0.16, h * 0.5, "D9D2C3", -18)          # tube
    shape(G, MSO_SHAPE.ROUNDED_RECTANGLE, cx - h * 0.27, cy - h * 1.04, h * 0.2, h * 0.1, body, -18)             # eyepiece
    oval(G, cx + h * 0.02, cy - h * 0.62, h * 0.14, h * 0.14, "E0A83A")                                          # knob
    g.rotation = deg
    return g


def pot(G, cx, cy, w, plant="happy"):
    """Terracotta pot with a seedling, drawn into group G. cy is the pot bottom."""
    h = w * 0.8
    shape(G, MSO_SHAPE.TRAPEZOID, cx - w / 2, cy - h, w, h, "C06A3E", 180, lw=4)
    rect(G, cx - w * 0.58, cy - h - h * 0.14, w * 1.16, h * 0.2, "A8552F", line=WHITE, lw=4)
    rect(G, cx - 3, cy - h - w * 0.55, 6, w * 0.45, "7FA05A")
    for side in (-1, 1):
        shape(G, MSO_SHAPE.OVAL, cx + side * w * 0.12 - w * 0.2, cy - h - w * 0.62, w * 0.4, w * 0.22,
              {"herb": "4E8F4F", "flower": "7FA05A"}.get(plant, LEAF), side * 30, lw=3)
    if plant == "flower":
        flower(G, cx, cy - h - w * 0.62, w * 0.14, stem=False)


def seedling_tray(s, cx, cy, w, deg=0):
    """Wooden tray of little pots: vegetable, herb and flower seedlings."""
    g, G = group(s)
    for i, kind in enumerate(("happy", "herb", "flower", "happy")):
        pot(G, cx - w * 0.36 + i * w * 0.24, cy - w * 0.04, w * 0.19, kind)
    shape(G, MSO_SHAPE.RECTANGLE, cx - w / 2, cy - w * 0.08, w, w * 0.16, "B98A5E", shadow=True)
    for k in range(3):
        rect(G, cx - w / 2 + 10, cy - w * 0.05 + k * w * 0.04, w - 20, 3, "8C6A4E")
    g.rotation = deg
    return g
