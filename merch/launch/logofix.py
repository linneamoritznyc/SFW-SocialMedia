"""Replace the AI-redrawn logo on a light product (cap, mug, tote) with the real full-colour SFW logo.
Finds the light product body, finds the dark logo blob on its front, fills it with the fabric colour, then sets the
real logo in, takes on the fabric shading and grain so it reads as printed or embroidered."""
import os, sys
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage as ndi

LOGO = "/home/user/sfw-merch-print-files/logos/SFW-logo-colour-transparent-3000px.png"


def fix(path, out, logo_scale=1.05, debug=None, box=None):
    im = Image.open(path).convert("RGB"); a = np.asarray(im, np.float32); h, w = a.shape[:2]
    L = a.mean(2); sat = a.max(2) - a.min(2)
    if box:
        return place_box(im, a, L, box, out)
    light = (L > np.quantile(L, .80)) & (sat < 60)
    light = ndi.binary_opening(light, iterations=3)
    lab, n = ndi.label(light)
    if not n: return False
    sizes = ndi.sum(light, lab, range(1, n + 1))
    top = set(np.unique(lab[: int(h * .08)])) | set(np.unique(lab[:, 0])) | set(np.unique(lab[:, -1]))
    for t in top:
        if t: sizes[t - 1] = 0                                                # mist and sky touch the top or sides
    body = lab == (1 + int(np.argmax(sizes)))
    body = ndi.binary_fill_holes(ndi.binary_closing(body, iterations=8))
    ys, xs = np.where(body); y0, y1, x0, x1 = ys.min(), ys.max(), xs.min(), xs.max()
    med = np.median(L[body & light])
    dark = body & ((L < med - 40) | (a[..., 1] - a[..., 0] > 18) | (a[..., 0] - a[..., 1] > 28))
    # logo sits on the upper front, within the middle of the body
    roi = np.zeros_like(dark); cy0, cy1 = y0 + int((y1 - y0) * .12), y0 + int((y1 - y0) * .62)
    cx0, cx1 = x0 + int((x1 - x0) * .2), x0 + int((x1 - x0) * .8); roi[cy0:cy1, cx0:cx1] = True
    dark &= roi
    dark = ndi.binary_closing(dark, iterations=6)
    lab2, n2 = ndi.label(dark)
    if not n2: return False
    s2 = ndi.sum(dark, lab2, range(1, n2 + 1)); blob = lab2 == (1 + int(np.argmax(s2)))
    by, bx = np.where(blob); ly0, ly1, lx0, lx1 = by.min(), by.max(), bx.min(), bx.max()
    cx, cy = (lx0 + lx1) / 2, (ly0 + ly1) / 2; size = max(ly1 - ly0, lx1 - lx0) * logo_scale
    # erase old logo: fill with blurred fabric colour (keeps shading)
    hole = ndi.binary_dilation(blob, iterations=int(size * .08) + 3)
    fab = a.copy(); fab[hole] = np.nan
    for _ in range(40):
        m = np.isnan(fab[..., 0])
        if not m.any(): break
        blur = np.stack([ndi.generic_filter(np.nan_to_num(fab[..., c], nan=0), np.mean, size=3) for c in range(3)], 2) if False else None
        f2 = np.where(np.isnan(fab), 0, fab); wgt = (~np.isnan(fab[..., 0])).astype(np.float32)
        num = np.stack([ndi.uniform_filter(f2[..., c], 9) for c in range(3)], 2); den = ndi.uniform_filter(wgt, 9)[..., None]
        fill = num / np.maximum(den, 1e-6)
        fab = np.where(np.isnan(fab) & (den > .05), fill, fab)
    fab = np.nan_to_num(fab, nan=med)
    shade = ndi.gaussian_filter(L, 25); shade = shade / max(shade[hole].mean(), 1)
    # set the real logo in
    lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); s = int(size)
    lg = lg.resize((s, int(s * lg.height / lg.width)), Image.LANCZOS)
    la = np.asarray(lg, np.float32); px, py = int(cx - lg.width / 2), int(cy - lg.height / 2)
    out_a = fab.copy()
    sl = (slice(max(py, 0), min(py + lg.height, h)), slice(max(px, 0), min(px + lg.width, w)))
    ls = (slice(sl[0].start - py, sl[0].stop - py), slice(sl[1].start - px, sl[1].stop - px))
    alpha = la[ls][..., 3:4] / 255 * .93
    col = la[ls][..., :3] * np.clip(shade[sl][..., None], .7, 1.15)
    tex = (L[sl] - ndi.gaussian_filter(L, 3)[sl])[..., None] * .6           # fabric weave from the photo
    out_a[sl] = out_a[sl] * (1 - alpha) + (col + tex) * alpha
    res = Image.fromarray(np.clip(out_a, 0, 255).astype(np.uint8))
    region = res.crop((lx0 - s, ly0 - s, lx1 + s, ly1 + s)).filter(ImageFilter.GaussianBlur(.7))
    res.paste(region, (lx0 - s, ly0 - s))
    g = np.asarray(res, np.float32) + (ndi.gaussian_filter(np.random.default_rng(1).normal(0, 1, (h, w)), .8) * 3)[..., None] * hole[..., None]
    Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).save(out, quality=94)
    return True


