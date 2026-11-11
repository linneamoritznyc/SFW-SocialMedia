"""Shared tools for SFW merch print files.

- Text is shaped with HarfBuzz (real kerning) and converted to outlines with fontTools,
  so no font is needed to print the SVG.
- Recraft SVG parts are rendered at their real print size, the white paper is dropped,
  every line thinner than 0.5 pt is thickened, and the result is traced back to one
  single-color vector path (so each part is exactly one allowed ink).
"""
import io, os, re, math, functools
import numpy as np
import cairosvg, uharfbuzz as hb, potrace
from PIL import Image
from fontTools.ttLib import TTFont
from fontTools.varLib import instancer
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from scipy import ndimage

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # merch/
FONT_DIR = os.path.join(os.path.dirname(ROOT), "assets", "font")
CACHE = os.path.join(ROOT, "tools", ".font-cache")

DPI = 300
PT = DPI / 72.0                 # px per point
MIN_LINE_PX = 0.5 * PT          # 0.5 pt = 2.08 px at 300 dpi

INK = {
    "soil-brown": "#4F3433", "deep-green": "#22371F", "food-web-green": "#156826",
    "light-green": "#59A66C", "cream": "#F4F1EA",
}
GARMENT = {
    "desert-dust": "#dcccb4", "khaki": "#6E6B4D", "black": "#111111",
    "oyster-tote": "#edcea5", "jungle": "#928355", "oyster-cap": "#f3e6cf",
}
# light garments: brown lines + Food Web Green accent; dark garments: cream + Light Green
SCHEME = {
    "light": {"line": INK["soil-brown"], "accent": INK["food-web-green"]},
    "dark": {"line": INK["cream"], "accent": INK["light-green"]},
}


# ---------------------------------------------------------------- fonts
@functools.lru_cache(None)
def font(name):
    """name: montserrat-800, montserrat-600, source-sans-400, source-sans-400-italic"""
    os.makedirs(CACHE, exist_ok=True)
    out = os.path.join(CACHE, name + ".ttf")
    if not os.path.exists(out):
        if name == "garamond-400":
            f = TTFont(os.path.join(FONT_DIR, "eb-garamond-latin-400-normal.woff2"))
        elif name.startswith("montserrat"):
            f = TTFont(os.path.join(FONT_DIR, "montserrat-latin-variable.woff2"))
            f = instancer.instantiateVariableFont(f, {"wght": int(name.split("-")[1])})
        else:
            f = TTFont(os.path.join(FONT_DIR, f"source-sans-3-latin-{name.split('-', 2)[2]}-normal.woff2"
                                    if not name.endswith("italic") else
                                    os.path.join(FONT_DIR, "source-sans-3-latin-400-italic.woff2")))
        f.flavor = None
        f.save(out)
    tt = TTFont(out)
    blob = hb.Blob.from_file_path(out)
    return tt, hb.Font(hb.Face(blob))


def text(s, fontname, size, x=0, y=0, tracking=0, anchor="start"):
    """Return (svg path d, width, info) for string s, baseline at y.
    size in px (font size, em), tracking in 1/1000 em."""
    tt, hbf = font(fontname)
    upem = tt["head"].unitsPerEm
    buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
    hb.shape(hbf, buf, {"kern": True, "liga": True})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    sc = size / upem; track = tracking / 1000 * upem
    pen_x = 0; parts = []; n = len(buf.glyph_infos)
    pos = []
    for i, (info, p) in enumerate(zip(buf.glyph_infos, buf.glyph_positions)):
        pos.append((order[info.codepoint], pen_x + p.x_offset, p.y_offset))
        pen_x += p.x_advance + (track if i < n - 1 else 0)
    width = pen_x * sc
    if anchor == "middle": x -= width / 2
    elif anchor == "end": x -= width
    for gname, gx, gy in pos:
        sp = SVGPathPen(gs)
        gs[gname].draw(TransformPen(sp, (sc, 0, 0, -sc, x + gx * sc, y - gy * sc)))
        parts.append(sp.getCommands())
    os2 = tt["OS/2"]
    return " ".join(parts), width, {"cap": os2.sCapHeight * sc, "x": os2.sxHeight * sc,
                                    "asc": tt["hhea"].ascent * sc, "desc": -tt["hhea"].descent * sc}


def text_width(s, fontname, size, tracking=0):
    return text(s, fontname, size, tracking=tracking)[1]


def fit_size(s, fontname, width, tracking=0):
    return width / text_width(s, fontname, 100, tracking) * 100


# ---------------------------------------------------------------- parts
def _disk(r):
    r = int(round(r)); y, x = np.ogrid[-r:r + 1, -r:r + 1]
    return x * x + y * y <= r * r


