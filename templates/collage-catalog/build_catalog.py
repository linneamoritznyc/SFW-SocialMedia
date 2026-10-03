"""Collage catalog: every cut-paper piece we have made, one per slide, on brand green with its name above it.
Not a social post; a library to browse and copy pieces from.

python3 templates/collage-catalog/build_catalog.py  ->  templates/collage-catalog/collage-catalog.pptx
Pieces come from assets/collage/cutouts/ (background removed). Whole-scene pieces, where background removal loses
the scene, come from assets/collage/originals/. Images are downscaled to 640 px so the deck stays under GitHub's file size limits.
Every element is editable: name text box, picture, background.
"""
import os, sys
from PIL import Image
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CUT, ORIG = "assets/collage/cutouts/", "assets/collage/originals/"
TMP = os.path.join(ROOT, "renders", ".tmp", "catalog")
PX = 9525
W, H = 1080, 1350
GREEN, CREAM, SAGE = "31662F", "F3F1EA", "B1BCB1"          # brand palette, docs/brand-colors.md
HEAD, BODY = "Montserrat", "Source Sans 3"

# Shown whole (from originals): scenes whose background removal would cut them apart.
SCENES = {"city-block-weed-1", "woodlot-pasture-1", "tree-compaction-1"}
# Left out: the banned soil cross-section look, tree attempts not used, and line art (not this style).
SKIP = {"field-cross-section-1", "tree-compaction-2", "tree-compaction-3"}

NAMES = {
    "cute-bacterium": "Bacterium", "nematode": "Nematode", "fungal-hyphae": "Fungal hyphae",
    "earthworm-paper": "Earthworm", "mushroom-paper": "Mushroom", "microscope-paper": "Microscope",
    "flagellate-ciliate": "Flagellate and ciliate", "bacteria-sand-grain": "Bacteria on a sand grain",
    "fungi-tie-crumbs": "Fungi tying soil crumbs", "soil-crumb": "Soil crumb (micro aggregate)",
    "pizza-box-root": "Pizza box with a root", "cupcakes-cookies-root": "Cupcakes and cookies on a root",
    "cupcakes-root-microbes": "Cupcakes, a root and microbes", "mixing-bowl-root": "Mixing bowl on a root",
    "sugar-jars": "Sugar, honey and molasses", "eggs-milk": "Eggs and milk", "flour-sack": "Flour sack",
    "tree-compaction": "Tree on a compacted layer", "tree-deep-roots": "Tree with deep roots",
    "dandelion-short-root": "Dandelion, short root", "lettuce-long-root": "Lettuce, long root",
    "periodic-table": "Periodic table", "woodlot-pasture": "Woodlot and pasture",
    "city-block-weed": "Weed in a cracked sidewalk", "biochar-compost": "Biochar and compost",
    "bird-beetle-wildflower": "Bird, beetle and wildflower", "coffee-cherries-branch": "Coffee cherries",
    "coffee-beans-paper": "Coffee beans", "coffee-cup-paper": "Coffee cup", "cocoa-beans": "Cocoa beans",
    "citrus-orange": "Orange", "cacao-pod": "Cacao pod", "banana-bunch": "Bananas", "tithonia-flower": "Tithonia",
    "happy-seedling": "Happy seedling", "seedling-tray": "Seedling tray", "leaf-sprig-paper": "Leaf sprig",
    "leaf-frame": "Leaf frame", "dried-flowers-1": "Dried flowers", "dried-flowers-2": "Dried flower sprig",
    "poop-sticker": "Poop", "cow-poop-sticker": "Cow pat", "dot-green": "Green dot", "dot-yellow": "Yellow dot",
    "dot-red": "Red dot",
    # creatures
    "critter-bacillus": "Rod-shaped bacterium (bacillus)", "critter-cocci": "Round bacteria (cocci)",
    "critter-spiral-bacterium": "Spiral bacterium", "critter-biofilm": "Biofilm bacteria",
    "critter-actinobacteria": "Actinobacteria", "critter-hypha": "Fungal hypha", "critter-mycorrhiza": "Mycorrhizal fungus",
    "critter-spore": "Fungal spore", "critter-mushroom": "Mushroom (fruiting body)", "critter-naked-amoeba": "Naked amoeba",
    "critter-testate-amoeba": "Testate amoeba", "critter-paramecium": "Paramecium", "critter-vorticella": "Vorticella",
    "critter-nematode-bacterial": "Bacterial-feeding nematode", "critter-nematode-fungal": "Fungal-feeding nematode",
    "critter-nematode-predatory": "Predatory nematode", "critter-nematode-root": "Root-feeding nematode",
    "critter-springtail": "Springtail (collembola)", "critter-oribatid-mite": "Oribatid mite",
    "critter-predatory-mite": "Predatory mite", "critter-pseudoscorpion": "Pseudoscorpion",
    "critter-tardigrade": "Tardigrade (water bear)", "critter-rotifer": "Rotifer", "critter-earthworm": "Earthworm",
    "critter-potworm": "Pot worm (enchytraeid)", "critter-woodlouse": "Woodlouse", "critter-centipede": "Centipede",
    "critter-root-tip": "Root tip with root hairs",
}

