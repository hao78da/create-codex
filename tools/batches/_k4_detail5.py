import json, collections, os, re
P = r'D:\frontend\_raw\out\data.json'
d = json.load(open(P, encoding='utf-8'))
items = d['items']
out = []
for tag in ['forge:plates/copper', 'forge:plates/brass', 'forge:plates/iron', 'forge:plates/obsidian', 'forge:plates/gold']:
    rows = []
    for rid, it in items.items():
        for r in (it.get('recipes') or []):
            if tag in json.dumps(r, ensure_ascii=False) and str(r.get('type')) in ('crafting_shaped', 'crafting_shapeless', 'mechanical_crafting'):
                rows.append(rid + "[" + str(r.get('type')) + "]x" + str((r.get('results') or [{}])[0].get('count')))
    out.append(tag + " -> " + "、".join(list(dict.fromkeys(rows))[:20]))
open(r'D:\frontend\_raw\batches\_k4_detail5.txt', 'w', encoding='utf-8').write("\n".join(out))
print("ok")
