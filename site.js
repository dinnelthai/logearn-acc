(function(){
  var isEn=location.pathname.indexOf('/en/')!==-1;
  var bodyRoot=document.body.getAttribute('data-kb-root');
  var root=bodyRoot!==null?bodyRoot:(isEn?'../':'');
  var pages=isEn?[
    ['Start here','index.html','Knowledge Base'],['Start here','learning-path.html','Beginner Path'],['Start here','faq.html','FAQ'],['Features','detail-page.html','Token Detail Page'],['Signals','signal-filter.html','Signal Filters'],['AI Strategy','ai-strategy.html','AI Strategy Engine'],['Review','recap.html','Daily Recaps']
  ]:[
    ['开始使用','index.html','知识库首页'],['开始使用','learning-path.html','新人学习路径'],['开始使用','faq.html','FAQ 常见问题'],['功能说明','detail-page.html','代币详情页'],['信号系统','signal-filter.html','六大信号筛选'],['AI 策略','ai-strategy.html','AI 策略引擎'],['案例与复盘','recap.html','每日复盘']
  ];
  var file=document.body.getAttribute('data-kb-page')||location.pathname.split('/').pop()||'index.html';
  var current=pages.findIndex(function(p){return p[1]===file});
  var nav='',group='';
  pages.forEach(function(p){if(p[0]!==group){group=p[0];nav+='<div class="kb-nav-group">'+group+'</div>'}nav+='<a href="'+root+p[1]+'"'+(p[1]===file?' aria-current="page"':'')+'>'+p[2]+'</a>'});
  var alt=document.body.getAttribute('data-kb-alt')||(isEn?'../'+file:'en/'+file);
  nav+='<div class="kb-nav-group">'+(isEn?'Language':'语言')+'</div><a href="'+alt+'">'+(isEn?'简体中文':'English')+'</a>';
  var sidebarSearch=document.getElementById('site-search-input')?'':'<div class="site-search"><input id="site-search-input" type="search" autocomplete="off" placeholder="'+(isEn?'Search the knowledge base…':'搜索整个知识库…')+'"></div>';
  document.body.insertAdjacentHTML('afterbegin','<button class="kb-nav-toggle" aria-label="'+(isEn?'Open navigation':'打开导航')+'" aria-expanded="false">☰</button><aside class="kb-sidebar" aria-label="'+(isEn?'Knowledge base navigation':'知识库导航')+'"><div class="kb-sidebar-head">LogEarn KB <button class="kb-sidebar-close" aria-label="'+(isEn?'Close navigation':'关闭导航')+'">×</button></div>'+sidebarSearch+nav+'</aside><div class="kb-overlay"></div>');
  var first=document.querySelector('header.hero, body > section');
  if(first&&current>0) first.insertAdjacentHTML('beforebegin','<nav class="kb-breadcrumb" aria-label="Breadcrumb"><a href="'+root+'index.html">'+(isEn?'Knowledge Base':'知识库')+'</a> / <span>'+pages[current][2]+'</span></nav>');
  if(current>0){
    var prev=pages[current-1],next=pages[current+1];
    var html='<nav class="kb-pager" aria-label="'+(isEn?'Article navigation':'文章导航')+'">';
    html+=prev?'<a href="'+root+prev[1]+'"><small>← '+(isEn?'Previous':'上一篇')+'</small>'+prev[2]+'</a>':'<span></span>';
    html+=next?'<a href="'+root+next[1]+'"><small>'+(isEn?'Next':'下一篇')+' →</small>'+next[2]+'</a>':'<span></span>';
    html+='</nav>';document.body.insertAdjacentHTML('beforeend',html);
  }
  if(file!=='index.html'){
    var article=document.querySelector('main, header.hero');
    var words=(document.querySelector('main')||document.body).textContent.trim().split(/\s+/).length;
    var minutes=Math.max(2,Math.ceil(words/(isEn?220:320)));
    var updated=document.querySelector('meta[name="last-updated"]');
    var date=updated?updated.content:'2026-08-19';
    var meta='<div class="kb-article-meta"><span><strong>'+(isEn?'Reading time':'阅读时间')+'</strong> · '+minutes+' '+(isEn?'min':'分钟')+'</span><span><strong>'+(isEn?'Last updated':'最后更新')+'</strong> · '+date+'</span><span><strong>'+(isEn?'Applies to':'适用版本')+'</strong> · '+(isEn?'Current web version':'当前网页版本')+'</span></div>';
    if(article)article.insertAdjacentHTML('afterend',meta);
    var actual=location.pathname.split('/').pop()||file;
    var key=location.pathname.indexOf('/ai/')!==-1?'ai/'+actual:file;
    var related={
      'learning-path.html':[['faq.html','FAQ'],['detail-page.html',isEn?'Token Detail Page':'代币详情页'],['signal-filter.html',isEn?'Signal Filters':'六大信号筛选']],
      'faq.html':[['learning-path.html',isEn?'Beginner Path':'新人学习路径'],['detail-page.html',isEn?'Token Detail Page':'代币详情页'],['signal-filter.html',isEn?'Signal Filters':'六大信号筛选']],
      'detail-page.html':[['signal-filter.html',isEn?'Signal Filters':'六大信号筛选'],['faq.html','FAQ'],['ai/quick-start.html',isEn?'AI Quick Start':'AI 策略快速开始']],
      'signal-filter.html':[['detail-page.html',isEn?'Token Detail Page':'代币详情页'],['ai/strategies.html',isEn?'Choose a Strategy':'官方策略怎么选'],['faq.html','FAQ']],
      'ai-strategy.html':[['ai/quick-start.html',isEn?'Quick Start':'快速开始'],['ai/strategies.html',isEn?'Choose a Strategy':'官方策略怎么选'],['ai/import.html',isEn?'Import a Strategy':'导入策略']],
      'recap.html':[['ai/cases.html',isEn?'Trading Cases':'实战案例'],['signal-filter.html',isEn?'Signal Filters':'六大信号筛选'],['ai/logic.html',isEn?'Strategy Logic':'策略逻辑']],
      'ai/quick-start.html':[['ai/strategies.html',isEn?'Choose a Strategy':'官方策略怎么选'],['ai/import.html',isEn?'Import a Strategy':'导入策略'],['ai/settings.html',isEn?'Strategy Settings':'策略设置']],
      'ai/strategies.html':[['ai/quick-start.html',isEn?'Quick Start':'快速开始'],['ai/settings.html',isEn?'Strategy Settings':'策略设置'],['ai/cases.html',isEn?'Trading Cases':'实战案例']],
      'ai/import.html':[['ai/quick-start.html',isEn?'Quick Start':'快速开始'],['ai/settings.html',isEn?'Strategy Settings':'策略设置'],['ai/logic.html',isEn?'Strategy Logic':'策略逻辑']],
      'ai/settings.html':[['ai/import.html',isEn?'Import a Strategy':'导入策略'],['ai/logic.html',isEn?'Strategy Logic':'策略逻辑'],['ai/cases.html',isEn?'Trading Cases':'实战案例']],
      'ai/logic.html':[['ai/settings.html',isEn?'Strategy Settings':'策略设置'],['ai/cases.html',isEn?'Trading Cases':'实战案例'],['ai/import.html',isEn?'Import a Strategy':'导入策略']],
      'ai/cases.html':[['ai/logic.html',isEn?'Strategy Logic':'策略逻辑'],['recap.html',isEn?'Daily Recaps':'每日复盘'],['signal-filter.html',isEn?'Signal Filters':'六大信号筛选']]
    };
    var rel=related[key]||related[file];
    if(rel){var langBase=isEn?'en/':'';document.body.insertAdjacentHTML('beforeend','<section class="kb-related"><h2>'+(isEn?'Related documentation':'相关文档')+'</h2><div class="kb-related-grid">'+rel.map(function(x){return'<a href="'+root+langBase+x[0]+'">'+x[1]+' →</a>'}).join('')+'</div></section>')}
    var issue='https://github.com/dinnelthai/logearn-acc/issues/new?title='+encodeURIComponent((isEn?'Documentation feedback: ':'文档纠错：')+document.title);
    document.body.insertAdjacentHTML('beforeend','<div class="kb-feedback">'+(isEn?'Found outdated or unclear information? ':'发现内容过期、步骤不清楚或截图不一致？')+'<a href="'+issue+'" target="_blank" rel="noopener">'+(isEn?'Send documentation feedback':'提交文档纠错')+'</a></div>');
  }
  var side=document.querySelector('.kb-sidebar'),over=document.querySelector('.kb-overlay'),toggle=document.querySelector('.kb-nav-toggle');
  function setOpen(on){side.classList.toggle('open',on);over.classList.toggle('open',on);toggle.setAttribute('aria-expanded',on?'true':'false')}
  toggle.addEventListener('click',function(){setOpen(!side.classList.contains('open'))});over.addEventListener('click',function(){setOpen(false)});document.querySelector('.kb-sidebar-close').addEventListener('click',function(){setOpen(false)});document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false)});
})();
