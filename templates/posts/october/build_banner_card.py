"""Mentor banner cards (the look of the Gerald Ramírez instructor post): full-bleed photo, dark green name band with
thin rules, line-drawn leaves top right, logo panel top left. Run: python3 build_banner_card.py"""
import math, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from lib import *

def leaf(s, cx, cy, length, ang, width=0.30, color=WHITE):
    """Outline leaf with a midrib, built from native freeform lines (rotated about its base)."""
    a = math.radians(ang); pts = []
    for t in [i / 12 for i in range(13)]:
        pts.append((t * length, math.sin(math.pi * t) * length * width / 2))
    for t in [i / 12 for i in range(12, -1, -1)]:
        pts.append((t * length, -math.sin(math.pi * t) * length * width / 2))
    rot = [(cx + x * math.cos(a) - y * math.sin(a), cy + x * math.sin(a) + y * math.cos(a)) for x, y in pts]
    sh = poly(s, rot, CREAM, line=color, lw=2)
    sh.fill.background()
    mid = [(cx, cy), (cx + length * 0.95 * math.cos(a), cy + length * 0.95 * math.sin(a))]
    ln = s.shapes.add_connector(1, Emu(int(mid[0][0] * PX)), Emu(int(mid[0][1] * PX)), Emu(int(mid[1][0] * PX)), Emu(int(mid[1][1] * PX)))
    ln.line.color.rgb = rgb(color); ln.line.width = Emu(2 * PX)

def card(d, photo_src, name, role, fy=0.3, note=""):
    s = d.slide(DEEP, note, counter=False, tid="Banner card")
    photo(s, 0, 0, 1080, 1010, photo_src, fy=fy)
    s._deck.meta[-1]['dark'] = True
    for cx, cy, ln_, ang in [(1085, -15, 330, 112), (1085, -15, 360, 132), (1085, -15, 300, 152), (1085, 120, 230, 158)]:
        leaf(s, cx, cy, ln_, ang)
    rrect(s, -60, -60, 400, 240, "3A3A3A", alpha=72, radius=40)       # logo panel, kept small so it stays off the face
    logo(s, x=50, y=40, size=110)
    for y in (770, 772, 1005, 1007): pass
    rect(s, 0, 1010, 1080, 340, DEEP)
    rect(s, 0, 940, 1080, 230, DEEP, alpha=78)
    rect(s, 0, 936, 1080, 4, LIGHT); rect(s, 0, 950, 1080, 2, LIGHT); rect(s, 0, 1170, 1080, 4, LIGHT)
    sz = fit(name, 900, [64, 58, 52], 1, True)
    text(s, 80, 965, 900, 110, name, sz, WHITE, HEAD, True, anchor="m")
    text(s, 80, 1070, 900, 70, role.upper(), 36, WHITE, BODY, anchor="m", track=1)
    text(s, 80, 1235, 920, 50, "@soilfoodwebschool", 30, CREAM, BODY)
    return s

d = Deck(1080, 1350, "banner-cards")
for n, r, f in (("Dr. Carla Portugal", "Instructor, Mentor and Researcher", "assets/mentors-teachers-day/carla-portugal.jpg"), ("Nick Padwick", "Farmer, Consultant and Mentor", "assets/mentors-teachers-day/nick-padwick.jpg"),
                ("Wes Sander", "Consultant and Mentor", "assets/mentors-teachers-day/wes-sander.jpg"), ("Gerald Ramírez", "Instructor and Mentor", "assets/mentors-teachers-day/gerald-ramirez.jpg"),
                ("Dr. Caterina Capri", "Advanced Programs Instructor", "Dr. Caterina Capri, portrait")):
    card(d, f, n, r, note="Banner-card alternative for the Teachers' Day mentors. Replace the two LOGO circles with the School logo and the second mark.")
d.finish("2026-10-05-mon-ig-teachers-day-banner-cards-alt.pptx", counters=False)
