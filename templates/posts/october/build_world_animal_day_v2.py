"""World Animal Day carousel, version 2 (Sunday 4 October 2026, Instagram, 7 slides, 1080 x 1350).
Styled after the print trifold (Trifold Design/build/): cream panels, Montserrat Bold headings, Source Sans 3 body,
thin brown rules at low alpha, square photos, small faint captions, logo small in a corner, no decoration.

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

SOURCES = ("Sources: Soil Food Web School, Compost Manual: [LINK FROM CARLA]. "
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


def label(s, y, t, fill, fg):
    w = len(t) * 18 * 1.3333 * 0.74 + 2 * 18
    rect(s, M, y, w, 40, fill)
    text(s, M, y, w, 40, t, 18, fg, HEAD, True, align="c", anchor="m", track=2)


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

    # 1 cover: full-bleed barnyard photo, Deep Green overlay at 40% on the bottom half
    s = d.slide(None, "Cover. Trifold-style v2. " + SOURCES + " " + cred_note("barnyard"), counter=False)
    pic(s, "barnyard", 0, 0, W, H, 0.5, 0.5)
    rect(s, 0, H / 2, W, H / 2, DEEP, alpha=40)
    text(s, M, 745, CW, 350, "Whose manure belongs in your compost?", 80, CREAM, HEAD, True, spacing=1.02)
    text(s, M, 1115, CW, 50, "Happy World Animal Day, October 4.", 30, CREAM, BODY)
    caption(s, H - 42, cred_line("barnyard"), CREAM, alpha=75)
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=True)

    # 2 manure is one ingredient
    s = d.slide(CREAM, "Three ingredient tiles. " + cred_note("manure", "grass-clippings", "wood-chips"), counter=False)
    y = head(s, M + 20, "Manure is one\ningredient.", 64) + 16
    body(s, y, "In a Soil Food Web compost pile, manure is the high-nitrogen part. It goes in with green plant material "
                 "and woody material. Bedding counts as woody material.", 32, h=240)
    rule(s, 612)
    tw = (CW - 2 * 24) / 3; ty = 652
    for i, (key, cap, fx, fy) in enumerate([("manure", "High nitrogen", 0.6, 0.6), ("grass-clippings", "Green", 0.5, 0.5),
                                            ("wood-chips", "Woody", 0.5, 0.5)]):
        x = M + i * (tw + 24)
        pic(s, key, x, ty, tw, tw, fx, fy)
        text(s, x, ty + tw + 16, tw, 36, cap, 22, DEEP, HEAD, True)
    caption(s, ty + tw + 60, cred_line("manure", "grass-clippings", "wood-chips"))
    source(s, "Soil Food Web School, Compost Manual")
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
    label(s, gy + 84, "WELCOME IN THE PILE", GREEN, CREAM)
    y = head(s, gy + 142, "Plant-eaters and poultry") + 12
    body(s, y, "Rabbit, goat, sheep, alpaca, guinea pig, horse, cow and chicken. Their manure is a great high-nitrogen "
                      "ingredient. Use it fresh, or dry it and store it until you build the pile.", h=260)
    source(s, "Soil Food Web School, Compost Manual")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 4 take extra care: pig
    s = d.slide(CREAM, "Pig. " + cred_note("pig"), counter=False)
    pic(s, "pig", M, M, CW, 700, 0.55, 0.45)
    caption(s, M + 712, cred_line("pig"))
    label(s, 836, "TAKE EXTRA CARE", GOLD, DEEP)
    head(s, 894, "Pig")
    body(s, 988, "Pig roundworm can infect people. Pig manure goes into a pile that completes the thermophilic requirements, "
                 "and raw pig manure stays away from produce.", h=240)
    source(s, "Miller et al. 2015, Emerging Infectious Diseases")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 5 keep out of food production: dog and cat
    s = d.slide(CREAM, "Dog and cat. " + cred_note("dog", "cat"), counter=False)
    pw = (CW - 16) / 2
    pic(s, "dog", M, M, pw, 700, 0.5, 0.45)
    pic(s, "cat", M + pw + 16, M, pw, 700, 0.5, 0.5)
    caption(s, M + 712, cred_line("dog", "cat"))
    label(s, 836, "KEEP OUT OF FOOD PRODUCTION", RED, CREAM)
    head(s, 894, "Dog and cat")
    body(s, 988, "Dog poop can carry roundworm, and cat poop can carry Toxoplasma. Keep both out of compost for food production.",
         h=240)
    source(s, "USDA NRCS 2005; CDC 2025")
    logo(s, W - M - 90, H - M - 90 * 668 / 743, 90, white=False)

    # 6 slow or hot
    s = d.slide(CREAM, "Two panels with a Food Web Green rule on the left edge, then a compost pile photo. "
                       "No steaming pile or compost thermometer was found on Unsplash; a garden fork in a compost pile is used instead. "
                       + cred_note("compost-fork"), counter=False)
    y = head(s, M + 20, "Slow or hot, both work.", 60) + 24
    for lead, rest in [("Cold or static pile: ", "fine for plant-eater and poultry manure, on a longer timeline."),
                       ("Thermophilic pile: ", "above 55°C (131°F) for 3 days at the center. Turn it so every part passes "
                                               "through the hot center.")]:
        n = 2 if len(lead + rest) < 75 else 3
        ph = n * 30 * 1.3333 * 1.3 + 8
        rect(s, M, y, 4, ph, GREEN)
        rich(s, M + 28, y, CW - 28, ph, [(lead, True), (rest, False)])
        y += ph + 28
    pic(s, "compost-fork", M, y + 20, CW, 1180 - (y + 20), 0.5, 0.6)
    caption(s, 1192, cred_line("compost-fork"))
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
