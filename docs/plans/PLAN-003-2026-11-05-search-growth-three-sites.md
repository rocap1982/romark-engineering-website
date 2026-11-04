---
plan: PLAN-003
title: Search growth for Romark, RJ Waller and ROAM — one engine, three sites
status: proposed (Rob to read 05/11/2026)
author: Claude for Rob, written overnight 04→05/11/2026
scope: romarkengineering.co.uk · rjwaller.co.uk · roamsystems.co.uk · Google Business Profiles · Workle content engine
---

# PLAN-003 — Search growth for the three sites

Rob's brief (04/11/2026, 21:05): "Formulate a plan to get us ranking high on Google. Link Roam, Romark and Wallers so each site helps each other's business and rankings. Think broadly. Think about scheduled drops." Written from evidence gathered tonight; every claim carries a confidence tag. Dates dd/mm/yyyy, prices ex VAT unless stated.

## 0. The short version

1. **Romark has almost no search footprint today.** [Certain] A search for "Romark Engineering" Stanford-le-Hope tonight returned nothing about the company. The old site was never a ranking asset: no page edited since 28/05/2024, 20 cloned town pages, and a hidden block of 105 links pointing at Safetech's own sites. Losing engineeringessex.co.uk costs less than it feels.
2. **The local map pack, not the website, is where fabrication enquiries come from.** [Likely] That is driven by the Google Business Profile: category, photos, posts, reviews, proximity. Safetech managed Romark's profile; whether Romark still owns it is unknown and is the first thing to settle.
3. **The three sites do not link to each other at all.** [Certain, grep of both Astro repos] Linking them honestly ("made by", "sister company") is cheap, legitimate and helps Google understand the group. It is not a ranking trick and will not behave like one.
4. **ROAM is the strongest asset and already has a content scheduler.** [Certain] 1,112 search clicks in the last three months, 32 pages indexed, 59 not indexed, a blog, a Google Merchant feed, and a weekly Monday content-drafting job that emails drafts to sales@. The model for "scheduled drops" exists; it needs to be copied to Romark and governed.
5. **RJ Waller is a black box.** [Certain] The repo is empty, the site blocks automated fetches, and the only known asset is a 5.0-rated Google Business Profile. It needs a 30-minute manual look before it gets a plan of its own.
6. **The engine is Workle, not a marketing agency.** The romark-web module already turns a workshop photo into a Google post, a LinkedIn post and alt text in 25 seconds with Rob as the only approver. This plan extends that into a calendar with scheduled publishing, and adds measurement so we know what is working within eight weeks instead of guessing.

Cost of everything below: £0 in subscriptions. Optional spend is flagged where it appears.

## 1. Evidence gathered tonight

| Site | State | Source |
|---|---|---|
| romarkengineering.co.uk | Live on Railway via Cloudflare since 04/11; 34 pages (9 services, 6 core, 20 location pages with the Safetech-era slugs kept); JSON-LD, sitemap, robots; Search Console verified 04/11, sitemap submitted, not yet crawled; no analytics | PLAN-002, this session |
| roamsystems.co.uk | Astro 6 on Railway; 9 products, 6 vehicle pages, 7 blog posts (3 still drafts), gallery, certifications, installers; Stripe checkout; Merchant feed; weekly content job + monthly calendar refresh emailing drafts to sales@; SEO/legal audit closed 12/06/2026; **open**: non-www→www 301 blocked because the Cloudflare zone sits in Identity Pixel's account (breaks the 30/10 ownership rule); GSC 1,112 clicks, 32 indexed / 59 not | `roamsystems-website/PROJECT_STATUS.md`; GSC screenshot 04/11 |
| rjwaller.co.uk | Unknown build; blocks automated fetches; repo `RJ-waller-website` empty; GBP live since 03/2026, 5.0 rating | hq `companies/wallers.md` |
| Search results | "sheet metal fabrication Essex": SAMS Fabrications, A&R Engineering, Tab Sheet, JD Fabrication, Addition Metal Fabrication, then directories (Checkatrade, Construction.co.uk). "CNC machining Essex": Geomiq, Chester Hall, Tridan, then job ads. "M1 crash tested campervan seat bed": retailers (Rusty Lee via TransporterHQ, Just Kampers) and forums. No result for Romark on any of them. | WebSearch 04/11 (US-weighted index, so treat as indicative) |
| Safetech's SEO reports | None found in jobs@ among 335 Safetech emails; only invoices and "we tried to contact you". There is no record of what the old site ranked for. | Outlook search 04/11 |

