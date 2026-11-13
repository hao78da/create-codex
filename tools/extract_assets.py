# -*- coding: utf-8 -*-
"""把 work/mods_intake/*.jar 里的模型与贴图解到 work/assets/<ns>/。

用途：render3d.py / backfill 类脚本需要按命名空间查找模型链，
但模组资源都在 jar 里。本脚本把它们摊平到磁盘，不打散 jar 本身。

解出的内容（保持 jar 内相对路径）：
    work/assets/<ns>/models/**.json
    work/assets/<ns>/blockstates/**.json
    work/assets/<ns>/textures/**.png
    work/assets/<ns>/lang/zh_cn.json   （按需）

用法：
    python tools/extract_assets.py              # 全部 jar
    python tools/extract_assets.py kuayue       # 只解某个命名空间
    python tools/extract_assets.py --list       # 只列出会解什么

约定：
  - 不覆盖已有文件（用 --force 才覆盖），便于增量补
  - jar 内同时含 minecraft 命名空间时也解开（父模型指向原版需要）
"""
import io
import json
import os
import sys
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
JARS = os.path.join(ROOT, 'work', 'mods_intake')
OUT = os.path.join(ROOT, 'work', 'assets')

# 只解这些子目录，其它（如 sounds/、shaders/）跳过以省空间
WANT = ('models/', 'blockstates/', 'textures/')


def main():
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    force = '--force' in sys.argv
    only_list = '--list' in sys.argv

    if not os.path.isdir(JARS):
        print('jar 目录不存在:', JARS)
        return

    jars = sorted(f for f in os.listdir(JARS) if f.endswith('.jar'))
    print('jar 数:', len(jars))
    if args:
        print('限定命名空间:', ', '.join(args))
    print()

    total_new = total_skip = total_ns = 0
    per_ns = {}

    for jn in jars:
        p = os.path.join(JARS, jn)
        try:
            z = zipfile.ZipFile(p)
        except Exception as e:
            print('跳过损坏 jar: %s (%s)' % (jn, e))
            continue

        names = z.namelist()
        # jar 内所有 assets/<ns>/
        nss = sorted({n.split('/')[1] for n in names
                      if n.startswith('assets/') and n.count('/') >= 2})
        if args:
            nss = [x for x in nss if x in args]

        extracted = 0
        for ns in nss:
            for n in names:
                if not n.startswith('assets/%s/' % ns):
                    continue
                rel = n[len('assets/%s/' % ns):]
                if not rel.startswith(WANT):
                    continue
                if not (rel.endswith('.json') or rel.endswith('.png')):
                    continue

                dst = os.path.join(OUT, ns, rel.replace('/', os.sep))
                if os.path.exists(dst) and not force:
                    total_skip += 1
                    continue
                if only_list:
                    print('  [list] %s/%s' % (ns, rel))
                    total_new += 1
                    continue

                os.makedirs(os.path.dirname(dst), exist_ok=True)
                try:
                    with z.open(n) as f, open(dst, 'wb') as o:
                        o.write(f.read())
                except Exception:
                    continue
                total_new += 1
                per_ns[ns] = per_ns.get(ns, 0) + 1
                extracted += 1

        total_ns += len(nss)
        if extracted and not only_list:
            print('%-34s +%-5d  %s' % (jn[:32], extracted, ','.join(nss)[:40]))

    print()
    print('=' * 60)
    print('新解出: %d 个文件' % total_new)
    print('已存在跳过: %d' % total_skip)
    print('涉及命名空间: %d' % len(per_ns))
    print('输出目录:', OUT)
    if per_ns and not only_list:
        print()
        print('文件最多的 15 个命名空间:')
        for k, v in sorted(per_ns.items(), key=lambda x: -x[1])[:15]:
            print('  %-24s %d' % (k, v))


if __name__ == '__main__':
    main()
