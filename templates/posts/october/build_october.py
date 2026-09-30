"""Builds the 9 October 2026 template masters and all 26 posts. Run: python3 build_october.py
Masters go to _templates/, posts to this folder. Also writes PHOTO-PLACEHOLDERS.md."""
import glob, os
os.chdir(os.path.dirname(os.path.abspath(__file__)))
from lib import *
import lib

MICRO = "assets/microscopy/fungal-spores-in-suspension.jpg"
AMOEBA = "assets/microscopy/sfw-amoeba-still-square.jpg"
SOIL = "assets/photo/hand-scooping-planter-bed-soil.jpg"
MULCH = "assets/photo/gloved-hands-red-bucket-mulch.jpg"
ROOTS = "assets/photo/hand-soil-roots-fungi.jpg"
GROUP = "assets/photo/workshop-group-around-compost-pile.jpg"
TREE = "assets/photo/erc-rancho-cacachilas-agro2.jpg"
WORM = "assets/photo/hand-wet-dirt-worm.jpg"
C = TAG

MENTORS = [("Dr. Carla Portugal", "Science Leader"), ("Nick Padwick", "Farmer, Norfolk"), ("Wes Sander", "Microscopy"),
           ("Gerald Ramirez", "Compost extracts and teas"), ("Dr. Caterina Capri", "Advanced Programs")]

def deck(name, w=1080, h=1350): return Deck(w, h, name)

# ============================================================ masters
def masters():
    out = "_templates/"
    d = deck("1-soil-regenerators"); 
    t1a(d, "Graduate photo", "Graduate Name", "Town, Country"); t1b(d, f"{C} Short quote from the graduate.", f"{C} Name, Place")
    t1c(d, "What the slide shows", "LABEL IN CAPS", f"{C} One line for the slide, three lines at most."); t1d(d, "LABEL IN CAPS", f"{C} One line, no photo.")
    t1e(d, f"{C} Closing quote.", f"{C} Name", f"Follow {C} handle"); d.finish(out + "1-soil-regenerators-in-the-wild.pptx")
    d = deck("2-did-you-know")
    t2a(d, MICRO, "DID YOU KNOW", f"{C} Headline, four lines at most.", f"{C} Small line."); t2b(d, 1, f"{C} One step, five lines at most."); t2b(d, 2, f"{C} One step with an image.", img=MICRO)
    t2c(d, f"{C} A question."); t2d(d, f"{C} Takeaway line.", extra=f"{C} Optional second line."); d.finish(out + "2-did-you-know-myth-buster.pptx")
    d = deck("3-checklist")
    t3a(d, f"{C} Headline.", ["item 1", "item 2", "item 3", "item 4"]); t3b(d, f"{C} Item name", f"{C} One or two lines.", ("check",), "item")
    t3b(d, f"{C} Item name", f"{C} One or two lines.", ("warn",), "item"); t3c(d, "HOW", [f"{C} Step one", f"{C} Step two", f"{C} Step three"]); d.finish(out + "3-checklist-yes-no.pptx")
    d = deck("4-mentor")
    t4a(d, "Mentor photo", "Mentor Name", "Role"); t4b(d, f"{C} Headline."); t4c(d, "Mentor photo", "Mentor Name", "Role")
    t4c(d, None, "Mentor One", "Role", duo=["Mentor one", "Mentor two"], name2="Mentor Two", role2="Role")
    t4c(d, "Mentor photo", "Mentor Name", "Role", quote=f"{C} Quote.”"); d.finish(out + "4-mentor.pptx")
    d = deck("5-big-number"); t5(d, "000", f"{C} units", f"{C} One line of context."); t5(d, None, None, "", bars=[("120", "Year one", 480, GREEN), ("135+", "Year two", 540, DEEP)]); d.finish(out + "5-big-number.pptx")
    d = deck("6-reel", 1080, 1920)
    t6a(d, "Cover photo", f"{C} Title", series=True); t6a(d, None, f"{C} Title", split=["left image", "right image"]); t6a(d, "circle image", f"{C} Title", circle=True); t6b(d, f"{C} Caption line.")
    d.finish(out + "6-reel-cover-and-caption-cards.pptx", counters=False)
    d = deck("7-story", 1080, 1920); t7(d, AMOEBA, f"{C} Headline", f"{C} Line"); d.finish(out + "7-instagram-story.pptx", counters=False)
    d = deck("8-donate"); t4c(d, "Recipient photo", f"{C} Name from Country studies with us on a scholarship.", None, lab="SCHOLARSHIP RECIPIENT")
    t1c(d, "photo", "LABEL", f"{C} One line."); t8_donate(d, "Your donations make this possible."); d.finish(out + "8-donate.pptx")
    d = deck("9-linkedin", 1200, 627); t9(d, "Photo"); d.finish(out + "9-linkedin-photo.pptx", counters=False)

