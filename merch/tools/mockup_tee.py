"""Flat-lay tee mockups (Stanley/Stella STTU169) at true print scale.

The print files are placed where Printful prints them: the front/back print area is 12 x 16 in
(3600 x 4800 px), the left chest is 3.5 in square. Fabric folds and texture are laid over the
print too, so the ink sits in the cloth. Mockups only; never upload these to Printful.

Usage: python3 mockup_tee.py CANDIDATE_DIR
"""
import io, os, sys
import numpy as np
import cairosvg
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
import sfw

PX = 50                      # mockup px per inch
W, H = 34 * PX, 32 * PX       # canvas
CX, TOP = W / 2, 1.5 * PX     # shoulder line, center
OUT = os.path.join(sfw.ROOT, "mockups")

GARMENTS = [("desert-dust", "light"), ("khaki", "dark"), ("black", "dark")]


def tee_path(back):
    neck = 1.0 if back else 3.3
    pts = (f"M -3.7,0 Q 0,{neck * 1.25:.2f} 3.7,0 L 9.3,1.5 L 15.0,7.6 L 11.9,10.6 L 10.3,9.0 "
           f"L 10.55,28.6 Q 0,29.0 -10.55,28.6 L -10.3,9.0 L -11.9,10.6 L -15.0,7.6 L -9.3,1.5 Z")
    return pts, neck


def svg_tee(hexcol, back):
    d, neck = tee_path(back)
    shade = "#000"
    inner = "" if back else (  # inside of the back collar seen through the front neck
        f'<path d="M -3.7,0 Q 0,1.2 3.7,0 Q 0,{neck * 1.25:.2f} -3.7,0 Z" fill="{hexcol}"/>'
        f'<path d="M -3.7,0 Q 0,1.2 3.7,0 Q 0,{neck * 1.25:.2f} -3.7,0 Z" fill="{shade}" opacity="0.28"/>')
    rib = f'<path d="M -3.7,0 Q 0,{neck * 1.25:.2f} 3.7,0" fill="none" stroke="{shade}" stroke-opacity="0.10" stroke-width="0.75"/>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">'
            f'<g transform="translate({CX},{TOP}) scale({PX})">'
            f'<path d="{d}" fill="{hexcol}"/>{inner}{rib}</g></svg>')


def mask_of(back):
    d, _ = tee_path(back)
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><g transform="translate({CX},{TOP}) scale({PX})">'
           f'<path d="{d}" fill="#fff"/></g></svg>')
    a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).convert("RGBA"))[..., 3]
    return a.astype(np.float32) / 255


def shading(mask, back, seed):
    """Multiply map (1 = no change): edge falloff, sleeve seams, a few soft drape folds, cotton grain."""
    rng = np.random.default_rng(seed)
    dist = ndimage.distance_transform_edt(mask > 0.5) / PX       # inches from the edge
    s = 1 - 0.16 * np.exp(-dist / 0.9)
    img = Image.new("L", (W, H), 128); dr = ImageDraw.Draw(img)
    def P(x, y): return (CX + x * PX, TOP + y * PX)
    # sleeve seams and hem stitching
    for sx in (-1, 1):
        dr.line([P(sx * 9.3, 1.5), P(sx * 10.3, 9.0)], fill=100, width=3)
        dr.line([P(sx * 11.9, 10.25), P(sx * 15.0 - sx * 0.35, 7.95)], fill=110, width=2)
    for x in np.arange(-10.3, 10.3, 0.22):
        dr.line([P(x, 27.75), P(x + 0.11, 27.75)], fill=112, width=2)
    # drape folds: soft dark and light diagonal streaks
    folds = [(-10, 9.5, -5, 15, 96), (10, 9.5, 5.5, 14, 98), (-6, 28, -3, 21, 104), (4, 28, 6.5, 20, 104),
             (-1.5, 6, 1.0, 13, 150), (-8, 18, -6.5, 26, 150)]
    for x0, y0, x1, y1, v in folds:
        dr.line([P(x0, y0), P(x1, y1)], fill=v, width=int(0.5 * PX))
    img = img.filter(ImageFilter.GaussianBlur(0.55 * PX))
    f = np.asarray(img, np.float32) / 128
    grain = ndimage.gaussian_filter(rng.normal(0, 1, (H, W)), 0.7) * 0.035 + 1
    return s * f * grain


def place(base, art_path, x_in, y_in, w_in):
    art = Image.open(art_path).convert("RGBA")
    w = int(round(w_in * PX)); h = int(round(art.height * w / art.width))
    art = art.resize((w, h), Image.LANCZOS)
    base.alpha_composite(art, (int(CX + x_in * PX), int(TOP + y_in * PX)))


def render(hexcol, back, prints, seed):
    base = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg_tee(hexcol, back).encode()))).convert("RGBA")
    for path, x, y, w in prints:
        place(base, path, x, y, w)
    m = mask_of(back)
    a = np.asarray(base).astype(np.float32)
    a[..., :3] *= shading(m, back, seed)[..., None]
    a[..., 3] = m * 255
    tee = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8))
    # soft drop shadow on a studio backdrop
    bg = Image.new("RGBA", (W, H), "#efece6")
    sh = Image.fromarray((m * 70).astype(np.uint8)).filter(ImageFilter.GaussianBlur(14))
    bg.paste(Image.new("RGBA", (W, H), "#3a3226"), (8, 14), sh)
    bg.alpha_composite(tee)
    return bg.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True)
    pf = os.path.join(sfw.ROOT, "print-files")
    back_art = os.path.join(sfw.ROOT, "previews")
    tiles = []
    for i, (gm, scheme) in enumerate(GARMENTS):
        hexcol = sfw.GARMENT[gm]
        # front: left chest 3.5 in square, on the wearer's left (viewer's right), top 3.4 in below the collar
        front = render(hexcol, False, [(os.path.join(pf, f"tee-chest-bacteria-{scheme}.png"), 3.0, 5.2, 3.5)], i)
        # back: 12 x 16 in print area, top 2.0 in below the back collar
        back_file = os.path.join(back_art, f"tee-back-cast-list-{scheme}-MOCKUP-art.png")
        back = render(hexcol, True, [(back_file, -6.0, 3.0, 12.0)], i + 10)
        front.save(os.path.join(OUT, f"tee-{gm}-front.png")); back.save(os.path.join(OUT, f"tee-{gm}-back.png"))
        tiles.append((gm, front, back))
    # one sheet: front and back per colour
    tw = 760; th = int(tw * H / W)
    sheet = Image.new("RGB", (tw * 2 + 60, (th + 60) * len(tiles) + 20), "#efece6")
    d = ImageDraw.Draw(sheet)
    for r, (gm, f, b) in enumerate(tiles):
        y = 20 + r * (th + 60)
        for c, im in enumerate((f, b)):
            sheet.paste(im.resize((tw, th), Image.LANCZOS), (20 + c * (tw + 20), y))
        d.text((30, y + th + 8), f"{gm.replace('-', ' ').title()}: front (left chest)  |  back (cast list)", fill="#4F3433")
    sheet.save(os.path.join(OUT, "tees-all-colours.png"))


if __name__ == "__main__":
    main()
