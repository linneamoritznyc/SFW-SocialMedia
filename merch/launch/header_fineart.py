"""Shop header 2880x1280 in the fine-art film look: Portra 800 LoRA landscape (capture language, no quality words),
real white SFW logo set in afterwards. Variants: landscape only, and the clean cap banner."""
import os, sys
import numpy as np
from PIL import Image, ImageOps
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from launch_fineart import post, wait, PORTRA

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "fineart", "header")
W, H = 2880, 1280
LOGO = "/home/user/sfw-merch-print-files/creative-code/logos/SFW-logo-flower-white-3000.png"
CAPTURE = ("Photographed on a Mamiya RZ67 with a 50mm lens at f/8, Kodak Portra 400 120 film, scanned on a Noritsu. "
           "Soft overcast light after rain, no fill. Fine organic grain, lifted shadows, restrained colour. Quiet, lots of air.")
SCENES = {
    "fence": "TOK style, a long silver weathered cedar fence with moss on the posts running across a wet meadow, fir-covered hills behind in low mist and cloud.",
    "meadow": "TOK style, a wide wet meadow of tall grass at the edge of a fir forest, mist hanging between the trees, a low grey sky.",
    "hills": "TOK style, layers of fir-covered hills fading into mist and low cloud, a damp field and an old mossy fence post in the foreground.",
}


def land(prompt, seed):
    return wait(post("https://api.replicate.com/v1/predictions", {"version": PORTRA, "input": {
        "prompt": f"{prompt} {CAPTURE}", "aspect_ratio": "21:9", "megapixels": "1", "lora_scale": 1.0,
        "num_inference_steps": 32, "guidance_scale": 3, "output_format": "png", "seed": seed}}))


def with_logo(im, size=260, margin=80):
    can = ImageOps.fit(im.convert("RGB"), (W, H), Image.LANCZOS).convert("RGBA")
    lg = Image.open(LOGO).convert("RGBA"); lg = lg.crop(lg.getbbox()); lg.thumbnail((size, size), Image.LANCZOS)
    a = np.asarray(lg).copy(); a[..., 3] = (a[..., 3] * .92).astype(np.uint8); lg = Image.fromarray(a)
    can.alpha_composite(lg, (W - lg.width - margin, H - lg.height - margin))
    return can.convert("RGB")


def main():
    os.makedirs(OUT, exist_ok=True); ims = []
    for name, p in SCENES.items():
        for seed in (1, 2):
            raw = os.path.join(OUT, f"raw-{name}-{seed}.png")
            if not os.path.exists(raw): land(p, seed).save(raw)
            im = with_logo(Image.open(raw)); im.save(os.path.join(OUT, f"header-{name}-{seed}.jpg"), quality=94); ims.append(im)
    cap = os.path.join(HERE, "fineart", "logo-cap-oyster", "logo-cap-oyster-1-hero-logo.jpg")
    if os.path.exists(cap):
        im = with_logo(Image.open(cap)); im.save(os.path.join(OUT, "header-cap.jpg"), quality=94); ims.append(im)
    s = Image.new("RGB", (2 * 1450 + 10, ((len(ims) + 1) // 2) * 650 + 10), "white")
    for i, im in enumerate(ims): s.paste(im.resize((1440, 640)), (10 + (i % 2) * 1450, 10 + (i // 2) * 650))
    s.save(os.path.join(OUT, "contact.jpg"), quality=90)


if __name__ == "__main__":
    main()
