"""Under Rose's Garden, Book 1: The Lollipop. First draft of pages 1 to 6, as an editable PowerPoint.

python3 templates/storybook/build_book1.py  ->  templates/storybook/under-roses-garden-book1-pages1-6.pptx

Each page is one 4:3 slide (1600 x 1200 px): a full-bleed collage scene, the characters as separate cut-out
pictures on top (so they stay the same from page to page and can be moved), and the story text on a cream paper
panel. Art: tools/storybook_generate.py (scenes, Rose, Grandma Worm, Pip, Ama, lollipop) and the creature set
(Barry = critter-bacillus, Myco = critter-mycorrhiza v2). The words are a first draft for Linnea to rewrite.
"""
import os
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
ORIG, CUT = "assets/collage/originals/", "assets/collage/cutouts/"
TMP = os.path.join(ROOT, "renders", ".tmp", "book")
PX, W, H = 9525, 1600, 1200
CREAM, INK, BROWN = "F3F1EA", "333130", "4C3634"
SERIF, HEAD = "EB Garamond", "Montserrat"

ART = {
    "garden": ORIG + "book-scene-garden-1.png", "town": ORIG + "book-scene-town-1.png",
    "sugar": ORIG + "book-scene-sugar-rain-1.png", "room": ORIG + "book-scene-worm-room-1.png",
    "rose": CUT + "book-rose-lollipop-1.png", "rose-run": CUT + "book-rose-running-1.png",
    "worm": CUT + "book-grandma-worm-1.png", "pip": CUT + "book-pip-flagellate-1.png",
    "ama": CUT + "book-ama-amoeba-1.png", "lolly": CUT + "book-lollipop-1.png",
    "barry": CUT + "critter-bacillus-1.png", "myco": CUT + "critter-mycorrhiza-2.png",
}
MISSING = []


def prep(rel, cut, maxpx):
    os.makedirs(TMP, exist_ok=True)
    im = Image.open(os.path.join(ROOT, rel))
    if cut:
        im = im.convert("RGBA"); im = im.crop(im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox())
    else:
        im = im.convert("RGB")
        # The model signs its scenes with a fake scribble in the bottom-right corner: cover it with the paper
        # texture from just to the left of it.
        w, h = im.size; bx0, by0, bx1, by1 = int(w * .79), int(h * .85), int(w * .97), int(h * .98)
        im.paste(im.crop((bx0 - (bx1 - bx0), by0, bx0, by1)), (bx0, by0))
    im.thumbnail((maxpx, maxpx), Image.LANCZOS)
    out = os.path.join(TMP, os.path.basename(rel).rsplit(".", 1)[0] + (".png" if cut else ".jpg"))
    im.save(out, **({"optimize": True} if cut else {"quality": 88}))
    return out, im.size


