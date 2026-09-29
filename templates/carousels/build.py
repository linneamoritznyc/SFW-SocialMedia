import os
"""Builds the four carousel templates as PPTX. Run: python3 build.py
1080 x 1350 (4:5). Colours and fonts from variants/_tokens.css. Every content
text box carries [COPY: Allison]; fixed labels (series name, handle) do not."""
from pptx import Presentation
from photos import crop
from pptx.util import Emu, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

PX = 9525
W, H = 1080, 1350
C = dict(cream="F4F1EA", panel="E6EADC", green="156826", moss="22371F", glow="DBE6A7",
         sage="A7B097", gold="C9A227", ink="333130", faint="6A665C", white="FFFFFF", scope="3C3841")
DISPLAY, SERIF, SANS = "Montserrat", "EB Garamond", "Source Sans 3"
TAG = "[COPY: Allison]"

def rgb(h): return RGBColor.from_string(h)

def new():
    p = Presentation(); p.slide_width = Emu(W*PX); p.slide_height = Emu(H*PX); return p

def slide(p, bg, notes=""):
    s = p.slides.add_slide(p.slide_layouts[6])
    s.background.fill.solid(); s.background.fill.fore_color.rgb = rgb(C[bg])
    if notes: s.notes_slide.notes_text_frame.text = notes
    return s

def rect(s, x, y, w, h, fill=None, line=None, shape=MSO_SHAPE.RECTANGLE, lw=1):
    r = s.shapes.add_shape(shape, Emu(x*PX), Emu(y*PX), Emu(w*PX), Emu(h*PX))
    if fill: r.fill.solid(); r.fill.fore_color.rgb = rgb(C[fill])
    else: r.fill.background()
    if line: r.line.color.rgb = rgb(C[line]); r.line.width = Emu(int(lw*PX))
    else: r.line.fill.background()
    r.shadow.inherit = False
    return r

def text(s, x, y, w, h, t, size, color="ink", font=SANS, bold=False, italic=False,
         align="l", anchor="t", spacing=None):
    size = max(size, 40) if size < 100 else size   # labels, handles: 40px minimum (phone)
    tb = s.shapes.add_textbox(Emu(x*PX), Emu(y*PX), Emu(w*PX), Emu(h*PX))
    tf = tb.text_frame; tf.word_wrap = True
    tf.margin_left = tf.margin_right = tf.margin_top = tf.margin_bottom = 0
    tf.vertical_anchor = dict(t=MSO_ANCHOR.TOP, m=MSO_ANCHOR.MIDDLE, b=MSO_ANCHOR.BOTTOM)[anchor]
    for i, line in enumerate(t.split("\n")):
        para = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        para.alignment = dict(l=PP_ALIGN.LEFT, c=PP_ALIGN.CENTER, r=PP_ALIGN.RIGHT)[align]
        if spacing: para.line_spacing = spacing
        r = para.add_run(); r.text = line
        f = r.font; f.size = Pt(size*0.75); f.name = font; f.bold = bold; f.italic = italic
        f.color.rgb = rgb(C[color])
    return tb

def copy(s, x, y, w, h, hint, size, **kw):
    size = 40 if size < 34 else (76 if size < 76 else size)   # body 76px minimum, small print 40px
    return text(s, x, y, w, h, f"{TAG} {hint}", size, **kw)

def photo(s, x, y, w, h, label, fill="sage"):
    rect(s, x, y, w, h, fill=fill)
    small = w < 500
    msg = f"[PHOTO: {label}]" if small else f"[PHOTO: {label}]\nRight-click, Change Picture. Only real SFW photos, with consent."
    text(s, x+20, y, w-40, h, msg, 22 if small else 30, color="glow" if fill == "moss" else "moss",
         font=DISPLAY, bold=True, align="c", anchor="m")

def bignum(s, x, y, w, color, size=200, h=300):
    copy(s, x, y, w, 40, "Big number", 26, color=color, font=DISPLAY, bold=True)
    text(s, x, y+50, w, h, "[Big number]", size, color=color, font=DISPLAY, bold=True, anchor="m")

def handle(s, color="faint", y=1280):
    text(s, 60, y, 960, 36, "@soilfoodwebschool", 28, color=color, font=DISPLAY, bold=True)

def dots(s, n, i, on="green", off="sage", y=1290):
    for k in range(n):
        rect(s, 1020 - (n-k)*30, y+8, 16, 16, fill=on if k == i else off, shape=MSO_SHAPE.OVAL)

def source(s, y=1200, color="faint", x=60, w=960):
    copy(s, x, y, w, 60, "Source: who, where, year.", 26, color=color)

