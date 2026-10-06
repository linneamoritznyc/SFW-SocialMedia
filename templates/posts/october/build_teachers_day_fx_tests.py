"""World Teachers' Day: ten versions of the Loida and Casey slide, each trying one of the Canva techniques Linnea listed
(6 Oct 2026). All keep Stephanie's layout (two people, bunting, new logo), her titles, the scratched-paper texture and
soil version B along the bottom. Every effect is drawn here (PIL), saved as a PNG, and placed as its own movable layer.

 1 ripped paper      photos pasted on torn paper scraps with masking tape
 2 gold brush        a painted gold brush stroke behind each name
 3 light leak        warm light leaking in from the top-right corner, plus film grain
 4 blurry gradient   soft brand-colour gradient blobs behind everything at about 40%
 5 gradient fade     photos fade out on their right edge into the paper, text overlaps the fade
 6 halftone          green halftone dots rising from the soil and fading out
 7 sparkles          a few small gold sparkles around the names
 8 arch frames       photos in arch-shaped frames
 9 drop shadow       photos lifted off the page with soft shadows and white borders
10 terrazzo          brand-colour terrazzo chips under the scratched paper

python3 templates/posts/october/build_teachers_day_fx_tests.py
"""
import os, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageChops, ImageFont
from lib import Deck, rect, text, Tilt, ROOT
from photos import crop
from build_oct_01_10 import logo, pic, save
from build_teachers_day_v2 import para, zoomed
from build_teachers_day_v3 import base, bunting, GREEN, GOLD, BROWN, INK, W, H, NOTE
from build_teachers_day_v4 import ORDER, soil

FX = os.path.join(ROOT, "renders", ".tmp", "fx"); os.makedirs(FX, exist_ok=True)
PAIR = [next(m for m in ORDER if m[0] == "Loida"), next(m for m in ORDER if m[0] == "Casey")]
CELL, X0, Y0, GAP = 470, 80, 190, 40
TX, TW = 595, 420
rgb = lambda h: tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def out(name): return os.path.join(FX, name)


def photo_img(m, size):
    p = zoomed(m[5]); return Image.open(crop(p, size, size, 0.5, 0.35)).convert("RGBA")


def names(s, m, y, color=GREEN, shadow=False):
    """Name and title only, same size, font and words as soil version B (Linnea, 6 Oct 2026: do not change the text)."""
    yy = para(s, TX, y + CELL / 2 - 70, TW, f"{m[0]} {m[1]}", (44, 40, 36), color, "Montserrat", True, sp=1.0, maxh=130) + 12
    para(s, TX, yy, TW, m[2], (26, 24), INK, "Source Sans 3", maxh=120)


def plain_photo(s, m, y):
    pic(s, os.path.relpath(save_img(photo_img(m, CELL * 2), f"p-{m[0]}.png"), ROOT), X0, y, CELL, CELL)


def save_img(im, name):
    p = out(name); im.save(p); return p


def rel(p): return os.path.relpath(p, ROOT)


