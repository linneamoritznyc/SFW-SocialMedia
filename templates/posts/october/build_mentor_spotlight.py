"""Mentor spotlight carousel, Instagram, 1080 x 1350, up to 6 slides. Reusable: give a name, a role and photos.

Every slide is a full-bleed photo, no text on the photos. Slide 1 only: Deep Green #22371F band across the bottom,
220 px tall, 90% opacity, the name in Montserrat Bold 52 pt Cream #F4F1EA and the role under it in Source Sans 3 30 pt
Light Green #59A66C, left aligned, 64 px side padding.
Slide order: close portrait first, then teaching or working, then their land or a workshop.

Photos are cropped to 4:5 around a focus point (fx, fy, 0 to 1; put it on the face or the hands) and only ever scaled
down, never stretched. A photo whose 4:5 crop would be under 1080 px wide is flagged and left out.

Add a mentor to MENTORS below, then:
  python3 templates/posts/october/build_mentor_spotlight.py carla --slide1     slide 1 only, to check
  python3 templates/posts/october/build_mentor_spotlight.py carla              all slides
Saves templates/posts/october/[DD-MM-YYYY-ddd-]ig-mentor-spotlight-<slug>.pptx, then renders it to
renders/october/ with tools/render_deck.py, as for the World Teachers' Day carousel. The date prefix is added once
the mentor has a "date".
"""
import datetime, os, subprocess, sys
from PIL import Image, ImageOps
from pptx.util import Emu
from lib import Deck, rect, text, ROOT, PX, PHBG, DEEP, CREAM, LIGHT, HEAD, BODY

try:
    from pillow_heif import register_heif_opener; register_heif_opener()   # iPhone .heic files
except ImportError:
    pass

W, H, BAND, PAD, MIN_W = 1080, 1350, 220, 64, 1080
NAME_PT, ROLE_PT = 52, 30
ORDER = ("portrait", "teaching", "land")       # land = their land or a workshop
FOCUS = {"portrait": (0.5, 0.3), "teaching": (0.5, 0.5), "land": (0.5, 0.5)}
HERE = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(ROOT, "renders", ".tmp")
MT = "assets/mentors-teachers-day/"

# slug: name and role exactly as on the World Teachers' Day carousel (build_teachers_day_v3.py STAFF, "Dr." as in
# build_teachers_day_final.py); photos as (kind, path from repo root, focus or None); date None until scheduled.
MENTORS = {
    "carla-portugal": dict(
        name="Dr. Carla Ribeiro Machado e Portugal", role="Mentor & Science Lead", date=None,
        photos=[("portrait", MT + "carla-portugal.jpg", (0.5, 0.25))]),
}


def check(path, focus):
    """Return (4:5 crop box at full resolution, None) or (None, reason it is left out)."""
    try:
        im = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, path)))
    except Exception as e:
        return None, f"cannot open ({e})"
    w, h = im.size
    cw = min(w, h * 4 / 5); ch = cw * 5 / 4
    if w < MIN_W: return None, f"{w} x {h}, under {MIN_W} px wide"
    if cw < MIN_W: return None, f"{w} x {h}, its 4:5 crop is only {int(cw)} px wide"
    fx, fy = focus
    x = min(max(fx * w - cw / 2, 0), w - cw); y = min(max(fy * h - ch / 2, 0), h - ch)
    return (round(x), round(y), round(x + cw), round(y + ch)), None


def cropped(path, box):
    os.makedirs(TMP, exist_ok=True)
    out = os.path.join(TMP, "spotlight-" + os.path.splitext(os.path.basename(path))[0].replace(" ", "-") + ".jpg")
    im = ImageOps.exif_transpose(Image.open(os.path.join(ROOT, path))).convert("RGB")
    im.crop(box).resize((W, H), Image.LANCZOS).save(out, quality=92)    # same 4:5 shape, scaled down only
    return out


def bleed(s, src):
    s.shapes.add_picture(src, 0, 0, Emu(W * PX), Emu(H * PX))


def placeholder(s, label):
    rect(s, 0, 0, W, H, PHBG)
    text(s, 120, 380, W - 240, 200, f"[PHOTO: {label}]", 40, DEEP, HEAD, True, align="c", anchor="m")


def band(s, name, role):
    rect(s, 0, H - BAND, W, BAND, DEEP, alpha=90)
    text(s, PAD, H - BAND, W - 2 * PAD, BAND, name + "\n", NAME_PT, CREAM, HEAD, True, anchor="m", spacing=1.0)
    _role(s.shapes[-1].text_frame, role)


def _role(tf, role):
    """Role as a second paragraph in the name box, so name and role stay together and centred in the band."""
    from pptx.util import Pt
    from lib import rgb
    p = tf.paragraphs[-1]; p.space_before = Pt(6)
    for r in p.runs: p._p.remove(r._r)          # the empty run text() left for the second line
    r = p.add_run(); r.text = role; f = r.font
    f.size = Pt(ROLE_PT); f.name = BODY; f.bold = False; f.color.rgb = rgb(LIGHT)


def build(slug, slide1_only=False):
    m = MENTORS[slug]
    used, flagged = [], []
    for kind, path, focus in m["photos"]:
        box, why = check(path, focus or FOCUS[kind])
        (flagged.append((path, why)) if why else used.append((kind, path, box)))
    used.sort(key=lambda p: ORDER.index(p[0]))
    used = used[:6]
    has_portrait = bool(used) and used[0][0] == "portrait"

    d = m["date"] and datetime.date.fromisoformat(m["date"])
    name = (f"{d:%d-%m-%Y}-{d:%a}".lower() + "-" if d else "") + f"ig-mentor-spotlight-{slug}"
    deck = Deck(name=name)
    note = f"Mentor spotlight: {m['name']}, {m['role']}. "

    s = deck.slide(None, note + "Slide 1: close portrait, name band.", counter=False)
    if has_portrait: bleed(s, cropped(used[0][1], used[0][2]))
    else: placeholder(s, f"close portrait of {m['name']}, at least 1080 px wide")
    band(s, m["name"], m["role"])
    rest = used[1:] if has_portrait else used
    if not slide1_only:
        for kind, path, box in rest:
            s = deck.slide(None, note + f"{kind.capitalize()} photo: {path}. No text on the photo.", counter=False)
            bleed(s, cropped(path, box))
    if slide1_only: name += "-slide-1"
    out = os.path.join(HERE, name + ".pptx")
    deck.finish(out, counters=False)
    subprocess.run([sys.executable, os.path.join(ROOT, "tools", "render_deck.py"), out], check=True)

    print(f"\n{m['name']}: {len(used)} usable photo(s), {'slide 1 only' if slide1_only else f'{len(deck.prs.slides)} slides'}")
    for path, why in flagged: print(f"  FLAGGED, left out: {path}: {why}")
    if not has_portrait: print("  No usable close portrait: slide 1 shows a PHOTO placeholder.")
    if len(used) < 3: print(f"  Fewer than 3 usable photos ({len(used)}).")
    return out


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    for slug in args or MENTORS:
        build(slug, "--slide1" in sys.argv)