# ------------------------------------------------------------------ 1
def graduate():
    p = new()
    s = slide(p, "moss", "Cover. Portrait needs the graduate's written consent. Headline: name, location.")
    photo(s, 0, 0, W, 900, "Large portrait of the graduate", fill="sage")
    rect(s, 0, 900, W, 450, fill="moss")
    text(s, 60, 60, 960, 40, "SOIL REGENERATORS IN THE WILD", 28, color="glow", font=DISPLAY, bold=True)
    copy(s, 60, 900, 960, 250, "Graduate name,\nTown, Country", 56, color="white", font=DISPLAY, bold=True, spacing=1.05)
    copy(s, 60, 1190, 960, 60, "One proud line about them.", 30, color="glow", font=SERIF, italic=True)
    dots(s, 5, 0, on="glow", off="scope")

    s = slide(p, "cream", "Slide 2. Land or project photo plus where they started.")
    photo(s, 0, 0, W, 860, "Their land or project, before or early on")
    copy(s, 60, 920, 960, 40, "Where they started", 30, color="green", font=DISPLAY, bold=True)
    copy(s, 60, 980, 960, 200, "One line: how it began.", 52, color="moss", font=SERIF, spacing=1.1)
    handle(s); dots(s, 5, 1)

    s = slide(p, "panel", "Slide 3. Name one practice or crop. No jargon without a definition.")
    text(s, 60, 60, 960, 40, "WHAT THEY CHANGED", 28, color="green", font=DISPLAY, bold=True)
    copy(s, 60, 200, 960, 420, "One line on the change. Name the practice or crop.", 60, color="moss", font=DISPLAY, bold=True, spacing=1.08)
    rect(s, 60, 760, 960, 4, fill="green")
    copy(s, 60, 820, 960, 240, "Optional: why, in their words.", 40, color="ink", font=SERIF, italic=True)
    handle(s); dots(s, 5, 2)

    s = slide(p, "moss", "Slide 4. One number, Harvest Gold. Needs the graduate's report and year in the source line.")
    text(s, 60, 60, 960, 40, "THE RESULT", 28, color="glow", font=DISPLAY, bold=True)
    bignum(s, 60, 200, 960, "gold", 170, 360)
    copy(s, 60, 650, 960, 260, "What it measures, against what.", 46, color="white", font=SERIF)
    source(s, 1150, color="sage")
    handle(s, "sage"); dots(s, 5, 3, on="glow", off="scope")

    s = slide(p, "cream", "Slide 5. Real quote, approved by the graduate. Do not paraphrase into a quote.")
    text(s, 60, 60, 300, 200, "“", 260, color="green", font=SERIF, bold=True)
    copy(s, 60, 280, 960, 640, "Short quote, their own words.", 66, color="moss", font=SERIF, italic=True, spacing=1.12)
    copy(s, 60, 980, 960, 50, "Graduate name", 30, color="green", font=DISPLAY, bold=True)
    text(s, 60, 1050, 960, 50, "@soilfoodwebschool graduate", 34, color="faint", font=DISPLAY, bold=True)
    dots(s, 5, 4)
    return p

# ------------------------------------------------------------------ 2
def ruled(s, dark=False):
    for y in range(150, H-80, 62):
        rect(s, 0, y, W, 2, fill="sage")
    rect(s, 96, 0, 3, H, fill="sage")  # margin line

def stamp(s):
    copy(s, 560, 40, 460, 90, "DD Mon YYYY\nPlace, Region", 26, color="green", font=DISPLAY, bold=True, align="r")

