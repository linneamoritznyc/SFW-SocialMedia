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