def put(s, key, cx, cy, w, flip=False):
    """Character cut-out centred at (cx, cy), w px wide. Placeholder label if the art does not exist yet."""
    rel = ART[key]
    if not os.path.exists(os.path.join(ROOT, rel)):
        MISSING.append(rel); label(s, cx - w / 2, cy - 40, w, 80, f"[{key}]"); return
    path, (iw, ih) = prep(rel, True, 900)
    h = w * ih / iw
    pic = s.shapes.add_picture(path, Emu(int((cx - w / 2) * PX)), Emu(int((cy - h / 2) * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    if flip:
        pic._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm").set("flipH", "1")


def scene(s, key):
    rel = ART[key]
    if not os.path.exists(os.path.join(ROOT, rel)):
        MISSING.append(rel); label(s, 0, 0, W, H, f"[scene: {key}]"); return
    path, (iw, ih) = prep(rel, False, 1800)
    r = max(W / iw, H / ih); w, h = iw * r, ih * r                    # cover the page
    s.shapes.add_picture(path, Emu(int((W - w) / 2 * PX)), Emu(int((H - h) / 2 * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def label(s, x, y, w, h, t):
    tb = s.shapes.add_textbox(Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    tf = tb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t; r.font.size = Pt(24); r.font.name = HEAD; r.font.bold = True
    r.font.color.rgb = RGBColor.from_string(BROWN)


def words(s, x, y, w, h, paras, pt=30):
    """Story text on a cream paper panel. paras: list of strings, one paragraph each."""
    panel = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    panel.fill.solid(); panel.fill.fore_color.rgb = RGBColor.from_string(CREAM); panel.line.fill.background()
    panel.shadow.inherit = False
    tb = s.shapes.add_textbox(Emu(int((x + 44) * PX)), Emu(int((y + 34) * PX)), Emu(int((w - 88) * PX)), Emu(int((h - 68) * PX)))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, t in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.18; p.space_after = Pt(10)
        r = p.add_run(); r.text = t; f = r.font
        f.size = Pt(pt); f.name = SERIF; f.color.rgb = RGBColor.from_string(INK)


def page_no(s, n):
    tb = s.shapes.add_textbox(Emu(int((W / 2 - 40) * PX)), Emu(int((H - 54) * PX)), Emu(int(80 * PX)), Emu(int(36 * PX)))
    p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(n); r.font.size = Pt(16); r.font.name = SERIF; r.font.color.rgb = RGBColor.from_string(CREAM)


def new_page(prs, note):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.notes_slide.notes_text_frame.text = note
    return s


def build():
    prs = Presentation(); prs.slide_width, prs.slide_height = Emu(W * PX), Emu(H * PX)

    # 1. Rose in the garden after the rain
    s = new_page(prs, "Page 1, above ground. Scene: garden after rain. Rose holds her strawberry lollipop.")
    scene(s, "garden"); put(s, "rose", 1150, 700, 470)
    words(s, 80, 80, 760, 420, [
        "It had rained all afternoon, and now the garden smelled of wet leaves and worms.",
        "Rose sat on the edge of the vegetable bed in her yellow boots, licking a strawberry lollipop."])
    page_no(s, 1)

    # 2. The lollipop drops, Rose runs in
    s = new_page(prs, "Page 2, above ground. The lollipop sinks into the soft soil; Rose runs in for dinner.")
    scene(s, "garden"); put(s, "lolly", 470, 930, 190); put(s, "rose-run", 1250, 720, 420)
    words(s, 80, 80, 820, 470, [
        "“Rose! Dinner!”",
        "Rose jumped. The lollipop slipped out of her fingers and landed, plop, in the soft wet soil. "
        "By the time she looked back, it had sunk out of sight.",
        "“Night night, dirt!” she called, and ran inside."])
    page_no(s, 2)

    # 3. The town under the garden
    s = new_page(prs, "Page 3, underground. First look at the town: tunnel streets, crumb houses, brown glow, Old Oak's roots.")
    scene(s, "town")
    words(s, 80, 760, 1440, 360, [
        "Far below Rose's boots there was a whole town. Its streets were tunnels. Its houses were soil crumbs, "
        "round and snug. Its lights were a soft brown glow.",
        "And tonight, something strange was happening to the ceiling."], pt=32)
    page_no(s, 3)

    # 4. Sugar rain: Barry tastes and splits in two
    s = new_page(prs, "Page 4, underground. Sugar rain. Barry tastes it and splits into two Barrys. Barry = critter-bacillus.")
    scene(s, "sugar"); put(s, "barry", 1060, 640, 260); put(s, "barry", 1330, 700, 260, flip=True)
    words(s, 80, 80, 780, 620, [
        "Drip. Drip. Drip. Something pink and sticky was raining down.",
        "Barry the Bacterium had a taste. “Sugar!” he gasped. And because Barry was a bacterium, and that is what "
        "bacteria do when they eat, he split in two.",
        "“Which Barry am I?” said Barry.",
        "“I was going to ask you that,” said Barry."])
    page_no(s, 4)

    # 5. Sixteen Barrys; Myco carries the news
    s = new_page(prs, "Page 5, underground. Sixteen Barrys fill the street (copies of the same cut-out, all movable). "
                      "Myco the postman (critter-mycorrhiza v2) passes the news from root to root.")
    scene(s, "sugar")
    spots = [(700 + (i % 6) * 140 + (i // 6) * 40, 560 + (i // 6) * 150) for i in range(16)]
    for i, (x, y) in enumerate(spots):
        put(s, "barry", x, y, 150, flip=bool(i % 2))
    put(s, "myco", 330, 900, 360)
    words(s, 80, 70, 900, 400, [
        "Two Barrys became four. Four became eight. Eight became sixteen. Soon the whole street was full of Barrys, "
        "all eating, all splitting, all asking which Barry they were.",
        "Myco the postman stretched his long, long arms from root to root and house to house: "
        "“Sugar on Crumb Street! Pass it on!”"], pt=28)
    page_no(s, 5)

    # 6. Pip and Ama arrive; Grandma Worm wakes
    s = new_page(prs, "Page 6, underground. Pip and Ama arrive for the party; the town shakes as Grandma Worm wakes.")
    scene(s, "town"); put(s, "pip", 620, 560, 230); put(s, "ama", 900, 600, 280); put(s, "worm", 1330, 760, 520)
    words(s, 80, 760, 1440, 360, [
        "Pip the Flagellate came zooming in on his two long tails. Ama the Amoeba came drifting after him, "
        "and Pip forgot how to swim.",
        "Then the floor began to tremble and the teacups began to rattle. “WHO,” rumbled Grandma Worm, "
        "“is making all that NOISE?”"], pt=30)
    page_no(s, 6)

    out = os.path.join(HERE, "under-roses-garden-book1-pages1-6.pptx")
    prs.save(out)
    print("wrote", os.path.relpath(out, ROOT))
    if MISSING: print("MISSING ART:", sorted(set(MISSING)))


if __name__ == "__main__":
    build()
