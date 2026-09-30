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

def sticker(rel, width, outline=14):
    """Transparent cut-out with a white sticker border and soft shadow. Returns a temp PNG path."""
    from PIL import ImageFilter, ImageChops
    im = Image.open(os.path.join(ROOT, rel)).convert("RGBA")
    r = width / im.width; im = im.resize((width, round(im.height*r)), Image.LANCZOS)
    pad = outline*3; W2, H2 = im.width+pad*2, im.height+pad*2
    base = Image.new("RGBA", (W2, H2), (0, 0, 0, 0)); base.paste(im, (pad, pad), im)
    a = base.split()[3]
    border = a.filter(ImageFilter.MaxFilter(outline*2+1)).filter(ImageFilter.GaussianBlur(1.5))
    shadow = ImageChops.offset(border, 6, 8).filter(ImageFilter.GaussianBlur(8)).point(lambda v: int(v*0.35))
    out = Image.new("RGBA", (W2, H2), (0, 0, 0, 0))
    out.paste(Image.new("RGBA", (W2, H2), (60, 50, 40, 255)), (0, 0), shadow)
    out.paste(Image.new("RGBA", (W2, H2), (255, 255, 255, 255)), (0, 0), border)
    out.paste(im, (pad, pad), im)
    p = os.path.join(_tmp, f"st{abs(hash((rel,width)))}.png"); out.save(p); return p
