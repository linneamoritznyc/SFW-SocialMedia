"""Design 3: BACTERIA / AND FUNGI...  (tee left chest + tee back)

Front (left chest, 3.5 in): "bacteria" in Source Sans 3 Italic, three rod bacteria under it,
SOIL FOOD WEB under that.
Back (5 x 13 in column): film-credit cast list. Each line = 0.6 in organism icon + name.
The tail steps down in size (size steps, never a gradient) and the final ellipsis dots
shrink one by one. Slide label at the bottom: "The soil food web · cast list".

Usage: python3 design3_cast_list.py
Chosen candidates are listed in chosen.json. Organisms with no accepted art yet get a
dashed empty slot, and the file is written as a proof to previews/ only, never to print-files/.
"""
import json, os, sys
import sfw, organisms
from sfw import DPI, PT

M = sfw.ROOT
CAND = sys.argv[1] if len(sys.argv) > 1 else None
CHOSEN = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "chosen.json")))

# organism key, italic connector, NAME, size step
LINES = [
    ("fungal-hyphae", "and", "FUNGI", 0),
    ("heliozoan", None, "PROTOZOA", 0),
    ("flagellate", None, "FLAGELLATES", 0),
    ("amoeba", None, "AMOEBAE", 0),
    ("ciliate", None, "CILIATES", 0),
    ("nematode", None, "NEMATODES", 0),
    ("oribatid-mite", None, "MICROARTHROPODS", 1),
    ("mycorrhiza", None, "MYCORRHIZAE", 2),
    ("actinobacteria", None, "ACTINOBACTERIA", 3),
    ("earthworm", None, "EARTHWORMS", 4),
    ("root-tip", "and every root they feed", None, 5),
]
STEP = [1.0, 0.88, 0.77, 0.67, 0.58, 0.5]
DROP_BLOBS = {"fungal-hyphae"}

TEE_W, TEE_H = 3600, 4800
CHEST = 1050
COL_W, COL_H = 5 * DPI, 13 * DPI
ICON = 0.6 * DPI
GAP = 0.25 * DPI
TRACK = 40


def icon(key, size, color, x, cy):
    """Code-drawn organism (organisms.icon) in a size x size slot. Returns (svg, None-if-missing flag)."""
    import numpy as np
    import zlib; rng = np.random.default_rng(zlib.crc32(key.encode()))
    return organisms.icon(key, x + size / 2, cy, size, color, rng), 0.0


def build_back(scheme):
    line, accent = sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]
    x0 = (TEE_W - COL_W) / 2
    top = 1.0 * DPI
    size = sfw.fit_size("MICROARTHROPODS", "montserrat-800", (COL_W - ICON - GAP) / STEP[1], TRACK)
    size = min(size, sfw.fit_size("NEMATODES", "montserrat-800", COL_W - ICON - GAP, TRACK))
    label_h = 0.6 * DPI + 0.16 * DPI + 7 * PT * 0.7
    avail = COL_H - label_h - 0.5 * DPI
    weights = [0.5 + 0.5 * STEP[s] for *_, s in LINES]   # rows shrink with their step
    unit = avail / sum(weights)
    body, stats, y = [], {}, top
    for (key, conn, name, step), wgt in zip(LINES, weights):
        s = STEP[step]
        isz, fs = ICON * s, size * s
        cy = y + ICON / 2 * (0.5 + 0.5 * s)
        # icons right-aligned to the text column so every name starts on the same left edge
        svg, share = icon(key, isz, line, x0 + ICON - isz, cy)
        body.append(svg); stats[key] = share
        tx = x0 + ICON + GAP
        base = cy + 0.70 * fs / 2          # Montserrat cap height is 0.70 em
        if name:
            x = tx
            if conn:
                d, w, _ = sfw.text(conn, "source-sans-400-italic", fs * 1.05, x=x, y=base)
                body.append(f'<path fill="{accent}" d="{d}"/>'); x += w + 0.28 * fs
            d, _, _ = sfw.text(name, "montserrat-800", fs, x=x, y=base, tracking=TRACK)
            body.append(f'<path fill="{line}" d="{d}"/>')
        else:  # closing line, italic, then three dots that step down
            fsi = fs * 1.2
            d, w, _ = sfw.text(conn, "source-sans-400-italic", fsi, x=tx, y=base)
            body.append(f'<path fill="{accent}" d="{d}"/>')
            dx = tx + w + 0.10 * fsi
            for r in (0.060 * fsi, 0.046 * fsi, 0.034 * fsi):
                r = max(r, sfw.MIN_LINE_PX)
                body.append(f'<circle cx="{dx + r:.1f}" cy="{base - r:.1f}" r="{r:.1f}" fill="{accent}"/>')
                dx += 2 * r + 0.13 * fsi
        y += unit * wgt
    lab, bottom = sfw.slide_label(TEE_W / 2, top + COL_H - label_h, "The soil food web", "cast list", line)
    body.append(lab)
    return sfw.svg_doc(TEE_W, TEE_H, "\n".join(body)), stats, bottom


