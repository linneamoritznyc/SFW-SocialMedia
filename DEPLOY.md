# Deploying the review site

The site lives in `public/`. It is the social post review tool, not the
Foundation website. `vercel.json` sets `outputDirectory` to `public`, so
**only `public/` is served**. Nothing in `docs/`, `drafts/`, `variants/` or
`assets/` is reachable from the deployed URL.

## Live

**https://sfw-social-media.vercel.app**, password `Wormhole123`.

Vercel project `sfw-social-media`, deployed from **`main`**.

**One setting still to change.** The project's production branch is still the
repository default, `claude/session-gni7rl`, which carries none of this. That is
why the first deploy returned 404. Production was deployed from `main`
explicitly, but until the setting changes, pushes to `main` build as previews
rather than production: Settings, Git, Production Branch, set to `main`.

## The password

`Wormhole123`, checked in `public/index.html`.

**This is a soft gate.** It stops anyone who wanders onto the URL from reading
the page, but the password is in the page source and anyone who opens developer
tools can read it. It is fine for sending a review link to a colleague. It is not
a lock.

Vercel's own Password Protection runs at the edge and never sends the page to an
unauthenticated visitor, which is the real lock. **It needs a Pro plan**, and
this account is not on one: setting it returns 428 invalid_password_protection.

Vercel Authentication was on, which admitted only Vercel team members and so
excluded the reviewer this site exists for. It is now off, so the URL opens for
anyone holding it. It is unlisted and carries `X-Robots-Tag: noindex, nofollow`,
but it is not locked, and it shows a named grower's unpublished trial results
before her consent is in. Do not post the link publicly.

To change the soft password, edit one line in `public/index.html`:

```js
const PASSWORD = "Wormhole123";
```

## Updating the artwork

The images in `public/img/` are renders of the HTML in `variants/`,
`templates/` and `motion/`. After changing any of those:

```sh
sh scripts/render-review.sh      # re-renders review/
rm -rf public/img && mkdir -p public/img
cp -r review/1-graduate-celebration/start-here   public/img/sandra
cp -r review/1-graduate-celebration/more-options public/img/sandra-more
cp -r review/2-umass-amherst  public/img/umass
cp -r review/3-scholarships   public/img/scholarships
cp -r review/4-india-tour     public/img/india
cp -r review/5-templates      public/img/templates
cp -r review/6-motion-stills  public/img/motion
find public/img -name "index.html" -delete
```

Captions, hashtags, status and the schedule are all in `public/posts.js`.
That file is the single place to edit text on the site.

## Note on the deleted Vercel config

`vercel.json` was removed early in this rebuild so the repository could never
deploy as a second copy of the live Foundation site. This one is scoped to
`public/` and carries `X-Robots-Tag: noindex, nofollow`, so it cannot serve the
website and will not be indexed. If the website rebuild later needs its own
Vercel config, the two have to be reconciled before that happens.
