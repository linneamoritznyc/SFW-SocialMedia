"""World Animal Day poop carousel, Sunday 4 October 2026 (Instagram, 10 slides, 1080 x 1350).

python3 build_world_animal_day.py  ->  04-10-2026-sun-ig-world-animal-day.pptx
Photos: assets/photo/animals/ (Unsplash, credits.txt). Stickers: assets/collage/cutouts/ (tools/collage_generate.py).
Every element is a native, editable PowerPoint object; photos and stickers are separate pictures.
"""
import os, random, tempfile
from PIL import Image, ImageFilter
from pptx.util import Emu
from lib import (Deck, Tilt, _place, rect, rrect, oval, poly, text, crop, ROOT, PX,
                 DEEP, GREEN, CREAM, GLOW, INK, FAINT, HEAD, BODY, WHITE)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "04-10-2026-sun-ig-world-animal-day.pptx")
GRAIN = "assets/collage/paper-grain-cream.jpg"
CUT = "assets/collage/cutouts/"
ANIMALS = "assets/photo/animals/"
TMP = tempfile.mkdtemp(prefix="wad-")

# Traffic light: status colours match the paper dots (dot-yellow and dot-red are not brand colours,
# they exist only for this traffic light).
LIGHTS = {
    "green": (CUT + "dot-green-1.png", GREEN, CREAM, "EASY AND LOW RISK"),
    "yellow": (CUT + "dot-yellow-1.png", "D9A521", DEEP, "HOT COMPOST IT FIRST"),
    "red": (CUT + "dot-red-1.png", "B5382B", CREAM, "KEEP IT OUT OF FOOD COMPOST"),
}
PAPER = "FFFDF7"
SOURCE_NOTE = ("Source: Rynk et al., On-Farm Composting Handbook (NRAES-54), 1992; US EPA 40 CFR Part 503; "
               "CDC, Toxocariasis and Toxoplasmosis fact sheets [VERIFY with Wes].")


# ---------------------------------------------------------------- credits (from credits.txt, written at download)
def credits():
    out = {}
    for line in open(os.path.join(ROOT, ANIMALS, "credits.txt")):
        f = line.rstrip("\n").split("\t")
        out[f[0].rsplit(".", 1)[0]] = dict(name=f[1].replace("Photo by ", "").replace(" on Unsplash", ""),
                                            profile=f[2].replace("Profile: ", ""))
    return out
CRED = credits()


def cred_note(*keys):
    return " ".join(f"Photo ({k}): {CRED[k]['name']} on Unsplash, {CRED[k]['profile']}." for k in keys)


# ---------------------------------------------------------------- paper grain
def make_grain():
    p = os.path.join(ROOT, GRAIN)
    if os.path.exists(p): return
    random.seed(4)
    base = Image.new("L", (1080, 1350), 128)
    noise = Image.effect_noise((1080, 1350), 10).filter(ImageFilter.GaussianBlur(0.6))
    base = Image.blend(base, noise, 0.5)
    im = Image.new("RGB", (1080, 1350))
    px_ = base.load(); o = im.load()
    c = (0xF4, 0xF1, 0xEA)
    for y in range(1350):
        for x in range(1080):
            d = (px_[x, y] - 128) * 0.35
            o[x, y] = tuple(max(0, min(255, int(v + d))) for v in c)
    from PIL import ImageDraw
    dr = ImageDraw.Draw(im)
    for _ in range(260):   # paper fibres
        x, y = random.uniform(0, 1080), random.uniform(0, 1350); ln = random.uniform(6, 22)
        dx, dy = random.uniform(-1, 1) * ln, random.uniform(-1, 1) * ln
        dr.line([(x, y), (x + dx, y + dy)], fill=(222, 214, 198), width=1)
    im.save(p, quality=90)


