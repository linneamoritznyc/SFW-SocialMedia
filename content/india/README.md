# India Accelerator Workshop, posts and stories

Thirty feed posts as six carousels of five, and twenty stories as four
sequences of five. Built 20 September 2026 from Linnea's six posts, the
enrollment page and the Isha Outreach marketing document. Every word on every
image is in `copy.md`; the renderer checks it.

Both formats share one frame, the one approved on 20 September: photograph on
top, cream band below, green eyebrow, Montserrat headline in Soil Brown, gold
for the one emphasised phrase, Source Sans body. Logo in cream, top left.

| Format | Size | Where | Zip |
| :-- | :-- | :-- | :-- |
| Feed posts | 1080 x 1350 | `posts/<carousel>/slide-N.png` | `india-posts.zip` |
| Stories | 1080 x 1920 | `stories/story-NN.png` | `india-stories.zip` |

Stories keep the bottom 500 px of the band empty for the countdown and link
stickers, and nothing sits in the top 250 px where the Instagram interface goes.
Each sequence uses one photograph height so a run reads as one piece.

## Rebuilding

```
node content/india/build/build.js
```

Edit the words in `build/data.js`, add them to `copy.md` if they are new
approved copy, and rebuild. The renderer prints five checks per file and stops
if any fails: exact size, all type on the band, logo present, copy found in
`copy.md`, and the sticker space empty. If a line does not fit, the photograph
gives up height. The type is never shrunk.

## Posts

### Post 1, the main announcement (`posts/carousel-1-announcement/`)

| Slide | Photo | Copy |
| :-- | :-- | :-- |
| 1 | Remi Clinton | The Accelerator Workshop comes to India this October. Ten immersive days at the Isha Yoga Center in Coimbatore, with field work on the Save Soil farm. |
| 2 | Ranjini Hemanth | Learn how to use beneficial soil microorganisms to improve soil function / increase water retention / reduce topsoil erosion / support healthier plants / make better use of organic waste / reduce dependence on costly external inputs |
| 3 | Cymatics In | Rather than spending years piecing together information through videos, books, or trial and error, participants practice the complete process on a working farm with guidance from experienced Soil Food Web mentors. |
| 4 | Nitish Surelia | Build and monitor compost. Prepare biological soil amendments. / Examine microorganisms under a microscope. / Apply amendments in the field. / Learn how to recognize and correct problems as they arise. |
| 5 | Saktheeswaran Govindarajan | Accommodation, meals, transport and materials included. Enrollment covers 13 nights of accommodation, daily meals, transportation between the Isha Yoga Center and the Save Soil farm, workshop materials, and direct access to the instructional team. Details on the school site. Link in bio. |

Caption: see `captions.md`.

### Post 2, what you take home (`posts/carousel-2-what-you-take-home/`)

| Slide | Photo | Copy |
| :-- | :-- | :-- |
| 1 | Selvan Tamilmani | What you take home Participants will leave with: |
| 2 | Ganesh Kulasekara | A practical understanding of how soil microorganisms influence nutrient availability, plant health, soil structure, and water retention. |
| 3 | Ranjini Hemanth | Experience converting locally available organic materials into high-quality biological compost. Skills for monitoring compost and responding to changes in moisture, temperature, aeration, and biological activity. |
| 4 | Cymatics In | Experience making compost extracts, teas, and other biological preparations for field application. An introduction to microscopy as a tool for evaluating soil, compost, and biological amendments. |
| 5 | Gowtham Agm | Greater confidence to begin applying these practices on their own farm, garden, composting operation, or restoration project. India, this October. Link in bio. |

Caption: see `captions.md`.

### Post 3, time (`posts/carousel-3-time/`)

| Slide | Photo | Copy |
| :-- | :-- | :-- |
| 1 | Div | The one thing you can’t get more of is time. |
| 2 | Navi | This workshop takes you from knowing you want to make compost to save your soil, / to knowing how to grow the biology that generates soil fertility through thermophilic compost and liquids, / to actually making them so you can continue on your own when you get home. |
| 3 | Navi | Learning this alone could take years. |
| 4 | Remi Clinton | If you want to be an agent of action now, this workshop is designed to get you up to speed fast and able to reproduce these results wherever in the world you work or live. |
| 5 | Gowtham Agm | Coimbatore, this October. Link in bio. |

Caption: see `captions.md`.

