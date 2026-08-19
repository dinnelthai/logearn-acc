#!/usr/bin/env python3
"""Fail on common static knowledge-base regressions."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit
import sys

ROOT=Path(__file__).parent
FILES=list(ROOT.glob('*.html'))+list((ROOT/'ai').glob('*.html'))+list((ROOT/'en').glob('*.html'))+list((ROOT/'en/ai').glob('*.html'))

class Parser(HTMLParser):
    def __init__(self): super().__init__(); self.links=[]; self.images=[]; self.ids=[]; self.meta=[]
    def handle_starttag(self,tag,attrs):
        d=dict(attrs)
        if 'id' in d:self.ids.append(d['id'])
        if tag in ('a','link','script'):
            u=d.get('href') or d.get('src')
            if u:self.links.append(u)
        if tag=='img':self.images.append(d)
        if tag=='meta':self.meta.append(d)

errors=[]
for path in FILES:
    p=Parser(); p.feed(path.read_text(encoding='utf-8'))
    if len(p.ids)!=len(set(p.ids)): errors.append(f'{path}: duplicate id')
    if not any(x.get('name')=='description' for x in p.meta): errors.append(f'{path}: missing description')
    for img in p.images:
        if not img.get('alt'): errors.append(f'{path}: image without alt')
        if img.get('src','').startswith('data:'): errors.append(f'{path}: embedded image remains')
    for href in p.links:
        if href.startswith(('http:','https:','mailto:','javascript:','data:','#')):continue
        part=urlsplit(href); target=(path.parent/unquote(part.path)).resolve()
        if part.path and not target.exists(): errors.append(f'{path}: missing {href}')
    if path.stat().st_size>250_000: errors.append(f'{path}: HTML exceeds 250KB')

if errors:
    print('\n'.join(errors));sys.exit(1)
print(f'OK: {len(FILES)} HTML pages checked')
