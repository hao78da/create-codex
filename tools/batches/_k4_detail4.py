import json
P = r'D:\frontend\_raw\out\data.json'
d = json.load(open(P, encoding='utf-8'))
items = d['items']
out = []
targets = ['create:ochrum', 'create:crimsite', 'create:veridium', 'create:asurine', 'create:scoria', 'create:scorchia', 'create:limestone', 'minecraft:tuff', 'minecraft:dripstone_block']
for rid, it in items.items():
    for r in (it.get('recipes') or []):
        s = json.dumps(r, ensure_ascii=False)
        if any(t in s for t in targets) and str(r.get('type')) in ('crushing', 'milling', 'splashing'):
            out.append(rid + " :: " + s[:420])
out.append("\n=== sleepers tag / misc tags ===")
import os
base = r'D:\frontend\_raw\create\Create-mc1.20.1-dev\src\generated\resources\data\create\tags'
for t in ['items/sleepers.json', 'item/sleepers.json', 'blocks/sleepers.json']:
    p = os.path.join(base, t)
    if os.path.exists(p):
        out.append(t + ": " + open(p, encoding='utf-8').read()[:400])
out.append("\n=== worldgen strata dirs ===")
for root, dirs, files in os.walk(r'D:\frontend\_raw\create\Create-mc1.20.1-dev\src\generated\resources\data\create\worldgen'):
    if 'strata' in root or 'layer' in root:
        out.append(root + " -> " + ", ".join(files[:12]))
open(r'D:\frontend\_raw\batches\_k4_detail4.txt', 'w', encoding='utf-8').write("\n".join(out))
print("ok")
