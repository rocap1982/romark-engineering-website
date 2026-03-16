---
doc_type: sprint
number: 003
status: complete
stage: done
created: 2026-03-16
last_updated: 2026-03-16
dates:
  start: 2026-03-16
  end: 2026-03-16
sprint_goal: "Build ~20 data-driven SEO landing pages with location-targeted content, FAQ sections, and Service+areaServed JSON-LD schemas"
---

# SPRINT-003: SEO Landing Pages

## Summary

Build the ~20 location-targeted SEO landing pages that drive organic search traffic for Romark Engineering. These pages target "{service} {location}" keyword combinations (e.g., "precision engineering essex", "laser cutting basildon") which the existing WordPress site already ranks for. Content is data-driven from `seo-pages.json`, rendered via a shared dynamic route, and includes FAQ sections with `FAQPage` JSON-LD for rich snippet eligibility.

- **Stage**: done
- **Scope**: `seo-pages.json` data file, SEO landing page template/component, FAQ component, dynamic routing integration, JSON-LD (Service + FAQPage), internal linking
- **Out of scope**: Domain migration/redirects, deployment to Railway, rate limiting, missing service images, Google Analytics integration

## Acceptance Criteria

- [x] `src/data/seo-pages.json` contains all ~20 SEO landing pages with full content (slug, title, meta, h1, content, targetKeywords, relatedServices, location, faqs)
- [x] Each SEO page renders at its correct root-level slug (e.g., `/precision-engineering-essex/`, `/laser-cutting-basildon/`)
- [x] No slug conflicts between SEO pages and service pages
- [x] Each SEO page includes: hero with location, main content (800-1500 words), related services links, FAQ section, CTA
- [x] Each SEO page has correct SEO meta (title, description, canonical URL, OG tags)
- [x] Each SEO page has JSON-LD: `Service` schema with `areaServed` for the target location
- [x] Each SEO page with FAQs has JSON-LD: `FAQPage` schema for rich snippet eligibility
- [x] FAQ component renders as an accessible accordion (keyboard navigable, aria attributes)
- [x] Related services section links to the correct service pages built in Sprint 002
- [x] `npm run build` succeeds with all ~34 pages prerendered (14 existing + ~20 new)
- [x] All new pages appear in the sitemap

## Contracts / Governance

- Contract-impacting changes expected: Yes — new data schema (`seo-pages.json`), new JSON-LD schemas (`FAQPage`)
- Plans: `docs/plans/PLAN-001-2026-03-15-website-rebuild-astro.md` (approved 2026-03-15) — `seo-pages.json` schema defined in "Data Schema: `src/data/seo-pages.json`" section
- Note: The `seo-pages.json` schema is already approved in PLAN-001. No additional plan approval needed.

## Work Plan

### Phase 1: Data File — Content Creation
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Create `src/data/seo-pages.json` with all ~20 SEO pages — scrape/adapt content from WordPress site, populate per PLAN-001 schema (slug, title, metaTitle, metaDescription, h1, content, targetKeywords, relatedServices, location, faqs) | [Data] | P0 | 120min | Done |

**SEO pages created** (20 pages, grouped by location):

**Essex (8)**: precision-engineering-essex, sheet-metal-fabrication-essex, machining-essex, sheet-metal-essex, laser-cutting-essex, cnc-milling-essex, stainless-steel-essex, metal-fabrication-essex

**London (5)**: sheet-metal-fabrication-london, precision-engineering-london, sheet-metal-london, aluminium-welding-london, prototype-engineering-london

**Basildon (2)**: precision-engineering-basildon, laser-cutting-basildon

**Kent (2)**: precision-engineering-kent, cnc-machining-kent

**General (3)**: fabrication-contractors, prototype-engineering-services, sheetmetal-work

### Phase 2: Components
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Create `src/components/FAQ.astro` — accessible accordion component with keyboard nav, aria-expanded, smooth open/close animation | [UI] | P0 | 45min | Done |
| Create `src/components/SeoLandingPage.astro` — page template with hero (h1 + location), main content area, related services grid, FAQ section, CTA | [UI] | P0 | 60min | Done |

### Phase 3: Routing Integration
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Update `src/pages/[slug].astro` to handle both service pages (from services.json) and SEO pages (from seo-pages.json) — use data source to determine which template to render | [UI] | P0 | 30min | Done |
| Add JSON-LD `Service` schema with `areaServed` for each SEO page (location-specific) | [UI] | P0 | 20min | Done |
| Add JSON-LD `FAQPage` schema for pages with FAQs (array of Question+Answer) | [UI] | P0 | 20min | Done |
| Add internal links: related services section linking to `/laser-profiling/`, `/cnc-machining/` etc. | [UI] | P1 | 15min | Done |

### Phase 4: Navigation + Discoverability
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Add "Areas We Serve" section to Footer linking to key SEO pages | [UI] | P1 | 20min | Done |
| Verify all new pages appear in sitemap after build | [Test] | P1 | 10min | Done |

