# -*- coding: utf-8 -*-
"""对页面里仍是 _unknown.png 的物品，尝试用 render3d 生成真图。

流程：
  1. 扫 docs/addon-*.html，找出所有 <div class="card" id="it-<ns>-<name>">
     且图标是 _unknown.png 的物品
  2. 对每个物品，在 work/assets/<ns>/models/{item,block}/<name>.json 找模型
  3. 命中的交给 render3d.render() 出图，写到 docs/assets/icons/3d_<ns>_<name>.png
  4. 打印统计，不碰页面（页面替换由 fix_placeholders.py 负责）

用法：
    python tools/render_missing.py              # 全量跑
    python tools/render_missing.py --ns kuayue  # 只跑某个命名空间
    python tools/render_missing.py --limit 20   # 只跑前 20 个（试水）
    python tools/render_missing.py --dry        # 只报告，不渲染
"""
import glob
import io
import json
import os
import re
import sys
import traceback
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

SITE = os.path.join(ROOT, 'docs')
ICONS = os.path.join(SITE, 'assets', 'icons')
ASSETS = os.path.join(ROOT, 'work', 'assets')

# 匹配：卡片 id + 卡片内的第一个 img 是 _unknown.png
CARD_RE = re.compile(
    r'<div class="card" id="it-([^"]+)">\s*<div class="ci"><img src="([^"]+)"', re.S)


def collect_placeholders():
    """返回 [(ns, name, page)]，已去重"""
    seen = set()
    out = []
    for f in glob.glob(os.path.join(SITE, 'addon-*.html')):
        s = io.open(f, encoding='utf-8', errors='replace').read()
        for m in CARD_RE.finditer(s):
            iid, src = m.group(1), m.group(2)
            if '_unknown.png' not in src:
                continue
            if '-' not in iid:
                continue
            ns, name = iid.split('-', 1)
            key = (ns, name)
            if key in seen:
                continue
            seen.add(key)
            out.append((ns, name, os.path.basename(f)))
    return out


_MODEL_INDEX = {}


def _build_index(ns):
    """递归建 ns -> {basename: [relpath]} 索引（模型可能在子目录里）"""
    if ns in _MODEL_INDEX:
        return _MODEL_INDEX[ns]
    idx = {}
    base = os.path.join(ASSETS, ns, 'models')
    if os.path.isdir(base):
        for root, _dirs, files in os.walk(base):
            for f in files:
                if not f.endswith('.json'):
                    continue
                rel = os.path.relpath(os.path.join(root, f), base)
                rel = rel.replace(os.sep, '/')[:-5]
                idx.setdefault(f[:-5], []).append(rel)
    _MODEL_INDEX[ns] = idx
    return idx


def find_model(ns, name):
    """在 work/assets/<ns>/models 里递归找同名模型，item/ 优先"""
    idx = _build_index(ns)
    cands = idx.get(name) or []
    if not cands:
        return None
    # 优先 item/，其次 block/，其余按字典序
    def rank(rel):
        if rel.startswith('item/'):
            return (0, rel)
        if rel.startswith('block/'):
            return (1, rel)
        return (2, rel)
    best = sorted(cands, key=rank)[0]
    return '%s:%s' % (ns, best)


def main():
    args = sys.argv[1:]
    only_ns = None
    if '--ns' in args:
        only_ns = args[args.index('--ns') + 1]
    limit = None
    if '--limit' in args:
        limit = int(args[args.index('--limit') + 1])
    dry = '--dry' in args

    items = collect_placeholders()
    print('占位物品总数: %d' % len(items), flush=True)
    if only_ns:
        items = [x for x in items if x[0] == only_ns]
        print('限定 %s: %d 个' % (only_ns, len(items)), flush=True)

    # 按命名空间排序，便于分批
    items.sort()
    if limit:
        items = items[:limit]
        print('限制前 %d 个' % limit, flush=True)

    print()

    # 延迟导入 render3d（它 import numpy/PIL，失败时不至于整体崩）
    try:
        import render3d as R
    except Exception as e:
        print('render3d 导入失败:', e)
        print('需要 numpy + Pillow')
        return

    ok, miss, err = [], [], []
    ns_stat = Counter()

    for i, (ns, name, page) in enumerate(items, 1):
        model = find_model(ns, name)
        if not model:
            miss.append((ns, name, 'no-model'))
            continue
        if dry:
            print('[%d/%d] %-40s -> %s' % (i, len(items), '%s:%s' % (ns, name), model), flush=True)
            ok.append((ns, name, page))
            ns_stat[ns] += 1
            continue

        out_icon = '3d_%s_%s.png' % (ns, name)
        dst = os.path.join(ICONS, out_icon)
        if os.path.exists(dst):
            ok.append((ns, name, page))
            ns_stat[ns] += 1
            continue

        try:
            # render() 只返回 (PIL.Image, missing列表)，不写文件
            im, missing = R.render(model)
            if im is None:
                miss.append((ns, name, 'no-image(%s)' % (missing if isinstance(missing, str) else 'empty')))
                continue
            im.save(dst)
            print('[%d/%d] %-42s ✓ %s' % (i, len(items), '%s:%s' % (ns, name), out_icon), flush=True)
            ok.append((ns, name, page))
            ns_stat[ns] += 1
        except Exception as e:
            err.append((ns, name, '%s: %s' % (type(e).__name__, str(e)[:60])))

    print()
    print('=' * 62)
    print('成功渲染: %d' % len(ok))
    print('无模型跳过: %d' % len([x for x in miss if x[2] == 'no-model']))
    print('渲染无输出: %d' % len([x for x in miss if x[2] == 'no-output']))
    print('异常: %d' % len(err))
    if ns_stat:
        print()
        print('按命名空间:')
        for k, v in ns_stat.most_common(20):
            print('  %-26s %d' % (k, v))
    if err:
        print()
        print('前 10 个异常:')
        for x in err[:10]:
            print('  %-40s %s' % ('%s:%s' % (x[0], x[1]), x[2]))


if __name__ == '__main__':
    main()
