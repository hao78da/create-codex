# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""重建整个标签体系：
   - Create 本体标签（仓库 tags/）
   - 全部原版物品标签（vanilla_tags_all.json）
   - 附属模组里的 Forge / c 标签（jar 内 tags 定义 + 配方引用）
每页写：成员、用到它的 Create 配方、哪些附属模组物品用到它。
"""
import glob
import io
import json
import os
import re
import zipfile

SITE = ROOT
TAGS = os.path.join(SITE, "tags")
ICONS = os.path.join(SITE, "assets", "icons")
OUT = _os.path.join(ROOT, 'tools', 'data')
REPO = r"D:\frontend\_raw\create\Create-mc1.20.1-dev\src"
JARS = _os.path.join(WORK, 'mods_intake')

DATA = json.load(io.open(os.path.join(OUT, "data.json"), encoding="utf-8"))
ITEMS = DATA["items"]
MC_ZH = json.load(io.open(os.path.join(OUT, "mc_zh.json"), encoding="utf-8"))

# 旧标签页里的中文名（重建前先抓）
OLD_ZH = {}
old_index = os.path.join(SITE, "tags.html")
if os.path.exists(old_index):
    h = io.open(old_index, encoding="utf-8").read()
    for m in re.finditer(r'<b>([^<]+)</b><small>([^<]+)</small>', h):
        OLD_ZH[m.group(2)] = m.group(1).strip()

SLUG = lambda t: t.replace(":", "_").replace("/", "_")


def zh_of(tag):
    if tag in OLD_ZH and OLD_ZH[tag] and not OLD_ZH[tag].startswith(("#", "forge", "minecraft", "create")):
        return OLD_ZH[tag]
    tail = tag.split(":")[-1].split("/")[-1]
    for k in ("item.minecraft." + tail, "block.minecraft." + tail):
        if MC_ZH.get(k):
            return MC_ZH[k]
    return tail.replace("_", " ")


# ---------- 1. 成员 ----------
members = {}

# 原版
vt = json.load(io.open(os.path.join(OUT, "vanilla_tags_all.json"), encoding="utf-8"))
for t, vals in vt.items():
    members.setdefault(t, [])
    members[t] += [v for v in vals if isinstance(v, str)]

# Create 本体
for p in glob.glob(os.path.join(REPO, "**", "data", "create", "tags", "**", "*.json"), recursive=True):
    rel = p.split("data" + os.sep + "create" + os.sep + "tags" + os.sep)[-1]
    kind, stem = rel.split(os.sep)[0], os.path.basename(p)[:-5]
    if kind not in ("items", "blocks"):
        continue
    try:
        d = json.load(io.open(p, encoding="utf-8"))
    except Exception:
        continue
    tag = "create:" + stem
    members.setdefault(tag, [])
    members[tag] += [v for v in d.get("values", []) if isinstance(v, str)]

# 附属 jar 里的标签定义（forge / c / 各模组自己的）
for jar in glob.glob(os.path.join(JARS, "*.jar")):
    try:
        z = zipfile.ZipFile(jar)
    except Exception:
        continue
    for n in z.namelist():
        m = re.match(r"data/([a-z0-9_]+)/tags/(items|blocks)/(.+)\.json$", n)
        if not m:
            continue
        ns, stem = m.group(1), m.group(3)
        if ns in ("minecraft", "create"):
            continue
        try:
            d = json.loads(z.read(n).decode("utf-8-sig"))
        except Exception:
            continue
        tag = "%s:%s" % (ns, stem)
        members.setdefault(tag, [])
        members[tag] += [v for v in d.get("values", []) if isinstance(v, str)]


def resolve(tag, seen=None):
    seen = seen or set()
    if tag in seen:
        return []
    seen.add(tag)
    out = []
    for v in members.get(tag, []):
        if v.startswith("#"):
            out += resolve(v[1:], seen)
        else:
            out.append(v)
    # 去重保序
    r = []
    for x in out:
        if x not in r:
            r.append(x)
    return r


# ---------- 1.5 被引用但没定义的标签（原版常用 tag / Forge 通用 tag）----------
REF_EXTRA = set(OLD_ZH)
for it in ITEMS.values():
    for rec in it.get("recipes") or []:
        for st in (rec.get("ingredients") or []):
            if isinstance(st, dict) and st.get("tag"):
                REF_EXTRA.add(st["tag"])
for pth in sorted(glob.glob(os.path.join(SITE, "addon-*.html"))):
    h = io.open(pth, encoding="utf-8").read()
    REF_EXTRA |= set(re.findall(r'#((?:[a-z0-9_]+):[a-z0-9_/]+)', h))
for t in REF_EXTRA:
    members.setdefault(t, [])

# 成员里嵌套引用的标签也要有页面
NESTED = set()
for _t, _vs in list(members.items()):
    for _v in _vs:
        if isinstance(_v, str) and _v.startswith("#"):
            NESTED.add(_v[1:])
for _t in NESTED:
    members.setdefault(_t, [])

# ---------- 2. 使用情况 ----------
use_items = {}      # tag -> [(item id)]
for iid, it in ITEMS.items():
    for rec in it.get("recipes") or []:
        for st in (rec.get("ingredients") or []):
            if isinstance(st, dict) and st.get("tag"):
                use_items.setdefault(st["tag"], set()).add(iid)

use_addons = {}     # tag -> [(page, card name)]
for p in sorted(glob.glob(os.path.join(SITE, "addon-*.html"))):
    page = os.path.basename(p)
    h = io.open(p, encoding="utf-8").read()
    for card in re.finditer(r'<div class="card" id="[^"]*">.*?(?=<div class="card"|\Z)', h, re.S):
        block = card.group(0)
        nm = re.search(r"<b>([^<]+)</b>", block)
        card_name = nm.group(1) if nm else ""
        HREF_TAG = {}
        for _sl in re.findall(r'tags/([a-z0-9_]+)\.html', block):
            HREF_TAG[_sl] = True
        ids = set(re.findall(r'#((?:forge|minecraft|create|c|tconstruct|thermal|immersiveengineering|[a-z0-9_]+):[a-z0-9_/]+)', block))
        for _sl in HREF_TAG:
            ids.add(_sl)
        for t in ids:
            use_addons.setdefault(t, []).append((page, card_name))


# 页面级兜底：整页出现的标签链接都记一笔（卡片解析失败时也能列出）
PAGE_SCAN = True
for pth in sorted(glob.glob(os.path.join(SITE, "addon-*.html"))):
    page = os.path.basename(pth)
    h = io.open(pth, encoding="utf-8").read()
    for slug in set(re.findall(r'tags/([a-z0-9_]+)\.html', h)):
        seen = [x for x in use_addons.get(slug, []) if x[0] == page]
        if not seen:
            use_addons.setdefault(slug, []).append((page, ""))

# ---------- 3. 图标 ----------
def icon_of(iid):
    ns, short = iid.split(":", 1)
    cands = []
    if ns == "create":
        cands += ["3d_create_%s.png" % short, "create_%s.png" % short]
    else:
        cands += ["hh3d_%s.png" % short, "minecraft_%s.png" % short, "hh_%s.png" % short]
    for c in cands:
        if os.path.exists(os.path.join(ICONS, c)):
            return c
    return None


TAG_FALLBACK = {
    "minecraft:axes": "minecraft_wooden_axe.png",
    "minecraft:pickaxes": "minecraft_wooden_pickaxe.png",
    "minecraft:shovels": "minecraft_wooden_shovel.png",
    "minecraft:hoes": "minecraft_wooden_hoe.png",
    "minecraft:swords": "minecraft_wooden_sword.png",
    "minecraft:planks": "minecraft_oak_planks.png",
    "minecraft:logs": "minecraft_oak_log.png",
    "minecraft:coals": "minecraft_coal.png",
    "minecraft:glass": "hh3d_glass.png",
    "minecraft:wool": "minecraft_white_wool.png",
    "create:amethyst": "minecraft_amethyst_block.png",
    "create:coral": "minecraft_brain_coral.png",
    "create:corals": "minecraft_brain_coral.png",
    "create:allurite": "create_allurite.png",
    "minecraft:buttons": "minecraft_oak_button.png",
    "minecraft:wooden_buttons": "minecraft_oak_button.png",
    "minecraft:stone_buttons": "minecraft_stone_button.png",
    "forge:plates/iron": "minecraft_iron_ingot.png",
    "forge:plates/gold": "minecraft_gold_ingot.png",
    "forge:plates/brass": "create_brass_sheet.png",
    "forge:plates/copper": "create_copper_sheet.png",
    "forge:ingots/brass": "create_brass_ingot.png",
    "forge:ingots/copper": "minecraft_copper_ingot.png",
    "forge:ingots/iron": "minecraft_iron_ingot.png",
    "forge:ingots/gold": "minecraft_gold_ingot.png",
    "forge:dusts/redstone": "minecraft_redstone.png",
    "forge:nuggets/iron": "minecraft_iron_nugget.png",
}
GEAR = "tag_generic.png" if os.path.exists(os.path.join(ICONS, "tag_generic.png")) else "_unknown.png"


_ALL_ICONS = [f for f in os.listdir(ICONS) if f.endswith(".png")]


def _by_tail(tag):
    tail = tag.split(":")[-1].split("/")[-1]
    cands = [tail, tail[:-1] if tail.endswith("s") else tail]
    for base in cands:
        for pre in ("3d_create_", "create_", "hh3d_", "minecraft_", "hh_"):
            f = pre + base + ".png"
            if os.path.exists(os.path.join(ICONS, f)):
                return f
    # 模糊：文件名里含这个单词（boats → oak_boat）
    for base in cands:
        hit = [f for f in _ALL_ICONS if base in f and not f.startswith(("_", "hh_"))]
        if hit:
            hit.sort(key=len)
            return hit[0]
    return None


def tag_icon(tag, mem):
    TAIL_CANDS = True
    if TAG_FALLBACK.get(tag) and os.path.exists(os.path.join(ICONS, TAG_FALLBACK[tag])):
        return TAG_FALLBACK[tag]
    for m in mem:
        ic = icon_of(m)
        if ic:
            return ic
    by_tail = _by_tail(tag)
    if by_tail:
        return by_tail
    return GEAR


# ---------- 4. 写页面 ----------
if os.path.isdir(TAGS):
    for f in glob.glob(os.path.join(TAGS, "*.html")):
        os.remove(f)
os.makedirs(TAGS, exist_ok=True)

TPL = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>#%s · 标签</title><link rel="stylesheet" href="../assets/style.css"></head><body>
<header class="top"><div class="wrap"><a class="logo" href="../index.html"><span class="gear"></span>CREATE CODEX<small>机械动力图鉴</small></a>
<nav><a href="../tags.html">标签</a><a href="../index.html">源码</a></nav></div></header>
<main class="wrap">
<nav class="crumb"><a href="../index.html">首页</a> / <a href="../tags.html">标签</a> / %s</nav>
<section class="item-hero"><img class="big" src="../assets/icons/%s" alt="">
<div><h1>#%s</h1><div class="idline"><span class="copyid" title="点击复制">%s</span></div>
<span class="badge">标签</span></div></section>
%s
%s
%s
</main>
<footer class="wrap foot">数据与图标来自 Create 与 Minecraft 资源，仅用于学习与教学；Minecraft 版权归 Mojang 所有。</footer>
</body></html>"""


