/* Every post that exists so far, with the artwork, the caption exactly as
   written, the hashtags, and what is still blocking it.
   Copy comes from the captions.md files in the repo. Nothing is invented here. */

const POSTS = [
{
  id: "field-notes-1",
  title: "Field Notes 1: Sandra Niggemeyer",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Single image",
  slot: "Thursday 22 October",
  status: "needs-consent",
  statusNote: "Her written consent, and the tag handle has to come from her.",
  intro: "Her field trial in Van, Texas. Twenty years fallow, clay and sand, butternut squash. Three plots, one season. Pick one image and one caption.",
  imageChoice: true,
  images: [
    { src: "img/sandra/01-number-first.png",    label: "Number first" },
    { src: "img/sandra/04-field-photograph.png",label: "Field photograph" },
    { src: "img/sandra/05-quote-card.png",      label: "Quote card" },
    { src: "img/sandra/06-honest-ledger.png",   label: "Honest ledger" },
    { src: "img/sandra/07-specimen-sheet.png",  label: "Specimen sheet" },
    { src: "img/sandra/13-magazine-cover.png",  label: "Magazine cover" }
  ],
  captions: [
    { name: "Option A, the counterintuitive one", recommended: true,
      pairs: "Pairs with the honest ledger, or the data card.",
      body: [
        "Her tea plot gained one percent organic matter. It also had the fewest squash bugs.",
        "Sandra Niggemeyer ran three plots on the same Texas ground, fallow for twenty years, clay and sand. Biologically complete compost tilled into one. Teas and extracts through the season on another. Water only on the third.",
        "The compost plot gained 46 percent organic matter. The control gained 14 percent on water alone. The tea plot gained one.",
        "But the tea plot carried the fewest squash bugs, and the control carried the most. Beneficial microorganisms applied as extracts occupy the leaf and root surfaces that pests would otherwise colonise. That is a different mechanism from building soil structure, and one season on one field cannot separate them.",
        "Her own conclusion: soil biology rebuilds the ground before it rebuilds the yield. In degraded soil, the first season is the ground.",
        "What did your first season on tired ground actually give you? Tell us below."
      ],
      tags: ["SoilFoodWeb","LivingSoil","SoilBiology","Compost","RegenerativeFarming","SoilHealth","SoilFoodWebFoundation"] },
    { name: "Option B, the number-led one",
      pairs: "Pairs with number first, or field photograph.",
      body: [
        "Twenty years fallow. One season of biology. 46 percent more organic matter.",
        "Sandra Niggemeyer put biologically complete compost into one plot of Texas clay and sand, teas and extracts into a second, and water only into a third. Bacteria and fungi produce the glues that bind soil particles into aggregates. Fungal hyphae weave those into larger ones. Protozoa and nematodes graze the bacteria and release nutrients at the root, in the form the plant can use.",
        "The honest version: the control gained 14 percent on water alone, and the tea plot gained one. Harvest was 35 ounces against 19. A real difference, and a small sample.",
        "Ground that has been left alone does not need a miracle. It needs the organisms back.",
        "Save this for the next time somebody tells you degraded soil takes a decade."
      ],
      tags: ["SoilFoodWeb","LivingSoil","SoilHealth","Compost","RegenerativeAgriculture","SoilBiology"] },
    { name: "Option C, the quiet one",
      pairs: "Pairs with the quote card.",
      body: [
        "“Soil biology rebuilds the ground before it rebuilds the yield.”",
        "That is Sandra Niggemeyer's own conclusion after a season of butternut squash on Texas clay and sand that had been fallow for twenty years.",
        "Three plots. Compost into one, teas and extracts into another, water only into the third. The compost plot gained 46 percent organic matter, the control 14 percent, the tea plot one. The harvest was 35 ounces, 30 and 19.",
        "Hail killed her first planting. Rodents took the second. Johnson grass ran the beds by June. She wrote all of it down, which is why the numbers are worth anything at all.",
        "In degraded soil, she says, the first season is the ground.",
        "Follow along. Every other Thursday we publish what a field trial actually found."
      ],
      tags: ["SoilFoodWeb","LivingSoil","SoilBiology","RegenerativeFarming","SoilHealth","SoilFoodWebFoundation"] }
  ],
  checks: [
    "Every number traced back to her report, and the control figure present.",
    "No internal course acronyms. Foundation Courses, not FC.",
    "The word “certified” does not appear.",
    "One call to action, not two."
  ],
  more: { label: "Twenty-one other directions for the same story", dir: "img/sandra-more/" }
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
  intro: "UMass Amherst announced a $120 million Future of Food Initiative. Soil cultivation is named inside the new centre's scope. We have no involvement; we are posting it because the direction is right.",
  images: [
    { src: "img/umass/slide-1.png", label: "1. $120 million" },
    { src: "img/umass/slide-2.png", label: "2. What it buys" },
    { src: "img/umass/slide-3.png", label: "3. The scope list" },
    { src: "img/umass/slide-4.png", label: "4. Then and now" },
    { src: "img/umass/slide-5.png", label: "5. 160 years" }
  ],
  captions: [
    { name: "Instagram caption", recommended: true, body: [
      "$120 million is going into the future of food, and soil made the list.",
      "UMass Amherst announced its Future of Food Initiative this month: four $30 million tranches, a new 36,000 square foot research building, five permanent endowments and a new Center for the Future of Food.",
      "Read the center's scope and one line stands out. Alongside food safety, food chemistry and processing, it names everything involving cultivation, including soil cultivation, seed effectiveness and clean water.",
      "Soil biology has spent decades being treated as a separate conversation from the food system. It is the same conversation. What lives in the ground decides what nutrients a plant can reach, how much water the soil holds, and how a crop handles a bad season. A food initiative that skips the biology is studying the last few feet of a much longer chain.",
      "The university was built in Amherst over 160 years ago so it would sit near farms and farmers. A century and a half later, the question is back where it started.",
      "What would you want a $120 million food research program to study first? Tell us in the comments."
    ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","FoodSecurity","RegenerativeAgriculture","SoilScience","Agroecology"] },
    { name: "LinkedIn version", note: "No artwork needed. Slide 1 or 3 works as a single image.", body: [
      "UMass Amherst announced a $120 million Future of Food Initiative this month, funded in four equal parts by a private family foundation, the Commonwealth of Massachusetts, the university itself, and a $30 million target still to be raised.",
      "It buys a 36,000 square foot research building, five permanent endowments including a chair in food science, and a new Center for the Future of Food.",
      "The detail worth reading closely is the center's scope. It covers food safety, food chemistry, processing, new types of food, and everything involving food cultivation including soil cultivation, seed effectiveness and clean water.",
      "Soil biology appearing inside the scope of a major food-systems program, rather than beside it, is a shift. The funding model behind it is also worth noting: private philanthropy, state money and institutional funds arriving together, at a moment when federal research funding is less certain.",
      "Massachusetts accounts for roughly 45% of New England's food system jobs and sales, and food and agriculture has been one of the only clusters in that region with sustained growth over the past decade. This is regional economic strategy as much as it is science.",
      "We have no involvement in this initiative. We are posting it because the direction is the right one."
    ], tags: ["SoilHealth","FoodSystems","RegenerativeAgriculture"] }
  ],
  checks: [
    "Three of the four tranches are committed. The fourth is $30 million still to be raised by the UMass Amherst Foundation. The slide says so.",
    "No partnership with UMass is claimed."
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
  intro: "Three frames. The top 250px and bottom 280px of each are left clear for the app interface.",
  images: [
    { src: "img/umass/story-1.png", label: "1. $120 million" },
    { src: "img/umass/story-2.png", label: "2. Soil is on the list" },
    { src: "img/umass/story-3.png", label: "3. Sticker frame" }
  ],
  captions: [ { name: "Stickers to place in the app", recommended: true, body: [
      "Frame 1: no stickers.",
      "Frame 2: no stickers.",
      "Frame 3: a link sticker labelled “Read the announcement”, and a poll sticker reading “Should soil biology be part of food science? Yes / It always was”.",
      "Frame 3 draws the two sticker positions as dashed outlines so the layout leaves room for them. Do not export the dashed boxes into the final image."
    ], tags: [] } ],
  checks: []
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
  intro: "The deck headline read “$72,000+ Full Scholarships Awarded in June alone!” That sentence has the Foundation as its subject and the recipients as the object. Reworked so the people are the subject, and the exclamation mark is gone.",
  images: [
    { src: "img/scholarships/slide-1.png", label: "1. The collage" },
    { src: "img/scholarships/slide-2.png", label: "2. Recipient" },
    { src: "img/scholarships/slide-3.png", label: "3. Recipient" },
    { src: "img/scholarships/slide-4.png", label: "4. Recipient" },
    { src: "img/scholarships/slide-5.png", label: "5. Recipient" },
    { src: "img/scholarships/slide-6.png", label: "6. Recipient" },
    { src: "img/scholarships/slide-7.png", label: "7. How the fund works" }
  ],
  captions: [
    { name: "Instagram caption", recommended: true, body: [
      "[N] people started their training in June without paying for it.",
      "They are in Kenya, India, Ethiopia, and [COUNTRY], and their scholarships came to $72,000. Some farm a few acres. Some work inside organisations. One of them wrote to us having read about soil biology and having no land at all yet.",
      "They take the same courses as every other student, in the same community, on the same terms. The only difference is who paid.",
      "The fund exists because people give to it. Scholarship-designated gifts go to student access and nothing else, and that is the entire mechanism. There is no endowment behind it and no grant. When someone funds a seat, someone sits in it.",
      "Swipe to meet five of them."
    ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","RegenerativeAgriculture","FoodSecurity","Agroecology","SoilFoodWebFoundation"] },
    { name: "LinkedIn version", note: "Framed toward people who might fund scholarships.", body: [
      "In June, [N] people began training in soil biology without paying for it. Their scholarships came to $72,000.",
      "They are in Kenya, India, Ethiopia and [COUNTRY]. Some farm a few acres. Some work inside organisations doing restoration or extension work. They take the same courses as every fee-paying student, in the same community, on the same terms.",
      "The mechanism is simple enough to describe in one line: scholarship-designated gifts go to student access and nothing else. There is no endowment behind the fund. A funded seat is a filled seat, in the same quarter.",
      "Priority goes to applicants working in under-resourced regions, which is where the gap between what the training costs and what a grower can pay is widest.",
      "If funding technical training in soil biology is something your organisation does, the scholarship fund is the most direct route we have."
    ], tags: ["SoilHealth","RegenerativeAgriculture","Scholarships"] }
  ],
  checks: [
    "Fill [N] and [COUNTRY] from the confirmed list.",
    "“One of them wrote to us having read about soil biology and having no land at all yet” is a placeholder. Replace with a true one or cut it.",
    "Pick the five across geography and starting point. The collage spans Kenya, India, Ethiopia, Latin America and Europe.",
    "The ask is on slide 7 and nowhere else."
  ],
  email: true
},
{
  id: "india-1",
  title: "India post 1: the invitation",
  pillar: "Events and Programs",
  platform: "Instagram",
  format: "Carousel, five slides",
  slot: "Wednesday 7 October",
  status: "blocked",
  statusNote: "Three of the four events are placeholders until confirmed. Dates disagree across our own materials. If a name is unconfirmed, the face comes off the graphic.",
  intro: "Co-hosted with Isha Outreach. The talks are the excuse; the room is the point.",
  images: [
    { src: "img/india/post1-slide-1.png", label: "1. The collage" },
    { src: "img/india/post1-slide-2.png", label: "2. The workshop" },
    { src: "img/india/post1-slide-3.png", label: "3. The lecture" },
    { src: "img/india/post1-slide-4.png", label: "4. Panel and seminar" },
    { src: "img/india/post1-slide-5.png", label: "5. The open question" }
  ],
  captions: [ { name: "Instagram caption", recommended: true, body: [
      "We are coming to India in October.",
      "Four events across the country: a lecture, a panel, a seminar, and a workshop, with people who have spent their careers on natural farming and soil policy. Delegates are coming from organizations leading that work globally.",
      "India has more Soil Food Web practitioners than we have events to hold, and most of them have never met each other. That is the actual reason for this trip. The talks are the excuse. The room is the point.",
      "If you are going, say so in the comments and tell us where you are coming from. We would like to know who will be there before we arrive."
    ], tags: ["SoilFoodWeb","LivingSoil","SoilHealth","NaturalFarming","SaveSoil","RegenerativeAgriculture","SoilBiology"] },
    { name: "The Save Soil line", note: "Tag Isha Outreach. Put this in the caption or the first comment.", body: [
      "Co-hosted with Isha Outreach, whose Conscious Planet: Save Soil campaign is where a lot of you are arriving from. You already know soil matters. We are the ones with the microscope."
    ], tags: [] } ],
  checks: [
    "“Delegates are coming from organizations leading that work globally” is a claim about who is attending. If the delegate list is not confirmed, cut the sentence.",
    "Soil Food Web spelled out. No initials in public copy.",
    "No exclamation marks, no percentages."
  ]
},
{
  id: "india-2",
  title: "India post 2: the science post",
  pillar: "Science Explained",
  platform: "Instagram",
  format: "Carousel, five slides",
  slot: "Unscheduled. Runs before the tour",
  status: "review",
  statusNote: "Carla signs off the recovery order on slide 4, or slide 4 drops to “bacteria first, fungi last” with nothing in between.",
  intro: "Not about the tour. The tour is one line on the last slide. This is the post an Indian grower who has never heard of the Foundation saves.",
  images: [
    { src: "img/india/post2-slide-1.png", label: "1. Forty years" },
    { src: "img/india/post2-slide-2.png", label: "2. Flooding and tilling" },
    { src: "img/india/post2-slide-3.png", label: "3. Why fungi go first" },
    { src: "img/india/post2-slide-4.png", label: "4. The order it returns" },
    { src: "img/india/post2-slide-5.png", label: "5. Three to ten years" }
  ],
  captions: [ { name: "Instagram caption", recommended: true, body: [
      "Rice, then wheat, then rice again, for forty years. The biology does not fail all at once. It fails in an order.",
      "Flooding a field for rice does two things at the same time. Water fills the pore space and pushes the oxygen out, so the root zone sits anaerobic for weeks. Then tillage cuts the fungal network, which is made of threads, into pieces.",
      "Bacteria tolerate both. Fungi tolerate neither. They need oxygen, they grow as a physical network, and they rebuild slowly: bacteria divide in hours, a hyphal network takes seasons.",
      "Lose the fungi and you lose what they were doing. The glues and threads that hold soil crumbs together, so water soaks in instead of running off. The slow release of nitrogen that favours your crop over the fast weeds that thrive on nitrate.",
      "It comes back in an order too. Bacteria first, then the protozoa that eat them and release nitrogen at the root, then beneficial nematodes, then fungi last. Which is why the first season of recovery rarely looks like much, and why people give up in it.",
      "Left alone, that recovery takes three to ten years depending on how far the soil has gone. The alternative is to grow the missing organisms separately and put them back, which is what compost and extracts are for.",
      "We are in India from 19 to 30 October, and the events are open."
    ], tags: ["SoilFoodWeb","SoilBiology","NaturalFarming","LivingSoil","SoilHealth","Agroecology","RegenerativeAgriculture"] } ],
  checks: [
    "No invented figures and no percentage anywhere.",
    "“Three to ten years” is the Foundation's own stated range for unaided recovery. It is labelled as that on the slide, not as a measured result from one site.",
    "The recovery order on slide 4 is taught in the Foundation Courses rather than cited in this repository. Needs Carla."
  ]
},
{
  id: "india-3",
  title: "India post 3: who was in the room",
  pillar: "Community Voice",
  platform: "Instagram",
  format: "Story, daily, plus one feed post",
  slot: "Thursday 5 November",
  status: "blocked",
  statusNote: "Nothing exists until the tour happens. Permission is asked in the room, on the day. Names are a separate yes from faces.",
  intro: "The feed post at the end of the week is entirely attendee photographs with names and where they travelled from. That is the post that makes the next tour easier to fill.",
  images: [
    { src: "img/india/post3-story.png",     label: "Daily story" },
    { src: "img/india/post3-attendees.png", label: "Attendees feed post" }
  ],
  captions: [ { name: "Caption for the attendees post", recommended: true, body: [
      "This is who was in the room.",
      "[N] people, from [list the places]. Some came a few hours. One came [furthest distance].",
      "Most of them had never met another Soil Food Web practitioner in person. That was the reason for the trip, more than any of the talks were.",
      "If you are working on soil biology somewhere in the region and you were not here, tell us where you are. We would rather know before we plan the next one."
    ], tags: ["SoilFoodWeb","LivingSoil","NaturalFarming","SoilHealth","SaveSoil","SoilBiology"] } ],
  checks: [
    "A raised hand in a full lecture is not consent to appear on a public account. Ask, then photograph.",
    "“Where you travelled from” is a detail people give, not one we look up."
  ]
}
];

/* The consent email, sent before anything is designed. One per recipient. */
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

/* The quarter, from the standing weekly template. Posts that exist in this
   review are linked; everything else is listed so the week reads honestly. */
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
    { name: "October", note: "Four India posts plus the daily stories. That is the ceiling. One Events and Programs post in the month, so nothing stacks.", weeks: [
      { w: "29 Sep", mon: "Myth 1, beans and tomatoes", wed: "no post", thu: "Failed piles, Loide", note: "Teaser week. Failed piles runs two weeks before Field Notes" },
      { w: "5 Oct",  mon: "India: Vijay Kumar and RYSS", wed: ["India: four events","india-1"], thu: "Favourite microbe 1, Sammie", note: "Two India posts. Neither is promotional except the events card" },
      { w: "12 Oct", mon: "India: Return to Earth (if cleared)", wed: "India: five scholars", thu: "Favourite microbe 2, Allison", note: "If Return to Earth is not cleared, move Before Soil Food Web 1 up" },
      { w: "19 Oct", mon: "Mycelium shirt", wed: "India stories, daily", thu: ["Field Notes 1, Sandra","field-notes-1"], note: "Workshop runs 19 to 30. Stories daily from the ground" },
      { w: "26 Oct", mon: "Before Soil Food Web 1, Gerald", wed: "India stories, daily", thu: "Favourite microbe 3, Carla", note: "" }
    ]},
    { name: "November", note: "The quiet stretch with no launch, which is why the evergreen Take Action and the two reels sit here.", weeks: [
      { w: "2 Nov",  mon: "Office hours reel", wed: "Fall soil prep", thu: ["India: who was in the room","india-3"], note: "The attendee post. The one that makes the next tour easier to fill" },
      { w: "9 Nov",  mon: "Myth 2", wed: ["Scholarship numbers carousel","scholarships"], thu: "Favourite microbe 4, Wes", note: "Scholarship is Community Voice, not a donation drive" },
      { w: "16 Nov", mon: "Before Soil Food Web 2, Wes", wed: "no post", thu: "Community, 4,680", note: "Blocked on the community link having a home" },
      { w: "23 Nov", mon: "sMApp: the formulas", wed: "Myth 3", thu: "Field Notes 2", note: "sMApp before the Field Notes series builds up, so the numbers are already trusted" },
      { w: "30 Nov", mon: "Favourite microbe 5, Ayşen", wed: "Spanish course", thu: "Before Soil Food Web 3, Brian", note: "Spanish is Events and Programs. Only promotional post that week" }
    ]},
    { name: "December", note: "The one stacking risk in the quarter is the week of 14 December. If the Portuguese course slips from 7 December into that week there are two promotional posts. Move the practicum post to 4 January if that happens.", weeks: [
      { w: "7 Dec",  mon: "Myth 4", wed: "Portuguese course", thu: "Favourite microbe 6, Gerald", note: "Hold Portuguese until it is live on the new platform" },
      { w: "14 Dec", mon: "Before Soil Food Web 4, Matthew", wed: "Advanced practicum access", thu: "Field Notes 3", note: "Two Events and Programs posts in eight days" },
      { w: "21 Dec", mon: "Favourite microbe 7, Casey", wed: "no post", thu: "Guardian carousel (if dated)", note: "Quiet week. Two posts" },
      { w: "28 Dec", mon: "no post", wed: "—", thu: "Favourite microbe 8, Isadora", note: "One post. Nobody is reading" }
    ]}
  ],
  unscheduled: [
    ["India: Return to Earth", "Not cleared. Pencilled at 12 October and comes out if it is not agreed"],
    ["Guardian carousel", "No publication date. Pencilled at 21 December"],
    ["Favourite microbe 9 and 10", "Brian and Tommy both chose “small underdog microbes”. Run them as a pair in January, or ask one to pick again"],
    ["Loide and Elena's microbes", "Not stated in the meeting. They are asked in the request email"],
    ["Before Soil Food Web 5", "Depends which five you want"],
    ["The wildfire reel", "Blocked on the video file. Slot it into any Monday once cut"],
    ["UMass Amherst", "Blocked on the UTM convention for the tracked link"],
    ["India: the science post", "Written but not slotted. It needs to run before the tour, and Carla has to sign off slide 4"]
  ]
};

const STATUS = {
  "ready":         ["Ready",            "#156826"],
  "review":        ["Needs a sign-off", "#C9A227"],
  "needs-consent": ["Needs consent",    "#C9A227"],
  "blocked":       ["Blocked",          "#8A4B3F"]
};
