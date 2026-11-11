"""Soil organisms drawn in code as engraved line art.

Every function draws straight into print pixels (300 dpi) and returns an SVG string.
Line widths are given in print px and never go below sfw.MIN_LINE_PX (0.5 pt).
Anatomy notes are next to each function; they follow standard light-microscope descriptions.
"""
import math
import numpy as np
from shapely.geometry import Polygon, Point, LineString
from shapely.ops import unary_union
from shapely import affinity
import sfw

MIN = sfw.MIN_LINE_PX + 0.4          # 2.5 px: comfortably above 0.5 pt


def lw(v):
    return max(v, MIN)


# ------------------------------------------------------------------ geometry helpers
def smooth(pts, n=200):
    """Catmull-Rom through pts, returns n points."""
    p = np.asarray(pts, float)
    if len(p) < 3:
        return np.linspace(p[0], p[-1], n)
    p = np.vstack([2 * p[0] - p[1], p, 2 * p[-1] - p[-2]])
    out = []
    segs = len(p) - 3
    for i in range(segs):
        p0, p1, p2, p3 = p[i:i + 4]
        for t in np.linspace(0, 1, max(2, n // segs), endpoint=False):
            t2, t3 = t * t, t * t * t
            out.append(0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t2 + (-p0 + 3 * p1 - 3 * p2 + p3) * t3))
    out.append(p[-2])
    return np.array(out)


def d_of(pts, close=False):
    pts = np.asarray(pts)
    s = "M" + "L".join(f"{x:.1f},{y:.1f}" for x, y in pts)
    return s + ("Z" if close else "")


def stroke(d, color, w, cap="round", extra=""):
    return f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{lw(w):.2f}" stroke-linecap="{cap}" stroke-linejoin="round"{extra}/>'


def fill(d, color, rule="evenodd"):
    return f'<path d="{d}" fill="{color}" fill-rule="{rule}"/>'


def poly_d(geom):
    out = []
    for g in getattr(geom, "geoms", [geom]):
        if g.is_empty or g.geom_type != "Polygon":
            continue
        out.append(d_of(np.array(g.exterior.coords)[:-1], True))
        for r in g.interiors:
            out.append(d_of(np.array(r.coords)[:-1], True))
    return "".join(out)


def outline(geom, color, w):
    return stroke(poly_d(geom), color, w)


def hatch(geom, angle, spacing, w, color, min_len=None):
    """Engraver's parallel lines clipped to geom. spacing >= line + 3.5 px so lines stay open in print."""
    if geom is None or geom.is_empty:
        return ""
    spacing = max(spacing, lw(w) + 3.5)
    minx, miny, maxx, maxy = geom.bounds
    cx, cy = (minx + maxx) / 2, (miny + maxy) / 2
    R = math.hypot(maxx - minx, maxy - miny) / 2 + 2
    ca, sa = math.cos(math.radians(angle)), math.sin(math.radians(angle))
    segs = []
    for o in np.arange(-R, R, spacing):
        l = LineString([(cx - ca * R - sa * o, cy - sa * R + ca * o), (cx + ca * R - sa * o, cy + sa * R + ca * o)])
        x = l.intersection(geom)
        for s in getattr(x, "geoms", [x]):
            if s.geom_type == "LineString" and s.length > (min_len or 2 * lw(w)):
                (x0, y0), (x1, y1) = s.coords[0], s.coords[-1]
                segs.append(f"M{x0:.1f},{y0:.1f}L{x1:.1f},{y1:.1f}")
    return stroke("".join(segs), color, w) if segs else ""


def stipple(geom, n, r, color, rng, bias=None):
    """n dots of radius r inside geom; bias(x, y) in 0..1 thins them out."""
    if geom.is_empty or n <= 0:
        return ""
    r = max(r, MIN / 2 + 0.2)
    minx, miny, maxx, maxy = geom.bounds
    pts, tries = [], 0
    from shapely.prepared import prep
    pg = prep(geom)
    while len(pts) < n and tries < n * 40:
        tries += 1
        x, y = rng.uniform(minx, maxx), rng.uniform(miny, maxy)
        if bias is not None and rng.random() > bias(x, y):
            continue
        if pg.contains(Point(x, y)):
            pts.append((x, y))
    return "".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{color}"/>' for x, y in pts)


def shade_crescent(geom, dx, dy, k=0.86):
    """The shadow side of a shape, light from the upper left."""
    c = geom.centroid
    inner = affinity.translate(affinity.scale(geom, k, k, origin=c), -dx, -dy)
    return geom.difference(inner)


def tube(centerlines, width):
    """Union of buffered centerlines (hyphae, filaments)."""
    return unary_union([LineString(c).buffer(width / 2, 16) for c in centerlines])


def along(line, step):
    """Points and unit tangents every `step` along a LineString."""
    out = []
    for s in np.arange(step / 2, line.length, step):
        p = np.array(line.interpolate(s).coords[0]); q = np.array(line.interpolate(min(s + 1, line.length)).coords[0])
        t = q - p; n = np.linalg.norm(t)
        if n == 0:
            continue
        out.append((p, t / n))
    return out


# ------------------------------------------------------------------ bacteria
def rod(cx, cy, L, W, ang, color, w, rng=None, dots=True):
    """Rod bacterium (bacillus): capsule with stippled nucleoid."""
    r = W / 2; h = max(L / 2 - r, 0.1)
    body = affinity.translate(affinity.rotate(LineString([(-h, 0), (h, 0)]).buffer(r, 24), ang, origin=(0, 0)), cx, cy)
    s = outline(body, color, w)
    if dots and rng is not None and W > 8 * w:
        inner = body.buffer(-1.8 * w)
        s += stipple(inner, int(inner.area / (14 * w * w)), w * 0.6, color, rng)
    return s, body


def coccus_colony(cx, cy, R, n, rcell, color, w, rng, solid=False):
    """Colony of cocci: small circles packed in a rounded cluster (stipple when tiny)."""
    out = []
    for _ in range(n):
        a = rng.uniform(0, 2 * math.pi); d = R * math.sqrt(rng.random())
        x, y = cx + d * math.cos(a), cy + d * math.sin(a) * 0.75
        if solid or rcell < 3 * w:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{max(rcell, MIN / 2 + .2):.1f}" fill="{color}"/>')
        else:
            out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{rcell:.1f}" fill="none" stroke="{color}" stroke-width="{lw(w):.2f}"/>')
    return "".join(out)


# ------------------------------------------------------------------ fungi
def hyphae(lines, width, color, w, septa=True, septa_step=None, solid=False):
    """Septate fungal hyphae: tubes with cross walls. lines = list of point lists (already smooth)."""
    shape = tube(lines, width)
    if solid:
        return fill(poly_d(shape), color), shape
    s = outline(shape, color, w)
    if septa:
        step = septa_step or width * 2.6
        segs = []
        for c in lines:
            ln = LineString(c)
            for p, t in along(ln, step)[1:-1]:
                n = np.array([-t[1], t[0]]) * (width / 2 - w * 0.4)
                a, b = p - n, p + n
                segs.append(f"M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}")
        s += stroke("".join(segs), color, w * 0.9)
    return s, shape


def branching(start, direction, length, rng, depth=2, spread=34, wiggle=0.08, shrink=0.62):
    """A main strand that branches `depth` times. Returns list of smooth point lists."""
    out = []

    def grow(p, ang, L, d):
        pts = [np.array(p, float)]
        n = 6
        a = ang
        for i in range(n):
            a += rng.normal(0, wiggle)
            pts.append(pts[-1] + L / n * np.array([math.cos(a), math.sin(a)]))
        out.append(smooth(pts, 60))
        if d > 0:
            for frac in (0.35, 0.7)[:max(1, d)]:
                bp = pts[int(frac * n)]
                side = rng.choice([-1, 1])
                grow(bp, ang + side * math.radians(spread + rng.uniform(-8, 8)), L * shrink * (1 - frac * 0.3), d - 1)

    grow(start, math.radians(direction), length, depth)
    return out


# ------------------------------------------------------------------ protists
def colpoda(cx, cy, size, rot, color, accent, rng, detail=1.0, w=3.0):
    """Colpoda (soil ciliate): kidney shape, concave side with oral vestibulum, somatic cilia fringe,
    food vacuoles, macronucleus. size = body length in px."""
    A, Bh = size / 2, size * 0.36
    th0, depth, wid = 1.5 * math.pi - 0.28, Bh * 0.29, 0.42
    pts = []
    for t in np.linspace(0, 2 * math.pi, 300, endpoint=False):
        x, y = A * math.cos(t), Bh * math.sin(t)
        if x < 0:
            y *= 1 - 0.10 * (-x / A)
        dt = (t - th0 + math.pi) % (2 * math.pi) - math.pi
        y += depth * math.exp(-(dt / wid) ** 2)
        pts.append((x, y))
    body = Polygon(pts)
    notch = np.array(pts[int(th0 / (2 * math.pi) * 300)])
    s = []
    nuc = Point(0.16 * A, 0.18 * Bh).buffer(0.2 * Bh)
    vac = [Point(fx * A, fy * Bh).buffer(r * Bh) for fx, fy, r in
           [(-0.5, 0.05, .11), (-0.25, 0.42, .12), (0.45, -0.35, .11), (0.5, 0.4, .1), (-0.1, -0.2, .09)][:max(2, int(5 * detail))]]
    pocket = LineString([tuple(notch + (0, -Bh * .07)), tuple(notch + (A * 0.05, Bh * 0.33))]).buffer(Bh * 0.1).intersection(body)
    keep = unary_union([nuc.buffer(w * 3), pocket.buffer(w * 3)] + [v.buffer(w * 3) for v in vac])
    if detail >= 0.6:
        s.append(hatch(shade_crescent(body, A * .1, Bh * .16).difference(keep), 38, 6 + 8 * detail, w * .85, color))
    if detail >= 0.9:  # kineties as dotted rows
        inner = body.buffer(-Bh * .06).difference(keep)
        dots = []
        for k in np.linspace(-0.9, 0.9, 11):
            for x in np.arange(-A, A, max(9 * w, size / 60)):
                u = x / A
                y = k * Bh * math.sqrt(max(0, 1 - u * u)) * .95 + .1 * Bh * (1 - u * u)
                if inner.contains(Point(x, y)):
                    dots.append((x, y))
        s.append("".join(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{lw(w) * .62:.1f}" fill="{color}"/>' for x, y in dots))
    s.append(outline(nuc, color, w * 1.6))
    s.append(stipple(nuc.buffer(-w * 2), int(nuc.area / (60 * w * w)), w * .6, color, rng))
    for v in vac:
        s.append(outline(v, color, w * 1.2))
        if detail >= 0.6:
            s.append(hatch(v.buffer(-w * 2), 30, 6 * w, w * .8, color))
    s.append(hatch(pocket, 70, 3.2 * w, w * .85, color))
    s.append(outline(body, color, w * 2.4))
    ring = LineString(pts + [pts[0]])
    N = int(np.clip(size / 3.2, 60, 380))
    L = max(size * 0.07, 5 * w)
    cil = []
    for i, (p, t) in enumerate(along(ring, ring.length / N)):
        n = np.array([t[1], -t[0]])
        if body.contains(Point(p + n * 2)):
            n = -n
        bend = math.radians(30 + 10 * math.sin(i / N * 2 * math.pi * 14))
        dvec = n * math.cos(bend) + t * math.sin(bend)
        e, c = p + dvec * L, p + n * L * .6
        cil.append(f"M{p[0]:.1f},{p[1]:.1f}Q{c[0]:.1f},{c[1]:.1f} {e[0]:.1f},{e[1]:.1f}")
    s.append(stroke("".join(cil), color, w))
    return f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot})">{"".join(s)}</g>'


def flagellate(cx, cy, size, rot, color, rng, w=3.0):
    """Bodo (kinetoplastid soil flagellate): small bean-shaped cell, two unequal flagella from an anterior
    pocket, one forward, one trailing; nucleus and kinetoplast. No cilia."""
    A, Bh = size * 0.32, size * 0.17
    pts = [(A * math.cos(t), Bh * math.sin(t) * (1 + 0.18 * math.cos(t))) for t in np.linspace(0, 2 * math.pi, 120, endpoint=False)]
    body = Polygon(pts)
    s = [hatch(shade_crescent(body, A * .12, Bh * .2, .8), 40, 5 * w, w * .85, color),
         outline(body, color, w * 2)]
    s.append(outline(Point(A * 0.1, 0).buffer(Bh * .38), color, w * 1.2))
    s.append(f'<circle cx="{-A * .55:.1f}" cy="{-Bh * .1:.1f}" r="{lw(w) * 1.3:.1f}" fill="{color}"/>')
    root = np.array([-A * .92, -Bh * .3])
    fwd = smooth([root, root + (-A * .4, -Bh * .7), root + (-A * .85, -Bh * .55), root + (-A * 1.15, -Bh * .9)], 60)
    trail = smooth([root, root + (A * .3, Bh * 1.2), root + (A * 1.1, Bh * 1.45), root + (A * 1.9, Bh * 1.25),
                    root + (A * 2.5, Bh * 1.55), root + (A * 2.9, Bh * 1.3)], 90)
    s.append(stroke(d_of(fwd), color, w * 1.2) + stroke(d_of(trail), color, w * 1.2))
    return f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot})">{"".join(s)}</g>'


