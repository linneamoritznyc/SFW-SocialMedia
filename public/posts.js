/* Every drafted post, September to December 2026.

   Captions are the house voice: short declaratives, the mechanism said plainly,
   the figure that disappoints kept in, one call to action, five to eight
   hashtags from the approved bank. No em dashes, no "certified", no course
   acronyms in public copy, no percentage without a named source.

   Copy comes from drafts/ and the captions.md files. Nothing here is invented.
   Where a post is not written yet, it says so and says what it needs. */

const POSTS = [

{
  id: "myth-1",
  title: "Myth 1: beans feed your tomatoes",
  pillar: "Science Explained",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 28 September",
  status: "ready",
  intro: "The most repeated piece of advice in home gardening, and it runs the wrong way round. First of four myth posts in the quarter.",
  images: [{ src: "img/templates/myth.png", label: "Myth card" }],
  planner: { ctaWords: "Save this for next spring, when the companion planting charts come back round.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Plant beans next to your tomatoes and they will feed them. It is the most repeated piece of advice in home gardening and it has the timing exactly backwards.",
    "Legumes do fix nitrogen. Rhizobium bacteria infect the root hairs and build nodules, and inside those nodules the bacteria convert nitrogen gas into a form a plant can use. Mycorrhizal fungi need to be in the partnership for it to work properly.",
    "But the bean is paying for that nitrogen with sugars, and it keeps what it pays for. Very little of it leaves while the plant is alive.",
    "It reaches the rest of the bed once the bean dies and decomposes, and even then it does not travel straight into a tomato root. Bacteria and fungi break the residue down and hold the nitrogen in their own bodies. Protozoa and nematodes graze on them and release the surplus at the root, in the form a plant can take up. Several organisms are involved in the delivery, and between them they run on a season rather than a summer.",
    "So grow the legume, then feed the bed with it. Chop it in at the end of the season, leave the roots in the ground, and let this year's beans feed next year's tomatoes.",
    "Save this for next spring, when the companion planting charts come back round."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","SoilHealth","RegenerativeAgriculture","GardenSoil","Mycorrhizae"] }],
  checks: ["Mechanism cited to Ingham et al. 1985 and the USDA Soil Biology Primer 1999, both on the card."],
  draft: "drafts/2026-09-17-myth-beans-feed-tomatoes.md"
},

{
  id: "failed-piles",
  title: "The most is learned from failed piles",
  pillar: "Science Explained",
  platform: "Instagram",
  format: "Quote card",
  slot: "Friday 2 October",
  status: "review",
  statusNote: "The meeting notes paraphrase Loide. Get her exact words before setting them in ninety-two point type inside quotation marks.",
  intro: "Loide Vasquez, Advanced Program Lead, first employee. Six words, and they are the thesis of the whole Field Notes series. Runs two weeks before Field Notes starts.",
  images: [{ src: "img/quotes/failed-piles.png", label: "Quote card" }],
  planner: { ctaWords: "Field Notes starts in two weeks.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "\"The most is learned from failed piles.\"",
    "Loide said that. She has been here since February 2019 and leads our advanced programme, and she was talking about compost. She is right about compost, and she is also describing the only honest way to teach anything.",
    "A pile that goes anaerobic tells you what your materials were actually doing. A pile that never heats tells you what your ratio really was. A pile that works tells you very little, because you never find out which of the things you did was the one that mattered.",
    "In two weeks we start publishing what our graduates found in their own field trials. Several of those trials did not go the way anyone hoped, and those are the ones we are most interested in.",
    "Field Notes starts in two weeks."
  ], tags: ["SoilFoodWeb","LivingSoil","Compost","SoilBiology","SoilHealth"] }],
  checks: ["Ask Loide for her exact words. A paraphrase in quotation marks at that size is a quote we did not verify."],
  draft: "drafts/2026-09-24-failed-piles.md"
},

{
  id: "india-ryss",
  title: "India: Vijay Kumar and RYSS",
  pillar: "The Bigger Picture",
  platform: "Instagram",
  format: "Single image or carousel",
  slot: "Monday 5 October",
  status: "blocked",
  statusNote: "The farmer figure has no source yet, and RYSS have to read the copy before it runs. A post about someone's work, in their grid, that they have not seen, is the one way this goes wrong.",
  intro: "Their work, at a scale nothing in our own record comes close to. Collab post: Evan or Kavi sends it.",
  images: [],
  needs: "No artwork. Needs a photograph RYSS are happy for us to use, or a text card. Do not use a stock field image.",
  planner: { ctaWords: "Tell us where you are working.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Across India, farmers have moved off conventional commodity cropping onto food forests and agroforestry, and they grow their own biofertilizers to do it. [SLOT: the number, with a source and a year, before this runs.]",
    "That is Vijay Kumar's work, with RYSS, at a scale worth knowing about on its own terms.",
    "What we can add is the biology of making your own. A bought amendment is a dose. You apply it, it gets used up, you buy it again. Organisms you grow yourself are a population: put them into living soil and they feed, reproduce, and carry on working after you have stopped.",
    "Which is also why it holds up where buying a product does not, when the supplier is far away and the money is not there.",
    "We are in India this month, teaching a workshop near Coimbatore.",
    "Tell us where you are working."
  ], tags: ["SoilFoodWeb","LivingSoil","NaturalFarming","SoilHealth","RegenerativeAgriculture","FoodSecurity"] }],
  checks: [
    "Fill the farmer figure from a named source with a year, or cut the sentence.",
    "RYSS see the copy first, per sop/collab-posts.md."
  ],
  draft: "drafts/2026-10-02-india-ryss-vijay-kumar.md"
},

