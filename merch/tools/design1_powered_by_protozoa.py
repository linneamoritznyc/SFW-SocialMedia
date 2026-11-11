"""Design 1: POWERED BY PROTOZOA (tee front, 3600 x 4800 px = 12 x 16 in at 300 dpi)

The Colpoda is drawn in code as engraved line art (Replicate had no credit when this was made;
see generation-log.md). Anatomy, after light-microscope and silver-stain plates of Colpoda:
  - kidney-shaped cell, concave side with the oral vestibulum (a funnel-shaped groove lined
    with dense oral cilia), anterior to the left
  - a fringe of several hundred even somatic cilia beating in a metachronal wave
  - kineties (rows of basal bodies) running across the cell, drawn as dotted rows
  - food vacuoles as hatched circles, some holding a bacterium being digested
  - one round macronucleus with a micronucleus beside it, a contractile vacuole at the posterior end
  - shading by engraver's hatching and cross-hatching, light from the upper left
Four rod bacteria drift toward the mouth (Food Web Green, the only accent).

Usage: python3 design1_powered_by_protozoa.py
"""
import math, os
import numpy as np
from shapely.geometry import Polygon, Point, LineString, MultiLineString
from shapely import affinity
import sfw
from sfw import DPI, PT

M = sfw.ROOT
W, H = 3600, 4800
rng = np.random.default_rng(7)

A, B = 1100, 800                    # half-length, half-width of the cell (local units)
LW_OUT, LW = 10, 3.2                 # contour and fine line weights (>= 0.5 pt after scaling)


# ------------------------------------------------------------------ the cell
def outline_pts(n=900):
    th0, depth, wid = 1.5 * math.pi - 0.28, 230, 0.42   # concave notch, a little anterior
    pts = []
    for t in np.linspace(0, 2 * math.pi, n, endpoint=False):
        x, y = A * math.cos(t), B * math.sin(t)
        if x < 0:                    # anterior end a little narrower
            y *= 1 - 0.10 * (-x / A)
        dt = (t - th0 + math.pi) % (2 * math.pi) - math.pi
        y += depth * math.exp(-(dt / wid) ** 2)
        pts.append((x, y))
    return pts


def notch_point(pts):
    th0 = 1.5 * math.pi - 0.28
    i = int(round(th0 / (2 * math.pi) * len(pts))) % len(pts)
    return np.array(pts[i])


def path_d(pts, close=True):
    s = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return s + (" Z" if close else "")


def hatch(geom, angle, spacing, lw, color):
    """Parallel engraved lines clipped to geom."""
    if geom.is_empty: return ""
    minx, miny, maxx, maxy = geom.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    R = math.hypot(maxx - minx, maxy - miny)
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    lines = []
    for o in np.arange(-R, R, spacing):
        p0 = (cx - ca * R - sa * o, cy - sa * R + ca * o)
        p1 = (cx + ca * R - sa * o, cy + sa * R + ca * o)
        seg = LineString([p0, p1]).intersection(geom)
        for s in getattr(seg, "geoms", [seg]):
            if s.length > lw * 2 and s.geom_type == "LineString":
                (x0, y0), (x1, y1) = s.coords[0], s.coords[-1]
                lines.append(f"M{x0:.1f},{y0:.1f}L{x1:.1f},{y1:.1f}")
    return (f'<path d="{"".join(lines)}" fill="none" stroke="{color}" stroke-width="{lw}" '
            f'stroke-linecap="round"/>') if lines else ""


