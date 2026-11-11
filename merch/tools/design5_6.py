"""Design 5: FUNGAL DOMINANT (cap front, embroidery, 1200 x 450 px = 4 x 1.5 in)
Design 6: DIRT IS DEAD. SOIL IS ALIVE. (tee front, 3600 x 4800 px)
"""
import math, os, json
import numpy as np
from shapely.geometry import Point, Polygon, LineString, box
from shapely.ops import unary_union
from shapely import affinity
import sfw, organisms as O
from sfw import DPI, PT

M = sfw.ROOT
MM = DPI / 25.4


# ------------------------------------------------------------------ design 5: cap
def cap(thread):
    """Solid shapes only, one thread colour. Hyphae strand 1.4 mm thick, letters about 8 mm tall."""
    W, H = 1200, 450
    s = []
    t = 1.4 * MM                                   # 16.5 px strands, embroidery-safe (>= 1 mm)
    main = [(70, 395), (120, 300), (175, 215), (215, 120), (240, 55)]
    b1 = [(150, 255), (100, 190), (85, 120)]
    b2 = [(200, 160), (265, 120), (300, 70)]
    shape = unary_union([LineString(O.smooth(l, 80)).buffer(t / 2, 16) for l in (main, b1, b2)])
    for tip, r in ((main[-1], t * .8), (b1[-1], t * .8), (b2[-1], t * .8)):
        shape = shape.union(Point(tip).buffer(r))
    s.append(O.fill(O.poly_d(shape), thread))
    x0 = 360
    tw = W - x0 - 30
    size = min(sfw.fit_size("DOMINANT", "montserrat-800", tw, 40), sfw.fit_size("FUNGAL", "montserrat-800", tw, 40))
    cap_h = 0.70 * size
    lead = 0.95 * size
    top = (H - (lead + cap_h)) / 2
    b1y = top + cap_h
    for word, y in (("FUNGAL", b1y), ("DOMINANT", b1y + lead)):
        d, _, _ = sfw.text(word, "montserrat-800", size, x=x0, y=y, tracking=40)
        s.append(f'<path fill="{thread}" d="{d}"/>')
    return sfw.svg_doc(W, H, "\n".join(s)), {"letter_height_mm": round(cap_h / MM, 1), "strand_mm": round(t / MM, 2)}


# ------------------------------------------------------------------ design 6: dirt / soil
def clod_shape(cx, cy, w, h, rng):
    pts = []
    for t in np.linspace(0, 2 * math.pi, 90, endpoint=False):
        r = 1 + .06 * math.sin(3 * t + 1) + .05 * math.sin(7 * t) + rng.normal(0, .015)
        y = math.sin(t) * (1.0 if math.sin(t) > 0 else .82)
        pts.append((cx + w / 2 * math.cos(t) * r, cy + h / 2 * y * r))
    return Polygon(pts).buffer(0)


