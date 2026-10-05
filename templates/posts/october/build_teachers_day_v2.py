"""World Teachers' Day (Monday 5 October 2026), version 2: postable today.

Only the four mentors with a photo and an advice line on file get a card; everyone else is thanked by name on the
last slide (no [ADVICE LINE NEEDED] or [VERIFY] text on any image). Paper-cut field notes style: brand green and
cream, straight cut-paper creatures from the collage library, no tape, nothing tilted.

python3 templates/posts/october/build_teachers_day_v2.py  ->  05-10-2026-mon-ig-teachers-day-v2.pptx
"""
import os
from PIL import Image
from pptx.util import Emu
from lib import Deck, rect, text, crop, ROOT, PX, HEAD, BODY
from build_oct_01_10 import logo, save
from build_oct_01_10 import MENTORS

GREEN, CREAM, SAGE, TAN, BLACK = "31662F", "F3F1EA", "B1BCB1", "C09D7F", "1A1A1A"   # docs/brand-colors.md
GARA = "EB Garamond"
CUT = "assets/collage/cutouts/"
W, H, M = 1080, 1350, 80

# Card order and the creature on each card. Places are from the mentor bios; Carla's is still [VERIFY], so it is left off.
CARDS = [("Dr. Carla Portugal", None, "critter-mycorrhiza-2.png",
          "PhD in Environmental Sciences. 20 years of environmental and farm consulting. Mentoring since 2019."),
         ("Wesley Sanders", "Sierra Nevada foothills, California", "microscope-paper-1.png",
          "Ten years as an agricultural journalist, then ten managing a farm. Mentoring since 2020."),
         ("Gerald Ramirez", "Costa Rica", "critter-paramecium-1.png",
          "Agronomist, University of Costa Rica. Teaches compost extracts and teas."),
         ("Nick Padwick", "West Norfolk, England", "critter-bacillus-1.png",
          "Manages Ken Hill Estate, home of Wild Ken Hill. Farmers Weekly Farmer of the Year, 2009.")]


def piece(s, rel, x, y, w, h):
    """Cut-paper piece fitted inside a box, straight."""
    p = os.path.join(ROOT, rel)
    im = Image.open(p).convert("RGBA"); box = im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox()
    out = os.path.join(ROOT, "renders", ".tmp", "trim-" + os.path.basename(rel)); os.makedirs(os.path.dirname(out), exist_ok=True)
    im = im.crop(box); im.thumbnail((900, 900)); im.save(out)
    r = min(w / im.width, h / im.height); pw, ph = im.width * r, im.height * r
    s.shapes.add_picture(out, Emu(int((x + (w - pw) / 2) * PX)), Emu(int((y + (h - ph) / 2) * PX)), Emu(int(pw * PX)), Emu(int(ph * PX)))


def build():
    d = Deck(name="05-10-2026-mon-ig-teachers-day-v2")
    by_name = {m[0]: m for m in MENTORS}

    s = d.slide(GREEN, "Cover. World Teachers' Day, 5 October (UNESCO). Creatures: collage library (flux-2-pro).", counter=False)
    text(s, M, 140, W - 2 * M, 40, "WORLD TEACHERS' DAY · 5 OCTOBER", 20, SAGE, HEAD, True, track=3)
    text(s, M, 200, W - 2 * M, 360, "Happy World Teachers' Day.", 76, CREAM, HEAD, True, spacing=1.0)
    text(s, M, 560, W - 2 * M, 140, "Our mentors' best advice, in one line each.", 36, CREAM, GARA, italic=True, spacing=1.15)
    for i, rel in enumerate(["microscope-paper-1.png", "cute-bacterium-1.png", "mushroom-paper-1.png", "happy-seedling-1.png"]):
        piece(s, CUT + rel, M + i * 235, 820, 200, 280)
    logo(s, W - M - 110, H - 70 - 110 * 668 / 743, 110, white=True)

    for name, place, creature, about in CARDS:
        _, role, advice, photo, focus, facts = by_name[name]
        s = d.slide(CREAM, f"Mentor card: {name}. Advice line and facts from the mentor bios, 30 Sep 2026: confirm with "
                           f"{name.split()[-1] if 'Dr.' not in name else 'Carla'} before posting. Photo: {photo} "
                           "(assets/mentors-teachers-day/README: written consent needed).", counter=False)
        s.shapes.add_picture(crop(photo, 920, 600, *focus), Emu(M * PX), Emu(M * PX), Emu(920 * PX), Emu(600 * PX))
        y = M + 600 + 40
        text(s, M, y, 720, 70, name, 50, GREEN, HEAD, True, anchor="m")
        role = role.replace("AP ", "Advanced Programs ")          # no acronyms in public text
        text(s, M, y + 74, 720, 40, role + (f" · {place}" if place else ""), 22, BLACK, BODY)
        text(s, M, y + 140, 700, 380, advice, 40, BLACK, GARA, italic=True, spacing=1.15)
        text(s, M, H - 175, 720, 70, about, 20, GREEN, BODY, spacing=1.15)
        piece(s, CUT + creature, 820, y + 30, 180, 300)
        text(s, W - M - 300, H - 70, 300, 30, "soilfoodweb.com", 18, GREEN, HEAD, True, align="r")

    s = d.slide(GREEN, "Closing: every mentor on the roster (Linnea, September 2026) thanked by name.", counter=False)
    text(s, M, 140, W - 2 * M, 260, "Thank you to every mentor who teaches our students to see soil.", 52, CREAM, HEAD,
         True, spacing=1.08)
    names = [m[0] for m in MENTORS]
    text(s, M, 470, W - 2 * M, 460, " · ".join(names), 26, SAGE, GARA, italic=True, spacing=1.35)
    piece(s, CUT + "critter-cocci-4.png", M, 1000, 220, 200)
    logo(s, W - M - 110, H - 70 - 110 * 668 / 743, 110, white=True)
    save(d, "05-10-2026-mon-ig-teachers-day-v2.pptx")


if __name__ == "__main__":
    build()
