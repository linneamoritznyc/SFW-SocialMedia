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


def generate(name, version):
    out = ORIG / f"{name}-{version}.png"
    style = STYLE
    if name in STYLE_OVERRIDES:
        style = style.replace(*STYLE_OVERRIDES[name])
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
    args = ap.parse_args()
    ORIG.mkdir(parents=True, exist_ok=True)
    for n in args.names:
        p = generate(n, args.version)
        if p:
            cutout(p)
            print(f"done {p.name}  running est total ${total_cost():.2f}")
        time.sleep(25)  # free Replicate account: one request at a time, about 6 a minute
