---
doc_type: plan
number: 001
status: approved
created: 2026-03-15
author: "Claude (AI)"
approver: ""
related_issues: ["IDEA-001"]
---

# PLAN-001: Romark Engineering Website Rebuild (WordPress → Astro)

## Problem Statement

### Current State

Romark Engineering's website (engineeringessex.co.uk) runs on WordPress with the Salient theme. It has 35 pages: 9 core service pages, 6 informational pages, and ~20 SEO landing pages. The site was last updated May–Dec 2023.

**Current tech**: WordPress, Salient theme, WP Rocket, Swiper.js, Open Sans font, hosted on unknown WordPress hosting provider.

**Current SEO** (Dec 2024 Safetech report): 12,212 impressions, 74 clicks, 215 sessions. Rankings include #2 for "Stainless Steel Essex", "Laser Cutting Basildon", "Prototype Engineering London", "Precision Engineering Basildon".

**Problems**:
- WordPress + Salient theme is heavy (multiple JS/CSS libraries loaded on every page)
- No direct control over markup or page speed optimization
- Ongoing maintenance burden (WordPress core, theme, and plugin updates)
- Security surface area (WordPress is a common attack target)
- Content last updated 2+ years ago

### Desired State

A modern, fast, informational website built with Astro (hybrid mode) + Tailwind CSS v4, deployed on Railway. The site preserves all existing URL slugs and SEO authority while delivering:
- Sub-second page loads via static HTML generation
- Built-in SEO infrastructure (JSON-LD, OG tags, sitemap, canonical URLs)
- Data-driven content model (JSON files for services, equipment, SEO pages)
- Contact form via server API route + Resend email delivery
- Domain migration from engineeringessex.co.uk to romarkengineering.com with 301 redirects

### Why This Matters

- **Performance**: Faster pages → better Core Web Vitals → better Google rankings → more enquiries
- **Maintainability**: No WordPress/plugin update burden; content in simple JSON files
- **Cost**: Railway hosting is cheaper than managed WordPress hosting
- **Security**: Static HTML has near-zero attack surface
- **Brand**: Domain moves to romarkengineering.com (branded, professional)

## Proposed Solution

### Canonical Changes Required

| Document | Change Type | Description |
|----------|-------------|-------------|
| `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` | Major (new) | Write from scratch for Romark Engineering — architecture, tech stack, domain model |
| `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` | Major (new) | Define schemas for services.json, equipment.json, seo-pages.json + API contract for contact endpoint |
| `CLAUDE.md` | Major (update) | Already updated from ROAM Systems to Romark Engineering; will need final updates once hosting/email confirmed |
| `PROJECT_STATUS.md` | Patch (update) | Track progress through sprints |

### Proposed Specification

#### Data Schema: `src/data/services.json`

```json
[
  {
    "slug": "laser-profiling",
    "name": "Laser Profiling",
    "shortDescription": "Precision laser cutting for steel up to 20mm and stainless up to 16mm",
    "description": "Full HTML-safe description paragraph(s)",
    "capabilities": [
      "Cuts steel up to 20mm thickness",
      "Cuts stainless steel up to 16mm",
      "+/- 0.1mm tolerances"
    ],
    "materials": ["carbon steel", "stainless steel", "aluminium", "copper", "brass"],
    "equipment": ["Amada LC Alpha IV 4Kw CO2 Laser"],
    "industries": ["automotive", "power generation", "architectural"],
    "image": "/images/services/laser-profiling.jpg",
    "metaTitle": "Laser Profiling Services | Romark Engineering Essex",
    "metaDescription": "Precision laser cutting services in Essex...",
    "order": 1
  }
]
```

9 services: Laser Profiling, Folding & Pressing, Fabrication & Welding, CNC Machining, Milling, Turning, Sheet Metal Welding, Blank Development, CAD Design.

#### Data Schema: `src/data/equipment.json`

```json
[
  {
    "category": "Laser & Cutting",
    "items": [
      {
        "name": "Amada LC Alpha IV",
        "type": "4Kw CO2 Laser",
        "specs": "Cuts steel up to 20mm, stainless up to 16mm",
        "relatedServices": ["laser-profiling"]
      }
    ]
  }
]
```

Categories: CAD & CNC Systems, Laser & Cutting, Pressing & Folding, Welding & Finishing.

#### Data Schema: `src/data/seo-pages.json`