def part(svg_path, max_w, max_h, k=4, min_line=MIN_LINE_PX, dark_thresh=0.55, drop_blobs=False):
    """Vectorize a generated part at print size.
    Returns dict(d=path in local px coords at print size, w, h, stats)."""
    svg = open(svg_path).read()
    vb = [float(v) for v in re.search(r'viewBox="([^"]+)"', svg).group(1).split()]
    # first pass: find ink bbox at low res
    lo = _raster(svg, 512, int(512 * vb[3] / vb[2]))
    ys, xs = np.nonzero(lo < dark_thresh)
    bx0, bx1, by0, by1 = xs.min(), xs.max() + 1, ys.min(), ys.max() + 1
    fx0, fy0 = bx0 / lo.shape[1], by0 / lo.shape[0]
    fw, fh = (bx1 - bx0) / lo.shape[1], (by1 - by0) / lo.shape[0]
    aspect = (fw * vb[2]) / (fh * vb[3])
    w, h = (max_w, max_w / aspect) if max_w / aspect <= max_h else (max_h * aspect, max_h)
    # hi-res render of the full image so the crop lands at w*k x h*k
    full_w, full_h = int(round(w * k / fw)), int(round(h * k / fh))
    hi = _raster(svg, full_w, full_h)
    cx0, cy0 = int(round(fx0 * full_w)), int(round(fy0 * full_h))
    m = hi[cy0:cy0 + int(round(h * k)), cx0:cx0 + int(round(w * k))] < dark_thresh
    if drop_blobs:  # remove compact filled shapes (stray organisms next to a line drawing)
        lab, n = ndimage.label(m)
        for i, sl in enumerate(ndimage.find_objects(lab), 1):
            comp = lab[sl] == i
            solid = ndimage.binary_fill_holes(comp).mean()
            hh, ww = comp.shape
            if comp.size > (6 * k) ** 2 and solid > 0.5 and max(hh, ww) / min(hh, ww) < 2.5:
                m[sl][comp] = False
    m = np.pad(m, 4 * k)
    before = m.sum()
    # thicken only what is thinner than min_line
    r = min_line * k / 2
    opened = ndimage.binary_opening(m, structure=_disk(r))
    thin = m & ~opened
    m = m | ndimage.binary_dilation(thin, structure=_disk(r))
    added = (m.sum() - before) / max(before, 1)
    bm = potrace.Bitmap(~m)   # potracer traces values below blacklevel, so ink must be False
    plist = bm.trace(turdsize=int((min_line * k) ** 2 / 2), opttolerance=0.4)
    off = 4 * k
    d = _plist_to_d(plist, 1 / k, -off / k)
    return {"d": d, "w": w, "h": h, "thickened_share": round(float(added), 3), "mask": m, "k": k}


def _raster(svg, w, h):
    png = cairosvg.svg2png(bytestring=svg.encode(), output_width=w, output_height=h, background_color="white")
    return np.asarray(Image.open(io.BytesIO(png)).convert("L"), dtype=np.float32) / 255


def _plist_to_d(plist, s, o):
    f = lambda p: f"{p.x * s + o:.2f},{p.y * s + o:.2f}"
    out = []
    for curve in plist:
        out.append("M" + f(curve.start_point))
        for seg in curve.segments:
            if seg.is_corner:
                out.append("L" + f(seg.c) + "L" + f(seg.end_point))
            else:
                out.append("C" + f(seg.c1) + " " + f(seg.c2) + " " + f(seg.end_point))
        out.append("Z")
    return "".join(out)


def save_part_svg(p, path, color="#000000"):
    with open(path, "w") as fh:
        fh.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {p["w"]:.1f} {p["h"]:.1f}" '
                 f'width="{p["w"]:.1f}" height="{p["h"]:.1f}"><path fill="{color}" fill-rule="evenodd" d="{p["d"]}"/></svg>')


# ---------------------------------------------------------------- layout helpers
def g(d, fill, tx=0, ty=0, scale=1, rot=0, cx=0, cy=0):
    t = f"translate({tx:.2f},{ty:.2f})"
    if rot: t += f" rotate({rot},{cx},{cy})"
    if scale != 1: t += f" scale({scale})"
    return f'<path transform="{t}" fill="{fill}" fill-rule="evenodd" d="{d}"/>'


