/* Render the India countdown stories, and audit each frame before it ships.
 *
 *   node content/india/countdown-stories/render.js
 *
 * Writes story-x.png per frame, and story-x-guides.png with the sticker band
 * drawn in for planning. Fails loudly, with a reason, if a frame breaks any
 * of the three rules the layout is built on:
 *
 *   1. every line of type sits inside the solid block, between the split at
 *      864 and the top of the sticker band at 1500;
 *   2. every text colour is one of the three allowed for that block colour;
 *   3. the mark sits on the photograph, below the interface band.
 *
 * Served over http rather than file:// because Chromium will not load
 * @font-face files across a file:// origin.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..', '..', '..');
const STORIES = ['a-deadline', 'b-hands', 'c-weeks', 'd-payment', 'e-next',
                 'f-extended', 'g-stillopen'];
const W = 1080, H = 1920;
const SPLIT = 864;        // photo above, solid block below
const STICKERS = 1500;    // top of the empty band, 420px tall
const UI_TOP = 250;

/* The three pairs, as hex. Nothing else may appear as a text colour. */
const CREAM = '#F4F1EA', SOIL = '#4F3433', MOSS = '#22371F',
      TAN = '#C89B7B', GOLD = '#C9A227', GREEN = '#156826';
const PAIRS = {
  [MOSS]:  { name: 'deep green block',    text: CREAM, eyebrow: GOLD },
  [SOIL]:  { name: 'Soil Brown block',    text: CREAM, eyebrow: TAN },
  [CREAM]: { name: 'Organic Cream block', text: SOIL,  eyebrow: GREEN },
};
const hex = (rgb) => {
  const m = rgb.match(/\d+/g);
  return '#' + m.slice(0, 3).map((n) => (+n).toString(16).padStart(2, '0')).join('').toUpperCase();
};

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg' };

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
 .zone--stickers{outline:3px dashed rgba(219,230,167,.6); outline-offset:-3px;
   background:rgba(219,230,167,.10)}
 .zone--stickers::after{content:"sticker band, 420px, keep empty";
   position:absolute;left:18px;top:14px;font:700 24px/1.3 Arial,sans-serif;
   letter-spacing:.1em;text-transform:uppercase;color:rgba(219,230,167,.9)}
 .zone--ui-top{outline:3px dashed rgba(255,255,255,.45); outline-offset:-3px}
`;

(async () => {
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  let problems = 0;

  for (const id of STORIES) {
    await page.goto(`http://127.0.0.1:${port}/content/india/countdown-stories/story-${id}.html`,
                    { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    const data = await page.evaluate(() => {
      const box = (el) => { const r = el.getBoundingClientRect();
        return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
      const fine = document.querySelector('.fine');
      const lastBody = [...document.querySelectorAll('.body p')].pop();
      const collide = fine && lastBody &&
        lastBody.getBoundingClientRect().bottom > fine.getBoundingClientRect().top + 1;
      const text = [...document.querySelectorAll('.eyebrow, h1, .body p, .fine p')].map((el) => ({
        what: (el.className || el.tagName).toString().split(' ')[0],
        copy: (el.textContent || '').trim().slice(0, 40),
        colour: getComputedStyle(el).color,
        size: getComputedStyle(el).fontSize,
        ...box(el),
      }));
      return {
        text,
        collide,
        mark: box(document.querySelector('.mark')),
        block: getComputedStyle(document.querySelector('.block')).backgroundColor,
      };
    });

    const blockHex = hex(data.block);
    const pair = PAIRS[blockHex];
    const hits = [];
    if (!pair) hits.push(`block colour ${blockHex} is not one of the three pairs`);

    for (const t of data.text) {
      if (t.h === 0) continue;
      if (t.y < SPLIT) hits.push(`${t.what} "${t.copy}" sits on the photograph (top ${t.y}, split ${SPLIT})`);
      if (t.y + t.h > STICKERS) hits.push(`${t.what} "${t.copy}" runs into the sticker band (bottom ${t.y + t.h})`);
      if (t.x < 90 || t.x + t.w > W - 90) hits.push(`${t.what} "${t.copy}" breaks the 90px margin`);
      if (pair) {
        const want = t.what === 'eyebrow' ? pair.eyebrow : pair.text;
        if (hex(t.colour) !== want) {
          hits.push(`${t.what} "${t.copy}" is ${hex(t.colour)}, the pair says ${want}`);
        }
      }
    }
    if (data.collide) hits.push('the last body line runs into the fine print');
    if (data.mark.y < UI_TOP) hits.push(`the mark sits in the interface band (top ${data.mark.y})`);
    if (data.mark.y + data.mark.h > SPLIT) hits.push(`the mark crosses the split (bottom ${data.mark.y + data.mark.h})`);

    const low = Math.max(...data.text.filter((t) => t.h).map((t) => t.y + t.h));
    console.log(`story-${id}: ${pair ? pair.name : blockHex}, ${data.text.length} lines, ` +
                `type runs ${Math.min(...data.text.map((t) => t.y))} to ${low}, ` +
                (hits.length ? `${hits.length} PROBLEM(S)` : 'all three checks pass'));
    hits.forEach((h) => console.log('   ! ' + h));
    problems += hits.length;

    await page.screenshot({ path: path.join(HERE, `story-${id}.png`) });
    await page.addStyleTag({ content: GUIDES });
    await page.screenshot({ path: path.join(HERE, `story-${id}-guides.png`) });
  }

  await browser.close();
  server.close();
  console.log(problems ? `\n${problems} problem(s). Fix before posting.`
                       : `\nAll ${STORIES.length} frames pass: type inside the block, colours from the pairs.`);
  process.exit(problems ? 1 : 0);
})();
