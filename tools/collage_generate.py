"""Generate cut-paper collage illustrations with Replicate (flux-2-pro) and cut out backgrounds locally with rembg.

Usage: python tools/collage_generate.py nematode fungal-hyphae amoeba --version 1
The token is read from REPLICATE_API_TOKEN (.env via python-dotenv, or the environment). It is never printed.
"""
import argparse
import datetime
import sys
import time
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

import replicate  # noqa: E402  (after load_dotenv so the token is in the environment)

ROOT = Path(__file__).resolve().parent.parent
ORIG = ROOT / "assets/collage/originals"
CUT = ROOT / "assets/collage/cutouts"
COST_FILE = ROOT / "generation-cost.txt"
REFERENCE = ROOT / "style-reference.png"

MODEL = "black-forest-labs/flux-2-pro"
STOP_AT = 9.00
# Estimate only: replicate.com pricing page was unreachable. Assumed $0.015 per output MP
# plus $0.015 per input MP, at 4 MP out and a ~2 MP reference. Verify against Replicate billing.
EST_PER_IMAGE = 0.09

STYLE = (
    "cut paper collage, kraft paper, graphite rubbing texture, colored pencil strokes, "
    "hand-cut uneven edges, overlapping paper layers, muted kraft brown, slate blue and graphite gray, "
    "one Food Web Green #156826 accent, cream paper background, scanned artwork. "
    "Use the reference image only for its cut-paper technique and texture, not its subjects or colors: "
    "no pink, no magenta, no red. Single subject centered and alone on a plain flat cream paper background, "
    "no text, no signature, no initials, no labels, no frame, no cast shadow, no torn or deckled paper edge."
)

LINE_STYLE = (
    "realistic botanical line drawing, fine black ink pen on plain white paper, scientific illustration style, "
    "clean confident contour lines with light hatching for shading, no color, no fill, no gray wash, "
    "single subject centered and alone, plain white background, no text, no signature, no frame, no border."
)

LINE_PIECES = {
    "coffee-branch": "a coffee plant branch with glossy leaves and clusters of coffee cherries",
    "cacao-pod": "a cacao pod hanging from a short stem with two leaves",
    "banana-plant": "a young banana plant with broad leaves",
    "pineapple-plant": "a pineapple growing on its plant with spiky leaves",
    "earthworm": "an earthworm curved in an S shape, showing its segments",
    "mushroom-cluster": "a small cluster of three wild mushrooms",
    "seedling-roots": "a young seedling with two leaves and its fine roots spreading below",
    "compost-pile": "a compost pile with a shovel and a garden fork leaning against it",
    "orange-branch": "a citrus branch with leaves and one orange",
    "tithonia": "a Mexican sunflower (Tithonia) flower with leaves on a stem",
    "millipede": "a millipede curled on a fallen leaf",
}