### Post 4, inputs (`posts/carousel-4-inputs/`)

| Slide | Photo | Copy |
| :-- | :-- | :-- |
| 1 | Ranjini Hemanth | Chemical inputs are expensive and they damage the soil you depend on. |
| 2 | Nitish Surelia | Biological and organic-based inputs can be expensive too, and many lack the biology needed to make a real difference, which leaves you tethered to an external source for imported amendments. |
| 3 | Cymatics In | Learning to create your own biological amendments from materials readily available and local to you is the best path to nutrient-rich living soil, and it can substantially decrease the cost of growing crops and managing land. |
| 4 | Saktheeswaran Govindarajan | Interrupt the cycle of waste and reduce the cost of inputs by turning organic materials into a valuable resource. Gain hands-on experience transforming locally available feedstocks into biologically rich compost that can be used to restore soil function rather than relying solely on purchased inputs. |
| 5 | Div | Ten days in India. Link in bio. |

Caption: see `captions.md`.

### Post 5, the setting (`posts/carousel-5-the-setting/`)

| Slide | Photo | Copy |
| :-- | :-- | :-- |
| 1 | At Infinity | The field work happens on the Save Soil farm, a Conscious Planet initiative, and the workshop is hosted by the Isha Foundation at their Yoga Center in Coimbatore, Tamil Nadu. |
| 2 | Ranjini Hemanth | A Save Soil Model Farm Established by Sadhguru in 2007 as part of Isha’s commitment to environmental restoration, the Regenerative Revolution Farm works to improve soil fertility while enhancing the economic well-being of farmers throughout Tamil Nadu and Puducherry. |
| 3 | Palak Pitroda | The Isha Yoga Center Your lodgings during the workshop are located at the Isha Yoga Center in Coimbatore, Tamil Nadu, India, a peaceful destination situated at the foothills of the Velliangiri Mountains, approximately 30 kilometers west of Coimbatore. |
| 4 | Saktheeswaran Govindarajan | Learn alongside farmers, composters, gardeners, land managers, and regenerative agriculture practitioners who share a commitment to healthier soils, healthier plants, and more resilient ecosystems. |
| 5 | Remi Clinton | Your people are here. October dates on the school site. Link in bio. |

Caption: see `captions.md`.

### Post 6, for current students (`posts/carousel-6-for-current-students/`)

| Slide | Photo | Copy |
| :-- | :-- | :-- |
| 1 | Navi | Months or years of independent practice, compressed. |
| 2 | Ganesh Kulasekara | For those pursuing Soil Food Web certification, the Accelerator Workshop offers an opportunity to satisfy the learning objectives for the BioComplete™ Compost Production and Biological Liquid Amendments courses. |
| 3 | Cymatics In | Over ten highly supported days you will build and manage biologically complete compost piles / monitor conditions and make timely adjustments / produce and apply compost extracts, teas and protozoan infusions / assess samples using microscopy with beginner support available / extract and observe nematodes / troubleshoot with direct guidance from mentors |
| 4 | Nitish Surelia | To qualify, students must meet the following requirements: Attend all 10 days of the workshop and fully participate in all activities. / Successfully complete all 4 Foundation Courses and the Soil Microscopy Course. / Complete the Pre-workshop Training Course and Assignment. / Complete the Post-workshop Graduation Assessment. |
| 5 | Navi | Save Your Seat, Don’t Delay! Details on the school site. Link in bio. |

Caption: see `captions.md`.

## Stories

Post each sequence in order, a few minutes apart. One link sticker per sequence, on the last frame, to school.soilfoodweb.com/courses/india-workshop-2026. Countdown sticker wherever enrollment is closing.

### Sequence A, the announcement

| File | Photo | Copy |
| :-- | :-- | :-- |
| story-01.png | Navi | The Accelerator Workshop comes to India this October. |
| story-02.png | At Infinity | Ten immersive days at the Isha Yoga Center in Coimbatore, with field work on the Save Soil farm. |
| story-03.png | Ranjini Hemanth | Build and monitor compost. Prepare biological amendments. Examine microorganisms under a microscope. Apply them in the field. |
| story-04.png | Cymatics In | Rather than spending years piecing this together from videos and trial and error, you practice the complete process with mentors beside you. |
| story-05.png | Saktheeswaran Govindarajan | Accommodation, meals, transport and materials included. Details on the school site. |

