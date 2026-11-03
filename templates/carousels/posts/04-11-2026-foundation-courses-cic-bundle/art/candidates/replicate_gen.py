import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "gen")  # raw outputs, not committed
PREFIX = ("Loose hand-painted watercolor illustration on warm off-white watercolor paper, soft muted earthy colours, "
          "thin grey ink outlines, elegant natural-history science-book plate, calm and accurate, plain light paper background, "
          "no text, no labels, no letters, no people.")
MODEL = "black-forest-labs/flux-1.1-pro"
P = {
 # slide 1 cover, 4:5
 "s1-seedling-a": ("A single young seedling with two leaves standing on the right side of the page, shown as a tall cut-away of the ground: "
   "a shallow line of dark crumbly compost at the surface, and below it a long fine root system reaching down, threaded with delicate white fungal hyphae, "
   "tiny rod bacteria, a round protozoan and a slender nematode painted small among the roots. The left side and lower left of the page are left empty paper.", "4:5"),
 "s1-seedling-b": ("A botanical study of a young bean seedling lifted out of the ground with its whole root system, roots wrapped in fine white fungal threads "
   "and clinging crumbs of rich dark compost, placed in the upper right of the page. Lower left of the page is empty paper.", "4:5"),
 "s1-seedling-c": ("A cut-away block of rich dark compost seen from the side in the upper right of the page, a small green seedling growing from its top, "
   "fine white fungal hyphae and pale roots running through the compost, a few tiny soil organisms. Generous empty paper around it, especially lower left.", "4:5"),
 # slide 2, 4:5
 "s2-roots-a": ("A delicate study of fine plant roots spreading downward and outward from the top left of the page, wrapped in a net of very fine white fungal hyphae, "
   "small crumbs of dark compost clinging to them, a few nematodes and round protozoa drawn very small. The right half of the page stays empty paper.", "4:5"),
 "s2-compost-b": ("A natural-history plate of a handful-sized mound of rich dark living compost at the top left of the page, with fine white fungal threads, "
   "a curled earthworm and small seedling sprouting from it, painted with care. The right half and bottom of the page are empty paper.", "4:5"),
 "s2-organisms-c": ("A natural-history plate of soil life scattered across the top half of the page like a specimen sheet: fungal hyphae branching, "
   "a cluster of rod-shaped bacteria, a ciliate protozoan, a testate amoeba, a nematode, a springtail, all painted softly in muted earth tones. Bottom half empty paper.", "4:5"),
 # panorama across both slides
 "pano-a": ("A wide horizontal cut-away of living soil: a thin line of garden ground across the top with a few young seedlings, below it rich dark crumbly compost "
   "and long fine roots reaching down, threaded with delicate white fungal hyphae, with tiny bacteria, protozoa and nematodes among them. "
   "The soil fades lightly into the paper at the bottom.", "16:9"),
 "pano-b": ("A wide horizontal botanical plate: on the left a young seedling with its full root system, in the centre a mound of rich dark compost, "
   "on the right fine roots and white fungal hyphae spreading, small soil organisms between them, all on empty paper.", "16:9"),
 "pano-c": ("A wide horizontal cut-away of soil: young seedlings at the surface, a long network of white fungal hyphae connecting their roots through rich dark compost, "
   "small nematodes and protozoa painted delicately, generous empty paper above and below.", "16:9"),
 # flower accent
 "flower-a": ("A botanical study of one sprig of small purple wildflowers with green leaves, isolated, on plain white paper.", "1:1"),
 "flower-b": ("A botanical study of a single purple coneflower (echinacea) with its stem and two leaves, isolated, on plain white paper.", "1:1"),
 "flower-c": ("A botanical study of a small cluster of purple violas with leaves, isolated, on plain white paper.", "1:1"),
}
def run(name):
    path = os.path.join(OUT, f"{name}.png")
    if os.path.exists(path): return name, "cached"
    text, ratio = P[name]
    body = json.dumps({"input": {"prompt": f"{PREFIX} {text}", "aspect_ratio": ratio, "output_format": "png",
        "safety_tolerance": 2, "prompt_upsampling": False}}).encode()
    tok = os.environ["REPLICATE_API_TOKEN"]
    req = urllib.request.Request(f"https://api.replicate.com/v1/models/{MODEL}/predictions", data=body,
        headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json", "Prefer": "wait"})
    for a in range(12):
        try: pred = json.load(urllib.request.urlopen(req, timeout=120)); break
        except urllib.error.HTTPError as e:
            if e.code != 429 or a == 11: return name, f"http {e.code}"
            time.sleep(12)
    while pred.get("status") not in ("succeeded", "failed", "canceled"):
        time.sleep(2)
        pred = json.load(urllib.request.urlopen(urllib.request.Request(pred["urls"]["get"], headers={"Authorization": f"Bearer {tok}"}), timeout=60))
    if pred["status"] != "succeeded": return name, f"failed {pred.get('error')}"
    url = pred["output"] if isinstance(pred["output"], str) else pred["output"][0]
    urllib.request.urlretrieve(url, path); return name, "ok"
if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    names = sys.argv[1:] or list(P)
    with ThreadPoolExecutor(3) as ex:
        for r in ex.map(run, names): print(*r, flush=True)