def heliozoan(cx, cy, size, color, rng, w=3.0, n_axo=40):
    """Actinophrys (sun animalcule): spherical cell with a foamy, vacuolated periphery, central nucleus,
    and many straight, stiff axopodia radiating out, each with tiny granules."""
    R = size * 0.27
    body = Point(0, 0).buffer(R, 64)
    s = [outline(body, color, w * 2)]
    placed = []
    for k in range(400):
        if len(placed) >= (26 if size > 300 else 9):
            break
        a = rng.uniform(0, 2 * math.pi); d = R * rng.uniform(.5, .8)
        rr = R * rng.uniform(.1, .15) * (1 if size > 300 else 1.4)
        c = np.array([d * math.cos(a), d * math.sin(a)])
        if all(np.linalg.norm(c - q) > rr + qr + 2 * lw(w) for q, qr in placed) and d + rr < R * .93:
            placed.append((c, rr))
            s.append(outline(Point(*c).buffer(rr), color, w))
    s.append(outline(Point(0, 0).buffer(R * .3), color, w * 1.4))
    s.append(f'<circle cx="0" cy="0" r="{R * .1:.1f}" fill="{color}"/>')
    ax = []
    gran = []
    for i in range(n_axo):
        a = i / n_axo * 2 * math.pi + rng.normal(0, .03)
        L = size * rng.uniform(.2, .23)
        p0 = np.array([math.cos(a), math.sin(a)]) * R
        p1 = p0 + np.array([math.cos(a), math.sin(a)]) * L
        ax.append(f"M{p0[0]:.1f},{p0[1]:.1f}L{p1[0]:.1f},{p1[1]:.1f}")
        if size > 300:
            for f in (.35, .65):
                g = p0 + (p1 - p0) * f
                gran.append(f'<circle cx="{g[0]:.1f}" cy="{g[1]:.1f}" r="{lw(w) * .75:.1f}" fill="{color}"/>')
    s.append(stroke("".join(ax), color, w))
    s.append("".join(gran))
    return f'<g transform="translate({cx:.1f},{cy:.1f})">{"".join(s)}</g>'


