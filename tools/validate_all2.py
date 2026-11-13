# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
import io,re,glob,os
SITE = _os.path.join(ROOT, "docs")
files=glob.glob(os.path.join(SITE,"*.html"))+glob.glob(os.path.join(SITE,"items","*.html"))+glob.glob(os.path.join(SITE,"tags","*.html"))+glob.glob(os.path.join(SITE,"vanilla","*.html"))+glob.glob(os.path.join(SITE,"mods","*.html"))
bad=[];refs=0
for p in files:
    base=os.path.dirname(p); t=io.open(p,encoding="utf-8").read()
    for m in re.finditer(r'(?:href|src)="([^"]+)"', t):
        u=m.group(1)
        if u.startswith(("http","#","data:","mailto:")): continue
        u=u.split("#")[0].split("?")[0]
        if not u: continue
        refs+=1
        if not os.path.exists(os.path.normpath(os.path.join(base,u))): bad.append((os.path.basename(p),u))
print("pages",len(files),"refs",refs,"broken",len(bad))
for b in bad[:8]: print(b)
