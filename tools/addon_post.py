# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
"""附属模组页面后处理：把可跳转的 chip 变成链接，并确保 anchors.js 已加载。

- 同页物品卡：<a class="ch" href="#<card-id>">（点击滚动 + 蓝框高亮由 anchors.js 提供）
- Create 本体物品：指向 items/<slug>.html
- 标签：指向 tags/<tag>.html

幂等：已经是 <a> 的 chip 会跳过。
由 gen_addon*.py 在写文件后调用，也可以单独跑 `python addon_post.py` 处理全部 addon-*.html。
"""
import io
import os
import re
import glob
import json

SITE = ROOT
DATA = r"D:\frontend\_raw\out\data.json"


def _load_site_maps():
    """中文名 / 英文名 -> items/<slug>.html；标签中文名 -> tags/<file>.html"""
    items = {}
    try:
        d = json.load(io.open(DATA, encoding="utf-8"))
        for iid, it in d["items"].items():
            slug = iid.split(":")[1]
            href = "items/%s.html" % slug
            for key in (it.get("n"), it.get("en")):
                if key:
                    items.setdefault(key.strip(), href)
                    items.setdefault(key.strip().lower(), href)
    except Exception as e:
        print("  [chips] data.json 读取失败:", e)

    # 原版物品：英文名 / 中文名 -> vanilla/<slug>.html
    try:
        for iid, it in d.get("vanilla", {}).items():
            slug = iid.split(":")[1]
            href = "vanilla/%s.html" % slug
            for key in (it.get("n"), it.get("en")):
                if key:
                    items.setdefault(key.strip().lower(), href)
    except Exception:
        pass

    # 中文名 -> minecraft id（用于中文 chip 指向原版页）
    try:
        for k, v in json.load(io.open(r"D:\frontend\_raw\out\mc_zh.json", encoding="utf-8")).items():
            for pref in ("item.minecraft.", "block.minecraft."):
                if k.startswith(pref) and v:
                    items.setdefault(v.strip().lower(), "vanilla/%s.html" % k[len(pref):])
    except Exception:
        pass

    tags = {}
    tp = os.path.join(SITE, "tags.html")
    if os.path.exists(tp):
        s = io.open(tp, encoding="utf-8").read()
        for m in re.finditer(r'href="(tags/[^"]+\.html)"[\s\S]{0,300}?<b>([^<]+)</b><small>([^<]+)</small>', s):
            href, label, tid = m.group(1), m.group(2).strip(), m.group(3).strip()
            tags[label] = href
            tags[label.lower()] = href
            tags[tid] = href
            tail = tid.split("/")[-1].split(":")[-1]
            pref = 0 if any(k in tid for k in ("ingots", "plates", "dusts", "nuggets", "storage_blocks")) else 1
            cur = tags.get("~" + tail)
            if cur is None or pref < cur[0]:
                tags["~" + tail] = (pref, href)
        for k in [k for k in tags if k.startswith("~")]:
            tags[k[1:]] = tags[k][1]
            del tags[k]
    return items, tags


def _strip_tags(s):
    s = re.sub(r"<[^>]+>", "", s)
    return re.sub(r"\s+", " ", s).strip()


def _card_map(html):
    """页面内 card id -> 卡片上的物品名"""
    out = {}
    for m in re.finditer(r'<div class="card" id="([^"]+)"', html):
        cid = m.group(1)
        seg = html[m.end():m.end() + 600]
        b = re.search(r"<b>([^<]+)</b>", seg)
        if b:
            out[cid] = b.group(1).strip()
    return out


def _find_span_end(html, start):
    """从 <span ...> 的 '<' 位置开始，返回配对的 </span> 之后的位置。"""
    i = start
    depth = 0
    while i < len(html):
        nxt_open = html.find("<span", i + 4)
        nxt_close = html.find("</span>", i + 4)
        if nxt_close < 0:
            return -1
        if nxt_open != -1 and nxt_open < nxt_close:
            depth += 1
            i = nxt_open
        else:
            if depth == 0:
                return nxt_close + len("</span>")
            depth -= 1
            i = nxt_close
    return -1