# ============================================================ posts
def P(name, fn, w=1080, h=1350, counters=True):
    d = deck(name, w, h); fn(d); d.finish(name + ".pptx", counters)

def boubacar(d):
    who = "Boubacar Tidiane Diallo, Guinea"
    t1a(d, "Boubacar among his coffee plants", "Boubacar Tidiane Diallo", "Guinea")
    t1b(d, "“Today, I ask a different question: What does the soil food web need to thrive?”", who)
    t1c(d, "his compost or mulched soil", "HOW HE FEEDS HIS SOIL", "Compost, vermicompost, activated biochar, permanent mulch, cover crops.")
    t1c(d, "coffee between cacao and banana", "WHAT HE GROWS TOGETHER", "Coffee, cacao, bananas, citrus, pineapple.")
    t1c(d, "earthworms in his soil", "WHAT CHANGED", "More earthworms, better soil structure, better moisture, stronger young plants.")
    t1e(d, "“I am cultivating the life that makes healthy agriculture possible.”", "Boubacar Tidiane Diallo", "Follow @boubacartidianediallo on YouTube")

def coffee(d):
    t2a(d, "wet coffee grounds on soil", "DID YOU KNOW", "Coffee grounds make your soil acidic.", "Mostly wrong. Here is the chemistry.", strike=True, note="Cover: Glow strikethrough marks it as a myth.")
    t2b(d, 1, "Hot water pulls most of the acid into your cup. Used grounds are close to neutral.")
    t2b(d, 2, "What stays in the grounds: nitrogen, plus leftover caffeine and tannins.")
    t2b(d, 3, "Caffeine is the coffee plant's own pesticide. It protects young leaves from insects and snails.")
    t2b(d, 4, "So fresh grounds spread on soil can slow seedlings down.")
    t2b(d, 5, "Compost flips it. Soil bacteria break down caffeine. One strain, found in a university flower bed, lives on caffeine alone.", img=MICRO, note="Microscopy image: soil sample with bacterial rods (general).")
    t2d(d, "Grounds go in the compost first, mixed with leaves or cardboard. Then onto the garden.")

def underwear(d):
    t3a(d, "Bury a pair of cotton underwear. Dig it up in 60 days.", ["clean white cotton brief next to a shovel"])
    t3c(d, "HOW", ["100% cotton, white", "Buried 15 cm deep", "Mark the spot"])
    t3b(d, "Almost gone?", "Your soil is full of life eating it.", ("check",), "tattered brief after two months")
    t3b(d, "Still whole?", "Your soil needs food for its microbes. Start with compost.", ("note",), "brief still whole after 60 days")

def cards(d):
    t4b(d, "Happy World Teachers' Day. Collect them all.")
    for n, r in MENTORS: t4a(d, f"{n}, square headshot", n, r)
    t4b(d, "Thank you to every mentor who teaches our students to see soil.")

def habitat(d): t7(d, AMOEBA, "The biggest habitat on Earth is under your feet.", "More than half of all species live in soil.", note="Leave y=1100 to 1450 empty for the poll sticker.")

