"""World Teachers' Day: the grid slide (slide 9) with the same fourteen mentors in different orders, to compare.

python3 templates/posts/october/build_teachers_day_grid_tests.py
"""
import unicodedata
from lib import Deck
from build_oct_01_10 import save
from build_teachers_day_options import MENTORS, CREAM, NOTE, bunting, faces

BY = {m[0]: m for m in MENTORS}
ORDERS = {
    "A alphabetical (current)": sorted(MENTORS, key=lambda m: unicodedata.normalize("NFD", m[1].split()[-1] if m[0] == "Carla" else m[1])),
    # close-up faces and wide outdoor shots alternate, so no two field photos sit side by side
    "B close-ups and field shots alternate": ["Carla", "Ib", "Isadora", "Gerald", "Loida", "Wesley", "Elena", "Tommy",
                                              "Brian", "Dora", "Delvin", "Ayşen", "Nick", "Casey"],
    # smiling faces at the corners and edges, the quieter photos in the middle
    "C smiles on the outside": ["Casey", "Ib", "Elena", "Isadora", "Gerald", "Tommy", "Loida", "Carla", "Dora",
                                "Wesley", "Delvin", "Ayşen", "Brian", "Nick"],
}

d = Deck(name="05-10-2026-mon-ig-teachers-day-grid-tests")
IB_AT = 8   # Linnea, 5 Oct 2026: Ib not in the top row; third photo of the third row (cell 10 = index 8)
for name, order in ORDERS.items():
    people = [BY[x] if isinstance(x, str) else x for x in order]
    j = next(k for k, p in enumerate(people) if p[0] == "Ib")
    people[j], people[IB_AT] = people[IB_AT], people[j]
    assert len(people) == 14 and len({p[0] for p in people}) == 14
    s = d.slide(CREAM, f"Grid test {name}." + NOTE, counter=False)
    bunting(s, y=20, n=11)
    faces(s, 185, people=people, with_logo=True)
save(d, "05-10-2026-mon-ig-teachers-day-grid-tests.pptx")
