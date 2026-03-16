---
doc_type: sprint
number: 002
status: complete
stage: done
created: 2026-03-16
last_updated: 2026-03-16
dates:
  start: 2026-03-16
  end: 2026-03-16
sprint_goal: "Build all core content pages: 9 service pages (data-driven), About Us, Equipment, Gallery, and Contact Us with working email form"
---

# SPRINT-002: Core Pages

## Summary

Build out the full page set for the Romark Engineering website. This includes 9 data-driven service pages, 4 core informational pages (About Us, Equipment, Gallery, Contact Us), a working contact form with Resend email delivery, and the data files (services.json, equipment.json) that power them. Content is scraped from the existing WordPress site and adapted for the new design.

- **Stage**: done
- **Scope**: Service pages, About Us, Equipment, Gallery, Contact Us, data files, contact form API, service page JSON-LD
- **Out of scope**: SEO landing pages (~20 location pages — Sprint 003), domain migration/redirects, deployment to Railway

## Acceptance Criteria

- [x] `src/data/services.json` contains all 9 services with full content (name, slug, description, capabilities, materials, equipment, image, meta)
- [x] `src/data/equipment.json` contains equipment catalog grouped by category
- [x] 9 service pages render at their correct slugs (e.g. `/laser-profiling/`, `/cnc-machining/`)
- [x] Each service page includes: hero, description, capabilities list, related equipment, CTA, correct SEO meta + JSON-LD (Service schema)
- [x] About Us page at `/about-us/` with company history, team info, certifications
- [x] Equipment page at `/equipment/` with categorized equipment table and JSON-LD (ItemList)
- [x] Gallery page at `/gallery/` with image grid (using extracted images from WordPress)
- [x] Contact Us page at `/contact-us/` with form (name, email, phone, company, service dropdown, message)
- [x] `POST /api/contact` endpoint sends email via Resend API to jobs@romarkengineering.com
- [x] All new pages use the existing Layout/Header/Footer/SEO components
- [x] `npm run build` succeeds with no errors
- [x] All nav links in Header and Footer resolve to real pages (no 404s)

## Contracts / Governance

- Contract-impacting changes expected: Yes — new data schemas (services.json, equipment.json), new API endpoint (POST /api/contact)
- Plans: `docs/plans/PLAN-001-2026-03-15-website-rebuild-astro.md` (approved 2026-03-15) — schemas and API contract defined in sections "Data Schema" and "API Contract"

## Work Plan

### Phase 1: Data Files — DONE
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Create `src/data/services.json` — populate all 9 services with content scraped from WordPress | [Data] | P0 | 60min | DONE |
| Create `src/data/equipment.json` — equipment catalog by category from WordPress /equipment/ page | [Data] | P0 | 30min | DONE |
| Organize extracted images into `public/images/services/` (rename from extracted folder) | [Data] | P1 | 15min | DONE |

### Phase 2: Service Page Template + Pages — DONE
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Create `src/pages/[slug].astro` dynamic route using services.json data | [UI] | P0 | 45min | DONE |
| Create `src/components/ServicePage.astro` — reusable service page layout (hero, content, capabilities, equipment, CTA) | [UI] | P0 | 60min | DONE |
| Add JSON-LD `Service` schema to service pages (linked to existing LocalBusiness) | [UI] | P0 | 20min | DONE |
| Ensure service images from extracted folder are wired to correct pages | [UI] | P1 | 15min | DONE (5 services missing images — deferred, not blocking) |

### Phase 3: Core Pages — DONE
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Create `src/pages/about-us.astro` — company history, values, team, certifications | [UI] | P0 | 45min | DONE |
| Create `src/pages/equipment.astro` — categorized equipment table with JSON-LD ItemList | [UI] | P0 | 45min | DONE |
| Create `src/pages/gallery.astro` — image grid using extracted images | [UI] | P1 | 30min | DONE |
| Create `src/components/GalleryGrid.astro` — responsive image grid (optional lightbox) | [UI] | P1 | 30min | Skipped — inline grid in gallery.astro sufficient |

### Phase 4: Contact Form + API — DONE
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Create `src/pages/contact-us.astro` — form with fields: name, email, phone, company, service dropdown, message | [UI] | P0 | 45min | DONE |
| Create `src/components/ContactForm.astro` — client-side validation + fetch submission | [UI] | P0 | 30min | Skipped — inline in contact-us.astro |
| Create `src/pages/api/contact.ts` — POST handler with validation + Resend email delivery | [API] | P0 | 45min | DONE |
| Install `resend` npm package | [Config] | P0 | 5min | DONE |
| Add `RESEND_API_KEY` to `.env.example` | [Config] | P1 | 5min | DONE |

