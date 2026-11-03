"""Instagram Story, Thu 5 Nov 2026: Costa Rica info session reminder. 1080 x 1920.
python3 templates/stories/05-11-2026-costa-rica-info-session/build.py -> previews/story.png
Photos are full-size originals from Linnea's Drive (Costa Rica workshop folders)."""
import os, subprocess
from PIL import Image, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.abspath(os.path.join(HERE, "../../.."))
P = lambda f: os.path.join(HERE, "photos", f)
S = lambda f: os.path.join(HERE, "stickers", f)
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
<div style="position:absolute;left:712px;top:1100px;width:368px;height:716px;background:#156826"></div>
<img src="file://{P('_hands.jpg')}" style="left:680px;top:1060px;width:328px;height:400px">
<img src="file://{P('_shed.jpg')}" style="left:680px;top:1476px;width:328px;height:300px">
<img src="file://{S('violets.png')}" style="left:850px;top:-70px;width:270px;object-fit:contain">
<img src="file://{S('coneflower.png')}" style="left:880px;top:1560px;width:260px;object-fit:contain">
<h1>Costa Rica<br>info session</h1><p>Tomorrow, 12pm Pacific<br>on Zoom. Free.</p></div>"""
open(os.path.join(HERE, "previews", "_s.html"), "w").write(html)
js = """const {chromium}=require('playwright');(async()=>{const b=await chromium.launch();const p=await b.newPage({viewport:{width:1080,height:1920}});
await p.goto('file://'+process.argv[2]);await p.evaluate(()=>document.fonts.ready);await p.waitForTimeout(400);
await p.locator('.s').screenshot({path:process.argv[3]});await b.close();})();"""
jp = os.path.join(HERE, "previews", "_r.js"); open(jp, "w").write(js)
subprocess.run(["node", jp, os.path.join(HERE, "previews", "_s.html"), os.path.join(HERE, "previews", "story.png")], check=True)
for f in ("_r.js", "_s.html"): os.remove(os.path.join(HERE, "previews", f))


# ------------------------------------------------------------------ editable PPTX (same layout as the PNG)
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_ANCHOR, MSO_AUTO_SIZE

PX = 9525
def cover(src, w, h, fy=0.5):
    im = Image.open(P(src)).convert("RGB"); s = max(w / im.width, h / im.height)
    cw, ch = round(w / s), round(h / s); x = (im.width - cw) // 2; y = round((im.height - ch) * fy)
    out = P(src.replace(".jpg", "_frame.jpg")); im.crop((x, y, x + cw, y + ch)).save(out, quality=93); return out

prs = Presentation(); prs.slide_width = Emu(1080 * PX); prs.slide_height = Emu(1920 * PX)
sl = prs.slides.add_slide(prs.slide_layouts[6])
def box(name, x, y, w, h, color):
    s = sl.shapes.add_shape(MSO_SHAPE.RECTANGLE, Emu(x * PX), Emu(y * PX), Emu(w * PX), Emu(h * PX))
    s.fill.solid(); s.fill.fore_color.rgb = RGBColor.from_string(color); s.line.fill.background(); s.shadow.inherit = False; s.name = name
def pic(name, path, x, y, w, h):
    s = sl.shapes.add_picture(path, Emu(x * PX), Emu(y * PX), Emu(w * PX), Emu(h * PX)); s.name = name
def text(name, x, y, w, h, lines, font, size, lh, bold, color):
    s = sl.shapes.add_textbox(Emu(x * PX), Emu(y * PX), Emu(w * PX), Emu(h * PX)); s.name = name
    tf = s.text_frame; tf.word_wrap = False; tf.auto_size = MSO_AUTO_SIZE.NONE; tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    for i, t in enumerate(lines):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph(); para.line_spacing = Pt(lh * 0.75)
        r = para.add_run(); r.text = t; f = r.font
        f.name = font; f.size = Pt(size * 0.75); f.bold = bold; f.italic = False; f.color.rgb = RGBColor.from_string(color)

def sticker(name, f, x, y, w):
    im = Image.open(S(f)); pic(name, S(f), x, y, w, round(w * im.height / im.width))

box("Background", 0, 0, 1080, 1920, "F4F1EA")
pic("Hero photo (garden class, Oct 2025)", cover("_hero.jpg", 1080, 1180, 0.4), 0, 0, 1080, 1180)
box("Green block", 712, 1100, 368, 716, "156826")
pic("Photo: hands in compost (Jul 2024)", cover("_hands.jpg", 328, 400), 680, 1060, 328, 400)
pic("Photo: class in the shed (Oct 2025)", cover("_shed.jpg", 328, 300), 680, 1476, 328, 300)
sticker("Flower: violets", "violets.png", 850, -70, 270)
sticker("Flower: coneflower", "coneflower.png", 880, 1560, 260)
text("Headline", 72, 1262, 600, 200, ["Costa Rica", "info session"], "Montserrat", 92, 100, True, "156826")
text("Details", 74, 1480, 560, 116, ["Tomorrow, 12pm Pacific", "on Zoom. Free."], "Source Sans 3", 46, 58, False, "333130")
sl.notes_slide.notes_text_frame.text = ("Thu 5 Nov 2026 Instagram Story. Add the link sticker in Instagram under the details: "
    "https://www.addevent.com/event/r4wt0g3yjd4h. Keep the top 250 px and bottom 250 px free of text (Instagram UI).")
out = os.path.join(HERE, "..", "05-11-2026-costa-rica-info-session-story.pptx")
prs.save(out); print("wrote", out)
import glob
for f in glob.glob(P("_*.jpg")): os.remove(f)
