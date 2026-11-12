# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""Create: Ultimate Factory —— 没物品、只加 37 条配方的包，单独做一页。"""
import io
import json
import os
import re
import zipfile

SITE = ROOT
ICONS = os.path.join(SITE, "assets", "icons")
OUT = os.path.join(SITE, "addon-ultimate-factory.html")
JAR = r"D:\frontend\_raw\mods_intake\create_ultimate_factory-2.2.4-forge-1.20.1.jar"
DATA = json.load(io.open(r"D:\frontend\_raw\out\data.json", encoding="utf-8"))
MC_ZH = json.load(io.open(r"D:\frontend\_raw\out\mc_zh.json", encoding="utf-8"))

items = DATA["items"]
vanilla = {k: v for k, v in DATA.get("vanilla", {}).items()} if isinstance(DATA.get("vanilla"), dict) else {}


def zh(iid):
    d = items.get(iid) or vanilla.get(iid) or {}
    n = d.get("n") or d.get("name") or ""
    if n:
        return n
    short = iid.split(":", 1)[-1]
    for k in ("item.minecraft." + short, "block.minecraft." + short):
        if MC_ZH.get(k):
            return MC_ZH[k]
    return short.replace("_", " ")


def icon(iid):
    ns, short = iid.split(":", 1)
    for c in ("3d_create_%s.png" % short if ns == "create" else "",
              "create_%s.png" % short if ns == "create" else "",
              "hh3d_%s.png" % short if ns == "minecraft" else "",
              "minecraft_%s.png" % short if ns == "minecraft" else ""):
        if c and os.path.exists(os.path.join(ICONS, c)):
            return c
    return "_unknown.png"


def page_of(iid):
    ns, short = iid.split(":", 1)
    if iid in items and os.path.exists(os.path.join(SITE, "items", short + ".html")):
        return "items/%s.html" % short
    if os.path.exists(os.path.join(SITE, "vanilla", short + ".html")):
        return "vanilla/%s.html" % short
    return None


rows = []
agg = {}
z = zipfile.ZipFile(JAR)
for n in z.namelist():
    if not re.search(r"/recipes?/.*\.json$", n):
        continue
    try:
        d = json.loads(z.read(n).decode("utf-8-sig"))
    except Exception:
        continue
    r = d.get("result") or d.get("results")
    r = r if isinstance(r, list) else [r]
    for x in r:
        if not isinstance(x, dict):
            continue
        rid = x.get("item") or x.get("id")
        if not rid:
            continue
        cnt = x.get("count", 1)
        href = page_of(rid)
        name = zh(rid)
        ic = icon(rid)
        label = '<img src="assets/icons/%s" alt=""><span>%s</span><b>×%d</b>' % (ic, name, cnt)
        if href:
            cell = '<a class="chip" href="%s">%s</a>' % (href, label)
        else:
            cell = '<span class="chip">%s</span>' % label
        agg.setdefault(rid, {"count": 0, "n": 0})
        agg[rid]["count"] += cnt
        agg[rid]["n"] += 1
        agg[rid]["cell"] = cell

for rid, a in sorted(agg.items(), key=lambda kv: zh(kv[0])):
    href = page_of(rid)
    label = '<img src="assets/icons/%s" alt=""><span>%s</span><b>×%d</b>' % (icon(rid), zh(rid), a["count"])
    title = "%s · 来自 %d 条配方" % (rid, a["n"])
    if href:
        cell = '<a class="chip" href="%s" title="%s">%s</a>' % (href, title, label)
    else:
        cell = '<span class="chip" title="%s">%s</span>' % (title, label)
    rows.append('<li>%s</li>' % cell)
body = "".join(rows)
html = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Create: Ultimate Factory · 附属模组</title>
<link rel="stylesheet" href="assets/style.css"><style>.chiprow{list-style:none;display:flex;flex-wrap:wrap;gap:8px;padding:0;margin:12px 0}</style></head><body>
<header class="top"><div class="wrap"><span class="logo"><span class="gear"></span>CREATE CODEX<small>机械动力图鉴</small></span>
<a class="backbtn" href="index.html">← 返回关系图</a></div></header>
<main class="wrap"><div class="hero"><img class="big" src="assets/icons/mod_create_ultimate_factory.png" alt="">
<h1>Create: Ultimate Factory</h1><div class="sub">附属模组</div>
<div class="tag">没有物品，只往 Create 里塞了 37 条工厂配方</div></div>
<div class="blk"><h2>这是什么</h2>
<p>一个「配方包」：jar 里<b>没有任何物品、方块、模型</b>，只有 <code>data/create_ultimate_factory/recipe/</code> 下的 37 个配方文件。</p>
<p>也就是说它不新增任何东西，只是把已有的原版材料 / Create 材料用工厂化的方式重新组合——比如把石头、矿、生物材料做成更容易量产的形态。</p>
</div>
<div class="blk"><h2>它加了哪些产出</h2>
<p>下面这些物品本来就是原版或 Create 的，现在多了一条（或几条）产线可以拿到它们。点名字看物品页。</p>
<ul class="chiprow">%s</ul></div>
<div class="ver"><b>命名空间：</b><code>create_ultimate_factory</code>　<b>1.20.1 版本（Forge）：</b>本页配方直接取自该版本的 jar。</div>
</main>
<footer class="wrap foot">数据与图标来自 Create 与 Minecraft 资源，仅用于学习与教学；Minecraft 版权归 Mojang 所有。</footer>
</body></html>""" % body

io.open(OUT, "w", encoding="utf-8").write(html)
print("wrote", OUT, "rows", len(rows))