def amoeba(cx, cy, size, rot, color, rng, w=3.0):
    """Naked lobose amoeba: irregular cell with blunt lobopodia, clear ectoplasm rim, granular
    endoplasm, one nucleus, one contractile vacuole."""
    R = size * 0.3
    lobes = [(0.15, .85), (1.25, .32), (2.4, .22), (3.6, .4), (4.7, .28), (5.5, .18)]
    pts = []
    for t in np.linspace(0, 2 * math.pi, 240, endpoint=False):
        r = R * (0.62 + sum(h * math.exp(-(((t - c + math.pi) % (2 * math.pi) - math.pi) / (.36 + .25 * h)) ** 2) for c, h in lobes))
        pts.append((r * math.cos(t), r * math.sin(t)))
    body = Polygon(pts).buffer(R * .1, 32).buffer(-R * .1, 32)
    endo = body.buffer(-R * .13)
    nuc = Point(R * .1, -R * .05).buffer(R * .17)
    cv = Point(-R * .35, R * .3).buffer(R * .13)
    s = [hatch(shade_crescent(body, R * .08, R * .1, .88), 35, max(6 * w, size / 40), w * .85, color),
         outline(body, color, w * 2),
         stroke(poly_d(endo), color, w * .9, extra=f' stroke-dasharray="{lw(w) * 2.5:.1f} {lw(w) * 2.5:.1f}"'),
         stipple(endo.difference(nuc.buffer(w * 2)).difference(cv.buffer(w * 2)), int(endo.area / (90 * w * w)), w * .6, color, rng),
         outline(nuc, color, w * 1.5), f'<circle cx="{R * .1:.1f}" cy="{-R * .05:.1f}" r="{R * .06:.1f}" fill="{color}"/>',
         outline(cv, color, w * 1.1)]
    return f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot})">{"".join(s)}</g>'


