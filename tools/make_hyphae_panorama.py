"""One continuous background for a carousel: colour blends from slide to slide and a hyphae network that crosses
every seam, so the slides placed side by side make one design. Cut into one image per slide.

python3 tools/make_hyphae_panorama.py OUT_DIR gold green brown ...   (one colour name per slide)
"""
import math, os, random, sys
from PIL import Image, ImageDraw, ImageFilter

SW, SH = 1080, 1350
C = {"gold": (0xD9, 0xA1, 0x3E), "green": (0x31, 0x66, 0x2F), "brown": (0x4C, 0x36, 0x34),
     "tan": (0xC0, 0x9D, 0x7F), "sage": (0xB1, 0xBC, 0xB1), "blue": (0x4B, 0x7F, 0xB4)}   # brand palette (docs/brand-colors.md)
FINE, MAIN = (250, 232, 196, 125), (252, 238, 210, 165)


def make(out, order, seed=42, clear=()):
    """clear: (slide_number, x0, y0, x1, y1) keep-out boxes (e.g. a logo). Hyphae are routed around them, never faded."""
    n = len(order); W, H = n * SW, SH
    grad = Image.new("RGB", (W, 1)); px = grad.load(); cent = [SW * i + SW / 2 for i in range(n)]
    for x in range(W):
        if x <= cent[0]: c = C[order[0]]
        elif x >= cent[-1]: c = C[order[-1]]
        else:
            i = int((x - SW / 2) // SW); t = (x - cent[i]) / SW
            t = min(1, max(0, (t - 0.3) / 0.4)); t = t * t * (3 - 2 * t)   # flat colour mid-slide, blend at the seam
            a, b = C[order[i]], C[order[i + 1]]; c = tuple(int(a[k] + (b[k] - a[k]) * t) for k in range(3))
        px[x, 0] = c
    bg = grad.resize((W, H)).convert("RGBA")
    net = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(net); random.seed(seed)

    zones = [((n_ - 1) * SW + x0, y0, (n_ - 1) * SW + x1, y1) for n_, x0, y0, x1, y1 in clear]

    def blocked(x, y, m=0):
        return any(zx0 - m <= x <= zx1 + m and zy0 - m <= y <= zy1 + m for zx0, zy0, zx1, zy1 in zones)

    def seg(x, y, nx, ny, w, col):
        d.line([(x, y), (nx, ny)], fill=col, width=max(1, int(w))); r = w / 2; d.ellipse([nx - r, ny - r, nx + r, ny + r], fill=col)

    def branch(x, y, a, w, depth, col):
        if depth == 0 or w < 1.1: return
        for _ in range(random.randint(4, 9)):
            a += random.uniform(-0.28, 0.28); L = random.uniform(14, 26)
            nx, ny = x + math.cos(a) * L, y + math.sin(a) * L
            if blocked(nx, ny, 12): return
            seg(x, y, nx, ny, w, col); x, y = nx, ny; w *= 0.965
        for _ in range(random.choice((2, 2, 3))):
            branch(x, y, a + random.uniform(-1.05, 1.05), w * random.uniform(0.5, 0.78), depth - 1, col)

    for _ in range(n * 12):                       # fine hyphae, spread evenly so every slide is equally busy
        branch(random.uniform(0, W), random.uniform(0, H), random.uniform(0, 2 * math.pi), random.uniform(6, 10), 7, FINE)
    for y0 in (260, 690, 1120):                   # three bold strands that run the full length, across every seam
        x, y, a, w = -40, y0 + random.uniform(-60, 60), random.uniform(-0.2, 0.2), 26
        while x < W + 40:
            a += random.uniform(-0.12, 0.12); a = max(-0.55, min(0.55, a))
            if y < 120: a = abs(a) * 0.6
            if y > H - 120: a = -abs(a) * 0.6
            L = random.uniform(18, 30); nx, ny = x + math.cos(a) * L, y + math.sin(a) * L
            for zx0, zy0, zx1, zy1 in zones:          # route around a logo: bend above or below it
                if zx0 - 160 <= nx <= zx1 + 20 and zy0 - 40 <= ny <= zy1 + 40:
                    up = (zy0 - 50) if (ny - zy0) < (zy1 - ny) and zy0 > 110 else (zy1 + 50)
                    if up < 110: up = zy1 + 50
                    a = math.atan2(up - y, 60); a = max(-1.1, min(1.1, a))
                    nx, ny = x + math.cos(a) * L, y + math.sin(a) * L
            seg(x, y, nx, ny, w, MAIN); x, y = nx, ny; w = 22 + 4 * math.sin(x / 400)
            if random.random() < 0.06 and not blocked(x, y, 80):
                branch(x, y, a + random.choice((-1, 1)) * random.uniform(0.6, 1.4), w * 0.55, 6, MAIN)
    net = net.filter(ImageFilter.GaussianBlur(1.1))
    bg.alpha_composite(net); bg = bg.convert("RGB")
    os.makedirs(out, exist_ok=True)
    bg.save(os.path.join(out, "panorama-full.jpg"), quality=90)
    for i in range(n):
        bg.crop((i * SW, 0, (i + 1) * SW, SH)).save(os.path.join(out, f"slide-{i + 1:02d}.jpg"), quality=92)


if __name__ == "__main__":
    # optional --clear 1:740,60,1000,340 3:... (slide:x0,y0,x1,y1)
    args, clear = sys.argv[2:], []
    if "--clear" in args:
        i = args.index("--clear"); boxes = args[i + 1:]; args = args[:i]
        for b in boxes:
            n_, xy = b.split(":"); clear.append((int(n_), *map(int, xy.split(","))))
    make(sys.argv[1], args, clear=clear)
