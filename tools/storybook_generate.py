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
    "scene-sugar-rain": "an underground street inside the soil with round soil-crumb houses, and pale pink, see-through "
                        "sugar drops gently dripping from the soil ceiling like soft rain; no characters",
    "scene-worm-room": "a cosy living room inside the soil: a small armchair, a round rug, a teapot and teacups on a "
                       "little table, a lamp made from a glowing seed, round soil walls; no characters",
    "scene-rose-dinner": "inside a small cosy kitchen in the evening: a wooden table with a bowl of soup, a window "
                         "showing the dark rainy garden outside; a six-year-old girl in a muddy dress with messy brown "
                         "hair sits at the table looking out of the window, wondering; simple cut-paper face with dot eyes",
    "scene-flowers": "a close-up of a few garden flowers and leaves just after rain, raindrops on the petals, "
                     "soft dark soil below, calm and quiet, lots of empty sky above; no people",
    "scene-lollipop-soil": "a close-up of soft dark wet garden soil after rain, with one small red strawberry "
                           "lollipop on a white stick lying half sunk into the soil, a few small leaves; calm, lots of "
                           "empty space; no people",
    "scene-sugar-drop": "a quiet tunnel street inside the soil with a few round soil-crumb houses, and one single small "
                        "pale pink see-through sugar drop hanging from the soil ceiling like a dewdrop, catching the "
                        "soft brown glow; calm, lots of empty space; no characters",
    "scene-barry-house": "close-up of one round soil-crumb house inside the soil at night, a tiny round door and a "
                         "small lit window, a little path in front; calm and cosy, lots of empty space; no characters",
    "scene-root-road": "a long pale tree root running sideways through dark soil like a road, a few soil crumbs and "
                       "small stones around it, soft brown glow; calm, lots of empty space; no characters",
    "scene-stick-street": "a quiet underground tunnel street inside the soil with round soil-crumb houses; a long plain "
                          "white plastic stick (a lollipop stick with no candy) has come down through the soil ceiling "
                          "and stands stuck upright in the middle of the street, a few crumbs drifting down; calm, soft "
                          "brown glow; no characters",
    "scene-garden-morning": "the same small back garden on a fresh sunny morning after rain, a damp vegetable bed of "
                            "dark soil with flowers, and one thin white plastic stick poking up out of the soil; calm, "
                            "lots of empty sky; no people",
    "scene-apple-core": "a close-up of soft dark garden soil with one apple core lying half planted in it, a few "
                        "small leaves, evening light; calm, lots of empty space; no people",
    "scene-town-night": "the underground town inside the soil late at night, cross-section, tunnel streets and round "
                        "soil-crumb houses with only a few tiny lit windows, very dark and calm, pale roots from the "
                        "ceiling; sleepy and peaceful; no characters",
    "scene-rose-bed": "a small cosy bedroom at night: a six-year-old girl with messy brown hair asleep in a little bed "
                      "under a patchwork quilt, a window showing the dark garden and a few stars; very calm; simple "
                      "cut-paper face with closed eyes",
    "scene-apple-below": "underground, seen from below: an apple core resting on the soil above, and pale roots and "
                         "fine fungal threads slowly reaching up towards it through dark soil, soft brown glow; calm; "
                         "no characters",
    "scene-bakery": "an underground bakery inside the soil: pale tree roots coming down from the ceiling, and small "
                    "cupcakes and cookies hanging from the root tips and set out on little shelves, warm brown glow; "
                    "no characters",
}
CHARACTERS = {  # 1:1, cut out
    "rose-lollipop": "a six-year-old girl named Rose in yellow rain boots and a muddy dress, messy brown hair, "
                     "holding a red strawberry lollipop, smiling; simple cut-paper face with small dot eyes",
    "rose-running": "the same six-year-old girl in yellow rain boots and a muddy dress, messy brown hair, running "
                    "away happily, seen from the side; simple cut-paper face with small dot eyes",
    # Grandma Worm was removed from the cast (Linnea, 4 Oct 2026); kept here only so the old file can be traced.
    "grandma-worm": "a very large old grandmother earthworm with clear segments and a saddle band, small round "
                    "spectacles and a knitted shawl, sleepy and kind, two googly eyes",
    "pip-flagellate": "a small nervous oval flagellate protozoan with two long whip tails, two googly eyes, cute",
    "ama-amoeba": "a soft shell-less amoeba, a translucent blob with rounded lobes, shy and pretty, two googly eyes",
    "lollipop": "a red strawberry lollipop on a white plastic stick",
    "rose-pulling-stick": "the same six-year-old girl Rose in yellow rain boots and a muddy dress, messy brown hair, "
                          "crouching and pulling a thin white plastic stick out of the ground, curious; simple "
                          "cut-paper face with small dot eyes",
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
