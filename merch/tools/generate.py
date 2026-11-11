"""Generate organism candidates with recraft-ai/recraft-v3-svg on Replicate.
Usage: python3 generate.py OUTDIR key [key ...]   (keys from ORGANISMS)
Token is read from REPLICATE_API_TOKEN and never printed."""
import json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

PATTERN = ("scientific engraving of {desc}, Ernst Haeckel plate style, fine black line art "
           "with cross-hatching, isolated on plain white background, single specimen, centered, "
           "no text, no letters, no words, no border")
ORGANISMS = {
 "bacteria-rods": "three smooth rod-shaped soil bacteria, simple capsule-shaped cells with rounded ends lying side by side at slight angles, finely stippled interiors, no hairs, no flagella, no tails",
 "fungal-hyphae": "a few thin microscopic fungal hyphae, long narrow tubes with regular cross walls (septa), branching at acute angles, sparse and open, microscope view, no mushrooms, not a tree",
 "heliozoan": "a soil protozoan, the sun animalcule Actinophrys, a round cell with a foamy vacuolated body and many fine straight radiating axopodia like a sunburst",
 "flagellate": "one single soil flagellate Bodo, a small oval bean-shaped cell with exactly two long whip-like flagella, one pointing forward and one trailing behind",
 "amoeba": "a naked soil amoeba, a single irregular cell with several blunt lobe-shaped pseudopodia, granular cytoplasm, one round nucleus and a contractile vacuole",
 "ciliate": "a soil ciliate Colpoda, one kidney-shaped single cell outlined by a dense fringe of many short even cilia, a notch-like oral groove on the concave side, small round food vacuoles inside",
 "nematode": "a bacterial-feeding soil nematode (Rhabditida), a smooth slender transparent unsegmented roundworm in a loose S curve, tapered pointed tail, blunt rounded head with no eyes, visible muscular pharynx with a round bulb behind the head, no stylet, no legs, not a snake",
 "oribatid-mite": "an oribatid soil mite, a tiny round glossy dome-shaped body like a miniature beetle, exactly eight short jointed legs, four on each side, two small sensory hairs on the front, top view",
 "mycorrhiza": "a short segment of a plant root seen from the side, thin fungal hyphae wrapping around it and entering it, small branched arbuscules visible inside the root cells, one large round fungal spore attached to a hypha outside",
 "actinobacteria": "soil actinobacteria Streptomyces, very thin branching filamentous hyphae with coiled spiral chains of tiny round spores at the tips",
 "earthworm": "a single earthworm, side view, gentle S curve, fine ring segments along the whole body, one thicker smooth saddle band about a third of the way from the head, no legs, no eyes",
 "root-tip": "a single slender plant root tip hanging vertically, rounded root cap at the bottom, a fine fuzz of root hairs a short distance above the tip, no side roots, no soil, no stem",
}

STYLE = os.environ.get("RECRAFT_STYLE", "any")

def run(desc, out):
    tok = os.environ["REPLICATE_API_TOKEN"]
    body = json.dumps({"input": {"prompt": PATTERN.format(desc=desc), "style": STYLE, "size": "1024x1024"}}).encode()
    req = urllib.request.Request("https://api.replicate.com/v1/models/recraft-ai/recraft-v3-svg/predictions",
        data=body, headers={"Authorization": f"Bearer {tok}", "Content-Type": "application/json", "Prefer": "wait=60"})
    for attempt in range(8):
        try:
            p = json.load(urllib.request.urlopen(req, timeout=120)); break
        except urllib.error.HTTPError as e:
            if attempt == 7 or e.code not in (429, 500, 502, 503): return f"ERR {out}: {e.code} {e.read()[:200]}"
            time.sleep(12 * (attempt + 1))
        except Exception as e:
            if attempt == 7: return f"ERR {out}: {e}"
            time.sleep(12)
    while p["status"] not in ("succeeded", "failed", "canceled"):
        time.sleep(2)
        r = urllib.request.Request(p["urls"]["get"], headers={"Authorization": f"Bearer {tok}"})
        p = json.load(urllib.request.urlopen(r))
    if p["status"] != "succeeded": return f"FAIL {out}: {p.get('error')}"
    url = p["output"] if isinstance(p["output"], str) else p["output"][0]
    urllib.request.urlretrieve(url, out + '.part'); os.rename(out + '.part', out)
    return f"ok {out}"

if __name__ == "__main__":
    outdir, keys = sys.argv[1], sys.argv[2:]
    n = int(os.environ.get("N", 4))
    os.makedirs(outdir, exist_ok=True)
    jobs = [(ORGANISMS[k], f"{outdir}/{k}-c{i}.svg") for k in keys for i in range(1, n + 1)]
    # sequential: low-credit Replicate accounts allow a burst of 1, 6 per minute
    for desc, out in jobs:
        if os.path.exists(out): continue
        print(run(desc, out), flush=True)
        time.sleep(11)
    old = json.load(open(f"{outdir}/prompts.json")) if os.path.exists(f"{outdir}/prompts.json") else {}
    json.dump({**old, **{k: PATTERN.format(desc=ORGANISMS[k]) for k in keys}}, open(f"{outdir}/prompts.json", "w"), indent=1)
