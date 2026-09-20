/* Build every India post and story, check each one, write the PNGs.
 *
 *   node content/india/build/build.js
 *
 * Writes content/india/posts/<carousel>/slide-N.png and
 * content/india/stories/story-NN.png, and prints per file:
 *   1. exact pixel size
 *   2. every line of type on the cream band, none over the photograph
 *   3. logo present, cream, top left
 *   4. copy found word for word in content/india/copy.md
 *   5. story: bottom 500px empty. post: type clears the bottom edge
 * Exits non zero if any answer is no. The photograph gives up height when the
 * type needs it; the type is never shrunk.
 */
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const http = require('http'); const path = require('path'); const fs = require('fs');
const { EYE, carousels, stories } = require('./data.js');

const HERE = __dirname, INDIA = path.resolve(HERE, '..'), REPO = path.resolve(HERE, '..', '..', '..');
const COPY = fs.readFileSync(path.join(INDIA, 'copy.md'), 'utf8');
const norm = (s) => s.replace(/[’‘]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, ' ').trim().toLowerCase();
const COPYN = norm(COPY);
const esc = (s) => s.replace(/&/g, '&amp;').replace(/</g, '&lt;');
const TYPES = { '.html': 'text/html; charset=utf-8', '.css': 'text/css; charset=utf-8', '.woff2': 'font/woff2', '.png': 'image/png', '.jpg': 'image/jpeg' };

