/* Render the India assets and check each one against the five rules.
 *
 * The finished PNGs are written to two sibling folders, ready to drag into
 * Drive: content/india/posts/ and content/india/stories/. The HTML that
 * makes them stays here.
 *
 *   node content/india/countdown-stories/render.js
 *
 * For every file it prints, in order:
 *   1. exact pixel size
 *   2. all text on the solid or cream band, none over the photograph
 *   3. logo present, cream, top left
 *   4. copy matches content/india/copy.md word for word
 *   5. story only: the bottom 500px is empty
 * and exits non zero if any answer is no.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..', '..', '..');
const COPY = fs.readFileSync(path.join(REPO, 'content', 'india', 'copy.md'), 'utf8');

const ASSETS = [
  ...[1,2,3,4,5,6].map((n) => ({ id: `india-post-${n}`,  w: 1080, h: 1350, kind: 'post'  })),
  ...[1,2,3,4,5,6,7,8].map((n) => ({ id: `india-story-${n}`, w: 1080, h: 1920, kind: 'story' })),
];
const CREAM = '#F4F1EA';
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg' };

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
const norm = (s) => s.replace(/\u2019/g, "'").replace(/\s+/g, ' ').trim().toLowerCase();

(async () => {
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  let bad = 0;

  for (const a of ASSETS) {
    const page = await browser.newPage({ viewport: { width: a.w, height: a.h }, deviceScaleFactor: 1 });
    await page.goto(`http://127.0.0.1:${port}/content/india/countdown-stories/${a.id}.html`,
                    { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    const d = await page.evaluate(() => {
      const box = (el) => { const r = el.getBoundingClientRect();
        return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
      const band = document.querySelector('.band');
      const img = document.querySelector('.mark img');
      return {
        frame: box(document.querySelector('.frame')),
        band: box(band),
        text: [...document.querySelectorAll('.eyebrow, h1, .lede, .support, .cta')].map((el) => ({
          what: el.tagName === 'H1' ? 'headline' : el.className,
          copy: (el.textContent || '').trim(),
          size: getComputedStyle(el).fontSize, colour: getComputedStyle(el).color, ...box(el),
        })),
        mark: { ...box(document.querySelector('.mark')), loaded: !!img && img.naturalWidth > 0,
                src: img ? img.getAttribute('src').split('/').pop() : '(none)' },
      };
    });

    const OUT = path.join(HERE, '..', a.kind === 'post' ? 'posts' : 'stories');
    fs.mkdirSync(OUT, { recursive: true });
    await page.screenshot({ path: path.join(OUT, `${a.id}.png`) });
    const dim = await page.evaluate(() => [0, 0]);
    await page.close();

    const png = fs.readFileSync(path.join(OUT, `${a.id}.png`));
    const pw = png.readUInt32BE(16), ph = png.readUInt32BE(20);

    const onBand = d.text.every((t) => t.y >= d.band.y - 1 && t.y + t.h <= d.band.y + d.band.h + 1);
    const strayText = d.text.filter((t) => !(t.y >= d.band.y - 1 && t.y + t.h <= d.band.y + d.band.h + 1));
    const logoOK = d.mark.loaded && d.mark.src.includes('cream') && d.mark.x <= 90 && d.mark.y <= 90;
    const copyOK = d.text.every((t) => norm(COPY).includes(norm(t.copy)));
    const missing = d.text.filter((t) => !norm(COPY).includes(norm(t.copy))).map((t) => t.copy);
    const lowest = Math.max(...d.text.map((t) => t.y + t.h));
    const bottomOK = a.kind === 'post' ? null : lowest <= a.h - 500;

    const yn = (v) => (v ? 'yes' : 'NO');
    console.log(`\n${a.id}.png`);
    console.log(`  1. size            ${pw} x ${ph}  ${pw === a.w && ph === a.h ? 'yes' : 'NO'}`);
    console.log(`  2. text on band    ${yn(onBand)}${strayText.length ? '  <- ' + strayText.map((t) => t.what).join(', ') : ''}`);
    console.log(`  3. logo cream, top left  ${yn(logoOK)}  (${d.mark.src}, at ${d.mark.x},${d.mark.y})`);
    console.log(`  4. copy matches copy.md  ${yn(copyOK)}${missing.length ? '  <- ' + missing.join(' | ') : ''}`);
    console.log(`  5. bottom 500 empty      ${a.kind === 'post' ? 'n/a, feed post' : yn(bottomOK) + `  (lowest text ${lowest}, limit ${a.h - 500})`}`);
    if (!(pw === a.w && ph === a.h) || !onBand || !logoOK || !copyOK || bottomOK === false) bad++;
  }

  await browser.close();
  server.close();
  console.log(bad ? `\n${bad} file(s) failed. Fix before posting.` : `\nAll ${ASSETS.length} files pass all five checks.`);
  process.exit(bad ? 1 : 0);
})();