_ZH2SLUG = None


def _zh2slug():
    """中文名 -> 原版物品 slug（只保留有页面的）。"""
    global _ZH2SLUG
    if _ZH2SLUG is not None:
        return _ZH2SLUG
    m = {}
    try:
        import json as _j
        here = os.path.dirname(os.path.abspath(__file__))
        mz = _j.load(io.open(os.path.join(here, "out", "mc_zh.json"), encoding="utf-8"))
        for k, v in mz.items():
            if not isinstance(v, str):
                continue
            for pre in ("item.minecraft.", "block.minecraft."):
                if k.startswith(pre):
                    slug = k[len(pre):]
                    if os.path.exists(os.path.join(SITE, "vanilla", slug + ".html")):
                        m.setdefault(v.strip(), slug)
    except Exception:
        pass
    _ZH2SLUG = m
    return m


_ZH2ITEM = None


def _zh2item():
    """中文名 -> Create 物品页 slug。"""
    global _ZH2ITEM
    if _ZH2ITEM is not None:
        return _ZH2ITEM
    m = {}
    try:
        import json as _j
        here = os.path.dirname(os.path.abspath(__file__))
        d = _j.load(io.open(os.path.join(here, "out", "data.json"), encoding="utf-8"))
        for iid, it in (d.get("items") or {}).items():
            short = iid.split(":", 1)[1]
            nm = it.get("n")
            if nm and os.path.exists(os.path.join(SITE, "items", short + ".html")):
                m.setdefault(nm.strip(), short)
    except Exception:
        pass
    _ZH2ITEM = m
    return m


def link_chips(html):
    items, tags = _load_site_maps()
    cards = {v: "#" + k for k, v in _card_map(html).items()}
    page_ids = set(re.findall(r'id="([^"]+)"', html))

    out = []
    pos = 0
    n = 0
    while True:
        i = html.find('<span class="ch', pos)
        if i < 0:
            out.append(html[pos:])
            break
        j = _find_span_end(html, i)
        if j < 0:
            out.append(html[pos:])
            break
        out.append(html[pos:i])
        block = html[i:j]

        inner = block[block.find(">") + 1: block.rfind("</span>")]
        raw = _strip_tags(inner).strip()
        label = raw.lstrip("#").strip()
        low = label.lower()
        if raw.startswith("#"):
            label = "~" + label  # 预留：优先按标签解释
        href = None
        if label.startswith("~"):
            name = label[1:]
            href = tags.get(name) or tags.get("~" + name.split(":")[-1].split("/")[-1]) or tags.get(name.split(":")[-1].split("/")[-1])
            label = name
        if not href:
            # 流体 chip（如 "lava 1mB" / "water 1mB"）→ 原版物品页
            mfl = re.match(r'^([a-z0-9_ ]+)\s+\d+mB$', label)
            if mfl:
                slug = mfl.group(1).strip().replace(' ', '_')
                if os.path.exists(os.path.join(SITE, 'vanilla', slug + '.html')):
                    href = 'vanilla/' + slug + '.html'
                    label = label
        if not href:
            _si = _zh2item().get(label)
            if _si:
                href = 'items/' + _si + '.html'
        if not href:
            _sl = _zh2slug().get(label)
            if _sl:
                href = 'vanilla/' + _sl + '.html'
        if not href:
            href = cards.get(label)
        if not href and label in items:
            href = items[label]
        if not href and label.lower() in items:
            href = items[label.lower()]
        if not href and low in items:
            href = items[low]
        if not href and label in tags:
            href = tags[label]
        if not href and low in tags:
            href = tags[low]

        if not href and not re.search(r"[\u4e00-\u9fff]", label):
            _slug = re.sub(r"[^a-z0-9 ]", "", label.lower()).strip().replace(" ", "_")
            if _slug and os.path.exists(os.path.join(SITE, "vanilla", _slug + ".html")):
                href = "vanilla/%s.html" % _slug
        if href and href.startswith("vanilla/") and not os.path.exists(os.path.join(SITE, href)):
            href = None
        if href and (href in page_ids or href.split("#")[-1] in page_ids or not href.startswith("#")):
            attrs = block[:block.find(">")][len("<span"):]
            block = '<a href="%s"%s>%s</a>' % (href, attrs, inner)
            n += 1
        out.append(block)
        pos = j

    return "".join(out), n


