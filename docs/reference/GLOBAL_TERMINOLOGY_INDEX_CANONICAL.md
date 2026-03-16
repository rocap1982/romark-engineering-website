---
doc_type: canonical_global_terminology_index
status: canonical
created: 2026-03-16
last_updated: 2026-03-16
---

# Global Terminology Index (Canonical)

This document defines the authoritative set of terms and definitions used across the repository.

## Terms

- **areaServed**: A schema.org property on `Service` JSON-LD that specifies the geographic area where the service is available. Used on SEO landing pages to target specific locations (Essex, London, Kent, Basildon).
- **FAQPage**: A schema.org structured data type (`@type: FAQPage`) embedded as JSON-LD on SEO landing pages. Contains `mainEntity` array of `Question`/`Answer` pairs for Google rich snippet eligibility.
- **JSON-LD**: JavaScript Object Notation for Linked Data. Structured data format embedded in HTML `<script type="application/ld+json">` tags for search engine consumption. Used for `LocalBusiness`, `Service`, `FAQPage`, and `ItemList` schemas.
- **SEO landing page**: A location- or industry-targeted page designed to capture long-tail organic search traffic for "{service} {location}" keyword combinations. Defined in `src/data/seo-pages.json` (20 entries) and rendered via `[slug].astro` with the `SeoLandingPage.astro` component.
- **Service schema**: A schema.org structured data type (`@type: Service`) embedded as JSON-LD on service pages and SEO landing pages. Includes `provider` (linked to `LocalBusiness`), `areaServed`, and `serviceType` properties.

