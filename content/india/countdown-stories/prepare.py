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
    # A. The Velliangiri Hills. Taken right of centre, where the far ridge and
    #    the bank of mist sit high in the frame and the forested ridge runs in
    #    along the bottom, under the type.
    'navi-EkQEfFhmhrg-unsplash.jpg':            (1900,    0, 4150, 4000),
    # B. The mountain under cloud. Sky trimmed off the top so the peak rides
    #    up into the clear part of the frame, well above where the scrim comes
    #    in and well above the headline.
    'nitish-surelia-OWyHIv86QSY-unsplash.jpg':  ( 486,  520, 2231, 3623),
    # C. Light breaking through storm cloud over the plain. The darkest
    #    picture in the set and the one with the most structure in its top
    #    half, which is the half this frame leaves uncovered.
    'cymatics-in-pz73YMEi21I-unsplash.jpg':     (1150,    0, 2416, 2250),
    # D. The terraces. Taken right of centre so the cut banks and the rows
    #    read beside the cream card rather than behind it.
    'ranjini-hemanth-KljpahUzp9U-unsplash.jpg': (2400,    0, 4650, 4000),
    # E. Sunset with a wide open sky. The horizon sits low, which leaves the
    #    middle of the frame empty for the type.
    'gowtham-agm-WUmWuxVdC1g-unsplash.jpg':     ( 235,    0, 2766, 4500),
    # F and G are the two extended-deadline frames, alternates of A. They get
    # their own pictures so a viewer who saw A does not think nothing changed.
    'remi-clinton-E5egsk4eUQ0-unsplash.jpg':    (1800,    0, 4050, 4000),
    'div-1UFPvT_Qrt4-unsplash.jpg':             (1400,    0, 2676, 2268),
}
for name, box in CROPS.items():
    im = Image.open(os.path.join(SRC, name))
    w, h = box[2]-box[0], box[3]-box[1]
    assert abs(w/h - 1080/1920) < 0.02, (name, w, h, w/h)
    out = im.crop(box).resize((1080, 1920), Image.LANCZOS)
    dst = os.path.join(OUT, name.replace('-unsplash.jpg', '-1080x1920.jpg'))
    out.save(dst, quality=90, subsampling=1, optimize=True)
    print('%-46s %s -> 1080x1920  %s KB' % (os.path.basename(dst), (w, h),
                                            round(os.path.getsize(dst)/1024)))
