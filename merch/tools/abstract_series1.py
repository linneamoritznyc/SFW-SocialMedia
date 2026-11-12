"""SFW abstract series 1: cubist abstractions of the Foundation's Microbe Library (Google Drive).

Every piece starts from one real micrograph and only rearranges it: facets, wedges, shards, mirrors,
flat tones. Brand colours only, flat, 3000 x 3000 px (10 x 10 in at 300 dpi).
Source micrographs are credited in abstract/CREDITS.md. Commercial use needs each photographer's OK.

Usage: python3 abstract_series1.py LIBRARY_DIR
"""
import math, os, sys
import numpy as np
import cv2
from PIL import Image
from scipy.spatial import Voronoi, Delaunay

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "abstract")
LIB = sys.argv[1]
S = 3000
W = 1500                                    # working size, upscaled at the end
HEX = {"deep": "#22371F", "brown": "#4F3433", "fwgreen": "#156826", "light": "#59A66C", "cream": "#F4F1EA"}
RGB = {k: np.array([int(v[i:i + 2], 16) for i in (1, 3, 5)], np.uint8) for k, v in HEX.items()}
DARK_TO_LIGHT = ["deep", "brown", "fwgreen", "light", "cream"]


def load(name, cx, cy, size):
    im = cv2.imread(os.path.join(LIB, name))
    x0, y0 = int(cx - size / 2), int(cy - size / 2)
    x0 = max(0, min(x0, im.shape[1] - size)); y0 = max(0, min(y0, im.shape[0] - size))
    crop = im[y0:y0 + size, x0:x0 + size]
    return cv2.resize(crop, (W, W), interpolation=cv2.INTER_AREA)


def gray(bgr):
    return cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32) / 255


def levels(g, qs):
    """Quantise g into len(qs)+1 levels at the given quantiles (0 = darkest)."""
    th = np.quantile(g, qs)
    return np.digitize(g, th)


def paint(lv, names):
    out = np.zeros(lv.shape + (3,), np.uint8)
    for i, n in enumerate(names):
        out[lv == i] = RGB[n]
    return out


def reflect(v):
    """Mirror coordinates at the borders (no smeared edge pixels)."""
    p = 2 * (W - 1)
    v = np.mod(v, p)
    return (W - 1 - np.abs(v - (W - 1))).astype(int)


def finish(rgb, name):
    im = Image.fromarray(rgb).resize((S, S), Image.LANCZOS)
    pal = np.stack([RGB[k] for k in DARK_TO_LIGHT]).astype(np.int32)
    a = np.asarray(im).astype(np.int32).reshape(-1, 3)
    idx = np.argmin(((a[:, None, :] - pal[None]) ** 2).sum(-1), 1)
    flat = pal[idx].reshape(S, S, 3).astype(np.uint8)
    Image.fromarray(flat).save(os.path.join(OUT, name + ".png"), dpi=(300, 300), optimize=True)
    return Image.fromarray(flat)


