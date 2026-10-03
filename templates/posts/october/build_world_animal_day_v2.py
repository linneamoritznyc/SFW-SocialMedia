"""World Animal Day carousel, version 2 (Sunday 4 October 2026, Instagram, 7 slides, 1080 x 1350).
Styled after the print trifold (Trifold Design/build/): cream panels, Montserrat Bold headings, Source Sans 3 body,
thin brown rules at low alpha, square photos, small faint captions, logo small in a corner, no decoration.
Photos: only the first version's (assets/photo/animals/). Icons: assets/icons/ (tools/icon_generate.py, flux-2-pro line icons).

python3 build_world_animal_day_v2.py  ->  04-10-2026-sun-ig-world-animal-day-v2.pptx
Photos: assets/photo/animals/ (Unsplash, credits.txt). Every element is a separate editable object.
"""
import os
from pptx.util import Emu, Pt
from lib import Deck, rect, text, crop, est_lines, ROOT, PX, DEEP, GREEN, CREAM, GOLD, INK, BROWN, FAINT, HEAD, BODY, rgb
from build_oct_01_10 import logo, save

W, H, M = 1080, 1350, 80          # slide and margin (the trifold's safe margin, scaled)
CW = W - 2 * M                    # column width
RED = "B23A2E"
AN = "assets/photo/animals/"
RULE_ALPHA = 22                   # the trifold's --rule: brown at 22%
ICON = "assets/icons/icon-{}-{}.png"

SOURCES = ("Sources: Soil Food Web School, Compost Manual: [LINK FROM CARLA]. "
           "Soil Food Web School, BioComplete Compost, Lecture 4: Thermophilic Composting (Part 2): https://pt.soilfoodweb.com/?p=2067. "
           "Miller et al. (2015). Ascariasis in humans and pigs on small-scale farms, Maine, USA, 2010 to 2013. "
           "Emerging Infectious Diseases, 21(2): https://doi.org/10.3201/eid2102.140048. "
           "USDA NRCS and Fairbanks Soil and Water Conservation District (2005). Composting Dog Waste: "
           "https://www.epa.gov/system/files/documents/2022-11/Composting-Dog-Waste-Booklet-Alaska.pdf. "
           "CDC (2025). About Toxoplasmosis: https://www.cdc.gov/toxoplasmosis/about/index.html. "
           "Course: https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production")


def credits():
    out = {}
    for line in open(os.path.join(ROOT, AN, "credits.txt")):
        f = line.rstrip("\n").split("\t")
        out[f[0].rsplit(".", 1)[0]] = dict(name=f[1].replace("Photo by ", "").replace(" on Unsplash", ""),
                                            page=f[3].replace("Photo page: ", ""))
    return out
CRED = credits()


def cred_line(*keys):
    return "Photo: " + ", ".join(CRED[k]["name"] for k in keys) + " on Unsplash"


def cred_note(*keys):
    return " ".join(f"Photo {k}.jpg: {CRED[k]['name']} on Unsplash, {CRED[k]['page']}." for k in keys)


def pic(s, key, x, y, w, h, fx=0.5, fy=0.5):
    p = crop(AN + key + ".jpg", int(w), int(h), fx, fy)
    return s.shapes.add_picture(p, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def rule(s, y, x=M, w=CW, color=BROWN, alpha=RULE_ALPHA):
    rect(s, x, y, w, 2, color, alpha=alpha)


def caption(s, y, t, color=FAINT, alpha=None, x=M, w=CW):
    text(s, x, y, w, 24, t, 14, color, BODY, alpha=alpha)


def source(s, t):
    text(s, M, H - M - 10, CW - 130, 24, t, 14, INK, BODY, alpha=70)


def icon(s, name, colour, x, y, h):
    p = os.path.join(ROOT, ICON.format(name, colour))
    from PIL import Image
    iw, ih = Image.open(p).size; w = h * iw / ih
    return s.shapes.add_picture(p, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX))), w


def label(s, y, t, fill, fg, ico):
    """Solid label: small line icon, then the text in 18 pt Montserrat Bold caps, tracking 2."""
    tw = len(t) * 18 * 1.3333 * 0.74
    w = 16 + 24 + 10 + tw + 16
    rect(s, M, y, w, 44, fill)
    icon(s, ico, "cream" if fg == CREAM else "deep", M + 16, y + 10, 24)
    text(s, M + 50, y, tw + 16, 44, t, 18, fg, HEAD, True, anchor="m", track=2)


