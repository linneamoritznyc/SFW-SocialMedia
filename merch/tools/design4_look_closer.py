"""Design 4: LOOK CLOSER. 400x (tote front, Econscious EC8000 Oyster, 3600 x 4200 px = 12 x 14 in)

An 11 in microscope field of view with the dark eyepiece edge as a thick solid ring. Inside, soil at
400x, drawn to one consistent scale (field of view about 450 um, so about 7.3 px per um):
septate fungal hyphae across the field (Food Web Green), a Colpoda, a flagellate, a nematode passing
through, bacteria as stipple, and one mite leg entering from the edge. Scale bar "20 µm".
Under it: LOOK CLOSER. in Montserrat ExtraBold and 400x in Source Sans 3 Italic, larger, like the
number on a magnification knob. Slide label, with the logo space beside it.
"""
import math, os, json
import numpy as np
from shapely.geometry import Point
from shapely.ops import unary_union
import sfw, organisms as O
from sfw import DPI, PT

M = sfw.ROOT
W, H = 3600, 4200
CX = W / 2
R = 5.5 * DPI
CY = 0.12 * DPI + R
RING = 0.32 * DPI
UM = 7.3                      # px per micrometre at this magnification


def field(line, accent, rng):
    w = 3.0
    clip = Point(CX, CY).buffer(R - RING + 4, 128)
    s = []
    # mite leg from the upper right edge
    leg_svg, leg = O.mite_leg((CX + R * .98, CY - R * .45), 196, 3.0 * DPI, 0.5 * DPI, line, rng, w=w)
    # nematode passing through the lower field (about 15 um wide)
    c = O.smooth([(CX - R * 1.1, CY + R * .25), (CX - R * .45, CY + R * .62), (CX + R * .1, CY + R * .42),
                  (CX + R * .5, CY + R * .7), (CX + R * .75, CY + R * .55)], 400)
    nem_svg, nem = O.nematode(c, 15 * UM, line, rng, w=w, detail=1)
    col_c = (CX - R * .35, CY - R * .2)
    col_svg = O.colpoda(*col_c, 60 * UM, -20, line, line, rng, detail=1, w=w)
    col = Point(col_c).buffer(60 * UM * .62)
    fl_c = (CX + R * .32, CY + R * .05)
    fl_svg = O.flagellate(*fl_c, 26 * UM, 15, line, rng, w=w)
    fl = Point(fl_c).buffer(26 * UM * .7)
    keep = unary_union([leg.buffer(30), nem.buffer(30), col.buffer(40), fl.buffer(20)])
    # hyphae across the whole field (3 to 5 um wide)
    lines = [O.smooth([(CX - R, CY - R * .55), (CX - R * .2, CY - R * .62), (CX + R * .5, CY - R * .2), (CX + R, CY - R * .1)], 300),
             O.smooth([(CX - R * .8, CY + R * .9), (CX - R * .55, CY + R * .1), (CX - R * .1, CY - R * .9)], 300),
             O.smooth([(CX + R * .1, CY + R), (CX + R * .25, CY + R * .2), (CX + R * .9, CY - R * .5)], 300)]
    for st, ang in [((CX - R * .2, CY - R * .6), -100), ((CX + R * .25, CY + R * .25), 20), ((CX - R * .6, CY + R * .4), 200)]:
        lines += O.branching(st, ang, 1.4 * DPI, rng, depth=1, spread=35, wiggle=.1)
    hy = O.tube(lines, 4.5 * UM).difference(keep).intersection(clip)
    s.append(O.outline(hy, accent, w * 1.3))
    segs = []
    for ln in lines:
        from shapely.geometry import LineString
        for p, t in O.along(LineString(ln), 16 * UM):
            n = np.array([-t[1], t[0]]) * (4.5 * UM / 2 - 1.5)
            a, b = p - n, p + n
            if hy.buffer(1).contains(Point(p)):
                segs.append(f"M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}")
    s.append(O.stroke("".join(segs), accent, w))
    # bacteria everywhere as stipple (1 to 2 um), thinning toward the edge, plus a few tiny rods
    open_ = clip.difference(keep.buffer(10)).difference(hy.buffer(6))
    s.append(O.stipple(open_, 2600, 3.6, line, rng, bias=lambda x, y: 0.4 + 0.6 * rng.random()))
    for _ in range(140):
        a = rng.uniform(0, 2 * math.pi); d = (R - RING) * math.sqrt(rng.random())
        x, y = CX + d * math.cos(a), CY + d * math.sin(a)
        if open_.contains(Point(x, y)):
            _, g = O.rod(x, y, 2.2 * UM * 1.6, 1.0 * UM * 1.6, rng.uniform(0, 180), line, w, dots=False)
            s.append(O.fill(O.poly_d(g), line))
    s += [col_svg, fl_svg, nem_svg, leg_svg]
    return "\n".join(s)