def chips(ids, limit=64):
    out = []
    for iid in ids[:limit]:
        short = iid.split(":", 1)[1]
        href = None
        if iid.startswith("create:") and os.path.exists(os.path.join(SITE, "items", short + ".html")):
            href = "../items/%s.html" % short
        elif os.path.exists(os.path.join(SITE, "vanilla", short + ".html")):
            href = "../vanilla/%s.html" % short
        nm = (ITEMS.get(iid) or {}).get("n") or zh_of(iid)
        ic = icon_of(iid)
        label = ('<img src="../assets/icons/%s" alt="">' % ic if ic else "") + "<span>%s</span>" % nm
        if href:
            out.append('<a class="chip" href="%s">%s</a>' % (href, label))
        else:
            out.append('<span class="chip">%s</span>' % label)
    if len(ids) > limit:
        out.append('<span class="chip">…还有 %d 个</span>' % (len(ids) - limit))
    return '<div class="chiprow">%s</div>' % "".join(out)


made = 0
for tag in sorted(members):
    mem = resolve(tag)
    ui = sorted(use_items.get(tag, []))
    ua = use_addons.get(tag) or use_addons.get(SLUG(tag)) or []
    name = zh_of(tag)
    sec = []
    if mem:
        sec.append('<section class="blk"><h2>成员<span class="cnt">%d</span></h2>%s</section>' % (len(mem), chips(mem)))
    else:
        sec.append('<section class="blk"><h2>成员</h2><p>这个标签的成员由 Forge 在运行时注册，jar 里没有写死。</p></section>')
    if ui:
        sec.append('<section class="blk"><h2>用到它的 Create 配方<span class="cnt">%d</span></h2>%s</section>'
                   % (len(ui), chips(ui)))
    else:
        sec.append('<section class="blk"><h2>用到它的 Create 配方</h2><p>本站收录的 Create 配方里没有用到它。</p></section>')
    if ua:
        lis = []
        seen = set()
        for page, cname in ua:
            key = (page, cname)
            if key in seen:
                continue
            seen.add(key)
            lis.append('<li><a href="../%s">%s</a> · %s</li>' % (page, page.replace("addon-", "").replace(".html", ""), cname))
        sec.append('<section class="blk"><h2>附属模组里的使用<span class="cnt">%d</span></h2><ul class="plainlist">%s</ul></section>'
                   % (len(lis), "".join(lis)))
    html = TPL % (name, name, tag_icon(tag, mem), name, tag, "\n".join(sec), "", "")
    io.open(os.path.join(TAGS, SLUG(tag) + ".html"), "w", encoding="utf-8").write(html)
    made += 1

