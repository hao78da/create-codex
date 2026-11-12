# -*- coding: utf-8 -*-
"""用 mcmod 1.20.1 附属模组清单，在 Modrinth 搜索对应 slug，
再验证是否有 1.20.1 Forge 构建；没有则记录，后续走 CurseForge。

用法: python _match_mods.py [--limit N]
输入: ../_mcmod_todo.json
输出: _matched.json  —— [{mcmod_id, title, en, modrinth_slug, size, ok}]
"""
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODO = os.path.join(ROOT, '_mcmod_todo.json')
OUT = os.path.join(ROOT, '_matched.json')

_PROXY = os.environ.get('MODS_PROXY', '').strip()
if _PROXY:
    _op = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': _PROXY, 'https': _PROXY}))
else:
    _op = urllib.request.build_opener()
_op.addheaders = [('User-Agent', 'Mozilla/5.0 Chrome/120'), ('Accept', '*/*')]

FACET = urllib.parse.quote('[["categories:forge"]]')


def search(name):
    url = 'https://api.modrinth.com/v2/search?query=%s&limit=3&facets=%s' % (
        urllib.parse.quote(name), FACET)
    try:
        return json.loads(_op.open(url, timeout=30).read().decode()).get('hits', [])
    except Exception:
        return []


def has_1201(slug):
    try:
        vs = json.loads(_op.open(
            'https://api.modrinth.com/v2/project/%s/version' % slug, timeout=30).read().decode())
    except Exception:
        return None
    for v in vs:
        if '1.20.1' in v.get('game_versions', []) and (
                'forge' in v.get('loaders', []) or 'neoforge' in v.get('loaders', [])):
            f = next((x for x in v['files'] if x['filename'].endswith('.jar')), v['files'][0])
            return f.get('size', 0)
    return None


def main():
    limit = None
    if '--limit' in sys.argv:
        limit = int(sys.argv[sys.argv.index('--limit') + 1])

    todo = json.load(io.open(TODO, encoding='utf-8'))
    if limit:
        todo = todo[:limit]
    print('待匹配 %d 条\n' % len(todo), flush=True)

    results = []
    for i, it in enumerate(todo, 1):
        en = it['en']
        title = it['title']
        hits = search(en)
        # 挑最像的：标题归一化后互相包含
        best = None
        key = re.sub(r'[^a-z0-9]', '', en.lower())
        for h in hits:
            hk = re.sub(r'[^a-z0-9]', '', h['title'].lower())
            if key and (key in hk or hk in key):
                best = h
                break
        if not best and hits:
            best = hits[0]

        if not best:
            print('[%d/%d] %-36s 搜索无果' % (i, len(todo), en[:34]), flush=True)
            results.append({**it, 'slug': None, 'ok': False, 'reason': 'search'})
            continue

        slug = best['slug']
        size = has_1201(slug)
        if size is None:
            print('[%d/%d] %-36s -> %-28s 无1.20.1' % (i, len(todo), en[:34], slug[:26]), flush=True)
            results.append({**it, 'slug': slug, 'title': title, 'mr_title': best['title'],
                            'ok': False, 'reason': 'no_1201'})
        else:
            print('[%d/%d] %-36s -> %-28s %.1fMB' % (i, len(todo), en[:34], slug[:26], size / 1048576), flush=True)
            results.append({**it, 'slug': slug, 'mr_title': best['title'],
                            'size': size, 'ok': True, 'reason': ''})
        time.sleep(0.25)

    json.dump(results, io.open(OUT, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    okc = sum(1 for r in results if r['ok'])
    print('\n=== 可加 %d / %d ===' % (okc, len(results)))
    print('结果已存:', OUT)


if __name__ == '__main__':
    main()