function html(kind, f, count, id) {
  const [file, who, pos] = f.photo;
  const parts = [];
  parts.push(`<p class="eyebrow">${esc(f.eyebrow || EYE)}${count ? `<span class="count">· ${count}</span>` : ''}</p>`);
  if (f.h1) parts.push(`<h1>${f.h1}</h1>`);
  if (f.num) parts.push(`<p class="num">${f.num}</p>`);
  if (f.lede) parts.push(`<p class="lede">${f.lede}</p>`);
  (f.support || []).forEach((s) => parts.push(`<p class="support">${s}</p>`));
  if (f.list) parts.push(`<div class="list">${f.list.map((s) => `<p>${s}</p>`).join('')}</div>`);
  if (f.cta) parts.push(`<p class="cta">${f.cta}</p>`);
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><title>${id}</title>
<link rel="stylesheet" href="../style.css"></head>
<body><div class="frame ${kind}" style="--pos:${pos}">
 <div class="photo"><img src="../../../../assets/india-free-images/${file}" alt=""><span class="credit">Photo: ${esc(who)} / Unsplash</span></div>
 <div class="band"></div>
 <div class="mark"><img src="../../../../assets/logo/sfw-foundation-wordmark-cream.png" alt="Soil Food Web Foundation"></div>
 <div class="copy">${parts.join('\n')}</div>
</div></body></html>`;
}

function serve() {
  return new Promise((resolve) => {
    const server = http.createServer((req, res) => {
      const file = path.join(REPO, decodeURIComponent(req.url.split('?')[0]));
      if (!file.startsWith(REPO) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); res.end(); return; }
      res.writeHead(200, { 'Content-Type': TYPES[path.extname(file).toLowerCase()] || 'application/octet-stream' });
      fs.createReadStream(file).pipe(res);
    });
    server.listen(0, '127.0.0.1', () => resolve(server));
  });
}

// The list of assets. group = a carousel or a story sequence.
const assets = [];
carousels.forEach((c, ci) => c.slides.forEach((s, si) => assets.push({
  kind: 'post', w: 1080, h: 1350, group: c.slug, frame: s, count: `${si + 1}/${c.slides.length}`,
  id: `${c.slug}-slide-${si + 1}`, out: path.join(INDIA, 'posts', c.slug, `slide-${si + 1}.png`) })));
let n = 0;
stories.forEach((q) => q.frames.forEach((s) => { n++; assets.push({
  kind: 'story', w: 1080, h: 1920, group: q.slug, frame: s, count: '',
  id: `story-${String(n).padStart(2, '0')}`, out: path.join(INDIA, 'stories', `story-${String(n).padStart(2, '0')}.png`) }); }));

(async () => {
  fs.mkdirSync(path.join(HERE, 'html'), { recursive: true });
  for (const a of assets) fs.writeFileSync(path.join(HERE, 'html', `${a.id}.html`), html(a.kind, a.frame, a.count, a.id));
  const server = await serve(); const port = server.address().port;
  const browser = await chromium.launch();

  const measure = async (a) => {
    const page = await browser.newPage({ viewport: { width: a.w, height: a.h }, deviceScaleFactor: 1 });
    await page.goto(`http://127.0.0.1:${port}/content/india/build/html/${a.id}.html`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    a.copyH = await page.evaluate(() => document.querySelector('.copy').getBoundingClientRect().height);
    return page;
  };

  // Pass 1: how tall is the type on each frame.
  for (const a of assets) { const p = await measure(a); await p.close(); }
  // Photograph height. Posts: per slide. Stories: one height per sequence, so a run reads as one piece.
  for (const a of assets) {
    if (a.kind === 'post') a.ph = Math.max(380, Math.min(860, Math.floor(1350 - 56 - a.copyH - 70)));
  }
  for (const q of stories) {
    const run = assets.filter((a) => a.group === q.slug);
    const ph = Math.max(480, Math.min(940, Math.floor(Math.min(...run.map((a) => 1420 - 58 - a.copyH - 24)))));
    run.forEach((a) => { a.ph = ph; });
  }

  // Pass 2: render and check.
  let bad = 0;
  for (const a of assets) {
    const page = await measure(a);
    await page.evaluate((ph) => document.querySelector('.frame').style.setProperty('--ph', ph + 'px'), a.ph);
    await page.waitForTimeout(50);
    const d = await page.evaluate(() => {
      const box = (el) => { const r = el.getBoundingClientRect(); return { x: Math.round(r.x), y: Math.round(r.y), w: Math.round(r.width), h: Math.round(r.height) }; };
      const img = document.querySelector('.mark img');
      const text = [...document.querySelectorAll('.eyebrow, h1, .lede, .support, .list p, .cta')].map((el) => {
        const clone = el.cloneNode(true); clone.querySelectorAll('.count').forEach((c) => c.remove());
        return { what: el.tagName === 'H1' ? 'headline' : el.className || 'list', copy: clone.textContent.trim(), ...box(el) };
      });
      const photo = document.querySelector('.photo img');
      return { band: box(document.querySelector('.band')), text,
        mark: { ...box(document.querySelector('.mark')), loaded: !!img && img.naturalWidth > 0, src: img.getAttribute('src').split('/').pop() },
        photoLoaded: photo.naturalWidth > 0 };
    });
    fs.mkdirSync(path.dirname(a.out), { recursive: true });
    await page.screenshot({ path: a.out });
    await page.close();
    const png = fs.readFileSync(a.out); const pw = png.readUInt32BE(16), ph = png.readUInt32BE(20);
    const onBand = d.text.every((t) => t.y >= d.band.y - 1 && t.y + t.h <= d.band.y + d.band.h + 1);
    const logoOK = d.mark.loaded && d.mark.src.includes('cream') && d.mark.x <= 90 && d.mark.y <= 90;
    const missing = d.text.filter((t) => !COPYN.includes(norm(t.copy))).map((t) => t.copy);
    const lowest = Math.max(...d.text.map((t) => t.y + t.h));
    const bottomOK = a.kind === 'story' ? lowest <= a.h - 500 : lowest <= a.h - 60;
    const sizeOK = pw === a.w && ph === a.h;
    const ok = sizeOK && onBand && logoOK && !missing.length && bottomOK && d.photoLoaded;
    const yn = (v) => (v ? 'yes' : 'NO');
    console.log(`${path.relative(INDIA, a.out)}  photo ${a.ph}px  ${ok ? 'PASS' : 'FAIL'}`);
    console.log(`  1. size ${pw} x ${ph} ${yn(sizeOK)}   2. type on band ${yn(onBand)}   3. logo cream top left ${yn(logoOK)}   4. copy in copy.md ${yn(!missing.length)}   5. ${a.kind === 'story' ? `bottom 500 empty ${yn(bottomOK)} (type ends ${lowest})` : `clears bottom ${yn(bottomOK)} (type ends ${lowest})`}${d.photoLoaded ? '' : '   photo NOT loaded'}`);
    if (missing.length) console.log('  not in copy.md: ' + missing.join(' | '));
    if (!ok) bad++;
  }
  await browser.close(); server.close();
  console.log(bad ? `\n${bad} file(s) failed.` : `\nAll ${assets.length} files pass.`);
  process.exit(bad ? 1 : 0);
})();