def build():
    line, accent = sfw.SCHEME["light"]["line"], sfw.SCHEME["light"]["accent"]
    rng = np.random.default_rng(400)
    body = [f'<clipPath id="fov"><circle cx="{CX}" cy="{CY}" r="{R - RING + 2:.1f}"/></clipPath>',
            f'<g clip-path="url(#fov)">\n{field(line, accent, rng)}\n</g>',
            f'<circle cx="{CX}" cy="{CY}" r="{R - RING / 2:.1f}" fill="none" stroke="{line}" stroke-width="{RING:.1f}"/>']
    # scale bar, inside, lower right
    bx, by = CX + R * .28, CY + R * .86
    L = 20 * UM
    body.append(f'<rect x="{bx:.1f}" y="{by:.1f}" width="{L:.1f}" height="11" fill="{line}"/>')
    d, _, _ = sfw.text("20 µm", "source-sans-400", 15 * PT, x=bx + L / 2, y=by - 18, anchor="middle")
    body.append(f'<path fill="{line}" d="{d}"/>')

    # LOOK CLOSER.  400x   one line, as wide as the circle minus a margin
    y0 = CY + R + 0.42 * DPI
    k = 1.55                                  # 400x is set larger, like the knob number
    a = sfw.text_width("LOOK CLOSER.", "montserrat-800", 100, 40)
    b = sfw.text_width("400x", "source-sans-400-italic", 100 * k)
    gap = 0.35 * 100
    size = (2 * R * .92) / (a + gap + b) * 100
    cap = 0.70 * size
    base = y0 + cap
    x = CX - (a + gap + b) * size / 100 / 2
    d, wa, _ = sfw.text("LOOK CLOSER.", "montserrat-800", size, x=x, y=base, tracking=40)
    body.append(f'<path fill="{line}" d="{d}"/>')
    d, _, _ = sfw.text("400x", "source-sans-400-italic", size * k, x=x + wa + gap * size / 100, y=base)
    body.append(f'<path fill="{accent}" d="{d}"/>')
    lab_top = base + 0.38 * DPI
    lab, bottom = sfw.slide_label(CX - 0.8 * DPI, lab_top, "Soil sample", "teaspoon of healthy soil · 400x", line)
    body.append(lab)
    logo = (CX + 0.55 * DPI, lab_top, 1.3 * DPI, bottom - lab_top)
    body.append(f'<!-- SFW logo space, keep clear: x={logo[0]:.0f} y={logo[1]:.0f} w={logo[2]:.0f} h={logo[3]:.0f} px -->')
    return sfw.svg_doc(W, H, "\n".join(body)), {"text_size_px": round(size), "bottom_in": round(bottom / DPI, 2)}


def main():
    svg, info = build()
    base = "tote-front-look-closer-400x"
    open(os.path.join(M, "source-svg", base + ".svg"), "w").write(svg)
    im = sfw.export_png(svg, os.path.join(M, "print-files", base + ".png"), W, H)
    info["thin_share"] = round(sfw.thin_line_check(im), 4)
    print(json.dumps(info))
    sfw.preview(im, sfw.GARMENT["oyster-tote"], os.path.join(M, "previews", f"{base}-on-oyster.png"))


if __name__ == "__main__":
    main()
