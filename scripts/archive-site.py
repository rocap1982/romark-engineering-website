#!/usr/bin/env python3
"""
archive-site.py — read-only archive of a WordPress site before the host strips it.

Written for https://engineeringessex.co.uk (Romark Engineering, Safetech-hosted WordPress).

What it does
  1. Crawls every internal URL reachable from the homepage, robots.txt Sitemap: lines,
     /sitemap.xml, /wp-sitemap.xml (and sitemap indexes). Same host only (www and bare
     host treated as one site). Respects robots.txt. One request per second across the
     whole run (pages AND images). Never touches admin / login / API / feed paths.
  2. Per page saves raw HTML, clean markdown of the main content, and a JSON record:
     <title>, meta description, H1-H3, canonical, every image (src + alt), internal and
     outbound links, word count, HTTP status.
  3. Downloads every referenced image. For WordPress resized files (name-WxH.ext) it also
     tries the un-suffixed original and keeps the largest. Original filenames kept under
     images/ (a yyyy-mm prefix is added only on a filename collision).
  4. index.csv, images.csv, links.csv, redirect-map.csv, crawl-log.jsonl, report.md.

Only GET requests are made. Nothing on the site is modified.

Usage
  python archive-site.py --out <folder> [--base-url https://engineeringessex.co.uk]
                         [--delay 1.0] [--max-pages 500] [--max-images 3000]
                         [--user-agent "..."]

Dependencies: requests, beautifulsoup4, markdownify, lxml
  pip install requests beautifulsoup4 markdownify lxml
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import os
import re
import sys
import time
import urllib.robotparser
from collections import OrderedDict, deque
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse, urlunparse, unquote

import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md

try:
    import lxml  # noqa: F401
    PARSER = "lxml"
except Exception:  # pragma: no cover
    PARSER = "html.parser"

DEFAULT_BASE = "https://engineeringessex.co.uk"
DEFAULT_UA = "RomarkSiteArchive/1.0 (archive of own site; python-requests)"

# Paths we never request, even if linked. Not an exhaustive security list — these are
# the WordPress surfaces that are not content and/or could have side effects.
BLOCKED_PATH_PREFIXES = (
    "/wp-admin", "/wp-login", "/wp-json", "/xmlrpc.php", "/wp-cron.php",
    "/wp-includes", "/cgi-bin", "/wp-signup", "/wp-activate", "/wp-register",
    "/wp-comments-post.php", "/wp-trackback.php", "/?s=", "/search/",
)
BLOCKED_PATH_PARTS = ("/feed", "/embed", "/trackback", "/comments/")
BLOCKED_QUERY_KEYS = ("replytocom", "share", "s", "p", "preview", "attachment_id", "add-to-cart")

IMAGE_EXT = {".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".avif", ".bmp", ".ico", ".tif", ".tiff"}
DOC_EXT = {".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".zip", ".dwg", ".dxf", ".step", ".stp"}
WP_RESIZE_RE = re.compile(r"^(?P<stem>.+?)-(?P<w>\d{2,5})x(?P<h>\d{2,5})(?P<ext>\.[A-Za-z0-9]{2,5})$")
WP_UPLOAD_DATE_RE = re.compile(r"/wp-content/uploads/(\d{4})/(\d{2})/")

# Evidence patterns for the filler-vs-real classification (reported, not auto-decided).
STOCK_NAME_RE = re.compile(
    r"(shutterstock|istock|depositphotos|dreamstime|adobestock|stock-photo|gettyimages|"
    r"pexels|unsplash|pixabay|123rf|bigstock|fotolia|canva|freepik|^\d{6,}[-_.]|^image\d*\.|^img_?\d+\.|^photo\d*\.)",
    re.I,
)
ROMARK_RE = re.compile(r"\bRomark\b", re.I)
LOCAL_RE = re.compile(r"Stanford[- ]le[- ]Hope|Baryta|SS17|Essex", re.I)
PHONE_RE = re.compile(r"01375\s?\d{3}\s?\d{3}")


# --------------------------------------------------------------------------- helpers

def now_iso() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def norm_host(host: str) -> str:
    host = (host or "").lower()
    return host[4:] if host.startswith("www.") else host


def normalise_url(url: str) -> str:
    """Strip fragment, default ports, trailing index.php; keep query (decided elsewhere)."""
    p = urlparse(url)
    scheme = p.scheme.lower() or "https"
    netloc = p.netloc.lower()
    if netloc.endswith(":80") or netloc.endswith(":443"):
        netloc = netloc.rsplit(":", 1)[0]
    path = p.path or "/"
    path = re.sub(r"/index\.php$", "/", path)
    if not path.startswith("/"):
        path = "/" + path
    return urlunparse((scheme, netloc, path, "", p.query, ""))


def is_blocked_path(url: str) -> str | None:
    p = urlparse(url)
    path = p.path.lower()
    for pre in BLOCKED_PATH_PREFIXES:
        if path.startswith(pre.lower()):
            return f"blocked-path:{pre}"
    for part in BLOCKED_PATH_PARTS:
        if part in path:
            return f"blocked-path:{part}"
    if p.query:
        keys = {kv.split("=", 1)[0].lower() for kv in p.query.split("&") if kv}
        bad = keys & set(BLOCKED_QUERY_KEYS)
        if bad:
            return f"blocked-query:{','.join(sorted(bad))}"
        # Any other query-string URL is a view of an existing page (sorting, tracking,
        # pagination variants) — record as skipped rather than crawl duplicates.
        return "skipped-querystring"
    return None


def guess_ext(path: str) -> str:
    return os.path.splitext(urlparse(path).path)[1].lower()


def safe_slug(url: str) -> str:
    p = urlparse(url)
    path = unquote(p.path).strip("/")
    if not path:
        return "index"
    slug = re.sub(r"[^A-Za-z0-9._-]+", "-", path.replace("/", "__")).strip("-")
    return slug[:150] or "index"


def human_size(n: int) -> str:
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.1f} {unit}" if unit != "B" else f"{n} B"
        n /= 1024.0
    return f"{n:.1f} GB"


def shingles(text: str, k: int = 8) -> set[str]:
    words = re.findall(r"[a-z0-9']+", text.lower())
    return {" ".join(words[i:i + k]) for i in range(max(0, len(words) - k + 1))}


# --------------------------------------------------------------------------- data

@dataclass
class PageRecord:
    url: str
    final_url: str = ""
    status: int | str = ""
    content_type: str = ""
    title: str = ""
    meta_description: str = ""
    canonical: str = ""
    h1: list[str] = field(default_factory=list)
    h2: list[str] = field(default_factory=list)
    h3: list[str] = field(default_factory=list)
    images: list[dict] = field(default_factory=list)
    internal_links: list[str] = field(default_factory=list)
    outbound_links: list[str] = field(default_factory=list)
    word_count: int = 0
    html_file: str = ""
    md_file: str = ""
    json_file: str = ""
    discovered_via: str = ""
    error: str = ""
    # evidence for filler-vs-real
    romark_mentions: int = 0
    local_mentions: int = 0
    phone_mentions: int = 0
    stock_named_images: int = 0
    max_similarity: float = 0.0
    most_similar_page: str = ""


class RateLimiter:
    def __init__(self, delay: float):
        self.delay = delay
        self.last = 0.0

    def wait(self):
        gap = time.monotonic() - self.last
        if gap < self.delay:
            time.sleep(self.delay - gap)
        self.last = time.monotonic()


# --------------------------------------------------------------------------- crawler

class Archiver:
    def __init__(self, base_url: str, out: Path, delay: float, max_pages: int, max_images: int, ua: str):
        self.base_url = normalise_url(base_url).rstrip("/")
        self.base = urlparse(self.base_url)
        self.host = norm_host(self.base.netloc)
        self.out = out
        self.pages_dir = out / "pages"
        self.images_dir = out / "images"
        self.files_dir = out / "files"
        self.raw_dir = out / "raw"
        for d in (self.pages_dir, self.images_dir, self.files_dir, self.raw_dir):
            d.mkdir(parents=True, exist_ok=True)
        self.limiter = RateLimiter(delay)
        self.max_pages = max_pages
        self.max_images = max_images
        self.session = requests.Session()
        self.session.headers.update({"User-Agent": ua, "Accept-Language": "en-GB,en;q=0.9"})
        self.ua = ua
        self.log_path = out / "crawl-log.jsonl"
        self.log_fh = open(self.log_path, "a", encoding="utf-8")
        self.robots: urllib.robotparser.RobotFileParser | None = None
        self.robots_text = ""
        self.sitemap_urls: list[str] = []
        self.pages: "OrderedDict[str, PageRecord]" = OrderedDict()
        self.skipped: list[dict] = []
        self.failed: list[dict] = []
        self.image_records: "OrderedDict[str, dict]" = OrderedDict()   # url -> record
        self.image_pages: dict[str, set[str]] = {}                     # url -> set(page urls)
        self.image_alts: dict[str, set[str]] = {}
        self.file_records: "OrderedDict[str, dict]" = OrderedDict()
        self.used_filenames: dict[str, str] = {}                       # local name -> source url
        self.started = now_iso()

    # ---- infrastructure

    def log(self, **kv):
        kv["ts"] = now_iso()
        self.log_fh.write(json.dumps(kv, ensure_ascii=False) + "\n")
        self.log_fh.flush()

    def is_internal(self, url: str) -> bool:
        return norm_host(urlparse(url).netloc) == self.host

    def get(self, url: str, kind: str, stream: bool = False, retries: int = 3) -> requests.Response | None:
        """Rate-limited GET with retries on network errors / 5xx / 429. Returns None on failure."""
        last_err = ""
        for attempt in range(1, retries + 1):
            self.limiter.wait()
            t0 = time.monotonic()
            try:
                r = self.session.get(url, timeout=(10, 60), allow_redirects=True, stream=stream)
                elapsed = round(time.monotonic() - t0, 3)
                self.log(kind=kind, url=url, final_url=r.url, status=r.status_code,
                         content_type=r.headers.get("Content-Type", ""), attempt=attempt, elapsed=elapsed)
                if r.status_code in (429, 500, 502, 503, 504) and attempt < retries:
                    time.sleep(2 ** attempt)
                    continue
                return r
            except requests.RequestException as e:
                last_err = f"{type(e).__name__}: {e}"
                self.log(kind=kind, url=url, status="error", error=last_err, attempt=attempt)
                if attempt < retries:
                    time.sleep(2 ** attempt)
        self.failed.append({"kind": kind, "url": url, "reason": last_err or "exhausted retries"})
        return None

    def allowed_by_robots(self, url: str) -> bool:
        if self.robots is None:
            return True
        try:
            return self.robots.can_fetch(self.ua, url) and self.robots.can_fetch("*", url)
        except Exception:
            return True

    # ---- discovery

    def load_robots(self):
        url = f"{self.base_url}/robots.txt"
        r = self.get(url, "robots")
        rp = urllib.robotparser.RobotFileParser()
        if r is not None and r.status_code == 200 and "html" not in r.headers.get("Content-Type", "").lower():
            self.robots_text = r.text
            (self.raw_dir / "robots.txt").write_text(r.text, encoding="utf-8")
            rp.parse(r.text.splitlines())
            for line in r.text.splitlines():
                if line.lower().startswith("sitemap:"):
                    self.sitemap_urls.append(line.split(":", 1)[1].strip())
            cd = rp.crawl_delay(self.ua) or rp.crawl_delay("*")
            if cd and cd > self.limiter.delay:
                self.limiter.delay = float(cd)
                self.log(kind="info", msg=f"robots.txt Crawl-delay {cd}s honoured")
        else:
            rp.parse([])  # no robots → everything allowed
            self.log(kind="info", msg="no robots.txt (or not plain text) — treating as allow-all")
        self.robots = rp

    def load_sitemaps(self) -> list[tuple[str, str]]:
        """Return [(url, via)] from every sitemap we can find. Saves raw XML."""
        found: list[tuple[str, str]] = []
        queue = deque()
        for u in self.sitemap_urls:
            queue.append(u)
        for cand in ("/sitemap.xml", "/wp-sitemap.xml", "/sitemap_index.xml"):
            queue.append(self.base_url + cand)
        seen = set()
        n = 0
        while queue:
            sm = queue.popleft()
            if sm in seen or not self.is_internal(sm):
                continue
            seen.add(sm)
            r = self.get(sm, "sitemap")
            if r is None or r.status_code != 200:
                continue
            ctype = r.headers.get("Content-Type", "").lower()
            body = r.text
            if "xml" not in ctype and not body.lstrip().startswith("<?xml") and "<urlset" not in body and "<sitemapindex" not in body:
                self.log(kind="info", msg=f"{sm} returned non-XML ({ctype}); ignored")
                continue
            n += 1
            (self.raw_dir / f"sitemap-{n:02d}-{safe_slug(sm)}.xml").write_text(body, encoding="utf-8")
            soup = BeautifulSoup(body, "xml")
            if soup.find("sitemapindex"):
                for loc in soup.find_all("loc"):
                    queue.append(loc.get_text(strip=True))
            else:
                for url_el in soup.find_all("url"):
                    loc = url_el.find("loc")
                    if loc:
                        found.append((loc.get_text(strip=True), f"sitemap:{sm}"))
                for loc in soup.find_all(re.compile(r"^image:loc$")):
                    self.note_image(loc.get_text(strip=True), "", f"sitemap:{sm}")
        return found

    # ---- page handling

    def enqueue_ok(self, url: str, via: str) -> bool:
        if not self.is_internal(url):
            return False
        reason = is_blocked_path(url)
        if reason:
            self.skipped.append({"url": url, "reason": reason, "via": via})
            return False
        ext = guess_ext(url)
        if ext in IMAGE_EXT:
            self.note_image(url, "", via)
            return False
        if ext in DOC_EXT:
            self.note_file(url, via)
            return False
        if not self.allowed_by_robots(url):
            self.skipped.append({"url": url, "reason": "robots-disallow", "via": via})
            return False
        return True

    def note_image(self, src: str, alt: str, page_url: str):
        if not src or src.startswith("data:"):
            return
        url = normalise_url(urljoin(page_url if page_url.startswith("http") else self.base_url, src))
        if not self.is_internal(url):
            # External images are recorded but not downloaded (CDN/gravatar/etc.).
            self.image_records.setdefault(url, {"url": url, "internal": False, "local_file": "", "bytes": 0, "status": "external-not-downloaded"})
        else:
            self.image_records.setdefault(url, {"url": url, "internal": True, "local_file": "", "bytes": 0, "status": ""})
        self.image_pages.setdefault(url, set()).add(page_url)
        if alt:
            self.image_alts.setdefault(url, set()).add(alt.strip())

    def note_file(self, href: str, page_url: str):
        url = normalise_url(urljoin(page_url if page_url.startswith("http") else self.base_url, href))
        if self.is_internal(url):
            self.file_records.setdefault(url, {"url": url, "local_file": "", "bytes": 0, "status": "", "pages": set()})
            self.file_records[url]["pages"].add(page_url)

    def extract_main(self, soup: BeautifulSoup) -> BeautifulSoup:
        for sel in ("#ajax-content-wrap", "main", "[role=main]", "#content", ".container-wrap", "article", "body"):
            node = soup.select_one(sel)
            if node is not None:
                main = BeautifulSoup(str(node), PARSER)
                for junk in main.select("script, style, noscript, iframe, form, nav, header, footer, #header-outer, #footer-outer, .nectar-social, .sharing-default-minimal, #ajax-loading-screen, #slide-out-widget-area, .wpcf7"):
                    junk.decompose()
                return main
        return soup

    def process_page(self, url: str, via: str):
        rec = PageRecord(url=url, discovered_via=via)
        self.pages[url] = rec
        r = self.get(url, "page")
        if r is None:
            rec.status = "error"
            rec.error = self.failed[-1]["reason"] if self.failed else "request failed"
            return
        rec.status = r.status_code
        rec.final_url = normalise_url(r.url)
        rec.content_type = r.headers.get("Content-Type", "")
        if not self.is_internal(rec.final_url):
            rec.error = f"redirected off-site to {rec.final_url}"
            self.skipped.append({"url": url, "reason": "redirect-offsite", "via": rec.final_url})
            return
        if "html" not in rec.content_type.lower():
            ext = guess_ext(rec.final_url)
            if ext in IMAGE_EXT:
                self.note_image(rec.final_url, "", via)
            elif ext in DOC_EXT:
                self.note_file(rec.final_url, via)
            rec.error = f"not html ({rec.content_type})"
            return
        html = r.text
        slug = safe_slug(rec.final_url if r.status_code == 200 else url)
        if r.status_code != 200:
            slug = f"{slug}__status-{r.status_code}"
        rec.html_file = f"pages/{slug}.html"
        (self.out / rec.html_file).write_text(html, encoding="utf-8")
        if r.status_code != 200:
            rec.error = f"http {r.status_code}"
            self.failed.append({"kind": "page", "url": url, "reason": f"http {r.status_code}"})
            return

        soup = BeautifulSoup(html, PARSER)
        rec.title = (soup.title.get_text(strip=True) if soup.title else "")
        md_tag = soup.find("meta", attrs={"name": re.compile("^description$", re.I)})
        rec.meta_description = (md_tag.get("content") or "").strip() if md_tag else ""
        can = soup.find("link", attrs={"rel": lambda v: v and "canonical" in ([v] if isinstance(v, str) else v)})
        rec.canonical = (can.get("href") or "").strip() if can else ""
        rec.h1 = [h.get_text(" ", strip=True) for h in soup.find_all("h1")]
        rec.h2 = [h.get_text(" ", strip=True) for h in soup.find_all("h2")]
        rec.h3 = [h.get_text(" ", strip=True) for h in soup.find_all("h3")]

        # Images: <img src/srcset/data-src/data-lazy-src>, <source srcset>, inline background-image, og:image, icons
        seen_imgs: "OrderedDict[str, str]" = OrderedDict()
        for img in soup.find_all(["img", "source"]):
            alt = img.get("alt") or ""
            for attr in ("src", "data-src", "data-lazy-src", "data-original", "data-bg", "data-background"):
                v = img.get(attr)
                if v and not v.startswith("data:"):
                    seen_imgs.setdefault(v, alt)
            for attr in ("srcset", "data-srcset", "data-lazy-srcset"):
                v = img.get(attr)
                if v:
                    for cand in v.split(","):
                        u = cand.strip().split(" ")[0]
                        if u and not u.startswith("data:"):
                            seen_imgs.setdefault(u, alt)
        for el in soup.find_all(style=re.compile(r"background(-image)?\s*:", re.I)):
            for m in re.finditer(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)", el["style"]):
                seen_imgs.setdefault(m.group(1), "")
        for el in soup.find_all(attrs={"data-bg-image": True}):
            seen_imgs.setdefault(el["data-bg-image"], "")
        for meta in soup.find_all("meta", attrs={"property": re.compile(r"^og:image", re.I)}):
            if meta.get("content"):
                seen_imgs.setdefault(meta["content"], "og:image")
        for link in soup.find_all("link", attrs={"rel": True}):
            rels = link["rel"] if isinstance(link["rel"], list) else [link["rel"]]
            if any(x in ("icon", "apple-touch-icon", "shortcut") for x in rels) and link.get("href"):
                seen_imgs.setdefault(link["href"], "icon")
        for src, alt in seen_imgs.items():
            abs_url = normalise_url(urljoin(rec.final_url, src))
            rec.images.append({"src": abs_url, "alt": alt})
            self.note_image(abs_url, alt, rec.final_url)
        rec.stock_named_images = sum(1 for i in rec.images if STOCK_NAME_RE.search(os.path.basename(urlparse(i["src"]).path)))

        # Links
        internal, outbound = OrderedDict(), OrderedDict()
        for a in soup.find_all("a", href=True):
            href = a["href"].strip()
            if not href or href.startswith(("#", "mailto:", "tel:", "javascript:")):
                continue
            abs_url = normalise_url(urljoin(rec.final_url, href))
            if self.is_internal(abs_url):
                internal[abs_url] = True
            else:
                outbound[abs_url] = True
        rec.internal_links = list(internal)
        rec.outbound_links = list(outbound)

        # Main content → markdown
        main = self.extract_main(soup)
        text = main.get_text(" ", strip=True)
        rec.word_count = len(re.findall(r"\b\w+\b", text))
        rec.romark_mentions = len(ROMARK_RE.findall(text))
        rec.local_mentions = len(LOCAL_RE.findall(text))
        rec.phone_mentions = len(PHONE_RE.findall(text))
        markdown = md(str(main), heading_style="ATX", strip=["script", "style"])
        markdown = re.sub(r"\n{3,}", "\n\n", markdown).strip()
        front = [
            f"# {rec.title or rec.final_url}", "",
            f"- source: {rec.final_url}",
            f"- archived: {now_iso()}",
            f"- canonical: {rec.canonical}",
            f"- meta_description: {rec.meta_description}", "",
            "---", "",
        ]
        rec.md_file = f"pages/{slug}.md"
        (self.out / rec.md_file).write_text("\n".join(front) + markdown + "\n", encoding="utf-8")
        rec.json_file = f"pages/{slug}.json"
        (self.out / rec.json_file).write_text(json.dumps(asdict(rec), indent=2, ensure_ascii=False), encoding="utf-8")
        setattr(rec, "_text", text)

    def crawl(self):
        self.load_robots()
        queue: deque[tuple[str, str]] = deque()
        queued: set[str] = set()

        def push(u: str, via: str):
            u = normalise_url(u)
            if u in queued or u in self.pages:
                return
            if self.enqueue_ok(u, via):
                queued.add(u)
                queue.append((u, via))

        push(self.base_url + "/", "homepage")
        for u, via in self.load_sitemaps():
            push(u, via)
        self.log(kind="info", msg=f"seeded {len(queue)} urls ({len(self.sitemap_urls)} robots sitemap hints)")

        while queue and len(self.pages) < self.max_pages:
            url, via = queue.popleft()
            # A redirect target we've already archived under its final URL — still record the alias.
            self.process_page(url, via)
            rec = self.pages[url]
            if rec.final_url and rec.final_url != url and rec.final_url not in self.pages and rec.status == 200:
                # Archive under final URL as well so redirect map knows both.
                self.pages[rec.final_url] = rec
            for link in rec.internal_links:
                push(link, url)
            for href in rec.internal_links:
                if guess_ext(href) in DOC_EXT:
                    self.note_file(href, url)
        if queue:
            self.log(kind="warn", msg=f"max-pages {self.max_pages} reached with {len(queue)} urls still queued")
            for u, via in queue:
                self.skipped.append({"url": u, "reason": "max-pages-reached", "via": via})

    # ---- images

    def local_name_for(self, url: str, suffix: str = "") -> str:
        path = urlparse(url).path
        name = unquote(os.path.basename(path)) or "unnamed"
        name = re.sub(r"[^A-Za-z0-9._-]+", "_", name)
        if suffix:
            stem, ext = os.path.splitext(name)
            name = f"{stem}{suffix}{ext}"
        if name in self.used_filenames and self.used_filenames[name] != url:
            m = WP_UPLOAD_DATE_RE.search(path)
            prefix = f"{m.group(1)}-{m.group(2)}_" if m else hashlib.sha1(url.encode()).hexdigest()[:8] + "_"
            name = prefix + name
        self.used_filenames[name] = url
        return name

    def download_binary(self, url: str, dest_dir: Path, kind: str) -> tuple[int, str, str]:
        """Returns (bytes, local_name, status). Does not keep a file on non-200."""
        r = self.get(url, kind, stream=True)
        if r is None:
            return 0, "", "error"
        if r.status_code != 200:
            r.close()
            return 0, "", f"http {r.status_code}"
        ctype = r.headers.get("Content-Type", "").lower()
        if "text/html" in ctype:
            r.close()
            return 0, "", "html-not-binary"
        name = self.local_name_for(normalise_url(r.url) if r.url else url)
        dest = dest_dir / name
        n = 0
        with open(dest, "wb") as fh:
            for chunk in r.iter_content(65536):
                fh.write(chunk)
                n += len(chunk)
        r.close()
        if n == 0:
            dest.unlink(missing_ok=True)
            return 0, "", "empty"
        return n, name, "ok"

    def fetch_images(self):
        internal = [u for u, rec in self.image_records.items() if rec["internal"]]
        # Group resized variants with their original so we keep the largest once.
        groups: "OrderedDict[str, list[str]]" = OrderedDict()
        for u in internal:
            base = os.path.basename(urlparse(u).path)
            m = WP_RESIZE_RE.match(base)
            key = u
            if m:
                key = u[: len(u) - len(base)] + m.group("stem") + m.group("ext")
            groups.setdefault(key, []).append(u)
        self.log(kind="info", msg=f"{len(internal)} internal image urls in {len(groups)} groups (resized variants collapsed)")
        done = 0
        for original_url, variants in groups.items():
            if done >= self.max_images:
                for v in variants:
                    self.image_records[v]["status"] = "max-images-reached"
                continue
            candidates = list(OrderedDict.fromkeys([original_url] + variants))
            best: tuple[int, str, str] | None = None
            results = {}
            for cand in candidates:
                if not self.allowed_by_robots(cand):
                    results[cand] = (0, "", "robots-disallow")
                    continue
                n, name, status = self.download_binary(cand, self.images_dir, "image")
                done += 1
                results[cand] = (n, name, status)
                if status == "ok" and (best is None or n > best[0]):
                    if best is not None:
                        (self.images_dir / best[1]).unlink(missing_ok=True)
                        self.used_filenames.pop(best[1], None)
                    best = (n, name, cand)
                elif status == "ok":
                    (self.images_dir / name).unlink(missing_ok=True)
                    self.used_filenames.pop(name, None)
            for cand in candidates:
                n, name, status = results[cand]
                if cand not in self.image_records:
                    # Original reached only via a -WxH variant: inherit the variants' pages and alt text.
                    self.image_records[cand] = {"url": cand, "internal": True, "local_file": "", "bytes": 0, "status": ""}
                    self.image_pages.setdefault(cand, set())
                    for v in variants:
                        self.image_pages[cand] |= self.image_pages.get(v, set())
                        if self.image_alts.get(v):
                            self.image_alts.setdefault(cand, set()).update(self.image_alts[v])
                rec = self.image_records[cand]
                rec["status"] = status
                rec["bytes_fetched"] = n
                if best and cand == best[2]:
                    rec["local_file"] = f"images/{best[1]}"
                    rec["bytes"] = best[0]
                    rec["kept"] = True
                else:
                    rec["kept"] = False
                    rec["kept_as"] = f"images/{best[1]}" if best else ""
            if best is None:
                self.failed.append({"kind": "image", "url": original_url, "reason": "; ".join(f"{c}: {results[c][2]}" for c in candidates)})

    def fetch_files(self):
        for url, rec in self.file_records.items():
            if not self.allowed_by_robots(url):
                rec["status"] = "robots-disallow"
                continue
            n, name, status = self.download_binary(url, self.files_dir, "file")
            rec["status"], rec["bytes"], rec["local_file"] = status, n, (f"files/{name}" if name else "")
            if status != "ok":
                self.failed.append({"kind": "file", "url": url, "reason": status})

    # ---- outputs

    def similarity_pass(self):
        texts = {u: getattr(r, "_text", "") for u, r in self.pages.items() if r.status == 200 and u == (r.final_url or u)}
        sh = {u: shingles(t) for u, t in texts.items()}
        urls = list(sh)
        for i, a in enumerate(urls):
            best, best_u = 0.0, ""
            for b in urls:
                if a == b or not sh[a] or not sh[b]:
                    continue
                inter = len(sh[a] & sh[b])
                j = inter / max(1, min(len(sh[a]), len(sh[b])))   # containment: how much of the smaller page is in the other
                if j > best:
                    best, best_u = j, b
            self.pages[a].max_similarity = round(best, 3)
            self.pages[a].most_similar_page = best_u

    def unique_pages(self) -> list[PageRecord]:
        seen, out = set(), []
        for u, r in self.pages.items():
            if id(r) in seen:
                continue
            seen.add(id(r))
            out.append(r)
        return out

    def write_outputs(self):
        pages = self.unique_pages()
        with open(self.out / "index.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["url", "title", "meta_description", "h1", "word_count", "image_count", "status"])
            for r in pages:
                w.writerow([r.url, r.title, r.meta_description, " | ".join(r.h1), r.word_count, len(r.images), r.status])
        with open(self.out / "redirect-map.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["old_url", "suggested_new_path"])
            seen_old = set()
            for u, r in self.pages.items():
                # One row per OLD url that answered 200 (directly or via redirect) — aliases included,
                # because each of them needs a 301 on the new site.
                if r.status == 200 and u not in seen_old:
                    seen_old.add(u)
                    w.writerow([u, ""])
        with open(self.out / "images.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["image_url", "internal", "kept", "local_file", "bytes", "status", "alt_text", "used_on_pages"])
            for u, rec in self.image_records.items():
                w.writerow([u, rec.get("internal"), rec.get("kept", ""), rec.get("local_file", ""), rec.get("bytes", 0),
                            rec.get("status", ""), " | ".join(sorted(self.image_alts.get(u, []))),
                            " | ".join(sorted(self.image_pages.get(u, [])))])
        with open(self.out / "links.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["from_page", "to_url", "type"])
            for r in pages:
                for l in r.internal_links:
                    w.writerow([r.final_url or r.url, l, "internal"])
                for l in r.outbound_links:
                    w.writerow([r.final_url or r.url, l, "outbound"])
        if self.file_records:
            with open(self.out / "files.csv", "w", newline="", encoding="utf-8") as fh:
                w = csv.writer(fh)
                w.writerow(["file_url", "local_file", "bytes", "status", "linked_from"])
                for u, rec in self.file_records.items():
                    w.writerow([u, rec["local_file"], rec["bytes"], rec["status"], " | ".join(sorted(rec["pages"]))])
        with open(self.out / "skipped.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["url", "reason", "found_via"])
            seen_skip = set()
            for s in self.skipped:
                if (s["url"], s["reason"]) in seen_skip:
                    continue
                seen_skip.add((s["url"], s["reason"]))
                w.writerow([s["url"], s["reason"], s["via"]])
        with open(self.out / "failed.csv", "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["kind", "url", "reason"])
            for f in self.failed:
                w.writerow([f["kind"], f["url"], f["reason"]])
        self.write_report(pages)

    def write_report(self, pages: list[PageRecord]):
        ok = [p for p in pages if p.status == 200]
        # One evidence row per final URL (a redirect alias shares its target's content).
        ok_by_final = list(OrderedDict((p.final_url or p.url, p) for p in ok).values())
        skipped_unique = {(s["url"], s["reason"]) for s in self.skipped}
        kept_imgs = [r for r in self.image_records.values() if r.get("kept")]
        img_bytes = sum(r["bytes"] for r in kept_imgs)
        file_bytes = sum(r["bytes"] for r in self.file_records.values())
        html_bytes = sum((self.out / p.html_file).stat().st_size for p in pages if p.html_file and (self.out / p.html_file).exists())
        total_bytes = sum(f.stat().st_size for f in self.out.rglob("*") if f.is_file())
        ext_imgs = [u for u, r in self.image_records.items() if not r["internal"]]

        lines = [
            f"# Archive report — {self.base_url}", "",
            f"- Run started: {self.started}  finished: {now_iso()}",
            f"- User-Agent: `{self.ua}`; delay {self.limiter.delay}s between requests; GET only",
            f"- robots.txt: {'found, honoured' if self.robots_text else 'not found / not plain text — treated as allow-all'}",
            f"- Sitemaps read: {len(list(self.raw_dir.glob('sitemap-*.xml')))} (raw copies in raw/)", "",
            "## Totals", "",
            "| Metric | Value |", "|---|---|",
            f"| Pages requested | {len(pages)} |",
            f"| Pages archived (HTTP 200, HTML) | {len(ok_by_final)} unique ({len(ok)} incl. redirect aliases) |",
            f"| Pages with other status | {len(pages) - len(ok)} |",
            f"| Internal image URLs seen | {sum(1 for r in self.image_records.values() if r['internal'])} |",
            f"| Images kept (largest per original) | {len(kept_imgs)} — {human_size(img_bytes)} |",
            f"| External image URLs (not downloaded) | {len(ext_imgs)} |",
            f"| Linked documents downloaded | {sum(1 for r in self.file_records.values() if r['status'] == 'ok')} — {human_size(file_bytes)} |",
            f"| Raw HTML | {human_size(html_bytes)} |",
            f"| Archive folder total | {human_size(total_bytes)} |",
            f"| URLs skipped by rule | {len(skipped_unique)} (skipped.csv) |",
            f"| Failures | {len(self.failed)} (failed.csv) |", "",
        ]
        if self.failed:
            lines += ["## Failed URLs", ""]
            for f in self.failed:
                lines.append(f"- [{f['kind']}] {f['url']} — {f['reason']}")
            lines.append("")
        non200 = [p for p in pages if p.status != 200]
        if non200:
            lines += ["## Pages not returning 200", ""]
            for p in non200:
                lines.append(f"- {p.url} → {p.status} {p.error}")
            lines.append("")

        lines += [
            "## Filler vs real-content evidence (per page)", "",
            "Heuristics only — the verdict column is a suggestion from the numbers in the same row, to be read against the page. ",
            "`similar` = share of this page's 8-word phrases that also appear on the most similar other page (1.0 = fully templated). ",
            "`stock-named` = images whose filename matches a stock-library or camera-default pattern. Alt text and filenames are in images.csv.", "",
            "| Page | Words | Romark | Local | Phone | Imgs | Stock-named | Similar | Most similar page | Suggested |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        for p in sorted(ok_by_final, key=lambda x: (-x.max_similarity, x.url)):
            verdict = []
            if p.max_similarity >= 0.6:
                verdict.append("templated copy")
            if p.romark_mentions == 0 and p.local_mentions == 0:
                verdict.append("no Romark/local reference")
            if p.images and p.stock_named_images / max(1, len(p.images)) >= 0.5:
                verdict.append("mostly stock-named images")
            if not verdict:
                verdict.append("looks like real content")
            sim_page = p.most_similar_page.replace(self.base_url, "") or "-"
            lines.append(f"| {p.final_url.replace(self.base_url, '') or '/'} | {p.word_count} | {p.romark_mentions} | {p.local_mentions} | {p.phone_mentions} | "
                         f"{len(p.images)} | {p.stock_named_images} | {p.max_similarity:.2f} | {sim_page} | {'; '.join(verdict)} |")
        lines += ["", "## Images with stock-library or camera-default filenames", ""]
        stock = [(u, r) for u, r in self.image_records.items() if STOCK_NAME_RE.search(os.path.basename(urlparse(u).path))]
        if stock:
            for u, r in stock:
                lines.append(f"- {u} — alt: {' | '.join(sorted(self.image_alts.get(u, []))) or '(none)'} — on {len(self.image_pages.get(u, []))} page(s)")
        else:
            lines.append("- none matched the filename patterns")
        lines += ["", "## Outbound domains linked", ""]
        domains: dict[str, int] = {}
        for p in ok:
            for l in p.outbound_links:
                d = urlparse(l).netloc
                domains[d] = domains.get(d, 0) + 1
        for d, n in sorted(domains.items(), key=lambda x: -x[1]):
            lines.append(f"- {d} ({n} link(s))")
        lines += ["", "## Files", "",
                  "- `index.csv` — url, title, meta_description, h1, word_count, image_count, status",
                  "- `redirect-map.csv` — old_url, suggested_new_path (blank, for Rob)",
                  "- `images.csv` — every image URL seen, what was kept, alt text, pages using it",
                  "- `links.csv` — every internal and outbound link per page",
                  "- `skipped.csv` / `failed.csv` — rule skips and failures",
                  "- `pages/<slug>.html|.md|.json` — raw HTML, markdown of main content, metadata",
                  "- `images/`, `files/`, `raw/` (robots.txt, sitemaps), `crawl-log.jsonl` (every request)", ""]
        (self.out / "report.md").write_text("\n".join(lines), encoding="utf-8")

    def run(self):
        self.log(kind="info", msg=f"start base={self.base_url} out={self.out}")
        self.crawl()
        self.fetch_images()
        self.fetch_files()
        self.similarity_pass()
        self.write_outputs()
        self.log_fh.close()


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--out", required=True, help="output folder (created if missing)")
    ap.add_argument("--base-url", default=DEFAULT_BASE)
    ap.add_argument("--delay", type=float, default=1.0, help="seconds between requests (default 1.0)")
    ap.add_argument("--max-pages", type=int, default=500)
    ap.add_argument("--max-images", type=int, default=3000)
    ap.add_argument("--user-agent", default=DEFAULT_UA)
    args = ap.parse_args(argv)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)
    a = Archiver(args.base_url, out, args.delay, args.max_pages, args.max_images, args.user_agent)
    a.run()
    pages = a.unique_pages()
    ok = sum(1 for p in pages if p.status == 200)
    kept = sum(1 for r in a.image_records.values() if r.get("kept"))
    print(f"done: {ok}/{len(pages)} pages archived, {kept} images kept, {len(a.failed)} failures -> {out / 'report.md'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
