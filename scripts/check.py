#!/usr/bin/env python3
"""Check generated files, local navigation, and publication completeness."""
import json
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.ids, self.links, self.papers = [], [], []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if 'id' in attrs:
            self.ids.append(attrs['id'])
        if tag in ('a', 'link', 'script', 'img'):
            self.links.append(attrs.get('href', attrs.get('src', '')))
        if tag == 'li' and 'publication-entry' in attrs.get('class', ''):
            self.papers.append(attrs['id'])
        if tag == 'img':
            assert attrs.get('alt'), 'Image missing alternate text'

page = Page()
source = (ROOT / 'index.html').read_text()
page.feed(source)
assert not [key for key, count in Counter(page.ids).items() if count > 1], 'Duplicate HTML IDs'
data = json.loads((ROOT / '_data/research.json').read_text())
assert set(page.papers) == {f'paper-{p["id"]}' for p in data['publications'] if p.get('selected')}
for link in page.links:
    url = urlsplit(link)
    if url.scheme or url.netloc:
        continue
    if url.path:
        assert (ROOT / unquote(url.path).lstrip('/')).exists(), f'Missing asset: {link}'
    elif url.fragment:
        assert url.fragment in page.ids, f'Missing anchor: {link}'
assert '@@' not in source
assert (ROOT / '.nojekyll').exists()
assert (ROOT / 'assets/Zihao-Zhao-CV.pdf').read_bytes().startswith(b'%PDF-')
for path in ('about', 'publications', 'cv', 'resume'):
    assert (ROOT / path / 'index.html').is_file()
print(f'Passed: {len(page.papers)} publications, unique anchors, all local assets/links, PDF, and legacy entry points.')
