"""SFW seamless vector patterns from the Microbe Library.

Motifs are traced (potrace) from real micrographs and only mirrored or repeated; the geometry around
them (tile frames, dots, stripes, scallops) is plain construction, like a knit or block-print repeat.

P1 jacquard   two-colour square tile, mirrored cyst medallion + dotted frame (knit-shirt style)
P2 blockprint half-drop of scalloped cream medallions on a dense ground traced from soil debris
P3 trim       striped border band with a dotted knit line

Output per pattern in merch/patterns/: <name>-tile.svg (vector), <name>-tile.png (300 dpi), <name>-repeat.png (3 x 3)
Usage: python3 patterns.py LIBRARY_DIR
"""
import io, math, os, sys
import numpy as np
import cv2, cairosvg, potrace
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "patterns")
LIB = sys.argv[1]
C = {"deep": "#22371F", "brown": "#4F3433", "fwgreen": "#156826", "light": "#59A66C", "cream": "#F4F1EA"}


# ------------------------------------------------------------------ tracing
def trace(mask, scale=1.0, ox=0.0, oy=0.0, turd=6):
    """Binary mask (True = ink) -> SVG path d, in mask pixels * scale + offset."""
    bm = potrace.Bitmap(~mask)
    pl = bm.trace(turdsize=turd, opttolerance=0.3)
    f = lambda p: f"{p.x * scale + ox:.1f},{p.y * scale + oy:.1f}"
    out = []
    for cv in pl:
        out.append("M" + f(cv.start_point))
        for s in cv.segments:
            out.append(("L" + f(s.c) + "L" + f(s.end_point)) if s.is_corner else
                       ("C" + f(s.c1) + " " + f(s.c2) + " " + f(s.end_point)))
        out.append("Z")
    return "".join(out)


