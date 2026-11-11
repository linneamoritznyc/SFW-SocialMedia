"""SFW merch v2: the Foundation's own microscopy (assets/microscopy/cutout-*.png), one ink, plus type.

Plates: each brightfield cutout is turned into an engraver's line screen. Line thickness follows the
photo's darkness, so the organism is exactly as photographed; nothing is drawn or generated.
Lines are never thinner than 0.5 pt (2.08 px at 300 dpi). One ink for the plate, one for the type.
Fonts: Montserrat 600/700, EB Garamond 400, upright, outlined. No captions or source lines on product.

Usage: python3 merch_v2.py
"""
import io, os, math, json, base64
import numpy as np
import cairosvg
from PIL import Image
import sfw
from sfw import DPI

M = sfw.ROOT
SRC = os.path.join(os.path.dirname(M), "assets", "microscopy")
OUT_PLATES = os.path.join(M, "plates")
W, H = 3600, 4800
PERIOD = 13.0          # line screen period, px (23 lines per inch)
ANGLE = 28             # degrees
MINW = 2.5             # thinnest printed line, px (0.5 pt = 2.08 px)


# ------------------------------------------------------------------ plate: photo -> one-ink line screen
def engrave(name, target_w=None, target_h=None, gamma=0.85):
    """Returns an L-mode mask (255 = ink) of the cutout at print size."""
    im = Image.open(os.path.join(SRC, name)).convert("RGBA")
    im = im.crop(im.split()[-1].getbbox())
    a = np.clip((np.asarray(im.split()[-1], np.float32) / 255 - 0.5) / 0.4, 0, 1)   # drop the soft matte
    g = np.asarray(im.convert("L"), np.float32) / 255
    d = 1 - g
    inside = a > 0.6
    lo, hi = np.percentile(d[inside], 3), np.percentile(d[inside], 99.5)
    d = np.clip((d - lo) / (hi - lo), 0, 1) ** gamma
    s = target_w / im.width if target_w else target_h / im.height
    tw, th = int(round(im.width * s)), int(round(im.height * s))
    up = lambda arr: np.asarray(Image.fromarray(arr.astype(np.float32), "F").resize((tw, th), Image.LANCZOS))
    D = np.clip(up(d), 0, 1) * np.clip(up(a), 0, 1)
    yy, xx = np.mgrid[0:th, 0:tw].astype(np.float32)
    t = math.radians(ANGLE)
    u = xx * math.sin(t) + yy * math.cos(t)
    dist = np.abs((u % PERIOD) - PERIOD / 2)
    width = D * PERIOD
    width = np.where(width < MINW * 0.5, 0, np.maximum(width, MINW))   # drop specks, thicken thin lines
    width = np.where(width > PERIOD - MINW, PERIOD + 1, width)          # close gaps too thin to print
    cover = np.where(width > 0, np.clip(width / 2 - dist + 0.5, 0, 1), 0)
    return Image.fromarray((cover * 255).astype(np.uint8), "L")


def colored(mask, hexcol):
    rgb = tuple(int(hexcol[i:i + 2], 16) for i in (1, 3, 5))
    out = Image.new("RGBA", mask.size, rgb + (0,))
    out.putalpha(mask)
    return out


# ------------------------------------------------------------------ type
def measure(runs):
    """Ink bbox (top, bottom) relative to baseline 0, and total width, for one line of runs."""
    body, x = [], 0
    for text, fontn, size, _col, track in runs:
        d, w, _ = sfw.text(text, fontn, size, x=x, y=0, tracking=track)
        body.append(d); x += w + (size * 0.28 if text and text[-1] != " " else 0)
    width = x - runs[-1][2] * 0.28
    big = max(r[2] for r in runs)
    off, hh = int(2 * big), int(4 * big)
    svg = sfw.svg_doc(int(width + 40), hh, f'<g transform="translate(20,{off})"><path d="{" ".join(body)}"/></g>')
    a = np.asarray(Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode()))).split()[-1])
    ys = np.nonzero(a.max(1) > 40)[0]
    return ys.min() - off, ys.max() - off, width


