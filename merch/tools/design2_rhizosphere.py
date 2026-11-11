"""Design 2: PROUD RESIDENT OF THE RHIZOSPHERE (tee front, 3600 x 4800 px = 12 x 16 in)

A 10 in round badge, like a vintage national-park patch. Inside: a soil cross-section around one
root tip.
  - root grows down from top center: root hairs, cell files, root cap
  - arbuscular mycorrhizal hyphae web out from the root (Food Web Green, the only accent).
    AM fungi are aseptate, so these hyphae have no cross walls; two round spores sit on them
  - bacteria colonies on the root surface (rhizoplane): tiny rods and cocci as stipple
  - a bacterial-feeding nematode (smooth lip region, pharyngeal bulb, no stylet) coiled lower left
  - Arcella (testate amoeba, domed shell with round central aperture) lower right
  - soil aggregates as stipple crumbs
Ring text: PROUD RESIDENT OF THE (top arc), RHIZOSPHERE (bottom arc, larger), stars at 3 and 9.
Label under the badge. 1.4 in logo space kept clear under the label.
"""
import math, os, json
import numpy as np
from shapely.geometry import Point, LineString
from shapely.ops import unary_union
import sfw, organisms as O
from sfw import DPI, PT

M = sfw.ROOT
W, H = 3600, 4800
CX = W / 2
R_OUT = 5 * DPI                  # 10 in badge
CY = 0.5 * DPI + R_OUT
BAND = 1.05 * DPI                # text ring
R_IN = R_OUT - BAND
TRACK = 40


def scene(line, accent, rng):
    s = []
    clip = Point(CX, CY).buffer(R_IN - 0.08 * DPI, 128)
    w = 3.0

    # root tip from the top center ------------------------------------------------
    root_top = (CX, CY - R_IN - 40)
    root_svg, root, rc, rn, rhalf = O.root_tip(root_top, R_IN * 1.22, 0.26 * DPI * 1.05 * 3, line, rng, w=w,
                                               hair_len=0.75 * DPI)
    root_zone = root.buffer(0.75 * DPI)          # root + hairs

    # organisms ---------------------------------------------------------------------
    nem_c = []
    for t in np.linspace(0, 1.55 * 2 * math.pi, 400):
        r = (0.62 - 0.20 * t / (3.1 * math.pi)) * DPI * 1.3
        nem_c.append((CX - 0.62 * R_IN + r * math.cos(t + 0.6), CY + 0.42 * R_IN + r * math.sin(t + 0.6) * .85))
    nem_c = O.smooth(nem_c[::-1], 400)            # head on the outside of the coil
    nem_svg, nem = O.nematode(nem_c, 0.19 * DPI, line, rng, w=w, detail=1)
    arc_c = (CX + 0.58 * R_IN, CY + 0.5 * R_IN)
    arc_r = 0.6 * DPI
    arc_svg = O.arcella(*arc_c, 2 * arc_r, line, rng, w=w)
    arc_g = Point(arc_c).buffer(arc_r)

    # AM hyphae web (aseptate), clipped around the organisms ---------------------------
    starts = []
    for frac, side in [(.30, -1), (.42, 1), (.55, -1), (.62, 1), (.72, -1), (.38, -1), (.50, 1)]:
        i = int(frac * (len(rc) - 1))
        starts.append((rc[i] + rn[i] * side * rhalf[i], side))
    lines = []
    for (p, side), L in zip(starts, [1.9, 1.8, 2.1, 1.9, 1.7, 1.3, 1.4]):
        ang = 180 + rng.uniform(-30, 30) if side < 0 else rng.uniform(-30, 30)
        lines += O.branching(p, ang, L * DPI, rng, depth=2, spread=40, wiggle=.14, shrink=.6)
    hy = O.tube(lines, 0.07 * DPI)
    keep = unary_union([root.buffer(4), nem.buffer(28), arc_g.buffer(28)])
    hy = hy.difference(keep).intersection(clip)
    spores = [Point(lines[1][-1]).buffer(0.13 * DPI), Point(lines[7][-1]).buffer(0.11 * DPI)]
    spores = [sp for sp in spores if sp.within(clip) and not sp.intersects(keep)]

    # soil aggregates (stipple crumbs) in the open ground ---------------------------------
    taken = unary_union([root_zone, nem.buffer(80), arc_g.buffer(80)] + [sp.buffer(30) for sp in spores])
    crumbs = []
    for _ in range(600):
        if len(crumbs) >= 15:
            break
        a = rng.uniform(0, 2 * math.pi); d = R_IN * math.sqrt(rng.uniform(.05, .9))
        R = rng.uniform(.28, .5) * DPI
        c = Point(CX + d * math.cos(a), CY + d * math.sin(a))
        g = c.buffer(R * 1.25)
        if g.within(clip) and not g.intersects(taken) and all(not g.intersects(o) for o in crumbs):
            crumbs.append(g)
    hy_keep = hy
    for g in crumbs:
        svg, shape = O.crumb(g.centroid.x, g.centroid.y, (g.bounds[2] - g.bounds[0]) / 2.6, line, rng, w=w)
        s.append(svg)

    # bacteria on the root surface (rhizoplane): colonies of tiny rods and cocci ------------
    col = []
    for frac in np.linspace(.15, .9, 11):
        i = int(frac * (len(rc) - 1))
        for side in (-1, 1):
            if rng.random() < .75:
                p = rc[i] + rn[i] * side * (rhalf[i] + 14)
                col.append(O.coccus_colony(p[0], p[1], 0.09 * DPI, 16, 3.4, line, 2.5, rng, solid=True))
                for _ in range(4):
                    q = p + rng.normal(0, 14, 2)
                    O_rod, _ = O.rod(q[0], q[1], 22, 9, rng.uniform(0, 180), line, 2.5, dots=False)
                    col.append(O.fill(O.poly_d(_), line))

    s.append(O.outline(hy_keep, accent, w * 1.3))
    for sp in spores:
        s.append(O.outline(sp, accent, w * 1.6) + O.outline(sp.buffer(-12), accent, w))
    s.append(root_svg)
    s.append("".join(col))
    s.append(nem_svg)
    s.append(arc_svg)
    return "\n".join(s)


