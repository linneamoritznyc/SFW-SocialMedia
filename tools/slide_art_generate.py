"""One-off cut-paper art for a slide, same model, reference image and cost log as tools/collage_generate.py.

python3 tools/slide_art_generate.py <name> "<subject>" [aspect] [--photo]   -> assets/collage/originals/<name>.png and cutouts/<name>.png
"""
import sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from collage_generate import MODEL, REFERENCE, ORIG, total_cost, log_cost, cutout, STOP_AT, EST_PER_IMAGE  # noqa: E402
import replicate  # noqa: E402

STYLE = ("cut paper collage, kraft paper, graphite rubbing texture, colored pencil strokes, hand-cut uneven edges, "
         "overlapping paper layers, scanned artwork. Palette: soil brown #4C3634, leaf greens #31662F and #6AA46F, "
         "warm gold #D39C48, small violet flowers like #7A4FA0, on a plain flat cream paper background. Use the "
         "reference image only for its cut-paper technique and texture, not its subjects or colors. No text, no "
         "signature, no labels, no frame, no cast shadow.")

PHOTO = "--photo" in sys.argv          # realistic photo, no collage style and no reference image
args = [a for a in sys.argv[1:] if a != "--photo"]
name, subject = args[0], args[1]
aspect = args[2] if len(args) > 2 else "16:9"
if total_cost() + EST_PER_IMAGE > STOP_AT: sys.exit(f"Stopping: estimated total would pass ${STOP_AT:.2f}")
out = ORIG / f"{name}.png"
for attempt in (1, 2):
    try:
        if PHOTO:
            o = replicate.run(MODEL, input={"prompt": subject, "aspect_ratio": aspect, "resolution": "4 MP",
                                            "output_format": "png"})
        else:
            with open(REFERENCE, "rb") as ref:
                o = replicate.run(MODEL, input={"prompt": f"{subject}. {STYLE}", "input_images": [ref],
                                                "aspect_ratio": aspect, "resolution": "4 MP", "output_format": "png"})
        out.write_bytes((o[0] if isinstance(o, (list, tuple)) else o).read())
        log_cost(name, 1, True); cutout(out)
        print(f"done {out}  running est total ${total_cost():.2f}"); break
    except Exception as e:  # noqa: BLE001
        log_cost(name, 1, False)
        if "401" in str(e): sys.exit("Replicate returned 401: stopping.")
        print("FAILED", str(e)[:200]); time.sleep(30)
