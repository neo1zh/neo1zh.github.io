#!/usr/bin/env python3
"""Build the static homepage and standalone LaTeX CV. Python standard library only."""
import html
import json
from pathlib import Path, PurePosixPath

ROOT = Path(__file__).resolve().parents[1]
data = json.loads((ROOT / '_data/research.json').read_text())
papers = data['publications']
assert len({p['id'] for p in papers}) == len(papers), 'Publication IDs must be unique'
for paper in papers:
    assert paper['status'] in ('accepted', 'published', 'under-review')
    assert not paper.get('url') or paper['url'].startswith('https://')
esc = html.escape

def authors(p):
    return esc(p['authors']).replace('Zihao Zhao', '<strong>Zihao Zhao</strong>')

def title(p):
    text = esc(p['title'])
    return f'<a href="{esc(p["url"])}">{text}</a>' if p.get('url') else text

def publication(p):
    status = ' · Accepted' if p['status'] == 'accepted' else ''
    link = f'<a class="paper-link" href="{esc(p["url"])}" aria-label="Read {esc(p["title"])}">Paper <span aria-hidden="true">↗</span></a>' if p.get('url') else ''
    return f'''<li class="publication-entry" id="paper-{p['id']}"><div class="publication-label"><span class="venue-badge">{esc(p['venue'])}</span><span class="publication-year">{p['year']}</span></div><div><h3 class="paper-title">{title(p)}</h3><p class="authors">{authors(p)}</p><p class="publication-citation"><em>{esc(p['venue'])} {p['year']}</em>{status}</p><div class="paper-actions">{link}</div></div></li>'''

portrait_path = data.get('portrait')
if portrait_path:
    path = PurePosixPath(portrait_path)
    assert path.is_absolute() and '..' not in path.parts and path.parts[1] in ('images', 'assets') and (ROOT / portrait_path.lstrip('/')).is_file(), 'Portrait must exist in /images/ or /assets/'
    portrait = f'<img class="portrait-image" src="{esc(portrait_path)}" width="440" height="550" alt="Zihao Zhao" fetchpriority="high">'
else:
    portrait = '<div class="portrait-placeholder" role="img" aria-label="Portrait placeholder for Zihao Zhao"><span aria-hidden="true">Zz.</span><small>Photo pending</small></div>'
portrait = f'<figure class="portrait">{portrait}<figcaption><span>Based at UIUC</span><span>Illinois, USA</span></figcaption></figure>'
accepted = [p for p in papers if p['status'] != 'under-review']
manuscripts = [p for p in papers if p['status'] == 'under-review']
page = (ROOT / 'templates/editorial.html').read_text()
for key, value in {
    'PORTRAIT': portrait,
    'PUBLICATIONS': '\n'.join(publication(p) for p in papers if p.get('selected')),
}.items():
    page = page.replace(f'@@{key}@@', value)
assert '@@' not in page
(ROOT / 'index.html').write_text(page)

def tex_escape(text):
    replacements = {'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '$': r'\$', '#': r'\#', '_': r'\_', '{': r'\{', '}': r'\}', '~': r'\textasciitilde{}', '^': r'\textasciicircum{}', '†': r'$\dagger$', '…': r'\ldots{}', '–': '--', '—': '---'}
    return ''.join(replacements.get(c, c) for c in text)

def tex_publication(p):
    byline = tex_escape(p['authors']).replace('Zihao Zhao', r'\textbf{Zihao Zhao}')
    venue = r'\emph{' + tex_escape(p['venue']) + '}, ' + str(p['year'])
    if p.get('details'):
        venue += ', ' + tex_escape(p['details'])
    venue += '.'
    if p['status'] == 'accepted':
        venue += ' Accepted.'
    if p.get('url'):
        venue += r' \href{' + p['url'] + r'}{[paper]}'
    return r'\pub{' + byline + '}{' + tex_escape(p['title']) + '}{' + venue + '}'

cv = (ROOT / 'templates/cv.tex').read_text()
cv = cv.replace('@@PUBLICATIONS@@', '\n'.join(map(tex_publication, accepted)))
cv = cv.replace('@@MANUSCRIPTS@@', '\n'.join(map(tex_publication, manuscripts)))
assert '@@' not in cv
(ROOT / 'assets/Zihao-Zhao-CV.tex').write_text(cv)

# Preserve familiar entry points without rendering the old template examples.
for path, target in {'about':'/', 'publications':'/#publications', 'cv':'/assets/Zihao-Zhao-CV.pdf', 'resume':'/assets/Zihao-Zhao-CV.pdf'}.items():
    folder = ROOT / path
    folder.mkdir(exist_ok=True)
    folder.joinpath('index.html').write_text(f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><meta http-equiv="refresh" content="0;url={target}"><link rel="canonical" href="https://neo1zh.github.io{target}"><title>Zihao Zhao</title></head><body><p><a href="{target}">Continue to Zihao Zhao’s website or CV</a>.</p></body></html>')
(ROOT / 'about.html').write_text((ROOT / 'about/index.html').read_text())
(ROOT / 'sitemap.xml').write_text(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"><url><loc>https://neo1zh.github.io/</loc><lastmod>{data["updated"]}</lastmod></url></urlset>\n')
print(f'Built homepage and LaTeX CV: {len(accepted)} published/accepted papers, {len(manuscripts)} under review.')
