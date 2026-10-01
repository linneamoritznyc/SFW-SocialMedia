"""1000 Farms study (Fri 2 Oct): clean marketing versions, no scrapbook.

Instagram: 3-slide seamless carousel. Top: one continuous photo strip, full bleed, whose photo edges sit mid-slide (the
middle photo crosses both slide seams), with one Glow rule under it across all three slides. Bottom: Deep Green, the
same text grid on every slide. LinkedIn: Deep Green text panel left, full-bleed soil photo right.
The photos are from the Foundation library; none of them is a 1000 Farms site (said in the slide notes).

python3 build_farms_panorama.py  ->  02-10-2026-fri-ig-1000-farms-study-panorama.pptx, 02-10-2026-fri-li-1000-farms-study.pptx
"""
import os
from PIL import Image, ImageOps
from pptx.util import Emu
from lib import Deck, rect, text, crop, ROOT, PX
from build_oct_01_10 import logo, logo_br, save, STUDY_SRC, STUDY_LINE
from build_boubacar_panorama import nlines, lh, HEADF, BODYF

N, SW, SH, STRIP_H = 3, 1080, 1350, 620
DEEP, CREAM, GLOW = (0x22, 0x37, 0x1F), "F4F1EA", "DBE6A7"
OUT_DIR = os.path.join(ROOT, "assets/collage/farms-panorama")
P = "assets/photo/"
STRIP = [(P + "hand-soil-roots-fungi.jpg", 810, 0.5, 0.45),          # x 0..810
         (P + "erc-rancho-cacachilas-agro.jpg", 1620, 0.5, 0.62),    # x 810..2430, crosses both seams
         (P + "handling-loose-soil.jpg", 810, 0.62, 0.55)]           # x 2430..3240
GAP = 8                                                             # Deep Green gutter between photos
X, W = 80, 920                                                      # text column, the same on every slide
PHOTOS = ("Photos (Foundation library, not 1000 Farms sites): hand-soil-roots-fungi.jpg, erc-rancho-cacachilas-agro.jpg "
          "(Rancho Cacachilas), handling-loose-soil.jpg. ")


def strip():
    im = Image.new("RGB", (N * SW, SH), DEEP); x = 0
    for rel, w, fx, fy in STRIP:
        p = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, rel))).convert("RGB")
        p = ImageOps.fit(p, (w - (GAP if x + w < N * SW else 0), STRIP_H), Image.LANCZOS, centering=(fx, fy))
        im.paste(p, (x, 0)); x += w
    im.paste(Image.new("RGB", (N * SW, 8), tuple(int(GLOW[i:i + 2], 16) for i in (0, 2, 4))), (0, STRIP_H))
    os.makedirs(OUT_DIR, exist_ok=True); im.save(os.path.join(OUT_DIR, "panorama-full.jpg"), quality=90)
    for i in range(N):
        im.crop((i * SW, 0, (i + 1) * SW, SH)).save(os.path.join(OUT_DIR, f"slide-{i + 1:02d}.jpg"), quality=92)


def place(s, path, x, y, w, h):
    s.shapes.add_picture(path, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def slide(d, i, note, eyebrow):
    s = d.slide(None, note, counter=False)
    place(s, os.path.join(OUT_DIR, f"slide-{i:02d}.jpg"), 0, 0, SW, SH)
    text(s, X, 690, W, 34, eyebrow, 22, GLOW, HEADF, True, track=3)
    text(s, X, SH - 78, 700, 30, STUDY_LINE, 20, GLOW, BODYF)
    return s


def para(s, y, t, pt, font, bold, sp=1.15, color=CREAM):
    h = nlines(t, pt, W * 0.96, font) * lh(pt, sp)
    text(s, X, y, W, h + 10, t, pt, color, font, bold, spacing=sp)
    return y + h


def ig():
    strip()
    d = Deck(name="02-10-2026-fri-ig-1000-farms-study-panorama")

    s = slide(d, 1, "Seamless 3-slide carousel, clean marketing style. " + STUDY_SRC + " " + PHOTOS, "NEW STUDY")
    text(s, X - 6, 720, W, 230, "39%", 180, CREAM, HEADF, True, spacing=1.0)
    para(s, 995, "more total carbon in the soil of the most regenerative farms.", 42, HEADF, True)
    logo_br(s, True, 110, m=60)

    s = slide(d, 2, "Second slide. " + STUDY_SRC, "SAME FARMS, MORE LIFE")
    text(s, X - 6, 720, W, 230, "77%", 180, CREAM, HEADF, True, spacing=1.0)
    y = para(s, 995, "more total fungi.", 42, HEADF, True) + 18
    para(s, y, "Soil microbes, insects, plants and birds were all more abundant.", 34, BODYF, False, 1.2)
    text(s, 0, SH - 78, SW - 60, 30, "soilfoodweb.com", 20, CREAM, HEADF, True, align="r")

    s = slide(d, 3, "Closing slide. Link for the caption: https://doi.org/10.1088/2976-601X/ae8f4e. " + STUDY_SRC, "THE FINDING")
    y = para(s, 735, "One practice alone changed nothing.", 64, HEADF, True, 1.05) + 26
    para(s, y, "Farms using just one regenerative practice looked the same as conventional farms. The outcomes came "
               "from the full system, living soil included.", 34, BODYF, False, 1.2)
    logo_br(s, True, 110, m=60)
    save(d, "02-10-2026-fri-ig-1000-farms-study-panorama.pptx")


def li():
    PH = P + "handling-loose-soil.jpg"
    d = Deck(1200, 627, name="02-10-2026-fri-li-1000-farms-study")
    s = d.slide("22371F", "LinkedIn image. " + STUDY_SRC + " Photo: " + PH + " (Foundation library, not a 1000 Farms site).",
                counter=False)
    place(s, crop(PH, 560, 627, 0.55, 0.5), 640, 0, 560, 627)
    rect(s, 640, 0, 6, 627, GLOW)
    text(s, 64, 95, 560, 170, "39%", 150, CREAM, HEADF, True, spacing=1.0)
    text(s, 70, 298, 560, 56, "more soil carbon", 40, CREAM, HEADF, True, spacing=1.0)
    rect(s, 72, 380, 80, 4, GLOW)
    text(s, 70, 402, 540, 80, "on the most regenerative farms,\n1000 Farms Initiative, 2026", 24, GLOW, BODYF, spacing=1.25)
    text(s, 70, 560, 540, 30, STUDY_LINE, 16, CREAM, BODYF)
    logo_br(s, True, 90, 1200, 627, 30)
    save(d, "02-10-2026-fri-li-1000-farms-study.pptx")


if __name__ == "__main__":
    ig(); li()
