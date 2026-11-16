"""Shop header 2880x1280: generated rainy meadow + fir hills, vintage film grade, real product cut out of the
Printful mockup in the middle, big serif word behind it, white SFW logo bottom right.
Also exports film() to grade any launch image."""
import io, os, sys
import numpy as np
import requests
from PIL import Image, ImageDraw, ImageFilter, ImageFont
from scipy import ndimage as ndi
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "header")
W, H = 2880, 1280
SERIF = "/mnt/skills/examples/canvas-design/canvas-fonts/LibreBaskerville-Regular.ttf"
LOGO = "/home/user/sfw-merch-print-files/creative-code/logos/SFW-logo-flower-white-3000.png"


def film(im, seed=0, fade=.10, grain=9):
    """Vintage film: lifted blacks, softened highlights, olive-warm cast, a little less saturation, grain, soft."""
    rng = np.random.default_rng(seed)
    a = np.asarray(im.convert("RGB"), np.float32) / 255
    g = a.mean(2, keepdims=True); a = g + (a - g) * .82                     # mute colour
    a = fade + a * (1 - fade - .06)                                          # lift blacks, roll off whites
    a *= np.array([1.03, 1.0, .9])                                           # warm olive cast
    a = np.clip(a, 0, 1) ** np.array([1.0, .97, 1.05])
    n = ndi.gaussian_filter(rng.normal(0, 1, a.shape[:2]), .8)[..., None]
    a = a * 255 + n * grain
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    return out.filter(ImageFilter.GaussianBlur(.6))


def background(seed):
    from launch_scenes import run
    p = ("Wide landscape photo of a wet green meadow with tall grass in the foreground, dark fir-covered hills behind "
         "with low mist and low clouds, overcast grey sky, after rain. Shot on vintage 35mm film, faded, slightly muted. "
         "No people, no buildings, no text.")
    return run("black-forest-labs/flux-1.1-pro", {"prompt": p, "aspect_ratio": "custom", "width": 1440, "height": 640, "output_format": "png", "seed": seed, "safety_tolerance": 2})


def cutout(path):
    """Product off its white mockup background: flood-fill the near-white from the edges, keep the rest."""
    im = Image.open(path).convert("RGB"); a = np.asarray(im, np.float32)
    white = (a.min(2) > 236)
    lab, _ = ndi.label(white)
    edge = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]]); edge = edge[edge > 0]
    sizes = ndi.sum(white, lab, range(1, lab.max() + 1))
    big = 1 + np.where(sizes > white.size * .004)[0]                  # big enclosed white areas (tote handle gap)
    bg = np.isin(lab, edge) | np.isin(lab, big)
    keep = ~ndi.binary_opening(bg, iterations=2)
    alpha = ndi.gaussian_filter(keep.astype(np.float32), 1.2)
    rgba = np.dstack([a, alpha * 255]).astype(np.uint8)
    out = Image.fromarray(rgba); return out.crop(out.getbbox())


def header(bg, product, word, name):
    bg = bg.resize((W, int(bg.height * W / bg.width)), Image.LANCZOS)
    bg = bg.crop((0, (bg.height - H) // 2, W, (bg.height - H) // 2 + H)) if bg.height >= H else bg.resize((W, H))
    can = bg.convert("RGBA"); d = ImageDraw.Draw(can)
    f = ImageFont.truetype(SERIF, 520)
    d.text((W / 2, H * .44), word, font=f, fill=(244, 242, 236, 255), anchor="mm")
    p = cutout(product); p.thumbnail((1000, 760), Image.LANCZOS)
    can.alpha_composite(p, ((W - p.width) // 2, H - p.height - 70))
    lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); lg.thumbnail((230, 230), Image.LANCZOS)
    can.alpha_composite(lg, (W - lg.width - 70, H - lg.height - 60))
    return film(can.convert("RGB"), seed=len(name))


def main():
    os.makedirs(OUT, exist_ok=True)
    bgs = []
    for s in (3, 7):
        p = os.path.join(OUT, f"bg-{s}.png")
        if not os.path.exists(p): background(s).save(p)
        bgs.append(Image.open(p).convert("RGB"))
    src = os.path.join(HERE, "source")
    looks = [(0, "logo-cap-oyster", "shop"), (1, "logo-tee-green", "shop"), (0, "mycelium-tote", "merch"), (1, "logo-cap-oyster", "goods")]
    ims = []
    for i, (b, prod, word) in enumerate(looks):
        im = header(bgs[b], os.path.join(src, prod + ".jpg"), word, f"{prod}-{word}")
        im.save(os.path.join(OUT, f"header-{i + 1}-{prod}-{word}.jpg"), quality=93); ims.append(im)
    s = Image.new("RGB", (2 * 1450 + 10, 2 * 650 + 10), "white")
    for i, im in enumerate(ims): s.paste(im.resize((1440, 640)), (10 + (i % 2) * 1450, 10 + (i // 2) * 650))
    s.save(os.path.join(OUT, "contact.jpg"), quality=90)
    # film grade on the cap scenes too
    cap = os.path.join(HERE, "logo-cap-oyster")
    for f in sorted(os.listdir(cap)):
        if f.endswith(".jpg") and "-film" not in f:
            film(Image.open(os.path.join(cap, f)), seed=3).save(os.path.join(cap, f.replace(".jpg", "-film.jpg")), quality=93)


if __name__ == "__main__":
    main()