def fix_empty_cells(html):
    """配方格里既没图标也没文字的格子，补一个 ? 占位，避免看起来像漏数据。"""
    return html.replace('<div class="cell"></div>',
                        '<div class="cell"><span class="ch" title="未知材料">?</span></div>')


def strip_site_nav(html):
    """附属页不需要全站导航：从本体关系图进来即可。"""
    return re.sub(r"<nav>[\s\S]*?</nav>", "", html, count=1)


def add_back_button(html):
    """附属页没有全站导航，给一个明确的返回按钮；logo 不再是链接。"""
    BTN = '<a class="backbtn" href="index.html">← 返回关系图</a>'
    html = re.sub(r'<a class="backbtn"[^>]*>.*?</a>', "", html, flags=re.S)
    html = re.sub(r'<a class="logo" href="[^"]*">([\s\S]*?)</a>',
                  r'<span class="logo">\1</span>', html, count=1)
    if "backbtn" in html:
        return html
    return re.sub(r'(<nav>[\s\S]*?</nav>)?</div></header>',
                  lambda m: (m.group(1) or "") + BTN + "</div></header>", html, count=1)


def ensure_anchors(html):
    if "anchors.js" in html:
        return html
    tag = '<script src="assets/anchors.js" defer></script>'
    if "</body>" in html:
        return html.replace("</body>", tag + "</body>", 1)
    return html + tag


def link_cells(html):
    """配方格里「本页有卡片」的物品：包一层页内锚点，点了滚过去并高亮。"""
    cards = {}
    for m in re.finditer(r'<div class="card" id="([^"]+)"', html):
        seg = html[m.start():m.start() + 700]
        nm = re.search(r"<b>([^<]+)</b>", seg)
        if nm:
            cards[nm.group(1).strip()] = m.group(1)
        sm = re.search(r"<small>([^<]+)</small>", seg)
        if sm:
            cards.setdefault(sm.group(1).split(":")[-1], m.group(1))
    if not cards:
        return html

    def cell_repl(m):
        inner = m.group(1)
        if 'class="celllink"' in inner or "<a " in inner:
            return m.group(0)
        name = ""
        t = re.search(r'title="([^"]+)"', inner)
        if t:
            name = t.group(1).strip()
        if not name:
            txt = re.sub(r"<[^>]+>", "", inner).strip()
            name = txt
        cid = cards.get(name)
        if not cid:
            return m.group(0)
        body = re.sub(r"</?span[^>]*>", "", inner)
        return '<div class="cell"><a class="celllink" href="#%s" title="%s">%s</a></div>' % (
            cid, name, body)

    return re.sub(r'<div class="cell">(.*?)</div>', cell_repl, html, flags=re.S)


def postprocess(path):
    if not os.path.exists(path):
        print("  [chips] 跳过（不存在）:", path)
        return 0
    html = io.open(path, encoding="utf-8").read()
    html = strip_site_nav(html)
    html = add_back_button(html)
    html = ensure_anchors(html)
    html = fix_empty_cells(html)
    html = relabel_tag_chips(html)
    html = fill_card_icons(html)
    html = unwrap_missing_links(html)
    html, _ids = ensure_card_ids(html)
    html = link_cells(html)
    html, n = link_chips(html)
    io.open(path, "w", encoding="utf-8").write(html)
    print("  [chips] %s 链接 %d 个" % (os.path.basename(path), n))
    return n


