"""Render a PPTX to renders/october/<name>/slide-NN.png and a contact sheet renders/october/<name>-contact.png.
python3 tools/render_deck.py templates/posts/october/<file>.pptx   (needs LibreOffice Impress and PyMuPDF)"""
import os, subprocess, sys, tempfile
import fitz
from PIL import Image

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "renders", "october")


def render(pptx):
    name = os.path.splitext(os.path.basename(pptx))[0]
    tmp = tempfile.mkdtemp()
    subprocess.run(["soffice", "--headless", "--convert-to", "pdf", "--outdir", tmp, os.path.abspath(pptx)],
                   check=True, capture_output=True)
    doc = fitz.open(os.path.join(tmp, name + ".pdf"))
    d = os.path.join(OUT, name); os.makedirs(d, exist_ok=True)
    for f in os.listdir(d): os.remove(os.path.join(d, f))
    ims = []
    for i, page in enumerate(doc, 1):
        zoom = 1080 / page.rect.width if page.rect.width < page.rect.height * 1.5 else 1200 / page.rect.width
        p = os.path.join(d, f"slide-{i:02d}.png"); page.get_pixmap(matrix=fitz.Matrix(zoom * 0.75 * 96 / 72 / 0.75 * 0.75, zoom * 0.75 * 96 / 72 / 0.75 * 0.75)).save(p)
        ims.append(Image.open(p).convert("RGB"))
    tw = 360; th = round(tw * ims[0].height / ims[0].width); cols = min(len(ims), 6); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (tw + 12) + 12, rows * (th + 12) + 12), (70, 70, 70))
    for i, im in enumerate(ims):
        sheet.paste(im.resize((tw, th)), (12 + (i % cols) * (tw + 12), 12 + (i // cols) * (th + 12)))
    sheet.save(os.path.join(OUT, name + "-contact.png"))
    print(name, len(ims), "slides", ims[0].size)


if __name__ == "__main__":
    for p in sys.argv[1:]: render(p)