def fieldnotes():
    p = new()
    s = slide(p, "cream", "Cover. Place and season, e.g. 'Spring 2026'. Trial name from the graduate's report.")
    ruled(s); stamp(s)
    text(s, 130, 60, 850, 40, "FIELD NOTES", 30, color="green", font=DISPLAY, bold=True)
    copy(s, 130, 400, 850, 300, "Trial name, as the graduate titled it", 66, color="moss", font=DISPLAY, bold=True, spacing=1.05)
    copy(s, 130, 780, 850, 130, "Place\nSeason and year", 46, color="green", font=SERIF, italic=True)
    dots(s, 6, 0)

    def page(n, label, hint, size=64, note=""):
        s = slide(p, "cream", note); ruled(s); stamp(s)
        text(s, 130, 60, 850, 40, label, 30, color="green", font=DISPLAY, bold=True)
        copy(s, 130, 230, 850, 800, hint, size, color="moss", font=SERIF, spacing=1.1)
        dots(s, 6, n); return s

    page(1, "THE QUESTION", "The question they tested.", note="Slide 2.")
    s = slide(p, "cream", "Slide 4 in series: the method. Name the control plot every time.")
    ruled(s); stamp(s)
    text(s, 130, 60, 850, 40, "THE METHOD", 30, color="green", font=DISPLAY, bold=True)
    for i, hint in enumerate(["Line 1: the plots.", "Line 2: the control.", "Line 3: what was measured."]):
        text(s, 130, 232+i*248, 90, 90, str(i+1), 72, color="green", font=DISPLAY, bold=True)
        copy(s, 230, 240+i*248, 750, 200, hint, 50, color="moss", font=SERIF, spacing=1.1)
    dots(s, 6, 2)

    s = slide(p, "cream", "The result. One measure, bars from zero, units stated. Report and year in the source line.")
    ruled(s); stamp(s)
    text(s, 130, 60, 850, 40, "THE RESULT", 30, color="green", font=DISPLAY, bold=True)
    bignum(s, 130, 190, 850, "green", 100, 200)
    copy(s, 130, 470, 850, 160, "What it measures, against what.", 60, color="moss", font=SERIF)
    # before/after bars from a shared baseline
    base = 1080
    rect(s, 130, base, 820, 3, fill="moss")
    rect(s, 230, base-200, 220, 200, fill="sage"); rect(s, 600, base-340, 220, 340, fill="green")
    text(s, 200, base+16, 280, 60, "Control", 28, color="moss", font=DISPLAY, bold=True, align="c")
    text(s, 570, base+16, 280, 60, "Trial", 28, color="moss", font=DISPLAY, bold=True, align="c")
    source(s, 1210, x=130, w=850)
    dots(s, 6, 3)

    page(4, "THE SURPRISE", "What surprised them, including what disappointed.", size=56, note="Series promise: we publish what the trial found, including when results disappoint.")

    s = slide(p, "cream", "Who ran it. Portrait needs written consent.")
    ruled(s); stamp(s)
    text(s, 130, 60, 850, 40, "WHO RAN IT", 30, color="green", font=DISPLAY, bold=True)
    photo(s, 130, 230, 300, 300, "Small portrait", fill="sage")
    text(s, 470, 250, 510, 260, f"{TAG} Graduate name\nPlace", 50, color="moss", font=DISPLAY, bold=True, spacing=1.05)
    copy(s, 130, 660, 850, 400, "Their ground, their crop, their years.", 46, color="moss", font=SERIF, spacing=1.1)
    text(s, 130, 1200, 850, 40, "@soilfoodwebschool", 28, color="faint", font=DISPLAY, bold=True)
    dots(s, 6, 5)
    return p

# ------------------------------------------------------------------ 3
def didyouknow(cover="assets/microscopy/fungal-spores-in-suspension.jpg", cover_note="brightfield soil sample: round spores and short bacterial rods"):
    p = new()
    s = slide(p, "scope", "Cover. Photo: " + cover + " (" + cover_note + "). Swap to match the fact. Fact must have a named source before posting.")
    s.shapes.add_picture(crop(cover, W, 640), 0, 0, Emu(W*PX), Emu(640*PX))
    text(s, 60, 670, 960, 40, "DID YOU KNOW", 28, color="glow", font=DISPLAY, bold=True)
    copy(s, 60, 730, 960, 460, "One surprising fact. Name the organism.", 50, color="white", font=DISPLAY, bold=True, spacing=1.1)
    text(s, 60, 1280, 960, 36, "Swipe for the mechanism", 28, color="glow", font=DISPLAY, bold=True)
    dots(s, 5, 0, on="glow", off="moss")

    steps = [("STEP 1", "Step one, one line."),
             ("STEP 2", "Step two, one line."),
             ("STEP 3", "Step three, one line.")]
    for i, (lab, hint) in enumerate(steps):
        s = slide(p, "cream", f"Mechanism {lab}. One line only. Diagram: draw it, or use assets/illustration; label parts in plain words.")
        text(s, 60, 60, 400, 40, lab, 28, color="green", font=DISPLAY, bold=True)
        rect(s, 60, 130, 960, 640, fill="panel", line="sage", lw=3)
        text(s, 90, 130, 900, 640, "[DIAGRAM: mechanism, step %d]\nLabel parts in plain words." % (i+1), 32, color="olive" if False else "faint", font=DISPLAY, bold=True, align="c", anchor="m")
        copy(s, 60, 830, 960, 330, hint, 54, color="moss", font=SERIF, spacing=1.1)
        source(s, 1190)
        handle(s); dots(s, 5, i+1)

    s = slide(p, "moss", "Close. One line, tied to the reader's own ground.")
    text(s, 60, 60, 960, 40, "WHY THIS MATTERS FOR YOUR SOIL", 30, color="glow", font=DISPLAY, bold=True)
    copy(s, 60, 300, 960, 600, "One line for their own soil.", 72, color="white", font=DISPLAY, bold=True, spacing=1.1)
    copy(s, 60, 1000, 960, 100, "One call to action, or none.", 36, color="glow", font=SERIF, italic=True)
    handle(s, "sage"); dots(s, 5, 4, on="glow", off="scope")
    return p

