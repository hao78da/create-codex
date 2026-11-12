# -*- coding: utf-8 -*-
import json, io, os

D = json.load(open(r'D:\frontend\_raw\out\data.json', encoding='utf-8'))
IT = D['items']

ids = []
for line in open(r'D:\frontend\_raw\out\groups3\k4.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip():
        continue
    parts = line.split('\t')
    ids.append(parts[0])

out = io.open(r'D:\frontend\_raw\batches\_k4_dump.txt', 'w', encoding='utf-8')


def cond(r):
    t = r.get('type', '?')
    s = t
    res = r.get('results') or []
    rs = ','.join('%s x%s' % (x.get('id'), x.get('count')) for x in res)
    if 'pattern' in r:
        s += ' pattern=' + '/'.join(r['pattern'])
        key = r.get('key') or {}
        s += ' key=' + ';'.join('%s=%s' % (k, v.get('id') or v.get('tag')) for k, v in key.items())
    if 'ingredients' in r:
        s += ' ing=' + ';'.join((x.get('id') or x.get('tag')) + 'x' + str(x.get('count')) for x in r['ingredients'])
    s += ' -> ' + rs
    if r.get('file'):
        s += ' [' + r['file'] + ']'
    return s


out.write('TOTAL %d\n\n' % len(ids))
for i in ids:
    if i not in IT:
        out.write('MISSING %s\n\n' % i)
        continue
    it = IT[i]
    out.write('=== %s | %s | %s\n' % (i, it.get('n'), it.get('en')))
    out.write('kind=%s icon=%s\n' % (it.get('kind'), it.get('icon')))
    if it.get('tooltip'):
        out.write('TOOLTIP: %s\n' % json.dumps(it['tooltip'], ensure_ascii=False))
    out.write('-- recipes (%d)\n' % len(it.get('recipes') or []))
    for r in (it.get('recipes') or []):
        out.write('   ' + cond(r) + '\n')
    p = it.get('ponder')
    if p:
        if isinstance(p, dict):
            out.write('-- ponder keys: %s\n' % list(p.keys()))
            for k, v in p.items():
                out.write('   %s: %s\n' % (k, json.dumps(v, ensure_ascii=False)[:1200]))
        else:
            out.write('-- ponder: %s\n' % json.dumps(p, ensure_ascii=False)[:1500])
    else:
        out.write('-- ponder: null\n')
    out.write('\n')
out.close()
print('ok')
