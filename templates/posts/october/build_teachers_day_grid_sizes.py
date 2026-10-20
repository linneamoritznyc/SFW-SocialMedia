"""World Teachers' Day: the last slide (everyone) in six different grid sizes, to choose from (Linnea, 6 Oct 2026).
Same background, bunting, title, logo and soil as the final carousel; only the grid changes.

python3 templates/posts/october/build_teachers_day_grid_sizes.py
"""
from lib import Deck, rect, text
from build_oct_01_10 import logo, save
from build_teachers_day_v2 import portrait
from build_teachers_day_v3 import bunting
from build_teachers_day_v4 import ORDER, soil
from build_teachers_day_final import bg_sage, NOTE, GREEN, INK, CREAM, W
from build_teachers_day_collage import gradient

TOP, BOT, MX = 340, 1200, 28          # grid area between the title and the soil


def label(m): return f"{m[0]} {m[1].split()[-1] if m[0] == 'Carla' else m[1]}"


def grid(s, rows, aspect=1.0, gap=10, names="below", round_=False, cell=None):
    """rows: people per row, e.g. [5, 5, 5] or [4, 4, 4, 3] (short rows are centred)."""
    cap = 40 if names == "below" else 0
    n = max(rows)
    if cell is None:
        cw = (W - 2 * MX - (n - 1) * gap) / n
        ch_max = (BOT - TOP - (len(rows) - 1) * gap) / len(rows) - cap
        cw = min(cw, ch_max / aspect)
    else: cw = cell
    ch = cw * aspect
    block = len(rows) * (ch + cap) + (len(rows) - 1) * gap
    y = TOP + (BOT - TOP - block) / 2; i = 0
    for k in rows:
        x = (W - k * cw - (k - 1) * gap) / 2
        for _ in range(k):
            m = ORDER[i]; i += 1
            portrait(s, m[5], m[6], x, y, cw, ch, round_=round_)
            if names == "below":
                text(s, x - 8, y + ch + 7, cw + 16, cap - 8, label(m), 17 if cw > 190 else 15, INK, "Source Sans 3", align="c")
            else:                                             # name on a soft dark fade inside the photo
                gradient(s, "1E140F", "1E140F", angle=90, x=x, y=y + ch - 70, w=cw, h=70, a1=0, a2=70)
                text(s, x + 4, y + ch - 40, cw - 8, 32, label(m), 17 if cw > 190 else 15, CREAM, "Source Sans 3", align="c")
            x += cw + gap
        y += ch + cap + gap


VARIANTS = [
    ("A  5 x 3 squares, names under", dict(rows=[5, 5, 5], gap=12)),
    ("B  5 x 3 squares, names on the photo, bigger", dict(rows=[5, 5, 5], gap=8, names="on")),
    ("C  5 x 3 tall photos (3:4), names on the photo, fills the space", dict(rows=[5, 5, 5], aspect=4 / 3, gap=8, names="on")),
    ("D  4-4-4-3 squares, names on the photo", dict(rows=[4, 4, 4, 3], gap=10, names="on")),
    ("E  4-4-4-3 squares, names under", dict(rows=[4, 4, 4, 3], gap=10)),
    ("F  5 x 3 circles, names under", dict(rows=[5, 5, 5], gap=14, round_=True)),
]

d = Deck(name="05-10-2026-mon-ig-teachers-day-grid-sizes")
for title, kw in VARIANTS:
    s = d.slide(None, "Grid " + title + "." + NOTE, counter=False); bg_sage(s); bunting(s)
    text(s, MX, 160, 760, 130, "Happy World Teachers' Day", 48, GREEN, "Montserrat", True, spacing=1.0)
    logo(s, W - MX - 150, 150, 150, white=False)
    grid(s, **kw)
    soil(s, 0)
save(d, "05-10-2026-mon-ig-teachers-day-grid-sizes.pptx")
