# -*- coding: utf-8 -*-
import json, io, os, glob

base = r'D:\frontend\_raw\create\Create-mc1.20.1-dev\src\generated\resources'
ids = []
for line in open(r'D:\frontend\_raw\out\groups3\k4.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if line.strip():
        ids.append(line.split('\t')[0])

out = io.open(r'D:\frontend\_raw\batches\_k4_info.txt', 'w', encoding='utf-8')
out.write('== block_info ==\n')
for i in ids:
    p = os.path.join(base, 'data', 'create', '.wiki', 'block_info', i.split(':')[1] + '.json')
    if os.path.exists(p):
        d = json.load(open(p, encoding='utf-8'))
        out.write('%s: %s\n' % (i, json.dumps(d, ensure_ascii=False, sort_keys=True)))
    else:
        out.write('%s: NOINFO\n' % i)

out.write('\n== stone_types tags ==\n')
for f in sorted(glob.glob(os.path.join(base, 'data', 'create', 'tags', 'items', 'stone_types', '*.json'))):
    d = json.load(open(f, encoding='utf-8'))
    vals = d.get('values', [])
    out.write('%s (%d): %s\n' % (os.path.basename(f), len(vals), ', '.join(v if isinstance(v, str) else str(v) for v in vals)))
out.close()
print('ok')