PIECES = {
    "nematode": "a bacterial-feeding nematode, a smooth tapered thread-like worm body, blunt head, pointed tail",
    "fungal-hyphae": "branching fungal hyphae, thin branching threads forming a network",
    "amoeba": "a naked amoeba, a soft irregular blob with rounded pseudopod lobes and a visible nucleus",
    "ciliate": "a ciliate protozoan, an oval cell covered in fine hairs (cilia)",
    "flagellate": "a flagellate protozoan, a small cell with one long whip-like tail (flagellum)",
    "vampire-amoeba": "a vampire amoeba, a small amoeba with a fine feeding probe piercing a fungal thread",
    "root-hairs": "fine root hairs, a root tip with many delicate hair-like extensions",
    "root-system": "a plant root system, a main root with branching lateral roots",
    "earthworm": "an earthworm, segmented pink-brown body with a clitellum band",
    "springtail": "a springtail, a tiny soil insect with a folded tail-like furcula and short antennae",
    "leaf-1": "a single simple oval leaf with a central vein",
    "leaf-2": "a single lobed oak-type leaf",
    "leaf-3": "a single long narrow grass-blade or willow-type leaf",
    "fallen-leaves": "a pile of fallen autumn leaves",
    "compost-pile": "a compost pile, a mound of mixed organic matter with a few leaves and food scraps",
    "microscope": "a laboratory microscope",
    "coffee-cup": "a coffee cup with coffee grounds spilling beside it",
    "eggshells": "broken eggshells, several curved shell fragments",
    "cotton-brief": "a plain folded cotton brief (underwear)",
    "raindrop-soil": "a single raindrop falling onto a small patch of soil",
    "poop-sticker": "a cute cartoon poop swirl sticker, three stacked soft kraft-brown paper coils with a pointed tip, small happy face drawn in graphite",
    "cow-poop-sticker": "a cute cow pat sticker, a flat round layered kraft-brown paper cow dung patty, wobbly concentric rings, small happy face drawn in graphite",
    "dot-green": "one flat round paper dot cut from Food Web Green #156826 colored paper, slightly uneven hand-cut circle, colored pencil texture",
    "dot-yellow": "one flat round paper dot cut from mustard yellow #D9A521 colored paper, slightly uneven hand-cut circle, colored pencil texture",
    "dot-red": "one flat round paper dot cut from brick red #B5382B colored paper, slightly uneven hand-cut circle, colored pencil texture",
    "dried-flowers-1": "a small bundle of pressed dried wildflowers and grasses, dried yarrow, oat stems and seed heads in faded ochre and straw colors",
    "dried-flowers-2": "a single pressed dried flower sprig, dried tansy with small button flowers and a few feathery leaves, faded ochre and olive",
    "hay-tuft": "a loose tuft of golden dry hay and straw stems",
    "feather": "a single soft speckled hen feather, brown and cream",
    "coffee-cup-spilled-grounds": "a cute cream coffee cup tipped on its side with dark brown coffee grounds spilling out in a little heap beside it",
    "field-cross-section": "a cross-section slice of a farm field like a slice of layered cake: short green cover crop plants on top, below them a thick layer of dark brown soil with pale plant roots and fine white branching fungal threads",
    "bird-beetle-wildflower": "a small brown songbird perched on a wildflower stem with yellow and blue flowers, and a small dark ground beetle at the foot of the stem, grouped together",
    "leaf-frame": "a square frame border made of overlapping cut-paper leaves, ferns and small sprigs in greens, kraft brown and slate blue, arranged around the edges, with a large empty plain cream center",
    "lemon-half": "a cute halved lemon, bright yellow cut-paper lemon half showing its segments, with a small leaf",
    "coffee-beans": "a small cute pile of three roasted coffee beans, dark brown cut paper with a center line on each bean",
    "sad-seedling": "a tiny droopy seedling sprouting from a small mound of soil, two drooping seed leaves, slightly wilted",
    "happy-seedling": "a tiny happy seedling sprouting from a small mound of dark soil, two perky round seed leaves",
    "microscope-paper": "a cute vintage laboratory microscope, simple chunky shapes, sage green and cream paper with graphite details",
    "leaf-sprig-paper": "a single cut-paper sprig of three rounded green leaves on a thin stem",
    "cute-bacterium": "a cute rod-shaped soil bacterium with a tiny smiling face and one wavy tail, pale green cut paper",
    "earthworm-paper": "a cute curled earthworm with a tiny smiling face, soft kraft pink-brown cut paper",
    "mushroom-paper": "a cute small brown mushroom with a round cap dotted with cream spots and a tiny smiling face",
    "coffee-cherries-branch": "a coffee plant branch with glossy dark green leaves and clusters of ripe red and green coffee cherries",
    "cacao-pod": "a single ripe cacao pod, ribbed and oval, ochre yellow with a short stem",
    "banana-bunch": "a small bunch of green and yellow bananas",
    "citrus-orange": "a whole orange with one leaf and a halved orange showing its segments",
    "pineapple": "a small cute pineapple with a spiky green crown",
    "coffee-cup-paper": "a cute cream coffee cup of black coffee on a saucer, with a tiny smiling face and a little curl of steam",
    "cocoa-beans": "three dried cocoa beans and one cacao pod split open showing pale beans inside",
    "coffee-beans-paper": "a small cute pile of roasted coffee beans, dark brown with a center line on each bean",
    "tithonia-flower": "a single Mexican sunflower (Tithonia) bloom, bright orange petals, with two green leaves on a stem",
    "seedling-tray": "a small wooden seedling tray holding six little pots of seedlings: lettuce, basil, a small tomato plant and tiny flower seedlings",
}


