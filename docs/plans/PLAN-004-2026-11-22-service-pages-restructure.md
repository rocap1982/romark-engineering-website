---
doc_type: plan
number: 004
status: implemented
created: 2026-11-22
author: Claude for Rob
approver: Rob (22/11/2026, in session)
related_issues: []
---

# PLAN-004: Service pages restructure — nine pages to seven, grouped menu

## Problem Statement

### Current State
Nine flat service pages in `src/data/services.json`, listed flat in the header, footer, homepage and contact form. Two are near-duplicates of a sibling (Sheet Metal Welding vs Fabrication & Welding; Blank Development is CAD work, 51 words). Milling and Turning sit beside CNC Machining instead of under it. Sheet metal, Romark's core trade, has no heading.

### Desired State (approved by Rob 22/11/2026)
- Menu groups: **Sheet Metal** (Laser Profiling, Folding & Pressing, Fabrication & Welding), **CNC Machining** (Milling, Turning), **CAD Design**.
- `sheet-metal-welding` merged into `fabrication-and-welding`; `blank-development` merged into `cad`. Seven pages remain.
- Milling and Turning keep their own pages and URLs (`/milling/`, `/turning/` — same as the old engineeringessex.co.uk URLs in `docs/redirects/engineeringessex-301-map.csv`).
- `/sheet-metal-welding/` and `/blank-development/` return 301 to the page that absorbed them.

### Why This Matters
Two pages competing for the same searches dilute both; a menu that mirrors how customers buy (sheet metal vs machining) is clearer.

## Proposed Solution

### Canonical Changes Required
| Document | Change Type | Description |
|----------|------|-------------|
| `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` | Minor | `services.json` gains optional `parent` (slug); two entries removed |

### Proposed Specification
- `services.json` entry: optional `"parent": "<slug>"`. Set on `milling` and `turning` (`"cnc-machining"`).
- Menu groups defined once in `src/data/service-menu.ts`, used by Header, Footer and homepage.
- CNC Machining page lists its children (Milling, Turning) as linked sub-headings; child pages' secondary button points back to CNC Machining.
- Merged content: unique capabilities, equipment and industries of the retired page are added to the absorbing page; metaTitle of CAD Design names blank development so the search term stays on the site.
- `relatedServices` in `seo-pages.json` and `equipment.json`: retired slugs replaced by their target, duplicates removed.
- Redirects: on-demand routes `src/pages/sheet-metal-welding.ts` and `src/pages/blank-development.ts` (`prerender = false`) returning 301, served by the Node adapter.

## Implementation Impact

### Code Changes Required
`src/data/services.json`, `src/data/service-menu.ts` (new), `src/data/seo-pages.json`, `src/data/equipment.json`, `src/components/Header.astro`, `src/components/Footer.astro`, `src/components/ServicePage.astro`, `src/pages/[slug].astro`, `src/pages/index.astro`, `src/pages/contact-us.astro`, two redirect routes.

### Verification
Build passes; 7 service pages + 20 location pages generated; no link to a retired slug left in `dist/`; `curl -I` against the production server returns 301 for both retired URLs; header checked by screenshot on desktop and phone.
