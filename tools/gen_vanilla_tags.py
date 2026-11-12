# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
"""生成 vanilla.html：本站用到的原版物品 -> 它们所属的标签。

数据来源：
- out/data.json 的 vanilla（273 个本站配方引用的原版物品）
- out/vanilla_tags_all.json（misode/mcmeta 1.20.1 原版 item tags）
- 模组仓库 data/*/tags/{items,blocks}（Create/Forge 的标签定义）

输出：D:\frontend\create-codex\vanilla.html
"""
import io
import json
import os
import re
import glob

RAW = _os.path.join(WORK, 'raw')
OUT = os.path.join(RAW, "out")
SITE = ROOT
TAG_DIR = os.path.join(RAW, "create", "Create-mc1.20.1-dev", "src", "generated", "resources", "data")


def load_tags():
    tags = {}
    # 仓库里的标签
    for f in glob.glob(os.path.join(TAG_DIR, "*", "tags", "*", "**", "*.json"), recursive=True):
        rel = os.path.relpath(f, TAG_DIR).replace(os.sep, "/").split("/")
        if len(rel) < 4 or rel[1] != "tags":
            continue
        kind = rel[2]
        if kind not in ("items", "blocks"):
            continue
        key = rel[0] + ":" + "/".join(rel[3:])[:-5]
        try:
            tags[key] = json.load(io.open(f, encoding="utf-8")).get("values", [])
        except Exception:
            pass
    # 原版标签（不覆盖已有）
    vp = os.path.join(OUT, "vanilla_tags_all.json")
    if os.path.exists(vp):
        for k, v in json.load(io.open(vp, encoding="utf-8")).items():
            tags.setdefault(k, v)
    elif os.path.exists(os.path.join(OUT, "vanilla_tags.json")):
        for k, v in json.load(io.open(os.path.join(OUT, "vanilla_tags.json"), encoding="utf-8")).items():
            tags.setdefault(k, v)
    return tags


