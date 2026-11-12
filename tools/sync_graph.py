# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""从 addon-*.html 自动同步 index.html 的 MODS 数组与 mods.html 卡片。"""
import io
import math
import os
import re
import html as _html

SITE = ROOT
IDX = os.path.join(SITE, "index.html")

pages = sorted(
    p for p in os.listdir(SITE)
    if p.startswith("addon-") and p.endswith(".html")
)

s = io.open(IDX, encoding="utf-8").read()
start = s.index("var MODS = [")
end = s.index("];", start)
body = s[start:end]

entries = re.findall(r"\{\s*id:'[^']+'.*?\},\s*", body, re.S)
have = {}
for e in entries:
    m = re.search(r"id:'([^']+)'", e)
    if m:
        have[m.group(1)] = e

# 每个页面 -> 节点信息
nodes = []
center = None
for eid, e in have.items():
    href = re.search(r"href:'([^']+)'", e)
    if href and href.group(1).startswith("catalog"):
        center = e
        continue
    nodes.append(e)

existing_hrefs = set(re.findall(r"href:'(addon-[^']+)'", "".join(nodes)))

for p in pages:
    if p in existing_hrefs:
        continue
    html = io.open(os.path.join(SITE, p), encoding="utf-8").read()
    h1 = re.search(r"<h1[^>]*>(.*?)</h1>", html, re.S)
    name = _html.unescape(re.sub(r"<[^>]+>", "", h1.group(1))).strip() if h1 else p
    hero = re.search(r'<img[^>]+src="(assets/icons/[^"]+)"', html)
    icon = hero.group(1) if hero else "assets/icons/_unknown.png"
    nid = p[len("addon-"):-len(".html")]
    nodes.append(
        "    { id:'%s', name:'%s', sub:'%s', level:1, parent:'create', ang:0, rf:1,\n"
        "      icon:'%s', href:'%s', tip:'', color:'#d9c7a8' }," % (
            nid, name.replace("'", ""), nid.upper(), icon, p)
    )
    existing_hrefs.add(p)

step = 2 * math.pi / len(nodes)
start_ang = -math.pi / 2 + 0.16
out = ["var MODS = ["]
if center:
    out.append(center.rstrip())
for i, e in enumerate(nodes):
    e = re.sub(r"ang:-?[\d.]+", "ang:%s" % round(start_ang + i * step, 3), e, 1)
    e = re.sub(r"rf:[\d.]+", "rf:%s" % (1.00 if i % 2 == 0 else 0.84), e, 1)
    out.append(e.rstrip())
new_body = "\n".join(out) + "\n"
s = s[:start] + new_body + s[end:]
io.open(IDX, "w", encoding="utf-8").write(s)
print("nodes:", len(nodes) + (1 if center else 0))