def ring(line, rng):
    s = []
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_OUT - 9:.1f}" fill="none" stroke="{line}" stroke-width="18"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_OUT - 38:.1f}" fill="none" stroke="{line}" stroke-width="4"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_IN:.1f}" fill="none" stroke="{line}" stroke-width="12"/>')
    s.append(f'<circle cx="{CX}" cy="{CY}" r="{R_IN + 26:.1f}" fill="none" stroke="{line}" stroke-width="4"/>')
    mid = R_IN + 26 + (R_OUT - 38 - R_IN - 26) / 2
    top_size = 0.50 * DPI
    d, span_top = sfw.text_arc("PROUD RESIDENT OF THE", "montserrat-800", top_size, CX, CY, mid - 0.70 * top_size / 2, 0, 120)
    s.append(f'<g fill="{line}">{d}</g>')
    bot_size = 0.64 * DPI
    d, span_bot = sfw.text_arc("RHIZOSPHERE", "montserrat-800", bot_size, CX, CY, mid + 0.70 * bot_size / 2, 180, 80, bottom=True)
    s.append(f'<g fill="{line}">{d}</g>')
    for ang in (90, 270):
        a = math.radians(ang)
        s.append(O.star(CX + mid * math.sin(a), CY - mid * math.cos(a), 0.15 * DPI, line))
    return "\n".join(s), {"top_arc_deg": round(span_top), "bottom_arc_deg": round(span_bot)}


def build(scheme):
    line, accent = sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]
    rng = np.random.default_rng(42)
    sc = scene(line, accent, rng)
    rg, info = ring(line, rng)
    body = [f'<clipPath id="inside"><circle cx="{CX}" cy="{CY}" r="{R_IN - 0.08 * DPI:.1f}"/></clipPath>',
            f'<g clip-path="url(#inside)">\n{sc}\n</g>', rg]
    lab, bottom = sfw.slide_label(CX, CY + R_OUT + 0.35 * DPI, "Rhizosphere", "living root zone · 100x", line)
    body.append(lab)
    logo = (CX - 0.7 * DPI, bottom + 0.3 * DPI, 1.4 * DPI, 1.4 * DPI)
    body.append(f'<!-- SFW logo space, keep clear: x={logo[0]:.0f} y={logo[1]:.0f} w={logo[2]:.0f} h={logo[3]:.0f} px -->')
    info["bottom_in"] = round((logo[1] + logo[3]) / DPI, 2)
    return sfw.svg_doc(W, H, "\n".join(body)), info


def main():
    for scheme in ("light", "dark"):
        svg, info = build(scheme)
        base = f"tee-front-rhizosphere-{scheme}"
        open(os.path.join(M, "source-svg", base + ".svg"), "w").write(svg)
        im = sfw.export_png(svg, os.path.join(M, "print-files", base + ".png"), W, H)
        info["off_palette"] = len(sfw.palette_check(im, [sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]]))
        info["thin_share"] = round(sfw.thin_line_check(im), 4)
        print(scheme, json.dumps(info))
        for gm in (["desert-dust"] if scheme == "light" else ["khaki", "black"]):
            sfw.preview(im, sfw.GARMENT[gm], os.path.join(M, "previews", f"tee-front-rhizosphere-on-{gm}.png"))


if __name__ == "__main__":
    main()
