# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""给附属模组配方里出现、但站内没有页面的原版物品批量建页。"""
import io
import json
import os
import re
import urllib.parse
import urllib.request

SITE = _os.path.join(ROOT, "docs")
ICONS = os.path.join(SITE, "assets", "icons")
TPL = io.open(os.path.join(SITE, "vanilla", "bamboo.html"), encoding="utf-8").read()
MC_ZH = json.load(io.open(os.path.join(DATA, "mc_zh.json"), encoding="utf-8"))
MISSING = json.load(io.open(os.path.join(DATA, "missing_vanilla.json"), encoding="utf-8"))


def title_case(slug):
    return "_".join(w.capitalize() for w in slug.split("_")) + ".png"


def zh(slug):
    for k in ("item.minecraft." + slug, "block.minecraft." + slug):
        if MC_ZH.get(k):
            return MC_ZH[k]
    return slug.replace("_", " ")


def local_icon(slug):
    for c in ("hh3d_%s.png" % slug, "minecraft_%s.png" % slug, "hh_%s.png" % slug):
        if os.path.exists(os.path.join(ICONS, c)):
            return c
    return None


# 索引：文件名 -> (category, subcategory)
idx = json.load(urllib.request.urlopen("https://honghemc.cn/assets.json", timeout=60))
files = []
for g in (idx if isinstance(idx, list) else [idx]):
    files += g.get("files") or []
by_name = {f.get("file"): f for f in files}


def fetch_icon(slug):
    have = local_icon(slug)
    if have:
        return have
    f = by_name.get(title_case(slug))
    if not f:
        return None
    q = lambda s: urllib.parse.quote(s, safe="")
    url = "https://honghemc.cn/images/%s/%s/%s" % (q(f["category"]), q(f["subcategory"]), q(f["file"]))
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        data = urllib.request.urlopen(req, timeout=40).read()
    except Exception:
        return None
    name = "vanilla_%s.png" % slug
    open(os.path.join(ICONS, name), "wb").write(data)
    return name


made = 0
no_icon = []
for iid in MISSING:
    slug = iid.split(":", 1)[1]
    out = os.path.join(SITE, "vanilla", slug + ".html")
    if os.path.exists(out):
        continue
    ic = fetch_icon(slug) or "_unknown.png"
    if ic == "_unknown.png":
        no_icon.append(slug)
    name = zh(slug)
    en = " ".join(w.capitalize() for w in slug.split("_"))
    desc = "Minecraft 原版物品。它没有 Create 的机制或配方，只作为附属模组配方的材料出现。"
    s = TPL
    s = re.sub(r"<title>.*?</title>", "<title>%s · 原版物品</title>" % name, s, flags=re.S)
    s = re.sub(r'(<img class="big" src=")[^"]*(")', r"\g<1>../assets/icons/%s\g<2>" % ic, s, count=1)
    s = re.sub(r"(<h1>).*?(</h1>)", r"\g<1>%s\g<2>" % name, s, count=1, flags=re.S)
    s = re.sub(r'(<div class="en">).*?(</div>)', r"\g<1>%s\g<2>" % en, s, count=1, flags=re.S)
    s = re.sub(r'(<span class="copyid"[^>]*>).*?(</span>)',
               r"\g<1>%s\g<2>" % iid, s, count=1, flags=re.S)
    s = re.sub(r'<section class="blk"><h2>属于这些标签</h2>.*?</section>',
               '<section class="blk"><h2>属于这些标签</h2><p>没有收录到它的标签。</p></section>',
               s, count=1, flags=re.S)
    io.open(out, "w", encoding="utf-8").write(s)
    made += 1

print("pages made:", made, "no icon:", len(no_icon))
print(no_icon[:20])
