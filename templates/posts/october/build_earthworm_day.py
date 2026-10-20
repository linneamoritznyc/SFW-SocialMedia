"""World Earthworm Day, Wednesday 21 October 2026 (Wormhole plan p08). Seven slides, words exactly as in the October
planning doc. Look per wormhole/voice.md: white backgrounds, real photography, an object cut out on pure white with a
small serif label, a small letter-spaced SOIL FOOD WEB wordmark. No beige, no gold, no tape, no tilted snapshots.

Photos: Unsplash (credits in assets/unsplash-earthworm/CREDITS.md and on each slide) and assets/photo/.
python3 templates/posts/october/build_earthworm_day.py
"""
from pptx.util import Emu
from lib import Deck, rect, text, crop, PX
from build_oct_01_10 import logo, pic, save

W, H, M = 1080, 1350, 80
GREEN, INK, GREY, WHITE = "31662F", "1F1F1F", "6B6B6B", "FFFFFF"
U = "assets/unsplash-earthworm/"
NOTE = " Photos: Unsplash, credits in assets/unsplash-earthworm/CREDITS.md. Words: October 2026 Social Media Planning Doc."


def wordmark(s, y=60, color=GREEN):
    text(s, M, y, W - 2 * M, 30, "SOIL FOOD WEB", 18, color, "Montserrat", True, track=6)


def credit(s, t, color=GREY, y=H - 44):
    text(s, M, y, W - 2 * M, 24, t, 13, color, "Source Sans 3")


def photo(s, rel, x, y, w, h, fx=0.5, fy=0.5):
    s.shapes.add_picture(crop(rel, int(w * 2), int(h * 2), fx, fy), Emu(int(x * PX)), Emu(int(y * PX)), Emu(int(w * PX)), Emu(int(h * PX)))


def photo_slide(d, rel, words, who, n, fx=0.5, fy=0.5, ph=760):
    """Real photo across the top, the slide's sentence on white below."""
    s = d.slide(WHITE, f"Slide {n}." + NOTE, counter=False)
    photo(s, rel, 0, 0, W, ph, fx, fy)
    wordmark(s, ph + 60)
    text(s, M, ph + 110, W - 2 * M, H - ph - 200, words, 40, INK, "Montserrat", True, spacing=1.15)
    credit(s, who)
    return s


def build():
    d = Deck(name="21-10-2026-wed-ig-world-earthworm-day")

    # 1 cover: full-bleed earthworm, white card (Fibershed style)
    s = d.slide(WHITE, "Slide 1: cover." + NOTE, counter=False)
    photo(s, U + "worm-dark-soil.jpg", 0, 0, W, H, 0.3, 0.5)
    rect(s, M, 820, W - 2 * M, 400, WHITE)
    text(s, M + 40, 865, W - 2 * M - 80, 30, "SOIL FOOD WEB", 18, GREEN, "Montserrat", True, track=6)
    text(s, M + 40, 920, W - 2 * M - 80, 40, "WORLD EARTHWORM DAY · OCTOBER 21", 20, GREY, "Montserrat", True, track=3)
    text(s, M + 40, 975, W - 2 * M - 80, 220, "How do worms work their magic?", 64, INK, "Montserrat", True, spacing=1.05)
    text(s, M, H - 44, W - 2 * M, 24, "Photo: Julian Zwengel on Unsplash", 13, WHITE, "Source Sans 3")

    # 2 the anecic earthworm, cut out on white with a small serif label
    s = d.slide(WHITE, "Slide 2: earthworm cut out on white." + NOTE, counter=False)
    wordmark(s)
    pic(s, U + "worm-cutout.png", 60, 200, 960)
    text(s, M, 640, W - 2 * M, 30, "Anecic earthworm", 28, GREY, "EB Garamond")
    rect(s, M, 690, 80, 3, GREEN)
    text(s, M, 730, W - 2 * M, 420, "Anecic earthworms dig vertical burrows that can reach 1 to 2 meters deep to break up compaction.",
         44, INK, "Montserrat", True, spacing=1.15)
    credit(s, "Photo: Julian Zwengel on Unsplash")

    photo_slide(d, U + "hands-soil-worms.jpg", "They spread microbes around as they move by lining the walls with mucus and casts, rich in nutrients and microbes.",
                "Photo: sippakorn yamkasikorn on Unsplash", 3, 0.5, 0.45, ph=720)
    photo_slide(d, U + "rain-grass.jpg", "Their channels let rain soak in fast without causing the ground to go anaerobic.",
                "Photo: Roman Synkevych on Unsplash", 4, 0.5, 0.6)

    # 5 question tile
    s = d.slide(WHITE, "Slide 5: question tile." + NOTE, counter=False)
    wordmark(s)
    text(s, M, 470, W - 2 * M, 300, "How to care for them?", 88, GREEN, "Montserrat", True, spacing=1.0)
    pic(s, U + "worm-cutout.png", 300, 860, 700)
    credit(s, "Photo: Julian Zwengel on Unsplash")

    photo_slide(d, "assets/photo/garden-vegetable-beds.jpg", "Digging cuts the burrows. No‑dig keeps the plumbing intact.",
                "Photo: SFW library", 6, 0.5, 0.5)

    s = photo_slide(d, U + "autumn-leaves-ground.jpg", "Add organic matter (Or simply don’t remove it)",
                    "Photo: Annie Spratt on Unsplash", 7, 0.5, 0.5)
    logo(s, W - M - 150, H - 200, 150, white=False)
    save(d, "21-10-2026-wed-ig-world-earthworm-day.pptx")


if __name__ == "__main__":
    build()
