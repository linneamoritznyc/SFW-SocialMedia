"""Generate clean line icons in the trifold's style with Replicate (flux-2-pro), one at a time, and save
reusable transparent PNGs in assets/icons/ (black original plus brand-colour versions).

Usage: python tools/icon_generate.py check-mark flame ...
The token is read from REPLICATE_API_TOKEN; it is never printed. Shares generation-cost.txt and the $10 cap
with tools/collage_generate.py: the log is read before every generation, and nothing runs that would pass the cap.
"""
import sys
from pathlib import Path

from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collage_generate import MODEL, EST_PER_IMAGE, total_cost, log_cost  # noqa: E402
import replicate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
ICONS = ROOT / "assets/icons"
ORIG = ICONS / "originals"
CAP = 10.00

STYLE = ("minimal flat line icon, single uniform medium stroke weight, rounded line caps and joins, pure black lines on a "
         "pure white background, clean vector pictogram for a professional editorial brochure, no fill, no shading, "
         "no gradient, no texture, no text, no letters, no frame, no border, no circle around it, one icon centered "
         "with a wide empty margin")

ICONSET = {
    "check-mark": "a check mark",
    "flame": "a single flame",
    "crossed-circle": "a prohibition sign: a circle with one diagonal line through it",
    "manure-fork": "a garden pitchfork with four tines standing upright next to a small rounded heap",
    "leaf": "a single leaf with a central vein and a short stem",
    "wood-log": "a cut wood log seen from the side with growth rings on its end, and two small wood chips beside it",
    "compost-thermometer": "a long probe compost thermometer with a round dial on top, pushed into a small mound",
}

COLOURS = {"deep": (0x22, 0x37, 0x1F), "cream": (0xF4, 0xF1, 0xEA), "green": (0x15, 0x68, 0x26)}


def to_icon(src, name):
    """White background to transparency (alpha from darkness), cropped to the strokes, saved per brand colour."""
    g = Image.open(src).convert("L")
    alpha = g.point(lambda v: 0 if v > 235 else min(255, int((235 - v) * 255 / 180)))
    box = alpha.point(lambda v: 255 if v > 40 else 0).getbbox()
    pad = 24
    box = (max(0, box[0] - pad), max(0, box[1] - pad), min(g.width, box[2] + pad), min(g.height, box[3] + pad))
    alpha = alpha.crop(box)
    for cname, rgb in COLOURS.items():
        im = Image.new("RGBA", alpha.size, rgb + (0,)); im.putalpha(alpha)
        im.save(ICONS / f"icon-{name}-{cname}.png")


def generate(name):
    ORIG.mkdir(parents=True, exist_ok=True)
    total = total_cost()                       # read the log before every generation
    if total + EST_PER_IMAGE > CAP:
        print(f"SKIPPED {name}: next generation would pass the ${CAP:.2f} cap (now ${total:.2f})")
        return None
    out = ORIG / f"icon-{name}.png"
    try:
        output = replicate.run(MODEL, input={"prompt": f"{ICONSET[name]}. {STYLE}", "aspect_ratio": "1:1",
                                             "resolution": "1 MP", "output_format": "png"})
        first = output[0] if isinstance(output, (list, tuple)) else output
        out.write_bytes(first.read())
        print(f"ok {name}  total now ${log_cost('icon-' + name, 1, True):.2f}")
    except Exception as e:  # noqa: BLE001
        log_cost("icon-" + name, 1, False)
        msg = str(e)
        if "401" in msg:
            sys.exit("Replicate returned 401: stopping.")
        print(f"FAILED {name}: {type(e).__name__}: {msg[:160]}")
        return None
    to_icon(out, name)
    return out


if __name__ == "__main__":
    import time
    for n in sys.argv[1:]:
        for attempt in (1, 2):                 # free account: 6 predictions a minute, burst of 1
            if generate(n): break
            time.sleep(30)
        time.sleep(12)
