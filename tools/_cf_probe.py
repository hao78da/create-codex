# -*- coding: utf-8 -*-
"""爬 mcmod class 页取 CurseForge slug，再用 cfwidget 验证 1.20.1 Forge。

用法: python _cf_probe.py
输入: ../_cf_todo.json
输出: _cf_result.json   [{id,title,en,cf_slug,ok,size,file}]
"""
import base64
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TODO = os.path.join(ROOT, 'tools', 'data', '_cf_todo.json')
OUT = os.path.join(ROOT, 'tools', 'data', '_cf_result.json')

_PROXY = os.environ.get('MODS_PROXY', '').strip()
if _PROXY:
    _op = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': _PROXY, 'https': _PROXY}))
else:
    _op = urllib.request.build_opener()
_op.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120'),
                  ('Accept', 'text/html,application/json')]


def fetch(url, timeout=40):
    with _op.open(url, timeout=timeout) as r:
        return r.read()


def cf_slug_from_class(cid):
    """从 mcmod class 页取 curseforge slug"""
    try:
        html = fetch('https://www.mcmod.cn/class/%s.html' % cid).decode('utf-8', 'replace')
    except Exception:
        return None
    for b64 in re.findall(r'link\.mcmod\.cn/target/([A-Za-z0-9+/=]+)', html):
        try:
            u = base64.b64decode(b64 + '==').decode('utf-8', 'replace')
        except Exception:
            continue
        m = re.search(r'curseforge\.com/minecraft/(?:[a-z\-]+/)?(?:mc-mods|mods)/([a-z0-9\-_]+)',
                      u, re.I)
        if m:
            return m.group(1)
    # 也看正文里的直链
    m = re.search(r'curseforge\.com/minecraft/mc-mods/([a-z0-9\-_]+)', html, re.I)
    return m.group(1) if m else None


def cf_pick(slug, retries=3):
    """cfwidget 查 1.20.1 forge 文件"""
    for i in range(retries):
        try:
            raw = fetch('https://api.cfwidget.com/minecraft/mc-mods/%s' % slug, 40)
            d = json.loads(raw.decode())
            break
        except Exception as e:
            if getattr(e, 'code', '') == 404:
                return None
            if i == retries - 1:
                return None
            time.sleep(2 + i * 2)
    files = d.get('files') or []
    hit = [f for f in files
           if '1.20.1' in (f.get('versions') or [])
           and any(x in (f.get('versions') or []) for x in ('Forge', 'NeoForge'))]
    if not hit:
        return None
    hit.sort(key=lambda f: f.get('uploaded_at') or '', reverse=True)
    f = hit[0]
    fid = f['id']
    return {
        'file_id': fid,
        'filename': f['display'],
        'size': f.get('filesize') or 0,
        'url': 'https://edge.forgecdn.net/files/%d/%03d/%s' % (fid // 1000, fid % 1000, f['display']),
    }


def main():
    todo = json.load(io.open(TODO, encoding='utf-8'))
    print('待探测 %d 条\n' % len(todo), flush=True)

    out = []
    for i, it in enumerate(todo, 1):
        cid, title, en = it['id'], it['title'], it['en']
        slug = cf_slug_from_class(cid)
        if not slug:
            print('[%d/%d] %-34s 无 CF 链接' % (i, len(todo), en[:32]), flush=True)
            out.append({**it, 'cf_slug': None, 'ok': False, 'reason': 'no_cf'})
            time.sleep(0.8)
            continue

        info = cf_pick(slug)
        if not info:
            print('[%d/%d] %-34s -> %-28s 无1.20.1' % (i, len(todo), en[:32], slug[:26]), flush=True)
            out.append({**it, 'cf_slug': slug, 'ok': False, 'reason': 'no_1201'})
        else:
            print('[%d/%d] %-34s -> %-28s %5.1fMB' % (
                i, len(todo), en[:32], slug[:26], info['size'] / 1048576), flush=True)
            out.append({**it, 'cf_slug': slug, 'ok': True, **info})
        time.sleep(1.2)

    json.dump(out, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    okc = sum(1 for x in out if x['ok'])
    print('\n=== 可加 %d / %d ===' % (okc, len(out)))
    print('总计 %.1f MB' % (sum(x.get('size', 0) for x in out if x['ok']) / 1048576))
    print('结果:', OUT)


if __name__ == '__main__':
    main()