SECTIONS = [
    ("Soil food web creatures", lambda k: k.startswith("critter-")),
    ("Soil life", lambda k: k in {"cute-bacterium", "nematode", "fungal-hyphae", "earthworm-paper", "mushroom-paper",
                                  "flagellate-ciliate", "bacteria-sand-grain", "fungi-tie-crumbs", "soil-crumb"}),
    ("Plants and roots", lambda k: k in {"tree-compaction", "tree-deep-roots", "dandelion-short-root", "lettuce-long-root",
                                         "happy-seedling", "seedling-tray", "leaf-sprig-paper", "leaf-frame", "tithonia-flower",
                                         "dried-flowers-1", "dried-flowers-2", "bird-beetle-wildflower"}),
    ("Kitchen and exudates", lambda k: k in {"pizza-box-root", "cupcakes-cookies-root", "cupcakes-root-microbes",
                                             "mixing-bowl-root", "sugar-jars", "eggs-milk", "flour-sack"}),
    ("Farm and food", lambda k: k in {"coffee-cherries-branch", "coffee-beans-paper", "coffee-cup-paper", "cocoa-beans",
                                      "citrus-orange", "cacao-pod", "banana-bunch", "biochar-compost", "pineapple"}),
    ("Places and things", lambda k: True),
]


def pieces():
    out = {}
    for f in sorted(os.listdir(os.path.join(ROOT, CUT))):
        stem = f.rsplit(".", 1)[0]
        if not f.endswith(".png") or f.startswith("line-") or stem in SKIP: continue
        key = stem.rsplit("-", 1)[0]
        out[key] = (ORIG if stem in SCENES else CUT) + f
    return out


def shrink(rel, cut):
    """Trimmed (cutouts) and downscaled to 1200 px, saved to a temp file."""
    os.makedirs(TMP, exist_ok=True)
    im = Image.open(os.path.join(ROOT, rel))
    if cut:
        im = im.convert("RGBA"); im = im.crop(im.split()[3].point(lambda v: 255 if v > 20 else 0).getbbox())
    else:
        im = im.convert("RGB")
    im.thumbnail((640, 640), Image.LANCZOS)
    out = os.path.join(TMP, os.path.basename(rel).rsplit(".", 1)[0] + (".png" if cut else ".jpg"))
    im.save(out, **({"optimize": True} if cut else {"quality": 88}))
    return out, im.size


def textbox(s, x, y, w, h, t, pt, color, font, bold, align=PP_ALIGN.CENTER, track=None):
    tb = s.shapes.add_textbox(Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))
    tf = tb.text_frame; tf.word_wrap = True; tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = align
    r = p.add_run(); r.text = t; f = r.font
    f.size = Pt(pt); f.name = font; f.bold = bold; f.color.rgb = RGBColor.from_string(color)
    if track: r._r.get_or_add_rPr().set("spc", str(track * 100))


def slide(prs):
    s = prs.slides.add_slide(prs.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = RGBColor.from_string(GREEN)
    return s


def build():
    prs = Presentation(); prs.slide_width, prs.slide_height = Emu(W * PX), Emu(H * PX)
    all_ = pieces(); done = set(); n = 0
    s = slide(prs)                                                              # title slide
    textbox(s, 80, 420, 920, 120, "Paper-cut field notes", 72, CREAM, HEAD, True)
    textbox(s, 80, 560, 920, 60, "The Soil Food Web Foundation collage library", 30, SAGE, BODY, False)
    logo = os.path.join(ROOT, "assets/logo/foundation-logo-white.png")
    s.shapes.add_picture(logo, Emu(int((W - 180) / 2 * PX)), Emu(int(900 * PX)), Emu(int(180 * PX)), Emu(int(180 * 668 / 743 * PX)))
    for title, test in SECTIONS:
        keys = [k for k in all_ if k not in done and test(k)]
        if not keys: continue
        s = slide(prs)                                                          # section divider
        textbox(s, 80, 560, 920, 200, title, 64, CREAM, HEAD, True)
        textbox(s, 80, 760, 920, 50, f"{len(keys)} pieces", 26, SAGE, BODY, False)
        for k in keys:
            done.add(k); n += 1
            rel = all_[k]; cut = rel.startswith(CUT)
            path, (iw, ih) = shrink(rel, cut)
            s = slide(prs)
            s.notes_slide.notes_text_frame.text = f"Piece: {rel}. Made with flux-2-pro and style-reference.png (tools/collage_generate.py)."
            textbox(s, 80, 70, 920, 36, title.upper(), 18, SAGE, HEAD, True, track=2)
            textbox(s, 80, 115, 920, 140, NAMES.get(k, k.replace("-", " ").capitalize()), 48, CREAM, HEAD, True)
            bx, by, bw, bh = 100, 300, 880, 960
            r = min(bw / iw, bh / ih); w, h = iw * r, ih * r
            s.shapes.add_picture(path, Emu(int((bx + (bw - w) / 2) * PX)), Emu(int((by + (bh - h) / 2) * PX)),
                                 Emu(int(w * PX)), Emu(int(h * PX)))
    out = os.path.join(HERE, "collage-catalog.pptx")
    prs.save(out)
    print("wrote", os.path.relpath(out, ROOT), n, "pieces")


if __name__ == "__main__":
    build()
