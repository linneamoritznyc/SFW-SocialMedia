
const { chromium } = require(require('child_process').execSync('npm root -g').toString().trim() + '/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium-1194/chrome-linux/chrome' });
  const p = await b.newPage({ viewport: { width: 1080, height: 1350 } });
  for (const f of ["/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-01.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-02.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-03.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-04.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-05.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-06.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-07.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-08.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-09.html", "/home/user/SFW-SocialMedia/renders/october/teachers-day-designs/design-10.html"]) { await p.goto('file://' + f); await p.waitForTimeout(400); await p.screenshot({ path: f.replace('.html', '.png') }); }
  await b.close();
})();