"""World Animal Day poop carousel, Sunday 4 October 2026 (Instagram, 10 slides, 1080 x 1350).

python3 build_world_animal_day.py  ->  04-10-2026-sun-ig-world-animal-day.pptx
Photos: assets/photo/animals/ (Unsplash, credits.txt). Stickers: assets/collage/cutouts/ (tools/collage_generate.py).
Every element is a native, editable PowerPoint object; photos and stickers are separate pictures.
"""
import os, random, tempfile
from PIL import Image, ImageFilter
from pptx.util import Emu
from lib import (Deck, Tilt, _place, rect, rrect, text, logo, crop, ROOT, PX,
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


def status_pill(s, x, y, light, pt=20):
    _, fill, fg, lab = LIGHTS[light]
    w = len(lab) * pt * 1.3333 * 0.74 + 40; h = 50
    rrect(s, x, y, w, h, fill, radius=25)
    text(s, x, y, w, h, lab, pt, fg, HEAD, True, align="c", anchor="m", track=2)
    return h


def slide(d, note):
    s = d.slide(CREAM, note)
    s.shapes.add_picture(os.path.join(ROOT, GRAIN), 0, 0, Emu(1080 * PX), Emu(1350 * PX))
    return s


def animal_text(s, x, y, w, name, light, body, name_pt=60, body_pt=34, name_lines=1, pill_pt=20):
    # LibreOffice and PowerPoint set Montserrat at about 1.25 x the point size in px per line
    text(s, x, y, w, name_lines * name_pt * 1.3333 * 1.25, name, name_pt, DEEP, HEAD, True, spacing=1.05)
    y += name_lines * name_pt * 1.3333 * 1.2 + 10
    y += status_pill(s, x, y, light, pill_pt) + 22
    text(s, x, y, w, 1300 - y, body, body_pt, INK, BODY, spacing=1.3)


# ================================================================ slides
def build():
    make_grain()
    d = Deck(name="04-10-2026-sun-ig-world-animal-day")

    # 1 cover: type only, collage pieces
    s = slide(d, "Cover. Sunday, October 4. World Animal Day: Whose poop goes in the compost? "
                 "CTA: none. Link: none. Idea: Stina (SLU). " + SOURCE_NOTE)
    piece(s, CUT + "dried-flowers-1-1.png", 150, 1150, 300, -18)
    piece(s, CUT + "dried-flowers-2-1.png", 985, 330, 180, 22)
    text(s, 80, 140, 800, 40, "WORLD ANIMAL DAY", 22, GREEN, HEAD, True, track=2)
    text(s, 80, 200, 840, 440, "Whose poop goes in your compost?", 84, DEEP, HEAD, True, spacing=1.05)
    text(s, 80, 680, 700, 110, "Happy World Animal Day, aka Animal Poop Day. 💩", 34, INK, BODY, spacing=1.3)
    piece(s, CUT + "poop-sticker-1.png", 560, 1010, 470, -6)
    for i, k in enumerate(("green", "yellow", "red")):
        piece(s, LIGHTS[k][0], 890, 800 + i * 120, 100, 8 * i)
    logo(s, outline=DEEP)

    # 2 the rule: type only
    s = slide(d, "The rule. Plant-eaters vs meat-eaters. Legend for the traffic-light dots. " + SOURCE_NOTE)
    piece(s, CUT + "dried-flowers-2-1.png", 110, 170, 170, -25)
    text(s, 80, 250, 920, 330, "The rule: plant-eaters' manure is compost gold.", 60, DEEP, HEAD, True, spacing=1.1)
    text(s, 80, 600, 880, 170, "Meat-eaters' poop carries parasites that can infect people.", 44, INK, BODY, spacing=1.25)
    rect(s, 80, 820, 120, 5, GREEN)
    for i, k in enumerate(("green", "yellow", "red")):
        y = 865 + i * 125
        piece(s, LIGHTS[k][0], 130, y + 45, 95, 10 * i - 8)
        text(s, 210, y, 640, 90, LIGHTS[k][3].capitalize(), 34, DEEP, HEAD, True, anchor="m", spacing=1.05)
    piece(s, CUT + "poop-sticker-1.png", 940, 1230, 180, 10)

    # 3-8 one animal (or two) per slide
    def one(key, name, light, body, extra=None, note=""):
        s = slide(d, f"{name}. {cred_note(key)} {note}{SOURCE_NOTE}")
        x, y, fw, fh = polaroid(s, key, 170, 110, 680, -2)
        tape(s, x + 40, y + 10, deg=-35); tape(s, x + fw - 40, y + 10, deg=35)
        piece(s, LIGHTS[light][0], x + fw - 20, y + 80, 160, 12)
        if extra: extra(s, x, y, fw, fh)
        animal_text(s, 90, 925, 900, name, light, body, 56, 32)
        return s

    def two(keys, name, light, body, note="", name_pt=56, name_lines=1):
        s = slide(d, f"{name}. {cred_note(*keys)} {note}{SOURCE_NOTE}")
        x1, y1, fw1, fh1 = polaroid(s, keys[0], 70, 170, 470, -4, 15)
        x2, y2, fw2, fh2 = polaroid(s, keys[1], 530, 120, 470, 3, 15)
        tape(s, x1 + 60, y1 + 10, deg=-30); tape(s, x2 + fw2 - 60, y2 + 10, deg=30)
        piece(s, LIGHTS[light][0], x2 + fw2 - 30, y2 + fh2 - 10, 150, 12)
        piece(s, CUT + "dried-flowers-1-1.png", 90, 700, 160, -30)
        animal_text(s, 90, 800, 900, name, light, body, name_pt, 32, name_lines)
        return s

    def dried(s, x, y, fw, fh): piece(s, CUT + "dried-flowers-1-1.png", x - 10, y + fh - 60, 190, -28)
    def cowpat(s, x, y, fw, fh): piece(s, CUT + "cow-poop-sticker-1.png", x + fw - 40, y + fh - 90, 210, -8)
    def flower2(s, x, y, fw, fh): piece(s, CUT + "dried-flowers-2-1.png", x - 5, y + fh - 90, 180, -20)

    one("rabbit", "Rabbit", "green", "Small dry pellets, rich in nitrogen, low odor. The easiest manure there is.", dried)
    two(("goat", "sheep"), "Goat and sheep", "green", "Dry pellets, C:N around 16:1. Mix with bedding and compost.")
    two(("alpaca", "guinea-pig"), "Alpaca, llama and guinea pig", "green",
        "Low-odor pellets. Guinea pig bedding composts right along with them.",
        note="No llama photo; the alpaca stands in for alpaca and llama. ", name_pt=52, name_lines=2)
    one("chicken", "Chicken", "yellow",
        "The hottest manure: C:N around 7:1, very high in nitrogen. Add lots of woody carbon or ammonia escapes.", flower2)
    one("cow", "Cow", "yellow", "C:N around 19:1, very wet. Add woody material and let it breathe.", cowpat)
    one("horse", "Horse", "yellow", "C:N around 25:1 with bedding, drier. Weed seeds survive unless the pile gets hot.", dried)

    # 9 pig (yellow) + dog and cat (red)
    s = slide(d, f"Pig, then dog and cat. {cred_note('pig', 'dog', 'cat')} {SOURCE_NOTE}")
    x, y, fw, fh = polaroid(s, "pig", 70, 90, 400, -3, 15)
    tape(s, x + 50, y + 8, deg=-30)
    piece(s, LIGHTS["yellow"][0], x + fw - 10, y + 50, 120, 10)
    animal_text(s, 540, 130, 470, "Pig", "yellow",
                "C:N around 14:1. Pigs share parasites and bacteria with people, so the pile must reach 55°C.", 52, 28)
    rect(s, 80, 675, 920, 3, DEEP, alpha=25)
    xd, yd, fwd, fhd = polaroid(s, "dog", 560, 720, 225, -4, 11)
    xc, yc, fwc, fhc = polaroid(s, "cat", 790, 745, 225, 4, 11)
    tape(s, xd + 30, yd + 6, 110, 36, -30)
    piece(s, LIGHTS["red"][0], xc + fwc - 40, yc - 10, 100, -10)
    animal_text(s, 80, 730, 450, "Dog and cat", "red",
                "Dog poop can carry roundworm and cat poop can carry Toxoplasma. Keep both out of any compost for food.", 52, 28,
                pill_pt=16)
    piece(s, CUT + "dried-flowers-2-1.png", 960, 1200, 150, 18)

    # 10 takeaway: type, one small compost print
    s = slide(d, "Takeaway. " + cred_note("compost-4") + " " + SOURCE_NOTE)
    text(s, 80, 150, 800, 40, "THE TAKEAWAY", 22, GREEN, HEAD, True, track=2)
    text(s, 80, 210, 920, 470, "Any 🟡 manure needs a thermal pile balanced to roughly 25 to 30:1 and held at "
         "55 to 68°C before it goes near food crops.", 48, DEEP, HEAD, True, spacing=1.15)
    x, y, fw, fh = polaroid(s, "compost-4", 110, 740, 340, -5, 13)
    tape(s, x + fw / 2, y + 4, 130, 40, -8)
    piece(s, CUT + "dried-flowers-1-1.png", 560, 930, 230, 14)
    piece(s, CUT + "poop-sticker-1.png", 760, 1000, 180, -8)
    text(s, 80, 1250, 760, 60, "Sources: Rynk et al., On-Farm Composting Handbook (NRAES-54), 1992; "
         "US EPA 40 CFR Part 503; CDC fact sheets on toxocariasis and toxoplasmosis.", 15, FAINT, BODY, spacing=1.2)
    logo(s, outline=DEEP)

    d.finish(OUT)
    print("wrote", OUT)


if __name__ == "__main__":
    build()
