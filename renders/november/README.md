# Dr. Elaine Ingham series (How to Build Great Soil, Part 1): renders

Built by `templates/posts/november/build_elaine_series.py` (all 15 posts; the 3 and 5 December posts render to
`renders/december/`). One folder of slide PNGs per post plus a `-contact.png` sheet.

Reel caption cards (21 Nov oxygen gauge) have no background in the PPTX, so they can be laid over footage;
the renders here come from the Deep Green preview copy (`python3 build_elaine_series.py reel_oxygen --preview`,
then render `renders/.tmp/preview/november/...`) so the text is readable. The PPTX itself stays transparent.

Placeholders still open (from the library search):
- Flagellate micrograph (2 Nov slide 5; 23 Nov grid). None in assets/microscopy/.
- Bacteria micrograph (23 Nov grid; 11 Nov story frame 2, a bacteria-rich field).
- Fungal hyphae micrograph (23 Nov grid; 7 Nov slide 6 uses the collage cutout instead).
- Recommended microscope photo (23 Nov slide 3, from Wes).
- 5 Nov LinkedIn uses sfw-amoeba-still-wide.jpg (amoebae, no hyphae in the same field).