{
  id: "india-1",
  title: "India: four events",
  pillar: "Events and Programs",
  platform: "Instagram",
  format: "Carousel, five slides",
  slot: "Wednesday 7 October",
  status: "blocked",
  statusNote: "Three of the four events are placeholders until confirmed, and the dates disagree across our own materials. If a name is unconfirmed, the face comes off the graphic.",
  intro: "Co-hosted with Isha Outreach. The only card with real details on it is the workshop.",
  images: [
    { src: "img/india/post1-slide-1.png", label: "1. The collage" },
    { src: "img/india/post1-slide-2.png", label: "2. The workshop" },
    { src: "img/india/post1-slide-3.png", label: "3. The lecture" },
    { src: "img/india/post1-slide-4.png", label: "4. Panel and seminar" },
    { src: "img/india/post1-slide-5.png", label: "5. The open question" }
  ],
  planner: { ctaWords: "", ctaLink: null, canva: "" },
  captions: [
    { name: "Instagram caption", recommended: true, body: [
      "We are coming to India in October.",
      "Four events across the country. A lecture, a panel, a seminar, and a workshop, with people who have spent their careers on natural farming and soil policy.",
      "India has more Soil Regenerators than we have events to hold, and most of them have never met each other in person. We are going partly to teach and mostly to get them in one room.",
      "If you are going, say so in the comments and tell us where you are coming from. We would like to know who will be there before we arrive."
    ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","NaturalFarming","SaveSoil","RegenerativeAgriculture","SoilBiology"] },
    { name: "The Save Soil line", note: "Tag Isha Outreach. Caption or first comment.", body: [
      "Co-hosted with Isha Outreach, whose Conscious Planet: Save Soil campaign is where a lot of you are arriving from. You already know soil matters. We are the ones with the microscope."
    ], tags: [] }
  ],
  checks: [
    "The line about delegates coming from organisations leading this work globally has been cut. It was a claim about who is attending and the delegate list is not confirmed.",
    "Soil Food Web spelled out. No initials in public copy.",
    "No exclamation marks, no percentages."
  ],
  draft: "drafts/2026-10-16-india-four-events.md"
},

{
  id: "microbe-1",
  title: "Favourite microbe 1: Sammie, tardigrades",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 9 October",
  status: "blocked",
  statusNote: "We hold no tardigrade image. Post 1 cannot run without one, and a diagram is not a post.",
  intro: "We asked everyone their favourite microbe at the all-team meeting as an icebreaker. It turned into a territorial dispute. Ten people, ten microbes, over ten weeks.",
  images: [],
  needs: "A tardigrade at 400x, our own. Nothing in the library matches. This is the first thing to put on a microscope.",
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Microscopy","SoilMicrobiome","SoilHealth"] }],
  checks: ["Ten named a microbe, not thirteen. Loide and Elena have not answered yet and are asked in the request email."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "india-return-to-earth",
  title: "India: Return to Earth",
  pillar: "The Bigger Picture",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 12 October, if cleared",
  status: "blocked",
  statusNote: "Not cleared. Comes out of the calendar entirely if it is not agreed, and Before Soil Food Web 1 moves up.",
  intro: "Pencilled only. Nothing is written into the schedule that has not been agreed by the people it is about.",
  images: [],
  needs: "Nothing made, and nothing should be made until this is cleared.",
  planner: { ctaWords: "See drafts/2026-10-12-india-return-to-earth.md for what is known.", ctaLink: "school.soilfoodweb.com. Blocked with the rest of this post.", canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "No caption yet, on purpose.",
    "This post is about someone else's project and it has not been agreed. Writing the copy first makes it harder to drop, and it should stay easy to drop.",
    "See drafts/2026-10-12-india-return-to-earth.md for what is known."
  ], tags: [] }],
  checks: ["Clear it or cut it. If it is not cleared by the start of October, move Before Soil Food Web 1 into this slot."],
  draft: "drafts/2026-10-12-india-return-to-earth.md"
},

{
  id: "india-five-scholars",
  title: "India: five scholars",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Carousel",
  slot: "Wednesday 14 October",
  status: "needs-consent",
  statusNote: "Five names, five faces, five quotes, none of them confirmed. Consent first, then the graphic.",
  intro: "Five people travelling to the Coimbatore workshop on full scholarships, taking a set of microscopes with them.",
  images: [],
  needs: "Five portraits and five one-line quotes, once consent is in. Use the scholarship slide layout.",
  planner: { ctaWords: "Follow the five.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Five people are travelling to our workshop in Coimbatore this month who could not otherwise have gone. They are going on full scholarships, and they are taking a set of microscopes with them.",
    "[SLOT: the five, by name and by where they work.]",
    "A two-week residential workshop priced for someone earning in dollars is out of reach of most of the people whose land it would change. Scholarships are how that gets fixed, and they are funded by people who give to them.",
    "[SLOT: one line from one of the five about what they intend to do with it.]",
    "Each of them will run a field trial on their own ground after this, and we will publish what they find, including the parts that disappoint.",
    "Follow the five."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","NaturalFarming","Microscopy","SaveSoil","Scholarships"] }],
  checks: ["Same consent email as the June scholarship post. Anyone who declines comes off the graphic."],
  draft: "drafts/2026-10-09-india-five-scholars.md",
  email: true
},

{
  id: "microbe-2",
  title: "Favourite microbe 2: Allison, twice beaten",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 16 October",
  status: "blocked",
  statusNote: "Depends on post 1 running first, and on an image we do not hold.",
  intro: "Runs second so the joke lands. She lost tardigrades to Sammie and her backup to Carla.",
  images: [],
  needs: "Artwork depends on which microbe Allison ends up with. Ask her before anything is made.",
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: [] }],
  checks: ["Ask Allison which microbe she ended up with."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "mycelium-shirt",
  title: "Be the mycelium you want to see in the world",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Quote card",
  slot: "Monday 19 October",
  status: "review",
  statusNote: "Asks a question about merchandise. Route the storefront question before it runs, because people will reply asking where to buy it.",
  intro: "From the phrase bank. Somebody said it at the all-team meeting and within a minute somebody else had asked for it on a shirt.",
  images: [{ src: "img/quotes/mycelium-shirt.png", label: "Quote card" }],
  planner: { ctaWords: "Would you wear it?", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Be the mycelium you want to see in the world.",
    "Somebody said it at our all-team meeting and within a minute somebody else had asked for it on a shirt.",
    "It is a joke and it is also accurate. Fungal threads run between plants, carry nutrients and water along the network, and hold soil crumbs together so the whole thing does not wash away in the first heavy rain. None of it is visible from above ground.",
    "Would you wear it?"
  ], tags: ["SoilFoodWeb","LivingSoil","Mycelium","SoilBiology","SoilHealth"] }],
  checks: ["Decide what the answer is if people ask where to buy it. There is no storefront."],
  draft: "drafts/2026-10-13-mycelium-shirt.md"
},

{
  id: "india-3",
  title: "India: who was in the room",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Daily story, plus one feed post",
  slot: "Stories 19 to 30 October. Feed post Friday 6 November",
  status: "blocked",
  statusNote: "None of this exists until the tour happens. Permission is asked in the room, on the day. Names are a separate yes from faces.",
  intro: "Rooms filling, someone at a microscope, a field visit. Then one feed post at the end that is entirely attendee photographs, with names and where they travelled from.",
  images: [
    { src: "img/india/post3-story.png", label: "Daily story" },
    { src: "img/india/post3-attendees.png", label: "Attendees feed post" }
  ],
  planner: { ctaWords: "If you are working on soil biology somewhere in the region and you were not here, tell us where you are. We would rather know before we plan the next one.", ctaLink: null, canva: "" },
  captions: [{ name: "Caption for the attendees post", recommended: true, body: [
    "This is who was in the room.",
    "[N] people, from [list the places]. Some came a few hours. One came [furthest distance].",
    "Most of them had never met another Soil Food Web practitioner in person. That was the reason for the trip, more than any of the talks were.",
    "If you are working on soil biology somewhere in the region and you were not here, tell us where you are. We would rather know before we plan the next one."
  ], tags: ["SoilFoodWeb","LivingSoil","NaturalFarming","SoilHealth","SaveSoil","SoilBiology"] }],
  checks: [
    "A raised hand in a full lecture is not consent to appear on a public account. Ask, then photograph.",
    "“Where you travelled from” is a detail people give, not one we look up.",
    "This is the post that makes the next tour easier to fill. A person deciding whether to come looks for someone like themselves in the room."
  ]
},

