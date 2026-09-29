"""Cover-crop a library photo to a box and return a temp JPEG path. Paths are relative to the repo root."""
import os, tempfile
from PIL import Image, ImageOps
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
_tmp = tempfile.mkdtemp(prefix="carousel-photos-")

def crop(rel, w, h, fx=0.5, fy=0.5, scale=1.0):
    im = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, rel))).convert("RGB")
    r = max(w/im.width, h/im.height); nw, nh = round(im.width*r), round(im.height*r)
    im = im.resize((nw, nh), Image.LANCZOS)
    x = round((nw-w)*fx); y = round((nh-h)*fy)
    out = os.path.join(_tmp, f"{abs(hash((rel,w,h,fx,fy)))}.jpg")
    im.crop((x, y, x+w, y+h)).save(out, quality=88); return out