# ------------------------------------------------------------------ 4
def checklist():
    p = new()
    s = slide(p, "moss", "Cover. Fill [Number] and [task] in the headline. Keep the Save this label.")
    rect(s, 60, 60, 210, 64, fill="gold", shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    text(s, 60, 60, 210, 64, "Save this", 32, color="moss", font=DISPLAY, bold=True, align="c", anchor="m")
    copy(s, 60, 300, 960, 700, "[Number] things to check before [task]", 100, color="white", font=DISPLAY, bold=True, spacing=1.05)
    copy(s, 60, 1080, 960, 100, "Who this is for, and when.", 38, color="glow", font=SERIF, italic=True)
    handle(s, "sage"); dots(s, 7, 0, on="glow", off="scope")

    for i in range(5):
        s = slide(p, "cream", f"Item {i+1}. One line. If a biological reason exists, say it. Keep to what the source supports.")
        text(s, 40, 200, 460, 760, str(i+1), 640, color="green", font=DISPLAY, bold=True, anchor="m")
        copy(s, 520, 300, 500, 520, f"Item {i+1}: one action.", 48, color="moss", font=DISPLAY, bold=True, spacing=1.1)
        rect(s, 520, 880, 150, 150, fill="panel", line="green", lw=3, shape=MSO_SHAPE.OVAL)
        text(s, 520, 880, 150, 150, "ICON", 28, color="green", font=DISPLAY, bold=True, align="c", anchor="m")
        text(s, 60, 60, 400, 40, f"{i+1} OF 5", 28, color="green", font=DISPLAY, bold=True)
        handle(s); dots(s, 7, i+1)

    s = slide(p, "panel", "Quick reference. Same five items, shortened to fit. Keep it screenshot-friendly.")
    text(s, 60, 60, 960, 40, "QUICK REFERENCE", 28, color="green", font=DISPLAY, bold=True)
    text(s, 60, 130, 960, 130, f"{TAG} [Number] things to check before [task]", 48, color="moss", font=DISPLAY, bold=True, spacing=1.05)
    for i in range(5):
        y = 300+i*170
        rect(s, 60, y, 960, 140, fill="white", shape=MSO_SHAPE.ROUNDED_RECTANGLE)
        rect(s, 84, y+34, 72, 72, fill="green", shape=MSO_SHAPE.OVAL)
        text(s, 84, y+34, 72, 72, str(i+1), 36, color="glow", font=DISPLAY, bold=True, align="c", anchor="m")
        text(s, 190, y, 800, 140, f"{TAG} Item {i+1}", 44, color="moss", font=DISPLAY, bold=True, anchor="m")
    handle(s); dots(s, 7, 6)
    return p

import datetime
DOW = "Mon Tue Wed Thu Fri Sat Sun".split()

# Two-week plan, 3 posts a week (Mon / Wed / Fri). Change START to move the whole plan.
START = datetime.date(2026, 10, 5)
PLAN = [
    (0,  "did-you-know",  "Did you know #1", lambda: didyouknow()),
    (2,  "graduate",      "Soil Regenerators in the wild #1", lambda: graduate()),
    (4,  "checklist",     "Numbered checklist", lambda: checklist()),
    (7,  "field-notes",   "Field Notes", lambda: fieldnotes()),
    (9,  "graduate",      "Soil Regenerators in the wild #2", lambda: graduate()),
    (11, "did-you-know",  "Did you know #2", lambda: didyouknow("assets/microscopy/sfw-amoeba-still-wide.jpg", "still from the amoeba microscopy loop")),
]

def date_deck(p, d, name):
    tag = f"POST: {DOW[d.weekday()]} {d.day} {d.strftime('%b %Y')} | {name}"
    p.core_properties.title = tag
    for s in p.slides:
        tf = s.notes_slide.notes_text_frame
        tf.text = tag + "\n" + tf.text
    return tag

if __name__ == "__main__":
    for fn, out in ((graduate, "soil-regenerators-in-the-wild"), (fieldnotes, "field-notes"), (didyouknow, "did-you-know"), (checklist, "numbered-checklist")):
        fn().save(out + ".pptx")   # undated master templates
    os.makedirs("posts", exist_ok=True)
    for offset, slug, name, make in PLAN:
        d = START + datetime.timedelta(days=offset)
        p = make(); date_deck(p, d, name)
        p.save(f"posts/{d.isoformat()}-{DOW[d.weekday()].lower()}-{slug}.pptx")