### Phase 5: Navigation Wiring + Verification — DONE
| Task | Domain | Priority | Estimate | Status |
|------|--------|----------|----------|--------|
| Verify all Header nav links resolve (no 404s) | [Test] | P0 | 10min | DONE |
| Verify all Footer links resolve | [Test] | P0 | 10min | DONE |
| Run `npm run build` — confirm all pages prerender successfully | [Test] | P0 | 10min | DONE |
| Run `npx astro check` — confirm no type errors | [Test] | P0 | 10min | DONE |
| Visual review of each service page | [Test] | P1 | 20min | DONE |

## Test Plan

### Automated — PASSED
```bash
# TypeScript type checking — 0 errors, 0 warnings
npx astro check

# Production build — all 14 pages prerendered
npm run build

# All service page slugs verified in dist/client/
# All core page slugs verified in dist/client/
```

### Manual — PASSED
- [x] Each of the 9 service pages loads with correct content, hero, capabilities list
- [x] Service page JSON-LD contains `@type: Service` with correct service name
- [x] About Us page shows company info and certifications
- [x] Equipment page shows categorized equipment table
- [x] Gallery page displays image grid
- [x] Contact form validates required fields (name, email, message)
- [x] Contact form shows success/error state after submission
- [x] All Header nav links navigate to real pages
- [x] All Footer service links navigate to correct service pages
- [x] Services dropdown in Header lists all 9 services with working links

## Review Gate — PASSED

- [x] All acceptance criteria met
- [x] All automated tests pass (`astro check` + `npm run build`)
- [x] Manual test checklist complete
- [x] All 9 service pages visually reviewed
- [x] Contact form tested (with/without Resend API key)
- [x] No 404 links in navigation

## Documentation DoD

- [x] Update `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` with services.json schema, equipment.json schema, and POST /api/contact contract
- [x] Update `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` with Sprint 002 architectural additions
- [x] Update `PROJECT_STATUS.md` to reflect Sprint 002 completion

## Audit Plan

Mini audit after sprint completion — verify:
- [x] services.json schema matches PLAN-001 specification
- [x] equipment.json schema matches PLAN-001 specification
- [x] POST /api/contact contract matches PLAN-001 specification
- [x] All service page slugs match WordPress URL structure (for future 301 redirects)

## Learnings

- **Dynamic route `[slug].astro` with `getStaticPaths()`**: Simple and effective for data-driven pages. One template + one JSON file = 9 pages. Preferred over individual page files.
- **Security hardening in API routes**: Contact form endpoints need CRLF injection prevention on all fields used in email headers/subjects, strict email regex, CSRF origin checking, Content-Type validation, and field length limits. Caught during /check-sprint.
- **JSON-LD position counters**: Avoid index math like `catIdx * 10 + itemIdx + 1` — use a flat sequential counter with IIFE `++pos` pattern to avoid collisions with variable-length categories.
- **Parallel sub-agent execution**: Delegating independent page builds to parallel agents (services, about, equipment, gallery, contact) was highly effective — all 14 pages built in one pass.
- **Missing service images**: 5 of 9 services don't have corresponding images in public/images/services/. Deferred — pages render fine with placeholder, but real images needed before launch.

## Decisions

- **Inline form/gallery over separate components**: ContactForm and GalleryGrid components were planned but skipped — the inline implementations in their pages were sufficient. Avoids unnecessary abstraction for one-use components.
- **`[slug].astro` over `[...slug].astro`**: Single-segment catch used for service pages to avoid matching nested paths accidentally.
- **HTML email template**: Built inline in contact.ts with `escape()` helper rather than using a templating library — keeps dependencies minimal.
- **Equipment JSON-LD as ItemList**: Used `@type: ItemList` with `ListItem` entries rather than individual `Product` schemas — more appropriate for an equipment catalog page.

## Deferred Items

- Source missing service images (laser-profiling, folding-pressing, sheet-metal-welding, blank-development, cad)
- Rate limiting on POST /api/contact (consider for Sprint 003 or later)
- DRY refactor: Header and Footer both define service/nav link arrays — could centralize
- Lightbox for gallery page (future enhancement)

## Notes

- Sprint completed in a single session (2026-03-16)
- /check-sprint found and fixed: CRLF injection vulnerability (P0), permissive email regex (P0), missing CSRF protection (P1), JSON-LD position counter bug (P1), missing single-quote escaping (P1), missing field length limits (P2)
- Skills decision: no new skill needed — patterns are standard Astro development
