---
doc_type: plan
plan_number: 2
status: review
created: 2026-10-30
last_updated: 2026-10-30
author: Claude (for Rob)
approver: ""
related_docs:
  - docs/plans/PLAN-001-2026-03-15-website-rebuild-astro.md
  - hq/companies/romark.md (Safetech entries 29/10–30/10/2026)
  - Romark-workle/docs/plans/2026-10-30-plan-168-romark-web-content-pipeline.md
---

# PLAN-002: Move the website off Safetech — checklist

**Status**: Review — ROB items are the gate
**Context (hq/companies/romark.md, 30/10/2026)**: Wayne Clatworthy (Safetech MD) has accepted
cancellation and is raising a ticket: SEO + GMB packages end 31/10/2026; the £606 collection due
01/11 cancelled; `romarkengineering.co.uk` transferred to Romark's GoDaddy account; WordPress
export; 301 from `engineeringessex.co.uk` (Safetech-owned) to our domain plus Search Console
access; hosting not renewed March 2027. Standing rule: Romark owns every domain, hosting account
and Google property in its own name; suppliers get manager access only.

Confidence tags: [Certain] = read from the repo, Railway or Nominet record this session;
[Likely] = vendor procedure from memory — this session's network blocks GoDaddy, Nominet,
Google and the old site, so verify before relying on the exact wording.

---

## 0. Decisions needed before anything else

**D1 — canonical domain.** [Certain] The repo disagrees with itself: `astro.config.mjs` says
`https://romarkengineering.co.uk`, `SEO.astro`'s fallback and `PROJECT_STATUS.md` say
`romarkengineering.com`, and the Railway service has BOTH attached. Rob's 30/10 brief says
`.co.uk`. Recommendation: **`romarkengineering.co.uk` canonical**, `.com` 301s to it (one site,
one set of Search Console history). Everything below assumes that.

**D2 — the WordPress export is an archive, not a target.** [Certain] PLAN-001 and three sprints
already rebuilt the 35 pages as Astro (34 prerendered: 14 core + 20 SEO landing), with the
April photo/video shoot integrated. Importing the WP export into a new WordPress host would
throw that away and keep a plugin-update burden. The export is kept for (a) the five service
images the Astro site still lacks, (b) any copy or gallery image not yet carried over,
(c) evidence. Target hosting is the existing Railway project.

**D3 — DNS host.** [Certain, Railway docs read 30/10/2026] Railway needs a CNAME-flattened or
ALIAS record at the root domain, and lists GoDaddy's nameservers as NOT supporting that; its
documented workaround is Cloudflare nameservers. Romark already has a Cloudflare account
(getworkle.com zone). So: **registrar GoDaddy, nameservers Cloudflare** — GoDaddy holds the
domain, Cloudflare serves the DNS.

---

## 1. Domain — `romarkengineering.co.uk` into Romark's name and GoDaddy account

