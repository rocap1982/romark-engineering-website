---
doc_type: idea
number: 001
status: accepted
created: 2026-03-15
last_updated: 2026-03-15
owner: "robertdicapite"
tags: [website, rebuild, astro, seo, engineering]
related_plans: ["PLAN-001"]
related_sprints: []
---

# IDEA-001: Romark Engineering Website Rebuild (WordPress → Astro)

## Summary

Rebuild the Romark Engineering website (engineeringessex.co.uk) from a WordPress/Salient theme site to a modern Astro static site with Tailwind CSS. The rebuild preserves all existing content and SEO rankings while delivering faster performance, better SEO infrastructure, and a cleaner, more maintainable codebase.

## Problem / Opportunity

### Current State

**Romark Engineering** — precision engineering & sheet metal fabrication company in Stanford-Le-Hope, Essex. Phone: 01375 673 447 / 01375 640 037.

Current website: WordPress with Salient theme, 35 pages (last updated May 2023–Dec 2023):

**Core Service Pages (9)**:
1. Laser Profiling — Amada LC Alpha IV 4Kw CO2 Laser, cuts steel up to 20mm, stainless to 16mm, ±0.1mm tolerances
2. Folding & Pressing — CNC press brakes (100–220 ton, 3–4m capacity)
3. Fabrication & Welding — TIG/MIG welding (6 of each), bespoke sheet metal fabrication
4. CNC Machining — XYZ 710 CNC Machining Centre, prototype to production
5. Milling — Bridgeport Mill with DRO
6. Turning — Harrison M300 600mm Lathe with DRO
7. Sheet Metal Welding
8. Blank Development
9. CAD Design — Solidworks, AutoCAD, Rhino3D, One CNC CAM

**Other Pages (6)**:
- Homepage
- About Us
- Equipment (full equipment list)
- Gallery (portfolio of work)
- Contact Us
- Sitemap

**SEO Landing Pages (~20)** — location-targeted:
- Essex: precision-engineering-essex, sheet-metal-fabrication-essex, machining-essex, sheet-metal-essex, laser-cutting-essex, cnc-milling-essex
- London: sheet-metal-fabrication-london, precision-engineering-london, sheet-metal-london, aluminium-welding-london, prototype-engineering-london
- Basildon: precision-engineering-basildon, laser-cutting-basildon
- Kent: precision-engineering-kent, cnc-machining-kent
- General: stainless-steel-essex, metal-fabrication-essex, fabrication-contractors, prototype-engineering-services, sheetmetal-work

**SEO Performance (Safetech Report, Dec 2024)**:
- 12,212 impressions / 74 clicks / 215 sessions / 402 page views
- 75% organic + direct traffic, 70.8% desktop
- Top rankings: #2 for "Stainless Steel Essex", "Laser Cutting Basildon", "Prototype Engineering London", "Precision Engineering Basildon"
- Top traffic pages: homepage (38 clicks), sheet-metal-london (6), aluminium-welding-london (5)

**Industries served**: Automotive, power generation, architectural.

**Outsourced finishes**: Powder coating, wet spray, electroplating, galvanising.

### Desired State

A modern, fast, SEO-optimized static website built with:
- **Astro 5** — static site generation with islands architecture for any interactive components
- **Tailwind CSS v4** — utility-first styling with brand tokens
- **TypeScript** — strict mode for maintainability
- All existing content preserved and improved
- SEO infrastructure baked in from the start (structured data, meta tags, sitemap, etc.)
- Contact form via API route (Resend or similar)
- Deployed on Railway or similar platform

### Why This Matters

- **Performance**: WordPress + Salient theme is heavy; static site will load significantly faster → better Core Web Vitals → better rankings
- **SEO**: Current site ranks well for some terms but has room for improvement with proper structured data, canonical URLs, and optimized meta tags
- **Maintainability**: Static site is easier to maintain than WordPress (no plugin updates, no security patches, no database)
- **Cost**: Lower hosting costs with static/hybrid deployment vs WordPress hosting
- **Control**: Full control over markup, no theme limitations

## Constraints

- Must preserve existing URL structure (301 redirects if any URLs change) to protect current rankings
- Must maintain or improve current SEO performance — no ranking regressions
- Content must be factually accurate to Romark Engineering's current capabilities
- Contact form must work reliably (enquiries are business-critical)
- Gallery images need to be migrated from the WordPress site
- Brand identity should be refreshed but recognizable to existing customers

## Architecture / Approach

### Tech Stack (confirmed)
- **Framework**: Astro 5/6 (hybrid mode with @astrojs/node standalone adapter)
- **Styling**: Tailwind CSS v4 via @tailwindcss/vite
- **Language**: TypeScript (strict)
- **Contact Form**: Server API route → Resend API → jobs@romarkengineering.com
- **Analytics**: Google Analytics (GA4)
- **Hosting**: Railway (auto-deploy via GitHub, same as ROAM Systems)
- **Domain**: romarkengineering.com (primary) + engineeringessex.co.uk (301 redirects)
- **Content**: JSON data files for services, equipment, SEO pages
- **Certifications**: ISO 9001, BS EN 1090

