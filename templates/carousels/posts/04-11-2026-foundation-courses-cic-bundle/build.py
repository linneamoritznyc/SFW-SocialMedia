"""Fall 2026 Enrollment Special: Foundation Courses + Compost Intensive Course bundle.
2-slide carousel, 1080 x 1350, Instagram and LinkedIn, Wednesday 4 November 2026.

  pip install python-pptx pillow numpy scipy
  python3 templates/carousels/posts/04-11-2026-foundation-courses-cic-bundle/build.py

    -> layers/        every picture as its own PNG (illustrations on paper, flower cutout, white logo)
    -> ../04-11-2026-foundation-courses-cic-bundle.pptx   editable, one named object per element (for Canva)
    -> previews/slide-1.png, slide-2.png   rendered from the same layout with the repo's own font files

One layout spec (SLIDES below) drives both the PPTX and the preview, so what you see in the preview is
where every object sits in the PPTX. Text is placed line by line on purpose: each line is a paragraph,
so Canva and PowerPoint never re-wrap a headline differently from the preview.

Art: watercolor illustrations generated on Replicate (FLUX 1.1 Pro, then Real-ESRGAN x2) with the house
prefix from SFWassetlibrarycontentautomation tools/wormhole-visuals/watercolor_gen.py. Prompts in
art/PROMPTS.md. They are illustrations, not photographs, and are never presented as SFW microscopy.
"""
import os, subprocess, json, shutil
import numpy as np
from PIL import Image, ImageFilter
from scipy import ndimage
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR, MSO_AUTO_SIZE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
ART, LAY, PREV = (os.path.join(HERE, d) for d in ("art", "layers", "previews"))
PPTX = os.path.join(HERE, "..", "04-11-2026-foundation-courses-cic-bundle.pptx")
for d in (LAY, PREV): os.makedirs(d, exist_ok=True)

W, H, PX = 1080, 1350, 9525          # 1 px = 9525 EMU (96 dpi), same as templates/carousels/build.py
GREEN, SOIL, BLUE, CREAM, INK, WHITE = "#156826", "#4F3433", "#3780B8", "#F4F1EA", "#333130", "#FFFFFF"
PAPER = "#F7F3EB"                      # one paper tone for both illustrations, so the swipe reads as one sheet

HEAD = "Montserrat"                    # Bold 700 for headlines
BODY = "Montserrat"                    # Regular 400 for the details (Montserrat on every run, for Canva)

def rgb(h): return tuple(int(h[i:i + 2], 16) for i in (1, 3, 5))


# ---------------------------------------------------------------------------------------------- layers
def on_paper(src, paper_from):
    """Re-tone an illustration so its paper is exactly PAPER (per-channel gain, no fades)."""
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    gain = np.array(rgb(PAPER), np.float32) / np.array(paper_from, np.float32)
    return Image.fromarray(np.clip(a * gain, 0, 255).astype(np.uint8))


def paper_of(src):
    a = np.asarray(Image.open(src).convert("RGB")).astype(np.float32)
    c = np.concatenate([a[:40, :40].reshape(-1, 3), a[:40, -40:].reshape(-1, 3), a[-40:, :40].reshape(-1, 3), a[-40:, -40:].reshape(-1, 3)])
    return np.median(c, axis=0)


def place(canvas, im, x, y, scale):
    im = im.resize((round(im.width * scale), round(im.height * scale)), Image.LANCZOS)
    canvas.paste(im, (round(x), round(y)))
    return canvas