def place_box(im, a, L, box, out):
    """box = (cx, cy, logo_width) in pixels, read off the image by eye."""
    h, w = L.shape; cx, cy, s = box
    hole = np.zeros((h, w), bool); r = int(s * .62)
    yy, xx = np.ogrid[:h, :w]; hole[((xx - cx) / (r * 1.05)) ** 2 + ((yy - cy) / (r * .95)) ** 2 < 1] = True
    area = hole
    m = int(r * 1.6); y0, y1, x0, x1 = max(cy - m, 0), min(cy + m, h), max(cx - m, 0), min(cx + m, w)
    sub = a[y0:y1, x0:x1]; k = int(r * .5) | 1
    small = Image.fromarray(sub.astype(np.uint8)).resize((max(1, (x1 - x0) // 4), max(1, (y1 - y0) // 4)))
    med = np.asarray(small.filter(ImageFilter.MedianFilter(min(31, (k // 4) | 1))).resize((x1 - x0, y1 - y0), Image.BILINEAR), np.float32)
    diff = np.zeros((h, w), bool); d_ = np.abs(sub - med); diff[y0:y1, x0:x1] = (d_.mean(2) > 22) | (d_.max(2) - d_.min(2) > 18)
    hole = area & ndi.binary_dilation(diff, iterations=4)                                     # only the old logo strokes
    keepm = (~hole).astype(np.float32)
    sig = max(6, r * .12)
    num = np.stack([ndi.gaussian_filter(a[..., c] * keepm, sig) for c in range(3)], 2)
    den = ndi.gaussian_filter(keepm, sig)[..., None]
    smooth = num / np.maximum(den, 1e-6)
    weave = (a - np.stack([ndi.gaussian_filter(a[..., c], 2) for c in range(3)], 2))   # fine texture
    ring = ndi.binary_dilation(hole, iterations=int(r * .3)) & ~hole
    sd = weave[ring].std(0) if ring.any() else np.array([3, 3, 3])
    nz = ndi.gaussian_filter(np.random.default_rng(5).normal(0, 1, (h, w)), .9)
    rolled = (nz / nz.std())[..., None] * np.minimum(sd, 2.5) * .5                                              # matched fabric noise
    soft = ndi.gaussian_filter(hole.astype(np.float32), 2)[..., None]
    fab = a * (1 - soft) + (smooth + rolled) * soft
    lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); s = int(s)
    lg = lg.resize((s, int(s * lg.height / lg.width)), Image.LANCZOS); la = np.asarray(lg, np.float32)
    px, py = int(cx - lg.width / 2), int(cy - lg.height / 2)
    shade = ndi.gaussian_filter(L, 20)[py:py + lg.height, px:px + lg.width]
    shade = shade / np.median(shade)
    alpha = la[..., 3:4] / 255 * .9
    base = la[..., :3]; g = base.mean(2, keepdims=True); base = g + (base - g) * .85       # thread is a touch duller
    col = base * np.clip(shade[..., None], .75, 1.1)
    edge = ndi.sobel(la[..., 3], 0)[..., None] / 255 * 6                                    # raised stitch edge
    col = col - edge
    tex = (L - ndi.gaussian_filter(L, 2))[py:py + lg.height, px:px + lg.width][..., None] * .5
    reg = fab[py:py + lg.height, px:px + lg.width]
    fab[py:py + lg.height, px:px + lg.width] = reg * (1 - alpha) + (col + tex) * alpha
    res = Image.fromarray(np.clip(fab, 0, 255).astype(np.uint8))
    crop = (px - 10, py - 10, px + lg.width + 10, py + lg.height + 10)
    res.paste(res.crop(crop).filter(ImageFilter.GaussianBlur(.8)), crop[:2])
    g = np.asarray(res, np.float32); n = ndi.gaussian_filter(np.random.default_rng(2).normal(0, 1, (h, w)), .8) * 4
    g[hole] += n[hole][:, None]
    Image.fromarray(np.clip(g, 0, 255).astype(np.uint8)).save(out, quality=94)
    return True


if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, fix(p, p.replace(".jpg", "-logo.jpg")))