def head(s, y, t, pt=60, color=DEEP, w=CW):
    """Headline; returns the y below it (measured, so a wrapped headline never runs into the body)."""
    h = est_lines(t, pt, w * 0.97, True) * pt * 1.3333 * 1.08 + 8
    text(s, M, y, w, h, t, pt, color, HEAD, True, spacing=1.05)
    return y + h


def body(s, y, t, pt=30, color=INK, w=CW, h=None):
    text(s, M, y, w, h or 300, t, pt, color, BODY, spacing=1.3)


def rich(s, x, y, w, h, runs, pt=30, color=INK, spacing=1.3):
    """One paragraph with several runs: (text, bold). Bold runs are Montserrat Bold, the rest Source Sans 3."""
    tb = s.shapes.add_textbox(0, 0, Emu(1), Emu(1)); tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.line_spacing = spacing
    for t, b in runs:
        r = p.add_run(); r.text = t; f = r.font
        f.size = Pt(pt); f.name = HEAD if b else BODY; f.bold = b; f.color.rgb = rgb(color)
    tb.left, tb.top, tb.width, tb.height = Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX))
    return tb


def build():
    d = Deck(name="04-10-2026-sun-ig-world-animal-day-v2")

    # 1 cover: full-bleed cow photo (its lower half is plain grass, calmer than the horse), Deep Green 40% on the bottom half
    s = d.slide(None, "Cover. Trifold-style v2. " + SOURCES + " " + cred_note("cow"), counter=False)
    pic(s, "cow", 0, 0, W, H, 0.5, 0.3)
    rect(s, 0, H / 2, W, H / 2, DEEP, alpha=40)
    text(s, M, 745, CW, 350, "Whose manure belongs in your compost?", 80, CREAM, HEAD, True, spacing=1.02)
    text(s, M, 1115, CW, 50, "Happy World Animal Day, October 4.", 30, CREAM, BODY)
    caption(s, H - 42, cred_line("cow"), CREAM, alpha=75)
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=True)

    # 2 manure: a high-nitrogen feedstock, three icon tiles
    s = d.slide(CREAM, "Three feedstock tiles with line icons from assets/icons/ (generated with flux-2-pro, no photos on this slide).",
                counter=False)
    head(s, M + 20, "Manure: a high-nitrogen feedstock", 64)
    body(s, 322, "A Soil Food Web thermophilic compost recipe combines three feedstocks: high-nitrogen material such as manure "
               "(about 10% in summer), green plant material (about 30%) and woody material (about 60%). Bedding, such as straw "
               "or wood shavings, counts toward the woody share.", 32, h=360)
    tw = (CW - 2 * 32) / 3; ty = 800; th_ = 230
    for i, (ico, cap) in enumerate([("manure-fork", "High nitrogen, 10%"), ("leaf", "Green, 30%"), ("wood-log", "Woody, 60%")]):
        x = M + i * (tw + 32)
        rect(s, x, ty, tw, th_, None, line=BROWN, lw=2)
        pc, iw = icon(s, ico, "deep", 0, 0, 130)
        pc.left = Emu(int((x + (tw - iw) / 2) * PX)); pc.top = Emu(int((ty + (th_ - 130) / 2) * PX))
        text(s, x - 16, ty + th_ + 16, tw + 32, 36, cap, 22, DEEP, HEAD, True, align="c")
    source(s, "Soil Food Web School, BioComplete Compost, Lecture 4")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 3 welcome in the pile: 4 x 2 grid
    grid = ["rabbit", "goat", "sheep", "alpaca", "guinea-pig", "horse", "cow", "chicken"]
    focus = {"rabbit": (0.5, 0.45), "goat": (0.55, 0.5), "sheep": (0.35, 0.5), "alpaca": (0.5, 0.3), "guinea-pig": (0.45, 0.5),
             "horse": (0.5, 0.55), "cow": (0.5, 0.4), "chicken": (0.5, 0.5)}
    s = d.slide(CREAM, "Plant-eaters and poultry. " + cred_note(*grid), counter=False)
    g = 8; tw = (CW - 3 * g) / 4
    for i, key in enumerate(grid):
        pic(s, key, M + (i % 4) * (tw + g), M + (i // 4) * (tw + g), tw, tw, *focus[key])
    gy = M + 2 * tw + g
    text(s, M, gy + 12, CW, 48, cred_line(*grid), 14, FAINT, BODY)
    label(s, gy + 84, "GOES IN", GREEN, CREAM, "check-mark")
    y = head(s, gy + 146, "Plant-eaters and poultry") + 12
    body(s, y, "Rabbit, goat, sheep, alpaca, guinea pig, horse, cow and chicken. Their manure is a great high-nitrogen "
                      "ingredient. Use it fresh, or dry it and store it until you build the pile.", h=260)
    source(s, "Soil Food Web School, Compost Manual")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 4 take extra care: pig
    s = d.slide(CREAM, "Pig. " + cred_note("pig"), counter=False)
    pic(s, "pig", M, M, CW, 600, 0.55, 0.45)
    caption(s, M + 612, cred_line("pig"))
    label(s, 740, "HOT PILE ONLY", GOLD, DEEP, "flame")
    y = head(s, 802, "Pig") + 10
    body(s, y, "Pig roundworm can infect people. Pig manure goes into a pile that completes the thermophilic requirements, "
                 "and raw pig manure stays away from produce.", h=240)
    source(s, "Miller et al. 2015, Emerging Infectious Diseases")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 5 keep out of food production: dog and cat
    s = d.slide(CREAM, "Dog and cat. " + cred_note("dog", "cat"), counter=False)
    pw = (CW - 16) / 2
    pic(s, "dog", M, M, pw, 420, 0.5, 0.45)          # shorter than slide 4's photo: this body runs to eight lines
    pic(s, "cat", M + pw + 16, M, pw, 420, 0.6, 0.55)
    caption(s, M + 432, cred_line("dog", "cat"))
    label(s, 556, "STAYS OUT", RED, CREAM, "crossed-circle")
    y = head(s, 618, "Dog and cat") + 10
    body(s, y, "Dog feces can carry roundworm (Toxocara) eggs. If swallowed, the larvae can migrate to the liver, lungs and eyes. "
               "Cat feces can carry Toxoplasma gondii, which people can also pick up from contaminated soil. USDA advises against "
               "using dog waste compost on food crops, even after hot composting, and against composting cat waste or litter at all.",
         h=380)
    source(s, "USDA NRCS 2005; CDC 2025")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 6 slow or hot
    s = d.slide(CREAM, "Two panels with a Food Web Green rule on the left edge, then the compost bin photo from the first version. "
                       "Thermometer icon: assets/icons/icon-compost-thermometer-green.png. " + cred_note("compost-4"), counter=False)
    y = head(s, M + 20, "Slow or hot, both work.", 64, w=CW - 130) + 24
    icon(s, "compost-thermometer", "green", W - M - 100, M + 24, 120)
    for lead, rest in [("Cold or static pile: ", "fine for plant-eater and poultry manure, on a longer timeline."),
                       ("Thermophilic pile: ", "above 55°C (131°F) for 3 days at the center. Turn it so every part passes "
                                               "through the hot center.")]:
        n = 2 if len(lead + rest) < 75 else 3
        ph = n * 30 * 1.3333 * 1.3 + 8
        rect(s, M, y, 4, ph, GREEN)
        rich(s, M + 28, y, CW - 28, ph, [(lead, True), (rest, False)])
        y += ph + 28
    pic(s, "compost-4", M, y + 20, CW, 1180 - (y + 20), 0.5, 0.6)
    caption(s, 1192, cred_line("compost-4"))
    source(s, "Soil Food Web School, Compost Manual")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 7 closing on Deep Green, logo large and centred in the lower third (trifold back panel)
    s = d.slide(DEEP, "Closing. Course: https://school.soilfoodweb.com/bundles/advanced-biocomplete-compost-production", counter=False)
    text(s, M, 200, CW, 320, "Learn to build the pile with us.", 72, CREAM, HEAD, True, spacing=1.05)
    rect(s, M, 540, 120, 4, GOLD)
    text(s, M, 580, CW, 120, "Advanced BioComplete Compost Production, at the Soil Food Web School. Link in bio.", 32, CREAM, BODY, spacing=1.3)
    lw = 240
    logo(s, (W - lw) / 2, 900 + (450 - lw * 668 / 743) / 2, lw, white=True)
    save(d, "04-10-2026-sun-ig-world-animal-day-v2.pptx")


if __name__ == "__main__":
    build()