### Site Structure

```
src/
├── pages/
│   ├── index.astro                    # Homepage
│   ├── about-us.astro                 # About Us
│   ├── contact-us.astro               # Contact form
│   ├── equipment.astro                # Equipment showcase
│   ├── gallery.astro                  # Work portfolio
│   ├── services/
│   │   ├── laser-profiling.astro
│   │   ├── folding-pressing.astro
│   │   ├── fabrication-and-welding.astro
│   │   ├── cnc-machining.astro
│   │   ├── milling.astro
│   │   ├── turning.astro
│   │   ├── sheet-metal-welding.astro
│   │   ├── blank-development.astro
│   │   └── cad.astro
│   ├── [seo-slug].astro               # Dynamic route for ~20 SEO landing pages
│   └── api/
│       └── contact.ts                 # Contact form handler
├── layouts/
│   └── Layout.astro                   # Master layout (head, nav, footer)
├── components/
│   ├── Header.astro
│   ├── Footer.astro
│   ├── Hero.astro
│   ├── ServiceCard.astro
│   ├── EquipmentTable.astro
│   ├── GalleryGrid.astro
│   ├── ContactForm.astro
│   └── SEO.astro                      # Reusable SEO component (meta, OG, JSON-LD)
├── data/
│   ├── services.json                  # Service definitions
│   ├── equipment.json                 # Equipment catalog
│   └── seo-pages.json                 # SEO landing page content
└── styles/
    └── global.css                     # Tailwind v4 theme tokens
```

### SEO Infrastructure (built-in from day 1)
- `robots.txt` — static file
- `sitemap.xml` — auto-generated by @astrojs/sitemap
- Canonical URLs on every page
- Open Graph + Twitter Card meta tags via SEO component
- JSON-LD structured data: LocalBusiness, Service, Organization
- Semantic HTML throughout
- Image optimization with descriptive alt text
- URL structure matches current site (no 301s needed for core pages)

### Content Strategy for SEO Landing Pages
- Template-driven: single `[seo-slug].astro` dynamic route
- Content defined in `seo-pages.json` with per-page: title, description, H1, body content, target keywords, related services
- Each page links back to relevant core service pages (internal linking)
- Unique content per page (not just location swaps) to avoid thin content penalties

### Implementation Phases

**Phase 1: Foundation** (Sprint 1)
- Project setup: Astro 5 + Tailwind v4 + TypeScript
- Master layout with SEO component
- Brand tokens (colors, fonts, spacing)
- Header/Footer components
- Homepage

**Phase 2: Core Pages** (Sprint 2)
- All 9 service pages with content from current site
- About Us page
- Equipment page
- Data files (services.json, equipment.json)

**Phase 3: Interactive & Media** (Sprint 3)
- Contact form with API route + email integration
- Gallery page with optimized images
- Image migration from WordPress

**Phase 4: SEO Landing Pages** (Sprint 4)
- Dynamic route for ~20 SEO pages
- seo-pages.json with unique content per page
- Internal linking strategy
- JSON-LD structured data for all pages

**Phase 5: Polish & Deploy** (Sprint 5)
- Performance optimization (image formats, lazy loading, preloading)
- Accessibility audit
- Cross-browser testing
- Railway deployment configuration
- DNS cutover plan

## Non-goals

- E-commerce / online ordering (Romark is B2B, enquiry-based — confirmed informational only)
- Blog / news section (not currently on the site; can be added later)
- Customer portal / login system
- CMS integration (content managed via code/data files)
- Multilingual support

## Decisions (all questions resolved)

1. **Brand refresh**: Full redesign — fresh modern engineering/fabrication look. Trust agent judgement on design. Informational site only (no e-commerce).
2. **Gallery images**: Download from current WordPress site. Many are stock images and will need replacing later with real photos.
3. **Contact form destination**: jobs@romarkengineering.com
4. **Analytics**: Google Analytics (GA4) — Safetech already uses it for monthly reports.
5. **Domain**: Primary domain **romarkengineering.com**, with **engineeringessex.co.uk** 301-redirecting to it (path-for-path to preserve SEO authority).
6. **Hosting**: Railway — same architecture as ROAM Systems (Astro hybrid + @astrojs/node standalone + Railway auto-deploy via GitHub).
7. **SEO landing pages**: Migrate existing content + enhance (longer descriptions 800-1500 words, local signals, FAQ sections, CTAs, internal cross-links, JSON-LD). Preserve exact URL slugs.
8. **Certifications**: ISO 9001 and BS EN 1090 — feature prominently on About Us page and in footer/trust bar.

## Traceability

- `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — needs to be written for Romark Engineering (currently a blank template from ROAM Systems setup)
- `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — needs data file schemas (services.json, equipment.json, seo-pages.json)
- `CLAUDE.md` — needs to be updated from ROAM Systems to Romark Engineering
- `PROJECT_STATUS.md` — needs to reflect the website rebuild project
