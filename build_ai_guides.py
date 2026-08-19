#!/usr/bin/env python3
"""Split the AI strategy handbook into focused bilingual guide pages."""
import re
from pathlib import Path

ROOT=Path(__file__).parent
GUIDES=[
 ('quick-start','zones','official-strategies','快速开始','Quick Start','了解策略引擎入口和整体工作流程。','Learn where the strategy engine appears and how the workflow fits together.'),
 ('strategies','official-strategies','import','官方策略怎么选','Choosing an Official Strategy','对比三大官方策略、适用场景和策略卡信息。','Compare the official strategies, their use cases, and strategy-card information.'),
 ('import','import','basic-settings','导入与更新策略','Importing and Updating','从官方仓库导入策略，并理解顶部操作入口。','Import strategies from the official repository and understand the top-bar actions.'),
 ('settings','basic-settings','logic','基本设置与交易参数','Settings and Trading Parameters','配置触发方式、交易参数和网格挂单。','Configure triggers, trading parameters, and grid orders.'),
 ('logic','logic','cases','策略逻辑与 ctx','Strategy Logic and ctx','理解判断代码、ctx 数据和一票否决规则。','Understand decision code, ctx data, and rejection rules.'),
 ('cases','cases',None,'实战案例与延伸阅读','Trading Cases and Further Reading','结合真实案例复盘策略，并继续学习相关知识点。','Review real cases and continue with related learning.'),
]

def extract_style(html):
    return re.search(r'<style>(.*?)</style>',html,re.S).group(1)

def section(html,start,end):
    a=re.search(r'<section id="'+re.escape(start)+r'"[^>]*>',html)
    if not a: raise RuntimeError('missing section '+start)
    if end:
        b=re.search(r'<section id="'+re.escape(end)+r'"[^>]*>',html[a.end():])
        stop=a.end()+b.start() if b else html.rfind('</body>')
    else:
        footer=html.find('<footer',a.end()); stop=footer if footer>=0 else html.rfind('</body>')
    return html[a.start():stop]

def build(lang):
    en=lang=='en'; source=ROOT/('sources/ai-strategy.en.html' if en else 'sources/ai-strategy.zh.html')
    html=source.read_text(encoding='utf-8'); outdir=ROOT/('en/ai' if en else 'ai');outdir.mkdir(parents=True,exist_ok=True)
    if not (ROOT/'ai-article.css').exists():(ROOT/'ai-article.css').write_text(extract_style((ROOT/'sources/ai-strategy.zh.html').read_text(encoding='utf-8')),encoding='utf-8')
    for slug,start,end,zh_title,en_title,zh_desc,en_desc in GUIDES:
        title=en_title if en else zh_title;desc=en_desc if en else zh_desc
        content=section(html,start,end).replace('src="../shots/','src="../../shots/').replace('src="shots/','src="../shots/')
        content=re.sub(r'href="(?!https?://|#|mailto:)([^"/]+\.html)',r'href="../\1',content)
        content=content.replace('href="#trade-params"','href="settings.html#trade-params"').replace('href="#knowledge"','href="cases.html#knowledge"')
        prevnext=[]
        for s,_,_,zt,et,_,_ in GUIDES: prevnext.append((s,et if en else zt))
        cards=''.join('<a class="guide-link" href="'+s+'.html"'+(' aria-current="page"' if s==slug else '')+'>'+t+'</a>' for s,t in prevnext)
        root='../../' if en else '../'; alt=(root+'ai/'+slug+'.html') if en else (root+'en/ai/'+slug+'.html')
        page='''<!doctype html><html lang="LANG"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>TITLE — LogEarn</title><meta name="description" content="DESC"><link rel="icon" href="ROOTshots/logo.png"><link rel="stylesheet" href="ROOTai-article.css"><link rel="stylesheet" href="ROOTsite.css"><style>.guide-local{max-width:900px;margin:0 auto;padding:18px 24px;display:flex;gap:8px;overflow:auto}.guide-link{white-space:nowrap;padding:7px 10px;border:1px solid var(--line);border-radius:8px;color:var(--text-dim);text-decoration:none;font-size:12px}.guide-link[aria-current="page"]{border-color:var(--green-dim);color:var(--green)}.guide-intro{max-width:900px;margin:0 auto;padding:58px 24px 24px}.guide-intro h1{margin:8px 0 12px}.guide-intro p{color:var(--text-dim)}</style></head><body data-kb-root="ROOT" data-kb-page="ai-strategy.html" data-kb-alt="ALT"><header class="guide-intro"><div class="eyebrow">EYEBROW</div><h1>TITLE</h1><p>DESC</p></header><nav class="guide-local" aria-label="GUIDENAV">CARDS</nav><main>CONTENT</main><script src="ROOTsite.js"></script><script src="ROOTsearch.js"></script></body></html>'''
        vals={'LANG':'en' if en else 'zh-CN','TITLE':title,'DESC':desc,'ROOT':root,'ALT':alt,'EYEBROW':'AI Strategy Guide' if en else 'AI 策略专题','GUIDENAV':'AI strategy guides' if en else 'AI 策略专题','CARDS':cards,'CONTENT':content}
        for k,v in vals.items():page=page.replace(k,v)
        (outdir/(slug+'.html')).write_text(page,encoding='utf-8')
        print((outdir/(slug+'.html')).relative_to(ROOT))

build('zh');build('en')