{
  id: "field-notes-1",
  title: "Field Notes 1: Sandra Niggemeyer",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 23 October",
  status: "needs-consent",
  statusNote: "Her written consent, and the tag handle has to come from her.",
  intro: "Van, Texas. Clay and sand, fallow twenty years, butternut squash. Three plots, one season. Pick one image and one caption.",
  imageChoice: true,
  images: [
    { src: "img/sandra/01-number-first.png",    label: "Number first" },
    { src: "img/sandra/04-field-photograph.png",label: "Field photograph" },
    { src: "img/sandra/05-quote-card.png",      label: "Quote card" },
    { src: "img/sandra/06-honest-ledger.png",   label: "Honest ledger" },
    { src: "img/sandra/07-specimen-sheet.png",  label: "Specimen sheet" },
    { src: "img/sandra/13-magazine-cover.png",  label: "Magazine cover" }
  ],
  planner: { ctaWords: "", ctaLink: null, canva: "" },
  captions: [
    { name: "Option A, the odd result", recommended: true,
      pairs: "Pairs with the honest ledger, or the data card.",
      body: [
        "Her tea plot gained one percent organic matter. It also had the fewest squash bugs.",
        "Sandra Niggemeyer ran three plots on the same Texas ground, fallow for twenty years, clay and sand. Biologically complete compost tilled into one. Teas and extracts through the season on another. Water only on the third.",
        "The compost plot gained 46 percent organic matter. The control gained 14 percent on water alone. The tea plot gained one.",
        "Then the tea plot carried the fewest squash bugs and the control carried the most. Organisms applied as extracts sit on the leaf and root surfaces that pests would otherwise get to first. That is not the same job as building soil structure, and one season on one field cannot tell you which of them did what.",
        "Her own conclusion: soil biology rebuilds the ground before it rebuilds the yield. In degraded soil, the first season is the ground.",
        "What did your first season on tired ground actually give you? Tell us below."
      ],
      tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Compost","RegenerativeFarming","SoilHealth","SoilFoodWebFoundation"] },
    { name: "Option B, the number",
      pairs: "Pairs with number first, or field photograph.",
      body: [
        "Twenty years fallow. One season of biology. 46 percent more organic matter.",
        "Sandra Niggemeyer put biologically complete compost into one plot of Texas clay and sand, teas and extracts into a second, and water only into a third.",
        "Bacteria and fungi make the glues that bind soil particles into crumbs. Fungal threads weave those crumbs into bigger ones. Protozoa and nematodes graze the bacteria and release nutrients at the root, in the form the plant can actually take up.",
        "The honest version: the control gained 14 percent on water alone, and the tea plot gained one. Harvest was 35 ounces against 19. A real difference, and a small sample.",
        "Ground that has been left alone does not need a miracle. It needs the organisms back.",
        "Save this for the next time somebody tells you degraded soil takes a decade."
      ],
      tags: ["SoilFoodWeb","LivingSoil","SoilHealth","Compost","RegenerativeAgriculture","SoilBiology"] },
    { name: "Option C, the quiet one",
      pairs: "Pairs with the quote card.",
      body: [
        "“Soil biology rebuilds the ground before it rebuilds the yield.”",
        "That is Sandra Niggemeyer's conclusion after a season of butternut squash on Texas clay and sand that had been fallow for twenty years.",
        "Three plots. Compost into one, teas and extracts into another, water only into the third. The compost plot gained 46 percent organic matter, the control 14, the tea plot one. The harvest was 35 ounces, 30 and 19.",
        "Hail killed her first planting. Rodents took the second. Johnson grass ran the beds by June. She wrote all of it down, which is why the numbers are worth anything at all.",
        "In degraded soil, she says, the first season is the ground.",
        "Follow along. Every other Thursday we publish what a field trial actually found."
      ],
      tags: ["SoilFoodWeb","LivingSoil","SoilBiology","RegenerativeFarming","SoilHealth","SoilFoodWebFoundation"] }
  ],
  checks: [
    "Every number traced back to her report, and the control figure present.",
    "No internal course acronyms. Foundation Courses, not the initials.",
    "The word “certified” does not appear.",
    "One call to action, not two."
  ],
  more: { label: "Twenty-one other directions for the same story", dir: "img/sandra-more/" }
},

{
  id: "before-sfw-1",
  title: "Before Soil Food Web 1: Gerald",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 26 October",
  status: "review",
  statusNote: "Gerald reads it first. It is his career being summarised in two sentences.",
  intro: "Almost everyone who works here arrived as a student or a practitioner. First of a series of five.",
  images: [],
  needs: "A photograph of Gerald, with his permission, or a text card. Nothing in the library.",
  planner: { ctaWords: "What were you doing before soil?", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Six years ago Gerald was a conventional agronomist, frustrated that he could not get at Dr. Elaine Ingham's teaching. He now teaches it.",
    "Almost everyone who works here arrived as a student or a practitioner first. A farmer. An agronomist. Someone managing orchards in California. A landscaper. People who were doing the work, ran into the limits of what they had been taught, and went looking for something that explained it.",
    "We mention it because the usual question about soil biology is whether the people teaching it have ever farmed anything. Most of this team did that first, and the teaching came second.",
    "What were you doing before soil?"
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","RegenerativeAgriculture","SoilBiology","CareerChange"] }],
  checks: ["Gerald approves the wording and the photograph."],
  draft: "drafts/2026-10-06-before-soil-food-web.md"
},

{
  id: "microbe-3",
  title: "Favourite microbe 3: Carla, amoebae",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 30 October",
  status: "review",
  statusNote: "We hold amoeba microscopy, so this one can actually be made. Carla checks the wording.",
  intro: "Carla referred to a kissing amoeba, and said she has to find a new one after somebody claimed hers.",
  images: [],
  needs: "Use assets/microscopy/cutout-2.png in the microbe template. Not yet built.",
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Microscopy","SoilMicrobiome","SoilHealth"] }],
  checks: ["Ask Carla what a kissing amoeba is before putting the phrase in public copy."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "office-hours",
  title: "Office hours, three times a week",
  pillar: "Events and Programs",
  platform: "Instagram reel",
  format: "Reel, 9:16",
  slot: "Monday 2 November",
  status: "blocked",
  statusNote: "Needs footage from an actual office hours call, and everyone audible or visible in it has to agree first.",
  intro: "Carla runs them. Students arrive with one specific question and stay the hour. We built a forum and a community formed in a live call instead.",
  images: [{ src: "img/motion/02-office-hours.png", label: "Motion frame" }],
  imageNote: "One frame from the animated version. The animation is in motion/02-office-hours.html and has to be screen-recorded at 1080x1920.",
  planner: { ctaWords: "Follow for what students actually ask.", ctaLink: null, canva: "" },
  captions: [{ name: "Reel caption", recommended: true, body: [
    "She came to office hours with one question and stayed the full hour. That happens three times a week, and almost nobody outside this organisation knows it exists.",
    "Carla runs them. Students in our advanced practicum can join once they have started the first part. They arrive with something specific: a ratio that looks wrong, a pile that will not heat, something at 400x they cannot name. Then they stay, because somebody else's problem turns out to be interesting too.",
    "[SLOT: one line naming what was actually asked in this clip.]",
    "We built a forum, and the community formed in a live call instead. Nobody planned that.",
    "Follow for what students actually ask."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","SoilHealth","Microscopy","RegenerativeAgriculture"] }],
  checks: [
    "Everyone audible or on screen agrees before the clip is cut, not after.",
    "Advanced practicum, spelled out. Not the initials."
  ],
  draft: "drafts/2026-10-20-office-hours-reel.md"
},

{
  id: "fall-soil-prep",
  title: "Four things to do before the frost",
  pillar: "Take Action",
  platform: "Instagram",
  format: "Single image",
  slot: "Wednesday 4 November",
  status: "review",
  statusNote: "The graduate anchor line is a placeholder. Either name a real graduate who recommended autumn compost, with her permission, or cut the line.",
  intro: "The growing season is over. The soil season is not. Four things, and why each one matters to the organisms rather than to the plants.",
  images: [{ src: "img/templates/checklist.png", label: "Checklist card" }],
  planner: { ctaWords: "Save this and work through it before your first frost.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "The growing season is over. The soil season is not.",
    "Four things worth doing between the last harvest and the first hard frost, and why each one matters to the organisms rather than to the plants.",
    "Put compost on now rather than in spring. Compost is an inoculant, not a fertiliser: what you are adding is organisms, and in autumn they get the whole cool, damp end of the year to spread, colonise residue and find their food. Ask them to establish and deliver at the same time in April and they will do both badly. [SLOT: graduate name] came out of her field trial recommending exactly this.",
    "Leave the residue. Every stalk you clear away is food removed from the bacteria and fungi whose glues and threads hold your soil in crumbs, and bare soil loses that structure to rain and to freeze and thaw.",
    "Get something living in the ground. A cover crop is for the roots rather than the cover. Living roots feed the microbial community around them right through the winter, and a mix feeds more of it than a single species will.",
    "Under snow the biology slows rather than stops, insulated and damp, still working through whatever you left it. An open winter with no snow freezes hard and dries out instead, which is the argument for mulch if you need one.",
    "Save this and work through it before your first frost."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","CoverCrops","Compost","GardenSoil","FallGardening"] }],
  checks: ["Name the graduate on the card or take the anchor line off it."],
  draft: "drafts/2026-11-03-fall-soil-prep.md"
},

{
  id: "myth-2",
  title: "Myth 2",
  pillar: "Science Explained",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 9 November",
  status: "blocked",
  statusNote: "Not written, and it should not be written yet. Nobody has chosen which myth this is.",
  intro: "The layout exists and works. The content does not.",
  images: [],
  needs: "Pick the myth first. The myth banks in the Drive folder are headed “Chat GPT top 20”, so they are a prompt list rather than a source, and nothing from them can be cited as a thing people believe.",
  planner: { ctaWords: "Myth 1 had all three. Somebody has to choose myths 2, 3 and 4 and say where each one comes from. Reuse templates/myth.html once they are chosen.", ctaLink: null, canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "No caption, on purpose.",
    "A myth post needs three things before it can be written: a myth that people demonstrably believe, a mechanism we can source, and something to do instead.",
    "Myth 1 had all three. Somebody has to choose myths 2, 3 and 4 and say where each one comes from. Reuse templates/myth.html once they are chosen."
  ], tags: [] }],
  checks: ["Choose the myth and name where the belief is documented. Not from the Chat GPT list."]
},

{
  id: "scholarships",
  title: "Scholarships, June",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Carousel, seven slides",
  slot: "Wednesday 11 November",
  status: "needs-consent",
  statusNote: "Nothing ships until every recipient whose face appears has replied yes. Anyone who declines comes out of the collage. Two figures are still unconfirmed.",
  intro: "The deck headline read “$72,000+ Full Scholarships Awarded in June alone!” That sentence has us as the subject and the recipients as the object. Reworked so the people are the subject, and the exclamation mark is gone.",
  images: [
    { src: "img/scholarships/slide-1.png", label: "1. The collage" },
    { src: "img/scholarships/slide-2.png", label: "2. Recipient" },
    { src: "img/scholarships/slide-3.png", label: "3. Recipient" },
    { src: "img/scholarships/slide-4.png", label: "4. Recipient" },
    { src: "img/scholarships/slide-5.png", label: "5. Recipient" },
    { src: "img/scholarships/slide-6.png", label: "6. Recipient" },
    { src: "img/scholarships/slide-7.png", label: "7. How the fund works" }
  ],
  planner: { ctaWords: "", ctaLink: null, canva: "" },
  captions: [
    { name: "Instagram caption", recommended: true, body: [
      "[N] people started their training in June without paying for it.",
      "They are in Kenya, India, Ethiopia, and [COUNTRY], and their scholarships came to $72,000. Some farm a few acres. Some work inside organisations doing restoration or extension work.",
      "They take the same courses as every other student, on the same terms. The only difference is who paid.",
      "The fund exists because people give to it. Scholarship-designated gifts go to student access and nothing else, and that is the whole mechanism. There is no endowment behind it and no grant. When somebody funds a seat, somebody sits in it.",
      "Swipe to meet five of them."
    ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","RegenerativeAgriculture","FoodSecurity","Agroecology","SoilFoodWebFoundation"] },
    { name: "LinkedIn version", note: "Framed toward people who might fund scholarships.", body: [
      "In June, [N] people began training in soil biology without paying for it. Their scholarships came to $72,000.",
      "They are in Kenya, India, Ethiopia and [COUNTRY]. Some farm a few acres. Some work inside organisations doing restoration or extension work. They take the same courses as every fee-paying student, on the same terms.",
      "The mechanism takes one line to describe: scholarship-designated gifts go to student access and nothing else. There is no endowment behind the fund. A funded seat is a filled seat, in the same quarter.",
      "Priority goes to applicants working in under-resourced regions, which is where the gap between what the training costs and what a grower can pay is widest.",
      "If funding technical training in soil biology is something your organisation does, the scholarship fund is the most direct route we have."
    ], tags: ["SoilHealth","RegenerativeAgriculture","Scholarships"] }
  ],
  checks: [
    "Fill [N] and [COUNTRY] from the confirmed list.",
    "The line about somebody who wrote in having no land yet has been cut. It was a placeholder for a real person and we do not have one.",
    "Pick the five across geography and starting point. The collage spans Kenya, India, Ethiopia, Latin America and Europe.",
    "The ask is on slide 7 and nowhere else. It arrives after six faces, which is the reason for the running order."
  ],
  email: true,
  draft: "drafts/2026-11-10-scholarship-numbers.md"
},

{
  id: "microbe-4",
  title: "Favourite microbe 4: Wes, a large testate amoeba",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 13 November",
  status: "review",
  statusNote: "The meeting notes record what Wes said as “cellastite”, heard rather than spelled. Ask him what he actually said before publishing a species name.",
  intro: "He likes that you can see what it has eaten inside it. We hold the microscopy for this one, so the card is already made.",
  images: [{ src: "img/templates/microbe.png", label: "Microbe card" }],
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Microscopy","SoilMicrobiome","SoilHealth"] }],
  checks: ["Confirm the species wording with Wes. Do not publish a name we heard rather than read."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "before-sfw-2",
  title: "Before Soil Food Web 2: Wes",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 16 November",
  status: "review",
  statusNote: "Wes reads it first.",
  intro: "Farmer, then our original lab tech. Sammie invited him into the webinars and the Lab Tech Program.",
  images: [],
  needs: "A photograph of Wes, with his permission.",
  planner: { ctaWords: "What were you doing before soil?", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Six years ago Gerald was a conventional agronomist, frustrated that he could not get at Dr. Elaine Ingham's teaching. He now teaches it.",
    "Almost everyone who works here arrived as a student or a practitioner first. A farmer. An agronomist. Someone managing orchards in California. A landscaper. People who were doing the work, ran into the limits of what they had been taught, and went looking for something that explained it.",
    "We mention it because the usual question about soil biology is whether the people teaching it have ever farmed anything. Most of this team did that first, and the teaching came second.",
    "What were you doing before soil?"
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","Microscopy","SoilBiology","CareerChange"] }],
  checks: ["Wes approves the wording and the photograph."],
  draft: "drafts/2026-10-06-before-soil-food-web.md"
},

{
  id: "community-4680",
  title: "4,680 people, and most have never posted",
  pillar: "Take Action",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 20 November",
  status: "blocked",
  statusNote: "Blocked on the community link having a home. Do not run a join post that points nowhere.",
  intro: "The free community. 207 people have posted. The rest read, which is what a room like this is mostly for.",
  images: [],
  needs: "A number card. The layout in variants/19-one-number.html fits it.",
  planner: { ctaWords: "Join them.", ctaLink: "The free community. Blocked: it has no link with a home yet.", canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "There are 4,680 people in our free community and most of them have never posted anything.",
    "207 have. The rest read, which is what a room like this is mostly for, and it is why it is worth joining even if you have no intention of saying anything for a year.",
    "It is free, it always has been, and it is separate from any course. People bring photographs of things they cannot identify, piles that will not heat, and results that make no sense to them. Somebody usually knows.",
    "[SLOT: the join link, once it has a home.]",
    "Join them."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","SoilBiology","RegenerativeAgriculture","GardenSoil"] }],
  checks: [
    "Both figures need a date. A membership count with no date is stale the week after it is posted.",
    "The link has to exist before this runs."
  ],
  draft: "drafts/2026-11-19-community-4680.md"
},

{
  id: "smapp",
  title: "Check our arithmetic",
  pillar: "Science Explained",
  platform: "Instagram reel",
  format: "Reel, 9:16",
  slot: "Monday 23 November",
  status: "blocked",
  statusNote: "Needs a screen capture of the real formula view. An earlier version of the artwork carried formulas that were written for the mock-up rather than taken from the software, and they have been removed.",
  intro: "Every calculation in our soil analysis software is now visible. Runs before the Field Notes series builds up, so the numbers are already trusted when the trials start landing.",
  images: [{ src: "img/motion/01-smapp-formulas.png", label: "Motion frame" }],
  imageNote: "The formula block is deliberately an empty capture slot. Fill it with a real screen recording, not a mock-up.",
  planner: { ctaWords: "Check our arithmetic.", ctaLink: "soilmapp.com. Confirm it lands on the page that shows the formulas.", canva: "" },
  captions: [{ name: "Reel caption", recommended: true, body: [
    "Most soil analysis software will not show you how it got the number. You count what you see down the microscope, you type it in, a result comes out, and you are asked to trust it.",
    "Every calculation in ours is now visible. You can follow it from your own count through to the figure it produces, and check it.",
    "That sounds like a minor feature. It is the difference between a measurement and a verdict: if you cannot see the formula you cannot argue with the result, and a number nobody can argue with is not a scientific finding, it is a reading off a box.",
    "We publish soil results from field trials and we intend to publish a great many more. Being able to check the arithmetic is what will make them worth reading.",
    "Check our arithmetic."
  ], tags: ["SoilFoodWeb","SoilBiology","Microscopy","SoilHealth","OpenScience","LivingSoil"] }],
  checks: ["Capture the real formula view. Do not recreate it in a design tool."],
  draft: "drafts/2026-10-27-smapp-transparency-reel.md"
},

{
  id: "myth-3",
  title: "Myth 3",
  pillar: "Science Explained",
  platform: "Instagram",
  format: "Single image",
  slot: "Wednesday 25 November",
  status: "blocked",
  statusNote: "Not written. Same as myth 2: nobody has chosen the myth.",
  intro: "Layout ready, content not chosen.",
  images: [],
  needs: "Pick the myth and name a source for the belief.",
  planner: { ctaWords: "No caption, on purpose. See myth 2 for what has to be decided first.", ctaLink: null, canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "No caption, on purpose. See myth 2 for what has to be decided first."
  ], tags: [] }],
  checks: ["Choose the myth and name where the belief is documented."]
},

{
  id: "field-notes-2",
  title: "Field Notes 2",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 27 November",
  status: "blocked",
  statusNote: "Not written, because we hold one field trial report and it is Sandra's.",
  intro: "The series runs every other Thursday. The second one has no trial behind it yet.",
  images: [],
  needs: "A second graduate's field trial report, and their consent. Nothing can be designed before that exists.",
  planner: { ctaWords: "Ask the advanced practicum who else finished this season and is willing to be written about. The series format and the layouts are already built, so this is a week of work once there is a report.", ctaLink: null, canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "No caption yet, and inventing one would defeat the point of the series.",
    "Field Notes publishes what a trial actually found, including the parts that disappoint. That requires a trial. We have Sandra's.",
    "Ask the advanced practicum who else finished this season and is willing to be written about. The series format and the layouts are already built, so this is a week of work once there is a report."
  ], tags: [] }],
  checks: ["Find the second trial. Everything else is ready."],
  draft: "sop/field-notes-series.md"
},

{
  id: "microbe-5",
  title: "Favourite microbe 5: Ayşen, flagellates",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 30 November",
  status: "blocked",
  statusNote: "We hold no flagellate image.",
  intro: "She loves seeing them as babies, running around. The first organisms to start the soil food web.",
  images: [],
  needs: "A flagellate at 400x, our own. Nothing in the library matches.",
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Microscopy","SoilMicrobiome","SoilHealth"] }],
  checks: ["Put a flagellate on a microscope before this is scheduled."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "spanish-course",
  title: "El Curso Intensivo de Compost, en español",
  pillar: "Events and Programs",
  platform: "Instagram",
  format: "Single image",
  slot: "Wednesday 2 December",
  status: "review",
  statusNote: "A native speaker on the team reads the Spanish before it posts. The only promotional post that week.",
  intro: "It has been available for a while and almost nobody knew, including inside the organisation.",
  images: [],
  needs: "A card in Spanish. Use the same layout as the announcement cards, with the Spanish set at the same sizes.",
  planner: { ctaWords: "Compártelo con quien lo necesite.", ctaLink: "The Compost Intensive Course in Spanish. Exact URL needed.", canva: "" },
  captions: [{ name: "Caption, in Spanish", recommended: true, body: [
    "El Curso Intensivo de Compost ya está disponible en español, con los vídeos transcritos.",
    "Enseña a producir compost biológicamente completo: no solo materia orgánica descompuesta, sino compost con los organismos vivos que el suelo necesita. Bacterias, hongos, protozoos y nematodos. La diferencia se ve al microscopio y se nota en el campo.",
    "Lo decimos ahora porque llevaba un tiempo disponible y casi nadie lo sabía. Ni siquiera dentro de la organización.",
    "Si conoces a alguien que trabaja la tierra y para quien el inglés ha sido la barrera, este es el momento de decírselo.",
    "Compártelo con quien lo necesite."
  ], tags: ["SoilFoodWeb","SueloVivo","BiologiaDelSuelo","AgriculturaRegenerativa","SaludDelSuelo","Compostaje"] }],
  checks: [
    "Compost Intensive Course, spelled out. Not the initials.",
    "Links go to school.soilfoodweb.com only."
  ],
  draft: "drafts/2026-11-26-course-in-spanish.md"
},

{
  id: "before-sfw-3",
  title: "Before Soil Food Web 3: Brian",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 4 December",
  status: "review",
  statusNote: "Brian reads it first.",
  intro: "Managing orchards in California, and in New Mexico before that.",
  images: [],
  needs: "A photograph of Brian, with his permission.",
  planner: { ctaWords: "What were you doing before soil?", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Six years ago Gerald was a conventional agronomist, frustrated that he could not get at Dr. Elaine Ingham's teaching. He now teaches it.",
    "Almost everyone who works here arrived as a student or a practitioner first. A farmer. An agronomist. Someone managing orchards in California. A landscaper. People who were doing the work, ran into the limits of what they had been taught, and went looking for something that explained it.",
    "We mention it because the usual question about soil biology is whether the people teaching it have ever farmed anything. Most of this team did that first, and the teaching came second.",
    "What were you doing before soil?"
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","RegenerativeAgriculture","SoilBiology","CareerChange"] }],
  checks: ["Brian approves the wording and the photograph."],
  draft: "drafts/2026-10-06-before-soil-food-web.md"
},

{
  id: "myth-4",
  title: "Myth 4",
  pillar: "Science Explained",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 7 December",
  status: "blocked",
  statusNote: "Not written. Same as myths 2 and 3.",
  intro: "Layout ready, content not chosen.",
  images: [],
  needs: "Pick the myth and name a source for the belief.",
  planner: { ctaWords: "No caption, on purpose. See myth 2 for what has to be decided first.", ctaLink: null, canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "No caption, on purpose. See myth 2 for what has to be decided first."
  ], tags: [] }],
  checks: ["Choose the myth and name where the belief is documented."]
},

{
  id: "portuguese-course",
  title: "O curso, em português",
  pillar: "Events and Programs",
  platform: "Instagram",
  format: "Single image",
  slot: "Wednesday 9 December",
  status: "blocked",
  statusNote: "Hold until it is actually live on the new platform. It is being republished, not newly released, and the link does not exist yet.",
  intro: "Part of the team is Brazilian. This is not a translation done from outside.",
  images: [],
  needs: "A card in Portuguese, and the live link.",
  planner: { ctaWords: "Marca alguém que precisa disto.", ctaLink: "The course in Portuguese. Blocked until it is live.", canva: "" },
  captions: [{ name: "Caption, in Portuguese", recommended: true, body: [
    "O curso está de volta, em português.",
    "Compost biologicamente completo: não apenas matéria orgânica decomposta, mas compost com os organismos que o solo precisa. Bactérias, fungos, protozoários e nematoides. A diferença aparece no microscópio e sente-se no campo.",
    "Vale dizer quem está por trás disto. Parte da nossa equipa é brasileira: de Minas Gerais, de Florianópolis, de Goiás. Não é uma tradução feita de fora. É a língua em que várias das pessoas que ensinam este método já trabalham.",
    "[SLOT: link, quando estiver no ar.]",
    "Marca alguém que precisa disto."
  ], tags: ["SoilFoodWeb","SoloVivo","BiologiaDoSolo","AgriculturaRegenerativa","SaudeDoSolo","Compostagem"] }],
  checks: [
    "A Brazilian member of the team reads it. The draft is written in European Portuguese in places and the team is Brazilian.",
    "If this slips into the week of 14 December there are two promotional posts in eight days. Move the advanced practicum post to 4 January if that happens."
  ],
  draft: "drafts/2026-12-03-course-in-portuguese.md"
},

{
  id: "microbe-6",
  title: "Favourite microbe 6: Gerald, fungi",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 11 December",
  status: "review",
  statusNote: "We hold fungal spores in suspension, which is not the same as hyphae. Decide whether that image carries the post.",
  intro: "Gerald loves a good ratio.",
  images: [],
  needs: "Fungal hyphae at 400x. We hold spores in suspension and no hyphae, which is the gap this series keeps running into.",
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Microscopy","SoilMicrobiome","SoilHealth"] }],
  checks: ["We hold no hyphae image. Either shoot one or accept the spore image with an honest caption line."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "before-sfw-4",
  title: "Before Soil Food Web 4: Matthew",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 14 December",
  status: "review",
  statusNote: "Matthew reads it first.",
  intro: "Landscaper, and a farmers association. Twenty years with microbes. Lives in Alto Paraíso de Goiás, Brazil.",
  images: [],
  needs: "A photograph of Matthew, with his permission.",
  planner: { ctaWords: "What were you doing before soil?", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Six years ago Gerald was a conventional agronomist, frustrated that he could not get at Dr. Elaine Ingham's teaching. He now teaches it.",
    "Almost everyone who works here arrived as a student or a practitioner first. A farmer. An agronomist. Someone managing orchards in California. A landscaper. People who were doing the work, ran into the limits of what they had been taught, and went looking for something that explained it.",
    "We mention it because the usual question about soil biology is whether the people teaching it have ever farmed anything. Most of this team did that first, and the teaching came second.",
    "What were you doing before soil?"
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","RegenerativeAgriculture","SoilBiology","CareerChange"] }],
  checks: [
    "Matthew approves the wording and the photograph.",
    "Permaculture certificate is his own qualification, not ours. The word “certified” stays out of anything describing our courses."
  ],
  draft: "drafts/2026-10-06-before-soil-food-web.md"
},

{
  id: "advanced-practicum",
  title: "What is behind the advanced practicum door",
  pillar: "Events and Programs",
  platform: "Instagram",
  format: "Carousel",
  slot: "Wednesday 16 December",
  status: "review",
  statusNote: "Promotional. If the Portuguese course slips from 7 December into this week, move this to 4 January.",
  intro: "Some of what we teach is only open to students in the advanced practicum. Worth explaining what sits behind that rather than letting people assume it is a paywall for its own sake.",
  images: [],
  needs: "Three cards, one per thing. The three-panel layout in variants/07-specimen-sheet.html fits.",
  planner: { ctaWords: "Everything is on the school site.", ctaLink: "school.soilfoodweb.com, the advanced practicum page. Exact URL needed.", canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Some of what we teach is only open to students in our advanced practicum. It is worth saying what sits behind that door, rather than letting people assume it is a paywall for its own sake.",
    "A mentor, with no clock running. Students get a primary mentor and access to the wider team, and the time is not metered by the hour.",
    "Office hours, three times a week, run by Carla. Students come with one question and almost nobody leaves at the fifteen minute mark.",
    "And a field trial on ground you choose. You design it, mark the plots, run it for a season, collect the data yourself and write up what you found. Supervising a piece of original research one student at a time is why that door exists at all.",
    "Then we publish what those trials found, including the seasons that went badly. Those are usually the useful ones.",
    "Everything is on the school site."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Microscopy","SoilHealth","RegenerativeAgriculture"] }],
  checks: [
    "Advanced practicum, spelled out. The internal short form does not appear in public copy.",
    "Links to school.soilfoodweb.com only."
  ],
  draft: "drafts/2026-12-10-advanced-practicum-access.md"
},

{
  id: "field-notes-3",
  title: "Field Notes 3",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 18 December",
  status: "blocked",
  statusNote: "Not written. Same as Field Notes 2: no trial behind it.",
  intro: "The third in the series, and the second one we do not have a report for.",
  images: [],
  needs: "A third graduate's field trial report, and their consent.",
  planner: { ctaWords: "A series that publishes an empty instalment to keep a cadence stops being worth following.", ctaLink: null, canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "No caption yet.",
    "If only one more trial report comes in this quarter, run it on 26 November and let this slot go to a favourite microbe post rather than running a Field Notes with nothing in it.",
    "A series that publishes an empty instalment to keep a cadence stops being worth following."
  ], tags: [] }],
  checks: ["Decide by the end of November whether there is a third trial. If not, move a microbe post into this slot."],
  draft: "sop/field-notes-series.md"
},

{
  id: "microbe-7",
  title: "Favourite microbe 7: Casey, rotifers",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Monday 21 December",
  status: "blocked",
  statusNote: "We hold no rotifer image.",
  intro: "Casey remembered late and posted it in the chat after his turn, which is worth keeping in the caption.",
  images: [],
  needs: "A rotifer at 400x, our own. Nothing in the library matches.",
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Microscopy","SoilMicrobiome","SoilHealth"] }],
  checks: ["Put a rotifer on a microscope before this is scheduled."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "guardian",
  title: "The Guardian piece",
  pillar: "The Bigger Picture",
  platform: "Instagram",
  format: "Carousel",
  slot: "Wednesday 23 December, if dated",
  status: "blocked",
  statusNote: "No publication date. Pencilled only, and it comes out of the calendar if there is still no date.",
  intro: "Nothing is written into the schedule that has not been published yet.",
  images: [],
  needs: "Nothing made, and nothing should be made until there is a publication date.",
  planner: { ctaWords: "Chase the date. If it is not confirmed by mid-December, this slot is a quiet week and that is fine.", ctaLink: null, canva: "" },
  captions: [{ name: "Not written", recommended: true, body: [
    "No caption, because there is no piece yet.",
    "When there is a date, this becomes a straightforward carousel: what was published, what it got right, and the one thing worth adding from our side.",
    "Chase the date. If it is not confirmed by mid-December, this slot is a quiet week and that is fine."
  ], tags: [] }],
  checks: ["Get the publication date or drop the slot."]
},

{
  id: "microbe-8",
  title: "Favourite microbe 8: Isadora, lichens",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Friday 1 January 2027",
  status: "blocked",
  statusNote: "We hold no lichen photograph. Nobody is reading on 31 December, so this is the one slot where a delay costs nothing.",
  intro: "Isadora says she loves all her microbes equally, and then picked lichens.",
  images: [],
  needs: "A lichen photograph, ours. A field photograph would do here; this one does not need microscopy.",
  planner: { ctaWords: "Tell us yours.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Sammie has a tardigrade as her avatar, which the rest of us took as settling it.",
    "We asked everyone their favourite microbe at the all-team meeting, as an icebreaker, and it turned into a territorial dispute. Allison wanted tardigrades. So did Lukas. Sammie had the avatar and therefore, the room decided, prior claim. She offered to share. Allison's backup had already been taken by Carla.",
    "Tardigrades are not really soil microbes in the sense the rest of this series is about. They are micro-animals. They live in the film of water around soil particles and moss, and they survive being dried out, frozen and irradiated in a way nothing else here does. Sammie called her own pick debatable before anyone else could.",
    "Ten people, ten microbes, over the next ten weeks. Nobody outside this organisation knows we do this.",
    "Tell us yours."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Lichen","SoilMicrobiome","SoilHealth"] }],
  checks: ["Find or shoot a lichen photograph."],
  draft: "drafts/2026-10-01-favourite-microbe-series.md"
},

{
  id: "bunch-of-microbes",
  title: "Aren't we all just a bunch of microbes?",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Quote card",
  slot: "Unscheduled. Evergreen, drops into any gap",
  status: "ready",
  intro: "From the phrase bank. It closed the all-team meeting over a full-bleed field image, and it is both a joke and the actual scientific claim.",
  images: [{ src: "img/quotes/bunch-of-microbes.png", label: "Quote card" }],
  planner: { ctaWords: "Save it for the next time someone asks what you do.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "In the end, aren't we all just a bunch of microbes?",
    "Somebody said it to close our all-team meeting and everyone laughed, and then nobody could find anything wrong with it. You carry a microbial population in numbers comparable to your own cells. It breaks down what you cannot, and it holds surfaces that something worse would otherwise take. So does the top six inches of a healthy field.",
    "Save it for the next time someone asks what you do."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilBiology","SoilMicrobiome","SoilHealth","Microscopy"] }],
  checks: ["Comparable to your own cells, not ten times. The ten to one figure has been corrected in the literature and we do not repeat it."],
  draft: "drafts/2026-10-23-bunch-of-microbes.md"
},

{
  id: "india-2",
  title: "India: the science post",
  pillar: "Science Explained",
  platform: "Instagram",
  format: "Carousel, five slides",
  slot: "Unscheduled. Has to run before the tour",
  status: "review",
  statusNote: "Carla signs off the recovery order on slide 4, or slide 4 drops to “bacteria first, fungi last” with nothing in between.",
  intro: "Not about the tour. The tour is one line on the last slide. This is the post an Indian grower who has never heard of us saves.",
  images: [
    { src: "img/india/post2-slide-1.png", label: "1. Forty years" },
    { src: "img/india/post2-slide-2.png", label: "2. Flooding and tilling" },
    { src: "img/india/post2-slide-3.png", label: "3. Why fungi go first" },
    { src: "img/india/post2-slide-4.png", label: "4. The order it returns" },
    { src: "img/india/post2-slide-5.png", label: "5. Three to ten years" }
  ],
  planner: { ctaWords: "We are in India from 19 to 30 October, and the events are open.", ctaLink: null, canva: "" },
  captions: [{ name: "Instagram caption", recommended: true, body: [
    "Rice, then wheat, then rice again, for forty years. The biology does not fail all at once. It fails in an order.",
    "Flooding a field for rice does two things at the same time. Water fills the pore space and pushes the oxygen out, so the root zone sits anaerobic for weeks. Then tillage cuts the fungal network, which is made of threads, into pieces.",
    "Bacteria tolerate both. Fungi tolerate neither. They need oxygen, they grow as a physical network, and they rebuild slowly: bacteria divide in hours, a hyphal network takes seasons.",
    "Lose the fungi and you lose what they were doing. The glues and threads that hold soil crumbs together, so water soaks in instead of running off. The slow release of nitrogen that favours your crop over the fast weeds that thrive on nitrate.",
    "It comes back in an order too. Bacteria first, then the protozoa that eat them and release nitrogen at the root, then beneficial nematodes, then fungi last. Which is why the first season of recovery rarely looks like much, and why people give up in it.",
    "Left alone, that recovery takes three to ten years depending on how far the soil has gone. The alternative is to grow the missing organisms separately and put them back, which is what compost and extracts are for.",
    "We are in India from 19 to 30 October, and the events are open."
  ], tags: ["SoilFoodWeb","SoilBiology","NaturalFarming","LivingSoil","SoilHealth","Agroecology","RegenerativeAgriculture"] }],
  checks: [
    "No invented figures and no percentage anywhere.",
    "“Three to ten years” is the Foundation's own stated range for unaided recovery. It is labelled as that on the slide, not as a measured result from one site.",
    "The recovery order on slide 4 is taught in the Foundation Courses rather than cited in this repository. Needs Carla."
  ]
},

{
  id: "umass-carousel",
  title: "UMass Amherst: the future of food",
  pillar: "The Bigger Picture",
  platform: "Instagram",
  format: "Carousel, five slides",
  slot: "Unscheduled. Runs on any Monday",
  status: "blocked",
  statusNote: "Blocked on the UTM convention for the tracked link. No partnership with UMass is claimed anywhere in this post.",
  intro: "UMass Amherst announced a $120 million Future of Food Initiative, and soil cultivation is named inside the new centre's scope. We have no involvement. We are posting it because the direction is right.",
  images: [
    { src: "img/umass/slide-1.png", label: "1. $120 million" },
    { src: "img/umass/slide-2.png", label: "2. What it buys" },
    { src: "img/umass/slide-3.png", label: "3. The scope list" },
    { src: "img/umass/slide-4.png", label: "4. Then and now" },
    { src: "img/umass/slide-5.png", label: "5. 160 years" }
  ],
  planner: { ctaWords: "", ctaLink: null, canva: "" },
  captions: [
    { name: "Instagram caption", recommended: true, body: [
      "$120 million is going into the future of food, and soil made the list.",
      "UMass Amherst announced its Future of Food Initiative this month: four $30 million tranches, a new 36,000 square foot research building, five permanent endowments and a new Center for the Future of Food.",
      "Read the center's scope and one line stands out. Alongside food safety, food chemistry and processing, it names everything involving cultivation, including soil cultivation, seed effectiveness and clean water.",
      "Soil biology usually gets treated as a separate conversation from the food system. What lives in the ground decides what nutrients a plant can reach, how much water the soil holds, and how a crop handles a bad season. A food programme that skips the biology is studying the last few feet of a much longer chain.",
      "The university was built in Amherst over 160 years ago so it would sit near farms and farmers. A century and a half later, the question is back where it started.",
      "What would you want a $120 million food research program to study first? Tell us in the comments."
    ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","FoodSecurity","RegenerativeAgriculture","SoilScience","Agroecology"] },
    { name: "LinkedIn version", note: "No artwork needed. Slide 1 or 3 works as a single image.", body: [
      "UMass Amherst announced a $120 million Future of Food Initiative this month, funded in four equal parts by a private family foundation, the Commonwealth of Massachusetts, the university itself, and a $30 million target still to be raised.",
      "It buys a 36,000 square foot research building, five permanent endowments including a chair in food science, and a new Center for the Future of Food.",
      "The detail worth reading closely is the center's scope. It covers food safety, food chemistry, processing, new types of food, and everything involving food cultivation including soil cultivation, seed effectiveness and clean water.",
      "Soil biology appearing inside the scope of a major food-systems program, rather than beside it, is a shift. So is the funding model: private philanthropy, state money and institutional funds arriving together, at a moment when federal research funding is less certain.",
      "Massachusetts accounts for roughly 45% of New England's food system jobs and sales, and food and agriculture has been one of the only clusters in that region with sustained growth over the past decade. This is regional economic strategy as much as it is science.",
      "We have no involvement in this initiative. We are posting it because the direction is the right one."
    ], tags: ["SoilHealth","FoodSystems","RegenerativeAgriculture"] }
  ],
  checks: [
    "Three of the four tranches are committed. The fourth is $30 million still to be raised by the UMass Amherst Foundation. The slide says so.",
    "No partnership with UMass is claimed.",
    "The 45% figure is sourced to the UMass announcement and appears only in the LinkedIn version."
  ]
},

{
  id: "umass-story",
  title: "UMass Amherst: story frames",
  pillar: "The Bigger Picture",
  platform: "Instagram story",
  format: "Three frames, 9:16",
  slot: "Same day as the carousel",
  status: "blocked",
  statusNote: "Same link blocker. Frame 3 needs a link sticker and a poll sticker placed in the app.",
  intro: "The top 250px and bottom 280px of each frame are left clear for the app interface.",
  images: [
    { src: "img/umass/story-1.png", label: "1. $120 million" },
    { src: "img/umass/story-2.png", label: "2. Soil is on the list" },
    { src: "img/umass/story-3.png", label: "3. Sticker frame" }
  ],
  planner: { ctaWords: "Frame 3 draws the two sticker positions as dashed outlines so the layout leaves room for them. Do not export the dashed boxes into the final image.", ctaLink: null, canva: "" },
  captions: [{ name: "Stickers to place in the app", recommended: true, body: [
    "Frame 1: no stickers.",
    "Frame 2: no stickers.",
    "Frame 3: a link sticker labelled “Read the announcement”, and a poll sticker reading “Should soil biology be part of food science? Yes / It always was”.",
    "Frame 3 draws the two sticker positions as dashed outlines so the layout leaves room for them. Do not export the dashed boxes into the final image."
  ], tags: [] }],
  checks: []
},

{
  id: "wildfire-reel",
  title: "The fire went through this garden",
  pillar: "Science Explained",
  platform: "Instagram reel",
  format: "Reel, 9:16",
  slot: "Unscheduled. Any Monday once the footage is cut",
  status: "blocked",
  statusNote: "Blocked on the video file. Nothing can be cut until we have it, and the speaker has to agree to be used.",
  intro: "One garden does not prove what saved it. It is a reason to go and look at the soil, which is what we do.",
  images: [],
  needs: "The wildfire footage. ffmpeg commands for the cut are in motion/ffmpeg.md once the file exists.",
  planner: { ctaWords: "Follow for what we find in the soil.", ctaLink: null, canva: "" },
  captions: [{ name: "Reel caption", recommended: true, body: [
    "The fire went through this garden. Parts of it came back.",
    "[SLOT: one sentence of what the speaker actually says happened.]",
    "Separately from this one garden, the mechanism is worth knowing. Bacteria and fungi produce the glues that bind soil particles into crumbs, fungal threads weave those crumbs into larger ones, and soil built that way behaves like a sponge. Soil without that structure sheds water instead of taking it in, and dries out faster once the rain stops.",
    "None of which proves what saved this particular garden. It is a reason to go and look at the soil underneath it.",
    "Follow for what we find in the soil."
  ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","Wildfire","RegenerativeAgriculture","SoilBiology"] }],
  checks: [
    "Do not claim the soil saved the garden. We did not test it.",
    "The speaker agrees to appear."
  ],
  draft: "drafts/2026-09-17-reel-wildfire-garden.md"
}

];

/* The consent email, sent before anything is designed. One per recipient,
   their name at the top, sent by a person rather than an address nobody reads. */
const CONSENT_EMAIL = {
  subject: "Your photo, and one sentence, for our social media",
  body: [
    "Hi [NAME],",
    "I am [YOUR NAME], I work on social media at the Soil Food Web Foundation.",
    "We would like to post about the scholarships awarded in June, and we would like to include you. That would mean your photograph, your first and last name, and the country you are in appearing on our Instagram, Facebook and LinkedIn accounts. The posts are public, so anyone can see them and they can be shared onward.",
    "Two questions.",
    "First, are you happy for us to do that? If you would rather we did not, please just reply “no thanks”. Nothing happens as a result. It does not affect your scholarship, your place on the course, or anything else, and you do not need to give a reason. If you prefer, we can use your first name only, or your country without your name.",
    "Second, if you are happy to be included: would you write one sentence about what you intend to do with the training? We would quote it exactly as you write it, next to your photo. It does not need to be polished. If you would rather not be quoted, that is fine too and we will just use your name and country.",
    "If you have a social handle you would like tagged, send that as well.",
    "One last thing: if there is a photograph of yourself you would prefer we use, please attach it. Otherwise we will use the one from your application.",
    "Thank you either way,",
    "[YOUR NAME]"
  ],
  why: "It says exactly where the photograph goes, it gives a one-word way out, it says out loud that declining costs them nothing, and it offers the middle options so that “no” is not the only alternative to “yes”. People being asked for a photograph by an organisation that funded them are not in a neutral position, and the email has to account for that."
};

const SCHEDULE = {
  principle: [
    ["This is a swap, not a volume increase",
     "The meeting's recommendation was to hold content volume flat. Cadence is already high and the website destination is still unfixed. Each of these replaces a generic post already scheduled. Three to four posts a week, unchanged. Better posts in the same slots."],
    ["The standing template",
     "Monday: Science Explained, or The Bigger Picture. Wednesday: Take Action, or Events and Programs. Thursday: Community Voice, or Science Explained."],
    ["The stacking rule",
     "Never two promotional pillars in one week. Events and Programs is the promotional pillar. Community Voice, Science Explained, Take Action and The Bigger Picture are not."],
    ["The India window takes priority",
     "Weeks of 5, 12, 19 and 26 October are India's. Anything else moves around them."]
  ],
  months: [
    { name: "September and October", note: "Four India posts plus the daily stories. That is the ceiling. One Events and Programs post in the month, so nothing stacks.", weeks: [
      { w: "29 Sep", mon: ["Myth 1, beans and tomatoes","myth-1"], wed: "no post", thu: ["Failed piles, Loide","failed-piles"], note: "Teaser week. Failed piles runs two weeks before Field Notes" },
      { w: "5 Oct",  mon: ["India: Vijay Kumar and RYSS","india-ryss"], wed: ["India: four events","india-1"], thu: ["Favourite microbe 1, Sammie","microbe-1"], note: "Two India posts. Neither is promotional except the events card" },
      { w: "12 Oct", mon: ["India: Return to Earth (if cleared)","india-return-to-earth"], wed: ["India: five scholars","india-five-scholars"], thu: ["Favourite microbe 2, Allison","microbe-2"], note: "If Return to Earth is not cleared, move Before Soil Food Web 1 up" },
      { w: "19 Oct", mon: ["Mycelium shirt","mycelium-shirt"], wed: ["India stories, daily","india-3"], thu: ["Field Notes 1, Sandra","field-notes-1"], note: "Workshop runs 19 to 30. Stories daily from the ground" },
      { w: "26 Oct", mon: ["Before Soil Food Web 1, Gerald","before-sfw-1"], wed: ["India stories, daily","india-3"], thu: ["Favourite microbe 3, Carla","microbe-3"], note: "" }
    ]},
    { name: "November", note: "The quiet stretch with no launch, which is why the evergreen Take Action and the two reels sit here.", weeks: [
      { w: "2 Nov",  mon: ["Office hours reel","office-hours"], wed: ["Fall soil prep","fall-soil-prep"], thu: ["India: who was in the room","india-3"], note: "The attendee post. The one that makes the next tour easier to fill" },
      { w: "9 Nov",  mon: ["Myth 2","myth-2"], wed: ["Scholarship numbers carousel","scholarships"], thu: ["Favourite microbe 4, Wes","microbe-4"], note: "Scholarship is Community Voice, not a donation drive" },
      { w: "16 Nov", mon: ["Before Soil Food Web 2, Wes","before-sfw-2"], wed: "no post", thu: ["Community, 4,680","community-4680"], note: "Blocked on the community link having a home" },
      { w: "23 Nov", mon: ["sMApp: the formulas","smapp"], wed: ["Myth 3","myth-3"], thu: ["Field Notes 2","field-notes-2"], note: "sMApp before the Field Notes series builds up, so the numbers are already trusted" },
      { w: "30 Nov", mon: ["Favourite microbe 5, Ayşen","microbe-5"], wed: ["Spanish course","spanish-course"], thu: ["Before Soil Food Web 3, Brian","before-sfw-3"], note: "Spanish is Events and Programs. Only promotional post that week" }
    ]},
    { name: "December", note: "The one stacking risk in the quarter is the week of 14 December. If the Portuguese course slips from 7 December into that week there are two promotional posts. Move the practicum post to 4 January if that happens.", weeks: [
      { w: "7 Dec",  mon: ["Myth 4","myth-4"], wed: ["Portuguese course","portuguese-course"], thu: ["Favourite microbe 6, Gerald","microbe-6"], note: "Hold Portuguese until it is live on the new platform" },
      { w: "14 Dec", mon: ["Before Soil Food Web 4, Matthew","before-sfw-4"], wed: ["Advanced practicum access","advanced-practicum"], thu: ["Field Notes 3","field-notes-3"], note: "Two Events and Programs posts in eight days if Portuguese slips" },
      { w: "21 Dec", mon: ["Favourite microbe 7, Casey","microbe-7"], wed: "no post", thu: ["Guardian carousel (if dated)","guardian"], note: "Quiet week. Two posts" },
      { w: "28 Dec", mon: "no post", wed: "—", thu: ["Favourite microbe 8, Isadora","microbe-8"], note: "One post. Nobody is reading" }
    ]}
  ],
  unscheduled: [
    ["India: the science post", "Written and ready. Has to run before the tour, and Carla signs off slide 4"],
    ["Aren't we all just a bunch of microbes?", "Evergreen. Drops into any gap"],
    ["UMass Amherst", "Blocked on the UTM convention for the tracked link"],
    ["The wildfire reel", "Blocked on the video file. Any Monday once it is cut"],
    ["India: Return to Earth", "Not cleared. Pencilled at 12 October and comes out if it is not agreed"],
    ["Guardian carousel", "No publication date. Pencilled at 24 December"],
    ["Favourite microbe 9 and 10", "Brian and Tommy both chose small underdog microbes. Run them as a pair in January, or ask one to pick again"],
    ["Loide and Elena's microbes", "Not stated in the meeting. They are asked in the request email"],
    ["Before Soil Food Web 5", "Casey. Depends which five you want"]
  ]
};

const STATUS = {
  "ready":         ["Ready",            "#156826"],
  "review":        ["Needs a sign-off", "#C9A227"],
  "needs-consent": ["Needs consent",    "#C9A227"],
  "blocked":       ["Blocked",          "#8A4B3F"]
};