def gray(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255


def cyst_quadrant(size):
    """Top-left quadrant of Robert Kenyon's encysted testate amoeba, centred on the cyst, as ink masks."""
    im = cv2.imread(os.path.join(LIB, "testate-encysted-robert-kenyon.jpg"))
    cx, cy, h = 683, 492, 175                                   # cyst centre and half-size in the original
    crop = im[cy - h:cy + h, cx - h:cx + h]
    crop = cv2.resize(crop, (2 * size, 2 * size), interpolation=cv2.INTER_CUBIC)
    g = cv2.bilateralFilter(gray(crop), 9, 0.07, 5)
    d = g - cv2.GaussianBlur(g, (0, 0), size / 18)
    dark = (-d) > np.quantile(-d, 0.80)                         # walls, rims, granules
    dark = cv2.morphologyEx(dark.astype(np.uint8), cv2.MORPH_OPEN, np.ones((3, 3))).astype(bool)
    yy, xx = np.mgrid[0:2 * size, 0:2 * size]
    r = np.hypot(xx - size, yy - size)
    dark &= r < size * 0.98                                     # round medallion
    return dark[:size, :size]


def mirrored(d_quadrant, cx, cy, q):
    """Four copies of a quadrant path mirrored about (cx, cy). Quadrant drawn in [0, q]."""
    tf = [f"translate({cx - q},{cy - q})",
          f"translate({cx + q},{cy - q}) scale(-1,1)",
          f"translate({cx - q},{cy + q}) scale(1,-1)",
          f"translate({cx + q},{cy + q}) scale(-1,-1)"]
    return tf


def svg(w, h, body):
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n{body}\n</svg>\n'


def save(name, s, w, h, tiles=3):
    open(os.path.join(OUT, f"{name}-tile.svg"), "w").write(s)
    png = cairosvg.svg2png(bytestring=s.encode(), output_width=w, output_height=h)
    tile = Image.open(io.BytesIO(png)).convert("RGB")
    tile.save(os.path.join(OUT, f"{name}-tile.png"), dpi=(300, 300), optimize=True)
    rep = Image.new("RGB", (w * tiles, h * tiles))
    for i in range(tiles):
        for j in range(tiles):
            rep.paste(tile, (i * w, j * h))
    rep.thumbnail((1500, 1500))
    rep.save(os.path.join(OUT, f"{name}-repeat.png"))
    return rep


# ------------------------------------------------------------------ P1 jacquard tile
def jacquard(ink="deep", ground="cream", T=1200):
    q = int(T * 0.36)
    quad = cyst_quadrant(q)
    d = trace(quad)
    cx = cy = T / 2
    body = [f'<rect width="{T}" height="{T}" fill="{C[ground]}"/>']
    body += [f'<path transform="{t}" d="{d}" fill="{C[ink]}" fill-rule="evenodd"/>' for t in mirrored(d, cx, cy, q)]
    # frame: a band shared by neighbouring tiles (half on each edge), two rules and a row of diamonds
    band = T * 0.075
    for edge in ("h", "v"):
        for pos in (0, T):
            if edge == "h":
                body.append(f'<rect x="0" y="{pos - band / 2}" width="{T}" height="{band}" fill="{C[ground]}"/>')
                for off in (-band / 2, band / 2):
                    body.append(f'<rect x="0" y="{pos + off - 4}" width="{T}" height="8" fill="{C[ink]}"/>')
            else:
                body.append(f'<rect x="{pos - band / 2}" y="0" width="{band}" height="{T}" fill="{C[ground]}"/>')
                for off in (-band / 2, band / 2):
                    body.append(f'<rect x="{pos + off - 4}" y="0" width="8" height="{T}" fill="{C[ink]}"/>')
    n = 12
    r = band * 0.26
    for k in range(n):
        t = (k + 0.5) * T / n
        for x, y in ((t, 0), (t, T), (0, t), (T, t)):
            body.append(f'<path d="M{x},{y - r}L{x + r},{y}L{x},{y + r}L{x - r},{y}Z" fill="{C[ink]}"/>')
    # corner cross where four tiles meet
    for x, y in ((0, 0), (T, 0), (0, T), (T, T)):
        R = band * 0.9
        body.append(f'<path d="M{x},{y - R}L{x + R * .35},{y - R * .35}L{x + R},{y}L{x + R * .35},{y + R * .35}L{x},{y + R}'
                    f'L{x - R * .35},{y + R * .35}L{x - R},{y}L{x - R * .35},{y - R * .35}Z" fill="{C[ink]}"/>')
    return save(f"p1-jacquard-{ink}-on-{ground}", svg(T, T, "\n".join(body)), T, T)


# ------------------------------------------------------------------ P2 block print, half drop
def ground_texture(T):
    """Seamless debris texture from Josia Martens' spore slide: a patch mirrored 2 x 2 (mirrors tile seamlessly)."""
    im = cv2.imread(os.path.join(LIB, "fungal-spore-josia-martens.jpg"))
    patch = im[200:1700, 2900:4400]                              # debris field, away from the spore
    g = gray(cv2.resize(patch, (T // 2, T // 2), interpolation=cv2.INTER_AREA))
    d = g - cv2.GaussianBlur(g, (0, 0), 6)
    m = np.abs(d) > np.quantile(np.abs(d), 0.84)
    m = cv2.morphologyEx(m.astype(np.uint8), cv2.MORPH_OPEN, np.ones((2, 2))).astype(bool)
    top = np.hstack([m, m[:, ::-1]])
    return np.vstack([top, top[::-1]])


def scallop(cx, cy, R, lobes=12, depth=0.07):
    pts = []
    for t in np.linspace(0, 2 * math.pi, 360, endpoint=False):
        r = R * (1 - depth * (0.5 - 0.5 * math.cos(lobes * t)))
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t)))
    return "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + "Z"


def blockprint(T=1500):
    tex = ground_texture(T)
    body = [f'<rect width="{T}" height="{T}" fill="{C["deep"]}"/>',
            f'<path d="{trace(tex, turd=4)}" fill="{C["light"]}" fill-rule="evenodd"/>']
    q = int(T * 0.15)
    d = trace(cyst_quadrant(q))
    R = T * 0.205
    # half drop: medallions at the corners and the centre (brick layout repeats seamlessly)
    centres = [(0, 0), (T, 0), (0, T), (T, T), (T / 2, T / 2)]
    for cx, cy in centres:
        body.append(f'<path d="{scallop(cx, cy, R)}" fill="{C["cream"]}"/>')
        body.append(f'<path d="{scallop(cx, cy, R * 0.86)}" fill="none" stroke="{C["fwgreen"]}" stroke-width="7"/>')
        body += [f'<path transform="{t}" d="{d}" fill="{C["deep"]}" fill-rule="evenodd"/>' for t in mirrored(d, cx, cy, q)]
    # small four-dot rosettes between medallions
    for cx, cy in ((T / 2, 0), (0, T / 2), (T, T / 2), (T / 2, T)):
        for a in range(4):
            x = cx + 26 * math.cos(a * math.pi / 2); y = cy + 26 * math.sin(a * math.pi / 2)
            body.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="15" fill="{C["cream"]}"/>')
    return save("p2-blockprint", svg(T, T, "\n".join(body)), T, T)


# ------------------------------------------------------------------ P3 trim
def trim(W=1200, H=300):
    body = [f'<rect width="{W}" height="{H}" fill="{C["deep"]}"/>',
            f'<rect y="{H * .18}" width="{W}" height="{H * .14}" fill="{C["cream"]}"/>',
            f'<rect y="{H * .68}" width="{W}" height="{H * .14}" fill="{C["cream"]}"/>']
    n = 24
    for k in range(n):
        x = (k + .5) * W / n
        body.append(f'<rect x="{x - 9}" y="{H * .44}" width="18" height="{H * .12}" fill="{C["light"]}"/>')
    return save("p3-trim", svg(W, H, "\n".join(body)), W, H, tiles=3)


def main():
    os.makedirs(OUT, exist_ok=True)
    reps = [jacquard("deep", "cream"), jacquard("cream", "fwgreen"), blockprint(), trim()]
    th = 620; pad = 24
    sheet = Image.new("RGB", (3 * th + 4 * pad, th + 2 * pad + 240), "#F4F1EA")
    for k, r in enumerate(reps[:3]):
        t = r.copy(); t.thumbnail((th, th)); sheet.paste(t, (pad + k * (th + pad), pad))
    t = reps[3].copy(); t = t.resize((3 * th + 2 * pad, 200)); sheet.paste(t, (pad, th + 2 * pad))
    sheet.save(os.path.join(OUT, "patterns-sheet.png"))


if __name__ == "__main__":
    main()