def main():
    data = json.load(io.open(os.path.join(OUT, "data.json"), encoding="utf-8"))
    vanilla = data["vanilla"]
    tags = load_tags()

    # 标签 -> 直接成员（解析一层嵌套）
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

    # 物品 -> 标签
    item_tags = {}
    for t, s in members.items():
        for it in s:
            if it in vanilla:
                item_tags.setdefault(it, []).append(t)

    # 使用次数：在 Create 配方的 ingredients 里出现多少次
    use = {}
    for iid, it in data["items"].items():
        for r in it.get("recipes") or []:
            for st in (r.get("ingredients") or []):
                if isinstance(st, dict) and st.get("id") in vanilla:
                    use[st["id"]] = use.get(st["id"], 0) + 1

    # 标签页文件名，用于链接
    labels = {}
    tp = os.path.join(SITE, "tags.html")
    if os.path.exists(tp):
        h = io.open(tp, encoding="utf-8").read()
        for m in re.finditer(r'<b>([^<]+)</b><small>([^<]+)</small>', h):
            labels[m.group(2)] = m.group(1)

    page_files = {}
    for f in glob.glob(os.path.join(SITE, "tags", "*.html")):
        page_files[os.path.basename(f)[:-5]] = True

    def tag_href(t):
        fn = t.replace(":", "_").replace("/", "_")
        return ("tags/%s.html" % fn) if fn in page_files else None

    rows = []
    for iid in sorted(vanilla, key=lambda x: (-use.get(x, 0), vanilla[x].get("n", x))):
        it = vanilla[iid]
        ts = sorted(item_tags.get(iid, []))
        chips = []
        for t in ts:
            href = tag_href(t)
            label = labels.get(t) or t.split(":")[-1]
            if href:
                chips.append('<a class="tg" href="%s">#%s</a>' % (href, label))
            else:
                chips.append('<span class="tg off">#%s</span>' % label)
        if not chips:
            chips = ['<span class="tg off">无</span>']
        _slug = iid.split(":")[1]
        _hh = "hh3d_%s.png" % _slug
        _icon = _hh if os.path.exists(os.path.join(SITE, "assets", "icons", _hh)) else (it.get("icon") or "_unknown.png")
        rows.append(
            '<a class="vrow" href="vanilla/%s.html" data-k="%s %s">'
            '<img src="assets/icons/%s" alt="" loading="lazy">'
            '<div class="vt"><b>%s</b><small>%s</small></div>'
            '<div class="vchips">%s</div>'
            '<div class="vuse">%d 条配方</div>'
            '</a>' % (
                _slug, it.get("n", ""), iid, _icon,
                it.get("n", iid), iid, "".join(chips), use.get(iid, 0)))

    html = """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>原版物品的标签 — Create Codex</title>
<link rel="preload" href="assets/fonts/Minecraft.ttf" as="font" crossorigin>
<link rel="stylesheet" href="assets/style.css">
<link rel="icon" href="assets/icons/create_logo.png">
<style>
.vrow{display:flex;gap:12px;align-items:center;background:var(--panel);border:1px solid var(--line);
  text-decoration:none;color:inherit;
  border-radius:10px;padding:8px 12px;margin-bottom:8px}
.vrow:hover{border-color:var(--brass)}
.vrow img{width:28px;height:28px;flex:0 0 auto;image-rendering:pixelated;object-fit:contain}
.vt{flex:0 0 190px;min-width:0}
.vt b{display:block;font-size:13.5px;color:#f0dfba;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vt small{display:block;color:var(--muted);font-size:11px;font-family:ui-monospace,Consolas,monospace;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.vchips{flex:1;display:flex;gap:5px;flex-wrap:wrap;min-width:0}
.tg{font-size:11px;color:#cbb894;background:#17130d;border:1px solid var(--line);border-radius:5px;
  padding:1px 6px;text-decoration:none;font-family:ui-monospace,Consolas,monospace}
.tg:hover{color:#fff;border-color:var(--brass)}
.tg.off{color:#6d6152}
.vuse{flex:0 0 78px;text-align:right;color:var(--muted);font-size:11.5px}
.vsearch{margin:18px 0 16px}
.vsearch input{width:100%%;max-width:420px;background:var(--panel);border:1px solid var(--line);
  border-radius:10px;padding:10px 14px;color:var(--text);font-size:14px;outline:none}
.vsearch input:focus{border-color:var(--brass)}
.vcount{color:var(--muted);font-size:12px;margin-left:10px}
</style></head><body>
<header class="top"><div class="wrap">
<a class="logo" href="index.html"><span class="gear"></span><span>CREATE CODEX<small>机械动力图鉴</small></span></a>
<nav><a href="catalog.html">全部物品</a><a href="tags.html">标签</a><a href="mods.html">模组</a><a href="vanilla.html" style="color:var(--brass2)">原版</a></nav>
</div></header>
<main class="wrap">
<div class="hero"><h1>原版物品的标签<span>VANILLA</span></h1>
<p>本站配方用到的 <b>%d</b> 个原版物品，各自属于哪些标签。标签名可点，进入标签详情。</p></div>
<div class="vsearch"><input id="q" type="search" placeholder="搜索物品名 / ID / 标签…" autocomplete="off"><span class="vcount" id="cnt">%d 个物品</span></div>
<div id="list">%s</div>
</main>
<footer class="foot"><div class="wrap"><p>数据：Minecraft 原版标签来自 <a href="https://github.com/misode/mcmeta">misode/mcmeta</a>（1.20.1）与 Create 模组自带的 Forge 标签定义；物品中文名来自模组语言文件。</p></div></footer>
<script>
(function(){var q=document.getElementById('q'),cnt=document.getElementById('cnt');
var rows=[].slice.call(document.querySelectorAll('.vrow'));
q.addEventListener('input',function(){var s=q.value.trim().toLowerCase(),n=0;
rows.forEach(function(r){var ok=!s||r.dataset.k.toLowerCase().indexOf(s)>-1;r.style.display=ok?'':'none';if(ok)n++;});
cnt.textContent=n+' 个物品';});})();
</script>
</body></html>""" % (len(vanilla), len(vanilla), "\n".join(rows))

    io.open(os.path.join(SITE, "vanilla.html"), "w", encoding="utf-8").write(html)
    print("vanilla.html:", len(rows), "items,", sum(1 for i in vanilla if item_tags.get(i)), "with tags")


if __name__ == "__main__":
    main()