# ---------------------------------------------------------------- effect assets
def torn_paper(w, h, seed):
    random.seed(seed); pad = 30
    im = Image.new("RGBA", (w + 2 * pad, h + 2 * pad), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    pts = []
    for side in range(4):
        n = 60
        for i in range(n):
            t = i / n; j = random.uniform(-9, 9)
            x, y = [(pad + t * w, pad + j), (pad + w + j, pad + t * h), (pad + w - t * w, pad + h + j), (pad + j, pad + h - t * h)][side]
            pts.append((x, y))
    d.polygon(pts, fill=(252, 250, 244, 255))
    sh = im.split()[3].filter(ImageFilter.GaussianBlur(10)).point(lambda v: int(v * .35))
    o = Image.new("RGBA", im.size, (0, 0, 0, 0)); o.paste((70, 55, 45, 255), (6, 10), sh); o.alpha_composite(im)
    return o


def tape(w=150, h=44):
    im = Image.new("RGBA", (w, h), (220, 229, 200, 185)); d = ImageDraw.Draw(im)
    for x in (0, w - 1):
        for y in range(0, h, 4): d.rectangle([x - 2, y, x + 2, y + 2], fill=(0, 0, 0, 0))
    return im


def brush_stroke(w, h, color, seed):
    random.seed(seed); S = 2
    im = Image.new("RGBA", (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for k in range(70):                                   # many dry-brush bristle lines along the stroke
        y = random.gauss(h * S / 2, h * S * .2); x0 = random.uniform(0, w * S * .08); x1 = w * S - random.uniform(0, w * S * .12)
        a = random.randint(60, 140); wd = random.randint(4, 10)
        pts = [(x0 + (x1 - x0) * t, y + math.sin(t * 3 + k) * 6 + random.uniform(-2, 2)) for t in [i / 30 for i in range(31)]]
        d.line(pts, fill=rgb(color) + (a,), width=wd)
    return im.filter(ImageFilter.GaussianBlur(1.2)).resize((w, h), Image.LANCZOS)


def light_leak():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for cx, cy, r, c, a in [(W + 60, -80, 700, (245, 190, 110), 150), (W - 120, 120, 380, (255, 225, 170), 120),
                            (W + 40, 520, 300, (235, 150, 90), 70)]:
        blob = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(blob).ellipse([cx - r, cy - r, cx + r, cy + r], fill=c + (a,))
        im.alpha_composite(blob.filter(ImageFilter.GaussianBlur(r * .45)))
    return im


def film_grain(a=26):
    random.seed(5); im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); px = im.load()
    for _ in range(120000):
        x, y = random.randrange(W), random.randrange(H); v = random.choice([(255, 255, 255), (40, 30, 25)])
        px[x, y] = v + (random.randint(8, a),)
    return im


def blurry_gradient():
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for cx, cy, r, c in [(150, 300, 420, "6AA46F"), (950, 420, 380, "D39C48"), (300, 1100, 420, "B1BCB1"),
                         (900, 1000, 360, "654D76"), (560, 700, 300, "C09D7F")]:
        blob = Image.new("RGBA", (W, H), (0, 0, 0, 0)); ImageDraw.Draw(blob).ellipse([cx - r, cy - r, cx + r, cy + r], fill=rgb(c) + (110,))
        im.alpha_composite(blob.filter(ImageFilter.GaussianBlur(170)))
    return im


def fade_right(img, start=.55):
    w, h = img.size; g = Image.linear_gradient("L").rotate(90).resize((w, h))      # 255 left -> 0 right
    g = g.point(lambda v: 255 if v > 255 * (1 - start) else int(v / (1 - start)))
    a = ImageChops.multiply(img.split()[3], g); img.putalpha(a); return img


def halftone(color="31662F", h=520):
    im = Image.new("RGBA", (W, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im); step = 18
    for y in range(0, h, step):
        for x in range(0, W + step, step):
            t = y / h; r = step * .5 * t ** 1.6
            ox = step / 2 if (y // step) % 2 else 0
            if r > .6: d.ellipse([x + ox - r, y - r, x + ox + r, y + r], fill=rgb(color) + (150,))
    return im


def sparkle(size, color=GOLD):
    S = 4; im = Image.new("RGBA", (size * S, size * S), (0, 0, 0, 0)); d = ImageDraw.Draw(im); c = size * S / 2
    pts = []
    for i in range(8):
        a = math.pi / 4 * i; r = c if i % 2 == 0 else c * .22
        pts.append((c + r * math.cos(a - math.pi / 2), c + r * math.sin(a - math.pi / 2)))
    d.polygon(pts, fill=rgb(color) + (255,))
    return im.resize((size, size), Image.LANCZOS)


def arch(img):
    w, h = img.size; m = Image.new("L", (w, h), 0); d = ImageDraw.Draw(m)
    d.rectangle([0, w / 2, w, h], fill=255); d.ellipse([0, 0, w, w], fill=255)
    img.putalpha(m); return img


def lifted(img, border=16):
    w, h = img.size; pad = 40
    o = Image.new("RGBA", (w + 2 * border + 2 * pad, h + 2 * border + 2 * pad), (0, 0, 0, 0))
    sh = Image.new("L", o.size, 0); ImageDraw.Draw(sh).rectangle([pad + 8, pad + 14, pad + w + 2 * border + 8, pad + h + 2 * border + 14], fill=110)
    o.paste((40, 30, 25, 255), (0, 0), sh.filter(ImageFilter.GaussianBlur(14)))
    ImageDraw.Draw(o).rectangle([pad, pad, pad + w + 2 * border, pad + h + 2 * border], fill=(252, 251, 247, 255))
    o.alpha_composite(img, (pad + border, pad + border)); return o, pad + border


def terrazzo():
    random.seed(8); im = Image.new("RGBA", (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for _ in range(260):
        cx, cy = random.uniform(0, W), random.uniform(0, H); r = random.uniform(5, 18)
        c = random.choice(["31662F", "D39C48", "B1BCB1", "C09D7F", "654D76", "4C3634"])
        pts = [(cx + r * random.uniform(.5, 1.2) * math.cos(a), cy + r * random.uniform(.5, 1.2) * math.sin(a))
               for a in [i * 2 * math.pi / 6 + random.uniform(-.3, .3) for i in range(6)]]
        d.polygon(pts, fill=rgb(c) + (70,))
    return im


# ---------------------------------------------------------------- slides
def slide(d, n, title):
    s = base(d, f"Version {n}: {title}." + NOTE); return s


def finish(s, n):
    bunting(s); logo(s, W - 40 - 120, 1040, 120, white=False); soil(s, 1)


def build():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-fx-tests")
    ys = [Y0, Y0 + CELL + GAP]

    s = slide(d, 1, "ripped paper")
    for i, (m, y) in enumerate(zip(PAIR, ys)):
        deg = [-2.5, 2][i]
        tp = save_img(torn_paper(CELL + 30, CELL + 30, i), f"torn{i}.png"); pic(s, rel(tp), X0 - 45, y - 45, CELL + 90, deg=deg)
        pic(s, rel(save_img(photo_img(m, CELL * 2), f"p{i}.png")), X0, y, CELL, CELL, deg=deg)
        tpp = save_img(tape(), "tape.png"); pic(s, rel(tpp), X0 + CELL / 2 - 75, y - 28, 150, 44, deg=deg - 4)
        names(s, m, y)
    finish(s, 1)

    s = slide(d, 2, "gold brush stroke")
    for i, (m, y) in enumerate(zip(PAIR, ys)):
        plain_photo(s, m, y)
        bp = save_img(brush_stroke(440, 110, GOLD, i), f"brush{i}.png")
        sh = pic(s, rel(bp), TX - 30, y + CELL / 2 - 20, 440, 110)          # under the lower half of the name
        names(s, m, y)
    finish(s, 2)

    s = slide(d, 3, "light leak and film grain")
    for m, y in zip(PAIR, ys): plain_photo(s, m, y); names(s, m, y)
    finish(s, 3)
    pic(s, rel(save_img(light_leak(), "leak.png")), 0, 0, W, H); pic(s, rel(save_img(film_grain(), "grain.png")), 0, 0, W, H)

    s = slide(d, 4, "blurry brand gradient")
    pic(s, rel(save_img(blurry_gradient(), "blurgrad.png")), 0, 0, W, H)
    for m, y in zip(PAIR, ys): plain_photo(s, m, y); names(s, m, y)
    finish(s, 4)

    s = slide(d, 5, "gradient fade on the photos")
    for i, (m, y) in enumerate(zip(PAIR, ys)):
        im = Image.open(crop(zoomed(m[5]), 1160, 940, 0.5, 0.35)).convert("RGBA")
        pic(s, rel(save_img(fade_right(im), f"fade{i}.png")), 0, y, 580, 470)
        names(s, m, y)
    finish(s, 5)

    s = slide(d, 6, "halftone dots")
    pic(s, rel(save_img(halftone(), "halftone.png")), 0, H - 520, W, 520)
    for m, y in zip(PAIR, ys): plain_photo(s, m, y); names(s, m, y)
    finish(s, 6)

    s = slide(d, 7, "gold sparkles")
    for m, y in zip(PAIR, ys): plain_photo(s, m, y); names(s, m, y)
    sp = rel(save_img(sparkle(80), "sparkle.png"))
    for x, y, sz in [(565, 300, 44), (1000, 230, 30), (590, 840, 30), (990, 760, 46), (540, 660, 22), (1020, 950, 24)]:
        pic(s, sp, x - sz / 2, y - sz / 2, sz, sz)
    finish(s, 7)

    s = slide(d, 8, "arch frames")
    for i, (m, y) in enumerate(zip(PAIR, ys)):
        pic(s, rel(save_img(arch(photo_img(m, CELL * 2)), f"arch{i}.png")), X0, y, CELL, CELL)
        names(s, m, y)
    finish(s, 8)

    s = slide(d, 9, "drop shadow and white border")
    for i, (m, y) in enumerate(zip(PAIR, ys)):
        im, off = lifted(photo_img(m, CELL - 32)); p = save_img(im, f"lift{i}.png")
        pic(s, rel(p), X0 - off + 16, y - off + 16, im.width, deg=[-1.5, 1.2][i])
        names(s, m, y)
    finish(s, 9)

    s = slide(d, 10, "brand terrazzo")
    pic(s, rel(save_img(terrazzo(), "terrazzo.png")), 0, 0, W, H)
    for m, y in zip(PAIR, ys): plain_photo(s, m, y); names(s, m, y)
    finish(s, 10)

    save(d, "05-10-2026-mon-ig-teachers-day-fx-tests.pptx")


if __name__ == "__main__":
    build()
