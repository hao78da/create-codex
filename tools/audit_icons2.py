# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
import io,re,glob,os
SITE = _os.path.join(ROOT, "docs")
out=[]
empty=[]; nohero=[]
for f in glob.glob(os.path.join(SITE,"addon-*.html")):
    s=io.open(f,encoding="utf-8").read()
    n=len(re.findall(r'<div class="ci">\s*</div>', s))
    if n: empty.append((os.path.basename(f),n))
for f in glob.glob(os.path.join(SITE,"tags","*.html")):
    s=io.open(f,encoding="utf-8").read()
    m=re.search(r'<div class="item-hero">([\s\S]{0,300}?)</div>', s)
    if not m or "<img" not in m.group(1): nohero.append(os.path.basename(f))
out.append("empty card icons: %s"%empty)
out.append("tag pages without hero img: %d %s"%(len(nohero), nohero[:6]))
io.open(os.path.join(DATA, "audit2.txt"),"w",encoding="utf-8").write("\n".join(out))
print("\n".join(out))