```json
[
  {
    "slug": "precision-engineering-essex",
    "title": "Precision Engineering Essex",
    "metaTitle": "Precision Engineering Essex | Romark Engineering",
    "metaDescription": "Expert precision engineering services in Essex...",
    "h1": "Precision Engineering in Essex",
    "content": "Full page content (800-1500 words) with HTML-safe markup",
    "targetKeywords": ["precision engineering essex", "cnc machining essex"],
    "relatedServices": ["cnc-machining", "milling", "turning"],
    "location": "Essex",
    "faqs": [
      {
        "question": "What precision engineering services do you offer in Essex?",
        "answer": "We offer CNC machining, milling, turning..."
      }
    ]
  }
]
```

~20 SEO landing pages covering Essex, London, Basildon, Kent locations.

#### API Contract: `POST /api/contact`

**Request**:
```json
{
  "name": "string (required)",
  "email": "string (required, valid email)",
  "phone": "string (optional)",
  "company": "string (optional)",
  "service": "string (optional, service slug)",
  "message": "string (required, max 5000 chars)"
}
```

**Response (success)**: `200 { "success": true }`
**Response (validation error)**: `400 { "error": "string" }`
**Response (server error)**: `500 { "error": "Failed to send message" }`

**Behavior**: Validates input → sends email via Resend API → delivers to jobs@romarkengineering.com with customer email as reply-to.

**Server route** (not prerendered): `export const prerender = false`

#### SEO Component Contract

Every page includes via `<SEO />` component:
- `<title>` — page-specific
- `<meta name="description">` — page-specific
- `<link rel="canonical">` — `https://romarkengineering.com/{slug}/`
- Open Graph tags: `og:title`, `og:description`, `og:image`, `og:url`, `og:type`
- Twitter Card tags: `twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`
- JSON-LD structured data:
  - Every page: `LocalBusiness` (company info, address, phone, geo)
  - Service pages: `Service` schema linked to the `LocalBusiness`
  - SEO pages: `Service` schema with `areaServed`
  - Equipment page: `ItemList` of equipment

#### Astro Configuration

```javascript
// astro.config.mjs
import { defineConfig } from 'astro/config';
import node from '@astrojs/node';
import sitemap from '@astrojs/sitemap';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  site: 'https://romarkengineering.com',
  output: 'hybrid',
  adapter: node({ mode: 'standalone' }),
  integrations: [sitemap()],
  vite: {
    plugins: [tailwindcss()]
  }
});
```

## Implementation Impact

### Code Changes Required

None — this is a greenfield build in the current working directory. No existing source code to modify.

### New Files

| File | Purpose |
|------|---------|
| `package.json` | Project dependencies and scripts |
| `astro.config.mjs` | Astro framework configuration |
| `tsconfig.json` | TypeScript configuration |
| `src/styles/global.css` | Tailwind v4 theme tokens (brand colors, fonts) |
| `src/layouts/Layout.astro` | Master layout (head, nav, footer, GA4, SEO) |
| `src/components/SEO.astro` | Reusable SEO/meta/JSON-LD component |
| `src/components/Header.astro` | Site header with navigation |
| `src/components/Footer.astro` | Site footer with contact info, certs, links |
| `src/components/Hero.astro` | Page hero/banner component |
| `src/components/ServiceCard.astro` | Service preview card for listings |
| `src/components/EquipmentTable.astro` | Equipment category table |
| `src/components/GalleryGrid.astro` | Image gallery grid with lightbox |
| `src/components/ContactForm.astro` | Contact form with client-side validation |
| `src/components/FAQ.astro` | FAQ accordion for SEO pages |
| `src/components/CertBadges.astro` | ISO 9001 / BS EN 1090 trust badges |
| `src/data/services.json` | 9 service definitions |
| `src/data/equipment.json` | Equipment catalog by category |
| `src/data/seo-pages.json` | ~20 SEO landing page content |
| `src/pages/index.astro` | Homepage |
| `src/pages/about-us.astro` | About Us |
| `src/pages/contact-us.astro` | Contact page with form |
| `src/pages/equipment.astro` | Equipment showcase |
| `src/pages/gallery.astro` | Project gallery |
| `src/pages/laser-profiling.astro` | Service page |
| `src/pages/folding-pressing.astro` | Service page |
| `src/pages/fabrication-and-welding.astro` | Service page |
| `src/pages/cnc-machining.astro` | Service page |
| `src/pages/milling.astro` | Service page |
| `src/pages/turning.astro` | Service page |
| `src/pages/sheet-metal-welding.astro` | Service page |
| `src/pages/blank-development.astro` | Service page |
| `src/pages/cad.astro` | Service page |
| `src/pages/[slug].astro` | Dynamic route for ~20 SEO landing pages |
| `src/pages/api/contact.ts` | Contact form API endpoint |
| `src/lib/email.ts` | Resend email helper |
| `public/robots.txt` | Search engine crawl directives |
| `public/images/` | Gallery and service images (migrated from WP) |
| `.env.example` | Required environment variables template |

