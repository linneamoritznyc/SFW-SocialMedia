"""Hand-cut paper collage pieces in the SFW brand palette (stacked stones, cut ferns, textured shapes).
Procedural, seeded, so the same pieces come out every run. Run: python3 make_collage.py  -> PNGs with transparent backgrounds."""
import math, os, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageChops
HERE = os.path.dirname(os.path.abspath(__file__))
PAL = dict(green=(49,102,47), deep=(30,63,29), sage=(177,188,177), brown=(76,54,52), tan=(192,157,127), blue=(75,127,180),
           sky=(104,160,206), pale=(215,234,253), cream=(243,241,234), gold=(211,156,72), purple=(101,77,118), leaf=(96,140,84))

def noise(w, h, scale, seed):
    r = np.random.RandomState(seed); small = r.rand(max(2, h // scale), max(2, w // scale)).astype("float32")
    im = Image.fromarray((small * 255).astype("uint8")).resize((w, h), Image.BICUBIC).filter(ImageFilter.GaussianBlur(scale / 3))
    a = np.asarray(im).astype("float32") / 255; return (a - a.min()) / (a.max() - a.min() + 1e-6)

def texture(w, h, color, kind, seed, color2=None):
    r = random.Random(seed); base = np.zeros((h, w, 3), "float32"); base[:] = color
    wash = noise(w, h, 90, seed) - 0.5
    layer = base * (1 + wash[..., None] * 0.30)
    grain = (np.random.RandomState(seed + 7).rand(h, w) - 0.5)[..., None] * 26
    layer = layer + grain
    img = Image.fromarray(np.clip(layer, 0, 255).astype("uint8"))
    d = ImageDraw.Draw(img)
    c2 = color2 or tuple(min(255, int(v * 1.35 + 20)) for v in color)
    if kind == "scribble":                        # crayon hatching
        for _ in range(int(w * h / 900)):
            x = r.randint(-20, w); y = r.randint(-20, h); L = r.randint(60, 200); a = r.uniform(-0.25, 0.25) - math.pi / 2
            d.line([(x, y), (x + L * math.cos(a), y + L * math.sin(a))], fill=c2, width=r.choice([2, 2, 3]))
    elif kind == "dots":
        step = 26
        for yy in range(0, h + step, step):
            for xx in range(0, w + step, step):
                ox = step // 2 if (yy // step) % 2 else 0
                rad = r.uniform(4, 7); d.ellipse((xx + ox - rad, yy - rad, xx + ox + rad, yy + rad), fill=c2)
    elif kind == "lines":                         # wavy print lines
        for yy in range(-10, h + 10, 16):
            pts = [(xx, yy + 6 * math.sin(xx / 30 + yy / 20 + seed)) for xx in range(0, w + 10, 8)]
            d.line(pts, fill=c2, width=3)
    elif kind == "brush":                         # mottled watercolour wash: blotches of a second tone, soft edges
        n1 = noise(w, h, 60, seed + 1); n2 = noise(w, h, 22, seed + 2)
        mask = np.clip((n1 * 0.7 + n2 * 0.3 - 0.5) * 5 + 0.5, 0, 1)[..., None]
        arr = np.asarray(img).astype("float32"); tone = np.array(tuple(int(0.55 * p + 0.45 * q) for p, q in zip(color, c2)), "float32")
        arr = arr * (1 - mask * 0.55) + tone * (mask * 0.55)
        img = Image.fromarray(np.clip(arr, 0, 255).astype("uint8"))
        d = ImageDraw.Draw(img)
        for _ in range(int(h / 40)):                       # a few dry-brush strokes
            y = r.randint(0, h); x0 = r.randint(-100, w // 2); d.line([(x0, y), (x0 + r.randint(w // 3, w), y + r.randint(-8, 8))], fill=c2, width=2)
        img = img.filter(ImageFilter.GaussianBlur(0.8))
    return img

def cut_shape(w, h, seed, n=None, pad=14, round_=0.0):
    """Scissor-cut polygon: straight edges, uneven, roughly filling the box."""
    r = random.Random(seed); n = n or r.randint(8, 13); pts = []
    for i in range(n):
        a = 2 * math.pi * i / n + r.uniform(-0.12, 0.12); k = r.uniform(0.78, 1.0)
        pts.append((w / 2 + (w / 2 - pad) * k * math.cos(a), h / 2 + (h / 2 - pad) * k * math.sin(a)))
    m = Image.new("L", (w * 2, h * 2), 0); ImageDraw.Draw(m).polygon([(x * 2, y * 2) for x, y in pts], fill=255)
    if round_: m = m.filter(ImageFilter.GaussianBlur(round_ * 2)).point(lambda v: 255 if v > 128 else 0)
    return m.resize((w, h), Image.LANCZOS)

def piece(w, h, color, kind, seed, color2=None, **kw):
    tex = texture(w, h, color, kind, seed, color2).convert("RGBA")
    m = cut_shape(w, h, seed, **kw); tex.putalpha(m)
    sh = Image.new("RGBA", (w, h), (0, 0, 0, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.25)))
    out = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0)); out.alpha_composite(sh, (5, 6)); out.alpha_composite(tex, (0, 0)); return out