# ---------------------------------------------------------------- collage pieces
def trimmed(rel):
    """Cutout PNG cropped to its visible pixels (so placement boxes hug the piece)."""
    out = os.path.join(TMP, os.path.basename(rel))
    if not os.path.exists(out):
        im = Image.open(os.path.join(ROOT, rel)).convert("RGBA")
        im.crop(im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox()).save(out)
    return out


def piece(s, rel, cx, cy, w, deg=0):
    """A cut-paper sticker or dried flower, centred at (cx, cy), w px wide."""
    p = trimmed(rel); iw, ih = Image.open(p).size; h = w * ih / iw
    pic = s.shapes.add_picture(p, 0, 0, Emu(1), Emu(1))
    _place(pic, cx - w / 2, cy - h / 2, w, h); pic.rotation = deg
    return pic


def tape(s, cx, cy, w=150, h=46, deg=-30):
    rect(s, cx - w / 2, cy - h / 2, w, h, GLOW, alpha=70, tl=Tilt(cx, cy, deg))


def polaroid(s, key, x, y, size, deg=0, credit_pt=17):
    """Square photo on a paper print with the Unsplash credit written in the bottom margin."""
    b, foot = size * 0.035, max(52, size * 0.1)
    fw, fh = size + 2 * b, size + b + foot
    tl = Tilt(x + fw / 2, y + fh / 2, deg)
    rect(s, x, y, fw, fh, PAPER, tl=tl, shadow=True)
    pic = s.shapes.add_picture(crop(ANIMALS + key + ".jpg", int(size), int(size), *FOCUS.get(key, (0.5, 0.5))), 0, 0, Emu(1), Emu(1))
    _place(pic, x + b, y + b, size, size, tl)
    c = CRED[key]
    text(s, x + b, y + b + size, size, foot, f"Photo: {c['name']} on Unsplash", credit_pt, FAINT, BODY,
         align="c", anchor="m", tl=tl)
    return x, y, fw, fh


# where to centre the square crop (fx, fy) so the animal stays in frame
FOCUS = {"rabbit": (0.5, 0.5), "goat": (0.5, 0.4), "sheep": (0.45, 0.5), "alpaca": (0.5, 0.35),
         "guinea-pig": (0.5, 0.5), "chicken": (0.5, 0.5), "cow": (0.5, 0.45), "horse": (0.5, 0.5),
         "pig": (0.5, 0.5), "dog": (0.5, 0.5), "cat": (0.5, 0.5), "compost-4": (0.5, 0.5)}


def status_pill(s, x, y, light, pt=24):
    _, fill, fg, lab = LIGHTS[light]
    w = len(lab) * pt * 1.3333 * 0.74 + 48; h = 60
    rrect(s, x, y, w, h, fill, radius=25)
    text(s, x, y, w, h, lab, pt, fg, HEAD, True, align="c", anchor="m", track=2)
    return h


def slide(d, note):
    s = d.slide(CREAM, note)
    s.shapes.add_picture(os.path.join(ROOT, GRAIN), 0, 0, Emu(1080 * PX), Emu(1350 * PX))
    return s


def animal_text(s, x, y, w, name, light, body, name_pt=64, body_pt=34, name_lines=1, pill_pt=24):
    # LibreOffice and PowerPoint set Montserrat at about 1.25 x the point size in px per line
    text(s, x, y, w, name_lines * name_pt * 1.3333 * 1.25, name, name_pt, DEEP, HEAD, True, spacing=1.05)
    y += name_lines * name_pt * 1.3333 * 1.2 + 10
    y += status_pill(s, x, y, light, pill_pt) + 22
    text(s, x, y, w, 1200 - y, body, body_pt, INK, BODY, spacing=1.3)


LOGO = "assets/logo/sfw-foundation-wordmark-240.png"   # new logo (Oct 2026), 240 px


def sfw_logo(s, x, y, w=200):
    s.shapes.add_picture(os.path.join(ROOT, LOGO), Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(w * 208 / 240 * PX)))


