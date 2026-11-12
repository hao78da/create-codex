# -*- coding: utf-8 -*-
"""按 _cf_ok.json 从 CurseForge CDN 下载 jar。

用法: python _cf_dl.py
"""
import io
import json
import os
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CF_OK = os.path.join(ROOT, '_cf_ok.json')
RAW = os.path.join(ROOT, 'work', 'mods_intake')
os.makedirs(RAW, exist_ok=True)

_PROXY = os.environ.get('MODS_PROXY', '').strip()
if _PROXY:
    _op = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': _PROXY, 'https': _PROXY}))
else:
    _op = urllib.request.build_opener()
_op.addheaders = [('User-Agent', 'Mozilla/5.0 Chrome/120')]


def main():
    items = json.load(io.open(CF_OK, encoding='utf-8'))
    print('待下载 %d 个\n' % len(items), flush=True)
    ok, fail = [], []
    for i, it in enumerate(items, 1):
        slug = it['cf_slug']
        dst = os.path.join(RAW, slug + '.jar')
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            print('[%d/%d] %-34s 已有' % (i, len(items), slug), flush=True)
            ok.append(slug)
            continue
        url = it['url']
        expect = it.get('size') or 0
        t0 = time.time()
        r = None
        try:
            r = _op.open(url, timeout=180)
            n = 0
            tmp = dst + '.part'
            with open(tmp, 'wb') as fh:
                while True:
                    b = r.read(262144)
                    if not b:
                        break
                    fh.write(b)
                    n += len(b)
            if expect and abs(n - expect) > 2048:
                os.remove(tmp)
                print('[%d/%d] %-34s 大小不符 %d!=%d' % (i, len(items), slug, n, expect), flush=True)
                fail.append(slug)
                continue
            os.replace(tmp, dst)
            dt = max(time.time() - t0, 0.001)
            print('[%d/%d] %-34s %.1fMB  %.0fs  %dKB/s' % (
                i, len(items), slug, n / 1048576, dt, n / 1024 / dt), flush=True)
            ok.append(slug)
        except Exception as e:
            print('[%d/%d] %-34s FAIL %s %s' % (i, len(items), slug, type(e).__name__,
                                                str(e)[:40]), flush=True)
            fail.append(slug)
            p = dst + '.part'
            if os.path.exists(p):
                os.remove(p)
        finally:
            if r is not None:
                try:
                    r.close()
                except Exception:
                    pass

    print('\n' + '=' * 62)
    print('成功 %d' % len(ok))
    if fail:
        print('失败 %d: %s' % (len(fail), ', '.join(fail)))


if __name__ == '__main__':
    main()