- [ ] ROB: Confirm you hold a GoDaddy account in Romark Engineering Ltd's name (not personal) at https://account.godaddy.com — create it if not. Same account should later hold `.com` if it is elsewhere.
- [ ] ROB: Reply to Wayne's ticket in writing asking for **two things in this order**: (1) Nominet registrant on `romarkengineering.co.uk` set to **Romark Engineering Ltd, 07411656, Unit 8 & 9 Baryta Close, Stanford-le-Hope SS17 0JE**, contact rob@romarkengineering.com; (2) the IPS tag changed to GoDaddy's. [Likely] For .uk domains there is no auth code: the losing registrar changes the IPS tag (GoDaddy's is `GODADDY`), then you accept the transfer inside GoDaddy; GoDaddy's .uk transfer-in is normally free of charge.
- [ ] Verify the registrant after (1) via Nominet's public RDAP (`https://rdap.nominet.uk/uk/domain/romarkengineering.co.uk`) — the earlier `engineeringessex.co.uk` lookup is recorded in hq; the same check works here.
- [ ] ROB: Also ask in the same ticket who the registrar is for **`romarkengineering.com`** (your email domain — [Guessing] not Safetech, but unconfirmed) and that no Safetech nameservers remain on it.
- [ ] Do not let Safetech "point `romarkengineering.co.uk` at the site" on their DNS — the point of the move is that no Romark property depends on Safetech nameservers after March 2027.

## 2. DNS — Cloudflare zone for `romarkengineering.co.uk`

- [ ] ROB: In Cloudflare (https://dash.cloudflare.com) add the zone `romarkengineering.co.uk` (Free plan) and copy the two assigned nameservers.
- [ ] ROB: In GoDaddy, set the domain's nameservers to those two Cloudflare nameservers (after the transfer completes; if Safetech still holds it when the Railway go-live is due, Safetech can set them instead — nameservers, not records).
- [ ] Records (I can add these once the zone exists and you've shared Cloudflare access, or you add them): [Certain, from Railway] root `CNAME @ → uv3px83f.up.railway.app` (proxied, orange), `TXT _railway-verify → railway-verify=312d7b8ecba7193e6de1d6d1f27174833addbcf2ba595ed8de20f7e8a62e0aaa`, `CNAME www → @` (proxied); SSL/TLS mode **Full** (not Full strict — Railway's doc is explicit); Universal SSL on; Bulk Redirect `https://www.romarkengineering.co.uk/*` → `https://romarkengineering.co.uk/$1` 301.
- [ ] Email: `romarkengineering.co.uk` carries no mail today ([Likely] — confirm no MX exists before cut-over so nothing is silently dropped); add `TXT @ "v=spf1 -all"` so the domain cannot be used for spoofing.
- [ ] Railway custom-domain check shows green for `.co.uk` (today: CNAME `REQUIRES_UPDATE`, certificate `ISSUING` — [Certain]).

## 3. The site — make the Astro build production-ready and deploy it

[Certain] Railway project "Romark Engineering Website" (`e17bd70c-90b4-4f7a-81db-5621dcdb39dc`) has one service with a placeholder deployment from 16/03/2026 and **no source repo connected**. Carry-overs from `docs/sessions/2026-04-11.md`: 5–8 MB JPGs, 7.4 MB hero poster, no contact-form rate limit, no GA.

- [ ] Connect the service source to `rocap1982/romark-engineering-website` `main` (I can do this via the Railway tooling with your go-ahead; it is a config change on the website project, not on Workle).
- [ ] Media: run the warehouse/gallery JPGs and the hero poster through sharp → WebP + sized variants; keep originals out of `public/`. (Code change in this repo — small fix.)
- [ ] Contact form: rate limit on `src/pages/api/contact` + `RESEND_API_KEY` set as a Railway variable (names only from here; value is yours).
- [ ] Pull the five missing service images from the WordPress export's `wp-content/uploads` once it arrives (§5).
- [ ] Set `GA_MEASUREMENT_ID` only if you actually want GA4; otherwise leave it unset — the layout already tolerates absence.
- [ ] Smoke test on `romark-engineering-website-production.up.railway.app` before DNS: home, one service page, one SEO page, contact form end to end, `sitemap-index.xml`, `robots.txt`.
- [ ] Cut over DNS (§2). Confirm `https://romarkengineering.co.uk/` serves the Astro site with a valid certificate.

## 4. 301 map — `engineeringessex.co.uk` → `romarkengineering.co.uk`

What Safetech must implement (it is their domain and their host): a **page-for-page 301** for
every old URL, kept live for **at least 12 months** (Google's own guidance for a site move is a
year minimum — [Likely]), plus a catch-all `/* → https://romarkengineering.co.uk/` for anything
not in the map. A homepage-only redirect loses the location-page rankings Rob is paying to
keep (#2 for several location keywords, Dec 2024 — PLAN-001).

- [ ] ROB: Allow `engineeringessex.co.uk` in this session's network settings, or send me the old `sitemap.xml` (`https://engineeringessex.co.uk/sitemap_index.xml` or `/sitemap.xml`) — I cannot reach the old site from here, and the map must come from its real URLs, not from memory.
- [ ] [Certain] The 20 SEO landing pages keep the same slug (SPRINT-003 acceptance: "All 20 page slugs match WordPress URL structure") — these are `/<slug>/ → /<slug>` straight across.
- [ ] The 9 service pages and 6 core pages need their old paths read from the sitemap, then mapped to: `laser-profiling`, `folding-pressing`, `fabrication-and-welding`, `cnc-machining`, `milling`, `turning`, `sheet-metal-welding`, `blank-development`, `cad`, `about-us`, `equipment`, `gallery`, `contact-us`, `/`.
- [ ] Deliver the map to Safetech as a plain CSV (`old_path,new_url,301`) in the ticket; ask them to confirm the implementation method (host-level rule, not a WordPress plugin that dies when WordPress is switched off).
- [ ] Verify with `curl -I` on ten sample URLs: status 301, `Location` = exact new URL, one hop, no 302.
- [ ] Keep the WordPress site running untouched until the redirects are confirmed (PLAN-001 rollback note).

## 5. WordPress export + property handover — what to ask Safetech for, exactly

- [ ] ROB: Ask for a **full site backup**, not only the WXR XML: WordPress export XML, the entire `wp-content/uploads` folder, the theme/plugin list, and a database dump. Store in SharePoint under Users 2/… alongside the existing Safetech folder. [Likely] the XML alone omits media files.
- [ ] ROB: Search Console — ask Safetech to add rob@romarkengineering.com (your Google account) as an **Owner** (not "Full" user) on the `engineeringessex.co.uk` property; delegated-owner is enough for Change of Address, but verified owner is better because it survives them removing you.
- [ ] ROB: Google Business Profile — confirm at https://business.google.com that **you** are Primary owner and Safetech is at most a Manager; remove their access after 31/10/2026. Update the Website field to `https://romarkengineering.co.uk/` on cut-over day.
- [ ] ROB: Google Analytics — ask whether a GA/UA/GA4 property exists for the old site and under whose account; if Safetech's, ask for an export of the last 24 months' pages/sessions (you can't transfer history into a new property).
- [ ] ROB: Ask Safetech to confirm in writing the hosting end date (March 2027) and that `engineeringessex.co.uk` DNS will keep the 301 host alive until then — the redirect is worthless if the domain is parked in February.

## 6. Search Console — Change of Address

Do this only after §2–§4 are live and verified. [Likely] procedure from memory — verify on the
tool's own page at https://search.google.com/search-console before clicking.

- [ ] Verify `romarkengineering.co.uk` as a **Domain property** in Search Console (TXT record in Cloudflare).
- [ ] Submit the new sitemap: `https://romarkengineering.co.uk/sitemap-index.xml`.
- [ ] In the OLD property (`engineeringessex.co.uk`) → Settings → Change of Address → pick the new property → Google checks that the homepage and sampled pages 301 to the new site → Validate & Update.
- [ ] Watch Coverage/Indexing on both properties for 6 weeks (PLAN-001 risk table). Expect a wobble; a cliff means a redirect is wrong.
- [ ] Leave the Change of Address in place; do not remove the old property.

## 7. After cut-over

- [ ] Update the three places in this repo that still say `.com` (`SEO.astro` fallback, `PROJECT_STATUS.md`) — small fix.
- [ ] Phase 2 of Workle Plan 168: on Approve, write the image + alt text + description into this site's gallery data and redeploy — that is what actually replaces the £350/month, not the GBP/LinkedIn email.
- [ ] Diary: Safetech hosting end March 2027; 12-month redirect review 30/10/2027; `romarkengineering.co.uk` renewal date (read from GoDaddy once transferred).
- [ ] hq: log the canonical-domain ruling and the Cloudflare-nameservers decision (done 30/10/2026 for the decision; ruling pending Rob).

---

## Approval

**Approver**: Rob di Capite
**Date Approved**:
**Conditions**: D1 (canonical domain) answered.