def build_front(scheme):
    line, accent = sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]
    W = CHEST
    tw = W - 2 * 0.12 * DPI
    fs = sfw.fit_size("bacteria", "source-sans-400-italic", tw)
    asc = 0.71 * fs                                  # height of the b ascender
    top = 0.10 * DPI
    d, _, _ = sfw.text("bacteria", "source-sans-400-italic", fs, x=W / 2, y=top + asc, anchor="middle")
    body = [f'<path fill="{line}" d="{d}"/>']
    y = top + asc + 0.14 * DPI
    p = sfw.part(os.path.join(M, "parts", "bacteria-rods.svg"), 1.7 * DPI, W - y - 0.42 * DPI)
    body.append(sfw.g(p["d"], accent, (W - p["w"]) / 2, y))
    y += p["h"] + 0.14 * DPI
    sz = 7 * PT
    d, _, _ = sfw.text("SOIL FOOD WEB", "montserrat-600", sz, x=W / 2, y=y + sz * 0.7, tracking=120, anchor="middle")
    body.append(f'<path fill="{line}" d="{d}"/>')
    bottom = y + sz * 0.7
    shift = (W - bottom - top) / 2            # center the block vertically in the square
    inner = "\n".join(body)
    return (sfw.svg_doc(W, W, f'<g transform="translate(0,{shift:.1f})">\n{inner}\n</g>'),
            {"bacteria-rods": p["thickened_share"]}, bottom + shift)


def main():
    report = {}
    for scheme in ("light", "dark"):
        for name, built, w, h in (("tee-chest-bacteria", build_front(scheme), CHEST, CHEST),
                                   ("tee-back-cast-list", build_back(scheme), TEE_W, TEE_H)):
            svg, stats, bottom = built
            complete = all(v is not None for v in stats.values())
            base = f"{name}-{scheme}"
            if complete:
                open(os.path.join(M, "source-svg", base + ".svg"), "w").write(svg)
                im = sfw.export_png(svg, os.path.join(M, "print-files", base + ".png"), w, h)
            else:  # proof only: missing organisms shown as dashed slots
                im = sfw.export_png(svg, os.path.join(sfw.ROOT, "previews", f"{base}-PROOF-print.png"), w, h)
                base += "-PROOF"
            garments = ["desert-dust"] if scheme == "light" else ["khaki", "black"]
            for gm in garments:
                sfw.preview(im, sfw.GARMENT[gm], os.path.join(M, "previews", f"{name}-on-{gm}{'' if complete else '-PROOF'}.png"))
            allowed = [sfw.SCHEME[scheme]["line"], sfw.SCHEME[scheme]["accent"]] + ([] if complete else ["#c0392b"])
            report[base] = {"complete": complete, "bottom_in": round(bottom / DPI, 2),
                            "off_palette": len(sfw.palette_check(im, allowed)),
                            "thin_share": round(sfw.thin_line_check(im), 4),
                            "missing": [k for k, v in stats.items() if v is None]}
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
