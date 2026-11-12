# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
"""为 273 个原版物品生成详情页（vanilla/<id>.html）。

数据：out/data.json 的 vanilla + items[].recipes；标签定义复用 gen_vanilla_tags.load_tags()。
"""
import io
import json
import os
import re
import glob
import html as H
import sys

RAW = _os.path.join(WORK, 'raw')
OUT = os.path.join(RAW, "out")
SITE = ROOT
PAGES = os.path.join(SITE, "vanilla")

sys.path.insert(0, RAW)
import gen_vanilla_tags as G


def esc(s):
    return H.escape(str(s or ""))


def icon_for(data, iid):
    slug = iid.split(":", 1)[1]
    hh = "hh3d_%s.png" % slug
    if os.path.exists(os.path.join(SITE, "assets", "icons", hh)):
        return hh
    return (data["vanilla"].get(iid) or {}).get("icon") or "_unknown.png"


def main():
    data = json.load(io.open(os.path.join(OUT, "data.json"), encoding="utf-8"))
    vanilla = data["vanilla"]
    tags = G.load_tags()

    members = {}
    for t, vals in tags.items():
        s = set()
        for v in vals:
            if isinstance(v, str):
                if v.startswith("#"):
                    for x in tags.get(v[1:], []):
                        if isinstance(x, str) and not x.startswith("#"):
                            s.add(x)
                else:
                    s.add(v)
        members[t] = s

    item_tags = {}
    for t, s in members.items():
        for it in s:
            if it in vanilla:
                item_tags.setdefault(it, []).append(t)

    page_files = {os.path.basename(f)[:-5] for f in glob.glob(os.path.join(SITE, "tags", "*.html"))}
    labels = {}
    tp = os.path.join(SITE, "tags.html")
    if os.path.exists(tp):
        h = io.open(tp, encoding="utf-8").read()
        for m in re.finditer(r"<b>([^<]+)</b><small>([^<]+)</small>", h):
            labels[m.group(2)] = m.group(1)

    def tag_href(t):
        fn = t.replace(":", "_").replace("/", "_")
        return ("../tags/%s.html" % fn) if fn in page_files else None

    # 哪些 Create 物品的配方用到这个原版物品（直接引用或经标签）
    used_by = {iid: [] for iid in vanilla}
    for src, it2 in data["items"].items():
        for r in it2.get("recipes") or []:
            for st in r.get("ingredients") or []:
                if not isinstance(st, dict):
                    continue
                sid, tg = st.get("id"), st.get("tag")
                if sid in used_by:
                    if src not in used_by[sid]:
                        used_by[sid].append(src)
                    break
                if tg:
                    for mem in members.get(tg, ()):
                        if mem in used_by and src not in used_by[mem]:
                            used_by[mem].append(src)
                    break

    os.makedirs(PAGES, exist_ok=True)

    HEAD = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s — Create Codex</title>
<link rel="preload" href="../assets/fonts/Minecraft.ttf" as="font" crossorigin>
<link rel="stylesheet" href="../assets/style.css">
<link rel="icon" href="../assets/icons/create_logo.png">
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="../index.html"><span class="gear"></span><span>CREATE CODEX<small>机械动力图鉴</small></span></a>
<nav><a href="../catalog.html">全部物品</a><a href="../tags.html">标签</a><a href="../mods.html">模组</a><a href="../vanilla.html" style="color:var(--brass2)">原版</a></nav>
</div></header>
<main class="wrap">
<div class="crumb"><a href="../index.html">首页</a> / <a href="../vanilla.html">原版物品</a> / %s</div>
"""

    FOOT = """<div class="pager"><span></span><a href="../vanilla.html">返回原版物品</a><span></span></div>
</main>
<footer class="foot"><div class="wrap"><p>原版物品本身没有本站页面级的合成表；这里列的是「哪些 Create 配方拿它当材料」。数据：Minecraft 1.20.1 标签 + Create 模组配方。</p></div></footer>
</body></html>
"""

    n = 0
    for iid, it in vanilla.items():
        slug = iid.split(":", 1)[1]
        name = it.get("n") or slug
        icon = icon_for(data, iid)

        chips = []
        for t in sorted(item_tags.get(iid, [])):
            href = tag_href(t)
            label = labels.get(t) or t.split(":")[-1]
            if href:
                chips.append('<a class="chip" href="%s"><span>#%s</span></a>' % (href, esc(label)))
            else:
                chips.append('<span class="chip" style="opacity:.5"><span>#%s</span></span>' % esc(label))

        recs = []
        for src in used_by.get(iid, []):
            s2 = src.split(":", 1)[1]
            recs.append('<a class="chip" href="../items/%s.html"><img src="../assets/icons/%s" alt="" loading="lazy" decoding="async"><span>%s</span></a>'
                        % (s2, icon_for(data, src), esc(data["items"][src].get("n", s2))))

        body = []
        body.append('<div class="item-hero"><img class="big" src="../assets/icons/%s" alt="">' % icon)
        body.append('<div><h1>%s</h1><div class="en">%s</div>'
                    '<div class="copyid"><span class="copyid">%s</span></div></div></div>'
                    % (esc(name), esc(iid), esc(iid)))
        body.append('<p class="tagline">Minecraft 原版物品。本站只收录 Create 模组的配方，所以这一页给的是「标签归属」和「哪些 Create 配方拿它当材料」。</p>')

        body.append('<section class="blk"><h2>属于这些标签 <span class="cnt">%d</span></h2>' % len(chips))
        body.append('<div class="related">%s</div>' % "".join(chips) if chips
                    else '<p class="uses-note">不属于任何已收录的标签。</p>')
        body.append("</section>")

        body.append('<section class="blk"><h2>被这些 Create 配方用到 <span class="cnt">%d</span></h2>' % len(recs))
        body.append('<div class="related">%s</div>' % "".join(recs) if recs
                    else '<p class="uses-note">本站收录的 Create 配方里没有直接用到它。</p>')
        body.append("</section>")

        doc = (HEAD % (esc(name), esc(name))) + "\n".join(body) + FOOT
        io.open(os.path.join(PAGES, slug + ".html"), "w", encoding="utf-8").write(doc)
        n += 1

    print("vanilla pages:", n)


if __name__ == "__main__":
    main()
