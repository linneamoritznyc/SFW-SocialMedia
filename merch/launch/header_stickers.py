"""Shop header 2880x1280: sky photo, products cut out of the real Printful mockups as die-cut stickers (white border,
slight tilt), little soil-life clipart stickers and the full-colour logo sticker scattered around."""
import os, sys
import numpy as np
from PIL import Image, ImageFilter, ImageDraw
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, "/home/user/sfw-merch-print-files/fine-art")
from header import cutout
from launch_fineart import post, wait
import cutouts

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "source"), os.path.join(HERE, "stickers")
W, H = 2880, 1280
LOGO = "/home/user/sfw-merch-print-files/logos/SFW-logo-colour-transparent-3000px.png"
INKS = {"Testate amoeba": (110, 90, 156), "Nematode": (155, 29, 82), "Fungal hyphae": (21, 104, 38), "Springtail": (196, 120, 60),
        "Tardigrade": (60, 111, 168), "Ciliate": (203, 160, 40), "Bacteria": (155, 29, 82), "Mycorrhizal root": (79, 52, 51)}


def sky(seed):
    p = ("Photo looking up at a bright blue sky with soft fluffy white cumulus clouds, summer afternoon, "
         "shot on 35mm film, slightly faded, gentle grain. Only sky, no trees, no birds, no text.")
    return wait(post("https://api.replicate.com/v1/models/black-forest-labs/flux-1.1-pro/predictions", {"input": {
        "prompt": p, "aspect_ratio": "custom", "width": 1440, "height": 640, "output_format": "png", "seed": seed, "safety_tolerance": 2}}))


def sticker(rgba, border, rot, shadow=True):
    """White die-cut border around the alpha, optional soft drop, then rotate."""
    a = np.asarray(rgba).copy(); al = a[..., 3] > 40
    lab, n = ndi.label(al)                                                   # drop stray specks
    if n > 1:
        sz = ndi.sum(al, lab, range(1, n + 1)); keep = np.isin(lab, 1 + np.where(sz > sz.max() * .02)[0])
        a[~keep, 3] = 0; al = keep; rgba = Image.fromarray(a)
    pad = border + 12
    can = np.zeros((a.shape[0] + 2 * pad, a.shape[1] + 2 * pad), bool); can[pad:-pad, pad:-pad] = al
    holes = ndi.binary_fill_holes(can) & ~can; hl, hn = ndi.label(holes)
    if hn:
        hs = ndi.sum(holes, hl, range(1, hn + 1)); can = can | np.isin(hl, 1 + np.where(hs < can.sum() * .01)[0])
    out = ndi.binary_dilation(can, iterations=border)
    out = ndi.gaussian_filter(out.astype(np.float32), 1.2) > .5
    st = Image.new("RGBA", out.shape[::-1], (0, 0, 0, 0))
    st.paste((255, 255, 255, 255), (0, 0), Image.fromarray((out * 255).astype(np.uint8)))
    st.alpha_composite(rgba, (pad, pad))
    st = st.rotate(rot, Image.BICUBIC, expand=True)
    if not shadow: return st
    sh = Image.new("RGBA", (st.width + 30, st.height + 30), (0, 0, 0, 0))
    m = st.split()[3].point(lambda v: int(v * .28)).filter(ImageFilter.GaussianBlur(9))
    sh.paste((20, 40, 70, 255), (14, 18), m); sh.alpha_composite(st, (0, 0))
    return sh


def clip(name, size):
    import io, cairosvg
    d = cutouts.d_of(dict((p[0], p[1]) for p in cutouts.PICTOS)[name]())
    c = "#%02x%02x%02x" % INKS[name]
    png = cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 400 400"><path d="{d}" fill="{c}" fill-rule="evenodd"/></svg>'.encode())
    im = Image.open(io.BytesIO(png)).convert("RGBA"); return im.crop(im.getbbox())


def build(bg, seed):
    rng = np.random.default_rng(seed)
    can = bg.resize((W, H), Image.LANCZOS).convert("RGBA")
    prods = [("logo-tee-green", 620), ("mycelium-tote", 560), ("logo-hoodie-black", 640), ("logo-cap-oyster", 470),
             ("mycelium-tee", 600), ("logo-mug", 430)]
    xs = np.linspace(260, W - 260, len(prods)); order = rng.permutation(len(prods))
    for i in order:
        name, s = prods[i]
        p = cutout(os.path.join(SRC, name + ".jpg")); p.thumbnail((s, s), Image.LANCZOS)
        st = sticker(p, 16, rng.uniform(-9, 9))
        x = int(xs[i] - st.width / 2 + rng.uniform(-40, 40)); y = int(H * .5 - st.height / 2 + rng.uniform(-110, 110))
        can.alpha_composite(st, (x, y))
    lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); lg.thumbnail((300, 300), Image.LANCZOS)
    st = sticker(lg, 14, rng.uniform(-8, 8)); can.alpha_composite(st, (W - st.width - 60, H - st.height - 50))
    return can.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True); ims = []
    for s in (1, 2):
        raw = os.path.join(OUT, f"sky-{s}.png")
        if not os.path.exists(raw): sky(s).save(raw)
        im = build(Image.open(raw).convert("RGB"), s); im.save(os.path.join(OUT, f"header-stickers-{s}.jpg"), quality=94); ims.append(im)
    c = Image.new("RGB", (1450, len(ims) * 650 + 10), "white")
    for i, im in enumerate(ims): c.paste(im.resize((1440, 640)), (5, 5 + i * 650))
    c.save(os.path.join(OUT, "contact.jpg"), quality=90)


if __name__ == "__main__":
    main()