# November 2026, Dr. Elaine Ingham "How to Build Great Soil" series (cute cut-paper, with style-reference.png)
PIECES.update({
    "pizza-box-root": "a cute cardboard pizza delivery box, lid slightly open, with a pale plant root poking up out of it",
    "cupcakes-cookies-root": "a long pale plant root lying sideways with small cupcakes and round cookies sitting along it",
    "tree-compaction": "a simple side-view soil diagram: a small tree on top; under the ground its root goes straight down only a short way, then splits into long roots that run flat to the left and to the right, like an upside-down letter T, lying along the top of a thick flat gray stripe; the gray stripe is solid and has no roots in it; a small blue puddle sits on the gray stripe next to the roots; brown soil above and below the gray stripe",
    "tree-deep-roots": "a tall soil cross-section: a small tree above the ground with roots reaching deep down through crumbly dark soil full of small crumbs and pores",
    "bacteria-sand-grain": "a large rounded sand grain with several tiny cute rod-shaped bacteria clinging to it with little sticky glue strands",
    "soil-crumb": "a single small round soil crumb made of many tiny bits of sand, silt and clay stuck together",
    "fungi-tie-crumbs": "several small soil crumbs tied together by thin white fungal threads wrapped around them like string around parcels",
    "city-block-weed": "a small city block with two little buildings and a cracked sidewalk, a weed growing up through the crack",
    "woodlot-pasture": "a small woodlot of trees beside an open green pasture with a fence between them",
    "periodic-table": "a periodic table chart grid of small blank square tiles, a few tiles in pale lime green, the rest cream, no letters or numbers on the tiles",
    "dandelion-short-root": "a dandelion plant with a yellow flower and a short taproot",
    "lettuce-long-root": "a lettuce plant with a long, deep, branching root system",
    "mixing-bowl-root": "a mixing bowl with a wooden spoon, sitting on top of a pale plant root",
    "sugar-jars": "four glass jars: white sugar, brown sugar, golden honey and dark molasses",
    "eggs-milk": "a glass milk bottle and three eggs",
    "flour-sack": "a small cloth flour sack, slightly open, with a little flour spilling",
    "cupcakes-root-microbes": "cupcakes and cookies along a pale plant root with tiny cute round microbes gathered around them",
    "biochar-compost": "a small pile of black biochar charcoal pieces beside a small pile of dark crumbly compost",
    "flagellate-ciliate": "two cute single-celled soil protozoa face to face: a small oval flagellate with one long whip tail, and a larger oval ciliate covered in fine hairs",
})