def carla(d): t4c(d, "Carla at a microscope", "Dr. Carla Portugal", "Science Leader", quote="The mentors, especially Carla Portugal.”")

def nick(d):
    t4c(d, "Nick with compost windrows", "Nick Padwick", "Norfolk, England")
    t5(d, "750", "tons of compost a year", "40 years of farming in the UK, Italy, Spain and Argentina.")

def wes_reel(d):
    t6a(d, None, "Spot the difference", split=["microscopy of soil from a conventional field", "microscopy of biologically active compost"])
    for l in ("Soil from a conventional field.", "Biologically active compost.", "Same microscope. Same magnification.", "Meet Wes Sander, our microscopy mentor."): t6b(d, l)

def gc(d):
    t4c(d, None, "Gerald Ramirez", "Compost extracts and teas", duo=["Gerald Ramirez, portrait", "Dr. Caterina Capri, portrait"], name2="Dr. Caterina Capri", role2="Advanced Programs")
    t2b(d, None, "Gerald teaches liquid amendments: compost extracts and teas that carry living biology from compost out to the field.", extra=[f"{C} Step 1", f"{C} Step 2", f"{C} Step 3"], img="assets/mentors-teachers-day/gerald-teaching.jpg", note="Small image: Gerald teaching (other people in frame: check consent).")
    t2b(d, None, "Caterina co-wrote research on how living cover crops protect soil, control weeds and build biological diversity.")

def lisa(d):
    t1a(d, "Lisa with her seedlings", "Lisa Price", "Australia")
    t1b(d, "“I have been busy inoculating home gardeners one seedling at a time.”", "Lisa Price, Australia")
    t1c(d, "seedling trays", "WHAT SHE GROWS", "Vegetable, herb and flower seedlings.")
    t1d(d, "HER POTTING MIX", "Grown in her own potting mix, made from her compost and full of beneficial microbes.")
    t1d(d, "WHAT SHE TEACHES", "She teaches every customer to grow their own food with the soil food web.")
    t1e(d, None, None, f"{C} business name and handle", lead="Find Lisa's seedlings at")

def julia(d):
    t6a(d, "Julia opening her worm bin", "Julia's worm bin", series=True)
    for l in ("Where Julia lives, green waste gets trucked away.", "So she makes her own vermicompost.", "Start your own: a box, damp cardboard, red wigglers, kitchen scraps."): t6b(d, l)

def michael(d):
    t2a(d, "Michael's family garden", "WORLD FOOD DAY", "Your food is only as nutritious as your soil is alive.")
    for i, tp in enumerate(["nutrient density in food", "bare soil over winter", "how organic food is marketed and priced", "insect damage on organic produce", "composting rules"], 1):
        t2c(d, f"{C} Question {i}: {tp}")
    t1b(d, "“For these questions and many more I found the answers while studying at the SFW school.”", "Michael Evrard, Germany")

def compost(d):
    t3a(d, "You can compost your hair. You probably shouldn't compost that ‘compostable’ fork.", ["hair", "cardboard", "eggshells", "‘compostable’ fork"])
    items = [("Hair and pet fur", "Pure protein. Adds nitrogen, breaks down slowly.", ("check",)),
             ("Cardboard and egg cartons", "Great carbon. Tear off plastic tape and shred it first.", ("check",)),
             ("Eggshells", "Same mineral as chalk. Crush them fine.", ("check",)),
             ("Paper tea bags", "Silky mesh bags are plastic and stay in soil for years.", ("check", "warn")),
             ("“Plant-based” tea bags and cutlery", "Most are PLA. It needs industrial heat above 60°C to break down.", ("warn",)),
             ("Cat litter", "Wood, paper, wheat and corn litters break down. Clay and silica never do. Keep anything with cat poop far from food gardens.", ("warn",)),
             ("Cotton and wool scraps", "Polyester sheds microplastics.", ("check",)),
             ("Dryer lint", "Only from natural fabrics.", ("check",)),
             ("Natural wine corks", "Real cork is tree bark. Chop it up.", ("check",))]
    for n, e, v in items: t3b(d, n, e, v, f"{n.lower()}, top-down on cream")

