# SEO (Always Apply)

Rob, 22/11/2026: improving Google ranking is one of the site's main objectives. Bake it into every change, do not bolt it on afterwards.

## Every change

- **URLs**: never change or delete a live page's slug without a server-side 301 to its closest replacement. Old engineeringessex.co.uk slugs are listed in `docs/redirects/engineeringessex-301-map.csv` — keep them.
- **Titles and meta descriptions**: each page names its main search term (service + Essex) once; meta descriptions stay under about 155 characters.
- **Internal links**: link related pages to each other (service ↔ sub-service ↔ location pages).
- **Structured data**: keep the LocalBusiness, Service and FAQPage JSON-LD accurate when content changes.

## Photos

- **Filename**: lowercase, hyphens, describes the photo in search terms: `<process>-<material>-<part>.jpg`, e.g. `cnc-milled-stainless-steel-slotted-blocks.jpg`. No camera names (`IMG_4961`), no stuffing (no "essex" in every filename).
- **Alt text**: one plain sentence saying what the photo shows: process, material, part, and the machine where known and true. Location at most once per page.
- **Size**: 1600 px long edge, JPEG quality 80, EXIF (incl. GPS) stripped.
- **Evidence only**: material, machine and process come from Rob or a document, never guessed. If not known, leave it out of the filename and alt text.

Follow Google's own guidance (Search Central: image SEO, helpful content). Write for people first.
