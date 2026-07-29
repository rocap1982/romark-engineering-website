/**
 * Prefix a root-absolute path with the configured Astro `base`.
 *
 * When the site is served from a domain root (the production case) `BASE_URL`
 * is `/` and this is a no-op. When it is served from a sub-path — e.g. a
 * GitHub Pages project site at /romark-engineering-website/ — every internal
 * link and asset URL needs the prefix or it 404s.
 *
 * Only root-absolute paths are rewritten; external URLs, `tel:`/`mailto:`
 * links and in-page anchors are returned untouched.
 */
export function withBase(path: string): string {
  if (!path.startsWith('/') || path.startsWith('//')) return path;
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  return `${base}${path}`;
}

/**
 * Strip the configured `base` off a pathname so it can be compared against
 * the root-absolute paths used in nav definitions.
 */
export function stripBase(pathname: string): string {
  const base = import.meta.env.BASE_URL.replace(/\/$/, '');
  if (base && pathname.startsWith(base)) {
    return pathname.slice(base.length) || '/';
  }
  return pathname;
}
