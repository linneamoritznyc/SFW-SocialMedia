"""Prepare the two things the story frames need that CSS cannot do.

    python3 content/india/countdown-stories/prepare.py

1. Two knockouts of the wordmark. The supplied logo is a colour mark and its
   green and brown vanish against a photograph. Each knockout keeps the shape
   and the transparency and replaces every colour with one flat brand colour:
   Organic Cream for the four dark frames, Soil Brown for frame E, whose
   scrim is Natural Tan.

2. A 1080 x 1920 crop of each chosen photograph. CSS object-fit can only
   choose one axis when the picture and the frame disagree this much, so the
   crops are cut here, by hand, with the subject placed where the type will
   not cover it. Each box below is (left, top, right, bottom) in the source
   file's own pixels.
"""
from PIL import Image
import os

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))
SRC  = os.path.join(REPO, 'assets', 'india-free-images')
OUT  = os.path.join(SRC, 'crops')
KNOCKOUTS = {'cream': (244, 241, 234), 'soil': (79, 52, 51)}

# --- the cream wordmark -----------------------------------------------------
for tone, rgb in KNOCKOUTS.items():
    logo = Image.open(os.path.join(REPO, 'assets', 'logo',
                                   'sfw-foundation-wordmark-240.png')).convert('RGBA')
    px = logo.load()
    for y in range(logo.size[1]):
        for x in range(logo.size[0]):
            a = px[x, y][3]
            px[x, y] = rgb + (a,) if a else (0, 0, 0, 0)
    dst = os.path.join(REPO, 'assets', 'logo', 'sfw-foundation-wordmark-%s.png' % tone)
    logo.save(dst)
    print('%s wordmark %s' % (tone, logo.size))

# --- the crops --------------------------------------------------------------
CROPS = {
    # The photograph is now the top 45 percent of the frame, 1080 x 864, so
    # the crop is a 1.25:1 window rather than a 9:16 slice. Each box is
    # (left, top, right, bottom) in the source file's own pixels, chosen so
    # the subject sits in the frame and the top left stays dark enough for a
    # cream logo.
    'navi-EkQEfFhmhrg-unsplash.jpg':            ( 500,    0, 5500, 4000),
    'nitish-surelia-OWyHIv86QSY-unsplash.jpg':  (   0,  900, 2717, 3074),
    'cymatics-in-pz73YMEi21I-unsplash.jpg':     ( 600,    0, 3413, 2250),
    'ranjini-hemanth-KljpahUzp9U-unsplash.jpg': ( 500,    0, 5500, 4000),
    'gowtham-agm-WUmWuxVdC1g-unsplash.jpg':     (   0,  800, 3000, 3200),
    'remi-clinton-E5egsk4eUQ0-unsplash.jpg':    ( 500,    0, 5500, 4000),
    'div-1UFPvT_Qrt4-unsplash.jpg':             ( 600,    0, 3435, 2268),
}
OUT_W, OUT_H = 1080, 864
for name, box in CROPS.items():
    im = Image.open(os.path.join(SRC, name))
    w, h = box[2]-box[0], box[3]-box[1]
    assert abs(w/h - OUT_W/OUT_H) < 0.02, (name, w, h, w/h)
    out = im.crop(box).resize((OUT_W, OUT_H), Image.LANCZOS)
    dst = os.path.join(OUT, name.replace('-unsplash.jpg', '-%sx%s.jpg' % (OUT_W, OUT_H)))
    out.save(dst, quality=90, subsampling=1, optimize=True)
    print('%-44s %s -> %sx%s  %s KB' % (os.path.basename(dst), (w, h), OUT_W, OUT_H,
                                        round(os.path.getsize(dst)/1024)))
