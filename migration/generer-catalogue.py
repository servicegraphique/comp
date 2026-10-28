#!/usr/bin/env python3
"""Regénère le catalogue local depuis les dossiers de LP convertis."""
from html import escape
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parent / "sites"


class Title(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data)


def page_info(directory):
    parser = Title()
    parser.feed((directory / "index.html").read_text(encoding="utf-8", errors="replace"))
    title = " ".join(" ".join(parser.parts).split()) or directory.name
    source = ""
    report = directory / "rapport-site.md"
    if report.is_file():
        for line in report.read_text(encoding="utf-8", errors="replace").splitlines():
            if line.startswith("- **Page source**"):
                source = line.split("`", 2)[1] if "`" in line else ""
                break
    return title, source


def main():
    pages = []
    for directory in sorted(ROOT.iterdir()):
        if directory.is_dir() and (directory / "index.html").is_file():
            title, source = page_info(directory)
            pages.append((directory.name, title, source))
    cards = "\n".join(
        '<a class="card" href="{slug}/" data-search="{search}">'
        '<strong>{title}</strong><span>{slug}</span><small>{source}</small></a>'.format(
            slug=escape(slug), title=escape(title), source=escape(source),
            search=escape((slug + " " + title + " " + source).lower()))
        for slug, title, source in pages)
    html = '''<!doctype html>
<html lang="fr"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Pages locales — catalogue</title><style>
:root{color-scheme:light;--ink:#18212f;--muted:#64748b;--line:#e2e8f0;--blue:#175cd3}*{box-sizing:border-box}body{margin:0;background:#f6f8fb;color:var(--ink);font:16px/1.5 system-ui,-apple-system,"Segoe UI",sans-serif}.wrap{max-width:1180px;margin:auto;padding:36px 24px 64px}header{margin-bottom:28px}h1{font-size:clamp(2rem,5vw,3.2rem);letter-spacing:-.04em;margin:0 0 8px}.intro{color:var(--muted);max-width:760px;margin:0}.toolbar{display:flex;gap:12px;align-items:center;margin:24px 0}input{width:min(100%,520px);padding:13px 15px;border:1px solid var(--line);border-radius:10px;font:inherit;background:#fff}#count{color:var(--muted);font-size:.92rem}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:14px}.card{display:flex;flex-direction:column;gap:5px;min-height:118px;padding:17px;background:#fff;border:1px solid var(--line);border-radius:12px;color:inherit;text-decoration:none;transition:transform .15s,border-color .15s}.card:hover,.card:focus-visible{transform:translateY(-2px);border-color:var(--blue);outline:none}.card strong{line-height:1.3}.card span{color:var(--blue);font-size:.87rem}.card small{margin-top:auto;color:var(--muted);overflow-wrap:anywhere}footer{margin-top:28px;color:var(--muted);font-size:.9rem}@media(prefers-reduced-motion:reduce){*{transition:none!important}}
</style></head><body><main class="wrap"><header><h1>Pages locales</h1><p class="intro">Catalogue des __COUNT__ pages Webflow converties. Chaque page a son dossier indépendant avec HTML, CSS, JavaScript et ressources locales. Un serveur HTTP local est conseillé; voir <code>migration/README-LOCAL.md</code>.</p></header>
<div class="toolbar"><label for="search">Rechercher une page</label><input id="search" type="search" placeholder="Nom, titre ou fichier source…" autocomplete="off"><span id="count">__COUNT__ pages</span></div><section class="grid" id="pages" aria-label="Pages converties">
__CARDS__
</section><footer>Les soumissions de formulaires et services CRM/SMS nécessitent leurs API distantes; les liens de partenaires restent externes. Les scripts de tracking ont été désactivés dans la version locale.</footer></main>
<script>const input=document.querySelector('#search'),cards=[...document.querySelectorAll('.card')],count=document.querySelector('#count');input.addEventListener('input',()=>{const q=input.value.trim().toLowerCase();let n=0;for(const card of cards){const show=card.dataset.search.includes(q);card.hidden=!show;if(show)n++;}count.textContent=n+' page'+(n===1?'':'s');});</script></body></html>'''.replace("__COUNT__", str(len(pages))).replace("__CARDS__", cards)
    (ROOT / "index.html").write_text(html, encoding="utf-8")
    print(f"Catalogue généré : {len(pages)} pages → {ROOT / 'index.html'}")


if __name__ == "__main__":
    main()
