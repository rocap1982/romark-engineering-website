---
doc_type: canonical_platform_overview
status: canonical
created: 2026-03-16
last_updated: 2026-03-16
sprint_updated: "003"
---

# Platform Overview (Canonical)

## Purpose

Marketing website for Romark Engineering, a precision engineering and sheet metal fabrication company based in Stanford-Le-Hope, Essex. Replaces the legacy WordPress/Salient site with a fast, static Astro build optimised for SEO and lead generation.

## Users and roles

- **Visitors**: prospective customers searching for precision engineering, sheet metal fabrication, and related services in Essex and the wider UK.
- **Site operators**: Romark Engineering staff who manage content updates and monitor enquiries via the contact form.

## System boundaries

- **In scope**: all public-facing pages (services, about, gallery, contact, SEO landing pages), contact form submission, sitemap generation, structured data, analytics.
- **Out of scope**: CRM, quoting/invoicing, email infrastructure (Resend API is an external dependency), DNS management, hosting platform internals.

## Architecture (high level)

- **Framework**: Astro 6.0.4, static output mode with `@astrojs/node` adapter for server routes (contact form API).
- **Styling**: Tailwind CSS v4.2.1 via `@tailwindcss/vite` plugin.
- **Language**: TypeScript (strict).
- **Integrations**: `@astrojs/sitemap` for automatic sitemap generation.
- **Fonts**: Michroma (brand/logo), Barlow Condensed (headings), Barlow (body) -- loaded via Google Fonts.
- **Analytics**: Google Analytics 4, conditionally loaded when the `GA4_ID` environment variable is set.
- **Email**: Resend API for contact form delivery (integrated via `POST /api/contact`).
- **Hosting**: Railway (planned, consistent with ROAM Systems infrastructure).
- **Domain**: `romarkengineering.com` (primary); `engineeringessex.co.uk` (301 redirect to primary).

## Key directories

- `src/pages/` -- Astro page routes: `index.astro` (home), `[slug].astro` (data-driven service pages AND SEO landing pages via `getStaticPaths()`), core pages (`about-us`, `equipment`, `gallery`, `contact-us`), API endpoints.
- `src/layouts/` -- Master layout (`Layout.astro`).
- `src/components/` -- Shared UI components (`SEO.astro`, `Header.astro`, `Footer.astro`, `Hero.astro`, `CertBadges.astro`, `ServicePage.astro`, `SeoLandingPage.astro`, `FAQ.astro`).
- `src/styles/` -- Global stylesheet with Tailwind v4 theme tokens.
- `src/data/` -- `services.json` (9 services), `equipment.json` (5 equipment categories), `seo-pages.json` (20 SEO landing pages).
- `src/pages/api/` -- Server routes (contact form).
- `public/images/` -- Static images (gallery, logo, hero).

## Brand identity

- **Primary blue** (`romark-blue`): `#1e3a5f`
- **Accent orange** (`romark-orange`): `#e8611a`
- **Steel grey** (`steel`): `#71797e`
- **Typography**: Michroma for the logo/brand mark; Barlow Condensed for headings; Barlow for body text.

## Core domain concepts

- **Service**: a distinct capability Romark offers (laser profiling, folding/pressing, fabrication/welding, CNC machining, milling, turning, sheet metal work, blank development, CAD design). Defined in `src/data/services.json` (9 entries). Each service is rendered via `[slug].astro` using `getStaticPaths()` and the `ServicePage.astro` component (hero, description, capabilities, equipment, materials, CTA sections).
- **Equipment**: a machine or tool used to deliver services. Defined in `src/data/equipment.json` (5 categories). Displayed on the Equipment page with JSON-LD `ItemList` structured data.
- **SEO landing page**: a location- or industry-targeted page designed to capture long-tail search traffic. Defined in `src/data/seo-pages.json` (20 entries). Each page is rendered via `[slug].astro` using the `SeoLandingPage.astro` component (hero with location, HTML content, related services grid, FAQ accordion, CTA). Includes `Service` JSON-LD with `areaServed` and `FAQPage` JSON-LD for rich snippet eligibility.
- **Enquiry**: a contact form submission from a prospective customer. Submitted via the Contact Us page (client-side validation) to `POST /api/contact` (server endpoint), which delivers the email via the Resend API.

## SEO strategy

- JSON-LD structured data (`LocalBusiness` schema) on every page; `Service` schema on service pages (linked to `LocalBusiness`); `ItemList` schema on the Equipment page; `FAQPage` schema on SEO landing pages (for rich snippet eligibility); `Service` schema with `areaServed` on SEO landing pages (location-targeted).
- Open Graph tags and Twitter Cards for social sharing.
- Canonical URLs on all pages.
- `robots.txt` in `public/`.
- Auto-generated `sitemap.xml` via `@astrojs/sitemap`.

## Certifications

- ISO 9001 (Quality Management)
- BS EN 1090 (Execution of Steel Structures)

Displayed site-wide via the `CertBadges.astro` component.

## Invariants (non-negotiable behaviour)

- Every public page includes structured data (JSON-LD), OG tags, canonical URL, and a meta description.
- The contact form validates client-side before submitting to the `POST /api/contact` server endpoint; no client-side JavaScript sends email directly.
- Brand colours and typography remain consistent across all pages.
- The site builds to fully static HTML except for the contact form API route.
- Certification badges appear on every page via the shared layout.

## Glossary

- **Astro**: static-site generator with optional server-side rendering; the core framework for this project.
- **Tailwind CSS v4**: utility-first CSS framework; configured via the Vite plugin rather than PostCSS.
- **Resend**: transactional email API used to deliver contact form submissions.
- **Railway**: cloud hosting platform for deployment.
- **JSON-LD**: linked-data format embedded in HTML `<script>` tags for search-engine structured data.
- **GA4**: Google Analytics 4, the current generation of Google's analytics platform.