# Soil food web creature set (Oct 2026): cute but anatomically right, googly eyes, small tan paper backing
CREATURE_STYLE_SWAP = ("no torn or deckled paper edge", "mounted on a small tan kraft paper backing with a softly torn edge")
CREATURES = {
    "critter-bacillus": "a rod-shaped bacterium (bacillus), a small smooth capsule shape with two googly eyes and a few thin wavy flagella",
    "critter-cocci": "a little cluster of four round cocci bacteria touching each other, each with tiny googly eyes",
    "critter-spiral-bacterium": "a spiral corkscrew-shaped bacterium with one googly eye at the front end",
    "critter-biofilm": "a group of small rod and round bacteria stuck together in a blob of sticky glossy clear paper glue, each with tiny googly eyes",
    "critter-actinobacteria": "actinobacteria: very thin branching threads like a delicate fan, with two tiny googly eyes at one thread tip",
    "critter-hypha": "a long fungal hypha thread with visible cross-walls (septa) and side branches, two googly eyes at the growing tip",
    "critter-mycorrhiza": "mycorrhizal fungal threads wrapping around a pale root hair, one thread tip with googly eyes waving",
    "critter-spore": "a round fungal spore like a small seed ball with one big googly eye",
    "critter-mushroom": "a small mushroom with a brown cap on a pale stem, two googly eyes on the stem",
    "critter-naked-amoeba": "a naked amoeba, a soft translucent blob mid-stretch with bulging lobed pseudopods and a visible nucleus, two googly eyes",
    "critter-testate-amoeba": "a testate amoeba: a soft blob peeking out of the opening of a small vase-shaped shell, two googly eyes",
    "critter-paramecium": "a paramecium, a slipper-shaped ciliate covered in short fine cilia hairs, two googly eyes",
    "critter-vorticella": "a vorticella, a bell-shaped ciliate with a ring of cilia at its rim, on a long thin coiled stalk, two googly eyes",
    "critter-nematode-bacterial": "a bacterial-feeding nematode, a smooth tapered worm with a smooth open tube-shaped mouth, two googly eyes",
    "critter-nematode-fungal": "a fungal-feeding nematode, a slim tapered worm with a thin needle-like stylet sticking out of its mouth, two googly eyes",
    "critter-nematode-predatory": "a predatory nematode, a tapered worm with a wide open mouth showing small teeth, two googly eyes",
    "critter-nematode-root": "a root-feeding nematode with a strong stylet pushed into a pale root, looking guilty with sideways googly eyes",
    "critter-springtail": "a springtail (collembola), a short soft body with long antennae and a folded spring tail (furcula) tucked underneath, two googly eyes",
    "critter-oribatid-mite": "an oribatid mite, a round armored shiny dark brown body on eight short legs, two googly eyes",
    "critter-predatory-mite": "a predatory mite with long legs and a pointed front, pale orange-brown, two googly eyes",
    "critter-pseudoscorpion": "a pseudoscorpion, a tiny flat body with big pincers held forward, no tail, two googly eyes",
    "critter-tardigrade": "a tardigrade (water bear), a chubby segmented body on eight stubby legs with little claws, two googly eyes",
    "critter-rotifer": "a rotifer with a wheel of cilia spinning at its head and a tapered body with a forked foot, two googly eyes",
    "critter-earthworm": "an earthworm with clear segments and a visible thick saddle band (clitellum), two googly eyes",
    "critter-potworm": "a small white pot worm (enchytraeid), slim and segmented, two googly eyes",
    "critter-woodlouse": "a woodlouse with segmented gray armored plates and short antennae, two googly eyes",
    "critter-centipede": "a centipede, a long flat segmented body with one pair of legs on each segment, two googly eyes",
    "critter-root-tip": "a plant root tip with fine root hairs, small clear drops of exudate leaking out, two googly eyes on the root cap",
}
PIECES.update(CREATURES)

# Colour exceptions to STYLE's "no red" rule (the user allowed a flat red paper dot only).
STYLE_OVERRIDES = {
    "dot-red": ("no pink, no magenta, no red", "no pink, no magenta, no other colors; the dot itself is brick red"),
    "dot-yellow": ("one Food Web Green #156826 accent, ", ""),
}


def total_cost():
    if not COST_FILE.exists():
        return 0.0
    total = 0.0
    for line in COST_FILE.read_text().splitlines():
        if line.startswith("TOTAL"):
            total = float(line.split("$")[1])
    return total


def log_cost(name, version, ok):
    total = total_cost() + (EST_PER_IMAGE if ok else 0.0)
    lines = [l for l in COST_FILE.read_text().splitlines() if not l.startswith("TOTAL")] if COST_FILE.exists() else [
        "Estimated cost log (estimate, not billing data). Stop at $9.00.",
    ]
    lines.append(f"{datetime.datetime.utcnow():%Y-%m-%d %H:%M} {name}-{version} {'ok' if ok else 'FAILED'} est ${EST_PER_IMAGE if ok else 0:.2f}")
    lines.append(f"TOTAL ${total:.2f}")
    COST_FILE.write_text("\n".join(lines) + "\n")
    return total