def elena(d):
    t1a(d, "the HealTerra team", "Elena Lininger", "HealTerra, Southern Oregon")
    t1d(d, "WHAT HAPPENS THERE", "Food waste goes in, living compost comes out.")
    t1c(d, "worm castings in hand", "WORM DIGESTER", "Compost and worm castings from a worm digester.")
    t1d(d, "HEALTERRA", "Part of a nonprofit that runs outdoor programs for veterans.")
    t1d(d, "WITH SFW GRADUATES", "A compost extractor built by SFW graduates, and biological testing with another graduate.")
    t1e(d, None, None, "Follow @healterra_org")

def courses(d):
    t2a(d, GROUP, "FOUNDATION COURSES", "Every graduate you met this month started with the same course.")
    for n in ("Boubacar, Guinea.", "Christina, Tennessee.", "Jason, Indiana."): t1c(d, n.split(",")[0] + ", small portrait", "GRADUATE", n)
    t2d(d, "The Foundation Courses. Learn soil biology, compost, extracts and microscopy.", extra="Scholarships available.")

def scholarship(d):
    t4c(d, "the recipient at their work", f"{C} Name from Country studies with us on a scholarship.", None, lab="SCHOLARSHIP RECIPIENT")
    t1c(d, "their land or work", "THEIR WORK", f"{C} What their land or work looks like.")
    t1c(d, "their plans", "WHAT NEXT", f"{C} What they want to do with what they learn.")
    t8_donate(d, "Your donations make this possible.")

def christina_reel(d):
    t6a(d, "Christina in the field", "Christina Olivero, Chattanooga", series=True)
    for l in ("Four years ago I worked in advertising.", "Then I joined one free webinar about protozoa.", "I had exactly zero clue what was happening. But I knew it was important.", "Today I run my own soil regeneration business."): t6b(d, l)

def carbon(d):
    t2a(d, SOIL, "CARBON", "3 ways to keep carbon in your soil. No lab needed.")
    t2b(d, 1, "Keep it covered. Bare soil loses carbon to sun, wind and rain. Mulch or plant it.", img=MULCH)
    t2b(d, 2, "Keep roots in the ground. Living roots feed carbon to fungi and bacteria all year.", img=ROOTS)
    t2b(d, 3, "Dig less. Every turn of the soil breaks up the fungal networks that hold carbon in place.", img="microscopy: fungal strands")
    t2d(d, "Soil holds more carbon than the air and all the world's plants combined.")

def jason(d):
    t1a(d, "Jason at his compost piles", "Jason Gearheart", "Integrated Elements Compost, Indiana")
    t5(d, None, None, "", bars=[("120", "Year one, yards", 480, GREEN), ("135+", "Year two, yards", 540, DEEP)])
    t1c(d, "woodchips next to finished compost", "WOODCHIPS IN", "Woodchips in. Biologically active compost out.")
    t1b(d, "“Every year I’ve been able to knock out a piece of the puzzle for efficiency without compromising quality.”", "Jason Gearheart, Indiana")

def angela(d):
    t1a(d, "Angela with a school group at the microscope, faces hidden", "Angela Viner", "Australia")
    t1d(d, "WHAT KIDS SHOUT", None, big="SOIL IS ALIVE!", sub="What kids shout when they get home from Angela's farm.")
    t1c(d, "her book in the garden", "SCHOOL GROUPS", "Hundreds of school groups. One microscope. A book about the organisms in the soil.")

def turns1(d):
    t2a(d, GROUP, "OUR FIRST YEAR", "We turned 1!", gold_rule=True)
    t5(d, ("[N]", f"{C} number"), "scholarships awarded", "")
    t5(d, ("[N]", f"{C} number"), "countries with students", "")
    t5(d, ("[N]", f"{C} milestone 3"), f"{C} milestone", "")
    t8_donate(d, "Year two: more scholarships, more countries, more living soil.")