# 1 ---------------------------------------------------------------- facets
def facets(rng):
    src = load("testate-encysting-jimena-fuentes-i2.jpg", 1900, 1373, 2746)
    g = cv2.bilateralFilter(gray(src), 9, 0.08, 7)
    lv = levels(g, [0.10, 0.22, 0.38, 0.62])
    edge = cv2.Sobel(g, cv2.CV_32F, 1, 0) ** 2 + cv2.Sobel(g, cv2.CV_32F, 0, 1) ** 2
    edge = cv2.GaussianBlur(np.sqrt(edge), (0, 0), 3)
    p = (edge ** 1.5 + (edge ** 1.5).mean() * 0.05).ravel(); p /= p.sum()
    n = 5200
    pick = rng.choice(p.size, n, replace=False, p=p)
    pts = np.c_[pick % W, pick // W].astype(float)
    pts = np.vstack([pts, [[-W, -W], [2 * W, -W], [-W, 2 * W], [2 * W, 2 * W]]])
    vor = Voronoi(pts)
    out = np.zeros((W, W, 3), np.uint8)
    names = ["deep", "brown", "fwgreen", "light", "cream"]
    for i, ri in enumerate(vor.point_region[:n]):
        reg = vor.regions[ri]
        if -1 in reg or not reg:
            continue
        poly = np.array([vor.vertices[v] for v in reg], np.int32)
        m = np.zeros((W, W), np.uint8); cv2.fillPoly(m, [poly], 1)
        vals = lv[m.astype(bool)]
        if vals.size == 0:
            continue
        out[m.astype(bool)] = RGB[names[int(np.bincount(vals).argmax())]]
    return finish(out, "01-facets-testate-amoeba")


# 2 ---------------------------------------------------------------- wedges (radial fracture)
def wedges(rng):
    src = load("stellate-amoeba-jimena-fuentes.jpg", 2040, 1432, 1700)
    g = gray(src)
    detail = g - cv2.GaussianBlur(g, (0, 0), 12)              # local contrast keeps the fine axopodia
    body = cv2.GaussianBlur(g, (0, 0), 3)
    v = np.abs(detail) * 3 + (body.mean() - body).clip(0) * 2
    lv = levels(v, [0.80, 0.93, 0.975])                        # most of the field stays dark
    c = W / 2
    yy, xx = np.mgrid[0:W, 0:W].astype(np.float32)
    r = np.hypot(xx - c, yy - c); th = np.arctan2(yy - c, xx - c)
    K = 10
    k = ((th + math.pi) / (2 * math.pi) * K).astype(int) % K
    rot = np.where(k % 2 == 0, 1, -1) * np.radians(rng.uniform(12, 24, K))[k]
    sc = np.where(k % 3 == 0, 1.25, np.where(k % 3 == 1, 0.82, 1.0))
    sx = reflect(c + r * sc * np.cos(th + rot))
    sy = reflect(c + r * sc * np.sin(th + rot))
    L = lv[sy, sx]
    a = paint(L, ["deep", "fwgreen", "light", "cream"])
    b = paint(L, ["cream", "light", "brown", "deep"])
    out = np.where((k % 2 == 0)[..., None], a, b)
    edge = cv2.Canny(k.astype(np.uint8) * 20, 1, 2) > 0
    out[cv2.dilate(edge.astype(np.uint8), np.ones((3, 3))) > 0] = RGB["brown"]
    return finish(out, "02-wedges-stellate-amoeba")


# 3 ---------------------------------------------------------------- shards (multiple viewpoints)
def shards(rng):
    src = load("nematode-molting-cameron-radman.jpg", 1700, 1300, 2700)
    g = cv2.bilateralFilter(gray(src), 9, 0.06, 7)
    d = g - cv2.GaussianBlur(g, (0, 0), 25)
    lv = levels(-d, [0.55, 0.85, 0.95])                        # 0 = calm field ... 3 = strongest structure
    pts = np.vstack([rng.uniform(0, W, (11, 2)), [[0, 0], [W, 0], [0, W], [W, W], [W / 2, 0], [0, W / 2], [W, W / 2], [W / 2, W]]])
    tri = Delaunay(pts)
    yy, xx = np.mgrid[0:W, 0:W].astype(np.float32)
    simplex = tri.find_simplex(np.c_[xx.ravel(), yy.ravel()]).reshape(W, W)
    out = np.zeros((W, W, 3), np.uint8)
    schemes = [["cream", "light", "brown", "deep"], ["deep", "fwgreen", "light", "cream"], ["brown", "fwgreen", "cream", "cream"]]
    for s in range(len(tri.simplices)):
        m = simplex == s
        if not m.any():
            continue
        a = math.radians(rng.uniform(-24, 24)); k = rng.uniform(0.85, 1.3)
        cx, cy = W / 2 + rng.normal(0, W * .06), W / 2 + rng.normal(0, W * .06)
        x, y = xx[m] - W / 2, yy[m] - W / 2
        sx = reflect(cx + (x * math.cos(a) - y * math.sin(a)) / k)
        sy = reflect(cy + (x * math.sin(a) + y * math.cos(a)) / k)
        names = schemes[s % 3]
        out[m] = np.stack([RGB[n] for n in names])[lv[sy, sx]]
    edges = cv2.Canny((simplex % 251).astype(np.uint8), 0, 1) > 0
    out[cv2.dilate(edges.astype(np.uint8), np.ones((3, 3))) > 0] = RGB["cream"]
    return finish(out, "03-shards-nematode")


# 4 ---------------------------------------------------------------- lines (mite)
def mite_lines(rng):
    src = load("mite-talbot-armstrong-i3.jpg", 1690, 1100, 1944)
    g = cv2.bilateralFilter(gray(src), 9, 0.08, 7)
    e = cv2.Canny((g * 255).astype(np.uint8), 18, 45)
    e = cv2.dilate(e, np.ones((2, 2)), iterations=1) > 0
    dark = cv2.GaussianBlur(g, (0, 0), 6) < np.quantile(g, 0.12)
    out = np.zeros((W, W, 3), np.uint8); out[:] = RGB["deep"]
    out[dark] = RGB["fwgreen"]
    out[e] = RGB["cream"]
    return finish(out, "04-lines-mite")


# 5 ---------------------------------------------------------------- mirrored medallion
def medallion(rng):
    im = cv2.imread(os.path.join(LIB, "testate-encysted-robert-kenyon.jpg"))
    q = im[200:870, 330:1000]                                 # the theca with its round cyst
    q = cv2.resize(q, (W // 2, W // 2), interpolation=cv2.INTER_CUBIC)
    g = cv2.bilateralFilter(gray(q), 9, 0.07, 5)
    d = g - cv2.GaussianBlur(g, (0, 0), 14)
    lv = levels(-d * 2 + (g.mean() - g), [0.5, 0.78, 0.92])
    tile = paint(lv, ["cream", "light", "fwgreen", "brown"])
    top = np.hstack([tile, tile[:, ::-1]])
    out = np.vstack([top, top[::-1]])
    return finish(out, "05-medallion-testate-amoeba")


# 6 ---------------------------------------------------------------- flat five-tone screenprint
def screenprint(rng):
    src = load("fungal-spore-josia-martens.jpg", 2204, 1717, 3400)
    g = cv2.bilateralFilter(gray(src), 15, 0.1, 9)
    g = cv2.medianBlur((g * 255).astype(np.uint8), 7).astype(np.float32) / 255
    d = g - cv2.GaussianBlur(g, (0, 0), 10)
    spore = cv2.GaussianBlur(g, (0, 0), 4) < np.quantile(g, 0.05)
    out = np.zeros((W, W, 3), np.uint8); out[:] = RGB["cream"]
    bg = levels(-np.abs(d), [0.06, 0.16])                          # debris as two light tones
    out[bg == 0] = RGB["fwgreen"]; out[bg == 1] = RGB["light"]
    inner = levels(d[spore], [0.35, 0.75])                          # walls dark, cells mid, highlights light
    out[spore] = np.stack([RGB["deep"], RGB["brown"], RGB["light"]])[inner]
    return finish(out, "06-screenprint-fungal-spore")


def main():
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(1104)
    pieces = [facets(rng), wedges(rng), shards(rng), mite_lines(rng), medallion(rng), screenprint(rng)]
    th, pad = 600, 24
    sheet = Image.new("RGB", (3 * th + 4 * pad, 2 * th + 3 * pad), tuple(RGB["cream"]))
    for k, p in enumerate(pieces):
        sheet.paste(p.resize((th, th), Image.LANCZOS), (pad + (k % 3) * (th + pad), pad + (k // 3) * (th + pad)))
    sheet.save(os.path.join(OUT, "series-1-sheet.png"))


if __name__ == "__main__":
    main()