### Sequence B, why attend

| File | Photo | Copy |
| :-- | :-- | :-- |
| story-06.png | Nitish Surelia | Learn by doing, with expert support. Build compost, monitor biological processes, prepare soil amendments, use a microscope, and apply biology in the field while receiving real-time guidance and troubleshooting support. |
| story-07.png | Ganesh Kulasekara | Learn faster with expert guidance. Receive immediate feedback from experienced mentors who can help you recognize problems, understand why they are happening, and make effective adjustments. |
| story-08.png | Selvan Tamilmani | Learn to look beneath the surface of soil and compost. Recognize signs of biological health or imbalance, and make more informed decisions based on what your system needs. |
| story-09.png | Saktheeswaran Govindarajan | Build confidence through repeated practice. Work with multiple compost piles, biological preparations, samples, and field applications so that the process becomes more familiar and repeatable. |
| story-10.png | Remi Clinton | Your people are here. Learn alongside farmers, composters, gardeners, land managers, and regenerative agriculture practitioners who share a commitment to healthier soils, healthier plants, and more resilient ecosystems. October dates on the school site. |

### Sequence C, the place

| File | Photo | Copy |
| :-- | :-- | :-- |
| story-11.png | Div | Coimbatore, Tamil Nadu. 19 to 30 October 2026. The field work happens on the Save Soil farm, a Conscious Planet initiative, and the workshop is hosted by the Isha Foundation at their Yoga Center in Coimbatore, Tamil Nadu. |
| story-12.png | Ranjini Hemanth | A Save Soil Model Farm Located approximately 3 km from the Isha Yoga Center, the farm will serve as our outdoor classroom for the Accelerator Workshop. Daily shuttle transportation will be provided. |
| story-13.png | Palak Pitroda | The Isha Yoga Center Your lodgings during the workshop are located at the Isha Yoga Center in Coimbatore, Tamil Nadu, India, a peaceful destination situated at the foothills of the Velliangiri Mountains, approximately 30 kilometers west of Coimbatore. |
| story-14.png | Cymatics In | Surrounded by nature and home to an international community, the center offers a calm and supportive environment for immersive learning, personal growth, and meaningful connection. |
| story-15.png | Navi | Coimbatore is well connected by air, rail, and road, with taxis and direct bus services available to the center. Details on the school site. |

### Sequence D, for current students, and the close

| File | Photo | Copy |
| :-- | :-- | :-- |
| story-16.png | Gowtham Agm | On the path to becoming a Soil Food Web Consultant? Accelerate your path to graduation! |
| story-17.png | Remi Clinton | Months or years of independent practice, compressed. For those pursuing Soil Food Web certification, the Accelerator Workshop offers an opportunity to satisfy the learning objectives for the BioComplete™ Compost Production and Biological Liquid Amendments courses. |
| story-18.png | Nitish Surelia | Over ten highly supported days you will build and manage biologically complete compost piles / monitor conditions and make timely adjustments / produce and apply compost extracts, teas and protozoan infusions / assess samples using microscopy with beginner support available / extract and observe nematodes / troubleshoot with direct guidance from mentors |
| story-19.png | Ganesh Kulasekara | To qualify, students must meet the following requirements: Attend all 10 days of the workshop and fully participate in all activities. / Successfully complete all 4 Foundation Courses and the Soil Microscopy Course. / Complete the Pre-workshop Training Course and Assignment. / Complete the Post-workshop Graduation Assessment. |
| story-20.png | Navi | Enrollment is filling up! If you are eager to accelerate your Soil Food Web Consultant education, or simply want to have the experience of a lifetime, don’t delay! Receive gold-standard Soil Food Web education and gain professional experience on-site in a place designed for holistic wellness and a deep realization of what the Earth needs now. Save Your Seat, Don’t Delay! |

## Photographs

All from Unsplash, listed with their photographers in
`assets/india-free-images/CREDITS.md`. None is a Soil Food Web workshop
photograph and none is presented as one; the photographer is named in small
type on every frame.

## Kept off the images

- Prices and payment plans. They are on the enrollment page, and a price on a
  card needs Stephanie's sign-off.
- "Proven to replace the need for chemical interventions", "this makes them out
  of the question" and "vastly decrease", from the Isha document. All three
  break the claims rules.
- "In just 2 weeks", because the same page says 10 days.
- Em dashes, and the acronym SFW.
