# -*- coding: utf-8 -*-
"""把页面里仍指向 _unknown.png 的物品卡，替换成已生成的真图。

只做定点替换，不重新生成整站（避免覆盖别人的改动）。

替换规则：
  1. 扫 docs/addon-*.html 里 <div class="card" id="it-<ns>-<name>">
  2. 若该卡的 <img src> 是 _unknown.png，查找候选真图：
       assets/icons/3d_<ns>_<name>.png      （render_missing 产出）
       assets/icons/<ns>_<name>.png         （原始平面图）
       assets/icons/create_<name>.png       （旧命名）
  3. 命中就替换 src，否则保留占位

用法：
    python tools/fix_placeholders.py            # 实际替换
    python tools/fix_placeholders.py --dry      # 只报告会替换多少
"""
import glob
import io
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SITE = os.path.join(ROOT, 'docs')
ICONS = os.path.join(SITE, 'assets', 'icons')

CARD_RE = re.compile(
    r'(<div class="card" id="it-([^"]+)">\s*<div class="ci"><img src=")([^"]+)(")', re.S)


def candidates(ns, name):
    return [
        'assets/icons/3d_%s_%s.png' % (ns, name),
        'assets/icons/3d_%s.png' % name,
        'assets/icons/%s_%s.png' % (ns, name),
        'assets/icons/create_%s.png' % name,
        'assets/icons/minecraft_%s.png' % name,
        'assets/icons/hh3d_%s.png' % name,
    ]


def main():
    dry = '--dry' in sys.argv

    pages = glob.glob(os.path.join(SITE, 'addon-*.html'))
    print('页面数: %d' % len(pages), flush=True)

    total_repl = 0
    pages_changed = 0
    stats = {}

    for f in pages:
        s = io.open(f, encoding='utf-8', errors='replace').read()
        orig = s
        cnt = [0]

        def rep(m):
            head, iid, src, tail = m.group(1), m.group(2), m.group(3), m.group(4)
            if '_unknown.png' not in src:
                return m.group(0)
            if '-' not in iid:
                return m.group(0)
            ns, name = iid.split('-', 1)
            for cand in candidates(ns, name):
                p = os.path.join(SITE, cand.replace('/', os.sep))
                if os.path.exists(p):
                    cnt[0] += 1
                    stats[ns] = stats.get(ns, 0) + 1
                    return head + cand + tail
            return m.group(0)

        s2 = CARD_RE.sub(rep, s)
        if s2 != orig:
            total_repl += cnt[0]
            pages_changed += 1
            if not dry:
                io.open(f, 'w', encoding='utf-8').write(s2)
            if cnt[0]:
                print('  %-42s +%d' % (os.path.basename(f), cnt[0]), flush=True)

    print()
    print('=' * 60)
    print('%s: %d 处' % ('会替换' if dry else '已替换', total_repl))
    print('%s页面: %d' % ('涉及' if dry else '改动', pages_changed))
    if stats:
        print()
        print('按命名空间:')
        for k, v in sorted(stats.items(), key=lambda x: -x[1])[:15]:
            print('  %-26s %d' % (k, v))


if __name__ == '__main__':
    main()
