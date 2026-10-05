"""World Teachers' Day (Monday 5 October 2026): every mentor on the team, one card each.

Roster: Linnea's mentor list, 5 Oct 2026 (14 people). About lines are drafted from the team notes in this repo
(SFW All-Team Meeting, 17 Sep 2026: drafts/2026-10-06-before-soil-food-web.md, drafts/2026-10-01-favourite-microbe-series.md),
the mentor bios collected 30 Sep 2026 and content/community.json. Allison checks and fills them in
(templates/posts/october/05-10-2026-mon-ig-teachers-day-mentors.md). Mentors with no about line yet show name and
role only, so no placeholder text reaches the image.

Paper-cut field notes style: brand green and cream, cut-paper flowers and leaves (no creatures), nothing tilted.
Photo where we have one, otherwise a small flower arrangement.

python3 templates/posts/october/build_teachers_day_v2.py  ->  05-10-2026-mon-ig-teachers-day-v2.pptx
"""
import os
from PIL import Image, ImageFont
from pptx.util import Emu
from lib import Deck, rect, text, crop, ROOT, PX, HEAD, BODY
from build_oct_01_10 import logo, save

GREEN, CREAM, SAGE, PANEL, BLACK = "31662F", "F3F1EA", "B1BCB1", "E4E6DC", "1A1A1A"   # docs/brand-colors.md
GARA = "EB Garamond"
CUT = "assets/collage/cutouts/"
MENT = "assets/mentors-teachers-day/"
W, H, M = 1080, 1350, 80
F = {k: CUT + v for k, v in dict(tithonia="tithonia-flower-1.png", dried="dried-flowers-1-1.png",
                                 tansy="dried-flowers-2-1.png", sprig="leaf-sprig-paper-1.png",
                                 seedling="happy-seedling-1.png", dandelion="dandelion-short-root-1.png",
                                 frame="leaf-frame-1.png").items()}

# first, last, role, about (draft, None = Allison to add), advice (None = none on file), photo, focus, flowers
MENTORS = [
    ("Tommy", "Tepper", "Director of Education & Mentor", None, None, None, None, ("tithonia", "sprig")),
    ("Loida", "Vasquez", "Advanced Programs Lead & Mentor", None, None, "assets/photo/loida-teaching-3.jpg", (0.3, 0.25), ("dried",)),
    ("Carla", "Portugal", "Science Lead & Mentor",
     "PhD in Environmental Sciences. 20 years of environmental and farm consulting. Mentoring since 2019.",
     "Bare soil erodes. Living roots and cover hold the aggregates together.", MENT + "carla-portugal.jpg", (0.5, 0.25), ("tansy",)),
    ("Wesley", "Sanders", "Advanced Programs Mentor",
     "A farmer and agricultural journalist, then our first lab tech. Runs Foothill Biological Soil Health Services in "
     "California's Sierra Nevada foothills.",
     "Compost can look finished and still lack the biology you need. Check it under the microscope before you apply it.",
     MENT + "wes-sander.jpg", (0.5, 0.35), ("sprig",)),
    ("Casey", "Williams", "Advanced Programs Mentor",
     "Around ten years of farming and gardening. A long-time student, now teaching. Favourite microbe: rotifers.",
     None, None, None, ("seedling", "sprig")),
    ("Brian", "Daubenspeck", "Advanced Programs Mentor",
     "Manages orchards in California, after years in New Mexico. Favourite microbes: the small underdogs.",
     None, None, None, ("dried", "tithonia")),
    ("Isadora", "Schmidt", "Advanced Programs Mentor",
     "From Florianópolis, Brazil, now living in Spain. Favourite: lichens, though she loves all her microbes equally.",
     None, None, None, ("tansy", "seedling")),
    ("Aysen", "Ustunay", "Advanced Programs Mentor",
     "Favourite microbe: flagellates. She loves watching them as babies, running around.",
     None, None, None, ("dandelion", "sprig")),
    ("Dora", "Tkalec", "Advanced Programs Mentor", None, None, None, None, ("tithonia", "tansy")),
    ("Gerald", "Ramirez", "Advanced Programs Mentor",
     "An agronomist from the University of Costa Rica, who went looking for Dr. Elaine's teaching. Now he teaches it, "
     "from compost extracts to teas.",
     "Extracts pull organisms off the compost into solution, so you can apply biology across a whole field.",
     MENT + "gerald-ramirez.jpg", (0.5, 0.3), ("dried",)),
    ("Elena", "Kalli", "Advanced Programs Admin", None, None, None, None, ("seedling", "dried")),
    ("Ib", "Borup Pederson", "Advanced Programs Mentor", None, None, None, None, ("sprig", "dandelion")),
    ("Nick", "Padwick", "Advanced Programs Mentor",
     "Manages Ken Hill Estate, home of Wild Ken Hill, in West Norfolk, England. Farmers Weekly Farmer of the Year, 2009.",
     "I make 750 tons of compost a year. Biology works at any scale.", MENT + "Nick.png", (0.5, 0.06), ("tansy",)),
    ("Delvin", "Solkinson", "Permaculture Lead Teacher", None, None, None, None, ("tithonia", "dried", "sprig")),
]

_F = {}
FONTFILE = {(HEAD, True): "~/.fonts/Montserrat-Bold.ttf", (BODY, False): "~/.fonts/SourceSans3-Regular.ttf",
            (GARA, False): "~/.fonts/EBGaramond-Italic.ttf"}


def lines(t, pt, w, font, bold=False):
    k = (font, bold, pt)
    if k not in _F: _F[k] = ImageFont.truetype(os.path.expanduser(FONTFILE[(font, bold)]), int(pt * 1.3333))
    n, cur = 1, ""
    for word in t.split(" "):
        trial = (cur + " " + word).strip()
        if cur and _F[k].getlength(trial) > w * 0.97: n += 1; cur = word
        else: cur = trial
    return n


def para(s, x, y, w, t, sizes, color, font, bold=False, italic=False, sp=1.15, maxh=9999):
    for pt in sizes:
        h = lines(t, pt, w, font, bold) * pt * 1.3333 * 1.17 * sp
        if h <= maxh: break
    text(s, x, y, w, h + 10, t, pt, color, font, bold, italic=italic, spacing=sp)
    return y + h


def piece(s, rel, x, y, w, h):
    """Cut-paper piece fitted inside a box, straight."""
    im = Image.open(os.path.join(ROOT, rel)).convert("RGBA"); im = im.crop(im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox())
    out = os.path.join(ROOT, "renders", ".tmp", "td-" + os.path.basename(rel)); os.makedirs(os.path.dirname(out), exist_ok=True)
    im.thumbnail((800, 800)); im.save(out)
    r = min(w / im.width, h / im.height); pw, ph = im.width * r, im.height * r
    s.shapes.add_picture(out, Emu(int((x + (w - pw) / 2) * PX)), Emu(int((y + (h - ph) / 2) * PX)), Emu(int(pw * PX)), Emu(int(ph * PX)))


def half(s, y0, first, last, role, about, advice, photo, focus, flowers):
    """One mentor in a 560 px tall band: photo (or a labelled photo box) left, name, role and about right."""
    name = f"{'Dr. ' if last == 'Portugal' else ''}{first} {last}"
    px_, pw, ph = M, 400, 520
    if photo:
        s.shapes.add_picture(crop(photo, pw, ph, *focus), Emu(px_ * PX), Emu(y0 * PX), Emu(pw * PX), Emu(ph * PX))
    else:
        rect(s, px_, y0, pw, ph, PANEL)
        piece(s, F[flowers[0]], px_ + 100, y0 + 60, pw - 200, ph - 200)
        text(s, px_, y0 + ph - 110, pw, 80, f"PHOTO NEEDED\n{name}", 18, "8A8577", HEAD, True, align="c")
    x, w = M + pw + 40, W - 2 * M - pw - 40
    y = para(s, x, y0 + 10, w, name, (36, 32, 28), GREEN, HEAD, True, sp=1.0) + 6
    y = para(s, x, y, w, role.replace("AP ", "Advanced Programs "), (18,), BLACK, BODY) + 18
    room = y0 + ph - y
    if advice:
        y = para(s, x, y, w, f"“{advice}”", (24, 22, 20), BLACK, GARA, italic=True, maxh=room * 0.6) + 12
        room = y0 + ph - y
    if about:
        para(s, x, y, w, about, (19, 18, 17, 16), GREEN if advice else BLACK, BODY, maxh=room)


def build():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-v2")

    s = d.slide(GREEN, "Cover. World Teachers' Day, 5 October. Cut-paper flowers from the collage library.", counter=False)
    text(s, M, 120, W - 2 * M, 40, "WORLD TEACHERS' DAY · 5 OCTOBER", 20, SAGE, HEAD, True, track=3)
    text(s, M, 180, W - 2 * M, 360, "Happy World Teachers' Day.", 76, CREAM, HEAD, True, spacing=1.0)
    text(s, M, 540, W - 2 * M, 160, "Meet the mentors who teach our students to see soil.", 36, CREAM, GARA,
         italic=True, spacing=1.15)
    for i, f in enumerate(["tithonia", "dried", "tansy", "sprig", "seedling"]):
        piece(s, F[f], M + i * 184, 780, 170, 380)
    logo(s, W - M - 110, H - 70 - 110 * 668 / 743, 110, white=True)

    for k in range(0, len(MENTORS), 2):                      # two mentors per slide: 7 slides
        pair = MENTORS[k:k + 2]
        s = d.slide(CREAM, "Mentors: " + ", ".join(f"{m[0]} {m[1]}" for m in pair) + ". About and advice lines: drafts "
                    "from the team notes, confirm with each mentor (05-10-2026-mon-ig-teachers-day-mentors.md). Photo "
                    "boxes marked PHOTO NEEDED: drop the mentor's photo in (written consent).", counter=False)
        for i, m in enumerate(pair):
            half(s, M + i * 600, *m)
        rect(s, M, M + 560, W - 2 * M, 2, SAGE)
        text(s, W - M - 300, H - 60, 300, 30, "soilfoodweb.com", 18, GREEN, HEAD, True, align="r")

    s = d.slide(GREEN, "Closing: every mentor on the roster thanked by name.", counter=False)
    text(s, M, 140, W - 2 * M, 260, "Thank you to every mentor who teaches our students to see soil.", 52, CREAM, HEAD,
         True, spacing=1.08)
    names = " · ".join(f"{m[0]} {m[1]}" for m in MENTORS)
    text(s, M, 470, W - 2 * M, 380, names, 30, CREAM, GARA, italic=True, spacing=1.35)
    for i, f in enumerate(["sprig", "tansy", "tithonia", "dried"]):
        piece(s, F[f], M + i * 190, 930, 170, 300)
    logo(s, W - M - 110, H - 70 - 110 * 668 / 743, 110, white=True)
    save(d, "05-10-2026-mon-ig-teachers-day-v2.pptx")


if __name__ == "__main__":
    build()
