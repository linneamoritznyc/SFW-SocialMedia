"""Cut the sign-up photograph band down to the height the layout now uses.

    python3 content/india/countdown-stories/recrop-signup.py

The sign-up story carries the enrollment page's urgency copy in full, and the
support paragraph was raised from 36px to 46px so it reads on a handset. The
rule is to shrink the photograph, never the type, so the band went from 690px
to 570px. Each -signup.jpg is trimmed in place to the new height, keeping the
window at the same vertical bias (0.42) the framing was chosen at, so the
subject stays where it was. Idempotent: a crop already at 570 is left alone.
"""
from PIL import Image
import glob
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
CROPS = os.path.join(REPO, 'assets', 'india-free-images', 'crops')
TARGET_H = 570
BIAS = 0.42

for src in sorted(glob.glob(os.path.join(CROPS, '*-signup.jpg'))):
    im = Image.open(src)
    w, h = im.size
    if h <= TARGET_H:
        print('%-46s %sx%s  already trimmed' % (os.path.basename(src), w, h))
        continue
    top = round((h - TARGET_H) * BIAS)
    im.crop((0, top, w, top + TARGET_H)).save(src, quality=90, subsampling=1, optimize=True)
    print('%-46s %sx%s -> %sx%s  (top %s)' % (os.path.basename(src), w, h, w, TARGET_H, top))