### Test Changes

No existing tests. New tests to create:
- Contact form API: validation, success, error cases
- SEO component: correct meta tags generated per page type
- Data files: validate JSON schemas match contract
- Build: successful `npm run build` with no errors

### Data / Migration Impact

**Content migration from WordPress**:
1. Download gallery images from engineeringessex.co.uk
2. Extract service page text content (already captured during IDEA-001 research)
3. Extract SEO landing page content from all ~20 pages
4. Organize into JSON data files matching the schemas above

**Domain migration**:
1. Deploy new site on Railway under romarkengineering.com
2. Configure engineeringessex.co.uk to 301-redirect path-for-path to romarkengineering.com
3. Submit updated sitemap to Google Search Console
4. Monitor rankings for 4-6 weeks post-migration

## Migration Plan

This is a greenfield rebuild, not a modification of the existing WordPress site. The WordPress site continues running until the new site is ready.

**Cutover steps** (Phase 5):
1. Deploy new Astro site to Railway on a staging subdomain
2. Verify all pages render correctly, contact form works, SEO markup is correct
3. Point romarkengineering.com DNS to Railway
4. Configure engineeringessex.co.uk to 301 redirect all paths to romarkengineering.com
5. Submit new sitemap.xml to Google Search Console for romarkengineering.com
6. Verify 301 redirects work path-for-path
7. Monitor Google Search Console for crawl errors and ranking changes

**Rollback**: If issues arise, revert DNS for romarkengineering.com and remove 301 redirects from engineeringessex.co.uk. WordPress site remains untouched as fallback.

## Alternatives Considered

### Alternative 1: Keep WordPress, just optimize
- **Description**: Stay on WordPress but optimize with better caching, image compression, and SEO plugins (Yoast/RankMath)
- **Pros**: No rebuild effort, familiar platform, quick wins possible
- **Cons**: Still WordPress maintenance burden, limited page speed gains, Salient theme overhead remains, security patches ongoing
- **Why not chosen**: Doesn't solve the core maintainability and performance problems. WordPress with Salient will always be heavier than static HTML.

### Alternative 2: Headless CMS + Astro
- **Description**: Use a headless CMS (Sanity, Contentful, Strapi) as the content backend with Astro as the frontend
- **Pros**: Non-technical users can edit content via CMS UI, content/code separation
- **Cons**: Additional service dependency, monthly cost for CMS, more complexity, overkill for ~35 mostly-static pages
- **Why not chosen**: Content changes are infrequent. JSON data files are simpler and free. A CMS adds complexity without proportional benefit for this site size.

### Alternative 3: Next.js instead of Astro
- **Description**: Use Next.js (React-based) instead of Astro
- **Pros**: Larger ecosystem, more tutorials/docs available
- **Cons**: Heavier runtime (ships React JS to client), more complex for a content site, slower page loads for static content
- **Why not chosen**: Astro is purpose-built for content sites — zero JS by default, islands architecture only where needed. It's also what the team already uses for ROAM Systems, so there's existing expertise.

## Traceability

- **Idea doc**: `docs/ideas/IDEA-001-2026-03-15-website-rebuild-astro.md`
- **Canonical docs**:
  - `docs/reference/PLATFORM_OVERVIEW_CANONICAL.md` — to be written (Sprint 1)
  - `docs/reference/SCHEMA_AND_CONTRACTS_CANONICAL.md` — to be written (Sprint 1)
- **Implementation files**: All files listed in "New Files" section above
- **Test files**: To be created per sprint
- **Related audits**: None yet (first build)

## Risks

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| SEO ranking drop during domain migration | Medium | High | 301 redirects path-for-path, preserve URL slugs, submit new sitemap to GSC, monitor for 6 weeks |
| Gallery images low quality (downloaded from WP) | High | Low | Flag stock images for later replacement with real photos; optimize what we have |
| Resend API delivery issues | Low | Medium | Test thoroughly before cutover; Resend has good deliverability; can swap to alternative (SendGrid, Postmark) if needed |
| Content accuracy (specs/capabilities may have changed) | Medium | Medium | Owner review of all service content before go-live; flag any uncertain specs |
| engineeringessex.co.uk redirect configuration | Low | High | Test redirects before removing WordPress; keep WordPress running as fallback until redirects confirmed working |
| Railway hosting outage | Low | Medium | Railway has good uptime SLA; site is mostly static so CDN caching helps; Cloudflare can be added as edge cache layer |

## Approval

- **Approver**: robertdicapite
- **Date**: 2026-03-15
- **Conditions**: None

## Implementation Record

- **Implemented by**:
- **Date**:
- **Sprint**:
- **Deviations from plan**:
