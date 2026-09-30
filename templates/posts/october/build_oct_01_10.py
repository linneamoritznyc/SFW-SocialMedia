"""October 1 to 10, 2026: every visual except Boubacar (skipped) and World Animal Day (built by build_world_animal_day.py).

python3 build_oct_01_10.py [post-number ...]   ->   templates/posts/october/DD-10-2026-*.pptx
Colours, fonts and templates from lib.py (the October spec). Every element is a separate editable object.
No slide numbers on any post.
"""
import os, sys
from PIL import Image
from pptx.util import Emu
from lib import (Deck, Tilt, _place, rect, rrect, oval, text, gradient, crop, fit, est_lines, ROOT, PX,
                 DEEP, GREEN, CREAM, GLOW, LIGHT, INK, FAINT, STRIPE, HEAD, BODY)

HERE = os.path.dirname(os.path.abspath(__file__))
GRAIN = "assets/collage/paper-grain-cream.jpg"          # 1080 x 1350, made by build_world_animal_day.py
CUT = "assets/collage/cutouts/"
MENT = "assets/mentors-teachers-day/"
LOGO_COLOR = "assets/logo/foundation-logo-color.png"     # 743 x 668
LOGO_WHITE = "assets/logo/foundation-logo-white.png"
RED = "B23A2E"
TMP = os.path.join(HERE, "..", "..", "..", "renders", ".tmp")


# ---------------------------------------------------------------- shared pieces
def pic(s, rel, x, y, w, h=None, deg=0):
    p = os.path.join(ROOT, rel)
    if h is None:
        iw, ih = Image.open(p).size; h = w * ih / iw
    sh = s.shapes.add_picture(p, 0, 0, Emu(1), Emu(1)); _place(sh, x, y, w, h); sh.rotation = deg
    return sh


def trimmed(rel):
    """Cutout cropped to its visible pixels, so the box hugs the piece."""
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(TMP, "trim-" + os.path.basename(rel))
    im = Image.open(os.path.join(ROOT, rel)).convert("RGBA")
    im.crop(im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox()).save(out)
    return out


def piece(s, rel, cx, cy, w, deg=0):
    """Collage cutout centred at (cx, cy), w px wide. Silently skipped if the cutout was never generated."""
    if not os.path.exists(os.path.join(ROOT, rel)):
        MISSING.add(rel); return None
    p = trimmed(rel); iw, ih = Image.open(p).size; h = w * ih / iw
    sh = s.shapes.add_picture(p, 0, 0, Emu(1), Emu(1)); _place(sh, cx - w / 2, cy - h / 2, w, h); sh.rotation = deg
    return sh


def fitpiece(s, rel, x, y, w, h, deg=0):
    """Cutout scaled to fit inside the box (x, y, w, h), centred."""
    if not os.path.exists(os.path.join(ROOT, rel)):
        MISSING.add(rel); return None
    iw, ih = Image.open(trimmed(rel)).size; r = min(w / iw, h / ih)
    return piece(s, rel, x + w / 2, y + h / 2, iw * r, deg)


def logo(s, x, y, w=90, white=True):
    return pic(s, LOGO_WHITE if white else LOGO_COLOR, x, y, w, w * 668 / 743)


def logo_br(s, white=True, w=90, W=1080, H=1350, m=60):
    return logo(s, W - m - w, H - m - w * 668 / 743, w, white)


def logo_box(s, x, y, w, h, radius=0):
    """Photo box with no photo yet: stripe paper with the colour logo in the middle."""
    (rrect(s, x, y, w, h, CREAM, radius=radius, pattern=STRIPE) if radius else rect(s, x, y, w, h, CREAM, pattern=STRIPE))
    lw = min(w, h) * 0.55
    logo(s, x + (w - lw) / 2, y + (h - lw * 668 / 743) / 2, lw, white=False)


