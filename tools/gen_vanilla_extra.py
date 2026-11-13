# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
"""为「附属页 chip 引用、但不在 273 个收录清单里」的原版物品补页面。

这些物品只在附属模组配方里出现，没有任何 Create 配方引用它们，
所以页面内容就是：图标 + 中文名 + 标签归属 + 一句说明。
"""
import io
import json
import os
import sys

RAW = _os.path.join(WORK, 'raw')
OUT = os.path.join(RAW, "out")
SITE = _os.path.join(ROOT, "docs")
PAGES = os.path.join(SITE, "vanilla")

sys.path.insert(0, RAW)
import gen_vanilla_tags as G

IDS = ["birch_sapling", "blue_ice", "bucket", "end_crystal", "lava", "netherite_ingot",
       "netherite_sword", "oak_sapling", "phantom_membrane", "stick", "water"]

HEAD = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — Create Codex</title>
<link rel="preload" href="../assets/fonts/Minecraft.ttf" as="font" crossorigin>
<link rel="stylesheet" href="../assets/style.css">
<link rel="icon" href="../assets/icons/create_logo.png">
</head><body>
<header class="top"><div class="wrap">
<a class="logo" href="../index.html"><span class="gear"></span><span>CREATE CODEX<small>机械动力图鉴</small></span></a>
<nav><a href="../catalog.html">全部物品</a><a href="../tags.html">标签</a><a href="../mods.html">模组</a><a href="../vanilla.html" style="color:var(--brass2)">原版</a></nav>
</div></header>
<main class="wrap">
<div class="crumb"><a href="../index.html">首页</a> / <a href="../vanilla.html">原版物品</a> / {name}</div>
<div class="item-hero"><img class="big" src="../assets/icons/{icon}" alt="">
<div><h1>{name}</h1><div class="en">minecraft:{slug}</div>
<div class="copyid"><span class="copyid">minecraft:{slug}</span></div></div></div>
<p class="tagline">Minecraft 原版物品。它只出现在附属模组的配方里，没有 Create 本体配方引用它。</p>
{body}
<div class="pager"><span></span><a href="../vanilla.html">返回原版物品</a><span></span></div>
</main>
<footer class="foot"><div class="wrap"><p>数据：Minecraft 1.20.1 标签 + 各模组配方。图标来自 honghemc.cn 的公开素材站，仅用于教学。</p></div></footer>
</body></html>
"""


def main():
    mc = json.load(io.open(os.path.join(OUT, "mc_zh.json"), encoding="utf-8"))
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

    page_files = {os.path.basename(f)[:-5] for f in os.listdir(os.path.join(SITE, "tags")) if f.endswith(".html")}
    labels = {}
    tp = os.path.join(SITE, "tags.html")
    if os.path.exists(tp):
        h = io.open(tp, encoding="utf-8").read()
        import re
        for m in re.finditer(r"<b>([^<]+)</b><small>([^<]+)</small>", h):
            labels[m.group(2)] = m.group(1)

    n = 0
    for slug in IDS:
        iid = "minecraft:" + slug
        name = mc.get("item.minecraft." + slug) or mc.get("block.minecraft." + slug) or slug.replace("_", " ")
        icon = "hhx_%s.png" % slug
        if not os.path.exists(os.path.join(SITE, "assets", "icons", icon)):
            icon = "hh3d_%s.png" % slug
        if not os.path.exists(os.path.join(SITE, "assets", "icons", icon)):
            icon = "_unknown.png"

        chips = []
        for t in sorted(t for t in members if iid in members[t]):
            fn = t.replace(":", "_").replace("/", "_")
            label = labels.get(t) or t.split(":")[-1]
            if fn in page_files:
                chips.append('<a class="chip" href="../tags/%s.html"><span>#%s</span></a>' % (fn, label))
            else:
                chips.append('<span class="chip" style="opacity:.55"><span>#%s</span></span>' % label)

        body = ""
        if chips:
            body = ('<section class="blk"><h2>属于这些标签 <span class="cnt">%d</span></h2>'
                    '<div class="related">%s</div></section>' % (len(chips), "".join(chips)))
        else:
            body = ('<section class="blk"><h2>属于这些标签</h2>'
                    '<p class="uses-note">不属于任何已收录的标签。</p></section>')

        doc = HEAD.format(name=name, icon=icon, slug=slug, body=body)
        io.open(os.path.join(PAGES, slug + ".html"), "w", encoding="utf-8").write(doc)
        n += 1

    print("extra vanilla pages:", n)


if __name__ == "__main__":
    main()
