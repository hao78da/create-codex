# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""补齐所有被引用但不存在的 tags/<slug>.html（占位页，成员未知）。"""
import glob
import io
import os
import re

SITE = ROOT
TAGS = os.path.join(SITE, "tags")

refs = set()
for p in glob.glob(os.path.join(SITE, "**", "*.html"), recursive=True):
    h = io.open(p, encoding="utf-8").read()
    for m in re.finditer(r'tags/([a-z0-9_]+)\.html', h):
        refs.add(m.group(1))

have = {os.path.basename(x)[:-5] for x in glob.glob(os.path.join(TAGS, "*.html"))}
missing = sorted(refs - have)

TPL = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>#%(name)s · 标签</title><link rel="stylesheet" href="../assets/style.css"></head><body>
<header class="top"><div class="wrap"><a class="logo" href="../index.html"><span class="gear"></span>CREATE CODEX<small>机械动力图鉴</small></a>
<nav><a href="../tags.html">标签</a><a href="../index.html">源码</a></nav></div></header>
<main class="wrap">
<nav class="crumb"><a href="../index.html">首页</a> / <a href="../tags.html">标签</a> / %(name)s</nav>
<section class="item-hero"><img class="big" src="../assets/icons/%(icon)s" alt="">
<div><h1>#%(name)s</h1><div class="idline"><span class="copyid">%(tag)s</span></div><span class="badge">标签</span></div></section>
<section class="blk"><h2>成员</h2><p>这个标签由 Forge 或模组在运行时注册，jar 里没有写死成员清单。</p></section>
<section class="blk"><h2>说明</h2><p>本站没有它的成员数据；它出现在配方里时用于匹配一整类材料。</p></section>
</main>
<footer class="wrap foot">数据与图标来自 Create 与 Minecraft 资源，仅用于学习与教学。</footer>
</body></html>"""

for slug in missing:
    tag = slug.replace("_", ":", 1).replace("_", "/")
    ic = "create_gear.png" if os.path.exists(os.path.join(SITE, "assets", "icons", "create_gear.png")) else "_unknown.png"
    io.open(os.path.join(TAGS, slug + ".html"), "w", encoding="utf-8").write(
        TPL % {"name": slug.split("_", 1)[-1].replace("_", " "), "tag": tag, "icon": ic}
    )
print("stub pages:", len(missing))