def photo_box(s, rel, x, y, w, h, fx=0.5, fy=0.5, radius=0):
    """Real photo cropped to the box, or the logo box when rel is None."""
    if rel is None:
        return logo_box(s, x, y, w, h, radius)
    p = crop(rel, int(w), int(h), fx, fy)
    sh = s.shapes.add_picture(p, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    if radius:
        from pptx.enum.shapes import MSO_SHAPE
        from lxml import etree
        A = "http://schemas.openxmlformats.org/drawingml/2006/main"
        sh.auto_shape_type = MSO_SHAPE.ROUNDED_RECTANGLE
        g = sh._element.spPr.find("{%s}prstGeom" % A); av = g.find("{%s}avLst" % A)
        if av is None: av = etree.SubElement(g, "{%s}avLst" % A)
        etree.SubElement(av, "{%s}gd" % A, name="adj", fmla="val %d" % int(min(50000, radius / min(w, h) * 100000)))
    return sh


def cream(d, note, w=1080, h=1350):
    s = d.slide(CREAM, note, counter=False)
    s.shapes.add_picture(os.path.join(ROOT, GRAIN), 0, 0, Emu(w * PX), Emu(h * PX))
    return s


def dark(d, note, bg=DEEP):
    return d.slide(bg, note, counter=False)


def lh(pt, spacing=1.2):
    """Rendered line height in px (LibreOffice and PowerPoint set about 1.2 x the size per line)."""
    return pt * 1.3333 * 1.2 * spacing


from PIL import ImageFont
FONTS = {(HEAD, True): "Montserrat-Bold.ttf", (HEAD, False): "Montserrat-Regular.ttf",
         (BODY, True): "SourceSans3-Bold.ttf", (BODY, False): "SourceSans3-Regular.ttf"}


def text_width(t, pt, font=HEAD, bold=True):
    f = ImageFont.truetype(os.path.expanduser("~/.fonts/" + FONTS[(font, bold)]), int(pt * 1.3333))
    return f.getlength(t)


def n_lines(t, pt, w, font=HEAD, bold=True):
    """Lines after word wrap, measured with the real brand fonts (installed in ~/.fonts)."""
    n = 0
    for para in t.split("\n"):
        n += 1; line = ""
        for word in para.split(" "):
            trial = (line + " " + word).strip()
            if line and text_width(trial, pt, font, bold) > w: n += 1; line = word
            else: line = trial
    return n


def block(s, x, y, w, t, pt, color=DEEP, font=HEAD, bold=True, spacing=1.15, align="l"):
    """Text box sized from the measured number of lines; returns the bottom y."""
    n = n_lines(t, pt, w * 0.97, font, bold)
    h = n * lh(pt, spacing)
    text(s, x, y, w, h + 10, t, pt, color, font, bold, align=align, spacing=spacing)
    return y + h


def source_line(s, t, dark_bg=False, W=1080, H=1350, right_gap=200):
    text(s, 80, H - 95, W - 80 - right_gap, 40, t, 18, GLOW if dark_bg else FAINT, BODY, alpha=85 if dark_bg else None)


def unsplash_credit(fname):
    for line in open(os.path.join(ROOT, "assets/photo/unsplash-credits.txt")):
        f = line.rstrip("\n").split("\t")
        if f[0] == fname:
            return f"{f[1]} ({f[2].replace('Profile: ', '')})."
    return "[CREDIT MISSING]"


MISSING = set()
BUILT = []


def save(d, fname):
    path = os.path.join(HERE, fname)
    d.finish(path, counters=False)
    BUILT.append(fname)
    print("wrote", fname)


# ================================================================ 1. Coffee myth (Thu 1 Oct), template 2
def coffee():
    d = Deck(name="01-10-2026-thu-ig-coffee-myth")
    src = ("Sources: Hardgrove and Livesley, Urban Forestry and Urban Greening, 2016, https://doi.org/10.1016/j.ufug.2016.02.015; "
           "Summers et al., Journal of Bacteriology, 2012, https://doi.org/10.1128/JB.06637-11; "
           "US EPA, 40 CFR Part 503, https://www.ecfr.gov/current/title-40/chapter-I/subchapter-O/part-503.")
    s = dark(d, "Template 2A myth. " + src + " Photo: " + unsplash_credit("coffee-grounds-close-up.jpg"))
    photo_box(s, "assets/photo/coffee-grounds-close-up.jpg", 0, 0, 1080, 600, 0.5, 0.5)
    rect(s, 0, 600, 1080, 8, GLOW)
    text(s, 80, 740, 920, 90, "Myth:", 64, GLOW, HEAD, True, anchor="m")
    lines = ["“Coffee grounds", "acidify your soil.”"]
    for i, ln in enumerate(lines):          # one box per line, each with a thick Glow strikethrough through its middle
        y = 840 + i * 118
        text(s, 80, y, 960, 110, ln, 72, CREAM, HEAD, True, anchor="m", spacing=1.0)
        rect(s, 66, y + 55, text_width(ln, 72) + 28, 16, GLOW)
    logo_br(s, True)

    def plain(t, pt=66, note=""):
        s = cream(d, note)
        top = 675 - n_lines(t, pt, 920 * 0.97) * lh(pt, 1.12) / 2
        rect(s, 80, top - 60, 140, 10, GREEN)
        block(s, 80, top, 920, t, pt, DEEP, HEAD, True, 1.12)
        return s
    plain("Brewing extracts most of the acids. Spent grounds sit close to neutral pH.")
    plain("The real issue: residual caffeine and chlorogenic acids. Both are allelopathic. They inhibit germination and root growth.", 58)
    plain("Fresh grounds spread on beds have reduced plant growth in trials.")

    s = cream(d, "Microscopy: assets/microscopy/sfw-amoeba-still-square.jpg. The library has no bacteria-only image; "
                 "this Foundation still shows an amoeba (a bacteria feeder). Swap in a bacteria micrograph if Wes has one [IMAGE NEEDED].")
    photo_box(s, "assets/microscopy/sfw-amoeba-still-square.jpg", 80, 80, 920, 600, 0.5, 0.5, radius=28)
    block(s, 80, 740, 920, "Composting breaks them down. Some soil bacteria, like Pseudomonas putida CBB5, use caffeine as their only carbon and nitrogen source.",
          46, DEEP, HEAD, True, 1.15)

    cup = CUT + "coffee-cup-spilled-grounds-1.png"; have = os.path.exists(os.path.join(ROOT, cup))
    s = cream(d, "Collage: coffee-cup-spilled-grounds." + ("" if have else " Not generated (Replicate throttled): type-only [COLLAGE NEEDED: coffee cup with spilled grounds]."))
    t6 = "Grounds are a green, nitrogen-rich input. Mix with woody browns and compost them hot, at 55°C or more."
    pt6 = 50 if have else 62
    top6 = 150 if have else 675 - n_lines(t6, pt6, 920 * 0.97) * lh(pt6, 1.12) / 2
    if not have: rect(s, 80, top6 - 60, 140, 10, GREEN)
    block(s, 80, top6, 920, t6, pt6, DEEP, HEAD, True, 1.12)
    if have: fitpiece(s, cup, 190, 640, 700, 620, -4)

    s = cream(d, "Sources slide.")
    text(s, 80, 150, 920, 110, "Sources.", 72, DEEP, HEAD, True)
    y = 330
    for t in ("Hardgrove and Livesley, Urban Forestry and Urban Greening, 2016: https://doi.org/10.1016/j.ufug.2016.02.015",
              "Summers et al., Journal of Bacteriology, 2012: https://doi.org/10.1128/JB.06637-11",
              "US EPA, 40 CFR Part 503: https://www.ecfr.gov/current/title-40/chapter-I/subchapter-O/part-503"):
        block(s, 80, y, 880, t, 22, INK, BODY, False, 1.25); y += 140
    logo_br(s, False, 110)
    save(d, "01-10-2026-thu-ig-coffee-myth.pptx")


# ================================================================ 2 and 3. 1000 Farms study (Fri 2 Oct)
STUDY_SRC = ("Sources: Lundgren et al., Environmental Research: Food Systems, 2026, https://doi.org/10.1088/2976-601X/ae8f4e; "
             "Ecdysis Foundation press release, 17 September 2026, https://www.globenewswire.com/news-release/2026/09/17/3363925/0/en/"
             "regenerative-farming-outpaces-tech-based-carbon-capture-solutions-in-first-large-scale-systemic-study.html")
STUDY_LINE = "Lundgren et al. 2026, Environ. Res.: Food Syst."
FIELD = CUT + "field-cross-section-1.png"


def field(s, x, y, w, h):
    """Field cross-section collage; until it is generated, a stand-in from existing cut-paper pieces:
    ferns above for the cover crop, the fungal-hyphae cutout below for fungal threads and roots."""
    if os.path.exists(os.path.join(ROOT, FIELD)):
        return fitpiece(s, FIELD, x, y, w, h)
    rect(s, x + w * 0.05, y + h * 0.42, w * 0.9, h * 0.52, "4F3433")          # soil band, Soil Brown
    piece(s, "assets/collage/fern-green.png", x + w * 0.32, y + h * 0.3, w * 0.5, -8)
    piece(s, "assets/collage/fern-sage.png", x + w * 0.7, y + h * 0.3, w * 0.45, 190)
    piece(s, CUT + "fungal-hyphae-1.png", x + w * 0.5, y + h * 0.68, w * 0.55, 90)


def farms():
    d = Deck(name="02-10-2026-fri-ig-1000-farms-study")
    s = dark(d, "Template 2A. " + STUDY_SRC + " Collage: field cross-section. Stand-in from existing cutouts (ferns over a soil band with the fungal-hyphae cutout) until field-cross-section is generated [COLLAGE NEEDED].")
    rect(s, 0, 0, 1080, 640, CREAM)
    s.shapes.add_picture(os.path.join(ROOT, GRAIN), 0, 0, Emu(1080 * PX), Emu(640 * PX))
    field(s, 90, 30, 900, 590)
    rect(s, 0, 640, 1080, 8, GLOW)
    block(s, 80, 700, 920, "“A new study of working farms: the most regenerative farms stored 39% more carbon in their soil.”",
          52, CREAM, HEAD, True, 1.12)
    source_line(s, STUDY_LINE, True)
    logo_br(s, True)

    def plain(t, pt=50, note=""):
        s = cream(d, note)
        block(s, 80, 330, 920, t, pt, DEEP, HEAD, True, 1.15)
        source_line(s, STUDY_LINE)
        return s

    def big(num, rest, note=""):
        s = cream(d, "Template 5 big number. " + note)
        text(s, 40, 330, 1000, 300, num, 220, GREEN, HEAD, True, align="c", anchor="m", spacing=1.0)
        block(s, 100, 680, 880, rest, 54, DEEP, HEAD, True, 1.12, align="c")
        source_line(s, STUDY_LINE)
        return s

    plain("The 1000 Farms Initiative, led by Ecdysis Foundation, measured farms across North America, from the most conventional to the most regenerative.", 46)
    big("39%", "more total soil carbon on the most regenerative farms.")
    big("77%", "more total fungi in regenerative soils.")
    bird = CUT + "bird-beetle-wildflower-1.png"; have = os.path.exists(os.path.join(ROOT, bird))
    s = cream(d, "Collage: bird-beetle-wildflower." + ("" if have else " Not generated (Replicate throttled): type-only [COLLAGE NEEDED: bird, beetle and wildflower]."))
    block(s, 80, 150 if have else 330, 920, "More life everywhere: soil microbes, insects, plants and birds. The more biodiversity, the more carbon stored.",
          48, DEEP, HEAD, True, 1.15)
    if have: fitpiece(s, bird, 200, 620, 680, 580, 3)
    source_line(s, STUDY_LINE)
    plain("Regenerative yields matched national averages, and net profit per acre was similar.")
    plain("One practice alone changed nothing. Farms using a single regenerative practice looked like conventional farms. The whole system matters.", 46)

    s = dark(d, "Closing. Paper title: not reachable from this session (doi.org and the journal were blocked); "
                "fill in the exact title from the DOI page [PAPER TITLE NEEDED].")
    block(s, 80, 300, 920, "Read the paper: Lundgren et al., Environmental Research: Food Systems, 2026.", 56, CREAM, HEAD, True, 1.12)
    y = 700
    text(s, 80, y, 920, 40, "[PAPER TITLE NEEDED]", 24, RED, BODY, True); y += 60
    text(s, 80, y, 920, 40, "Environmental Research: Food Systems", 24, GLOW, BODY); y += 50
    text(s, 80, y, 920, 40, "https://doi.org/10.1088/2976-601X/ae8f4e", 24, GLOW, BODY)
    source_line(s, STUDY_LINE, True)
    logo_br(s, True)
    save(d, "02-10-2026-fri-ig-1000-farms-study.pptx")


def farms_li():
    d = Deck(1200, 627, name="02-10-2026-fri-li-1000-farms-study")
    s = d.slide(DEEP, "LinkedIn image. " + STUDY_SRC + " Right half: the slide 1 collage on Food Web Green so the white logo reads.",
                counter=False)
    rect(s, 600, 0, 600, 627, GREEN)
    field(s, 630, 40, 540, 460)
    text(s, 50, 150, 520, 2 * lh(64, 1.05) + 10, "39% more soil carbon", 64, CREAM, HEAD, True, spacing=1.05)
    text(s, 50, 150 + 2 * lh(64, 1.05) + 20, 500, 90, "on the most regenerative farms, 1000 Farms Initiative, 2026", 24, GLOW, BODY, spacing=1.2)
    logo_br(s, True, 90, 1200, 627, 30)
    save(d, "02-10-2026-fri-li-1000-farms-study.pptx")


# ================================================================ 5. World Teachers' Day trading cards (Mon 5 Oct)
MENTORS = [
    # name, role, advice, photo, (fx, fy), facts (based, since, background, known for)
    ("Tommy Tepper", "Director of Education & Mentor", None, None, None, ["[VERIFY]"] * 4),
    ("Loida Vasquez", "Advanced Programs Lead & Mentor", None, "assets/photo/loida-teaching-3.jpg", (0.3, 0.2), ["[VERIFY]"] * 4),
    ("Dr. Carla Portugal", "Science Lead & Mentor",
     "“Bare soil erodes. Living roots and cover hold the aggregates together.”", MENT + "carla-portugal.jpg", (0.5, 0.25),
     ["Brazil [VERIFY]", "2019", "PhD in Environmental Sciences, 20 years of environmental and farm consulting", "[VERIFY]"]),
    ("Wesley Sanders", "AP Mentor",
     "“Compost can look finished and still lack the biology you need. Check it under the microscope before you apply it.”",
     MENT + "wes-sander.jpg", (0.5, 0.35),
     ["Sierra Nevada foothills, California", "2020", "10 years as an agricultural journalist, then 10 years managing a farm",
      "Foothill Biological Soil Health Services"]),
    ("Casey Williams", "AP Mentor", None, None, None, ["[VERIFY]"] * 4),
    ("Brian Daubenspeck", "AP Mentor", None, None, None, ["[VERIFY]"] * 4),
    ("Isadora Schmidt", "AP Mentor", None, None, None, ["[VERIFY]"] * 4),
    ("Aysen Ustunay", "AP Mentor", None, None, None, ["[VERIFY]"] * 4),
    ("Dora Tkalec", "AP Mentor", None, None, None, ["[VERIFY]"] * 4),
    ("Gerald Ramirez", "AP Mentor",
     "“Extracts pull organisms off the compost into solution, so you can apply biology across a whole field.”",
     MENT + "gerald-ramirez.jpg", (0.5, 0.3),
     ["Costa Rica", "[VERIFY]", "Agronomist, University of Costa Rica", "[VERIFY]"]),
    ("Elena Kalli", "AP Admin", None, None, None, ["[VERIFY]"] * 4),
    ("Ib Borup Pederson", "AP Mentor", None, None, None, ["[VERIFY]"] * 4),
    ("Nick Padwick", "AP Mentor", "“I make 750 tons of compost a year. Biology works at any scale.”", MENT + "Nick.png", (0.5, 0.12),
     ["West Norfolk, England", "[VERIFY]", "Farmers Weekly Farm Manager and Farmer of the Year, 2009",
      "Managing Ken Hill Estate, home of Wild Ken Hill"]),
    ("Delvin Solkinson", "Permaculture Lead Teacher", None, None, None, ["[VERIFY]"] * 4),
]
LEAF_FRAME = CUT + "leaf-frame-1.png"   # not generated (Replicate throttled); leaf_frame() builds one from existing pieces


def leaf_frame(s, flip=False):
    """Leaf frame from cutouts already in the library: ferns, leaf sprigs and dried flowers around the edges."""
    P = [("assets/collage/fern-green.png", 300, 200, 520, -20), ("assets/collage/fern-sage.png", 800, 190, 460, 200),
         ("assets/collage/leaf-sprig-tan.png", 110, 640, 170, 4), ("assets/collage/leaf-sprig-blue.png", 975, 700, 160, -6),
         (CUT + "dried-flowers-1-1.png", 230, 1110, 330, -35), (CUT + "dried-flowers-2-1.png", 860, 1120, 280, 30),
         ("assets/collage/fern-green.png", 560, 1215, 420, 175)]
    for rel, cx, cy, w, deg in P:
        if flip: cy = 1350 - cy; deg = -deg
        piece(s, rel, cx, cy, w, deg)


class _G:
    """Lets lib drawing helpers draw into a group shape."""
    def __init__(self, grp, deck): self.shapes, self._deck = grp.shapes, deck


def card(d, name, role, advice, photo, focus, facts):
    note = (f"Trading card: {name}. Facts from the mentor bios collected on 30 Sep 2026 (soilfoodweb.com was blocked from this session); "
            "confirm every fact and the advice line with the mentor before posting.")
    if photo is None: note += f" [PHOTO NEEDED: {name}, headshot]"
    if photo and "carla" in photo: note += " Carla's headshot is only 499 px; ask for a larger file."
    if name == "Gerald Ramirez": note += " Bio also says 'Teaching the CLP and CTP courses' (left off: no acronyms in public text)."
    s = dark(d, note)
    grp = s.shapes.add_group_shape(); g = _G(grp, d)
    X, Y, W, H = 90, 55, 900, 1240            # card master: every card uses exactly these numbers
    rrect(g, X, Y, W, H, CREAM, radius=28, shadow=True)
    if photo:
        photo_box(g, photo, X + 36, Y + 36, W - 72, 560, *focus, radius=24)
    else:
        logo_box(g, X + 36, Y + 36, W - 72, 560, radius=24)
    npt = fit(name, W - 72, [56, 52, 48], 1, True)
    text(g, X + 36, Y + 612, W - 72, 80, name, npt, DEEP, HEAD, True, anchor="m")
    text(g, X + 36, Y + 695, W - 72, 40, role, 26, GREEN, BODY, True)
    adv = advice or "[ADVICE LINE NEEDED]"
    text(g, X + 36, Y + 752, W - 72, 230, adv, 34, DEEP if advice else RED, HEAD, True, spacing=1.12)
    labels = ("BASED IN", "TEACHING SINCE", "BACKGROUND", "KNOWN FOR")
    for i, (lab, val) in enumerate(zip(labels, facts)):
        cx = X + 36 + (i % 2) * 380; cy = Y + 990 + (i // 2) * 115
        text(g, cx, cy, 350, 26, lab, 15, GREEN, HEAD, True, track=2)
        text(g, cx, cy + 26, 350, 86, val, 18, INK, BODY, spacing=1.1)
    logo(g, X + W - 36 - 90, Y + H - 36 - 81, 90, white=False)
    grp.rotation = 3
    return s


def teachers():
    d = Deck(name="05-10-2026-mon-ig-teachers-day")
    src = "Source: mentor roster from Linnea, September 2026, and mentor bios on https://soilfoodweb.com. "
    s = dark(d, "Opening slide. " + src + "Leaf frame built from existing cutouts (ferns, leaf sprigs, dried flowers).")
    leaf_frame(s)
    block(s, 230, 470, 620, "Happy World Teachers' Day. Our mentors' best advice, in one line each.", 50, CREAM, HEAD, True, 1.12, align="c")
    logo_br(s, True)
    for m in MENTORS:
        card(d, *m)
    s = dark(d, "Closing slide. Leaf frame built from existing cutouts.")
    leaf_frame(s, flip=True)
    block(s, 230, 520, 620, "Thank you to every mentor who teaches our students to see soil.", 50, CREAM, HEAD, True, 1.12, align="c")
    logo_br(s, True)
    save(d, "05-10-2026-mon-ig-teachers-day.pptx")


# ================================================================ 6. World Habitat Day story (Mon 5 Oct), template 7
def habitat():
    d = Deck(1080, 1920, name="05-10-2026-mon-ig-story-habitat-day")
    s = dark(d, "Story. Source: Anthony, Bender and van der Heijden, PNAS, 2023, https://doi.org/10.1073/pnas.2304663120. "
                "Microscopy: assets/microscopy/testate-amoeba-encysting-40x-joy-kaluf.jpg (Joy Kaluf, per the file name). "
                "Leave y 1100 to 1450 empty for the poll sticker.")
    photo_box(s, "assets/microscopy/testate-amoeba-encysting-40x-joy-kaluf.jpg", 0, 0, 1080, 1920, 0.45, 0.5)
    rect(s, 0, 0, 1080, 1920, DEEP, alpha=50)
    y = block(s, 100, 600, 880, "The biggest habitat on Earth is under your feet.", 72, CREAM, HEAD, True, 1.1, align="c")
    block(s, 100, y + 40, 880, "More than half of all species live in soil.", 44, GLOW, BODY, False, 1.2, align="c")
    logo(s, (1080 - 180) / 2, 1500, 180, white=True)
    save(d, "05-10-2026-mon-ig-story-habitat-day.pptx")


# ================================================================ 7 to 10. Meet our mentors (single image, reused layout)
LEAF_CORNER = CUT + "leaf-frame-corner-1.png"


def make_leaf_corner():
    """Top-left corner of the post 5 leaf frame, saved as its own cutout for the mentor posts."""
    src = os.path.join(ROOT, LEAF_FRAME); out = os.path.join(ROOT, LEAF_CORNER)
    if os.path.exists(src) and not os.path.exists(out):
        im = Image.open(src).convert("RGBA"); w, h = im.size
        im.crop((0, 0, int(w * 0.45), int(h * 0.45))).save(out)


def mentor(d, photo, name, role, focus=(0.5, 0.3), note="", corner="br"):
    s = dark(d, note)
    photo_box(s, photo, 0, 0, 1080, 878, *focus)           # top 65%
    rect(s, 0, 878, 1080, 472, DEEP)
    sprig = CUT + "dried-flowers-2-1.png"            # the same sprig used in the post 5 leaf frame
    if corner == "br": piece(s, sprig, 985, 790, 190, 28)
    else: piece(s, sprig, 95, 110, 190, -28)
    rrect(s, 80, 920, 330, 60, GLOW, radius=30)
    text(s, 80, 920, 330, 60, "Meet our mentors", 24, DEEP, HEAD, True, align="c", anchor="m")
    npt = fit(name, 800, [60, 54, 50], 1, True)
    text(s, 80, 1010, 900, 90, name, npt, CREAM, HEAD, True, anchor="m")
    text(s, 80, 1105, 800, 50, role, 30, GLOW, BODY)
    logo_br(s, True)
    return s


def carla():
    d = Deck(name="06-10-2026-tue-ig-mentor-carla-portugal")
    mentor(d, MENT + "carla-portugal.jpg", "Dr. Carla Portugal", "Science Lead & Mentor", (0.5, 0.2),
           "First 'Meet our mentors' post; posts 8 to 10 reuse this layout. No photo of Carla at a microscope in the library; "
           "this is her headshot (499 px, upscaled: ask for a larger file or a microscope photo) [PHOTO NEEDED: higher resolution].")
    save(d, "06-10-2026-tue-ig-mentor-carla-portugal.pptx")


def nick():
    d = Deck(name="07-10-2026-wed-ig-mentor-nick-padwick")
    mentor(d, MENT + "Nick.png", "Nick Padwick", "AP Mentor", (0.5, 0.1),
           "Photo: assets/mentors-teachers-day/Nick.png (Nick in a field with a spade). No photo with his windrows or compost turner "
           "in the library; the Drive photo from Wild Soils, Nov 2024, is the same small group shot as assets/photo/carla-nicks-son-nick-eri-wild-soils-event-11-2024.jpg.",
           corner="tl")
    save(d, "07-10-2026-wed-ig-mentor-nick-padwick.pptx")


def wes():
    d = Deck(name="08-10-2026-thu-ig-mentor-wesley-sanders")
    mentor(d, MENT + "wes-sander.jpg", "Wesley Sanders", "AP Mentor", (0.5, 0.38),
           "Photo: assets/mentors-teachers-day/wes-sander.jpg (headshot outdoors). No photo of Wes at his microscope and no soil comparison "
           "video of his in assets/video/, so no still was used [PHOTO NEEDED: Wes at his microscope]. "
           "Name as given in the brief; the website and earlier posts spell it 'Wes Sander' [VERIFY].")
    save(d, "08-10-2026-thu-ig-mentor-wesley-sanders.pptx")


def gerald_caterina():
    d = Deck(name="09-10-2026-fri-ig-mentors-gerald-caterina")
    mentor(d, MENT + "gerald-teaching.jpg", "Gerald Ramirez", "AP Mentor", (0.22, 0.4),
           "Photo: assets/mentors-teachers-day/gerald-teaching.jpg (Gerald teaching a workshop). Confirm it is the Costa Rica workshop, "
           "March 2025, demonstrating liquid amendments [VERIFY]. Earlier posts spell his name Ramírez [VERIFY].")
    mentor(d, None, "Dr. Caterina Capri", "Advanced Programs Instructor", note="[PHOTO NEEDED: Caterina headshot from Allison]", corner="tl")
    save(d, "09-10-2026-fri-ig-mentors-gerald-caterina.pptx")


# ================================================================ 11. Soil Regenerators in the wild: Lisa Price (Sat 10 Oct), template 1
def lisa():
    d = Deck(name="10-10-2026-sat-ig-soil-regenerators-lisa-price")
    s = dark(d, "Template 1A. [PHOTO NEEDED: Lisa with her seedlings] Seedling-tray collage not generated (Replicate throttled) [COLLAGE NEEDED: seedling tray].")
    logo_box(s, 0, 0, 1080, 1350)
    gradient(s, 0, 743, 1080, 607, DEEP, 0, 92)
    rrect(s, 80, 80, 620, 70, DEEP, alpha=85, radius=35)
    text(s, 80, 80, 620, 70, "Soil Regenerators in the wild", 26, GLOW, HEAD, True, align="c", anchor="m")
    piece(s, CUT + "seedling-tray-1.png", 900, 330, 300, 8)
    rect(s, 80, 1056, 120, 4, LIGHT)
    text(s, 80, 1090, 820, 100, "Lisa Price, Australia", 64, CREAM, HEAD, True, anchor="m")
    logo_br(s, True)
    save(d, "10-10-2026-sat-ig-soil-regenerators-lisa-price.pptx")


POSTS = {1: coffee, 2: farms, 3: farms_li, 5: teachers, 6: habitat, 7: carla, 8: nick, 9: wes, 10: gerald_caterina, 11: lisa}

if __name__ == "__main__":
    for n in [int(a) for a in sys.argv[1:]] or POSTS:
        POSTS[n]()
    if MISSING: print("MISSING cutouts:", ", ".join(sorted(MISSING)))
