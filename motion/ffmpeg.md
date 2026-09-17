# ffmpeg, against footage we actually hold

Real commands against real files. Durations below were read out of the file
headers, not guessed. **ffmpeg is not installed in this container, so these have
not been executed.** They are written to run on your machine.

## What is in `assets/video/`

| File | Size | Duration | Notes |
| :-- | :-- | :-- | :-- |
| `wild-ken-hill-wkh-2026-reel.mp4` | 406x720 | **40.88s** | The full Wild Ken Hill reel, full quality |
| `wild-ken-hill-wkh-2026-reel-web.mp4` | 406x720 | 40.90s | Same reel, web weight |
| `wild-ken-hill-img-1465.mp4` | 406x720 | 8.01s | Workshop clip |
| `wild-ken-hill-img-1467.mp4` | 406x720 | 8.01s | Workshop clip |
| `wild-ken-hill-img-1471.mp4` | 406x720 | 7.47s | Workshop clip |
| `sfw-amoeba-loop-square.mp4` | 1080x1080 | 10.00s | Microscopy, clean |
| `sfw-amoeba-loop-hero.mp4` | 1280x720 | 10.00s | Microscopy, clean |
| `sfw-amoeba-instagram-4x5.mp4` | 1080x1350 | 10.00s | **Caption burned into the bottom 270px** |
| `sfw-teas-square.mp4` | 1079x1080 | 3.93s | Compost tea |
| `amoeba-square-1/2/3.mp4` | 480x480 | 8 / 8 / 4s | Small exports |

**The four long-form videos are not here.** "How Our Garden Survived a Wildfire"
and the other three are in Drive at 126 to 154 MB. Put one in `assets/video/`
and I can write its cut list the same way.

## The aspect ratio you need to know about

406x720 is 0.5639. A 9:16 reel is 0.5625. **The Wild Ken Hill footage is already
almost exactly reel shape**, which means it upscales to 1080x1920 with a two
pixel crop and no letterboxing. That is unusually lucky.

```
scale=-2:1920,crop=1080:1920
```

---

## 1. Wild Ken Hill reel, first 8 seconds, as a 1080x1920 reel

The GIF export notes already say the first 8 seconds is the usable excerpt and
that the full 41 seconds is too long.

```bash
ffmpeg -ss 0 -t 8 -i assets/video/wild-ken-hill-wkh-2026-reel.mp4 \
  -vf "scale=-2:1920,crop=1080:1920,setsar=1" \
  -r 30 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -an \
  out/wkh-reel-8s-vertical.mp4
```

`-an` drops the audio. Every clip we hold is used silent on the site, so check
whether this one has usable audio before you throw it away.

## 2. Three workshop clips, cut together, 23.5 seconds

Full length of all three, in order, upscaled and normalised.

```bash
printf "file '%s'\n" \
  assets/video/wild-ken-hill-img-1465.mp4 \
  assets/video/wild-ken-hill-img-1467.mp4 \
  assets/video/wild-ken-hill-img-1471.mp4 > /tmp/wkh.txt

ffmpeg -f concat -safe 0 -i /tmp/wkh.txt \
  -vf "scale=-2:1920,crop=1080:1920,setsar=1,fps=30" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -an \
  out/wkh-three-clips-vertical.mp4
```

Total 23.49 seconds. Under the 30 second mark, so it runs as a single reel.

## 3. Trim each clip to its best 4 seconds first

Three 8 second clips back to back is slow. **I have not watched these**, so these
timecodes are a starting structure, not a judgement about the footage. Adjust the
`-ss` values once you have looked.

```bash
ffmpeg -ss 2 -t 4 -i assets/video/wild-ken-hill-img-1465.mp4 -c copy out/a.mp4
ffmpeg -ss 2 -t 4 -i assets/video/wild-ken-hill-img-1467.mp4 -c copy out/b.mp4
ffmpeg -ss 1.5 -t 4 -i assets/video/wild-ken-hill-img-1471.mp4 -c copy out/c.mp4
```

Then concat as above. Result is 12 seconds, which is the right length for a
carousel opener or a story.

## 4. Amoeba microscopy as a 1080x1920 background loop

The square loop centred in a vertical frame, on the brand moss green, so text
sits above and below it.

```bash
ffmpeg -i assets/video/sfw-amoeba-loop-square.mp4 \
  -vf "scale=1080:1080,pad=1080:1920:0:420:0x22371F,setsar=1,fps=30" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -an \
  out/amoeba-vertical-bg.mp4
```

`0x22371F` is `--moss`. Ten seconds, loops cleanly because the source does.

## 5. Strip the burned-in caption off the Instagram export

`sfw-amoeba-instagram-4x5.mp4` is 1080x1350 with a white caption card reading
"What lives in one drop?" across the bottom 270px. The picture above it is a
clean 1080x1080.

```bash
ffmpeg -i assets/video/sfw-amoeba-instagram-4x5.mp4 \
  -vf "crop=1080:1080:0:0,setsar=1" \
  -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -an \
  out/amoeba-square-clean.mp4
```

## 6. Compost tea, slowed and looped to 8 seconds

The source is only 3.93 seconds, which is short for a reel. Slow to 50% and
ping-pong it.

```bash
ffmpeg -i assets/video/sfw-teas-square.mp4 \
  -filter_complex "[0:v]setpts=2.0*PTS,scale=1080:1080,split[a][b];[b]reverse[r];[a][r]concat=n=2:v=1[v]" \
  -map "[v]" -r 30 -c:v libx264 -crf 18 -preset slow -pix_fmt yuv420p -an \
  out/teas-8s-pingpong.mp4
```

15.7 seconds at 2.0x. Use `setpts=1.0*PTS` for a 7.9 second version, which is
closer to the 8 second ceiling.

## 7. Poster frames, which we have none of

`assets/video/` holds no still from any clip, which is why none of them can be
posted with a thumbnail today.

```bash
for f in assets/video/*.mp4; do
  ffmpeg -ss 1 -i "$f" -frames:v 1 -q:v 2 \
    "assets/video/posters/$(basename "${f%.mp4}").jpg"
done
```

One second in, so you do not get a black first frame.

## Screen-recording the motion pages

For the four files in `motion/`, not ffmpeg but worth writing down.

- Open in Chromium at 100%, window sized so the 1080x1920 stage is unscaled.
- **Delete the two `.zone` elements first.** They are layout guides, not artwork.
- Record at 30fps. Each loop is under 8 seconds and the last frame fades to
  transparent so the loop point is clean.
- The counters use CSS `@property`, which is Chromium only. They will not
  animate in Safari or Firefox.
