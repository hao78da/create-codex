# -*- coding: utf-8 -*-
"""根据 _ns_map.json 自动为有物品的模组生成 spec 片段。

用法: python _gen_specs.py [--out specs.txt]
读取: ../_ns_map.json  ../_matched_ok.json（取 mcmod 中文名/英文名）
输出: 可直接粘进 gen_addon_multi.py 的 dict(...) 列表
"""
import io
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

NS_MAP = os.path.join(ROOT, '_ns_map.json')
MATCHED = os.path.join(ROOT, '_matched_ok.json')


def esc(s):
    s = s.replace('\\', '\\\\').replace("'", "\\'")
    return s


def main():
    nsm = json.load(io.open(NS_MAP, encoding='utf-8'))
    matched = {x['slug']: x for x in json.load(io.open(MATCHED, encoding='utf-8'))}

    lines = []
    for slug, v in sorted(nsm.items()):
        ns = v['ns']
        cnt = max(v['counts'].values())
        info = matched.get(slug, {})
        mr_title = info.get('mr_title') or info.get('en') or slug
        cn = info.get('title') or ''
        # 中文名（mcmod 的 title 里括号前那部分，去掉 [短名] 前缀）
        cnname = re.sub(r'^\[[^\]]+\]\s*', '', cn).strip()
        cnname = re.sub(r'[（(][^（()）]*[)）]\s*$', '', cnname).strip()

        tag = '%s' % (mr_title[:40])
        intro = '来自 mcmod 1.20.1 附属模组清单，共 %d 个物品。' % cnt

        lines.append(
            "    dict(slug='%s', ns='%s', title='%s',\n"
            "         tag='%s',\n"
            "         intro='%s',\n"
            "         groups=[])," % (
                slug, ns, esc(mr_title), esc(tag), esc(intro)))

    out = os.path.join(ROOT, 'specs.txt')
    io.open(out, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
    print('生成 %d 条 spec ->' % len(lines), out)
    print()
    print(lines[0])


if __name__ == '__main__':
    main()
