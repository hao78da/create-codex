# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""把 addon-*.html 中未出现在 mods.html 的页面补成卡片。"""
import io
import os
import re

SITE = _os.path.join(ROOT, "docs")
MODS = os.path.join(SITE, "mods.html")

html = io.open(MODS, encoding="utf-8").read()
have = set(re.findall(r'href="(addon-[^"]+\.html)"', html))

cards = []
for p in sorted(os.listdir(SITE)):
    if not (p.startswith("addon-") and p.endswith(".html")) or p in have:
        continue
    page = io.open(os.path.join(SITE, p), encoding="utf-8").read()
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", page, re.S)
    name = re.sub(r"<[^>]+>", "", h1.group(1)).strip() if h1 else p
    hero = re.search(r'<img[^>]+src="(assets/icons/[^"]+)"', page)
    icon = hero.group(1) if hero else "assets/icons/_unknown.png"
    ns = re.search(r"<small>([a-z0-9_]+):([a-z0-9_]+)</small>", page)
    ns = ns.group(1) if ns else ""
    # 简介：取「这是什么」后的第一段
    desc = ""
    m = re.search(r"这是什么</h2>(.*?)</section>", page, re.S)
    if m:
        ps = re.findall(r"<p[^>]*>(.*?)</p>", m.group(1), re.S)
        for x in ps:
            t = re.sub(r"<[^>]+>", "", x).strip()
            if len(t) > 10:
                desc = t[:80]
                break
    cards.append(
        '<a class="modcard" href="%s">\n'
        '  <img src="%s" alt="">\n'
        '  <div class="t"><b>%s</b><small>%s</small>\n'
        '  <i>%s</i></div>\n'
        "</a>" % (p, icon, name, ns, desc.replace("<", ""))
    )

if cards:
    html = html.replace("</div></section>", "\n".join(cards) + "\n</div></section>", 1)
    io.open(MODS, "w", encoding="utf-8").write(html)

print("added cards:", len(cards))
for c in cards:
    print("  ", re.search(r'href="([^"]+)"', c).group(1))
