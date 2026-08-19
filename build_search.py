#!/usr/bin/env python3
"""Build bilingual full-text search indexes from the static HTML pages."""
import json, re
from html import unescape
from pathlib import Path

ROOT=Path(__file__).parent
def clean(s):
    s=re.sub(r'<(script|style)[^>]*>.*?</\1>',' ',s,flags=re.S|re.I)
    s=re.sub(r'<[^>]+>',' ',s)
    return re.sub(r'\s+',' ',unescape(s)).strip()

def build(folder):
    out=[]
    paths=sorted(folder.glob('*.html'))+sorted((folder/'ai').glob('*.html'))
    for path in paths:
        name=path.relative_to(folder).as_posix()
        html=path.read_text(encoding='utf-8')
        title=clean(re.search(r'<title>(.*?)</title>',html,re.S|re.I).group(1)).split('—')[0].strip()
        sections=list(re.finditer(r'<h([12])(?:\s+[^>]*)?(?:id="([^"]+)")?[^>]*>(.*?)</h\1>',html,re.S|re.I))
        if not sections: sections=[None]
        for i,m in enumerate(sections):
            start=m.end() if m else 0; end=sections[i+1].start() if m and i+1<len(sections) else len(html)
            heading=clean(m.group(3)) if m else title
            anchor=(m.group(2) or '') if m else ''
            body=clean(html[start:end])[:1800]
            if body: out.append({'title':title,'heading':heading,'text':body,'url':name+('#'+anchor if anchor else '')})
    return out

for lang,folder in [('zh',ROOT),('en',ROOT/'en')]:
    (ROOT/f'search-index.{lang}.json').write_text(json.dumps(build(folder),ensure_ascii=False,separators=(',',':')),encoding='utf-8')
    print(f'built search-index.{lang}.json')