def stones(seed=3):
    specs = [(360, 190, "green", "scribble"), (270, 110, "deep", "brush"), (430, 190, "tan", "brush"), (230, 100, "brown", "brush"), (300, 250, "cream", "brush"),
             (420, 120, "blue", "lines"), (390, 180, "brown", "scribble"), (250, 160, "sage", "dots")]
    W, H = 520, 1200; out = Image.new("RGBA", (W, H), (0, 0, 0, 0)); y = 20
    for i, (w, h, c, k) in enumerate(specs):
        col = PAL[c]; p = piece(w, h, col, k, seed + i, PAL["cream"] if c in ("deep", "brown") else None, round_=6)
        out.alpha_composite(p, (W // 2 - w // 2 + random.Random(seed + i).randint(-40, 40), y)); y += h - 14
    return out.crop(out.getbbox())

def fern(length=900, seed=5, color=None, leaflets=16):
    """Arched frond: rachis curve with serrated pinnae either side, tapering to the tip."""
    color = color or PAL["green"]; r = random.Random(seed); W, H = length, int(length * 0.62)
    S = 2; m = Image.new("L", (W * S, H * S), 0); d = ImageDraw.Draw(m)
    def P(t): return (40 + t * (W - 80), H * 0.78 - math.sin(t * math.pi * 0.85) * H * 0.62)
    def tang(t):
        x1, y1 = P(min(1, t + 0.01)); x0, y0 = P(max(0, t - 0.01)); L = math.hypot(x1 - x0, y1 - y0) or 1; return (x1 - x0) / L, (y1 - y0) / L
    d.line([(P(i / 80)[0] * S, P(i / 80)[1] * S) for i in range(81)], fill=255, width=9)
    for k in range(leaflets):
        t = 0.06 + 0.90 * k / (leaflets - 1); x, y = P(t); tx, ty = tang(t)
        Lp = H * 0.34 * math.sin(math.pi * (0.10 + 0.90 * (1 - t) ** 0.8)) * r.uniform(0.92, 1.05)
        for side in (-1, 1):
            ang = math.atan2(ty, tx) + side * (1.15 - 0.30 * t) ; dx, dy = math.cos(ang), math.sin(ang)
            ex, ey = x + dx * Lp, y + dy * Lp; nx, ny = -dy, dx; pts = []; steps = 8
            for s_ in range(steps + 1):
                u = s_ / steps; wv = math.sin(math.pi * u ** 0.8) * Lp * 0.17 * (0.6 if s_ % 2 else 1.0)
                pts.append((x + (ex - x) * u + nx * wv, y + (ey - y) * u + ny * wv))
            for s_ in range(steps, -1, -1):
                u = s_ / steps; wv = math.sin(math.pi * u ** 0.8) * Lp * 0.17 * (0.6 if s_ % 2 else 1.0)
                pts.append((x + (ex - x) * u - nx * wv, y + (ey - y) * u - ny * wv))
            d.polygon([(a_ * S, b_ * S) for a_, b_ in pts], fill=255)
    m = m.resize((W, H), Image.LANCZOS); tex = texture(W, H, color, "brush", seed, PAL["leaf"] if color == PAL["green"] else None).convert("RGBA"); tex.putalpha(m)
    sh = Image.new("RGBA", (W, H), (0, 0, 0, 0)); sh.putalpha(m.filter(ImageFilter.GaussianBlur(3)).point(lambda v: int(v * 0.22)))
    out = Image.new("RGBA", (W + 8, H + 8), (0, 0, 0, 0)); out.alpha_composite(sh, (5, 6)); out.alpha_composite(tex, (0, 0)); return out.crop(out.getbbox())

def leafy(seed=11, color=None):
    """Broad-leaf sprig silhouette, cut from one sheet of coloured paper."""
    color = color or PAL["tan"]; W, H = 520, 900; r = random.Random(seed)
    tex = texture(W, H, color, "brush", seed).convert("RGBA"); m = Image.new("L", (W * 2, H * 2), 0); d = ImageDraw.Draw(m)
    d.line([(W, H * 2 - 20), (W - 20, H)] + [(W + 10, 120)], fill=255, width=14)
    for k in range(6):
        y = H * 2 - 200 - k * 260; side = -1 if k % 2 else 1; cx = W + side * 150; ln = 260 - k * 14
        pts = [(W - 10 * side, y), (cx - side * 20, y - ln * 0.55), (cx + side * 90, y - ln * 0.8), (cx + side * 200, y - ln * 0.2), (cx + side * 60, y + ln * 0.12)]
        d.polygon(pts, fill=255)
    m = m.resize((W, H), Image.LANCZOS); tex.putalpha(m); return tex.crop(tex.getbbox())

if __name__ == "__main__":
    stones().save(os.path.join(HERE, "stones-stack.png"))
    fern(900, 5, PAL["green"]).save(os.path.join(HERE, "fern-green.png"))
    fern(800, 9, PAL["sage"]).save(os.path.join(HERE, "fern-sage.png"))
    leafy(11, PAL["tan"]).save(os.path.join(HERE, "leaf-sprig-tan.png"))
    leafy(12, PAL["blue"]).save(os.path.join(HERE, "leaf-sprig-blue.png"))
    for i, (c, k, w, h) in enumerate([("green", "scribble", 520, 720), ("blue", "lines", 460, 560), ("sage", "dots", 420, 420), ("brown", "brush", 520, 300), ("tan", "brush", 600, 420), ("deep", "brush", 520, 380)]):
        piece(w, h, PAL[c], k, 30 + i, PAL["cream"] if c in ("deep", "brown", "blue") else None).save(os.path.join(HERE, f"cut-{c}-{k}.png"))
    print(sorted(f for f in os.listdir(HERE) if f.endswith(".png")))
