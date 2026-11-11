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

## Design 1, POWERED BY PROTOZOA: Colpoda drawn in code

Replicate still returned `402 Insufficient credit`, so the Colpoda was drawn in code
(`tools/design1_powered_by_protozoa.py`), not generated. Anatomy drawn: kidney-shaped cell, oral vestibulum as a
cross-hatched pocket on the concave side lined with oral cilia, 360 somatic cilia with a metachronal wave,
17 kineties as dotted rows of basal bodies, stippled macronucleus with micronucleus, double-ruled contractile vacuole
at the posterior end, 9 hatched food vacuoles (3 holding a bacterium being digested), engraver's hatching and
cross-hatching on the shaded side. Four rod bacteria trail into the mouth. No flagella on the ciliate.
Not yet checked against a Wikimedia Commons reference photo.

Revisions after looking at the preview: cilia cut from 520 to 360 and lengthened (they read as fur); oral groove
changed from a hard triangle to a rounded pocket; bacteria moved from a far corner to a trail into the mouth.
Checks: finest line 2.9 px (0.5 pt = 2.08 px); ciliate 9.0 x 7.9 in; text block 9.0 in wide; logo space
1.4 x 1.4 in kept clear under the slide label (coordinates in the SVG comment).

## All organisms now drawn in code (user's choice, Replicate out of credit)

`tools/organisms.py` draws every organism as engraved vector line art: Colpoda, Bodo flagellate, Actinophrys
heliozoan, lobose amoeba, Arcella, Rhabditid nematode (no stylet), earthworm with clitellum, oribatid mite,
mite leg, septate hyphae, aseptate AM hyphae with spores, arbuscule, Streptomyces with spore spirals, root tip,
rod bacteria, cocci colonies, stipple soil crumbs. Every line is at least 2.5 px at 300 dpi (0.5 pt = 2.08 px).
Typography is the priority in every layout; organisms support the words.
