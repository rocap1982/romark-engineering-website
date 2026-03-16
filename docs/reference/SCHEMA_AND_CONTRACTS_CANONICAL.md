---
doc_type: canonical_schema_contracts
status: canonical
created: 2026-03-16
last_updated: 2026-03-16
sprint_updated: "003"
---

# Schema & Contracts (Canonical)

This document is the canonical source for:

- data file schemas (services, equipment, SEO landing pages)
- API endpoint contracts (request/response + errors)
- validation rules and security constraints

## Data Schemas

### Entity: Service (`src/data/services.json`)

Array of service objects. Each service has:

| Field             | Type       | Required | Constraints                        |
|-------------------|------------|----------|------------------------------------|
| slug              | string     | yes      | URL-safe identifier, unique        |
| name              | string     | yes      | Display name                       |
| shortDescription  | string     | yes      | One-line summary                   |
| description       | string     | yes      | Full description paragraph         |
| capabilities      | string[]   | yes      | List of capability statements      |
| materials         | string[]   | yes      | May be empty (e.g. CAD)           |
| equipment         | string[]   | yes      | Equipment names or software tools  |
| industries        | string[]   | yes      | Target industry identifiers        |
| image             | string     | yes      | Path under `/images/services/`     |
| metaTitle         | string     | yes      | SEO page title                     |
| metaDescription   | string     | yes      | SEO meta description               |
| order             | number     | yes      | Display order (1-based, unique)    |

**Primary key**: `slug`

**Current count**: 9 services.

### Entity: Equipment (`src/data/equipment.json`)

Array of category objects. Each category contains equipment items.

**Category object:**

| Field    | Type     | Required | Constraints               |
|----------|----------|----------|---------------------------|
| category | string   | yes      | Category display name     |
| items    | Item[]   | yes      | Equipment in this category|

**Item object:**

| Field           | Type       | Required | Constraints                              |
|-----------------|------------|----------|------------------------------------------|
| name            | string     | yes      | Equipment or software name               |
| type            | string     | yes      | Equipment type descriptor                |
| specs           | string     | yes      | Key specifications summary               |
| relatedServices | string[]   | yes      | Service slugs this equipment belongs to  |

**Relationship**: `relatedServices[]` references `Service.slug`.

**Current categories**: 5 (Laser & Cutting, Pressing & Folding, CNC & Machining, Welding & Finishing, CAD & Design).

### Entity: SEO Landing Page (`src/data/seo-pages.json`)

Array of SEO landing page objects. Each page targets a specific keyword + location combination.

| Field            | Type       | Required | Constraints                                                        |
|------------------|------------|----------|--------------------------------------------------------------------|
| slug             | string     | yes      | URL-safe, unique, no conflicts with services.json slugs            |
| title            | string     | yes      | Page title                                                         |
| metaTitle        | string     | yes      | SEO meta title                                                     |
| metaDescription  | string     | yes      | SEO meta description, max 160 chars                                |
| h1               | string     | yes      | Page heading                                                       |
| content          | string     | yes      | HTML content (rendered via `set:html`)                             |
| targetKeywords   | string[]   | yes      | Target SEO keywords                                                |
| relatedServices  | string[]   | yes      | Service slugs from services.json                                   |
| location         | string     | yes      | Target location (may be empty string for general/non-location pages) |
| faqs             | FAQ[]      | yes      | Array of FAQ objects                                               |

**FAQ object:**

| Field    | Type   | Required |
|----------|--------|----------|
| question | string | yes      |
| answer   | string | yes      |

**Primary key**: `slug`

**Current count**: 20 pages.

**Relationship**: `relatedServices[]` references `Service.slug`; `slug` must not conflict with `Service.slug`.

**JSON-LD schemas**: Each SEO landing page generates two structured data schemas:
- **Service** schema with `areaServed` — uses `Place` type for location-specific pages, `Country` type for general (non-location) pages.
- **FAQPage** schema for pages that have FAQs (all current pages include FAQs).

## API Contracts

### POST `/api/contact`

Server-rendered Astro API route (`prerender = false`). Sends a contact form enquiry via the Resend API.

#### Request

- **Content-Type**: `application/json` (enforced; returns 400 if missing)
- **Origin header**: must match site origin (CSRF protection; returns 403 if mismatched)

**Body:**

| Field   | Type   | Required | Max Length | Constraints                           |
|---------|--------|----------|------------|---------------------------------------|
| name    | string | yes      | 100        | No CRLF/null bytes                    |
| email   | string | yes      | —          | Must match email regex; no CRLF/null  |
| phone   | string | no       | 30         | No CRLF/null bytes                    |
| company | string | no       | 100        | —                                     |
| service | string | no       | 100        | No CRLF/null bytes                    |
| message | string | yes      | 5000       | —                                     |

All string values are trimmed before processing.

#### Security

- **CSRF**: origin header checked against `url.origin`; mismatched origin returns 403.
- **Content-Type validation**: rejects requests without `application/json`.
- **CRLF injection protection**: name, email, phone, and service fields are rejected if they contain `\r`, `\n`, or `\0`.
- **HTML entity escaping**: all user input is escaped (`&`, `<`, `>`, `"`, `'`) before inclusion in the email HTML body.

#### Responses

All responses include `Content-Type: application/json`.

| Status | Body                                | Condition                                     |
|--------|-------------------------------------|-----------------------------------------------|
| 200    | `{ "success": true }`               | Email sent successfully                       |
| 400    | `{ "error": "<validation message>" }` | Invalid JSON, missing Content-Type, or validation failure |
| 403    | `{ "error": "Unauthorized" }`       | Origin header mismatch (CSRF)                 |
| 500    | `{ "error": "Failed to send message" }` | Missing API key or Resend API error       |

#### Email delivery

- **Provider**: Resend API (`RESEND_API_KEY` environment variable)
- **From**: `Romark Engineering <noreply@romarkengineering.com>`
- **To**: `jobs@romarkengineering.com`
- **Reply-To**: submitter's email address
- **Subject**: `Website Enquiry: {service} — {name}` (if service provided) or `Website Enquiry from {name}`
- **Body**: HTML table template with escaped field values

## Versioning Policy

- **Minor**: additive/backward compatible (new optional fields, new endpoints)
- **Major**: breaking (required field changes, endpoint removal, response shape changes)
- **Patch**: clarification (documentation updates, constraint tightening)

## Migration Policy

- Data file changes (services.json, equipment.json, seo-pages.json) are deployed with the static build; no runtime migration required.
- API contract changes require a plan document and explicit approval before implementation.