def generate(name, version, line=False):
    if line:
        return generate_line(name, version)
    out = ORIG / f"{name}-{version}.png"
    style = STYLE
    if name in STYLE_OVERRIDES:
        style = style.replace(*STYLE_OVERRIDES[name])
    if name in CREATURES:
        style = style.replace(*CREATURE_STYLE_SWAP)
    prompt = f"{PIECES[name]}. {style}"
    last_err = None
    for attempt in (1, 2):  # one retry at most
        if total_cost() >= STOP_AT:
            sys.exit(f"Stopping: estimated total reached ${STOP_AT:.2f}")
        try:
            with open(REFERENCE, "rb") as ref:
                output = replicate.run(
                    MODEL,
                    input={
                        "prompt": prompt,
                        "input_images": [ref],
                        "aspect_ratio": "1:1",
                        "resolution": "4 MP",
                        "output_format": "png",
                    },
                )
            first = output[0] if isinstance(output, (list, tuple)) else output
            out.write_bytes(first.read())
            log_cost(name, version, True)
            return out
        except Exception as e:  # noqa: BLE001
            last_err = e
            log_cost(name, version, False)
            # free account: 6 predictions a minute, burst of 1; a throttle (429) needs a real pause
            time.sleep(30 if "429" in str(e) else 3)
    print(f"FAILED {name}-{version}: {type(last_err).__name__}: {str(last_err)[:200]}")
    return None


def generate_line(name, version):
    """Line art: no style reference (it is cut paper), plain prompt. Saved to originals/line-<name>-<v>.png."""
    out = ORIG / f"line-{name}-{version}.png"
    prompt = f"{LINE_PIECES[name]}. {LINE_STYLE}"
    last_err = None
    for attempt in (1, 2):
        if total_cost() >= STOP_AT:
            sys.exit(f"Stopping: estimated total reached ${STOP_AT:.2f}")
        try:
            output = replicate.run(MODEL, input={"prompt": prompt, "aspect_ratio": "1:1", "resolution": "4 MP", "output_format": "png"})
            first = output[0] if isinstance(output, (list, tuple)) else output
            out.write_bytes(first.read())
            log_cost("line-" + name, version, True)
            return out
        except Exception as e:  # noqa: BLE001
            last_err = e
            log_cost("line-" + name, version, False)
            time.sleep(30 if "429" in str(e) else 3)
    print(f"FAILED line-{name}-{version}: {type(last_err).__name__}: {str(last_err)[:200]}")
    return None


def line_cutout(path, color=(0x22, 0x37, 0x1F)):
    """Dark ink becomes opaque Deep Green, white paper becomes transparent."""
    from PIL import Image, ImageOps
    CUT.mkdir(parents=True, exist_ok=True)
    g = ImageOps.autocontrast(Image.open(path).convert("L"), cutoff=1)
    a = g.point(lambda v: 0 if v > 235 else min(255, int((235 - v) * 1.35)))
    im = Image.new("RGBA", g.size, color + (0,)); im.putalpha(a)
    im = im.crop(a.point(lambda v: 255 if v > 40 else 0).getbbox())
    im.save(CUT / path.name)


def cutout(path):
    from PIL import Image
    from rembg import remove

    CUT.mkdir(parents=True, exist_ok=True)
    img = Image.open(path).convert("RGB")
    remove(img).save(CUT / path.name)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("names", nargs="+")
    ap.add_argument("--version", type=int, default=1)
    ap.add_argument("--line", action="store_true", help="realistic line drawing, no style reference")
    args = ap.parse_args()
    ORIG.mkdir(parents=True, exist_ok=True)
    for n in args.names:
        p = generate(n, args.version, args.line)
        if p:
            line_cutout(p) if args.line else cutout(p)
            print(f"done {p.name}  running est total ${total_cost():.2f}")
        time.sleep(25)  # free Replicate account: one request at a time, about 6 a minute