def dirt_soil(scheme):
    line, accent = sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]
    W, H = 3600, 4800
    rng = np.random.default_rng(66)
    w = 3.0
    CX = W / 2
    CW, CH = 9 * DPI, 4.6 * DPI
    top = 0.9 * DPI
    CY = top + CH / 2
    clod = clod_shape(CX, CY, CW, CH, rng)
    gap = 0.12 * DPI
    left = clod.intersection(box(0, 0, CX - gap / 2, H))
    right = clod.intersection(box(CX + gap / 2, 0, W, H))
    right = affinity.translate(right, 0.12 * DPI, 0)           # the split opens slightly
    s = []
    # LEFT: dead dirt, sparse flat hatching, cracks, nothing living
    s.append(O.hatch(left.buffer(-12), 30, 46, w, line))
    cracks = []
    for st in [(CX - CW * .35, CY - CH * .3), (CX - CW * .18, CY + CH * .1), (CX - CW * .4, CY + CH * .25)]:
        p = np.array(st); a = rng.uniform(-.6, .6)
        pts = [p]
        for _ in range(7):
            a += rng.normal(0, .5)
            pts.append(pts[-1] + 70 * np.array([math.cos(a), math.sin(a)]))
        cracks.append(O.d_of(pts))
    s.append(O.stroke("".join(cracks), line, w * 2.2))
    s.append(O.outline(left, line, w * 3))
    # RIGHT: living soil
    rx0, ry0, rx1, ry1 = right.bounds
    # root growing in from above
    root_svg, root, rc, rn, rh = O.root_tip((rx0 + (rx1 - rx0) * .55, ry0 - 1.2 * DPI), 3.0 * DPI, 0.38 * DPI, line, rng, w=w,
                                           hair_len=0.45 * DPI)
    # earthworm curling out of the bottom edge
    ew_c = O.smooth([(rx0 + (rx1 - rx0) * .25, ry1 - .6 * DPI), (rx0 + (rx1 - rx0) * .45, ry1 - .2 * DPI),
                     (rx0 + (rx1 - rx0) * .55, ry1 + .45 * DPI), (rx0 + (rx1 - rx0) * .78, ry1 + .65 * DPI),
                     (rx0 + (rx1 - rx0) * .9, ry1 + .35 * DPI)], 400)
    ew_svg, ew = O.earthworm(ew_c, 0.34 * DPI, line, rng, w=w)
    keep = unary_union([root.buffer(0.3 * DPI), ew.buffer(30)])
    inside = right.buffer(-14)
    # crumbs (aggregates)
    crumbs = []
    for _ in range(800):
        if len(crumbs) >= 16:
            break
        R = rng.uniform(.22, .42) * DPI
        x, y = rng.uniform(rx0, rx1), rng.uniform(ry0, ry1)
        g = Point(x, y).buffer(R * 1.2)
        if g.within(inside) and not g.intersects(keep) and all(not g.intersects(c) for c in crumbs):
            crumbs.append(g)
    for g in crumbs:
        s.append(O.crumb(g.centroid.x, g.centroid.y, (g.bounds[2] - g.bounds[0]) / 2.5, line, rng, w=w, density=1.3)[0])
    # hyphae threading between the crumbs
    lines = []
    for st, ang in [((rx0 + 40, ry0 + CH * .35), 10), ((rx0 + 60, ry0 + CH * .7), -15), ((rx1 - 60, ry0 + CH * .2), 170)]:
        lines += O.branching(st, ang, 2.6 * DPI, rng, depth=2, spread=40, wiggle=.18, shrink=.55)
    hy = O.tube(lines, 0.05 * DPI).intersection(inside).difference(keep)
    hy = hy.difference(unary_union([c.buffer(-20) for c in crumbs]))
    s.append(O.outline(hy, line, w * 1.1))
    # bacteria colonies
    for _ in range(14):
        x, y = rng.uniform(rx0, rx1), rng.uniform(ry0, ry1)
        if inside.contains(Point(x, y)) and not keep.contains(Point(x, y)):
            s.append(O.coccus_colony(x, y, 0.08 * DPI, 14, 3.4, line, w, rng, solid=True))
    s.append(O.outline(right, line, w * 3))
    s.append(f'<g>{root_svg}</g>')
    s.append(ew_svg)
    # TEXT: DIRT IS DEAD. small and plain under the left half; SOIL IS ALIVE. larger, green, under the right
    lcx = (left.bounds[0] + left.bounds[2]) / 2
    rcx = (right.bounds[0] + right.bounds[2]) / 2
    half_w = CW / 2 - 0.2 * DPI
    big = sfw.fit_size("ALIVE.", "montserrat-800", half_w, 40)
    big = min(big, sfw.fit_size("SOIL IS", "montserrat-800", half_w, 40))
    small = big * 0.5
    ty = ry1 + 1.05 * DPI
    b1 = ty + .7 * big
    for word, y in (("SOIL IS", b1), ("ALIVE.", b1 + .95 * big)):
        d, _, _ = sfw.text(word, "montserrat-800", big, x=rcx, y=y, tracking=40, anchor="middle")
        s.append(f'<path fill="{accent}" d="{d}"/>')
    sb = b1 + .95 * big - .7 * big + .7 * small          # align DIRT IS DEAD. with the bottom line
    small = big * 0.52
    for word, y in (("DIRT IS", b1 + .95 * big - .95 * small), ("DEAD.", b1 + .95 * big)):
        d, _, _ = sfw.text(word, "montserrat-600", small, x=lcx, y=y, tracking=40, anchor="middle")
        s.append(f'<path fill="{line}" d="{d}"/>')
    lab, bottom = sfw.slide_label(CX, b1 + .95 * big + 0.45 * DPI, "Before and after", "biology restored", line)
    s.append(lab)
    logo = (CX - 0.7 * DPI, bottom + 0.3 * DPI, 1.4 * DPI, 1.4 * DPI)
    s.append(f'<!-- SFW logo space, keep clear: x={logo[0]:.0f} y={logo[1]:.0f} w={logo[2]:.0f} h={logo[3]:.0f} px -->')
    return sfw.svg_doc(W, H, "\n".join(s)), {"big_px": round(big), "bottom_in": round((logo[1] + logo[3]) / DPI, 2)}


def main():
    for name, thread, garment in (("cap-front-fungal-dominant-cream", sfw.INK["cream"], "jungle"),
                                  ("cap-front-fungal-dominant-deep-green", sfw.INK["deep-green"], "oyster-cap")):
        svg, info = cap(thread)
        open(os.path.join(M, "source-svg", name + ".svg"), "w").write(svg)
        im = sfw.export_png(svg, os.path.join(M, "print-files", name + ".png"), 1200, 450)
        info["colors"] = len(sfw.palette_check(im, [thread]))
        print(name, json.dumps(info))
        sfw.preview(im, sfw.GARMENT[garment], os.path.join(M, "previews", f"{name}-on-{garment.split('-')[0]}.png"), width=1200)
    for scheme in ("light", "dark"):
        svg, info = dirt_soil(scheme)
        base = f"tee-front-dirt-is-dead-soil-is-alive-{scheme}"
        open(os.path.join(M, "source-svg", base + ".svg"), "w").write(svg)
        im = sfw.export_png(svg, os.path.join(M, "print-files", base + ".png"), 3600, 4800)
        info["thin_share"] = round(sfw.thin_line_check(im), 4)
        print(base, json.dumps(info))
        for gm in (["desert-dust"] if scheme == "light" else ["khaki", "black"]):
            sfw.preview(im, sfw.GARMENT[gm], os.path.join(M, "previews", f"tee-front-dirt-is-dead-soil-is-alive-on-{gm}.png"))


if __name__ == "__main__":
    main()
