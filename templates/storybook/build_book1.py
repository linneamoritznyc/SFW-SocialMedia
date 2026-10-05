"""Under Rose's Garden, Book 1: The Lollipop. The whole book as one editable PowerPoint, with an appendix.

python3 templates/storybook/build_book1.py  ->  templates/storybook/under-roses-garden-book1-complete.pptx

32 book pages (title, dedication, story pages 1 to 29, The End), then an appendix: the characters, the scene
library, the story notes and the print notes.

Print spec (picture book, 10 x 8 in landscape trim): each slide is 10.25 x 8.25 in = trim plus 0.125 in bleed on
every side. Art runs to the bleed edge; text and page numbers stay 0.5 in inside the trim (IngramSpark margin;
KDP's minimum is 0.375 in). Sources: kidillus.com/learn/book-trim-sizes-bleed-margins, neolemon.com (KDP sizes).
Layout is written on a 1600 x 1200 design grid and mapped onto the page. Story pages: a full-bleed collage scene,
the characters as separate cut-out pictures on top (movable), black text on a soft cream fade.
The art is kept at its generated size (2048 px wide, about 200 DPI on this page) so the file stays small enough to
share; upscale the scenes before sending to a printer.
Art: tools/storybook_generate.py and the creature set (Barry = critter-bacillus, Myco = critter-mycorrhiza v2).
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
DPI = 160                                   # internal unit: 160 units per inch
W, H = int(10.25 * DPI), int(8.25 * DPI)     # 1640 x 1320: 10 x 8 in trim + 0.125 in bleed all round
PX = 914400 // DPI                          # EMU per unit
BLEED, SAFE = int(0.125 * DPI), int((0.125 + 0.5) * DPI)   # safe area starts 0.5 in inside the trim
FS = 10.25 / 16.667                         # font scale from the old 16.7 in wide draft to the real page
sx = lambda x: x * W / 1600                 # design grid -> page
sy = lambda y: y * H / 1200
CREAM, INK, BROWN = "F3F1EA", "333130", "4C3634"
SERIF, HEAD = "EB Garamond", "Montserrat"

ART = {
    "garden": ORIG + "book-scene-garden-1.png", "flowers": ORIG + "book-scene-flowers-1.png",
    "lolly-soil": ORIG + "book-scene-lollipop-soil-1.png", "drop": ORIG + "book-scene-sugar-drop-1.png",
    "house": ORIG + "book-scene-barry-house-1.png", "root-road": ORIG + "book-scene-root-road-1.png",
    "dinner": ORIG + "book-scene-rose-dinner-1.png", "stick": ORIG + "book-scene-stick-street-1.png",
    "morning": ORIG + "book-scene-garden-morning-1.png", "apple": ORIG + "book-scene-apple-core-1.png",
    "rose-pull": CUT + "book-rose-pulling-stick-1.png", "night": ORIG + "book-scene-town-night-1.png",
    "bed": ORIG + "book-scene-rose-bed-1.png", "apple-below": ORIG + "book-scene-apple-below-1.png", "town": ORIG + "book-scene-town-1.png",
    "sugar": ORIG + "book-scene-sugar-rain-1.png", "room": ORIG + "book-scene-worm-room-1.png",
    "rose": CUT + "book-rose-lollipop-1.png", "rose-run": CUT + "book-rose-running-1.png",
"pip": CUT + "book-pip-flagellate-1.png",
    "ama": CUT + "book-ama-amoeba-1.png", "lolly": CUT + "book-lollipop-1.png",
    "barry": CUT + "critter-bacillus-1.png", "myco": CUT + "critter-mycorrhiza-2.png",
}
MISSING = []
SIGNATURES = {"book-scene-garden-1.png": [(.88, .86, .99, .95)], "book-scene-town-1.png": [(.81, .87, .89, .955)],
              "book-scene-sugar-drop-1.png": [(.80, .89, .97, .97)]}


def prep(rel, cut, maxpx):
    os.makedirs(TMP, exist_ok=True)
    im = Image.open(os.path.join(ROOT, rel))
    if cut:
        im = im.convert("RGBA"); im = im.crop(im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox())
    else:
        im = im.convert("RGB")
        # The model signed two scenes with a fake scribble: cover just that spot with the texture beside it.
        w, h = im.size
        for fx0, fy0, fx1, fy1 in SIGNATURES.get(os.path.basename(rel), []):
            bx0, by0, bx1, by1 = int(w * fx0), int(h * fy0), int(w * fx1), int(h * fy1)
            im.paste(im.crop((bx0, by0 - (by1 - by0), bx1, by0)), (bx0, by0))   # patch taken from just above
        # Kept at the generated size (about 200 DPI on the page) so the deck can be shared; upscale before print.
        return_path = os.path.join(TMP, os.path.basename(rel).rsplit(".", 1)[0] + ".jpg")
        im.save(return_path, quality=82)
        return return_path, im.size
    im.thumbnail((maxpx, maxpx), Image.LANCZOS)
    out = os.path.join(TMP, os.path.basename(rel).rsplit(".", 1)[0] + (".png" if cut else ".jpg"))
    im.save(out, **({"optimize": True} if cut else {"quality": 88}))
    return out, im.size


def put(s, key, cx, cy, w, flip=False, deg=0):
    """Character cut-out centred at (cx, cy), w px wide. Placeholder label if the art does not exist yet."""
    rel = ART[key]
    if not os.path.exists(os.path.join(ROOT, rel)):
        MISSING.append(rel); label(s, cx - w / 2, cy - 40, w, 80, f"[{key}]"); return
    path, (iw, ih) = prep(rel, True, 1000)
    cx, cy, w = sx(cx), sy(cy), sx(w)
    h = w * ih / iw
    pic = s.shapes.add_picture(path, Emu(int((cx - w / 2) * PX)), Emu(int((cy - h / 2) * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    pic.rotation = deg
    if flip:
        pic._element.spPr.find("{http://schemas.openxmlformats.org/drawingml/2006/main}xfrm").set("flipH", "1")


def scene(s, key):
    rel = ART[key]
    if not os.path.exists(os.path.join(ROOT, rel)):
        MISSING.append(rel); label(s, 0, 0, W, H, f"[scene: {key}]"); return
    path, (iw, ih) = prep(rel, False, 4000)
    r = max(W / iw, H / ih); w, h = iw * r, ih * r                    # cover the page
    s.shapes.add_picture(path, Emu(int((W - w) / 2 * PX)), Emu(int((H - h) / 2 * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def label(s, x, y, w, h, t):
    tb = s.shapes.add_textbox(Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    tf = tb.text_frame; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = t; r.font.size = Pt(14); r.font.name = HEAD; r.font.bold = True
    r.font.color.rgb = RGBColor.from_string(BROWN)


def words(s, x, y, w, h, paras, pt=30):
    """Story text on a cream paper panel. paras: list of strings, one paragraph each. Kept inside the safe area."""
    x, y, w, h = sx(x), sy(y), sx(w), sy(h)
    x = max(x, SAFE); y = max(y, SAFE); w = min(w, W - SAFE - x); h = min(h, H - SAFE - y)
    pt = round(pt * FS, 1)
    panel = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    panel.fill.solid(); panel.fill.fore_color.rgb = RGBColor.from_string(CREAM); panel.line.fill.background()
    panel.shadow.inherit = False
    tb = s.shapes.add_textbox(Emu(int((x + 40) * PX)), Emu(int((y + 30) * PX)), Emu(int((w - 80) * PX)), Emu(int((h - 60) * PX)))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, t in enumerate(paras):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.line_spacing = 1.18; p.space_after = Pt(10)
        r = p.add_run(); r.text = t; f = r.font
        f.size = Pt(pt); f.name = SERIF; f.color.rgb = RGBColor.from_string(INK)


def fade(s, top=True, depth=0.34):
    """Soft cream fade from the top (or bottom) edge into the picture, so black text reads without a box.
    Drawn as a transparent PNG (smooth ease-out), placed as its own picture so it can be moved or deleted."""
    os.makedirs(TMP, exist_ok=True)
    h = int(H * depth); path = os.path.join(TMP, f"fade-{'top' if top else 'bottom'}.png")
    if not os.path.exists(path):
        im = Image.new("RGBA", (64, h), (0xF3, 0xF1, 0xEA, 0)); px = im.load()
        for yy in range(h):
            t = yy / (h - 1) if top else 1 - yy / (h - 1)       # 0 at the page edge, 1 inside the picture
            a = int(225 * (1 - t) ** 1.6)
            for xx in range(64): px[xx, yy] = (0xF3, 0xF1, 0xEA, a)
        im.save(path)
    y = 0 if top else H - h
    s.shapes.add_picture(path, 0, Emu(int(y * PX)), Emu(int(W * PX)), Emu(int(h * PX)))


def line(s, t, top=True, pt=26):
    """One or two short lines of black story text, centred, inside the safe area, on a fade."""
    fade(s, top)
    y = SAFE + 10 if top else H - SAFE - 180
    tb = s.shapes.add_textbox(Emu(int(SAFE * PX)), Emu(int(y * PX)), Emu(int((W - 2 * SAFE) * PX)), Emu(int(170 * PX)))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.TOP if top else MSO_ANCHOR.BOTTOM
    for i, para in enumerate(t.split("\n")):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER; p.line_spacing = 1.2
        r = p.add_run(); r.text = para; f = r.font
        f.size = Pt(pt); f.name = SERIF; f.color.rgb = RGBColor.from_string("1A1A1A")


def page_no(s, n):
    tb = s.shapes.add_textbox(Emu(int((W / 2 - 40) * PX)), Emu(int((H - SAFE - 30) * PX)), Emu(int(80 * PX)), Emu(int(30 * PX)))
    p = tb.text_frame.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = str(n); r.font.size = Pt(11); r.font.name = SERIF
    r.font.color.rgb = RGBColor.from_string(CREAM)


def new_page(prs, note):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.notes_slide.notes_text_frame.text = (note + " PRINT: 10 x 8 in landscape trim, 0.125 in bleed (page 10.25 x 8.25 in), "
                                           "text 0.5 in inside trim, 300 DPI art.")
    return s


# ---------------------------------------------------------------- title, plain and appendix pages
def title(s, t, sub):
    tb = s.shapes.add_textbox(Emu(int(SAFE * PX)), Emu(int((SAFE + 40) * PX)), Emu(int((W - 2 * SAFE) * PX)), Emu(int(300 * PX)))
    tf = tb.text_frame; tf.word_wrap = True
    for i, (txt, pt, italic) in enumerate([(t, 48, False)] + ([(sub, 22, True)] if sub else [])):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = PP_ALIGN.CENTER; p.space_after = Pt(8)
        r = p.add_run(); r.text = txt; f = r.font
        f.size = Pt(pt); f.name = SERIF; f.italic = italic; f.color.rgb = RGBColor.from_string("1A1A1A")


def plain(s, color=CREAM):
    bg = s.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, Emu(W * PX), Emu(H * PX))
    bg.fill.solid(); bg.fill.fore_color.rgb = RGBColor.from_string(color); bg.line.fill.background(); bg.shadow.inherit = False


def words_plain(s, paras, x=None, y=None, w=None, h=None, pt=16, italic=False, align=PP_ALIGN.CENTER, head=None):
    x = SAFE if x is None else x; w = (W - 2 * SAFE) if w is None else w
    y = SAFE if y is None else y; h = (H - SAFE - y) if h is None else h
    tb = s.shapes.add_textbox(Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    tf = tb.text_frame; tf.word_wrap = True
    items = ([(head, True)] if head else []) + [(t, False) for t in paras]
    for i, (t, is_head) in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.alignment = align; p.space_after = Pt(6); p.line_spacing = 1.15
        r = p.add_run(); r.text = t; f = r.font
        f.size = Pt(28 if is_head else pt); f.name = SERIF; f.italic = italic and not is_head
        f.color.rgb = RGBColor.from_string("1A1A1A")


def cast_card(prs, name, about, keys, note):
    """One character on cream: the cut-out(s), the name and one line about them."""
    s = new_page(prs, "Appendix, character: " + note)
    plain(s)
    words_plain(s, [about], y=SAFE, h=170, pt=16, head=name)
    n = len(keys); slot = (W - 2 * SAFE) / n
    for i, key in enumerate(keys):
        rel = ART.get(key, key)
        if not os.path.exists(os.path.join(ROOT, rel)): MISSING.append(rel); continue
        cut = rel.startswith(CUT)
        path, (iw, ih) = prep(rel, cut, 1000) if cut else prep_small(rel)
        bw, bh = slot - 40, H - SAFE - 330 - SAFE
        r = min(bw / iw, bh / ih); w, h = iw * r, ih * r
        x = SAFE + i * slot + (slot - w) / 2; y = SAFE + 300 + (bh - h) / 2
        s.shapes.add_picture(path, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def prep_small(rel):
    """Whole picture (not cut out), kept small: for appendix tiles."""
    os.makedirs(TMP, exist_ok=True)
    im = Image.open(os.path.join(ROOT, rel)).convert("RGB"); im.thumbnail((1000, 1000), Image.LANCZOS)
    out = os.path.join(TMP, "small-" + os.path.basename(rel).rsplit(".", 1)[0] + ".jpg"); im.save(out, quality=84)
    return out, im.size


def appendix(prs):
    s = new_page(prs, "Appendix divider.")
    plain(s, "E9E3D6")
    words_plain(s, ["Characters, scenes, story notes and print notes.", "Not part of the printed book."],
                y=420, pt=18, italic=True, head="Appendix")

    cast_card(prs, "Rose", "About 6. Curious, messy and kind. She talks to the ground (“Night night, dirt!”) and never "
              "knows anyone hears her.", ["rose", "rose-run", "rose-pull"], "Rose, three poses.")
    cast_card(prs, "Barry the Bacterium", "Rod-shaped and always hungry. When he eats sugar he splits into two Barrys, "
              "then four. He never knows which Barry he is.", ["barry"], "Barry = critter-bacillus.")
    cast_card(prs, "Myco the mycorrhizal fungus", "The town's postman. His long arms reach everywhere and hold hands "
              "with the tree roots, trading minerals for the sugars the roots make. In Book 1 he explains plastic.",
              ["myco"], "Myco = critter-mycorrhiza v2.")
    cast_card(prs, "Pip the Flagellate", "Small, fast and nervous, with two long tails. He has a crush on Ama.",
              ["pip"], "Pip.")
    cast_card(prs, "Ama the Amoeba", "Changes shape when she's embarrassed.", ["ama"], "Ama.")
    cast_card(prs, "For later books", "Ned the Nematode (night watchman), Cilia the Ciliate (arrives when the soil "
              "runs out of air), and more of the soil food web.",
              [ORIG + "book-ned-nematode-1.png", CUT + "critter-paramecium-1.png", CUT + "critter-nematode-bacterial-1.png"],
              "Ned (book-ned-nematode), Cilia (critter-paramecium), a bacterial-feeding nematode.")
    cast_card(prs, "More creatures", "From the creature set, for future books.",
              [CUT + "critter-cocci-4.png", CUT + "critter-testate-amoeba-1.png", "lolly"],
              "Cocci, testate amoeba, the lollipop cut-out.")

    # scene library: every scene used in the book, four per slide
    keys = ["garden", "flowers", "lolly-soil", "town", "house", "drop", "root-road", "dinner", "stick", "morning",
            "apple", "night", "bed", "apple-below"]
    for k in range(0, len(keys), 4):
        s = new_page(prs, "Appendix: scene library " + ", ".join(ART[x] for x in keys[k:k + 4]))
        plain(s); words_plain(s, [], y=SAFE, h=80, head="Scene library")
        gw, gh = (W - 2 * SAFE - 40) / 2, (H - 2 * SAFE - 140) / 2
        for i, key in enumerate(keys[k:k + 4]):
            path, (iw, ih) = prep_small(ART[key])
            r = min(gw / iw, (gh - 30) / ih); w, h = iw * r, ih * r
            x = SAFE + (i % 2) * (gw + 40) + (gw - w) / 2; y = SAFE + 110 + (i // 2) * (gh + 20)
            s.shapes.add_picture(path, Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
            words_plain(s, [key], x=SAFE + (i % 2) * (gw + 40), y=y + h + 2, w=gw, h=30, pt=11)

    s = new_page(prs, "Appendix: the world.")
    plain(s)
    words_plain(s, ["Above ground is Rose's garden. Below it is a whole town in the soil, lit by a soft brown glow, "
                    "with tunnels for streets and soil crumbs for houses.",
                    "Every story starts with something Rose does up top, and the town lives with the result.",
                    "Every book ends with Rose learning one new thing about what the garden likes, without ever "
                    "knowing who taught her."], align=PP_ALIGN.LEFT, head="The world")
    s = new_page(prs, "Appendix: running threads and later books.")
    plain(s)
    words_plain(s, ["Barry's hunger: how many Barrys there are shows how much food came down.",
                    "Pip and Ama: Pip gets one small step closer in each book.",
                    "Cilia's warnings: when she arrives, the soil needs air.",
                    "Later books: The Apple Core (a happy feast), The Flood (too much water, Cilia arrives), The Spade "
                    "(Myco's arms are cut and regrow), Spike's Raid (a root-nibbling nematode; Pip is brave), "
                    "Winter Sleep (the town slows down)."], align=PP_ALIGN.LEFT, head="Running threads and later books")
    s = new_page(prs, "Appendix: the science behind Book 1.")
    plain(s)
    words_plain(s, ["Soil microbes break food down with enzymes that fit things that were once alive: leaves, fruit, "
                    "bread, sugar. In the book these are the “keys”.",
                    "Plastic is made of long chains that soil enzymes mostly cannot unlock. It does not rot away; it "
                    "slowly breaks into tiny pieces (microplastics) and can last hundreds of years.",
                    "Bacteria multiply by splitting in two when they have food, which is why there are more Barrys.",
                    "Mycorrhizal fungi trade minerals and water with roots in exchange for sugars."],
                align=PP_ALIGN.LEFT, head="The science behind Book 1")
    s = new_page(prs, "Appendix: print notes.")
    plain(s)
    words_plain(s, ["Trim size 10 × 8 in landscape. Each slide is 10.25 × 8.25 in: trim plus 0.125 in bleed on "
                    "every side.",
                    "Text and page numbers stay at least 0.5 in inside the trim.",
                    "32 book pages (title, dedication, 29 story pages, The End). Picture books are printed in "
                    "multiples of 8 pages.",
                    "The art is about 200 DPI at this size. Upscale the scenes to 300 DPI before sending to a printer.",
                    "Remove the appendix before exporting the print file."], align=PP_ALIGN.LEFT, head="Print notes")


def build():
    """Slow opening: one or two things per page, very few words (Linnea, 4 Oct 2026). The sugar, the Barrys and
    the rest of the town come later in the book."""
    prs = Presentation(); prs.slide_width, prs.slide_height = Emu(W * PX), Emu(H * PX)

    s = new_page(prs, "Title page.")
    scene(s, "garden"); fade(s, True, 0.5)
    title(s, "Under Rose's Garden", "Book 1: The Lollipop")

    s = new_page(prs, "Dedication page (left blank for Linnea to fill in).")
    plain(s); words_plain(s, ["For ..."], y=520, pt=24, italic=True)

    s = new_page(prs, "Page 1. The garden after rain, nobody in it yet.")
    scene(s, "garden"); line(s, "It had rained all afternoon."); page_no(s, 1)

    s = new_page(prs, "Page 2. Close-up: the flowers, still dripping.")
    scene(s, "flowers"); line(s, "Everything was still dripping."); page_no(s, 2)

    s = new_page(prs, "Page 3. Rose and her strawberry lollipop.")
    scene(s, "garden"); put(s, "rose", 1060, 700, 420); line(s, "Rose had a strawberry lollipop."); page_no(s, 3)

    s = new_page(prs, "Page 4. Close-up: the lollipop has dropped into the soft soil.")
    scene(s, "lolly-soil"); line(s, "Plop.", top=False, pt=32); page_no(s, 4)

    s = new_page(prs, "Page 5. Rose runs inside for dinner and says goodnight to the ground.")
    scene(s, "garden"); put(s, "rose-run", 1180, 720, 400)
    line(s, "“Rose! Dinner!”\n“Night night, dirt!”"); page_no(s, 5)

    s = new_page(prs, "Page 6. Underground: the town under the garden, quiet. Someone heard her.")
    scene(s, "town"); line(s, "Down below, someone heard her.", top=False); page_no(s, 6)

    # Pages 7 to 16: the town wakes up, one thing at a time.
    s = new_page(prs, "Page 7. Barry's crumb house, Barry outside it.")
    scene(s, "house"); put(s, "barry", 1220, 780, 400); line(s, "This is Barry. He lives in a crumb house."); page_no(s, 7)

    s = new_page(prs, "Page 8. A single pale sugar drop hangs from the ceiling.")
    scene(s, "drop"); line(s, "Drip.", top=False, pt=32); page_no(s, 8)

    s = new_page(prs, "Page 9. Barry under the drop, tasting it.")
    scene(s, "drop"); put(s, "barry", 800, 560, 360); line(s, "Barry had a taste.\n“Sugar!”", top=False); page_no(s, 9)

    s = new_page(prs, "Page 10. Barry has split into two Barrys (two copies of the same cut-out).")
    scene(s, "house"); put(s, "barry", 1060, 780, 360); put(s, "barry", 1360, 780, 360, flip=True)
    line(s, "And then there were two Barrys."); page_no(s, 10)

    s = new_page(prs, "Page 11. Four Barrys on the street.")
    scene(s, "town")
    for i, (x, y) in enumerate([(380, 840), (680, 870), (980, 840), (1280, 870)]):
        put(s, "barry", x, y, 300, flip=bool(i % 2))
    line(s, "“Which Barry am I?” asked Barry.", top=False); page_no(s, 11)

    s = new_page(prs, "Page 12. Cut away, above ground: Rose at dinner, looking out at the rainy garden.")
    scene(s, "dinner"); line(s, "Up above, Rose was having her soup.", top=False); page_no(s, 12)

    s = new_page(prs, "Page 13. Myco the postman on a root road (critter-mycorrhiza v2).")
    scene(s, "root-road"); put(s, "myco", 800, 640, 620); line(s, "Myco the postman carried the news.", top=False)
    page_no(s, 13)

    s = new_page(prs, "Page 14. Pip and Ama arrive.")
    scene(s, "town"); put(s, "pip", 520, 760, 380); put(s, "ama", 1060, 780, 420)
    line(s, "Pip came zooming. Ama came drifting.", top=False); page_no(s, 14)

    # Grandma Worm was removed from the cast (Linnea, 4 Oct 2026); pages 15 and 16 no longer use her or her room.
    s = new_page(prs, "Page 15. Everyone together on the street: four Barrys, Pip, Ama and Myco.")
    scene(s, "town")
    for i, (x, y) in enumerate([(300, 870), (520, 890), (1180, 880), (1400, 900)]):
        put(s, "barry", x, y, 250, flip=bool(i % 2))
    put(s, "pip", 760, 760, 300); put(s, "ama", 960, 790, 320)
    line(s, "It turned into a party.", top=False); page_no(s, 15)

    s = new_page(prs, "Page 16. The sugar drop again, quiet. Cliffhanger: the lollipop stick is coming (next pages).")
    scene(s, "drop"); line(s, "Then something much bigger began to come down.", top=False); page_no(s, 16)

    # Pages 17 to 26: the stick, Myco explains plastic, Rose takes it away (Linnea, 4 Oct 2026).
    s = new_page(prs, "Page 17. The lollipop stick has come down into the street. The candy has melted away.")
    scene(s, "stick"); line(s, "It was a stick.", top=False, pt=32); page_no(s, 17)

    s = new_page(prs, "Page 18. Barry tries to eat it.")
    scene(s, "stick"); put(s, "barry", 1040, 780, 420)
    line(s, "Barry took a bite.\nNothing happened.", top=False); page_no(s, 18)

    s = new_page(prs, "Page 19. Pip pokes it.")
    scene(s, "stick"); put(s, "pip", 560, 760, 420)
    line(s, "Pip gave it a poke.\nNothing happened.", top=False); page_no(s, 19)

    s = new_page(prs, "Page 20. Myco wraps his arms around it, looking for something to trade.")
    scene(s, "stick"); put(s, "myco", 900, 700, 520)
    line(s, "Myco wrapped his arms around it.\nThere was nothing to trade.", top=False); page_no(s, 20)

    s = new_page(prs, "Page 21. Myco begins to explain. True science: soil life breaks food down with enzymes that "
                      "fit things that were once alive.")
    scene(s, "root-road"); put(s, "myco", 800, 640, 560)
    line(s, "“We can eat anything that was once alive,” said Myco.", top=False); page_no(s, 21)

    s = new_page(prs, "Page 22. The keys image: each kind of food has a key that unlocks it.")
    scene(s, "town"); put(s, "myco", 800, 760, 480)
    line(s, "“Leaves. Apples. Bread. Sugar.\nWe have a key for each of them.”", top=False); page_no(s, 22)

    s = new_page(prs, "Page 23. True science: plastic is long chains the soil's enzymes mostly cannot unlock. It does "
                      "not rot away; it slowly breaks into tiny bits (microplastics) and lasts hundreds of years.")
    scene(s, "stick"); put(s, "myco", 1200, 760, 440)
    line(s, "“But this is plastic.\nNobody down here has a key for it.”", top=False); page_no(s, 23)

    s = new_page(prs, "Page 24. Pip and Ama. Pip's crush: one small step in every book.")
    scene(s, "town"); put(s, "pip", 660, 800, 340); put(s, "ama", 1000, 820, 360)
    line(s, "Pip tried to say hello to Ama.\nMaybe tomorrow.", top=False); page_no(s, 24)

    s = new_page(prs, "Page 25. Morning, above ground. Rose finds the stick and pulls it out.")
    scene(s, "morning"); put(s, "rose-pull", 890, 700, 500)   # her body covers the stick in the scene
    line(s, "In the morning, Rose found the stick.\nShe put it in the bin."); page_no(s, 25)

    s = new_page(prs, "Page 26. Rose plants an apple core instead: good food for the soil.")
    scene(s, "apple"); line(s, "Then she planted an apple core.\n“Night night, dirt!”", top=False); page_no(s, 26)

    # Pages 27 to 29: goodnight (Linnea, 4 Oct 2026).
    s = new_page(prs, "Page 27. The town at night; the Barrys answer Rose's goodnight.")
    scene(s, "night")
    for i, (x, y) in enumerate([(300, 740), (480, 770), (660, 740), (840, 770), (1020, 740), (1200, 770)]):
        put(s, "barry", x, y, 200, flip=bool(i % 2))
    line(s, "Down below, all the sleepy Barrys said,\n“Night night, Rose.”", top=False); page_no(s, 27)

    s = new_page(prs, "Page 28. Rose asleep. She never knows who answered.")
    scene(s, "bed"); line(s, "Rose didn't hear them.\nBut she smiled in her sleep."); page_no(s, 28)

    s = new_page(prs, "Page 29. Last page, and a hint of Book 2 (The Apple Core): roots and fungal threads reach for it.")
    scene(s, "apple-below"); line(s, "And down in the dark, someone smelled apples.", top=False); page_no(s, 29)

    s = new_page(prs, "The End.")
    scene(s, "flowers"); fade(s, True, 0.5); title(s, "The End", None)

    appendix(prs)
    out = os.path.join(HERE, "under-roses-garden-book1-complete.pptx")
    prs.save(out)
    print("wrote", os.path.relpath(out, ROOT))
    if MISSING: print("MISSING ART:", sorted(set(MISSING)))


if __name__ == "__main__":
    build()