def slide_label(cx, top, line1, line2, color):
    """The shared slide label, 2.2 x 0.6 in, thin rule, with SOIL FOOD WEB under it.
    Returns (svg, bottom_y)."""
    W, H = 2.2 * DPI, 0.6 * DPI
    rule = 0.75 * PT
    x0 = cx - W / 2
    out = [f'<rect x="{x0 + rule/2:.2f}" y="{top + rule/2:.2f}" width="{W - rule:.2f}" height="{H - rule:.2f}" '
           f'fill="none" stroke="{color}" stroke-width="{rule:.2f}"/>']
    size = 10.5 * PT
    for s, fn, base in ((line1, "source-sans-400-italic", top + H * 0.44), (line2, "source-sans-400", top + H * 0.80)):
        d, w, _ = text(s, fn, size)
        if w > W - 40:  # shrink to fit inside the rule
            d, w, _ = text(s, fn, size * (W - 40) / w)
        d, w, _ = text(s, fn, size * min(1, (W - 40) / w), x=cx, y=base, anchor="middle")
        out.append(f'<path fill="{color}" d="{d}"/>')
    sfw_size = 7 * PT
    d, w, info = text("SOIL FOOD WEB", "montserrat-600", sfw_size, x=cx, y=top + H + 0.16 * DPI + sfw_size * 0.7,
                      tracking=120, anchor="middle")
    out.append(f'<path fill="{color}" d="{d}"/>')
    return "\n".join(out), top + H + 0.16 * DPI + sfw_size * 0.7


def svg_doc(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}">\n'
            f'{body}\n</svg>\n')


def export_png(svg_str, path, w, h):
    png = cairosvg.svg2png(bytestring=svg_str.encode(), output_width=w, output_height=h)
    im = Image.open(io.BytesIO(png)).convert("RGBA")
    im.save(path, dpi=(DPI, DPI), optimize=True)
    return im


def preview(im, garment_hex, path, pad=0.08, width=1200):
    """Flat preview: the design on a rectangle of the garment color."""
    W = int(im.width * (1 + 2 * pad)); H = int(im.height * (1 + 2 * pad))
    bg = Image.new("RGBA", (W, H), garment_hex)
    bg.alpha_composite(im, (int(im.width * pad), int(im.height * pad)))
    bg = bg.convert("RGB")
    bg.thumbnail((width, width * 4))
    bg.save(path)
    return bg


def palette_check(im, allowed_hex):
    """Every pixel with alpha > 0 must be one of the allowed inks (antialiasing only
    changes alpha, never color, because each path has one flat fill)."""
    a = np.asarray(im).astype(int)
    rgb = a[..., :3][a[..., 3] > 64]            # ignore the faintest antialias pixels (rounding)
    allowed = np.array([[int(h[i:i + 2], 16) for i in (1, 3, 5)] for h in allowed_hex])
    dist = np.abs(rgb[:, None, :] - allowed[None, :, :]).max(-1).min(-1)
    bad = rgb[dist > 4]
    return {tuple(c) for c in np.unique(bad, axis=0)} if len(bad) else set()


def thin_line_check(im, min_px=MIN_LINE_PX):
    """Share of ink pixels that sit in features thinner than min_px."""
    m = np.asarray(im)[..., 3] > 127
    opened = ndimage.binary_opening(m, structure=_disk((min_px - 0.5) / 2))
    return float((m & ~opened).sum() / max(m.sum(), 1))


def text_arc(s, fontname, size, cx, cy, radius, center_deg, tracking=0, bottom=False):
    """Outlined text along a circle. center_deg: 0 = top, clockwise. Top text sits outside its baseline
    (reads clockwise); bottom text reads left to right with letters standing toward the center.
    radius = baseline radius."""
    tt, hbf = font(fontname)
    upem = tt["head"].unitsPerEm
    buf = hb.Buffer(); buf.add_str(s); buf.guess_segment_properties()
    hb.shape(hbf, buf, {"kern": True})
    gs = tt.getGlyphSet(); order = tt.getGlyphOrder()
    sc = size / upem; track = tracking / 1000 * upem
    glyphs, x = [], 0
    infos = list(zip(buf.glyph_infos, buf.glyph_positions))
    for i, (info, p) in enumerate(infos):
        adv = p.x_advance + (track if i < len(infos) - 1 else 0)
        glyphs.append((order[info.codepoint], x, p.x_advance))
        x += adv
    total = x * sc
    span = math.degrees(total / radius)
    out = []
    for gname, gx, adv in glyphs:
        mid = (gx + adv / 2) * sc
        if not bottom:
            ang = center_deg - span / 2 + math.degrees(mid / radius)
            rot = ang
        else:
            ang = center_deg + span / 2 - math.degrees(mid / radius)
            rot = ang - 180
        a = math.radians(ang)
        px, py = cx + radius * math.sin(a), cy - radius * math.cos(a)
        sp = SVGPathPen(gs)
        gs[gname].draw(TransformPen(sp, (sc, 0, 0, -sc, -adv / 2 * sc, 0)))
        out.append(f'<path transform="translate({px:.2f},{py:.2f}) rotate({rot:.3f})" d="{sp.getCommands()}"/>')
    return "".join(out), span