def mark(s, light, cx, cy, d):
    """Checkmark on the green dot, exclamation mark on the red one (drawn over the paper dot)."""
    k = d / 140
    if light == "green":
        poly(s, [(cx-38*k, cy+2*k), (cx-24*k, cy-12*k), (cx-8*k, cy+4*k), (cx+30*k, cy-34*k),
                 (cx+44*k, cy-20*k), (cx-8*k, cy+32*k)], CREAM)
    elif light == "red":
        text(s, cx - d/2, cy - d/2, d, d, "!", 78 * k, CREAM, HEAD, True, align="c", anchor="m", spacing=1.0)


def dot(s, light, cx, cy, d, deg=0):
    piece(s, LIGHTS[light][0], cx, cy, d, deg); mark(s, light, cx, cy, d)


C_TO_F = {55: 131, 68: 154}   # 55 C = 131 F, 68 C = 154.4 F
HOT = "🌡️ Hot pile: 55 to 68°C (131 to 154°F)"
TEMPS = {"green": "🌡️ Cold pile is fine. Hot pile: 55 to 68°C (131 to 154°F)",
         "yellow": HOT,
         "pig": "🌡️ At least 55°C (131°F), up to 68°C (154°F)",
         "red": "🌡️ Not for food compost at any temperature"}
TEMP_NOTE = (" Temperature line: 55 to 68°C from the takeaway; Fahrenheit converted (55°C = 131°F, 68°C = 154°F). "
             "'Cold pile is fine' for green manures [VERIFY with Wes].")


def temp_label(s, t, y=1212):
    w = min(920, len(t) * 26 * 1.3333 * 0.46 + 80); tl = Tilt(80 + w/2, y + 34, -1)
    rect(s, 80, y, w, 68, PAPER, tl=tl, shadow=True)
    text(s, 110, y, w - 40, 68, t, 26, DEEP, BODY, True, anchor="m", tl=tl)
    tape(s, 90, y + 8, 90, 32, -40)