### Phase 5: Verification
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Run `npx astro check` — confirm no type errors | [Test] | P0 | 10min | Done |
| Run `npm run build` — confirm all ~34 pages prerender successfully | [Test] | P0 | 10min | Done |
| Verify no slug conflicts between service and SEO pages | [Test] | P0 | 10min | Done |
| Visual review of 3-5 representative SEO pages (different locations) | [Test] | P1 | 20min | Done |
| Verify FAQ accordion opens/closes correctly, keyboard accessible | [Test] | P1 | 10min | Done |
| Verify related services links point to correct service pages | [Test] | P1 | 10min | Done |

## Test Plan

### Automated
```bash
# TypeScript type checking
npx astro check
# Result: 0 errors, 0 warnings, 4 hints — PASSED

# Production build (catches template errors, missing imports, data issues)
npm run build
# Result: 34 pages prerendered (14 existing + 20 new) — PASSED

# Verify all 20 SEO page slugs exist in build output
# Result: All 20 slugs confirmed in dist/client/ — PASSED

# Verify JSON-LD in build output
# FAQPage and areaServed both present in precision-engineering-essex — PASSED
```

### Manual
- [x] SEO page loads with correct h1, location-specific content, and hero
- [x] FAQ accordion opens/closes items, only one open at a time (or all toggleable)
- [x] FAQ accordion is keyboard accessible (Enter/Space to toggle, Tab to navigate)
- [x] Related services section shows correct service links for the page's relatedServices
- [x] JSON-LD contains `@type: Service` with `areaServed` matching the page's location
- [x] JSON-LD contains `@type: FAQPage` with correct Question/Answer pairs
- [x] Meta title and description are page-specific (not generic)
- [x] Pages with different locations show different content (not just find-and-replace location names)
- [x] Footer "Areas We Serve" links navigate to correct SEO pages
- [x] All 20 SEO pages appear in sitemap.xml

## Review Gate

- [x] All acceptance criteria met
- [x] All automated tests pass (`astro check` + `npm run build`)
- [x] Manual test checklist complete
- [x] 3-5 representative SEO pages visually reviewed
- [x] FAQ accessibility verified
- [x] No 404 links from SEO pages to service pages

## Documentation DoD

- [x] Update `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` with `seo-pages.json` schema
- [x] Update `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` if routing pattern changed
- [x] Update `docs/reference/GLOBAL_TERMINOLOGY_INDEX_CANONICAL.md` with new terms (SEO landing page, areaServed, FAQPage)
- [x] Update `PROJECT_STATUS.md` to reflect Sprint 003 completion

## Audit Plan

Mini audit after sprint completion — verify:
- [x] seo-pages.json schema matches PLAN-001 specification
- [x] All SEO page slugs match WordPress URL structure (for future 301 redirects)
- [x] No slug conflicts between services.json and seo-pages.json
- [x] JSON-LD FAQPage schema follows schema.org specification
- [x] Internal links between SEO pages and service pages are bidirectional where appropriate

Audit: `docs/audits/active/AUDIT-003-2026-03-16-seo-landing-pages.md` — **PASS**

## Notes

### Learnings (Step 4)

1. **Merged dynamic route pattern works well**: Combining services and SEO pages in a single `[slug].astro` with type discriminator (`type: 'service' | 'seo'`) is clean and avoids duplicate routing logic. This pattern should be reused if additional data-driven page types are added.

2. **JSON-LD array support was a prerequisite**: The SEO.astro component needed to be updated to accept `Record<string, unknown>[]` before SEO pages could have both Service and FAQPage schemas. This was a small but critical infrastructure change.

3. **Empty location edge case**: General SEO pages (fabrication-contractors, prototype-engineering-services, sheetmetal-work) have empty `location` fields. The SeoLandingPage template needed conditional checks in three places (hero subtitle, related services text, CTA text) to avoid "in " with no location.

4. **CSS grid-rows transition for accordion**: Using `grid-rows-[0fr]` / `grid-rows-[1fr]` with CSS transitions provides smooth open/close animation without JavaScript height calculations. This is the same pattern used in the header mobile menu.

5. **Content as HTML in JSON**: Storing page content as HTML strings in seo-pages.json with `set:html` rendering works well for rich content (headings, lists, links, bold). Global CSS scoping via `.seo-content` class keeps styling consistent without per-page overrides.

6. **Dev server requires restart for new data files**: After creating seo-pages.json and updating [slug].astro, the running dev server showed 404 for new pages. Restarting the dev server resolved this (same issue as Sprint 002).

### Skills Decision (Step 5)

No new skill needed. The SEO landing page pattern is straightforward data-driven page generation — the same `[slug].astro` + JSON data pattern established in Sprint 002 for services.

### Plan/Idea Review (Step 6)

Sprint 003 aligns with PLAN-001 specifications:
- seo-pages.json schema matches the plan's "Data Schema: `src/data/seo-pages.json`" section
- All 20 page slugs match the WordPress URL structure for future 301 redirects
- JSON-LD schemas (Service + FAQPage) implemented as specified
- No scope gaps or deviations from the plan
- Footer "Areas We Serve" links added for discoverability (not explicitly in PLAN-001 but a natural addition)