def type_block(lines, cx, top, gap_lines=0.22 * DPI):
    """lines: list of lists of runs (text, font, size, color, tracking). Centered. Returns svg, bottom."""
    out = []
    y = top
    def top_m(runs):  # cap or ascender height from font metrics
        return max(0.70 * r[2] if r[1].startswith("montserrat") else 0.70 * r[2] for r in runs)
    def bot_m(runs):  # descender room only where lowercase descenders can occur
        return max(0.24 * r[2] if (not r[1].startswith("montserrat") and any(c in r[0] for c in "gjpqy,")) else 0.0 for r in runs)
    prev = None
    for runs in lines:
        t, b, width = measure(runs)
        base = y + top_m(runs)
        x = cx - width / 2
        for text, fontn, size, col, track in runs:
            d, w, _ = sfw.text(text, fontn, size, x=x, y=base, tracking=track)
            out.append(f'<path fill="{col}" d="{d}"/>')
            x += w + size * 0.28
        y = base + max(bot_m(runs), 0.0) + gap_lines
    return "\n".join(out), y - gap_lines


# ------------------------------------------------------------------ designs
G, MS, MB = "garamond-400", "montserrat-600", "montserrat-700"


def plate_place(canvas, mask_rgba, top):
    x = (W - mask_rgba.width) // 2
    canvas.alpha_composite(mask_rgba, (x, int(top)))
    return top + mask_rgba.height


def fit_plate(name, max_w=9 * DPI, max_h=10 * DPI):
    im = Image.open(os.path.join(SRC, name)); bb = im.split()[-1].getbbox()
    w, h = bb[2] - bb[0], bb[3] - bb[1]
    return (max_w, None) if h / w <= max_h / max_w else (None, max_h)


def group_plate(specs, block_w=9 * DPI):
    """Several organisms in one specimen block. specs: (file, rel_w, x_frac, y_px). Returns L mask."""
    masks = [(engrave(f, target_w=rw * block_w), xf, y) for f, rw, xf, y in specs]
    hgt = int(max(y + m.height for m, xf, y in masks))
    canvas = Image.new("L", (int(block_w), hgt), 0)
    for m, xf, y in masks:
        x = int(xf * block_w - m.width / 2)
        canvas.paste(Image.fromarray(np.maximum(np.asarray(canvas.crop((x, y, x + m.width, y + m.height))), np.asarray(m))), (x, y))
    return canvas