Reading of the competition [Likely]: thin. The Essex fabrication results are small firms with basic sites plus directories, which means a well-structured site with real photos, real capability detail and a worked Business Profile can reach page one for the county-level terms within a few months. The campervan market is the opposite: crowded with retailers and forums, where ROAM's M1 claim is the only durable differentiator and must be stated precisely (the 06/2026 audit already corrected its scope).

## 2. How Google actually decides (the bit that shapes everything else)

- **Map pack (local)**: Business Profile completeness, primary category, photos and posts, review count and recency, proximity to the searcher, and whether the website confirms the same name, address and phone. Reviews and photos move it fastest. [Likely, from Google's own local ranking guidance]
- **Organic**: does the page answer the query better than the others (specifics, photos, proof), do other reputable sites point at it, is it fast and indexable. Since 2022 Google demotes templated location pages that only swap the town name. [Certain on the policy, Likely on the effect here]
- **Cross-linking sites you own**: fine when it reflects reality and sits in context (a "Made in Essex by Romark Engineering" line on ROAM, a "Precision machining by our sister company RJ Waller" line on Romark's CNC page). Harmful when it is a sitewide footer blast of keyword links in every direction. Same-owner links carry little authority anyway; the value is entity clarity and sending real customers to the right company. [Likely]
- **Timescale**: a new domain typically takes 3–4 months to settle. Expect the Romark numbers to look poor until February 2027 whatever we do; the work in weeks 1–6 is what makes March good. [Likely]

## 3. Entity structure: make the group legible

- **Romark Engineering Ltd** — manufacturer; sheet metal, laser, fold, weld; BS EN 1090 EXC2, ISO 9001. Hub site.
- **RJ Waller Precision Engineers Ltd** — sister company, 50/50; CNC milling and turning. Separate legal entity, separate site, separate Business Profile.
- **ROAM Systems** — product brand, IP in Romark Holdings, manufactured by Romark. Product site with checkout.

Actions:
- Organisation JSON-LD on all three with `sameAs` pointing at the others, the LinkedIn pages and the Business Profiles; identical name/address/phone formatting on each site and each profile. [Me]
- A short **"Our group"** page on romarkengineering.co.uk (three paragraphs, one photo each, honest wording about ownership) and a one-line footer credit on the other two: "Part of the Romark Engineering group, Stanford-le-Hope, Essex". [Me, Rob approves wording]
- Contextual links only where they help a customer: Romark CNC page → RJ Waller; RJ Waller fabrication mentions → Romark; ROAM certifications/about → Romark; Romark gallery → ROAM product. No link blocks, no keyword anchors. [Me]

## 4. Keyword targets, one cluster per site

[Guessing on search volume: no UK keyword tool is available from here. Search Console will give real numbers within 8 weeks; the list is re-ranked then.]

| Site | Primary | Supporting | Page that carries it |
|---|---|---|---|
| Romark | sheet metal fabrication Essex | laser cutting Essex, CNC folding, MIG/TIG welding fabrication Essex, BS EN 1090 fabricator, sheet metal London / Kent / Basildon | home, service pages, the rewritten location pages |
| RJ Waller | CNC machining Essex | CNC turning Essex, precision engineers Stanford-le-Hope, sliding-head turning (Star SR-32J), stainless turned parts | home + 3 capability pages |
| ROAM | campervan seat bed M1 tested | VW T6 seat bed, Transit Custom campervan seats, campervan kitchen pod UK, U-shape vs rock and roll | product, vehicle and blog pages (already exist) |

Rule for the 20 Romark location pages: keep the slugs (they were in the old sitemap, any residual equity lands there) but rewrite each so it says something only Romark can say for that place or service: machine limits (AF4000 bed 5000×1500, 12 mm steel, 10 mm aluminium), lead times, certifications, a real job photo. Two pages a week until done. Pages that cannot be made genuinely different get merged and 301'd.

## 5. The content engine and scheduled drops

**What exists**: romark-web (live 04/11): WEB photo → draft Google post, LinkedIn post, alt text, target page → Rob approves → pack emailed to rob@. ROAM: Monday 09:00 job drafts blog + social copy to sales@; monthly calendar refresh on the 1st.

**Cadence** (the "drops"):

| Drop | Romark | RJ Waller | ROAM |
|---|---|---|---|
| Google Business Profile post with photo | weekly, Tuesday | fortnightly | fortnightly |
| LinkedIn company post | fortnightly | monthly | fortnightly |
| Website gallery item (approved photo + alt text) | weekly | monthly | with each product/vehicle update |
| Case study page (job with customer permission, NDA-screened) | monthly | quarterly | quarterly (installer story) |
| Blog / guide post | — (not a blog site) | — | twice a month (pipeline exists) |
| Service / product page refresh | one page a fortnight (location pages first) | quarterly | quarterly |
| Review request after completed job | automatic 24 h after Order Complete, opt-in per client (built, needs the review link) | later, via Waller Workle | post-purchase email (Stripe) |

**Mechanics I will build in Workle (Plan 168 Phase 2, needs a plan + Rob's OK because it touches the schema)**:
1. `scheduled_for` on a web content item and a **Calendar** tab on `/romark/web-content`: Rob approves on Friday, picks a slot or accepts the next free one; nothing publishes without an approved item in the slot.
2. **Gallery publish**: an approved item is committed to the website repo's gallery data on its date (JPEG + alt text + target page); Railway rebuilds; the item shows on the service page it targets. Fully automatic once approved.
3. **Morning-brief line** every Monday: "Content: 2 slots this week, 1 filled" so an empty week is visible, not silent.
4. **Google post publishing**: the Business Profile API needs Google to approve API access for the account, which takes weeks and sometimes fails for small businesses. [Likely] Until then the pack email stays the path: Rob pastes. Apply for access anyway in week 1.
5. **LinkedIn publishing**: the organisation-post API needs LinkedIn partner approval; not worth chasing. Paste from the pack. [Certain on the restriction]
6. **ROAM**: point its Monday job at the same approval queue so one page governs all three brands (ROAM items tagged by brand, Adam Healey as an approver for ROAM only, Rob for the rest).

**Supply**: the engine starves without photos. Standing ask to the shop floor: one phone photo of anything finished and non-confidential, emailed to Romarkagent@ with subject WEB, any day. Cap stays at 20 a day.

## 6. Links and authority that mean something

Only links a real person would create. In order of effort:

1. **Internal links** on each site (service pages → gallery → case studies → contact). [Me]
2. **Cross-site links** as in §3. [Me]
3. **Certification bodies**: the BS EN 1090 certificate (0513ISO-cpr-26242-003) and the ISO 9001 certificate each have an issuing body with a public register; make sure Romark's entry is current and links to the .co.uk. [Rob to name the bodies; I draft the requests]
4. **ROAM installers**: ~17 approved installers; each installer page on roamsystems.co.uk links out, and most would link back to "approved ROAM installer" if asked. That is the single best link source in the group. [Me to draft the email, Adam to send]
5. **Suppliers and customers** who publish partner or case-study pages (GSF Slides, Southco/Zygology, Seat Surgeons, Evolution Vans for ROAM; Ford SVO and Ricardo are off limits under NDA). Ask only where there is a story. [Rob decides who]
6. **Local**: Essex Chambers of Commerce member directory, Thurrock Council business support, Made in Britain membership (fee applies [Guessing on amount, check madeinbritain.org before deciding]), Thurrock Gazette for a genuine story (apprenticeships, the Made Smarter grant if awarded, the solar expansion).
7. **LinkedIn company pages** for all three, kept alive by the fortnightly drops; LinkedIn pages rank for brand searches on their own.

Not doing: directory spam, paid links, guest-post networks, anything Safetech did.

## 7. Reviews

- **Romark**: the review-request automation is built and waiting for `ROMARK_GOOGLE_REVIEW_URL`. That link comes from the Business Profile once ownership is confirmed. Opt-in per client on `/romark/web-content` → Reviews; start with five friendly repeat customers.
- **RJ Waller**: already 5.0; keep the count moving with a manual ask after each job until Waller Workle carries the same automation.
- **ROAM**: add a review ask to the Stripe order-confirmation email 14 days after dispatch; installers can ask end customers too.

## 8. Technical work per site

- **Romark**: done this week (region, health check, CI, uptime, fonts, CSP). Remaining: Cloudflare Web Analytics snippet (free, no cookie banner needed), Organisation schema update, "Our group" page, cross-links. Watch Search Console for the first crawl of the sitemap.
- **ROAM**: (a) the 59 not-indexed pages need a look — likely legacy Shopify URLs, policy pages and duplicates; (b) move the Cloudflare zone from Identity Pixel's account into Rob's, same rule as Romark; (c) then the non-www→www 301; (d) finish the three draft blog posts. [Me, one PR each]
- **RJ Waller**: 30-minute manual audit by Rob or Chris (what it is built on, who hosts it, whether it has a sitemap). If it is an old builder site, rebuild it on the Romark Astro template: same code, different data, two days' work, hosted on Railway for a few pounds a month. The empty repo suggests this was already the intention.

## 9. Measurement, or we are guessing again

- Search Console on all three domains in Rob's Google account (Romark done 04/11; ROAM exists; Waller to add).
- Cloudflare Web Analytics on all three (free, privacy-safe, no consent banner).
- A **monthly search report** in Workle's morning brief on the first Monday: clicks, impressions, top queries, top pages, map-pack actions from the Business Profile, review count, per site, month on month. Search Console has an API; read access via a service account Rob adds to each property. [Me, after the Phase 2 plan]
- Decision rule: anything that has not moved after eight weeks gets changed, not repeated.

## 10. Optional paid bridge

While the new domain settles, a small Google Ads search campaign for "sheet metal fabrication Essex" and "laser cutting Essex" with the county as the only location would put Romark on page one tomorrow. [Guessing] £10–15 a day is enough for the volume these terms carry. Not required; worth it only if the order book has room in January. The real value is the search-term data it hands back, which also sharpens §4.

## 11. First 90 days

| Weeks | Romark | RJ Waller | ROAM | Engine |
|---|---|---|---|---|
| 1–2 | Confirm GBP ownership, set website field, get review link, set `ROMARK_GOOGLE_REVIEW_URL`; Organisation schema + "Our group" page + cross-links; Cloudflare analytics; first two location pages rewritten | Rob/Chris 30-min audit; add Search Console | Cloudflare zone moved to Rob; non-www 301; Search Console check of not-indexed pages | Plan 168 Phase 2 written (calendar, scheduled publish, gallery commit, brief line); staff told about WEB photos |
| 3–6 | Weekly GBP post + gallery item; two location pages a week; first case study; certification-body listings; apply for GBP API access | Decide rebuild or not; if rebuild, Astro template, 2 days | Installer back-link emails sent; draft blog posts finished; review ask in order email | Phase 2 built and live; Monday brief line running |
| 7–12 | Cadence holds; Essex Chambers / Made in Britain decision; second and third case studies; Search Console review at week 8 and §4 re-ranked | Waller site live on new template with 3 capability pages; GBP posts fortnightly | Two posts a month; product page refresh with new photos | First monthly search report (early January); 90-day review with numbers |

## 12. Who does what

**Me, without asking** (each as its own small PR, reported when live): schema and cross-links on Romark and ROAM; "Our group" page draft; Cloudflare analytics; location-page rewrites two a week; ROAM not-indexed investigation; installer and certification-body email drafts; Plan 168 Phase 2 plan document; monthly report once the API access exists.

**ROB:** (one at a time, as usual)
- [x] 04/11/2026 22:00 — Rob is primary owner of both Romark and RJ Waller profiles (personal Gmail; move to a company account later). Safetech removed as manager. Name changed from Safetech's stuffed "Romark Engineering | Metal Fabrication | Sheet Metalwork | Essex" to "Romark Engineering Ltd" (pending, no re-verify). Description rewritten (plant + certs + sister companies). Website field engineeringessex.co.uk → romarkengineering.co.uk. Categories already right.
- ROB: Copy the "Ask for reviews" link from the Romark profile and paste it to me so I can set `ROMARK_GOOGLE_REVIEW_URL`.
- ROB: Ask Chris for 30 minutes on rjwaller.co.uk: what it is built on, who hosts it, whether he wants it rebuilt on the Romark template.
- ROB: Tell the shop floor the WEB photo rule (one line in the Monday meeting is enough).
- ROB: Approve the "Our group" wording and the footer credit line when I send them.
- ROB: Name the two certification bodies (BS EN 1090, ISO 9001) so I can check their registers.
- ROB: Decide on the optional Ads bridge and the Made in Britain membership once I have the fee.

## 13. Risks and limits

- **NDA leakage** in photos: the five moderation flags are advisory and Rob is the only approver; the module never auto-publishes. Case studies need written customer permission; Ford and Ricardo stay out.
- **Doorway pages**: the 20 location pages are a liability until rewritten; the rewrite schedule in §4 is the mitigation, and pages that cannot be made distinct are merged.
- **Cross-link spam**: §3 keeps links contextual and few; if Google ever treats them badly the fix is removal, not penalty recovery.
- **Time**: the cadence in §5 costs Rob about 20 minutes a week of approvals once the calendar exists. If that slips, the Monday brief line will say so.
- **Measurement gap**: nothing in §4 is backed by UK search volumes tonight. The first Search Console review at week 8 replaces the guesses.
- **Unverified**: rjwaller.co.uk and roamsystems.co.uk could not be fetched from this session, and search results came from a US-weighted index. Both are flagged where they matter.
