"""Picture-book art for "Under Rose's Garden", in the same cut-paper collage style (flux-2-pro + style-reference.png).

Scenes are full illustrations (4:3, background kept). Characters are single cut-outs (1:1, background removed with
rembg) so they look the same on every page and stay movable in the PowerPoint.
Shares generation-cost.txt and the cap with tools/collage_generate.py; the log is read before every generation.

python3 tools/storybook_generate.py scene-garden rose-lollipop ...
"""
import sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from collage_generate import MODEL, REFERENCE, ORIG, STYLE, total_cost, log_cost, cutout, STOP_AT  # noqa: E402
import replicate  # noqa: E402

SCENE_STYLE = STYLE.replace(
    "Single subject centered and alone on a plain flat cream paper background, ",
    "A full children's picture-book scene filling the whole frame, warm and calm, lots of texture, ")

SCENES = {   # 4:3, kept whole
    "scene-garden": "a small back garden just after rain: a damp vegetable bed of soft dark soil in front, puddles, "
                    "flowers and a few rows of plants, a small wooden house with a lit window in the background, "
                    "pale evening sky; no people",
    "scene-town": "an underground town inside the soil, seen as a cross-section: winding tunnels as streets, round soil "
                  "crumbs as little houses with tiny windows and doors, pale tree roots hanging down from the ceiling, "
                  "a soft warm brown glow; no characters",
    "scene-sugar-rain": "an underground street inside the soil with crumb houses, and sticky pink strawberry syrup "
                        "dripping down from the soil ceiling in shiny drops and puddles; no characters",
    "scene-worm-room": "a cosy living room inside the soil: a small armchair, a round rug, a teapot and teacups on a "
                       "little table, a lamp made from a glowing seed, round soil walls; no characters",
    "scene-rose-dinner": "inside a small cosy kitchen in the evening: a wooden table with a bowl of soup, a window "
                         "showing the dark rainy garden outside; a six-year-old girl in a muddy dress with messy brown "
                         "hair sits at the table looking out of the window, wondering; simple cut-paper face with dot eyes",
    "scene-bakery": "an underground bakery inside the soil: pale tree roots coming down from the ceiling, and small "
                    "cupcakes and cookies hanging from the root tips and set out on little shelves, warm brown glow; "
                    "no characters",
}
CHARACTERS = {  # 1:1, cut out
    "rose-lollipop": "a six-year-old girl named Rose in yellow rain boots and a muddy dress, messy brown hair, "
                     "holding a red strawberry lollipop, smiling; simple cut-paper face with small dot eyes",
    "rose-running": "the same six-year-old girl in yellow rain boots and a muddy dress, messy brown hair, running "
                    "away happily, seen from the side; simple cut-paper face with small dot eyes",
    "grandma-worm": "a very large old grandmother earthworm with clear segments and a saddle band, small round "
                    "spectacles and a knitted shawl, sleepy and kind, two googly eyes",
    "pip-flagellate": "a small nervous oval flagellate protozoan with two long whip tails, two googly eyes, cute",
    "ama-amoeba": "a soft shell-less amoeba, a translucent blob with rounded lobes, shy and pretty, two googly eyes",
    "lollipop": "a red strawberry lollipop on a white plastic stick",
    "ned-nematode": "Ned, a friendly night-watchman nematode, a smooth tapered worm wearing a tiny peaked cap and holding a small glowing lantern, two googly eyes",
}


def run(name):
    scene = name in SCENES
    if total_cost() + 0.09 > STOP_AT:
        print(f"SKIPPED {name}: would pass the cap (now ${total_cost():.2f})"); return None
    prompt = (SCENES[name] + ". " + SCENE_STYLE) if scene else (CHARACTERS[name] + ". " + STYLE)
    out = ORIG / f"book-{name}-1.png"
    for attempt in (1, 2):
        try:
            with open(REFERENCE, "rb") as ref:
                o = replicate.run(MODEL, input={"prompt": prompt, "input_images": [ref], "output_format": "png",
                                                "aspect_ratio": "4:3" if scene else "1:1", "resolution": "4 MP"})
            out.write_bytes((o[0] if isinstance(o, (list, tuple)) else o).read())
            log_cost("book-" + name, 1, True)
            if not scene: cutout(out)
            print(f"done {out.name}  running est total ${total_cost():.2f}")
            return out
        except Exception as e:  # noqa: BLE001
            log_cost("book-" + name, 1, False)
            if "401" in str(e): sys.exit("Replicate returned 401: stopping.")
            print(f"FAILED {name}: {str(e)[:160]}"); time.sleep(30)


if __name__ == "__main__":
    for n in sys.argv[1:] or list(SCENES) + list(CHARACTERS):
        run(n); time.sleep(12)
