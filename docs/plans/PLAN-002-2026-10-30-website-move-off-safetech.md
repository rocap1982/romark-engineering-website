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

## 1. Domain — `romarkengineering.co.uk` (already Romark's; nothing to ask Safetech)

[Certain, rob@ mailbox 30/10/2026] The domain has been in **Rob's own Fasthosts account (no.
1291216) since 15/03/2026**: Nominet confirmed the IPS tag change to `LIVEDOMAINS` at Rob's
request that evening (the day of the Safetech cancellation email); Fasthosts "Domain Transfer
£0.00" order 15/03/2026; renewed 25/04/2026 (£15.40 inc VAT), **expiry 25/05/2027**. Safetech
invoiced its renewal as late as 05/05/2021, so Wayne's "we look after it" was true once and is
seven months stale. It is NOT at GoDaddy (GoDaddy holds `roamsystems.co.uk` and the
`engineeringessex.co/.uk/.cn/.com.cn` defensive variants).

- [x] [Certain, Fasthosts page 30/10/2026] Registrant **Romark Engineering Limited, UK Limited Company**, Baryta Close address, rob@ contact; registered 25/05/2011; auto-renew 25/04/2027. Ownership rule satisfied — keep the registrar at Fasthosts, no GoDaddy transfer.
- [ ] [Certain] Nameservers are still **`ns0.safetechhosting.co.uk` (+1)** — Safetech hosts only the DNS zone. Move them to Cloudflare NOW (§2), via Fasthosts → domain → "Manage nameservers"; do not wait for the site cut-over, and do not route it through Safetech's ticket.
- [ ] **`romarkengineering.com` is NOT with Safetech** — [Certain, Rob 30/10/2026] its registrar/DNS is held by Ryan Edkins (Workle's upstream author; admin collaborator on `Romark-workle`). It is the company EMAIL domain (M365 MX/SPF/DKIM), so it is the one domain where a DNS slip stops the business. Separate track, not part of the Safetech ticket: ROB: find out whether Romark Engineering Ltd is the registrant of record and which registrar holds it (ICANN lookup: https://lookup.icann.org/en/lookup — registrant is usually redacted, registrar is not); then plan a transfer into Romark's own GoDaddy account with every existing DNS record (MX, SPF, DKIM, DMARC, autodiscover, any verification TXTs) exported and re-created BEFORE nameservers move. Not before the `.co.uk` cut-over — one domain at a time.
  - [Certain, RDAP 30/10/2026] created 26/08/2008, expires 26/08/2027, updated 25/08/2026; nameservers `ns1-3.livedns.co.uk` ([Likely] Fasthosts); registrar via Tucows (tieredaccess.com gateway); **registrant kind = individual, Essex** — a person, not Romark Engineering Ltd.
  - [Certain] Rob's own Fasthosts account carries a "Standard Email – romarkengineering.com" product (£26.53 + VAT/yr) but NO `.com` domain renewal invoice (the only `.com` renewed there is sheetmetallaser.com) — so the `.com` registration is [Likely] in a *different* Fasthosts account (Ryan's), while the email product is legacy from before M365. ROB: check the Fasthosts Domains list — if `romarkengineering.com` is NOT listed, the registration is Ryan's account; if the Standard Email product has no mailboxes in use, cancel it.
  - Order of work: (1) ROB: get the registration into Romark's own Fasthosts account (Fasthosts can move a domain between accounts on both parties' say-so — [Likely]) or obtain the EPP code from Ryan; (2) registrant → Romark Engineering Ltd (07411656), rob@ as contact; (3) export every DNS record and re-create in a Cloudflare zone; (4) switch nameservers to Cloudflare and verify mail flow (send/receive, DKIM pass) the same hour.

## 2. DNS — Cloudflare zone for `romarkengineering.co.uk`

- [x] ROB: In Cloudflare (https://dash.cloudflare.com) add the zone `romarkengineering.co.uk` (Free plan); accept the record import it offers (captures whatever Safetech's zone holds); copy the two assigned nameservers.
- [x] ROB: In Fasthosts → `romarkengineering.co.uk` → Manage nameservers, replace the two `safetechhosting` entries with the two Cloudflare nameservers. Propagation up to 24–48 h; nothing on this domain carries email, so there is no mail risk.
- [x] 30/10/2026: zone created, nameservers `elle` / `miles.ns.cloudflare.com` set at Fasthosts. Import showed Safetech's cPanel default zone (web A 185.26.150.45, mail A 185.26.150.41, MX, SPF naming blue.safetechhosting.co.uk, ftp/imap/smtp/webmail/ipv4). Rob confirmed **no one uses @romarkengineering.co.uk mail**.
- [x] Zone clean-down DONE 30/10/2026 (final: root A 185.26.150.45 proxied, www CNAME @ proxied, _dmarc, _railway-verify, SPF `v=spf1 -all`): delete ipv4/mail/webmail A, ftp/imap/smtp CNAME, MX; SPF → `v=spf1 -all`; add `_dmarc TXT v=DMARC1; p=reject; adkim=s; aspf=s`; add `_railway-verify TXT railway-verify=312d7b8ecba7193e6de1d6d1f27174833addbcf2ba595ed8de20f7e8a62e0aaa`. KEEP root `A 185.26.150.45` + `www CNAME @` (both proxied) until the site is ready.
- [ ] At cut-over: replace root A with `CNAME @ → uv3px83f.up.railway.app` (proxied); SSL/TLS mode **Full** (not Full strict — Railway's doc is explicit); Universal SSL on; Bulk Redirect `https://www.romarkengineering.co.uk/*` → `https://romarkengineering.co.uk/$1` 301.
- [ ] Railway custom-domain check shows green for `.co.uk` (today: CNAME `REQUIRES_UPDATE`, certificate `ISSUING` — [Certain]).

## 3. The site — make the Astro build production-ready and deploy it

[Certain] Railway project "Romark Engineering Website" (`e17bd70c-90b4-4f7a-81db-5621dcdb39dc`) has one service with a placeholder deployment from 16/03/2026 and **no source repo connected**. Carry-overs from `docs/sessions/2026-04-11.md`: 5–8 MB JPGs, 7.4 MB hero poster, no contact-form rate limit, no GA.

- [x] 30/10/2026 18:19 — service source connected to `rocap1982/romark-engineering-website` `main`; first deployment b3054cf1 (0670b40) SUCCESS in 68 s, listening on 8080; auto-deploys on push. Local smoke test first: all routes 200, 404 OK, empty contact POST → 400.
- [x] 30/10/2026 (53a74c3, deploy fe0448d1 SUCCESS 19:07): images 49 MB → 2.3 MB (1920 px, mozjpeg q80, EXIF stripped; seven service PNGs → JPEG, refs updated); videos were 4K HEVC → H.264 720p, 25 MB → 6.7 MB; missing `/images/og-default.jpg` created (SEO.astro pointed every og:image at it).
- [x] 01/11/2026: contact route already had 5/hour/IP + origin check + injection guards (April status was stale). Hardened: `cf-connecting-ip` preferred over spoofable `x-forwarded-for`; honeypot `website` field — bots get a 200 and nothing is sent. Local proof: 6th POST → 429, spoofed XFF still 429, honeypot 200. `RESEND_API_KEY` is already set on the Railway service.
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
