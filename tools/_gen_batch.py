# -*- coding: utf-8 -*-
"""按 _todo.txt 逐个生成附属页，直接复用 gen_addon_multi 的 build()。

用法: python _gen_batch.py [起始索引]
避免 shell 传参混入 CR，也便于失败续跑。
"""
import io
import os
import sys
import traceback

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
os.chdir(HERE)

TODO = os.path.join(HERE, '_todo.txt')


def main():
    start = int(sys.argv[1]) if len(sys.argv) > 1 else 0
    slugs = [l.strip() for l in io.open(TODO, encoding='utf-8') if l.strip()][start:]

    import gen_addon_multi as G

    mods = {m['slug']: m for m in G.MODS}
    print('待生成 %d 个\n' % len(slugs), flush=True)

    ok, fail = 0, []
    for i, slug in enumerate(slugs, 1):
        spec = mods.get(slug)
        if not spec:
            print('[%d/%d] %-38s 无配置' % (i, len(slugs), slug), flush=True)
            fail.append(slug)
            continue
        try:
            G.build(spec)
            ok += 1
        except Exception as e:
            print('[%d/%d] %-38s ERR %s %s' % (i, len(slugs), slug, type(e).__name__, str(e)[:50]),
                  flush=True)
            fail.append(slug)

    # 一次性跑后处理
    print('\n后处理…', flush=True)
    try:
        import addon_post as AP
        AP.postprocess_all()
    except Exception:
        traceback.print_exc()

    print('\n' + '=' * 62)
    print('成功 %d / %d' % (ok, len(slugs)))
    if fail:
        print('失败 %d: %s' % (len(fail), ', '.join(fail)))


if __name__ == '__main__':
    main()
