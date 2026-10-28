#!/usr/bin/env python3
"""Audit sans dépendances Python des sites statiques générés.
Vérifie les fichiers attendus, les ressources HTML/CSS locales et la syntaxe JS.
Le lecteur vidéo YouTube identifié est rapporté comme exception distante connue.
"""
from html.parser import HTMLParser
from pathlib import Path
import re
import subprocess
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent / "sites"
YOUTUBE_ALLOWED = "www.youtube.com"


class Resources(HTMLParser):
    def __init__(self):
        super().__init__()
        self.resources = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        for name in ("src", "poster", "data-src", "data-poster-url"):
            if attrs.get(name):
                self.resources.append((tag, name, attrs[name]))
        if tag == "link" and any(x in attrs.get("rel", "").lower() for x in ("stylesheet", "icon")):
            if attrs.get("href"):
                self.resources.append((tag, "href", attrs["href"]))
        for name in ("srcset", "data-srcset"):
            for part in attrs.get(name, "").split(","):
                value = part.strip().split()
                if value:
                    self.resources.append((tag, name, value[0]))
        for value in attrs.get("data-video-urls", "").split(","):
            if value.strip():
                self.resources.append((tag, "data-video-urls", value.strip()))


def is_external(url):
    return url.startswith(("http://", "https://", "//"))


def check_resource(site, tag, attr, value):
    if is_external(value):
        host = urlsplit(value if not value.startswith("//") else "https:" + value).hostname or ""
        if host == YOUTUBE_ALLOWED:
            return "youtube", None
        return "external", (site.name, tag, attr, value)
    if value.startswith(("data:", "javascript:", "mailto:", "tel:", "#")):
        return "inline", None
    path = value.split("#", 1)[0].split("?", 1)[0]
    if not path:
        return "inline", None
    target = (site / path.lstrip("/")) if not value.startswith("/") else (ROOT / path.lstrip("/"))
    if not target.exists():
        return "broken", (site.name, tag, attr, value)
    return "local", None


def main():
    sites = sorted(p for p in ROOT.iterdir() if p.is_dir() and (p / "index.html").is_file())
    missing, broken, external, youtube = [], [], [], []
    js_failures = []
    for site in sites:
        for required in ("index.html", "style.css", "script.js", "img"):
            if not (site / required).exists():
                missing.append((site.name, required))
        parser = Resources()
        parser.feed((site / "index.html").read_text(encoding="utf-8", errors="replace"))
        for tag, attr, value in parser.resources:
            result, detail = check_resource(site, tag, attr, value)
            if result == "broken":
                broken.append(detail)
            elif result == "external":
                external.append(detail)
            elif result == "youtube":
                youtube.append((site.name, value))
        css = (site / "style.css").read_text(encoding="utf-8", errors="replace")
        for value in re.findall(r"url\(\s*[\"']?([^\"')]+)", css, re.I):
            result, detail = check_resource(site, "css", "url", value)
            if result == "broken":
                broken.append(detail)
            elif result == "external":
                external.append(detail)
            elif result == "youtube":
                youtube.append((site.name, value))
        node = subprocess.run(["node", "--check", str(site / "script.js")],
                              capture_output=True, text=True)
        if node.returncode:
            js_failures.append((site.name, node.stderr.strip().splitlines()[-1:]))

    print(f"Pages analysées : {len(sites)}")
    print(f"Structure manquante : {len(missing)}")
    print(f"Références locales cassées : {len(broken)}")
    print(f"Ressources distantes inattendues : {len(external)}")
    print(f"Erreurs de syntaxe JavaScript : {len(js_failures)}")
    print(f"Ressources YouTube conservées (service externe) : {len(youtube)}")
    for label, rows in (("MISSING", missing), ("BROKEN", broken),
                        ("EXTERNAL", external), ("JS", js_failures)):
        for row in rows:
            print(label, row)
    if missing or broken or external or js_failures:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
