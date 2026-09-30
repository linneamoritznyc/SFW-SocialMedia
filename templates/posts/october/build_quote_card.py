"""Mentor quote card (the look of the existing Carla card): photo overlapping the page, line-drawn mushrooms and spores,
soft wave, footer bar. Palette: SFW greens. Run: python3 build_quote_card.py"""
import math, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from lib import *
LINE = "7F8F73"   # muted green line art

def wave(s, x0, x1, base, amp, y_bottom, fill, phase=0.0):
    pts = [(x, base + amp * math.sin((x - x0) / (x1 - x0) * 2 * math.pi * 0.9 + phase) - amp * 0.6 * ((x - x0) / (x1 - x0))) for x in range(int(x0), int(x1) + 1, 20)]
    pts += [(x1, y_bottom), (x0, y_bottom)]
    poly(s, pts, fill)

def mushroom(s, cx, base, h, cap_w):
    cap_h = cap_w * 0.55; stem_w = max(10, cap_w * 0.16)
    rrect(s, cx - stem_w / 2, base - h, stem_w, h, None, radius=stem_w / 2, line=LINE, lw=2)
    rect(s, cx - cap_w / 2, base - h - cap_h * 0.55, cap_w, cap_h, None, line=LINE, lw=2, kind=MSO_SHAPE.ROUND_2_SAME_RECTANGLE, radius=None).adjustments[0] = 0.5
    rect(s, cx - cap_w / 2 + 6, base - h - cap_h * 0.55 + cap_h * 0.55, cap_w - 12, 6, None, line=LINE, lw=2)

def spores(s, pts):
    for cx, cy, r in pts:
        oval(s, cx - r, cy - r, 2 * r, 2 * r, None, line=LINE, lw=2)
        for k in range(6):
            a = k * 1.05; rr = r * 0.55
            oval(s, cx + rr * math.cos(a) - 3, cy + rr * math.sin(a) - 3, 6, 6, LINE)

def card(d, photo_src, quote, name, role, note=""):
    s = d.slide(CREAM, note, counter=False, tid="Quote card")
    collage(s, 'cut-green-scribble.png', -40, -30, w=220, rot=-8); collage(s, 'cut-blue-lines.png', 880, -20, w=200, rot=10)
    collage(s, "cut-sage-dots.png", 610, 770, w=230, rot=-6); collage(s, "stones-stack.png", 880, 720, h=470)
    collage(s, "fern-green.png", 560, 1010, w=470, rot=-4)
    photo(s, 0, 300, 560, 930, photo_src, note=note)
    text(s, 610, 150, 400, 52, "“", 60, GREEN, HEAD, True, alpha=40)
    sz = fit(quote, 400, [40, 36, 32], 9, True); h = th(quote, sz, 400, True, 1.2)
    text(s, 610, 210, 400, h + 10, quote, sz, DEEP, HEAD, True, align="c", spacing=1.2)
    y = 210 + h + 30
    rect(s, 660, y, 300, 2, DEEP); 
    text(s, 610, y + 20, 400, 40, name, 26, DEEP, HEAD, True, align="c")
    text(s, 610, y + 62, 400, 34, role, 24, DEEP, BODY, align="c")
    rect(s, 0, 1230, 1080, 120, DEEP)
    logo(s, x=80, y=1245, size=90)
    text(s, 200, 1230, 460, 120, "Soil Food Web", 34, GLOW, HEAD, True, anchor="m")
    text(s, 640, 1230, 360, 120, "@soilfoodwebschool", 26, CREAM, BODY, align="r", anchor="m")
    return s

d = Deck(1080, 1350, "quote-card")
card(d, "assets/mentors-teachers-day/carla-portugal.jpg", f"{TAG} Quote in Carla's own words.", "Dr. Carla Portugal", "Soil Food Web Mentor",
     note="Photo is only 499 px wide, so it is soft at this size: swap for a larger cut-out photo. Quote must be Carla's own words.")
d.finish("2026-10-06-tue-ig-mentor-carla-quote-card.pptx", counters=False)