def design(key, scheme):
    ink = sfw.SCHEME[scheme]["line"]; acc = sfw.SCHEME[scheme]["accent"]
    canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    top = 0.15 * DPI
    if key == "powered-by-protozoa":
        tw, th = fit_plate("cutout-3.png")
        mask = engrave("cutout-3.png", tw, th)
        y = plate_place(canvas, colored(mask, ink), top) + 0.6 * DPI
        pb = 0.5 * DPI / 0.70                      # cap height 0.5 in
        # "protozoa" 2 in tall (ascender of t to descender of p)
        t_, b_, _ = measure([("protozoa", G, 1000, ink, 0)])
        pz = 2 * DPI / (b_ - t_) * 1000
        lines = [[("POWERED BY", MS, pb, ink, 180)], [("protozoa", G, pz, ink, 0)]]
        svg, bottom = type_block(lines, W / 2, y, gap_lines=0.25 * DPI)
        files = ["cutout-3.png"]
    elif key == "be-the-mycelium":
        # no hyphae in the Foundation's own microscopy yet: type-only until a mycelium image exists
        m = 1.0 * DPI / 0.70 * 0.62
        gsz = m * 1.45
        lines = [[("Be the", G, gsz, ink, 0), ("MYCELIUM", MB, m, acc, 40)],
                 [("you want to see", G, gsz, ink, 0)],
                 [("in the world", G, gsz, ink, 0)]]
        # scale so the widest line is 10 in
        widest = max(measure(l)[2] for l in lines)
        k = 10 * DPI / widest
        lines = [[(t, f, s * k, c, tr) for t, f, s, c, tr in l] for l in lines]
        y = top + 0.5 * DPI
        svg, bottom = type_block(lines, W / 2, y, gap_lines=0.18 * DPI)
        files = []
    elif key == "bunch-of-microbes":
        mask = group_plate([("cutout-3.png", 0.60, 0.5, 0), ("cutout-2.png", 0.36, 0.19, int(2.7 * DPI)),
                            ("cutout-1.png", 0.33, 0.81, int(2.85 * DPI))])
        y = plate_place(canvas, colored(mask, ink), top) + 0.6 * DPI
        m = sfw.fit_size("A BUNCH OF MICROBES?", MB, 9.6 * DPI, 40)
        lines = [[("In the end, aren’t we all just", G, m * 1.12, ink, 0)], [("A BUNCH OF MICROBES?", MB, m, ink, 40)]]
        svg, bottom = type_block(lines, W / 2, y, gap_lines=0.2 * DPI)
        files = ["cutout-3.png", "cutout-2.png", "cutout-1.png"]
    elif key == "under-the-microscope":
        mask = engrave("cutout-1.png", target_w=7 * DPI)     # round specimen: 7 in reads better than 9
        y = plate_place(canvas, colored(mask, ink), top) + 0.6 * DPI
        m = sfw.fit_size("UNDER THE MICROSCOPE", MB, 9.6 * DPI, 40)
        lines = [[("Have you tested it", G, m * 1.5, ink, 0)], [("UNDER THE MICROSCOPE", MB, m, ink, 40)],
                 [("yet?", G, m * 1.5, ink, 0)]]
        svg, bottom = type_block(lines, W / 2, y, gap_lines=0.2 * DPI)
        files = ["cutout-1.png"]
    plate_layer = canvas.copy()
    text_layer = Image.open(io.BytesIO(cairosvg.svg2png(bytestring=sfw.svg_doc(W, H, svg).encode(),
                                                        output_width=W, output_height=H))).convert("RGBA")
    canvas.alpha_composite(text_layer)
    return canvas, plate_layer, svg, files, bottom


def main():
    os.makedirs(OUT_PLATES, exist_ok=True)
    report = {}
    for key in ("powered-by-protozoa", "be-the-mycelium", "bunch-of-microbes", "under-the-microscope"):
        for scheme in ("light", "dark"):
            im, plate_layer, svg, files, bottom = design(key, scheme)
            base = f"tee-front-{key}-{scheme}"
            im.save(os.path.join(M, "print-files", base + ".png"), dpi=(DPI, DPI), optimize=True)
            # source SVG: outlined type plus the one-ink plate as an embedded image
            open(os.path.join(M, "source-svg", base + ".svg"), "w").write(svg_with_plate(svg, plate_layer))
            allowed = [sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]]
            report[base] = {"bottom_in": round(bottom / DPI, 2), "off_palette": len(sfw.palette_check(im, allowed)),
                            "thin_share": round(sfw.thin_line_check(im), 4), "plates": files}
            for gm in (["desert-dust"] if scheme == "light" else ["khaki", "black"]):
                sfw.preview(im, sfw.GARMENT[gm], os.path.join(M, "previews", f"tee-front-{key}-on-{gm}.png"))
    print(json.dumps(report, indent=1))


def svg_with_plate(type_svg, im):
    buf = io.BytesIO(); im.save(buf, "PNG")
    b64 = base64.b64encode(buf.getvalue()).decode()
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{H}" '
            f'viewBox="0 0 {W} {H}">\n<image width="{W}" height="{H}" xlink:href="data:image/png;base64,{b64}"/>\n{type_svg}\n</svg>\n')


if __name__ == "__main__":
    main()