def arcella(cx, cy, size, color, rng, w=3.0):
    """Arcella (testate amoeba), seen from above: round, domed brown shell (test) with a finely
    punctate surface and a round central aperture with a rim."""
    R = size / 2
    shell = Point(0, 0).buffer(R, 96)
    s = [outline(shell, color, w * 2.4), outline(shell.buffer(-R * .07), color, w)]
    # punctate surface: rings of small pits
    pits = []
    for ring_r in np.arange(R * .32, R * .88, max(R * .075, 4.5 * w)):
        n = int(2 * math.pi * ring_r / max(R * .075, 4.5 * w))
        off = rng.uniform(0, 1)
        for i in range(n):
            a = (i + off) / n * 2 * math.pi
            pits.append(f'<circle cx="{ring_r * math.cos(a):.1f}" cy="{ring_r * math.sin(a):.1f}" r="{lw(w) * .65:.1f}" fill="{color}"/>')
    s.append("".join(pits))
    s.append(hatch(shade_crescent(shell, R * .12, R * .14, .9), 40, max(5 * w, R / 14), w * .85, color))
    ap = Point(0, 0).buffer(R * .22, 64)
    s.append(outline(ap, color, w * 2) + outline(ap.buffer(R * .05), color, w))
    s.append(hatch(ap.buffer(-w * 2), -45, 4 * w, w * .85, color))
    return f'<g transform="translate({cx:.1f},{cy:.1f})">{"".join(s)}</g>'


# ------------------------------------------------------------------ worms
def worm_body(center, widths, head_round=True):
    """Polygon around a centerline with a width profile (list of half-widths per point)."""
    c = np.asarray(center)
    t = np.gradient(c, axis=0); t /= np.linalg.norm(t, axis=1)[:, None]
    n = np.stack([-t[:, 1], t[:, 0]], 1)
    left = c + n * np.asarray(widths)[:, None]
    right = c - n * np.asarray(widths)[:, None]
    return Polygon(np.vstack([left, right[::-1]])).buffer(0), n, t


