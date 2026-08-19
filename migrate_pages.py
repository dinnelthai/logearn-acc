#!/usr/bin/env python3
"""One-time migration: externalize embedded images and add shared KB assets."""
import base64, re, subprocess
from pathlib import Path

ROOT=Path(__file__).parent
files=list(ROOT.glob('*.html'))+list((ROOT/'en').glob('*.html'))
shots=ROOT/'shots'; shots.mkdir(exist_ok=True)

# Preserve four Chinese-alt signal screenshots with stable ASCII filenames.
signal_names={
    '信号类型下拉菜单,单独勾选早期精选':'signal-early-select',
    '过滤条件设置弹窗,信号标签页':'signal-early-filter',
    '信号类型下拉菜单,勾选苏醒信号':'signal-wake-select',
    '过滤条件设置弹窗,苏醒信号参数':'signal-wake-filter',
}
try:
    old=subprocess.check_output(['git','show','HEAD:signal-filter.html'],cwd=ROOT,text=True)
    for alt,slug in signal_names.items():
        m=re.search(r'<img src="data:image/([^;]+);base64,([^"]+)" alt="'+re.escape(alt)+'">',old)
        if m:
            ext='jpg' if m.group(1)=='jpeg' else m.group(1)
            (shots/f'{slug}.{ext}').write_bytes(base64.b64decode(m.group(2)))
except Exception as exc:
    print('signal image recovery skipped:',exc)

for path in files:
    html=path.read_text(encoding='utf-8')
    prefix='../' if path.parent.name=='en' else ''
    for alt,slug in signal_names.items():
        html=html.replace(('src="../shots/.jpg"' if prefix else 'src="shots/.jpg"')+' alt="'+alt+'"','src="'+prefix+'shots/'+slug+'.jpg" alt="'+alt+'"')
    html=re.sub(r'<link rel="icon" type="image/png" href="data:image/png;base64,[^"]+">','<link rel="icon" type="image/png" href="'+prefix+'shots/logo.png">',html)
    def image(m):
        attrs=m.group(1); data=m.group(2); tail=m.group(3)
        altm=re.search(r'alt="([^"]*)"',tail); alt=altm.group(1) if altm else 'image'
        slug='logo' if 'logo' in alt.lower() else re.sub(r'[^a-z0-9-]+','-',alt.lower()).strip('-')
        ext='jpg' if 'jpeg' in attrs else ('png' if 'png' in attrs else 'webp')
        target=shots/f'{slug}.{ext}'
        if not target.exists(): target.write_bytes(base64.b64decode(data))
        loading='' if slug=='logo' else ' loading="lazy" decoding="async"'
        return '<img src="'+prefix+'shots/'+target.name+'"'+tail.rstrip('>')+loading+'>'
    html=re.sub(r'<img src="data:image/([^;]+);base64,([^"]+)"([^>]*)>',image,html)
    css=prefix+'site.css'; js=prefix+'site.js'; search=prefix+'search.js'
    if 'site.css' not in html: html=html.replace('</head>','  <link rel="stylesheet" href="'+css+'">\n</head>')
    # Shared navigation must run before search so it can add a sidebar search field.
    html=re.sub(r'\s*<script src="(?:\.\./)?(?:site|search)\.js"></script>','',html)
    html=html.replace('</body>','  <script src="'+js+'"></script>\n  <script src="'+search+'"></script>\n</body>')
    if '<meta name="description"' not in html:
        title=re.search(r'<title>(.*?)</title>',html,re.S).group(1).split('—')[0].strip()
        html=html.replace('</title>','</title>\n  <meta name="description" content="'+title+' · LogEarn 产品知识库">',1)
    path.write_text(html,encoding='utf-8')
    print(path.relative_to(ROOT))
