#!/usr/bin/env python3
"""Static QA checks for site routing, links and basic SEO metadata.

Fails with non-zero exit when critical checks do not pass.
"""

from __future__ import annotations

import re
import sys
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Dict, List, Tuple
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
SITEMAP = SITE / "sitemap.xml"

REQUIRED_ROUTES = [
    "/",
    "/servicios/",
    "/servicios/desarrollo-web/",
    "/servicios/automatizacion/",
    "/servicios/soporte-it/",
    "/proyectos/",
    "/proyectos/trackflow/",
    "/proyectos/clawmate/",
    "/proyectos/talk-to-the-machine/",
    "/certificaciones/",
    "/sobre-mi/",
    "/contacto/",
    "/faq/",
    "/legal/aviso-legal/",
    "/legal/privacidad/",
    "/legal/cookies/",
    "/privacy-policy/",
    "/terms-of-service/",
    "/data-deletion/",
    "/auth/tiktok/callback/",
    "/auth/facebook/callback/",
    "/gracias/",
]


@dataclass
class ParsedPage:
    route: str
    file_path: Path
    title: str
    h1: str
    canonical: str
    links: List[str]
    is_redirect_alias: bool


class HtmlInspector(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.title = ""
        self.h1 = ""
        self.canonical = ""
        self.links: List[str] = []
        self.redirect_target = ""
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag: str, attrs: List[Tuple[str, str]]) -> None:
        data = dict(attrs)
        if tag == "a":
            href = (data.get("href") or "").strip()
            if href:
                self.links.append(href)
        elif tag == "title":
            self._in_title = True
        elif tag == "h1" and not self.h1:
            self._in_h1 = True
        elif tag == "link" and (data.get("rel") or "").lower() == "canonical":
            self.canonical = (data.get("href") or "").strip()
        elif tag == "meta" and (data.get("http-equiv") or "").lower() == "refresh":
            content = (data.get("content") or "").strip()
            m = re.search(r"url\s*=\s*(.+)$", content, flags=re.IGNORECASE)
            if m:
                self.redirect_target = m.group(1).strip()

    def handle_endtag(self, tag: str) -> None:
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data: str) -> None:
        text = data.strip()
        if not text:
            return
        if self._in_title:
            self.title += text
        if self._in_h1:
            self.h1 += (" " if self.h1 else "") + text


def route_from_index(path: Path) -> str:
    rel = path.parent.relative_to(SITE)
    if str(rel) == ".":
        return "/"
    return "/" + str(rel).replace("\\", "/") + "/"


def parse_pages() -> Dict[str, ParsedPage]:
    pages: Dict[str, ParsedPage] = {}
    for index in sorted(SITE.rglob("index.html")):
        html = index.read_text(encoding="utf-8", errors="ignore")
        parser = HtmlInspector()
        parser.feed(html)
        route = route_from_index(index)
        pages[route] = ParsedPage(
            route=route,
            file_path=index,
            title=parser.title,
            h1=parser.h1,
            canonical=parser.canonical,
            links=parser.links,
            is_redirect_alias=bool(parser.redirect_target),
        )
    return pages


def normalize_internal_href(href: str) -> str:
    parsed = urlsplit(href)
    path = parsed.path
    if not path:
        return ""
    if not path.endswith("/"):
        path += "/"
    return path


def check_sitemap() -> List[str]:
    issues: List[str] = []
    if not SITEMAP.exists():
        return ["Missing site/sitemap.xml"]

    text = SITEMAP.read_text(encoding="utf-8", errors="ignore")
    if "https://jonathanesteban.dev/servicios/soporte-it/" not in text:
        issues.append("Sitemap missing canonical support IT URL /servicios/soporte-it/")
    if "https://jonathanesteban.dev/soporte-it/" in text:
        issues.append("Sitemap still contains deprecated /soporte-it/ URL")
    if "https://jonathanesteban.dev/auth/tiktok/callback/" in text:
        issues.append("Sitemap should not list OAuth callback URL /auth/tiktok/callback/")
    if "https://jonathanesteban.dev/auth/facebook/callback/" in text:
        issues.append("Sitemap should not list OAuth callback URL /auth/facebook/callback/")
    return issues


def main() -> int:
    pages = parse_pages()
    failures: List[str] = []
    warnings: List[str] = []

    for route in REQUIRED_ROUTES:
        if route not in pages:
            failures.append(f"Missing required route: {route}")

    for route, page in pages.items():
        if not page.title:
            failures.append(f"Missing <title>: {route} ({page.file_path})")
        if not page.h1 and not page.is_redirect_alias:
            failures.append(f"Missing <h1>: {route} ({page.file_path})")
        if not page.canonical:
            warnings.append(f"Missing canonical: {route} ({page.file_path})")

        for href in page.links:
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#")):
                continue
            if not href.startswith("/"):
                continue
            target = normalize_internal_href(href)
            if target and target not in pages:
                failures.append(
                    f"Broken internal link: {route} -> {href} (resolved: {target})"
                )

    failures.extend(check_sitemap())

    print("QA summary")
    print(f"- Pages parsed: {len(pages)}")
    print(f"- Required routes: {len(REQUIRED_ROUTES)}")
    print(f"- Failures: {len(failures)}")
    print(f"- Warnings: {len(warnings)}")

    if warnings:
        print("\nWarnings:")
        for item in warnings:
            print(f"  - {item}")

    if failures:
        print("\nFailures:")
        for item in failures:
            print(f"  - {item}")
        return 1

    print("\nAll critical QA checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