def nematode(center, W, color, rng, w=3.0, detail=1.0):
    """Bacterial-feeding nematode (Rhabditida): smooth unsegmented body, blunt rounded lip region with
    no stylet, a tubular pharynx (corpus, isthmus) ending in a round basal bulb with a valve, granular
    intestine, pointed tail. center = smooth centerline from head to tail."""
    c = np.asarray(center); N = len(c)
    u = np.linspace(0, 1, N)
    half = W / 2 * np.minimum(1, np.sqrt(np.clip(u / 0.035, 0.02, 1)) * 0.6 + 0.4) * np.where(u > .82, np.clip((1 - u) / .18, .04, 1) ** 1.2, 1)
    body, n, t = worm_body(c, half)
    s = []
    i_bulb = int(N * .13)
    if detail >= .5:
        s.append(hatch(body.intersection(LineString(c - n * half[:, None] * .45).buffer(W * .28)), 80, max(4.2 * w, W / 6), w * .85, color))
    # pharynx: lumen line, corpus swelling, isthmus, basal bulb
    lum = c[2:i_bulb]
    s.append(stroke(d_of(lum), color, w))
    if detail >= .5:
        corp = worm_body(c[2:int(N * .07)], np.full(int(N * .07) - 2, W * .17))[0]
        s.append(outline(corp, color, w * .9))
    bulb = Point(c[i_bulb]).buffer(W * .24)
    s.append(outline(bulb, color, w * 1.3))
    if detail >= .5:
        v = c[i_bulb]; tt = t[i_bulb]; nn = n[i_bulb]
        for k in (-1, 1):
            a, b = v - tt * W * .1 + nn * k * W * .12, v + tt * W * .08
            s.append(stroke(f"M{a[0]:.1f},{a[1]:.1f}L{b[0]:.1f},{b[1]:.1f}", color, w))
    # intestine: granules between bulb and anus
    i0, i1 = i_bulb + int(N * .03), int(N * .84)
    gut = worm_body(c[i0:i1], half[i0:i1] * .55)[0]
    if detail >= .5:
        s.append(stipple(gut, int(gut.area / (40 * w * w) * detail), w * .65, color, rng))
    s.append(stroke(d_of(np.vstack([(c - n * half[:, None] * .55)[i0:i1]])), color, w * .8))
    s.append(stroke(d_of(np.vstack([(c + n * half[:, None] * .55)[i0:i1]])), color, w * .8))
    s.append(outline(body, color, w * 2.2))
    return "".join(s), body


def earthworm(center, W, color, rng, w=3.0, clitellum=(0.26, 0.36)):
    """Earthworm: cylindrical body ringed by segments (annuli), a smooth swollen saddle (clitellum)
    a third of the way back, rounded head with prostomium, blunt tail."""
    c = np.asarray(center); N = len(c)
    u = np.linspace(0, 1, N)
    half = W / 2 * (0.75 + 0.25 * np.sin(np.clip(u, 0, 1) * math.pi) ** .4)
    half = half * np.where((u > clitellum[0]) & (u < clitellum[1]), 1.12, 1)
    half = half * np.minimum(1, np.sqrt(np.clip(u / .04, .05, 1)) * .5 + .5) * np.minimum(1, np.sqrt(np.clip((1 - u) / .04, .05, 1)) * .6 + .4)
    body, n, t = worm_body(c, half)
    seg = max(W * .26, 4 * lw(w))
    line = LineString(c)
    rings = []
    clit = []
    for s_ in np.arange(seg, line.length - seg * .5, seg):
        i = min(int(s_ / line.length * (N - 1)), N - 1)
        a = c[i] + n[i] * half[i] * .98; b = c[i] - n[i] * half[i] * .98
        mid = c[i] + t[i] * half[i] * .18
        d = f"M{a[0]:.1f},{a[1]:.1f}Q{mid[0]:.1f},{mid[1]:.1f} {b[0]:.1f},{b[1]:.1f}"
        (clit if clitellum[0] < u[i] < clitellum[1] else rings).append(d)
    s = [hatch(body.intersection(LineString(c - n * half[:, None] * .8).buffer(W * .16)), 75, max(5 * w, W / 7), w * .85, color),
         stroke("".join(rings), color, w)]
    i0, i1 = int(N * clitellum[0]), int(N * clitellum[1])
    cb = worm_body(c[i0:i1], half[i0:i1] * 1.0)[0]
    s.append(hatch(cb, 20, max(4.5 * w, W / 9), w * .9, color))
    s.append(outline(cb, color, w * 1.4))
    s.append(outline(body, color, w * 2.2))
    return "".join(s), body