print("tag pages:", made)

# ---------- 5. 索引 ----------
groups = {"create": [], "minecraft": [], "other": []}
for tag in sorted(members, key=lambda t: (-len(resolve(t)), t)):
    ns = tag.split(":")[0]
    g = "create" if ns == "create" else ("minecraft" if ns == "minecraft" else "other")
    groups[g].append(tag)

cards = []
for g, title in (("create", "Create 本体标签"), ("minecraft", "原版物品标签"), ("other", "附属模组 / Forge 标签")):
    ts = groups[g]
    if not ts:
        continue
    cards.append('<h2 class="sec">%s<span class="cnt">%d</span></h2><div class="grid-tags">' % (title, len(ts)))
    for tag in ts:
        mem = resolve(tag)
        name = zh_of(tag)
        cards.append('<a class="tagcard" href="tags/%s.html"><img src="assets/icons/%s" alt="">'
                     '<div class="t"><b>%s</b><small>%s</small></div></a>'
                     % (SLUG(tag), tag_icon(tag, mem), name, tag))
    cards.append("</div>")

idx = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>标签索引 · Create Codex</title><link rel="stylesheet" href="assets/style.css"><style>.tagcard img{width:46px;height:46px;object-fit:contain;flex:0 0 46px}.tagcard{align-items:center}</style></head><body>
<header class="top"><div class="wrap"><a class="logo" href="index.html"><span class="gear"></span>CREATE CODEX<small>机械动力图鉴</small></a>
<nav><a href="tags.html">标签</a><a href="index.html">源码</a></nav></div></header>
<main class="wrap">
<div class="hero"><h1>标签索引</h1><div class="sub">TAGS</div>
<p>共 <b>%d</b> 个标签：Create 本体、原版物品、以及附属模组用到的 Forge 标签。点开看成员和用处。</p></div>
%s
</main>
<footer class="wrap foot">数据与图标来自 Create 与 Minecraft 资源，仅用于学习与教学；Minecraft 版权归 Mojang 所有。</footer>
</body></html>""" % (made, "\n".join(cards))
io.open(os.path.join(SITE, "tags.html"), "w", encoding="utf-8").write(idx)
print("index written")