def capsule(cx, cy, L, Wd, ang, color, lw, stipple=True):
    """A rod bacterium: capsule outline with stippled cytoplasm."""
    r = Wd / 2; h = L / 2 - r
    body = affinity.rotate(LineString([(-h, 0), (h, 0)]).buffer(r, 32), ang, origin=(0, 0))
    body = affinity.translate(body, cx, cy)
    out = [f'<path d="{path_d(list(body.exterior.coords)[:-1])}" fill="none" stroke="{color}" stroke-width="{lw}"/>']
    if stipple:
        inner = body.buffer(-lw * 1.6)
        n = int(inner.area / 260)
        minx, miny, maxx, maxy = inner.bounds
        dots = []
        while len(dots) < n:
            p = (rng.uniform(minx, maxx), rng.uniform(miny, maxy))
            if inner.contains(Point(p)): dots.append(p)
        rr = max(lw * 0.62, sfw.MIN_LINE_PX / 2 + 0.3)
        out.append("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rr:.1f}" fill="{color}"/>' for x, y in dots))
    return "".join(out), body


def colpoda(line, accent):
    pts = outline_pts()
    body = Polygon(pts)
    parts = []

    # organelles (local coords) ------------------------------------------------
    nuc_c, nuc_r = (0.16 * A, 0.18 * B), 0.21 * B
    mic_c, mic_r = (nuc_c[0] - nuc_r - 30, nuc_c[1] + nuc_r * 0.55), 34
    cv_c, cv_r = (0.80 * A, 0.05 * B), 62
    vac = [(-0.55, 0.05, 78, True), (-0.32, 0.40, 92, False), (-0.12, -0.18, 70, False),
           (0.45, -0.38, 86, True), (0.52, 0.42, 74, False), (-0.70, -0.30, 56, False),
           (0.30, 0.62, 60, False), (-0.45, 0.68, 52, True), (0.66, -0.05, 48, False)]
    vac = [((fx * A, fy * B), r, food) for fx, fy, r, food in vac]
    notch = notch_point(pts)
    funnel_tip = notch + np.array([70, 250])
    funnel = LineString([tuple(notch + (0, -60)), tuple(notch + (30, 120)), tuple(funnel_tip)]).buffer(78, 32).intersection(body.buffer(-8))
    holes = [Point(nuc_c).buffer(nuc_r + 18), Point(cv_c).buffer(cv_r + 14), funnel.buffer(20)] + \
            [Point(c).buffer(r + 16) for c, r, _ in vac]
    keepout = holes[0]
    for h in holes[1:]: keepout = keepout.union(h)

    # shading: hatching on the lower right crescent, cross-hatching deepest --------
    shade1 = body.difference(affinity.translate(affinity.scale(body, 0.84, 0.80), -120, -140)).difference(keepout)
    shade2 = body.difference(affinity.translate(affinity.scale(body, 0.93, 0.90), -60, -80)).difference(keepout)
    parts.append(hatch(shade1, 38, 17, LW * 0.85, line))
    parts.append(hatch(shade2, -52, 17, LW * 0.85, line))

    # kineties: dotted rows of basal bodies running across the cell ---------------
    dots = []
    inner = body.buffer(-40).difference(keepout).difference(shade2)
    for k in np.linspace(-0.92, 0.92, 17):
        for x in np.arange(-A, A, 24):
            u = x / A
            y = k * B * math.sqrt(max(0, 1 - u * u)) * 0.95 + 0.10 * B * (1 - u * u) + 28 * u * k
            if inner.contains(Point(x, y)):
                dots.append((x, y))
    parts.append("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.4" fill="{line}"/>' for x, y in dots))

    # macronucleus (stippled) and micronucleus ----------------------------------
    parts.append(f'<circle cx="{nuc_c[0]:.1f}" cy="{nuc_c[1]:.1f}" r="{nuc_r:.1f}" fill="none" stroke="{line}" stroke-width="7"/>')
    nd = []
    while len(nd) < 420:
        p = rng.uniform(-1, 1, 2)
        if p @ p < 0.86 and rng.random() < 0.35 + 0.65 * ((p[0] + p[1] + 2) / 4):  # denser lower right
            nd.append(np.array(nuc_c) + p * nuc_r)
    parts.append("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.6" fill="{line}"/>' for x, y in nd))
    parts.append(f'<circle cx="{mic_c[0]:.1f}" cy="{mic_c[1]:.1f}" r="{mic_r}" fill="{line}"/>')

    # contractile vacuole: clear, double outline ---------------------------------
    parts.append(f'<circle cx="{cv_c[0]:.1f}" cy="{cv_c[1]:.1f}" r="{cv_r}" fill="none" stroke="{line}" stroke-width="5"/>'
                 f'<circle cx="{cv_c[0]:.1f}" cy="{cv_c[1]:.1f}" r="{cv_r - 14}" fill="none" stroke="{line}" stroke-width="3"/>')

    # food vacuoles: hatched circles, some with a bacterium being digested --------
    for (cx, cy), r, food in vac:
        parts.append(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="none" stroke="{line}" stroke-width="5"/>')
        if food:
            ang = rng.uniform(0, 180)
            svg, rod = capsule(cx, cy, r * 1.15, r * 0.48, ang, accent, 4.2, stipple=False)
            parts.append(svg)
            parts.append(hatch(Point(cx, cy).buffer(r - 9).difference(rod.buffer(10)), 30, 15, LW * 0.8, line))
        else:
            parts.append(hatch(Point(cx, cy).buffer(r - 9), 30, 15, LW * 0.8, line))

    # oral vestibulum: dark funnel lined with oral cilia ------------------------
    parts.append(hatch(funnel, 70, 12, LW * 0.85, line))
    parts.append(hatch(funnel.buffer(-16), -20, 12, LW * 0.85, line))
    rim = funnel.exterior.difference(body.exterior.buffer(14))
    for seg in getattr(rim, "geoms", [rim]):
        parts.append(f'<path d="{path_d(list(seg.coords), False)}" fill="none" stroke="{line}" stroke-width="7" stroke-linejoin="round"/>')

    # contour --------------------------------------------------------------------
    parts.append(f'<path d="{path_d(pts)}" fill="none" stroke="{line}" stroke-width="{LW_OUT}" stroke-linejoin="round"/>')
    parts.append(f'<path d="{path_d(list(body.buffer(-22).exterior.coords)[:-1])}" fill="none" stroke="{line}" '
                 f'stroke-width="{LW * 0.9}"/>')                                    # pellicle

    # somatic cilia: hundreds of even strokes, metachronal wave ---------------------
    ring = LineString(pts + [pts[0]])
    N = 360
    cil, ends = [], []
    for i in range(N):
        s = i / N * ring.length
        p = np.array(ring.interpolate(s).coords[0]); q = np.array(ring.interpolate(s + 3).coords[0])
        t = (q - p) / np.linalg.norm(q - p); n = np.array([t[1], -t[0]])
        if Point(p + n * 5).within(body): n = -n
        L = 128 + 8 * math.sin(i / N * 2 * math.pi * 3)
        bend = math.radians(30 + 10 * math.sin(i / N * 2 * math.pi * 18))   # metachronal wave
        d = n * math.cos(bend) + t * math.sin(bend)
        e = p + d * L; c = p + n * L * 0.6
        cil.append(f"M{p[0]:.1f},{p[1]:.1f}Q{c[0]:.1f},{c[1]:.1f} {e[0]:.1f},{e[1]:.1f}")
        ends.append(e)
    parts.append(f'<path d="{"".join(cil)}" fill="none" stroke="{line}" stroke-width="{LW}" stroke-linecap="round"/>')
    # oral cilia beating into the vestibulum
    oc = []
    for i in range(18):
        u = i / 17
        p = notch + np.array([-95 + 200 * u, 10 + 30 * math.sin(u * math.pi)])
        tip = notch + np.array([20 + 60 * (u - 0.5), 150 + 50 * math.sin(u * math.pi)])
        oc.append(f"M{p[0]:.1f},{p[1]:.1f}L{tip[0]:.1f},{tip[1]:.1f}")
    parts.append(f'<path d="{"".join(oc)}" fill="none" stroke="{line}" stroke-width="{LW}" stroke-linecap="round"/>')

    # bacteria drifting toward the mouth ---------------------------------------
    mouth = notch + np.array([20, 40])
    approach = [(-40, -230, 140, 54), (90, -400, 150, 56), (-110, -560, 136, 52), (60, -720, 146, 56)]
    bact = []
    for dx, dy, L, Wd in approach:
        cx, cy = mouth[0] + dx, mouth[1] + dy
        ang = math.degrees(math.atan2(mouth[1] - cy, mouth[0] - cx)) + rng.uniform(-18, 18)
        svg, rod = capsule(cx, cy, L, Wd, ang, accent, 5)
        bact.append(svg)
    parts.append("".join(bact))
    allpts = np.array(pts + [tuple(e) for e in ends] + [(mouth[0] - 190, mouth[1] - 790), (mouth[0] + 140, mouth[1] - 790)])
    return "\n".join(parts), allpts


# ------------------------------------------------------------------ layout
def build(scheme):
    line, accent = sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]
    art, pts = colpoda(line, accent)
    rot = -15                                        # swimming, tilted 15 degrees
    th = math.radians(rot)
    R = np.array([[math.cos(th), -math.sin(th)], [math.sin(th), math.cos(th)]])
    rp = pts @ R.T
    minx, miny = rp.min(0); maxx, maxy = rp.max(0)
    target_w = 9 * DPI
    s = target_w / (maxx - minx)
    top = 0.55 * DPI
    tx = W / 2 - s * (minx + maxx) / 2
    ty = top - s * miny
    cil_h = (maxy - miny) * s
    body = [f'<g transform="translate({tx:.1f},{ty:.1f}) scale({s:.4f}) rotate({rot})">\n{art}\n</g>']

    # type: POWERED BY / PROTOZOA (1.6x), the block as wide as the ciliate
    s2 = sfw.fit_size("PROTOZOA", "montserrat-800", target_w, 40)
    s1 = s2 / 1.6
    y = top + cil_h + 0.45 * DPI
    b1 = y + 0.70 * s1
    d, w1, _ = sfw.text("POWERED BY", "montserrat-800", s1, x=W / 2, y=b1, tracking=40, anchor="middle")
    body.append(f'<path fill="{line}" d="{d}"/>')
    b2 = b1 + 0.95 * s2 * 0.86                     # tight leading for caps, 0.95 of the size less the descender room
    d, w2, _ = sfw.text("PROTOZOA", "montserrat-800", s2, x=W / 2, y=b2, tracking=40, anchor="middle")
    body.append(f'<path fill="{line}" d="{d}"/>')
    lab, bottom = sfw.slide_label(W / 2, b2 + 0.40 * DPI, "Colpoda sp.", "soil ciliate · 400x", line)
    body.append(lab)
    logo = (W / 2 - 0.7 * DPI, bottom + 0.35 * DPI, 1.4 * DPI, 1.4 * DPI)   # kept clear for the SFW logo
    body.append(f'<!-- SFW logo space, keep clear: x={logo[0]:.0f} y={logo[1]:.0f} w={logo[2]:.0f} h={logo[3]:.0f} px -->')
    info = {"ciliate_w_in": round(target_w / DPI, 2), "ciliate_h_in": round(cil_h / DPI, 2),
            "line_scale": round(s, 3), "fine_line_px": round(LW * 0.8 * s, 2),
            "text_w_in": round(w2 / DPI, 2), "bottom_in": round((logo[1] + logo[3]) / DPI, 2), "logo_box_px": logo}
    return sfw.svg_doc(W, H, "\n".join(body)), info


def main():
    import json, mockup_tee as mk
    for scheme in ("light", "dark"):
        svg, info = build(scheme)
        base = f"tee-front-powered-by-protozoa-{scheme}"
        open(os.path.join(M, "source-svg", base + ".svg"), "w").write(svg)
        im = sfw.export_png(svg, os.path.join(M, "print-files", base + ".png"), W, H)
        info["off_palette"] = len(sfw.palette_check(im, [sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]]))
        info["thin_share"] = round(sfw.thin_line_check(im), 4)
        print(scheme, json.dumps(info))
        for gm in (["desert-dust"] if scheme == "light" else ["khaki", "black"]):
            sfw.preview(im, sfw.GARMENT[gm], os.path.join(M, "previews", f"tee-front-powered-by-protozoa-on-{gm}.png"))
            tee = mk.render(sfw.GARMENT[gm], False, [(os.path.join(M, "print-files", base + ".png"), -6.0, 3.0, 12.0)], 3)
            tee.save(os.path.join(M, "mockups", f"tee-{gm}-powered-by-protozoa.png"))


if __name__ == "__main__":
    main()
