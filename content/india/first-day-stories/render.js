/* Render the four India first-day stories to 1080 x 1920 PNGs and check them.
 *
 *   node content/india/first-day-stories/render.js
 *
 * Checks, per frame: no text box in the top 250px or bottom 270px, no text box
 * off the frame, no two text boxes overlapping, no text overflowing its box.
 * Served over http because Chromium will not load fonts across file://.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..', '..', '..');
const STORIES = ['1-coimbatore', '2-seminar', '3-learning', '4-thank-you'];
const W = 1080, H = 1920, TOP = 250, BOTTOM = H - 270;
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.woff2': 'font/woff2', '.png': 'image/png' };

function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const rel = decodeURIComponent(req.url.split('?')[0]).replace(/^\/+/, '');
      const file = path.join(REPO, rel);
      if (!file.startsWith(REPO) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) {
        res.writeHead(404); res.end(); return;
      }
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

(async () => {
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  let problems = 0;

  for (const id of STORIES) {
    await page.goto(`http://127.0.0.1:${port}/content/india/first-day-stories/story-${id}.html`,
      { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    const r = await page.evaluate(() => {
      const fonts = ['Montserrat', 'EB Garamond'].map((f) => document.fonts.check(`16px "${f}"`));
      const imgs = [...document.images].map((i) => i.complete && i.naturalWidth > 0);
      const boxes = [...document.querySelectorAll('.label, h1, .body, .card')].map((el) => {
        const b = el.getBoundingClientRect();
        return { what: el.className || el.tagName, text: el.textContent.trim().slice(0, 30),
          x: b.x, y: b.y, w: b.width, h: b.height,
          overflow: (() => { const rg = document.createRange(); rg.selectNodeContents(el); const t = rg.getBoundingClientRect(); return t.right > b.right + 1 || t.left < b.left - 1 || el.scrollWidth > el.clientWidth + 1; })() };
      });
      return { fonts, imgs, boxes, text: document.querySelector('.frame').innerText };
    });
    const hits = [];
    if (r.fonts.includes(false)) hits.push('a brand font did not load');
    if (r.imgs.includes(false)) hits.push('a photo did not load');
    if (/—|\d\s*\/\s*\d|Day 1|Entry No/i.test(r.text)) hits.push('counter, label or em dash in text');
    const text = r.boxes.filter((b) => b.what !== 'card');
    for (const b of r.boxes) {
      if (b.y < TOP || b.y + b.h > BOTTOM) hits.push(`${b.what} "${b.text}" in the interface zone (${Math.round(b.y)} to ${Math.round(b.y + b.h)})`);
      if (b.x < 0 || b.x + b.w > W) hits.push(`${b.what} "${b.text}" off the frame`);
      if (b.overflow) hits.push(`${b.what} "${b.text}" overflows`);
    }
    for (let i = 0; i < text.length; i++) for (let j = i + 1; j < text.length; j++) {
      const a = text[i], b = text[j];
      if (a.x < b.x + b.w && a.x + a.w > b.x && a.y < b.y + b.h && a.y + a.h > b.y)
        hits.push(`"${a.text}" overlaps "${b.text}"`);
    }
    const lo = Math.min(...r.boxes.map((b) => b.y)), hi = Math.max(...r.boxes.map((b) => b.y + b.h));
    console.log(`story-${id}: text from ${Math.round(lo)} to ${Math.round(hi)}px, ` +
      (hits.length ? `${hits.length} PROBLEM(S)` : 'clear'));
    hits.forEach((h) => console.log('   ! ' + h));
    problems += hits.length;
    await page.screenshot({ path: path.join(HERE, `story-${id}.png`) });
  }
  await browser.close();
  server.close();
  console.log(problems ? `\n${problems} problem(s).` : '\nAll four clear.');
  process.exit(problems ? 1 : 0);
})();
