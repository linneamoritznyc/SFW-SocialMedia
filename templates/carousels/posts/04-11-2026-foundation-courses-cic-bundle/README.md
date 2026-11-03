# 04-11-2026 Foundation Courses + Compost Intensive Course bundle

Instagram + LinkedIn, Wednesday 4 November 2026. Two slides, 1080 x 1350.
Editable file: `../04-11-2026-foundation-courses-cic-bundle.pptx` (open in Canva or PowerPoint, Montserrat installed).

Rebuild everything (layers, PPTX, previews) from the repository root:

    pip install python-pptx pillow numpy scipy
    python3 templates/carousels/posts/04-11-2026-foundation-courses-cic-bundle/build.py

## Objects in the PPTX

| Slide 1 (cover) | Slide 2 (what's in it) |
| :-- | :-- |
| Background (paper) | Background (paper) |
| Illustration (bean seedling and root ball) | Illustration (soil band, seedlings, roots) |
| Green box (Food Web Green) | Brown box (Soil Brown) |
| Headline, Montserrat Bold 86 px | Headline, Montserrat Bold 68 px |
| Details, Montserrat Regular 52 px | Details, Montserrat Regular 52 px |
| SFW logo (white, 150 px) | SFW logo (white, 150 px) |
| Flower (continues on slide 2) | Flower (continues from slide 1) |

The coneflower is placed one slide-width apart on the two slides, so its head is cut by the cover's right
edge and finishes on slide 2's left edge when you swipe. Move both together, or neither.

## Design

- Cover: the green box sits top left and bleeds off two edges; the seedling's left leaves tuck under it.
  The plant falls to the lower right, where the flower half-appears at the edge to pull the swipe.
- Slide 2 mirrors the diagonal: the soil band runs across the top and the brown box sits bottom right,
  so the roots run down behind it as if the box is the soil itself.
- One paper tone (`#F7F3EB`) under both illustrations, so the two slides read as one sheet.
- Slide 2's box is about 57% of the slide (the cover's is 41%). Eight lines of 52 px type can't fit
  in a smaller box. The painted ground line and root crowns stay fully visible above it. To shrink the box,
  drop one item; don't make the type smaller.
- Wording cut to fit at 52 px: "2 batches of compost, yours to keep" became "2 batches of compost to keep".
  Long items wrap to two lines.

## Art

Watercolor illustrations, generated on Replicate with FLUX 1.1 Pro and upscaled x2 with Real-ESRGAN.
They are illustrations, never presented as SFW photographs or microscopy. Prompt prefix and prompts:
`art/candidates/replicate_gen.py` (prefix adapted from SFWassetlibrarycontentautomation
`tools/wormhole-visuals/watercolor_gen.py`). Twelve candidates in `art/candidates/*.jpg`.
Chosen: `s1-seedling-b` (cover), `pano-a` (slide 2), `flower-b` (coneflower).
Rejected: `s1-seedling-c` (came back as a mock-up on an orange table), `pano-b` (black letterbox bars),
`pano-c` and `s2-*` (busier or weaker than the chosen ones).

`previews/` is for visual QA only; post from the PPTX.
