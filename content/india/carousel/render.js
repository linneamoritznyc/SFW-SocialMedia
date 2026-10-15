/* Render the six India carousel slides to 1080 x 1350 PNGs and run the four
 * checks before anything is shown or posted:
 *
 *   1. No counter, no eyebrow label, no photo credit on any slide.
 *   2. Headline 88px (110px on the cover), body 46px, on every slide.
 *   3. All text inside the central 1080 x 1080 square (y 135 to 1215).
 *   4. The swipe arrow on slide 1 and on no other slide.
 *
 *   node content/india/carousel/render.js
 *
 * Served over http rather than opened as file:// because Chromium will not
 * load @font-face files across a file:// origin.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http');
const path = require('path');
const fs = require('fs');

const HERE = __dirname;
const REPO = path.resolve(HERE, '..', '..', '..');
const W = 1080, H = 1350, SAFE_TOP = 135, SAFE_BOTTOM = 1215;
const SLIDES = [1, 2, 3, 4, 5, 6];

const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8',
  '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg', '.svg': 'image/svg+xml' };

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

(async () => {
  const server = await serve();
  const port = server.address().port;
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: W, height: H }, deviceScaleFactor: 1 });
  let problems = 0;
  const rows = [];

  for (const n of SLIDES) {
    await page.goto(`http://127.0.0.1:${port}/content/india/carousel/slide-${n}.html`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);

    const r = await page.evaluate(() => {
      const all = [...document.querySelectorAll('.frame *')];
      const textEls = all.filter((el) => [...el.childNodes].some((c) => c.nodeType === 3 && c.textContent.trim()));
      const words = textEls.map((el) => el.textContent.trim());
      const cs = (el) => getComputedStyle(el);

      const counter = words.filter((t) => /\b\d+\s*(\/|of)\s*\d+\b/i.test(t));
      const credit = words.filter((t) => /unsplash|photo:|credit/i.test(t));
      const eyebrow = textEls.filter((el) => cs(el).textTransform === 'uppercase' || /^[A-Z][A-Z\s]{3,}$/.test(el.textContent.trim()));
      const decor = all.filter((el) => ['rule', 'bar', 'line', 'divider'].some((c) => el.classList.contains(c)));

      const fonts = textEls.map((el) => ({
        what: el.tagName.toLowerCase() + (el.className ? '.' + el.className : ''),
        size: parseFloat(cs(el).fontSize),
        family: cs(el).fontFamily.split(',')[0].replace(/"/g, ''),
        weight: cs(el).fontWeight,
        text: el.textContent.trim().slice(0, 40),
      }));

      const outside = [];
      for (const el of textEls) {
        for (const rect of el.getClientRects()) {
          if (rect.width === 0 || rect.height === 0) continue;
          if (rect.top < 135 || rect.bottom > 1215 || rect.left < 0 || rect.right > 1080) {
            outside.push({ text: el.textContent.trim().slice(0, 30), top: Math.round(rect.top), bottom: Math.round(rect.bottom) });
          }
        }
      }
      const logo = document.querySelector('.logo');
      const logoBox = logo ? logo.getBoundingClientRect() : null;
      const arrows = document.querySelectorAll('.arrow').length;
      const loaded = ['700 88px Montserrat', '400 46px "Source Sans 3"'].map((f) => document.fonts.check(f));
      return { counter, credit, eyebrow: eyebrow.map((e) => e.textContent.trim()), decor: decor.length,
               fonts, outside, arrows, loaded,
               logo: logoBox && { top: Math.round(logoBox.top), bottom: Math.round(logoBox.bottom), w: Math.round(logoBox.width) } };
    });

    const h1 = r.fonts.filter((f) => f.what === 'h1');
    const body = r.fonts.filter((f) => f.what === 'p');
    const cta = r.fonts.filter((f) => f.what === 'p.cta');
    const wantH1 = n === 1 ? 110 : 88;
    const okH1 = h1.every((f) => f.size === wantH1 && f.family === 'Montserrat' && f.weight === '700');
    const okBody = body.every((f) => f.size === 46 && f.family === 'Source Sans 3' && f.weight === '400');
    const okCta = cta.every((f) => f.size === 54 && f.family === 'Montserrat' && f.weight === '700');
    const okArrow = n === 1 ? r.arrows === 1 : r.arrows === 0;
    const okClean = !r.counter.length && !r.credit.length && !r.eyebrow.length && !r.decor;
    const okInside = !r.outside.length && (!r.logo || (r.logo.top >= SAFE_TOP && r.logo.bottom <= SAFE_BOTTOM));
    const ok = okH1 && okBody && okCta && okArrow && okClean && okInside && r.loaded.every(Boolean);
    if (!ok) problems++;

    rows.push({ slide: n,
      '1 clean': okClean ? 'yes' : `NO ${JSON.stringify({ counter: r.counter, credit: r.credit, eyebrow: r.eyebrow, decor: r.decor })}`,
      '2 sizes': (okH1 && okBody && okCta) ? `headline ${h1.map((f) => f.size).join('/')}, body ${body.map((f) => f.size).join('/')}${cta.length ? ', last line ' + cta[0].size : ''}` : 'NO ' + JSON.stringify(r.fonts),
      '3 inside': okInside ? 'yes' : 'NO ' + JSON.stringify(r.outside),
      '4 arrow': okArrow ? (n === 1 ? 'yes, one' : 'none') : `NO, ${r.arrows}`,
      fonts: r.loaded.every(Boolean) ? 'loaded' : 'NOT LOADED',
    });

    await page.screenshot({ path: path.join(HERE, `slide-${n}.png`) });
  }

  await browser.close();
  server.close();
  console.table(rows);
  console.log(problems ? `\n${problems} slide(s) failed. Fix before showing.` : '\nAll six slides pass the four checks.');
  process.exit(problems ? 1 : 0);
})();
