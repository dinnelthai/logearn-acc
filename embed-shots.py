#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""把截图内嵌进 HTML 的占位框。

图片统一放 img/(可以按主题分子文件夹,比如 img/Strategy/),文件名不用改。三步:

    python3 embed-shots.py --scan                    # 列出 img/ 里还没用过的图
    python3 embed-shots.py --map <文件> <槽位>        # 把某张图绑到某个占位框
    python3 embed-shots.py                           # 内嵌所有已绑定的图

--map 的文件名带上子目录,例如:

    python3 embed-shots.py --map Strategy/1.png ai-engine-panel

占位框在 HTML 里写成:
    <div class="shot-frame pending">
          截图待补充 · <槽位名>
        </div>

已经填过的槽位不会被覆盖;想重填,先把 HTML 里那块改回 pending 占位。
运行前会自动备份到 backup/。红框标注(.callout)仍需手工加。
"""
import base64, io, os, re, shutil, sys, time

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, "img")
SHOTS = os.path.join(BASE, "shots")
BACKUP = os.path.join(BASE, "backup")
MANIFEST = os.path.join(SHOTS, "manifest.txt")
PAGES = ["detail-page.html", "signal-filter.html", "ai-strategy.html",
         "faq.html", "index.html"]
EXTS = (".png", ".jpg", ".jpeg", ".webp", ".gif")

# 槽位 -> 裁切与显示设置
#   crop:   (left, top, right, bottom) 按原图像素裁切,None = 不裁
#   scale:  裁完之后的放大倍数,用于小图放大后仍能读清
#   narrow: True = 限宽 460px 居中(弹窗类竖图用)
SETTINGS = {
    # 详情页全图,红箭头已在图里,保持原样
    "detail-entry":   {"crop": None, "scale": 1, "narrow": False},
    "trench-entry":   {"crop": None, "scale": 1, "narrow": False},
    "chart-log":      {"crop": None, "scale": 1, "narrow": False},
    # 标头 ⋯ 菜单,裁出菜单本身放大 2 倍
    "chart-headmenu": {"crop": (60, 735, 520, 1130), "scale": 2, "narrow": False},
    # 工具栏细条,裁出来放大 2 倍才看得清 USD / 市值
    "chart-usd-mcap": {"crop": (300, 25, 1250, 160), "scale": 2, "narrow": False},
    "faq-usd-toggle": {"crop": (300, 25, 1250, 160), "scale": 2, "narrow": False},
    # 弹窗类,裁到弹窗本身再限宽 460px
    "stage2-normal":  {"crop": (565, 80, 1230, 1445), "scale": 1, "narrow": True},
    "stage2-feature": {"crop": None, "scale": 1, "narrow": True},
    "trench-normal":  {"crop": None, "scale": 1, "narrow": True},
    "trench-feature": {"crop": None, "scale": 1, "narrow": True},
    # 策略引擎:顶栏原图带红箭头,保持原样;导入弹窗只占原图 40%,裁到弹窗本身
    "official-strategy-1": {"crop": None, "scale": 1, "narrow": False},
    "official-strategy-2": {"crop": None, "scale": 1, "narrow": False},
    "import-entry":   {"crop": None, "scale": 1, "narrow": False},
    "import-dialog":  {"crop": (195, 157, 500, 390), "scale": 2, "narrow": True},
    # 基本设置页:上半页整屏,下半页原图已经是放大过的截图,直接用
    "ai-engine-panel":       {"crop": None, "scale": 1, "narrow": False},
    "strategy-trade-config": {"crop": None, "scale": 1, "narrow": False},
    "grid-order":            {"crop": None, "scale": 1, "narrow": False},
    "strategy-logic":        {"crop": None, "scale": 1, "narrow": False},
    # 购买 Credits:充值弹窗和购买按钮是宽图,消费账单是竖长弹窗限宽
    "credits-recharge":      {"crop": None, "scale": 1, "narrow": False},
    "credits-buy":           {"crop": None, "scale": 1, "narrow": False},
    "credits-bill":          {"crop": None, "scale": 1, "narrow": True},
    # 实战案例:竖版海报图,原图即可,限宽显示
    "case-layooo":           {"crop": None, "scale": 1, "narrow": True},
}
DEFAULT = {"crop": None, "scale": 1, "narrow": False}


def find_shot(slot):
    if not os.path.isdir(SHOTS):
        return None
    for fn in sorted(os.listdir(SHOTS)):
        stem, ext = os.path.splitext(fn)
        if stem == slot and ext.lower() in EXTS:
            return os.path.join(SHOTS, fn)
    return None


def encode(path, cfg):
    from PIL import Image
    im = Image.open(path)
    if cfg["crop"]:
        im = im.crop(cfg["crop"])
    if cfg["scale"] != 1:
        im = im.resize((int(im.width * cfg["scale"]), int(im.height * cfg["scale"])),
                       Image.LANCZOS)
    # 页面最宽 770px、窄图 460px,按 2 倍屏封顶,别把 2000px 原图整个塞进去
    cap = 940 if cfg["narrow"] else 1540
    if im.width > cap:
        im = im.resize((cap, int(im.height * cap / im.width)), Image.LANCZOS)
    buf = io.BytesIO()
    im.convert("RGB").save(buf, "JPEG", quality=82, optimize=True)
    return base64.b64encode(buf.getvalue()).decode(), im.size


def main():
    if not os.path.isdir(SHOTS):
        os.makedirs(SHOTS)
        print("已创建 shots/,把截图放进去再跑一次。")
        return

    os.makedirs(BACKUP, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    filled, missing = [], []

    for page in PAGES:
        p = os.path.join(BASE, page)
        if not os.path.exists(p):
            continue
        html = io.open(p, encoding="utf-8").read()
        original = html

        for slot in re.findall(r'截图待补充 · ([a-z0-9-]+)', html):
            path = find_shot(slot)
            if not path:
                missing.append(slot)
                continue
            cfg = dict(DEFAULT, **SETTINGS.get(slot, {}))
            b64, size = encode(path, cfg)
            cls = "shot-frame narrow" if cfg["narrow"] else "shot-frame"
            placeholder_re = re.compile(
                r'(<div class="shot-frame pending">\n)'
                r'(\s+)截图待补充 · %s\n'
                r'(\s+)(</div>)' % re.escape(slot)
            )
            if not placeholder_re.search(html):
                print("  ! %s 的占位框格式对不上,跳过" % slot)
                continue

            def repl(m, cls=cls, b64=b64, slot=slot):
                img = '<img src="data:image/jpeg;base64,%s" alt="%s">' % (b64, slot)
                return '<div class="%s">\n' % cls + m.group(2) + img + '\n' + m.group(3) + m.group(4)

            html = placeholder_re.sub(repl, html)
            filled.append((slot, os.path.basename(path), size, page))

        if html != original:
            shutil.copy(p, os.path.join(BACKUP, "%s.%s" % (page, stamp)))
            io.open(p, "w", encoding="utf-8").write(html)

    if filled:
        print("已嵌入:")
        for slot, fn, size, page in filled:
            print("  %-16s <- %-24s %dx%d  (%s)" % (slot, fn, size[0], size[1], page))
        print("\n备份在 backup/,时间戳 %s" % stamp)
    if missing:
        print("\n还缺(shots/ 里没找到对应文件):")
        for slot in sorted(set(missing)):
            print("  %s.png" % slot)
    if not filled and not missing:
        print("没有待填的占位框。")


def read_manifest():
    """槽位 -> 源文件名"""
    m = {}
    if os.path.exists(MANIFEST):
        for line in io.open(MANIFEST, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#"):
                slot, src = line.split("\t", 1)
                m[slot] = src
    return m


def scan():
    """列出 img/ 里还没绑定到任何槽位的图,以及 HTML 里还空着的占位框。"""
    from PIL import Image
    used = set(read_manifest().values())
    if not os.path.isdir(IMG):
        print("img/ 不存在。")
        return

    # img/ 下可以按主题分子文件夹(img/Strategy/…),这里连子目录一起扫
    unused = []
    for root, dirs, files in os.walk(IMG):
        dirs.sort()
        for f in sorted(files):
            if os.path.splitext(f)[1].lower() not in EXTS:
                continue
            rel = os.path.relpath(os.path.join(root, f), IMG)
            if rel not in used:
                unused.append(rel)
    if unused:
        print("img/ 里还没用过的图:")
        for rel in unused:
            im = Image.open(os.path.join(IMG, rel))
            print("  %-32s %dx%d" % (rel, im.width, im.height))
    else:
        print("img/ 里的图都已绑定。")

    pending = []
    for page in PAGES:
        p = os.path.join(BASE, page)
        if os.path.exists(p):
            html = io.open(p, encoding="utf-8").read()
            for slot in re.findall(r'截图待补充 · ([a-z0-9-]+)', html):
                pending.append((slot, page))
    print()
    if pending:
        print("HTML 里还空着的占位框:")
        for slot, page in pending:
            print("  %-18s (%s)" % (slot, page))
    else:
        print("没有空着的占位框。")


def map_shot(src, slot):
    """把 img/<src> 绑到 <slot>,复制进 shots/ 并记进 manifest。"""
    path = os.path.join(IMG, src)
    if not os.path.exists(path):
        print("img/%s 不存在" % src)
        return
    os.makedirs(SHOTS, exist_ok=True)
    ext = os.path.splitext(src)[1].lower()
    shutil.copy(path, os.path.join(SHOTS, slot + ext))

    m = read_manifest()
    m[slot] = src
    with io.open(MANIFEST, "w", encoding="utf-8") as f:
        f.write(u"# 槽位\t源文件(img/ 下)\n")
        for k in sorted(m):
            f.write(u"%s\t%s\n" % (k, m[k]))
    print("%s  <-  img/%s" % (slot, src))
    print("跑 python3 embed-shots.py 内嵌。")


if __name__ == "__main__":
    if "--scan" in sys.argv:
        scan()
    elif "--map" in sys.argv:
        i = sys.argv.index("--map")
        try:
            map_shot(sys.argv[i + 1], sys.argv[i + 2])
        except IndexError:
            print("用法: embed-shots.py --map <img里的文件名> <槽位名>")
    else:
        main()
