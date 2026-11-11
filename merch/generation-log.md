# Merch generation log

Model: `recraft-ai/recraft-v3-svg` on Replicate. Full prompt per organism in `tools/prompts-used.json`.
Prompt pattern (from the brief): "scientific engraving of [organism], Ernst Haeckel plate style, fine black line
art with cross-hatching, isolated on plain white background, single specimen, centered, no text, no letters,
no words, no border".

## Style choice

The model's schema offers `any`, `engraving`, `line_art`, `line_circuit`, `linocut`.

| Style tried | Result | Decision |
|---|---|---|
| `engraving` (48 images, all 12 organisms x 4) | White lines cut out of a solid black block (scratchboard). Every image is a full black square, so there is no isolated specimen and no background to remove. On a shirt it prints as a black tile. | Rejected, all 48 |
| `line_art` (2 each of bacteria, nematode, springtail) | Heavy, cartoon-thick outlines, flat black fills. Not engraved. | Rejected |
| `any` (2 each of the same three) | Fine engraved line art with hatching and stipple, isolated on white. Closest to a Haeckel plate. | **Used** |

## Anatomy review, `engraving` batch (all rejected for the black-block problem; noted for the prompts)

- Springtail, all 4: drawn as woodlice, 7 or more leg pairs, no furcula. Replaced in the brief's cast list
  ("microarthropods") by an oribatid mite, which is easier to draw correctly (8 legs, domed body).
- Nematode, all 4: snake heads with eyes. Prompt now says blunt rounded head, no eyes, not a snake.
- Mycorrhiza, all 4: drawn as whole trees. Prompt now asks for a root segment with hyphae entering it.
- Root tip, all 4: drawn as a stump with a root ball. Prompt now asks for one root tip with root cap.
- Earthworm, all 4: no clitellum. Prompt now asks for the saddle band.

## `any` batch, design 3 organisms

| Organism | c1 | c2 | c3 | c4 | Pick |
|---|---|---|---|---|---|
| bacteria-rods | 2 cells only | rods with spots, cluttered pili | 3 rods, stippled, peritrichous flagella (real in soil bacilli) | 2 cells, dense | **c3** |
| fungal-hyphae | segmented tube reads as a worm | spore chains, looks like actinobacteria | not generated (credit ran out) | septate branching hyphae; 3 stray blobs removed in code | **c4** |
| heliozoan (protozoa) | ciliate-like cell with wavy tentacles, no straight axopodia | not generated | same fault as c1 | same fault, plus a long tail | none, all rejected |
| flagellate | ciliary fringe as well as flagella (that makes it a ciliate) | same | same | not generated | none, all rejected |
| amoeba, ciliate, nematode, oribatid-mite, mycorrhiza, actinobacteria, earthworm, root-tip | not generated | | | | **blocked** |

Generation stopped with `402 Insufficient credit` on the Replicate account. Before that, the account was held to
6 predictions a minute (Replicate's limit when credit is under $5).

## Processing applied to every accepted part

1. Rendered at the exact print size it is used at (icons 0.6 in and the size steps below it, chest bacteria 1.7 in).
2. White paper dropped, only dark pixels kept, so each part becomes one flat ink (the nearest-ink remap is
   exact: every part has one fill color, chosen per garment).
3. Every feature thinner than 0.5 pt (2.08 px at 300 dpi) thickened to 0.5 pt; thicker lines are untouched.
4. Traced back to vector (potrace) so the source SVGs contain no raster.
