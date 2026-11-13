# -*- coding: utf-8 -*-
"""为占位的附属模组抓取官方简介，输出 _desc.json。

数据源：
  1) Modrinth  /v2/project/<slug>  -> title, description
  2) CurseForge cfwidget            -> title, summary
只取摘要文本，不下载 jar。
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PH = os.path.join(ROOT, '_ph.json')
OUT = os.path.join(ROOT, '_desc.json')

_PROXY = os.environ.get('MODS_PROXY', '').strip()
if _PROXY:
    _op = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': _PROXY, 'https': _PROXY}))
else:
    _op = urllib.request.build_opener()
_op.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120'),
                  ('Accept', 'application/json')]


def get(url, timeout=30):
    with _op.open(url, timeout=timeout) as r:
        return json.loads(r.read().decode())


def clean(txt, limit=160):
    """去掉 markdown / html，压成一句中文或英文摘要。"""
    if not txt:
        return ''
    t = re.sub(r'<[^>]+>', ' ', txt)
    t = re.sub(r'\[([^\]]*)\]\([^)]*\)', r'\1', t)
    t = re.sub(r'[*_`#>|]', '', t)
    t = re.sub(r'\s+', ' ', t).strip()
    # 截到第一个句号/句末
    m = re.search(r'[。！？.!?]\s', t)
    if m and m.start() < limit:
        t = t[:m.start() + 1]
    if len(t) > limit:
        t = t[:limit].rstrip(' ,;，；') + '…'
    return t


def from_modrinth(slug):
    try:
        d = get('https://api.modrinth.com/v2/project/%s' % slug)
        return {
            'src': 'Modrinth',
            'title': d.get('title', ''),
            'desc': clean(d.get('description', '')),
            'body': clean(d.get('description', ''), 400),
        }
    except Exception:
        return None


def from_cf(slug):
    for i in range(3):
        try:
            d = get('https://api.cfwidget.com/minecraft/mc-mods/%s' % slug, 40)
            return {
                'src': 'CurseForge',
                'title': d.get('title', ''),
                'desc': clean(d.get('summary', '')),
                'body': clean(d.get('summary', ''), 400),
            }
        except Exception as e:
            if getattr(e, 'code', '') == 404:
                return None
            if i == 2:
                return None
            time.sleep(2 + i * 2)


def main():
    ph = json.load(io.open(PH, encoding='utf-8'))
    print('待抓 %d 个\n' % len(ph), flush=True)

    out = {}
    ok = miss = 0
    for i, it in enumerate(ph, 1):
        slug = it['slug']
        r = from_modrinth(slug)
        if not r:
            r = from_cf(slug)
            time.sleep(0.8)
        if r and r['desc']:
            out[slug] = r
            ok += 1
            print('[%d/%d] %-38s %-10s %s' % (i, len(ph), slug[:36], r['src'], r['desc'][:56]), flush=True)
        else:
            miss += 1
            print('[%d/%d] %-38s 无简介' % (i, len(ph), slug[:36]), flush=True)
        time.sleep(0.2)

    json.dump(out, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n抓到 %d / %d，缺 %d' % (ok, len(ph), miss))
    print('输出:', OUT)


if __name__ == '__main__':
    main()
