---
last_updated: 2026-04-11
active_sprint: none
stage: idle
---

# Current Status

## Active Sprint

None — Sprint 003 completed.

## Stage

idle

## This Week's Priorities

- [ ] Optimise new media (warehouse jpgs 5–8MB each, banner video 7.6MB) — run through sharp/ffmpeg for WebP + compressed MP4
- [ ] Verify with client: XYZ 710/510 VMC specs + Harrison lathe details for equipment table
- [ ] Verify with client: do they have waterjet capability (claims removed from SEO pages this session)
- [ ] Source missing service images (5 of 9 services)
- [ ] Rate limiting for contact form API
- [ ] Deployment to Railway / Cloudflare Pages
- [ ] Domain migration (engineeringessex.co.uk -> romarkengineering.co.uk) with 301 redirects

## Blockers

None.

## Recently Closed Work

| Work | Date | Notes |
|------|------|-------|
| Equipment specs corrected site-wide | 2026-04-11 | Laser: 12mm/12mm/10mm (5000×1500). HFE 220-4 (4m). Added Barnes + Ward Forsythe hydraulic presses. Replaced CNC fleet with XYZ 710/510 + Bridgeport/XYZ manual mills + Harrison lathe. New "Metal Finishing" category. Updated across equipment.json, services.json, seo-pages.json, index.astro, about-us.astro, equipment.astro |
| New media assets integrated | 2026-04-11 | Banner video on homepage hero, workshop clip on About, warehouse photos on About/Equipment/Gallery, 4 product shots added to gallery. Hero.astro gained `backgroundVideo` + `posterImage` props |
| SPRINT-003 SEO Landing Pages completed | 2026-03-16 | 20 location-targeted pages, FAQ accordion, Service+FAQPage JSON-LD, Footer "Areas We Serve" |
| SPRINT-002 Core Pages completed | 2026-03-16 | 9 service pages, About Us, Equipment, Gallery, Contact Us + API, security hardening |
| SPRINT-001 Foundation Setup completed | 2026-03-16 | Astro scaffolding, brand design, layout, SEO, header/footer, homepage |
| PLAN-001 created + approved | 2026-03-15 | Full contract plan with data schemas, API, SEO |

## Notes / Decisions

- All 34 pages now prerendered (14 core + 20 SEO landing); all build clean in ~3.5s
- Homepage hero now uses `/videos/romark-banner.mp4` (7.6MB, autoplay/muted/loop) with `warehouse-welder.jpg` poster
- About Us has embedded `/videos/romark-workshop-clip.mp4` (17MB, controlled playback) in a new "Inside Our Workshop" section
- Skipped `.mov` variant (2.1GB — not web-suitable)
- Warehouse jpgs are 7–8MB raw — acceptable for dev but must be optimised before production deploy
- Equipment data now reflects current shop floor (per client's 2026-04-11 update); old `.claude/launch.json` port 4321 changed to 4329 (stale process was holding 4321)
- Site ready for deployment pending: media optimisation, service images, rate limiting, Railway setup, domain migration