def vampire(d):
    t6a(d, "vampire amoeba, microscopy (from Wes's blog)", "Happy Halloween from the soil", circle=True)
    for l in ("Meet the vampire amoeba.", "It punches a hole in its prey's cell wall...", "...and drains it from the inside.", "Read Wes's full blog.", "Link in bio."): t6b(d, l)

def li(desc):
    def f(d): t9(d, desc)
    return f

def li_wes(d): t9_wes(d, "microscopy: conventional field", "microscopy: biologically active compost")

POSTS = [
    ("2026-10-01-thu-ig-boubacar", boubacar, {}), ("2026-10-01-thu-ig-coffee-myth", coffee, {}), ("2026-10-04-sun-ig-underwear-test", underwear, {}),
    ("2026-10-05-mon-ig-teachers-day-trading-cards", cards, {}), ("2026-10-05-mon-ig-story-habitat-day", habitat, dict(h=1920, counters=False)),
    ("2026-10-06-tue-ig-mentor-carla", carla, {}), ("2026-10-07-wed-ig-mentor-nick", nick, {}),
    ("2026-10-08-thu-ig-reel-wes", wes_reel, dict(h=1920, counters=False)), ("2026-10-09-fri-ig-mentor-gerald-caterina", gc, {}),
    ("2026-10-10-sat-ig-lisa-price", lisa, {}), ("2026-10-14-wed-ig-reel-julia", julia, dict(h=1920, counters=False)),
    ("2026-10-16-fri-ig-world-food-day-michael", michael, {}), ("2026-10-17-sat-ig-can-this-go-in-my-compost", compost, {}),
    ("2026-10-19-mon-ig-elena-healterra", elena, {}), ("2026-10-20-tue-ig-foundation-courses", courses, {}),
    ("2026-10-21-wed-ig-scholarship-recipient", scholarship, {}), ("2026-10-23-fri-ig-reel-christina", christina_reel, dict(h=1920, counters=False)),
    ("2026-10-24-sat-ig-carbon-3-ways", carbon, {}), ("2026-10-26-mon-ig-jason", jason, {}), ("2026-10-28-wed-ig-angela", angela, {}),
    ("2026-10-29-thu-ig-foundation-turns-1", turns1, {}), ("2026-10-31-sat-ig-reel-vampire-amoeba", vampire, dict(h=1920, counters=False)),
    ("2026-10-01-thu-li-boubacar", li("wide shot of the syntropic system at Gnaly: coffee between banana, cacao and citrus, mulched soil visible"), dict(w=1200, h=627, counters=False)),
    ("2026-10-08-thu-li-wes", li_wes, dict(w=1080, h=1080, counters=False)),
    ("2026-10-16-fri-li-michael", li("Michael's family garden"), dict(w=1200, h=627, counters=False)),
    ("2026-10-23-fri-li-christina", li("Christina teaching a workshop or running a soil test"), dict(w=1200, h=627, counters=False)),
    ("2026-10-26-mon-li-jason", li("Jason at his facility, windrows and bagged compost in the same shot"), dict(w=1200, h=627, counters=False)),
]

if __name__ == "__main__":
    for f in glob.glob("*.pptx") + glob.glob("_templates/*.pptx"): os.remove(f)
    masters()
    for name, fn, kw in POSTS: P(name, fn, **kw)
    lib.REGISTRY.sort()
    with open("PHOTO-PLACEHOLDERS.md", "w") as f:
        f.write("# PHOTO placeholders to fill, October 2026\n\nGenerated by build_october.py. Masters in _templates/ are excluded.\n\n")
        cur = None
        for deckname, n, label in lib.REGISTRY:
            if deckname.startswith(("1-", "2-", "3-", "4-", "5-", "6-", "7-", "8-", "9-")): continue
            if deckname != cur: f.write(f"\n## {deckname}\n"); cur = deckname
            f.write(f"- Slide {n}: {label}\n")
    print(len(POSTS), "posts,", len(glob.glob('_templates/*.pptx')), "masters")
