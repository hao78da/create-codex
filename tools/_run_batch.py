# -*- coding: utf-8 -*-
"""批量下载 _slugs.txt 里的全部 slug，内部直接调用 _dl_mods 的函数。

用法: python _run_batch.py [起始索引]
用途: 避免 shell 传参时混入 CR 字符，也便于续传。
"""
import io
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import _dl_mods as D  # noqa: E402

SLUGS = os.path.join(os.path.dirname(HERE), 'tools', 'data', '_slugs.txt')


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    slugs = [l.strip() for l in io.open(SLUGS, encoding='utf-8') if l.strip()]
    slugs = slugs[start:]
    print('待处理 %d 个（从 %d 开始）\n' % (len(slugs), start), flush=True)

    ok, skip, fail = [], [], []
    for i, slug in enumerate(slugs, 1):
        dst = os.path.join(D.RAW, slug + '.jar')
        if os.path.exists(dst) and os.path.getsize(dst) > 0:
            print('[%d/%d] %-36s 已有' % (i, len(slugs), slug), flush=True)
            ok.append(slug)
            continue

        picked = src = None
        p = D.pick_modrinth(slug)
        if p:
            picked, src = p, 'Modrinth'
        if not picked:
            p = D.pick_curseforge(slug)
            if p:
                picked, src = p, 'CurseForge'
            else:
                time.sleep(0.6)
        if not picked:
            print('[%d/%d] %-36s 两源均无 1.20.1 Forge' % (i, len(slugs), slug), flush=True)
            skip.append(slug)
            continue

        ver, url, fn, size = picked
        st, n = D.save(slug, url, dst, size)
        if st.startswith('ok') or st == 'exists':
            print('[%d/%d] %-36s %-10s %5.1fMB  %s' % (
                i, len(slugs), slug, src, (size or 0) / 1048576, st), flush=True)
            ok.append(slug)
        else:
            print('[%d/%d] %-36s %-10s FAIL %s' % (i, len(slugs), slug, src, st), flush=True)
            fail.append(slug)

    print('\n' + '=' * 62)
    print('成功 %d' % len(ok))
    if skip:
        print('跳过 %d: %s' % (len(skip), ', '.join(skip)))
    if fail:
        print('失败 %d: %s' % (len(fail), ', '.join(fail)))


if __name__ == '__main__':
    main()