def cutout(src, thr=26):
    """Flower sticker: remove paper connected to the border, keep pale petals inside, feather 1 px."""
    im = Image.open(src).convert("RGB"); a = np.asarray(im).astype(np.int16)
    paper = paper_of(src)
    diff = np.abs(a - paper).max(axis=2)
    fg = diff > thr
    fg = ndimage.binary_closing(fg, iterations=3)
    fg = ndimage.binary_fill_holes(fg)
    lab, n = ndimage.label(fg)
    sizes = ndimage.sum(fg, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 0.02 * sizes.max()])
    m = Image.fromarray((keep * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(1.2))
    out = im.copy(); out.putalpha(m)
    return out.crop(out.getbbox())


def white_logo():
    im = Image.open(os.path.join(ROOT, "assets", "logo", "sfw-foundation-wordmark-240.png")).convert("RGBA")
    white = Image.new("RGBA", im.size, (255, 255, 255, 255)); white.putalpha(im.getchannel("A"))
    return white


def build_layers():
    # Slide 1: the bean seedling with its root ball, right of centre, falling to the lower right.
    s = os.path.join(ART, "seedling-root-ball.jpg")
    seed = on_paper(s, paper_of(s))
    c = Image.new("RGB", (W, H), PAPER)
    sc = S1_ART["scale"]
    place(c, seed, S1_ART["x"], S1_ART["y"], sc)
    c.save(os.path.join(LAY, "slide-1-illustration.png"))
    # Slide 2: the soil band, seedlings at the top, roots running down behind the box.
    s = os.path.join(ART, "soil-band.jpg")
    band = on_paper(s, paper_of(s))
    c = Image.new("RGB", (W, H), PAPER)
    place(c, band, S2_ART["x"], S2_ART["y"], S2_ART["scale"])
    c.save(os.path.join(LAY, "slide-2-illustration.png"))
    cutout(os.path.join(ART, "coneflower.jpg")).save(os.path.join(LAY, "flower-coneflower.png"))
    white_logo().save(os.path.join(LAY, "sfw-logo-white.png"))


# ---------------------------------------------------------------------------------------------- layout
# Art placement: where the source illustration sits on the 1080 x 1350 slide (px, scale of source).
S1_ART = dict(x=-44, y=-42, scale=0.64)
S2_ART = dict(x=-760, y=-390, scale=1.0)

LOGO_W = 150
LOGO_H = round(LOGO_W * 208 / 240)


def slide1():
    pad_l, pad_t, pad_r, pad_b = 72, 66, 64, 66
    hs, hlh = 86, 90                                   # headline px, line height px
    head = ["Foundation", "Courses +", "Compost", "Intensive", "Course"]
    ds, dlh = 52, 64
    det = [("Fall 2026 Bundle,", 0), ("until 30 November", 0), ("Link in bio", 58)]
    hy = pad_t
    hh = hlh * len(head) + 8
    dy = hy + hh + 40
    dh = dlh * len(det) + sum(g for _, g in det)
    box_w = 72 + 521 + 56 + 0                          # hugs the widest headline line ("Foundation")
    box_w = max(box_w, 72 + 330 + 40 + LOGO_W + pad_r)
    over = max(0, LOGO_H / 2 - dlh / 2)              # the logo hangs below the last line; pad from the logo
    box_h = round(dy + dh + over + pad_b)
    last_line_mid = dy + dh - dlh / 2
    return dict(name="Cover", el=[
        dict(k="rect", name="Background", x=0, y=0, w=W, h=H, fill=PAPER),
        dict(k="img", name="Illustration", src="slide-1-illustration.png", x=0, y=0, w=W, h=H),
        dict(k="rect", name="Green box", x=0, y=0, w=box_w, h=box_h, fill=GREEN),
        dict(k="text", name="Headline", x=72, y=hy, w=box_w - 72 - 40, h=hh, lines=[(t, 0) for t in head],
             size=hs, lh=hlh, font=HEAD, bold=True, color=CREAM),
        dict(k="text", name="Details", x=72, y=dy, w=box_w - 72 - LOGO_W - pad_r - 16, h=dh, lines=det,
             size=ds, lh=dlh, font=BODY, bold=False, color=CREAM),
        dict(k="img", name="SFW logo", src="sfw-logo-white.png", x=box_w - pad_r - LOGO_W,
             y=round(last_line_mid - LOGO_H / 2), w=LOGO_W, h=LOGO_H),
        flower(FLOWER1, "Flower (continues on slide 2)"),
    ])


# The coneflower straddles the swipe: its head is cut by slide 1's right edge and finishes on slide 2's left edge.
FLOWER_W = 360
FLOWER1 = dict(x=W - round(0.57 * FLOWER_W), y=870, w=FLOWER_W)          # bottom right of the cover, bleeding off
FLOWER2 = dict(x=FLOWER1["x"] - W, y=FLOWER1["y"], w=FLOWER_W)            # the same flower, one slide-width on


def flower(f, name="Flower"):
    im = Image.open(os.path.join(LAY, "flower-coneflower.png"))
    return dict(k="img", name=name, src="flower-coneflower.png", x=f["x"], y=f["y"], w=f["w"], h=round(f["w"] * im.height / im.width))


def slide2():
    pad_l, pad_t, pad_r, pad_b = 62, 58, 66, 58
    hs, hlh = 68, 76
    head = ["What\u2019s in the bundle"]
    ds, dlh = 52, 58
    g = 26
    det = [("4 Foundation Courses,", 0), ("start today", 0),
           ("Compost Intensive: 10 weeks,", g), ("live with a mentor", 0),
           ("Pick your cohort:", g), ("January, May or August 2027", 0),
           ("2 batches of compost to keep", g),
           ("Dr. Elaine\u2019s webinar archive", g),
           ("Link in bio", 58)]
    hh = hlh * len(head) + 6
    dh = dlh * len(det) + sum(gg for _, gg in det)
    inner = 770
    box_w = pad_l + inner + pad_r
    over = max(0, LOGO_H / 2 - dlh / 2)
    box_h = round(pad_t + hh + 30 + dh + over + pad_b)
    bx, by = W - box_w, H - box_h
    hy = by + pad_t
    dy = hy + hh + 30
    last_line_mid = dy + dh - dlh / 2
    return dict(name="What's in it", el=[
        dict(k="rect", name="Background", x=0, y=0, w=W, h=H, fill=PAPER),
        dict(k="img", name="Illustration", src="slide-2-illustration.png", x=0, y=0, w=W, h=H),
        dict(k="rect", name="Brown box", x=bx, y=by, w=box_w, h=box_h, fill=SOIL),
        dict(k="text", name="Headline", x=bx + pad_l, y=hy, w=inner, h=hh, lines=[(t, 0) for t in head],
             size=hs, lh=hlh, font=HEAD, bold=True, color=CREAM),
        dict(k="text", name="Details", x=bx + pad_l, y=dy, w=inner, h=dh, lines=det,
             size=ds, lh=dlh, font=BODY, bold=False, color=CREAM),
        dict(k="img", name="SFW logo", src="sfw-logo-white.png", x=W - pad_r - LOGO_W,
             y=round(last_line_mid - LOGO_H / 2), w=LOGO_W, h=LOGO_H),
        flower(FLOWER2, "Flower (continues from slide 1)"),
    ])


# ---------------------------------------------------------------------------------------------- PPTX
def write_pptx(slides):
    p = Presentation(); p.slide_width = Emu(W * PX); p.slide_height = Emu(H * PX)
    blank = p.slide_layouts[6]
    for i, sd in enumerate(slides, 1):
        s = p.slides.add_slide(blank)
        for e in sd["el"]:
            x, y, w, h = (Emu(round(e[k] * PX)) for k in ("x", "y", "w", "h"))
            if e["k"] == "rect":
                sh = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
                sh.fill.solid(); sh.fill.fore_color.rgb = RGBColor.from_string(e["fill"][1:])
                sh.line.fill.background(); sh.shadow.inherit = False
                sh.text_frame.text = ""
            elif e["k"] == "img":
                sh = s.shapes.add_picture(os.path.join(LAY, e["src"]), x, y, w, h)
            else:
                sh = s.shapes.add_textbox(x, y, w, h)
                tf = sh.text_frame; tf.word_wrap = False; tf.auto_size = MSO_AUTO_SIZE.NONE
                tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
                tf.vertical_anchor = MSO_ANCHOR.TOP
                for j, (t, gap) in enumerate(e["lines"]):
                    para = tf.paragraphs[0] if j == 0 else tf.add_paragraph()
                    para.alignment = PP_ALIGN.LEFT
                    para.line_spacing = Pt(e["lh"] * 0.75)
                    para.space_before = Pt(gap * 0.75); para.space_after = Pt(0)
                    r = para.add_run(); r.text = t
                    f = r.font; f.name = e["font"]; f.size = Pt(e["size"] * 0.75); f.bold = e["bold"]; f.italic = False
                    f.color.rgb = RGBColor.from_string(e["color"][1:])
            sh.name = e["name"]
        s.notes_slide.notes_text_frame.text = (
            f"Wed 4 Nov 2026, Instagram + LinkedIn. Fall 2026 Enrollment Special: Foundation Courses + Compost Intensive Course. "
            f"Slide {i}: {sd['name']}. Fonts: Montserrat Bold (headline), Montserrat Regular (details). "
            "Illustrations are AI watercolor, never presented as SFW photos or microscopy. No prices, no discounts, no codes.")
    p.core_properties.title = "04-11-2026 Foundation Courses + Compost Intensive Course bundle"
    p.save(PPTX)


# ---------------------------------------------------------------------------------------------- preview
def write_html(slides):
    font = os.path.join(ROOT, "assets", "font", "montserrat-latin-variable.woff2")
    css = (f"@font-face{{font-family:'Montserrat';font-weight:100 900;src:url('file://{font}') format('woff2-variations');}}"
           "*{margin:0;padding:0;box-sizing:border-box}body{background:#ddd}"
           f".s{{position:relative;width:{W}px;height:{H}px;overflow:hidden}}"
           ".e{position:absolute}.t{white-space:pre;font-kerning:normal}")
    pages = []
    for sd in slides:
        out = []
        for e in sd["el"]:
            st = f"left:{e['x']}px;top:{e['y']}px;width:{e['w']}px;height:{e['h']}px;"
            if e["k"] == "rect":
                out.append(f'<div class="e" style="{st}background:{e["fill"]}"></div>')
            elif e["k"] == "img":
                out.append(f'<img class="e" style="{st}" src="file://{os.path.join(LAY, e["src"])}">')
            else:
                ls = "".join(f'<div style="margin-top:{g}px;height:{e["lh"]}px;line-height:{e["lh"]}px">{t}</div>' for t, g in e["lines"])
                out.append(f'<div class="e t" style="{st}font-family:{e["font"]};font-size:{e["size"]}px;'
                           f'font-weight:{700 if e["bold"] else 400};color:{e["color"]}">{ls}</div>')
        pages.append(f'<div class="s">{"".join(out)}</div>')
    for i, pg in enumerate(pages, 1):
        with open(os.path.join(PREV, f"_slide-{i}.html"), "w") as f:
            f.write(f"<!doctype html><meta charset=utf-8><style>{css}</style>{pg}")


def render():
    js = """
const { chromium } = require('playwright');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({viewport:{width:1080,height:1350}});
  for (const i of [1,2]) {
    await p.goto('file://' + process.argv[2] + '/_slide-' + i + '.html'); await p.evaluate(() => document.fonts.ready);
    await p.waitForTimeout(300);
    await p.locator('.s').screenshot({ path: process.argv[2] + '/slide-' + i + '.png' });
  }
  await b.close();
})();"""
    jsp = os.path.join(PREV, "_render.js")
    open(jsp, "w").write(js)
    subprocess.run(["node", jsp, PREV], check=True)
    for f in ("_render.js", "_slide-1.html", "_slide-2.html"):
        os.remove(os.path.join(PREV, f))


if __name__ == "__main__":
    build_layers()
    slides = [slide1(), slide2()]
    write_pptx(slides)
    write_html(slides)
    render()
    json.dump([{k: v for k, v in e.items()} for sd in slides for e in sd["el"]], open(os.path.join(PREV, "layout.json"), "w"), indent=1)
    print("wrote", os.path.relpath(PPTX, ROOT))
