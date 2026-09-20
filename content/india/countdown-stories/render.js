/* Render the five India countdown stories to 1080 x 1920 PNGs, and check that
 * nothing is drawn where a sticker or the Instagram interface goes.
 *
 *   node content/india/countdown-stories/render.js
 *
 * Writes, per story:  story-x.png         the frame to post
 *                     story-x-guides.png  the same frame with the reserved
 *                                         areas painted in, for planning only
 *
 * Served over http rather than opened as file:// because Chromium will not
 * load @font-face files across a file:// origin, and these are set in the
 * repository's own self-hosted fonts.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..', '..', '..');
const STORIES = ['a', 'b', 'c', 'd', 'e'];
const W = 1080, H = 1920;

/* The reserved rectangles, in the same numbers as _story.css. */
const RESERVED = [
  { name: 'interface, top',    x: 0,   y: 0,    w: W,   h: 250 },
  { name: 'interface, bottom', x: 0,   y: 1670, w: W,   h: 250 },
  { name: 'countdown sticker', x: 190, y: 1120, w: 700, h: 300 },
  { name: 'link sticker',      x: 220, y: 1490, w: 640, h: 160 },
];

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg',
  '.svg': 'image/svg+xml' };

function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const file = path.join(REPO, rel);
      if (!file.startsWith(REPO) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404); res.end('not found: ' + rel); return;
      }
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

const GUIDES = `
 .zone{outline:3px dashed rgba(219,230,167,.55); outline-offset:-3px;
   background:rgba(219,230,167,.10)}
 .zone::after{position:absolute;left:14px;top:10px;font:700 22px/1.3 Arial,sans-serif;
   letter-spacing:.12em;text-transform:uppercase;color:rgba(219,230,167,.85)}
 .zone--ui-top::after{content:"Instagram interface, keep clear"}
 .zone--ui-bottom::after{content:"Instagram interface, keep clear"}
 .zone--countdown::after{content:"countdown sticker, 700 x 300"}
 .zone--link::after{content:"link sticker"}
`;

(async () => {
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  let problems = 0;

  for (const id of STORIES) {
    const url = `http://127.0.0.1:${port}/content/india/countdown-stories/story-${id}.html`;
    await page.goto(url, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    /* Geometry check: every drawn element against every reserved rectangle. */
    const boxes = await page.evaluate(() => {
      const sel = '.lockup, .eyebrow, h1, .sub, .partner, .card, .credit, .shape, .plate';
      return [...document.querySelectorAll(sel)].map((el) => {
        const r = el.getBoundingClientRect();
        return { what: (el.className || el.tagName).toString().split(' ')[0],
                 text: (el.textContent || '').trim().slice(0, 34),
                 x: Math.round(r.x), y: Math.round(r.y),
                 w: Math.round(r.width), h: Math.round(r.height) };
      });
    });

    const hits = [];
    for (const b of boxes) {
      if (b.w === 0 || b.h === 0) continue;
      if (b.x < 0 || b.y < 0 || b.x + b.w > W || b.y + b.h > H) {
        hits.push(`${b.what} runs off the frame (${b.x},${b.y} ${b.w}x${b.h})`);
      }
      for (const z of RESERVED) {
        if (b.x < z.x + z.w && b.x + b.w > z.x && b.y < z.y + z.h && b.y + b.h > z.y) {
          hits.push(`${b.what} "${b.text}" overlaps ${z.name} (${b.x},${b.y} ${b.w}x${b.h})`);
        }
      }
    }
    const low = Math.max(...boxes.filter((b) => b.h && b.what !== 'shape').map((b) => b.y + b.h));
    console.log(`story-${id}: ${boxes.length} boxes, lowest text ends at ${low}px, ` +
                (hits.length ? `${hits.length} PROBLEM(S)` : 'clear'));
    hits.forEach((h) => console.log('   ! ' + h));
    problems += hits.length;

    await page.screenshot({ path: path.join(HERE, `story-${id}.png`) });
    await page.addStyleTag({ content: GUIDES });
    await page.screenshot({ path: path.join(HERE, `story-${id}-guides.png`) });
  }

  await browser.close();
  server.close();
  console.log(problems ? `\n${problems} problem(s). Fix before posting.` : '\nAll five clear.');
  process.exit(problems ? 1 : 0);
})();
