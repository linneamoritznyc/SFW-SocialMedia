"""Teachers Day 'meet the teacher' card, 1080 x 1350. Run: python3 build_teacher_card.py
Card elements are laid out flat, then rotated about the card centre by TILT degrees."""
import math, os
from PIL import Image, ImageDraw
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

PX = 9525; W, H = 1080, 1350; TILT = -3
CREAM, PAPER, BROWN, GREEN, GOLD, GRAY, WHITE, INK = "F4F1EA", "FBF9F4", "4F3433", "156826", "C9A227", "A7B097", "FFFFFF", "333130"
NAME_RIBBON = BROWN   # swap to GOLD if preferred; white text on gold is low contrast
HAND, DISPLAY = "Caveat", "Montserrat"
CX, CY = W/2, H/2
here = os.path.dirname(os.path.abspath(__file__))

# textured background: warm cream, faint diagonal stripes, light grain
bg = Image.new("RGB", (W, H), "#EFE9DA"); d = ImageDraw.Draw(bg)
for k in range(-H, W+H, 26): d.line([(k, 0), (k+H, H)], fill="#E8E1CF", width=6)
bgp = os.path.join(here, "teacher-card-bg.png"); bg.save(bgp)

prs = Presentation(); prs.slide_width = Emu(W*PX); prs.slide_height = Emu(H*PX)
s = prs.slides.add_slide(prs.slide_layouts[6])
s.shapes.add_picture(bgp, 0, 0, Emu(W*PX), Emu(H*PX))
s.notes_slide.notes_text_frame.text = ("Teachers Day card. One per teacher. Photo: head and shoulders, smiling, written consent. "
    "Bio: years on the team, what they teach, life outside work; use only what the teacher approved.")

def tilt(sh, x, y, w, h):
    cx, cy = x+w/2-CX, y+h/2-CY; a = math.radians(TILT)
    nx = CX + cx*math.cos(a) - cy*math.sin(a); ny = CY + cx*math.sin(a) + cy*math.cos(a)
    sh.left, sh.top = Emu(int((nx-w/2)*PX)), Emu(int((ny-h/2)*PX)); sh.rotation = TILT + getattr(sh, "_r0", 0)

def shape(kind, x, y, w, h, fill, line=None, lw=0, rot0=0):
    r = s.shapes.add_shape(kind, Emu(x*PX), Emu(y*PX), Emu(w*PX), Emu(h*PX))
    r.fill.solid(); r.fill.fore_color.rgb = RGBColor.from_string(fill)
    if line: r.line.color.rgb = RGBColor.from_string(line); r.line.width = Emu(lw*PX)
    else: r.line.fill.background()
    r.shadow.inherit = False; tilt(r, x, y, w, h); return r

def text(x, y, w, h, t, size, color, font, bold=False, align=PP_ALIGN.LEFT, anchor=MSO_ANCHOR.TOP, ls=None):
    tb = s.shapes.add_textbox(Emu(x*PX), Emu(y*PX), Emu(w*PX), Emu(h*PX)); tf = tb.text_frame
    tf.word_wrap = True; tf.vertical_anchor = anchor
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    p = tf.paragraphs[0]; p.alignment = align
    if ls: p.line_spacing = ls
    r = p.add_run(); r.text = t; r.font.size = Pt(size*0.75); r.font.name = font; r.font.bold = bold
    r.font.color.rgb = RGBColor.from_string(color); tilt(tb, x, y, w, h); return tb

# card
shape(MSO_SHAPE.RECTANGLE, 62, 56, 976, 1238, "DDD5C2")           # soft offset shadow
shape(MSO_SHAPE.RECTANGLE, 50, 44, 976, 1238, PAPER)             # card

# photo, top left, thin cream border
shape(MSO_SHAPE.RECTANGLE, 96, 96, 390, 390, CREAM, GRAY, 3)
shape(MSO_SHAPE.RECTANGLE, 112, 112, 358, 358, GRAY)
text(124, 112, 334, 358, "[PHOTO: square, head and shoulders, smiling. Change Picture.]", 26, "22371F", DISPLAY, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

# scalloped badge, top right
bx, by, br = 780, 290, 175
for i in range(20):
    a = 2*math.pi*i/20; cx, cy = bx+math.cos(a)*(br-14), by+math.sin(a)*(br-14)
    shape(MSO_SHAPE.OVAL, cx-30, cy-30, 60, 60, CREAM)
shape(MSO_SHAPE.OVAL, bx-br+16, by-br+16, 2*br-32, 2*br-32, CREAM)
shape(MSO_SHAPE.OVAL, bx-135, by-135, 270, 270, PAPER, GOLD, 3)
logo = os.path.join(here, "..", "..", "assets", "logo", "sfw-foundation-wordmark-240.png")
pic = s.shapes.add_picture(logo, Emu(int((bx-95)*PX)), Emu(int((by-82)*PX)), Emu(190*PX), Emu(165*PX))
tilt(pic, bx-95, by-82, 190, 165)

# bio, slightly rotated with the card
text(110, 540, 860, 400, "[COPY: Allison] Short personal bio in the teacher's own voice. How long she has been on the team, "
     "what she teaches, and a few fun details about life outside work. Warm and a little funny. Four or five lines.",
     46, INK, HAND, False, ls=1.0)

# ribbons: name (top), title (overlapping below), thin gray URL stripe
shape(MSO_SHAPE.RECTANGLE, 86, 1000, 908, 118, GRAY)  # placeholder removed below
s.shapes._spTree.remove(s.shapes[-1]._element)
shape(MSO_SHAPE.RECTANGLE, 40, 960, 1000, 130, NAME_RIBBON)
text(60, 960, 960, 130, "[COPY: Allison] TEACHER NAME", 64, WHITE, DISPLAY, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
shape(MSO_SHAPE.RECTANGLE, 100, 1070, 880, 92, GREEN)
text(100, 1070, 880, 92, "[COPY: Allison] Job title", 38, WHITE, DISPLAY, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)
shape(MSO_SHAPE.RECTANGLE, 150, 1162, 780, 40, GRAY)
text(150, 1162, 780, 40, "school.soilfoodweb.com", 24, "22371F", DISPLAY, True, PP_ALIGN.CENTER, MSO_ANCHOR.MIDDLE)

prs.save(os.path.join(here, "teachers-day-card.pptx"))