# ================================================================ slides
def build():
    make_grain()
    d = Deck(name="04-10-2026-sun-ig-world-animal-day")

    # 1 cover: type only, collage pieces
    s = slide(d, "Cover. Sunday, October 4. World Animal Day: Whose poop goes in the compost? "
                 "CTA: none. Link: none. Idea: Stina (SLU). 12 slides. " + SOURCE_NOTE)
    piece(s, CUT + "dried-flowers-1-1.png", 150, 1160, 300, -18)
    piece(s, CUT + "dried-flowers-2-1.png", 985, 360, 170, 22)
    sfw_logo(s, 80, 80, 210)
    text(s, 80, 290, 900, 80, "World Animal Day", 52, GREEN, HEAD, True)
    text(s, 80, 395, 840, 420, "Whose poop goes in your compost?", 80, DEEP, HEAD, True, spacing=1.05)
    text(s, 80, 815, 680, 110, "Happy World Animal Day, aka Animal Poop Day. 💩", 34, INK, BODY, spacing=1.3)
    piece(s, CUT + "poop-sticker-1.png", 560, 1110, 380, -6)
    for i, k in enumerate(("green", "yellow", "red")):
        dot(s, k, 900, 900 + i * 115, 100, 8 * i)

    # 2 the rule: type only
    s = slide(d, "The rule. Plant-eaters vs meat-eaters. Legend for the traffic-light dots. " + SOURCE_NOTE)
    piece(s, CUT + "dried-flowers-2-1.png", 110, 170, 170, -25)
    text(s, 80, 250, 920, 330, "The rule: plant-eaters' manure is compost gold.", 60, DEEP, HEAD, True, spacing=1.1)
    text(s, 80, 600, 880, 170, "Meat-eaters' poop carries parasites that can infect people.", 44, INK, BODY, spacing=1.25)
    rect(s, 80, 820, 120, 5, GREEN)
    for i, k in enumerate(("green", "yellow", "red")):
        y = 865 + i * 125
        dot(s, k, 130, y + 45, 95, 10 * i - 8)
        text(s, 210, y, 640, 90, LIGHTS[k][3].capitalize(), 34, DEEP, HEAD, True, anchor="m", spacing=1.05)
    piece(s, CUT + "poop-sticker-1.png", 940, 1230, 180, 10)

    # 3-10 one animal (or two) per slide
    def one(key, name, light, body, extra=None, note="", temp=None):
        s = slide(d, f"{name}. {cred_note(key)} {note}{SOURCE_NOTE}{TEMP_NOTE}")
        x, y, fw, fh = polaroid(s, key, 220, 95, 580, -2)
        tape(s, x + 40, y + 10, deg=-35); tape(s, x + fw - 40, y + 10, deg=35)
        dot(s, light, x + fw - 20, y + 80, 150, 12)
        if extra: extra(s, x, y, fw, fh)
        animal_text(s, 90, 785, 900, name, light, body, 64, 34)
        temp_label(s, TEMPS[temp or light])
        return s

    def two(keys, name, light, body, note="", name_pt=64, name_lines=1):
        s = slide(d, f"{name}. {cred_note(*keys)} {note}{SOURCE_NOTE}{TEMP_NOTE}")
        x1, y1, fw1, fh1 = polaroid(s, keys[0], 70, 170, 470, -4, 15)
        x2, y2, fw2, fh2 = polaroid(s, keys[1], 530, 120, 470, 3, 15)
        tape(s, x1 + 60, y1 + 10, deg=-30); tape(s, x2 + fw2 - 60, y2 + 10, deg=30)
        dot(s, light, x2 + fw2 - 30, y2 + fh2 - 10, 140, 12)
        piece(s, CUT + "dried-flowers-1-1.png", 90, 700, 160, -30)
        animal_text(s, 90, 780, 900, name, light, body, name_pt, 34, name_lines)
        temp_label(s, TEMPS[light])
        return s

    def dried(s, x, y, fw, fh): piece(s, CUT + "dried-flowers-1-1.png", x - 10, y + fh - 60, 190, -28)
    def cowflowers(s, x, y, fw, fh):
        piece(s, CUT + "dried-flowers-1-1.png", x + fw - 10, y + fh - 90, 200, 24)
        piece(s, CUT + "dried-flowers-2-1.png", x - 5, y + fh - 80, 160, -22)
    def flower2(s, x, y, fw, fh): piece(s, CUT + "dried-flowers-2-1.png", x - 5, y + fh - 90, 180, -20)

    CN = "carbon-to-nitrogen ratio (C:N)"
    one("rabbit", "Rabbit", "green", "Small dry pellets, rich in nitrogen, low odor. The easiest manure there is.", dried)
    two(("goat", "sheep"), "Goat and sheep", "green", f"Dry pellets, {CN} around 16:1. Mix with bedding and compost.")
    two(("alpaca", "guinea-pig"), "Alpaca, llama and guinea pig", "green",
        "Low-odor pellets. Guinea pig bedding composts right along with them.",
        note="No llama photo; the alpaca stands in for alpaca and llama. ", name_pt=56, name_lines=2)
    one("chicken", "Chicken", "yellow",
        f"The hottest manure: {CN} around 7:1, very high in nitrogen. Add lots of woody carbon or ammonia escapes.", flower2)
    one("cow", "Cow", "yellow", f"{CN[0].upper() + CN[1:]} around 19:1, very wet. Add woody material and let it breathe.", cowflowers)
    one("horse", "Horse", "yellow",
        f"{CN[0].upper() + CN[1:]} around 25:1 with bedding, drier. Weed seeds survive unless the pile gets hot.", dried)
    one("pig", "Pig", "yellow",
        f"{CN[0].upper() + CN[1:]} around 14:1. Pigs share parasites and bacteria with people, so the pile must reach 55°C.",
        flower2, temp="pig")
    two(("dog", "cat"), "Dog and cat", "red",
        "Dog poop can carry roundworm and cat poop can carry Toxoplasma. Keep both out of any compost for food.")

    # 11 how hot is hot: thermometer in Celsius and Fahrenheit
    s = slide(d, "Temperatures in Celsius and Fahrenheit. 55 to 68°C from the post; EPA line from 40 CFR Part 503, "
                 "Appendix B (process to further reduce pathogens) [VERIFY with Wes]. " + SOURCE_NOTE)
    text(s, 80, 130, 960, 110, "How hot is hot?", 72, DEEP, HEAD, True)
    ty = lambda c: 1100 - c * 9.6          # 0 to 80 °C on the tube
    rrect(s, 150, ty(80) - 20, 90, ty(0) - ty(80) + 40, PAPER, radius=45, line=DEEP, lw=3)
    rect(s, 150 + 25, ty(68), 40, ty(0) - ty(68) + 10, "D9A521")
    oval(s, 120, ty(0) - 20, 150, 150, "D9A521", line=DEEP, lw=3)
    rect(s, 110, ty(68), 170, ty(55) - ty(68), "D9A521", alpha=30)
    for c in (68, 55):
        rect(s, 240, ty(c) - 2, 50, 4, DEEP)
        text(s, 305, ty(c) - 32, 400, 64, f"{c}°C  ({C_TO_F[c]}°F)", 40, DEEP, HEAD, True, anchor="m")
    text(s, 305, ty(55) + 45, 735, 130, "Every 🟡 manure goes into this window before it goes near food crops.",
         32, INK, BODY, spacing=1.2)
    text(s, 305, ty(55) + 205, 735, 230, "US EPA rule: at least 55°C (131°F) for 3 days in a covered or aerated pile, "
         "or for 15 days with 5 turns in a windrow.", 32, INK, BODY, spacing=1.2)
    dot(s, "green", 350, 1085, 70); text(s, 400, 1050, 660, 70, "Cold pile is fine.", 30, DEEP, BODY, True, anchor="m")
    dot(s, "red", 350, 1170, 70); text(s, 400, 1135, 660, 70, "Not for food compost at any temperature.", 30, DEEP, BODY, True, anchor="m")
    piece(s, CUT + "dried-flowers-2-1.png", 985, 430, 130, 20)
    text(s, 80, 1265, 760, 40, "Sources: US EPA 40 CFR Part 503; Rynk et al., On-Farm Composting Handbook (NRAES-54), 1992.",
         15, FAINT, BODY)

    # 12 takeaway: type, one small compost print
    s = slide(d, "Takeaway. " + cred_note("compost-4") + " " + SOURCE_NOTE)
    text(s, 80, 130, 920, 110, "The takeaway", 76, DEEP, HEAD, True)
    text(s, 80, 270, 920, 470, "Any 🟡 manure needs a thermal pile balanced to roughly 25 to 30:1 carbon to nitrogen and "
         "held at 55 to 68°C (131 to 154°F) before it goes near food crops.", 44, INK, BODY, spacing=1.25)
    x, y, fw, fh = polaroid(s, "compost-4", 110, 790, 330, -5, 13)
    tape(s, x + fw / 2, y + 4, 130, 40, -8)
    piece(s, CUT + "dried-flowers-1-1.png", 560, 940, 210, 14)
    piece(s, CUT + "poop-sticker-1.png", 690, 1150, 140, -8)
    sfw_logo(s, 810, 1040, 190)
    text(s, 80, 1250, 760, 60, "Sources: Rynk et al., On-Farm Composting Handbook (NRAES-54), 1992; "
         "US EPA 40 CFR Part 503; CDC fact sheets on toxocariasis and toxoplasmosis.", 15, FAINT, BODY, spacing=1.2)

    d.finish(OUT, counters=False)   # no slide numbers on posts
    print("wrote", OUT)


if __name__ == "__main__":
    build()
