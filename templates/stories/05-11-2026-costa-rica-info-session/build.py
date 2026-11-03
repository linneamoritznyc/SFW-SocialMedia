"""Instagram Story, Thu 5 Nov 2026: Costa Rica info session reminder. 1080 x 1920.
python3 templates/stories/05-11-2026-costa-rica-info-session/build.py -> previews/story.png
Photos are full-size originals from Linnea's Drive (Costa Rica workshop folders)."""
import os, subprocess
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
P = lambda f: os.path.join(HERE, "photos", f)
def crop(src, box, out):  # box as fractions (l, t, r, b) of the original
    im = ImageOps.exif_transpose(Image.open(P(src))); w, h = im.size
    im.crop((int(box[0]*w), int(box[1]*h), int(box[2]*w), int(box[3]*h))).save(P(out), quality=94)
crop("PXL_20251022_170527960.jpg", (0.26, 0.0, 0.94, 1.0), "_hero.jpg")
crop("PXL_20240716_224324982_HandsInSoil.jpg", (0.10, 0.18, 0.95, 0.95), "_hands.jpg")
crop("PXL_20251024_162252612.jpg", (0.12, 0.33, 0.80, 0.72), "_shed.jpg")
font = lambda f: "file://" + os.path.join(ROOT, "assets", "font", f)
html = f"""<!doctype html><meta charset=utf-8><style>
@font-face{{font-family:M;font-weight:700;src:url('{font("montserrat-latin-variable.woff2")}')}}
@font-face{{font-family:S;src:url('{font("source-sans-3-latin-400-normal.woff2")}')}}
*{{margin:0;padding:0}} .s{{position:relative;width:1080px;height:1920px;background:#F4F1EA;overflow:hidden}}
img{{position:absolute;object-fit:cover;display:block}}
h1{{position:absolute;left:72px;top:1262px;font:700 92px/100px M;color:#156826;letter-spacing:-0.01em}}
p{{position:absolute;left:74px;top:1480px;font:400 46px/58px S;color:#333130}}
</style><div class=s>
<img src="file://{P('_hero.jpg')}" style="left:0;top:0;width:1080px;height:1180px;object-position:50% 40%">
<img src="file://{P('_hands.jpg')}" style="left:680px;top:1060px;width:328px;height:400px">
<img src="file://{P('_shed.jpg')}" style="left:680px;top:1476px;width:328px;height:300px">
<h1>Costa Rica<br>info session</h1><p>Tomorrow, 12pm Pacific<br>on Zoom. Free.</p></div>"""
open(os.path.join(HERE, "previews", "_s.html"), "w").write(html)
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.locator('.s').screenshot({path:process.argv[3]});await b.close();})();"""
jp = os.path.join(HERE, "previews", "_r.js"); open(jp, "w").write(js)
subprocess.run(["node", jp, os.path.join(HERE, "previews", "_s.html"), os.path.join(HERE, "previews", "story.png")], check=True)
for f in ("_r.js", "_s.html"): os.remove(os.path.join(HERE, "previews", f))
