"""Seamless carousel background, soil cross-section: cream paper above a rolling ground line, brand-brown soil below with
groundcover along the surface and roots and hyphae growing down through it. One wide image, cut into 1080 x 1350 slices,
so the ground, plants and roots run unbroken from slide to slide. Brand colours only (docs/brand-colors.md).

python3 tools/make_soil_panorama.py OUT_DIR N_SLIDES [GROUND_Y]
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter

SW, SH = 1080, 1350
CREAM, BROWN, GREEN, TAN, SAGE = (0xF3, 0xF1, 0xEA), (0x4C, 0x36, 0x34), (0x31, 0x66, 0x2F), (0xC0, 0x9D, 0x7F), (0xB1, 0xBC, 0xB1)


def make(out, n, ground=835, seed=7):
    W, H = n * SW, SH
    random.seed(seed)
    im = Image.new("RGB", (W, H), CREAM)
    # faint paper grain on the cream
    g = Image.effect_noise((W // 4, H // 4), 18).resize((W, H)).filter(ImageFilter.GaussianBlur(1))
    im = Image.blend(im, Image.merge("RGB", [g.point(lambda v: 243 + (v - 128) * 0.05)] * 3), 0.25)
    gy = lambda x: ground + 14 * math.sin(x / 260) + 8 * math.sin(x / 97 + 1.3)      # rolling ground line, continuous
    d = ImageDraw.Draw(im)
    d.polygon([(0, H)] + [(x, gy(x)) for x in range(0, W + 1, 6)] + [(W, H)], fill=BROWN)

    layer = Image.new("RGBA", (W, H), (0, 0, 0, 0)); L = ImageDraw.Draw(layer)

    def seg(x, y, nx, ny, w, col):
        L.line([(x, y), (nx, ny)], fill=col, width=max(1, int(w))); r = w / 2; L.ellipse([nx - r, ny - r, nx + r, ny + r], fill=col)

    def root(x, y, a, w, depth, col):
        if depth == 0 or w < 1: return
        for _ in range(random.randint(4, 8)):
            a += random.uniform(-0.3, 0.3); a = max(0.25, min(math.pi - 0.25, a))     # keep growing downward
            s = random.uniform(12, 22); nx, ny = x + math.cos(a) * s, y + math.sin(a) * s
            if ny > H + 20: return
            seg(x, y, nx, ny, w, col); x, y = nx, ny; w *= 0.95
        for _ in range(random.choice((2, 2, 3))):
            root(x, y, a + random.uniform(-0.9, 0.9), w * random.uniform(0.55, 0.8), depth - 1, col)

    # fine hyphae through the whole soil layer
    for _ in range(n * 26):
        x = random.uniform(0, W); y = random.uniform(ground + 40, H)
        a = random.uniform(0, 2 * math.pi); w = random.uniform(2, 3.5)
        for _ in range(random.randint(8, 20)):
            a += random.uniform(-0.5, 0.5); s = random.uniform(8, 16); nx, ny = x + math.cos(a) * s, y + math.sin(a) * s
            if ny < gy(nx) + 10: break
            seg(x, y, nx, ny, w, SAGE + (70,)); x, y = nx, ny
    # roots from the surface, spaced evenly so every slide gets the same density
    for i in range(n * 9):
        x = (i + random.uniform(0.2, 0.8)) * SW / 9
        root(x, gy(x) + 4, math.pi / 2 + random.uniform(-0.4, 0.4), random.uniform(7, 12), 6, TAN + (120,))
    # soil crumbs
    for _ in range(n * 220):
        x = random.uniform(0, W); y = random.uniform(ground + 30, H); r = random.uniform(1.5, 4)
        L.ellipse([x - r, y - r, x + r, y + r], fill=TAN + (55,))
    # leaf litter along the surface, then a continuous fringe of groundcover
    for x in range(0, W, 3):
        L.line([(x, gy(x) - 2), (x, gy(x) + random.uniform(6, 14))], fill=TAN + (230,), width=3)
    for _ in range(n * 70):
        x = random.uniform(0, W); base = gy(x) + 2; h = random.uniform(18, 46); lean = random.uniform(-0.5, 0.5)
        L.line([(x, base), (x + lean * h, base - h)], fill=GREEN + (255,), width=random.choice((3, 4, 5)))
    im = im.convert("RGBA"); im.alpha_composite(layer.filter(ImageFilter.GaussianBlur(0.8))); im = im.convert("RGB")
    os.makedirs(out, exist_ok=True)
    im.save(os.path.join(out, "panorama-full.jpg"), quality=90)
    for i in range(n):
        im.crop((i * SW, 0, (i + 1) * SW, SH)).save(os.path.join(out, f"slide-{i + 1:02d}.jpg"), quality=92)


if __name__ == "__main__":
    make(sys.argv[1], int(sys.argv[2]), int(sys.argv[3]) if len(sys.argv) > 3 else 835)
