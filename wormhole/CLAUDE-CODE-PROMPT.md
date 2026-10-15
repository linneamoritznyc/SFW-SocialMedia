# Build Wormhole: the SFW social media preview, editor and agent pipeline

You are working for Linnea, who runs social media for the Soil Food Web Foundation (SFW). Work on your own to the goal below. Do not ask me about branches, commits or merges: make a branch, commit as you go, open a PR at the end, and give me the live URL.

## Goal
A password-protected website called **Wormhole** (password: `Wormhole`) where the SFW team sees every planned post the way it will look on Instagram and LinkedIn, can edit the text live, and where a background agent pipeline drafts new posts and visuals by itself. Linnea is dyslexic and cannot work from long Google Docs; this site replaces reading the doc. Nobody chats with the agents. They run on a schedule and their output appears in Wormhole as drafts.

## Where things are
- Base app: `github.com/linneamoritznyc/SFWassetlibrarycontentautomation` (Content Studio). Next.js 14 + Tailwind in `apps/web`, Supabase Postgres, R2 storage, job queue in `packages/queue`, Claude wrapper in `packages/ai/src/claude.ts`, posts schema in `supabase/migrations/0005_production.sql`, post preview component `apps/web/components/PhoneFrame.tsx`, Scout news scraper in `workers/light/src/jobs/scout_fetch.ts` + `scout_rank.ts`, clip jobs in `workers/media`, Remotion reels in `packages/remotion`. Build Wormhole inside this app.
- Seed data and rules: `github.com/linneamoritznyc/SFW-SocialMedia`, branch `wormhole`, folder `wormhole/`:
  - `posts.json`: 27 planned posts, 16 Oct to 13 Nov 2026 (date, iso, topic, platform, cta, words = slide text, link, sources, visual note, caption, status). Mentor posts have empty captions on purpose: Linnea pastes those.
  - `voice.md`: the house voice, banned patterns, doc format and visual look. Every writing and design agent must load it into its system prompt.
- Assets: `SFW-SocialMedia/assets/photo`, `assets/microscopy/cutout-*.png`, `assets/logo/sfw-foundation-wordmark-240.png`.
- Clipping: `github.com/linneamoritznyc/SFW-Clipping` (Python: yt-dlp, faster-whisper, Claude clip selection in `clipper/selection.py`, vertical cut in `clipper/engines/local.py`).

## Phase 1, ship tonight: the Wormhole site
1. Route `/wormhole` in `apps/web`. Gate it with a shared password page. Store the password in env `WORMHOLE_PASSWORD=Wormhole`, set an httpOnly cookie for 30 days. Keep the existing magic-link login for the rest of Content Studio.
2. Import `posts.json` into the `posts` table (add columns if needed: `iso_date`, `topic`, `slides jsonb`, `cta`, `link`, `sources jsonb`, `visual_note`, `status`). Write an idempotent seed script `pnpm wormhole:seed`.
3. Three views, switch with big tabs at the top:
   - **Instagram feed**: phone-width column, real IG look: avatar + `soilfoodwebschool`, swipeable carousel (4:5) with dots, heart/comment/share/save icons, caption with "more", hashtags in blue. A date chip above each post ("Thu 22 Oct").
   - **Instagram grid**: the profile grid, newest first, so we see how the feed looks as a whole.
   - **LinkedIn feed**: company post look: "Soil Food Web Foundation", caption above the image with "...see more", image or document carousel below.
   - Carousel slides come from uploaded images first; if a slide has no image yet, render it as a clean white text slide from `slides[]` (black text, small letter-spaced SOIL FOOD WEB wordmark), so every post is visible from day one.
4. **Live editing**: an "Edit" button on each post opens fields for caption, slide text, CTA and link right under the post. Typing updates the preview instantly. Save automatically (debounced 800 ms) and broadcast with Supabase Realtime so Allison's edits appear live on Linnea's screen. Keep every save in `post_versions` with who and when. Show a small "Saved" state.
5. **Images**: drag-and-drop upload per slide (Canva exports) to R2; reorder slides by drag.
6. **Status chips** per post: Draft, Copy approved (Allison), Approved (Stephanie), Scheduled. Filter by status and by week.
7. **Big readable type**, high contrast, generous spacing, a toggle for larger text. White page, SFW green as the only accent. Works on a phone.
8. **Export** button: download the selected week as an HTML file in Stephanie's exact Google Doc template from `voice.md` (H2 date, H3 topic, H3 CTA, normal Words/Link/Source, H3 Visual Asset, H3 Caption/Body Copy), ready to paste into the October planning doc.
9. Deploy to Vercel. Give me the URL.

## Phase 2: the agent pipeline (runs on its own, no chat)
Use the existing job queue and `packages/ai/src/claude.ts`. Models: `claude-sonnet-5-5` for writing and critique, `claude-haiku-5-5` for ranking and checks. All agents load `voice.md`.
1. **Planner** (weekly cron): reads the posts table, the promo dates below and any gaps (fewer than 3 posts in a week, any promo or event without a post) and creates draft post rows with a topic, pillar and sources to use.
2. **Writer**: drafts caption + slide text for each planned row, using the 5 best existing captions in `posts.json` as few-shot examples.
3. **Critic**: checks every draft against `voice.md` (banned patterns, em dashes, hashtags count, procedure names) and checks every number and claim against the row's sources. Fails go back to the Writer once; second fail is marked "Needs Linnea" with the reason.
4. **Visual agent** with Replicate (use my Replicate API key from env `REPLICATE_API_TOKEN`):
   - background removal on photos of objects (compost, roots, worms, microscope images) to make cutouts on pure white with a small serif label;
   - image generation only for missing generic subjects (vegetables, harvest tables, fallen leaves), with a style reference from the photos Linnea marks as "moodboard" in the asset library. Never generate people, never fake SFW workshop photos, never stock.
   - the white event card (Fibershed style) rendered from HTML to PNG for events and course dates.
5. **Scout**: run the existing news scraper weekly; the top 5 items become the monthly "Fun Soil News" draft with a link per story.
6. **Clips**: for each webinar URL Linnea adds, run the SFW-Clipping selection logic and create Reel drafts (2 to 3 word cover, word-by-word subtitles, link in first comment).
7. **Budget guard**: log the cost of every Claude and Replicate call (already in `ai_calls`), show the month's spend in Wormhole's header, stop all agents at 90 USD per month.

## Promo dates to plan around
- Foundation Courses and Compost Intensive (CIC) promo 19 Oct to 30 Nov 2026; early bird 19 Oct to 1 Nov; CIC starts 18 Jan 2027.
- Accelerator Workshop Costa Rica promo 12 Oct 2026 to 11 Jan 2027; workshop 18 to 25 Jan 2027.
- Advanced Programs promo from 8 Nov. Giving Tuesday 1 Dec 2026. World Soil Day 5 Dec. New Year webinar series January.

## Hard rules
- Never connect or write to the SFW Google Drive. Never put links to Linnea's Minerva Drive in anything SFW will see.
- Never invent a fact, name, price or date. Missing info becomes a visible "[needs: what, from whom]" chip on the post.
- No em dashes anywhere in generated copy.
- Ads are a separate project. Keep them out of Wormhole.

## Done means
Phase 1 live on a Vercel URL behind the password, all 27 posts visible in the three views, live editing works in two browser windows at once, export matches the template. Then Phase 2 merged with the agents running on cron and the spend counter visible. Report back with the URL and one line per phase on what works.
