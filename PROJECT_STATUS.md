---
project: romark-engineering-website
status: active
last_updated: 2026-11-22

# "Resume context" pointers (keep these current)
sprint_current_status: docs/sprints/CURRENT_STATUS.md
active_work: "All 3 sprints complete + new media integrated + equipment specs corrected site-wide. Next: media optimisation, rate limiting, deployment"
latest_session_log: docs/sessions/2026-11-04.md
roadmap_next_phase: "LIVE on Railway at romarkengineering.co.uk (main auto-deploys). Next: 301 redirects from engineeringessex.co.uk, rate limiting"
canonical_architecture_decision: ""
active_audits_dir: docs/audits/active/
skills_index: .claude/skills/
canonical_reference_root: docs/reference/
---

This file is the **fastest way to resume work** with minimal context.

## Current State

**Romark Engineering** — precision engineering & sheet metal fabrication website rebuild. Moving from WordPress (engineeringessex.co.uk) to Astro 5 + Tailwind CSS v4.

### FBS Pipeline Status

| Stage | Status |
|-------|--------|
| IDEA-001 (Website Rebuild) | accepted |
| PLAN-001 (Full Rebuild Plan) | approved |
| SPRINT-001 (Foundation Setup) | complete (done) |
| SPRINT-002 (Core Pages) | complete (done) |
| SPRINT-003 (SEO Landing Pages) | complete (done) |

### What Exists

- **Astro foundation built** (Sprint 001): project scaffolding, brand design system, master layout, SEO infrastructure, header/footer components, homepage
- **Core pages built** (Sprint 002): 9 data-driven service pages, About Us, Equipment, Gallery, Contact Us with Resend email form, JSON-LD schemas (Service + ItemList), security-hardened API endpoint
- **SEO landing pages built** (Sprint 003): 20 location-targeted pages from seo-pages.json, FAQ accordion component, Service+areaServed JSON-LD, FAQPage JSON-LD, Footer "Areas We Serve" links
- **Total pages**: 34 prerendered (14 core + 20 SEO landing)
- **Old site archived 04/11/2026**: `archive/engineeringessex-2026-11-04/` (35 pages, 112 images, `report.md` findings, `redirect-map.csv` awaiting new paths); tool: `scripts/archive-site.py`
- **Original WordPress site** (engineeringessex.co.uk): 35 pages (9 service, 6 core, ~20 SEO landing), good SEO rankings (#2 for several location-targeted keywords), Dec 2024: 12,212 impressions, 74 clicks, 215 sessions

### What's Next

- Source missing service images (5 of 9 services)
- Rate limiting for contact form API
- ~~Deployment~~ **DONE — the site is LIVE**: Railway project "Romark Engineering Website", custom domain `romarkengineering.co.uk`, `main` auto-deploys (verified 22/11/2026 via Railway deployments + domains). A merge to main changes what customers see.
- Photo intake (22/11/2026): Rob drops photos from his iPhone into the `Website Photos` folder in his work OneDrive; a session reads them with the ms365 connector (`read_resource` saves the file to disk). iCloud is blocked by the cloud session network policy.
- Domain migration (engineeringessex.co.uk -> romarkengineering.com) with 301 redirects
- Google Analytics integration

Update this file when:
- priorities change,
- the active sprint changes,
- a major decision is made,
- an audit opens/closes meaningful P0/P1 issues,
- canonical references move.
