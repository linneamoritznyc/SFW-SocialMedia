"""Fine-art launch photos. Step 1: google/nano-banana places the real Printful mockup in the scene, described as a
medium-format film capture. Step 2: a light img2img pass through shapestudio/portra-800-flux ("TOK style") at low
strength so the product stays as made. Usage: python3 launch_fineart.py [product ...]
Out: merch/launch/fineart/<product>/<product>-<n>-4x5.jpg (2048x2560), -hero.jpg (2880x1280), contact sheets."""
import base64, concurrent.futures as cf, io, os, sys, time
import requests
from PIL import Image, ImageOps

HERE = os.path.dirname(os.path.abspath(__file__))
SRC, OUT = os.path.join(HERE, "source"), os.path.join(HERE, "fineart")
TOKEN = os.environ.get("REPLICATE_API_TOKEN") or sys.exit("REPLICATE_API_TOKEN is missing")
H = {"Authorization": f"Bearer {TOKEN}", "Content-Type": "application/json", "Prefer": "wait=60"}
PORTRA = "3d616c81c96b5578e485988d51f260c4159b8ce7822cf13fa0af63a7e5c833c2"

CAPTURE = ("Photographed on a Mamiya RZ67 with a 110mm lens at f/4, Kodak Portra 400 120 film, scanned on a Noritsu. "
           "Soft overcast light after rain, from one direction, no fill. Gentle falloff behind the subject, fine organic "
           "grain, lifted shadows, restrained colour, faint halation on bright edges. Quiet still-life composition with "
           "lots of air around the object, slightly off-centre. Damp moss, cedar, ferns, mist in the distance. "
           "No people, no hands. Do not add any text. Keep the product exactly as in the reference image: same colour, "
           "same print or embroidery, same placement and size.")
SCENES = {
    "logo-tee-green": "This t-shirt hangs on a plain wooden hanger on a silver weathered cedar fence with moss on the posts, wet meadow grass below.",
    "logo-hoodie-black": "This zip hoodie hangs on a plain wooden hanger on a silver weathered cedar fence with moss on the posts, wet meadow grass below.",
    "mycelium-tee": "This t-shirt is pegged to a cotton clothesline between two old fence posts at the edge of a field, fir-covered hills in mist behind, the fabric slightly damp and lifting in the wind.",
    "mycelium-tote": "This tote bag is pegged to a cotton clothesline between two old fence posts at the edge of a field, fir-covered hills in mist behind, the fabric slightly damp and lifting in the wind.",
    "logo-cap-oyster": "This cap rests on a moss-covered log on the forest floor, ferns around it, small droplets on the moss. Close still-life framing: the cap fills about a third of the frame, front facing the camera so the logo reads clearly.",
    "logo-mug": "This mug stands on a wet wooden porch rail, a thin thread of steam rising, a rain-dark field behind.",
    "group": "All of these products hang along one mossy wooden fence like a small farm stand: shirts and hoodie on wooden hangers, the tote on a post, the cap on a post, the mug on the top rail. Low clouds over fir trees behind.",
}


def uri(im, side=1600):
    im = im.convert("RGB"); im.thumbnail((side, side)); b = io.BytesIO(); im.save(b, "JPEG", quality=93)
    return "data:image/jpeg;base64," + base64.b64encode(b.getvalue()).decode()


def wait(r):
    r.raise_for_status(); p = r.json()
    while p["status"] in ("starting", "processing"):
        time.sleep(3); p = requests.get(p["urls"]["get"], headers=H, timeout=60).json()
    if p["status"] != "succeeded": raise RuntimeError(f"{p['status']} {p.get('error')}")
    o = p["output"]; o = o[0] if isinstance(o, list) else o
    return Image.open(io.BytesIO(requests.get(o, timeout=180).content)).convert("RGB")


def post(url, body):
    for _ in range(8):
        r = requests.post(url, headers=H, json=body, timeout=180)
        if r.status_code != 429: return r
        time.sleep(20)
    return r


def place(images, scene, aspect):
    return wait(post("https://api.replicate.com/v1/models/google/nano-banana/predictions",
                     {"input": {"prompt": f"{scene} {CAPTURE}", "image_input": images, "aspect_ratio": aspect, "output_format": "png"}}))


def portra(im, scene, seed, strength=.14):
    return wait(post("https://api.replicate.com/v1/predictions", {"version": PORTRA, "input": {
        "prompt": f"TOK style, {scene} Kodak Portra film photograph, overcast, quiet.", "image": uri(im, 1400),
        "prompt_strength": strength, "lora_scale": .9, "num_inference_steps": 30, "guidance_scale": 3,
        "megapixels": "1", "output_format": "png", "seed": seed}}))


LOGO = "/home/user/sfw-merch-print-files/logos/SFW-logo-colour-transparent-3000px.png"
LOGO_NOTE = (" The logo on the product must be exactly the logo in the last reference image, in its full original colours "
             "(green, purple flowers and brown roots), sharp and correctly spelled SOIL FOOD WEB FOUNDATION, embroidered or printed.")


def logo_uri():
    lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); bg = Image.new("RGB", lg.size, "white")
    bg.paste(lg, (0, 0), lg); return uri(bg, 1200)


def job(name, k):
    out = os.path.join(OUT, name); os.makedirs(out, exist_ok=True)
    if name == "group":
        imgs = [uri(Image.open(os.path.join(SRC, f"{p}.jpg")), 900) for p in SCENES if p != "group"]
    else:
        imgs = [uri(Image.open(os.path.join(SRC, f"{name}.jpg")))]
    imgs = imgs + [logo_uri()]
    for aspect, size, tag in (("4:5", (2048, 2560), "4x5"), ("21:9", (2880, 1280), "hero")):
        a = place(imgs, SCENES[name] + LOGO_NOTE, aspect)
        a.save(os.path.join(out, f"{name}-{k + 1}-{tag}-step1.png"))
        b = portra(a, SCENES[name], 40 + k)
        ImageOps.fit(b, size, Image.LANCZOS).save(os.path.join(out, f"{name}-{k + 1}-{tag}.jpg"), quality=94)
    return name, k


def contact(name):
    d = os.path.join(OUT, name)
    a = [Image.open(os.path.join(d, f)).resize((480, 600)) for f in sorted(os.listdir(d)) if f.endswith("-4x5.jpg")]
    h = [Image.open(os.path.join(d, f)).resize((960, 427)) for f in sorted(os.listdir(d)) if f.endswith("-hero.jpg")]
    s = Image.new("RGB", (4 * 490 + 10, 620 + ((len(h) + 1) // 2) * 437 + 10), "white")
    for i, im in enumerate(a): s.paste(im, (10 + i * 490, 10))
    for i, im in enumerate(h): s.paste(im, (10 + (i % 2) * 980, 620 + (i // 2) * 437))
    s.save(os.path.join(OUT, f"contact-{name}.jpg"), quality=90)


def main():
    n_opt = int(os.environ.get("N", 4)); names = sys.argv[1:] or list(SCENES)
    with cf.ThreadPoolExecutor(4) as ex:
        for f in cf.as_completed([ex.submit(job, n, k) for n in names for k in range(n_opt)]):
            try: print("ok", f.result())
            except Exception as e: print("fail", str(e)[:200])
    for n in names:
        try: contact(n)
        except Exception as e: print("contact fail", n, e)


if __name__ == "__main__":
    main()
