# -*- coding: utf-8 -*-
"""批量下载附属模组 jar 到 work/mods_intake/。

用法: python _dl_mods.py <slug> [<slug> ...]
选择逻辑复刻 gen_addon_multi.py 的 fetch_jar():
  1.20.1 且 loaders 含 forge/neoforge，取第一个匹配版本的文件
"""
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "work", "mods_intake")
os.makedirs(RAW, exist_ok=True)

API = 'https://api.modrinth.com/v2/project/%s/version'


def pick(slug):
    vs = json.loads(urllib.request.urlopen(API % slug, timeout=40).read().decode())
    for v in vs:
        if '1.20.1' in v.get('game_versions', []) and (
                'forge' in v.get('loaders', []) or 'neoforge' in v.get('loaders', [])):
            f = next((x for x in v['files'] if x['filename'].endswith('.jar')),
                     v['files'][0])
            return v['version_number'], f['url'], f['filename'], f.get('size', 0)
    return None


def download(slug, url, dst, expect):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        print('  %-24s 已存在 %.1f MB' % (slug, os.path.getsize(dst) / 1048576), flush=True)
        return True
    req = urllib.request.Request(url, headers={'User-Agent': 'create-codex/1.0'})
    t0 = time.time()
    try:
        r = urllib.request.urlopen(req, timeout=90)
        n = 0
        tmp = dst + '.part'
        with open(tmp, 'wb') as f:
            while True:
                b = r.read(262144)
                if not b:
                    break
                f.write(b)
                n += len(b)
        if expect and n != expect:
            print('  %-24s 大小不符 %d != %d' % (slug, n, expect), flush=True)
            os.remove(tmp)
            return False
        os.replace(tmp, dst)
        print('  %-24s %.1f MB  %.0fs  (%d KB/s)' % (
            slug, n / 1048576, time.time() - t0, n / 1024 / max(1, time.time() - t0)), flush=True)
        return True
    except Exception as e:
        print('  %-24s FAIL %s %s' % (slug, type(e).__name__, str(e)[:60]), flush=True)
        for p in (dst + '.part',):
            if os.path.exists(p):
                os.remove(p)
        return False


def main():
    slugs = sys.argv[1:]
    if not slugs:
        print('用法: python _dl_mods.py <slug> [...]')
        return
    print('目标 %d 个模组\n' % len(slugs), flush=True)
    ok, skip, fail = [], [], []
    for i, slug in enumerate(slugs, 1):
        print('[%d/%d] %s' % (i, len(slugs), slug), flush=True)
        try:
            info = pick(slug)
        except Exception as e:
            print('  查询失败 %s' % e, flush=True)
            fail.append(slug)
            continue
        if not info:
            print('  无 1.20.1 forge 构建', flush=True)
            skip.append(slug)
            continue
        ver, url, fn, size = info
        print('  版本 %s  %.1f MB' % (ver, size / 1048576), flush=True)
        dst = os.path.join(RAW, slug + '.jar')
        if download(slug, url, dst, size):
            ok.append(slug)
        else:
            fail.append(slug)
        print('', flush=True)

    print('=' * 60)
    print('成功 %d: %s' % (len(ok), ', '.join(ok)))
    if skip:
        print('跳过 %d: %s' % (len(skip), ', '.join(skip)))
    if fail:
        print('失败 %d: %s' % (len(fail), ', '.join(fail)))


if __name__ == '__main__':
    main()