# ------------------------------------------------------------------ arthropods
def oribatid(cx, cy, size, rot, color, rng, w=3.0):
    """Oribatid mite, dorsal view: rounded, glossy notogaster (dome), a smaller prodorsum in front,
    two club-shaped sensilli, four pairs of jointed legs, a few setae."""
    L = size
    noto = Point(0, L * .12).buffer(L * .3).intersection(Point(0, L * .12).buffer(L * .3))
    noto = affinity.scale(noto, 1.0, 1.12)
    pro = affinity.scale(Point(0, -L * .27).buffer(L * .16), 1, 1.05)
    s = []
    legs = []
    for side in (-1, 1):
        for k, (ang, ln) in enumerate([(-130, .36), (-160, .3), (160, .3), (125, .38)]):
            base = np.array([side * L * (.17 if k < 2 else .22), -L * .27 + k * L * .12 + (0 if k < 2 else L * .1)])
            a = math.radians(ang if side < 0 else 180 - ang)
            pts = [base]
            seglen = L * ln / 4
            for j in range(4):
                a += side * math.radians(-12 if k < 2 else 12)
                pts.append(pts[-1] + seglen * np.array([math.cos(a), math.sin(a)]))
            pl = np.array(pts)
            legs.append(LineString(pl).buffer(max(L * .022, 2.2 * w) * 1.0, 8))
            for j, p in enumerate(pl[1:-1]):
                s.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{max(L * .028, 2.6 * w):.1f}" fill="none" stroke="{color}" stroke-width="{lw(w):.2f}"/>')
            tip = pl[-1]
            s.append(stroke(f"M{tip[0]:.1f},{tip[1]:.1f}l{math.cos(a) * L * .04:.1f},{math.sin(a) * L * .04:.1f}", color, w))
    s.insert(0, "".join(outline(g, color, w * 1.3) for g in legs))
    dome = noto
    s.append(f'<path d="{poly_d(dome)}" fill="none" stroke="{color}" stroke-width="{lw(w * 2.4):.2f}"/>')
    s.append(hatch(shade_crescent(dome, L * .05, L * .06, .82), 40, max(5 * w, L / 30), w * .85, color))
    # glossy highlight left clear, upper left
    pro = pro.difference(dome.buffer(w * 2))
    s.append(outline(pro, color, w * 2))
    s.append(hatch(shade_crescent(pro, L * .03, L * .04, .8), 40, max(5 * w, L / 30), w * .85, color))
    for side in (-1, 1):  # sensilli
        b = np.array([side * L * .1, -L * .2])
        e = b + np.array([side * L * .1, -L * .1])
        s.append(stroke(f"M{b[0]:.1f},{b[1]:.1f}L{e[0]:.1f},{e[1]:.1f}", color, w))
        s.append(f'<circle cx="{e[0]:.1f}" cy="{e[1]:.1f}" r="{max(L * .02, 1.6 * w):.1f}" fill="{color}"/>')
    if size > 300:
        for k in range(6):  # notogastral setae
            p = np.array([(-1) ** k * L * .14 * (1 + k // 2 * .3), L * (.0 + k // 2 * .14)])
            s.append(stroke(f"M{p[0]:.1f},{p[1]:.1f}l{(-1) ** k * L * .03:.1f},{L * .02:.1f}", color, w))
    return f'<g transform="translate({cx:.1f},{cy:.1f}) rotate({rot})">{"".join(s)}</g>'


def mite_leg(base, direction, length, width, color, rng, w=3.0):
    """One arthropod leg entering the field: five tapering, jointed segments with setae and a
    claw at the tip (scale joke: at 400x a mite leg is huge)."""
    a = math.radians(direction)
    p = np.array(base, float)
    s = []
    bends = [0, 10, -14, 18, -10]
    ws = [1, .86, .74, .6, .46]
    segs = [.26, .24, .2, .17, .13]
    pts = [p]
    for k in range(5):
        a += math.radians(bends[k])
        pts.append(pts[-1] + length * segs[k] * np.array([math.cos(a), math.sin(a)]))
    shapes = []
    for k in range(5):
        p0, p1 = pts[k], pts[k + 1]
        seg = LineString([p0, p1]).buffer(width * ws[k] / 2, 16)
        shapes.append(seg)
        s.append(hatch(shade_crescent(seg, width * .06, width * .08, .8), 50, max(5 * w, width / 9), w * .85, color))
        s.append(outline(seg, color, w * 2.2))
        tt = (p1 - p0) / np.linalg.norm(p1 - p0); nn = np.array([-tt[1], tt[0]])
        for j in range(4):  # setae
            q = p0 + (p1 - p0) * (0.25 + j * .18) + nn * width * ws[k] / 2 * (1 if j % 2 else -1)
            e = q + (tt * .8 + nn * (1 if j % 2 else -1) * .6) * width * .45
            s.append(stroke(f"M{q[0]:.1f},{q[1]:.1f}L{e[0]:.1f},{e[1]:.1f}", color, w * 1.1))
    tip, tt = pts[-1], (pts[-1] - pts[-2]) / np.linalg.norm(pts[-1] - pts[-2])
    nn = np.array([-tt[1], tt[0]])
    for k in (-1, 1):
        c1 = tip + tt * width * .35 + nn * k * width * .15
        e = tip + tt * width * .25 + nn * k * width * .35
        s.append(stroke(f"M{tip[0]:.1f},{tip[1]:.1f}Q{c1[0]:.1f},{c1[1]:.1f} {e[0]:.1f},{e[1]:.1f}", color, w * 1.6))
    return "".join(s), unary_union(shapes)


# ------------------------------------------------------------------ roots and symbionts
def root_tip(top, length, W, color, rng, w=3.0, hairs=True, hair_len=None, direction=90, cells=True):
    """Root tip: root cap of loose layered cells at the apex, a smooth elongation zone, then a zone of
    long fine root hairs. Cell files run lengthwise. direction 90 = growing downward."""
    a = math.radians(direction)
    d = np.array([math.cos(a), math.sin(a)]); n = np.array([-d[1], d[0]])
    top = np.array(top, float)
    u = np.linspace(0, 1, 120)
    half = W / 2 * np.where(u < .82, 1 - .08 * u, np.sqrt(np.clip((1 - u) / .18, 0, 1)) * .92)
    c = top + np.outer(u * length, d)
    body, nn, tt = worm_body(c, half + 0.01)
    s = []
    if cells:
        files = []
        for f in np.linspace(-.7, .7, 5):
            pts = c + nn * (half * f)[:, None]
            files.append(d_of(pts[:int(len(pts) * .85)]))
        s.append(stroke("".join(files), color, w * .9))
        cross = []
        fr = np.linspace(-.7, .7, 5)
        lanes = list(zip(np.r_[-.95, fr], np.r_[fr, .95]))
        step = max(.07, 9 * lw(w) / length)
        for j, (f0, f1) in enumerate(lanes):
            for k in np.arange(0.04 + (j % 2) * step / 2, .8, step):
                i = int(k * 119)
                p, q = c[i] + nn[i] * half[i] * f0, c[i] + nn[i] * half[i] * f1
                cross.append(f"M{p[0]:.1f},{p[1]:.1f}L{q[0]:.1f},{q[1]:.1f}")
        s.append(stroke("".join(cross), color, w * .7))
    # root cap: nested arcs
    tip = c[-1]
    cap = []
    for k in range(1, 5):
        r = W * .14 * k
        cc = tip - d * r * 1.05
        arc = [cc + r * (math.cos(t) * d + math.sin(t) * n) for t in np.linspace(-1.25, 1.25, 30)]
        cap.append(d_of(arc))
    s.append(stroke("".join(cap), color, w * 1.1))
    s.append(hatch(body.intersection(LineString(c + nn * half[:, None] * .55).buffer(W * .22)), 20, max(5 * w, W / 8), w * .85, color))
    if hairs:
        hl = hair_len or W * 1.3
        hs = []
        for s_ in np.arange(.06, .5, max(.012, 4.5 * lw(w) / length)):
            i = int(s_ * 119)
            for side in (-1, 1):
                p = c[i] + nn[i] * side * half[i]
                L = hl * (0.55 + 0.45 * rng.random()) * min(1, (0.5 - s_) / .2 + .25)
                ang = side * math.radians(rng.uniform(55, 85))
                dirv = math.cos(ang) * nn[i] * side + math.sin(abs(ang)) * (-tt[i]) * .35
                dirv = dirv / np.linalg.norm(dirv)
                mid = p + dirv * L * .5 + tt[i] * L * .08 * rng.normal()
                e = p + dirv * L
                hs.append(f"M{p[0]:.1f},{p[1]:.1f}Q{mid[0]:.1f},{mid[1]:.1f} {e[0]:.1f},{e[1]:.1f}")
        s.append(stroke("".join(hs), color, w))
    s.append(outline(body, color, w * 2.2))
    return "".join(s), body, c, nn, half


def arbuscule(cx, cy, size, color, w, rng):
    """Arbuscule: a tiny tree of dichotomously branching fungal hyphae inside one cortex cell."""
    segs = []

    def br(p, a, L, d):
        e = p + L * np.array([math.cos(a), math.sin(a)])
        segs.append(f"M{p[0]:.1f},{p[1]:.1f}L{e[0]:.1f},{e[1]:.1f}")
        if d > 0 and L > 3 * lw(w):
            for k in (-1, 1):
                br(e, a + k * math.radians(32 + rng.uniform(-6, 6)), L * .66, d - 1)

    br(np.array([cx, cy + size * .45]), -math.pi / 2, size * .32, 4)
    return stroke("".join(segs), color, w)


def actino(cx, cy, size, color, rng, w=3.0):
    """Streptomyces (actinobacteria): very thin branching filaments (narrower than fungal hyphae, no
    septa visible) ending in coiled spiral chains of round spores."""
    s = []
    lines = branching((cx - size * .4, cy + size * .3), -30, size * .7, rng, depth=2, spread=40, wiggle=.12)
    s.append(stroke("".join(d_of(l) for l in lines), color, w * 1.3))
    for l in lines:
        tip, prev = l[-1], l[-6]
        dv = (tip - prev) / np.linalg.norm(tip - prev)
        nv = np.array([-dv[1], dv[0]])
        r = max(size * .035, 2.8 * lw(w) / 2 + 1)
        coils = 7
        for k in range(coils):
            ph = k * 1.15
            p = tip + dv * (k + 1) * r * 1.5 + nv * math.sin(ph) * r * 1.6
            s.append(f'<circle cx="{p[0]:.1f}" cy="{p[1]:.1f}" r="{r:.1f}" fill="none" stroke="{color}" stroke-width="{lw(w):.2f}"/>')
    return "".join(s)


def crumb(cx, cy, R, color, rng, w=3.0, density=1.0, seed_shape=None):
    """Soil aggregate: an irregular crumb built only from stipple, denser at the rim and lower right."""
    pts = []
    k = rng.uniform(0, 6)
    for t in np.linspace(0, 2 * math.pi, 60, endpoint=False):
        r = R * (1 + .18 * math.sin(3 * t + k) + .1 * math.sin(5 * t + 2 * k) + rng.normal(0, .03))
        pts.append((cx + r * math.cos(t), cy + r * math.sin(t) * .8))
    g = Polygon(pts).buffer(0)
    c = np.array([cx, cy])

    def bias(x, y):
        d = math.hypot(x - cx, (y - cy) / .8) / R
        return min(1, .25 + .9 * d ** 2 + .25 * ((x - cx) + (y - cy)) / R)

    n = int(g.area / (26 * w * w) * density)
    return stipple(g, n, w * .8, color, rng, bias), g


def star(cx, cy, r, color):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .42
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return fill(d_of(pts, True), color)


# ------------------------------------------------------------------ icon set (cast list, field-guide index)
def icon(key, cx, cy, size, color, rng):
    """One organism fitted to a size x size square centered on (cx, cy). Line weight scales with size
    but never drops below 0.5 pt."""
    h = size
    w = max(MIN, size / 60)
    if key == "fungal-hyphae":
        ls = branching((cx - h * .45, cy + h * .32), -35, h * .95, rng, depth=2, spread=38, wiggle=.06)
        return hyphae(ls, max(h * .08, 3.2 * w), color, w, septa_step=h * .16)[0]
    if key == "heliozoan":
        return heliozoan(cx, cy, h * 1.0, color, rng, w=w, n_axo=22)
    if key == "flagellate":
        return flagellate(cx + h * .12, cy, h * .8, -8, color, rng, w=w)
    if key == "amoeba":
        return amoeba(cx, cy, h * 1.1, 0, color, rng, w=w)
    if key == "ciliate":
        return colpoda(cx, cy, h * .82, -15, color, color, rng, detail=.3, w=w)
    if key == "nematode":
        c = smooth([(cx - h * .46, cy + h * .08), (cx - h * .26, cy - h * .2), (cx, cy - h * .1), (cx + h * .18, cy + h * .14),
                    (cx + h * .36, cy + h * .16), (cx + h * .47, cy - h * .06)], 300)
        return nematode(c, h * .085, color, rng, w=w, detail=.4)[0]
    if key == "oribatid-mite":
        return oribatid(cx, cy + h * .04, h * .88, 0, color, rng, w=w)
    if key == "mycorrhiza":
        s = [root_tip((cx - h * .5, cy - h * .02), h * .98, h * .34, color, rng, w=w, hairs=False, direction=0)[0]]
        s.append(arbuscule(cx - h * .08, cy - h * .06, h * .28, color, w, rng))
        ls = [smooth([(cx + h * .02, cy + h * .14), (cx + h * .08, cy + h * .3), (cx + h * .25, cy + h * .4)], 40)]
        s.append(hyphae(ls, max(h * .05, 2.6 * w), color, w, septa=False)[0])
        s.append(outline(Point(cx + h * .33, cy + h * .4).buffer(h * .09), color, w * 1.4))
        return "".join(s)
    if key == "actinobacteria":
        return actino(cx, cy, h * .9, color, rng, w=w)
    if key == "earthworm":
        c = smooth([(cx - h * .46, cy + h * .12), (cx - h * .22, cy - h * .16), (cx + h * .05, cy - h * .1), (cx + h * .26, cy + h * .12),
                    (cx + h * .46, cy - h * .04)], 300)
        return earthworm(c, h * .14, color, rng, w=w)[0]
    if key == "root-tip":
        return root_tip((cx, cy - h * .5), h * .98, h * .2, color, rng, w=w, hair_len=h * .2)[0]
    raise KeyError(key)
