"""SFW shop launch images: real Printful mockups placed into rainy farm scenes with an image-edit model.
Usage: python3 launch_scenes.py [product ...]   (reads REPLICATE_API_TOKEN from the environment, never prints it)
Out: merch/launch/<product>/<product>-<n>-4x5.jpg (2048x2560) and -hero.jpg (2880x1280), contact.jpg"""
import base64, concurrent.futures as cf, io, os, sys, time
import requests
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "source")
TOKEN = os.environ.get("REPLICATE_API_TOKEN") or sys.exit("REPLICATE_API_TOKEN is missing")
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "Prefer": "wait=60"}

FILM = ("Shot on 35mm Kodak Portra 400 film, soft diffused light under a grey overcast sky, deep greens, damp textures, "
        "gentle film grain, slightly muted colour, handmade small-batch lived-in feel. No people, no faces, no hands. "
        "Do not add any text, letters or logos. Keep the product exactly as in the input image: same colour, same print, "
        "same placement and size of the print, do not redraw or change the artwork on it.")
FENCE = ("Hang this exact garment on a simple wooden hanger on a silver weathered cedar fence with moss on the posts, "
         "wet meadow grass below, soft overcast sky just after rain.")
LINE = ("Peg this exact item to a cotton clothesline strung between two old fence posts at the edge of a field, misty "
        "fir-covered hills behind, fabric slightly damp and moving gently in the wind.")
LOG = "Lay this exact cap on a moss-covered log on the forest floor, ferns around it, small water droplets on the moss."
PORCH = "Place this exact mug on a wet wooden porch rail, a little steam rising from it, a rain-dark field behind."
GROUP = ("Hang all of these exact products along one mossy wooden fence like a small farm stand: the tees and hoodie on "
         "hangers, the tote hung from a post, the cap on a post, the mug on the top rail. Low clouds over fir trees behind.")

PRODUCTS = {"logo-tee-green": FENCE, "logo-hoodie-black": FENCE, "mycelium-tee": LINE, "mycelium-tote": LINE,
            "logo-cap-oyster": LOG, "logo-mug": PORCH}


def data_uri(path, side=1400):
    im = Image.open(path).convert("RGB"); im.thumbnail((side, side))
    b = io.BytesIO(); im.save(b, "JPEG", quality=92)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def run(model, inp):
    for _ in range(6):
        r = requests.post(f"https://api.replicate.com/v1/models/{model}/predictions", headers=H, json={"input": inp}, timeout=180)
        if r.status_code == 429: time.sleep(20); continue
        r.raise_for_status(); p = r.json(); break
    while p["status"] in ("starting", "processing"):
        time.sleep(3); p = requests.get(p["urls"]["get"], headers=H, timeout=60).json()
    if p["status"] != "succeeded": raise RuntimeError(f"{model}: {p['status']} {p.get('error')}")
    out = p["output"]; out = out[0] if isinstance(out, list) else out
    return Image.open(io.BytesIO(requests.get(out, timeout=180).content)).convert("RGB")


def edit(images, prompt, aspect, seed):
    if len(images) == 1:
        return run("black-forest-labs/flux-kontext-pro", {"prompt": prompt, "input_image": images[0], "aspect_ratio": aspect,
                                                          "output_format": "png", "safety_tolerance": 2, "seed": seed})
    return run("google/nano-banana", {"prompt": prompt, "image_input": images, "aspect_ratio": aspect, "output_format": "png"})


def finish(im, size):
    return ImageOps.fit(im, size, Image.LANCZOS)          # upscale/crop to the delivery size


def job(name, prompt, images, k):
    out = os.path.join(HERE, name); os.makedirs(out, exist_ok=True)
    full = f"{prompt} {FILM}"
    finish(edit(images, full, "4:5", 10 + k), (2048, 2560)).save(os.path.join(out, f"{name}-{k + 1}-4x5.jpg"), quality=93)
    finish(edit(images, full, "21:9", 20 + k), (2880, 1280)).save(os.path.join(out, f"{name}-{k + 1}-hero.jpg"), quality=93)
    return name, k


def contact():
    rows = []
    for name in list(PRODUCTS) + ["group"]:
        d = os.path.join(HERE, name)
        fs = sorted(f for f in os.listdir(d) if f.endswith("-4x5.jpg")) if os.path.isdir(d) else []
        if fs: rows.append([Image.open(os.path.join(d, f)).resize((320, 400)) for f in fs])
    if not rows: return
    s = Image.new("RGB", (4 * 330 + 10, len(rows) * 410 + 10), "white")
    for r, ims in enumerate(rows):
        for c, im in enumerate(ims): s.paste(im, (10 + c * 330, 10 + r * 410))
    s.save(os.path.join(HERE, "contact.jpg"), quality=90)


def main():
    want = sys.argv[1:] or list(PRODUCTS) + ["group"]
    jobs = []
    for name in want:
        if name == "group":
            imgs = [data_uri(os.path.join(SRC, f"{p}.jpg"), 900) for p in PRODUCTS]; prompt = GROUP
        else:
            imgs = [data_uri(os.path.join(SRC, f"{name}.jpg"))]; prompt = PRODUCTS[name]
        jobs += [(name, prompt, imgs, k) for k in range(4)]
    with cf.ThreadPoolExecutor(4) as ex:
        for f in cf.as_completed([ex.submit(job, *j) for j in jobs]):
            try: print("ok", f.result())
            except Exception as e: print("fail", str(e)[:200])
    contact()


if __name__ == "__main__":
    main()
