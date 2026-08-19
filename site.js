(function(){
  var isEn=location.pathname.indexOf('/en/')!==-1;
  var base=isEn?'':'en/';
  var root=isEn?'../':'';
  var pages=isEn?[
    ['Start here','index.html','Knowledge Base'],['Start here','faq.html','FAQ'],['Features','detail-page.html','Token Detail Page'],['Signals','signal-filter.html','Signal Filters'],['AI Strategy','ai-strategy.html','AI Strategy Engine'],['Review','recap.html','Daily Recaps']
  ]:[
    ['开始使用','index.html','知识库首页'],['开始使用','faq.html','FAQ 常见问题'],['功能说明','detail-page.html','代币详情页'],['信号系统','signal-filter.html','六大信号筛选'],['AI 策略','ai-strategy.html','AI 策略引擎'],['案例与复盘','recap.html','每日复盘']
  ];
  var file=location.pathname.split('/').pop()||'index.html';
  var current=pages.findIndex(function(p){return p[1]===file});
  var nav='',group='';
  pages.forEach(function(p){if(p[0]!==group){group=p[0];nav+='<div class="kb-nav-group">'+group+'</div>'}nav+='<a href="'+root+p[1]+'"'+(p[1]===file?' aria-current="page"':'')+'>'+p[2]+'</a>'});
  nav+='<div class="kb-nav-group">'+(isEn?'Language':'语言')+'</div><a href="'+(isEn?'../'+file:'en/'+file)+'">'+(isEn?'简体中文':'English')+'</a>';
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
  var side=document.querySelector('.kb-sidebar'),over=document.querySelector('.kb-overlay'),toggle=document.querySelector('.kb-nav-toggle');
  function setOpen(on){side.classList.toggle('open',on);over.classList.toggle('open',on);toggle.setAttribute('aria-expanded',on?'true':'false')}
  toggle.addEventListener('click',function(){setOpen(!side.classList.contains('open'))});over.addEventListener('click',function(){setOpen(false)});document.querySelector('.kb-sidebar-close').addEventListener('click',function(){setOpen(false)});document.addEventListener('keydown',function(e){if(e.key==='Escape')setOpen(false)});
})();
