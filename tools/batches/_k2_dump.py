# -*- coding: utf-8 -*-
import json, io, sys

d = json.load(open(r'D:\frontend\_raw\out\data.json', encoding='utf-8'))
ids = [l.split('\t')[0] for l in open(r'D:\frontend\_raw\out\groups3\k2.txt', encoding='utf-8').read().strip().split('\n')]

out = io.StringIO()

def short(x, n=180):
    s = json.dumps(x, ensure_ascii=False) if not isinstance(x, str) else x
    s = s.replace('\n', ' ')
    return s[:n]

for idx, iid in enumerate(ids):
    it = d['items'][iid]
    out.write('=== %02d %s | %s | %s\n' % (idx + 1, iid, it.get('n'), it.get('en')))
    rs = it.get('recipes') or []
    for r in rs[:4]:
        t = r.get('type', '')
        line = '  R[%s] ' % t
        if r.get('pattern'):
            line += 'pat=%s ' % r['pattern']
        if r.get('key'):
            line += 'key=%s ' % short(r['key'], 200)
        if r.get('ingredients'):
            line += 'ing=%s ' % short(r['ingredients'], 240)
        if r.get('results'):
            line += 'res=%s ' % short(r['results'], 160)
        if r.get('processing'):
            line += 'proc=%s ' % short(r['processing'], 120)
        extra = {k: v for k, v in r.items() if k not in ('type', 'pattern', 'key', 'ingredients', 'results', 'processing')}
        if extra:
            line += 'x=%s ' % short(extra, 140)
        out.write(line.strip() + '\n')
    p = it.get('ponder') or []
    if p:
        for e in p[:2]:
            out.write('  P: %s\n' % short(e, 700))
    out.write('\n')

open(r'D:\frontend\_raw\batches\_k2_dump.txt', 'w', encoding='utf-8').write(out.getvalue())
print('ok', len(out.getvalue()))
