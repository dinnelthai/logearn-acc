/* 全站搜索小组件。给页面里放一个 <input id="site-search-input">，这个脚本会接管它。
   命中列表是手写的索引，不是全文抓取——覆盖主要页面/板块/高频问题即可。 */
(function () {
  var DATA = [
    { t: "新人入门 · FAQ 常见问题", d: "常见问题分类检索、搜关键词", u: "faq.html" },
    { t: "怎么购买 Credits?", d: "充值 SOL、购买 100K Credits、账单与用量估算", u: "faq.html#buy-credits" },
    { t: "VIP 怎么买?", d: "周卡 / 月卡 / 100X NFT 三条路径", u: "faq.html#buy-vip" },
    { t: "K 线看不见、指标不对", d: "USD/市值口径、log 坐标、清空本地缓存", u: "faq.html#cat-异常排查" },
    { t: "看板配置常见问题", d: "信号看板与战壕看板的过滤条件区别", u: "faq.html#cat-看板配置" },
    { t: "风控判断常见问题", d: "止盈止损、仓位与风控相关问答", u: "faq.html#cat-风控判断" },
    { t: "界面操作常见问题", d: "新创建 / 即将迁移 / 已迁移等界面说明", u: "faq.html#cat-界面操作" },
    { t: "信号系统常见问题", d: "六大信号是什么、怎么只看一种信号", u: "faq.html#cat-信号系统" },
    { t: "六大信号自定义筛选", d: "早期精选、苏醒信号等六种信号的过滤设置", u: "signal-filter.html" },
    { t: "代币详情页布局", d: "K 线、指标、信号看板、战壕看板的区域说明", u: "detail-page.html" },
    { t: "AI 策略引擎", d: "策略引擎四个入口、官方三大策略、导入与配置", u: "ai-strategy.html" },
    { t: "官方推荐的三大策略", d: "1.5段策略、强势盘策略、苏醒接力策略对比", u: "ai-strategy.html#official-strategies" },
    { t: "导入官方策略", d: "从 GitHub 拿策略文本，粘贴导入", u: "ai-strategy.html#import" },
    { t: "基本设置这一页", d: "触发方式、交易参数、网格挂单", u: "ai-strategy.html#basic-settings" },
    { t: "策略逻辑:写判断代码", d: "ctx 数据、一票否决写法、代码示例", u: "ai-strategy.html#logic" },
    { t: "实战案例", d: "苏醒策略命中案例复盘(LAYOOO、CZ26)", u: "ai-strategy.html#cases" },
    { t: "复盘归档", d: "每日复盘、直播回放", u: "recap.html" },
    { t: "知识库首页", d: "六大分区总览、官方资源入口", u: "index.html" }
  ];

  function injectStyle() {
    if (document.getElementById("site-search-style")) return;
    var css =
      ".site-search{position:relative;max-width:420px;}" +
      ".site-search input{width:100%;box-sizing:border-box;background:var(--bg-card,#121512);" +
      "border:1px solid var(--line,#24302a);border-radius:10px;color:var(--text,#e9efe9);" +
      "font-size:14px;padding:10px 14px;outline:none;font-family:inherit;}" +
      ".site-search input:focus{border-color:var(--green-dim,#1f5c3f);}" +
      ".site-search input::placeholder{color:var(--text-faint,#5a685f);}" +
      ".site-search-results{position:absolute;left:0;right:0;top:calc(100% + 6px);z-index:20;" +
      "background:var(--bg-card,#121512);border:1px solid var(--line,#24302a);border-radius:10px;" +
      "overflow:hidden;box-shadow:0 12px 28px rgba(0,0,0,.35);display:none;max-height:340px;overflow-y:auto;}" +
      ".site-search-results a{display:block;padding:10px 14px;text-decoration:none;" +
      "border-bottom:1px solid var(--line,#24302a);color:var(--text,#e9efe9);}" +
      ".site-search-results a:last-child{border-bottom:none;}" +
      ".site-search-results a:hover,.site-search-results a.active{background:var(--bg-card-2,#171b17);}" +
      ".site-search-results .r-title{font-size:13.5px;font-weight:500;}" +
      ".site-search-results .r-desc{font-size:12px;color:var(--text-faint,#5a685f);margin-top:2px;}" +
      ".site-search-empty{padding:14px;font-size:13px;color:var(--text-faint,#5a685f);}";
    var style = document.createElement("style");
    style.id = "site-search-style";
    style.textContent = css;
    document.head.appendChild(style);
  }

  function search(q) {
    q = (q || "").trim().toLowerCase();
    if (!q) return [];
    return DATA.filter(function (item) {
      return (item.t + item.d).toLowerCase().indexOf(q) !== -1;
    }).slice(0, 8);
  }

  function init() {
    var input = document.getElementById("site-search-input");
    if (!input) return;
    injectStyle();

    var wrap = input.closest(".site-search") || input.parentNode;
    var box = document.createElement("div");
    box.className = "site-search-results";
    wrap.style.position = wrap.style.position || "relative";
    wrap.appendChild(box);

    function render(items) {
      if (!items.length) {
        box.innerHTML = input.value.trim()
          ? '<div class="site-search-empty">没有匹配的内容,换个关键词试试</div>'
          : "";
        box.style.display = input.value.trim() ? "block" : "none";
        return;
      }
      box.innerHTML = items
        .map(function (item) {
          return (
            '<a href="' + item.u + '"><div class="r-title">' + item.t +
            '</div><div class="r-desc">' + item.d + "</div></a>"
          );
        })
        .join("");
      box.style.display = "block";
    }

    input.addEventListener("input", function () {
      render(search(input.value));
    });
    input.addEventListener("focus", function () {
      if (input.value.trim()) render(search(input.value));
    });
    input.addEventListener("keydown", function (e) {
      if (e.key === "Enter") {
        var items = search(input.value);
        if (items[0]) location.href = items[0].u;
      }
    });
    document.addEventListener("click", function (e) {
      if (!wrap.contains(e.target)) box.style.display = "none";
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