def postprocess_all():
    total = 0
    for p in sorted(glob.glob(os.path.join(SITE, "addon-*.html"))):
        total += postprocess(p)
    print("  [chips] 合计", total)
    return total



def relabel_tag_chips(html):
    """把 tags/x.html 链接里的英文短名（#eggs）换成 tags.html 上的中文名（#鸡蛋）。"""
    tp = os.path.join(SITE, "tags.html")
    if not os.path.exists(tp):
        return html
    h = io.open(tp, encoding="utf-8").read()
    labels = {}
    for m in re.finditer(r'<b>([^<]+)</b><small>([^<]+)</small>', h):
        labels[m.group(2).replace(":", "_").replace("/", "_")] = m.group(1)
    def rep(m):
        fname, label = m.group(1), labels.get(m.group(1))
        if not label:
            return m.group(0)
        return m.group(0).replace(m.group(2), "#" + label, 1)
    return re.sub(r'href="tags/([^"]+)\.html"[^>]*>(#[^<]*)<', rep, html)


_ICON_CACHE = None


def _icon_names():
    global _ICON_CACHE
    if _ICON_CACHE is None:
        _ICON_CACHE = set(os.listdir(os.path.join(SITE, "assets", "icons")))
    return _ICON_CACHE


def fill_card_icons(html):
    """卡片左上角的图标位是空的就按物品 id 找一个替代图，实在没有用齿轮占位。"""
    names = _icon_names()
    out, pos, n = [], 0, 0
    while True:
        i = html.find('<div class="ci"></div>', pos)
        if i < 0:
            out.append(html[pos:])
            break
        out.append(html[pos:i])
        seg = html[i:i + 600]
        m = re.search(r"<small>([a-z0-9_]+):([a-z0-9_/]+)</small>", seg)
        pick = "_unknown.png"
        if m:
            short = m.group(2).split("/")[-1]
            for cand in ("create_" + short + ".png", "3d_create_" + short + ".png",
                         "hh3d_" + short + ".png", "hhx_" + short + ".png",
                         "minecraft_" + short + ".png", m.group(1) + "_" + short + ".png"):
                if cand in names:
                    pick = cand
                    break
            n += 1
        out.append('<div class="ci"><img src="assets/icons/%s" alt="" loading="lazy"></div>' % pick)
        pos = i + len('<div class="ci"></div>')
    return "".join(out)


def unwrap_missing_links(html):
    """指向不存在页面的链接去掉 href，避免死链。"""
    def rep(m):
        tag, href, inner = m.group(1), m.group(2), m.group(3)
        if href.startswith(("tags/", "vanilla/", "items/")):
            if not os.path.exists(os.path.join(SITE, href.split("#")[0])):
                attrs = re.sub(r'href="[^"]*"', "", m.group(0)[:m.group(0).find(">")])
                return "<span%s>%s</span>" % (attrs.replace("<a", ""), inner)
        return m.group(0)
    return re.sub(r'<a([^>]*href="([^"]+)"[^>]*)>([\s\S]*?)</a>', rep, html)


def ensure_card_ids(html):
    """给没有 id 的物品卡补一个 id（用卡片里的命名空间:名字推），供页内 chip 跳转。"""
    out = []
    pos = 0
    n = 0
    while True:
        i = html.find('<div class="card">', pos)
        if i < 0:
            out.append(html[pos:])
            break
        out.append(html[pos:i])
        seg = html[i:i + 900]
        m = re.search(r"<small>([a-z0-9_]+):([a-z0-9_/]+)</small>", seg)
        if m:
            cid = "it-" + m.group(1) + "-" + m.group(2).replace("/", "-")
            out.append('<div class="card" id="%s">' % cid)
            n += 1
        else:
            out.append('<div class="card">')
        pos = i + len('<div class="card">')
    return "".join(out), n


if __name__ == "__main__":
    postprocess_all()
