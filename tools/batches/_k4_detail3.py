import json, collections
P = r'D:\frontend\_raw\out\data.json'
d = json.load(open(P, encoding='utf-8'))
items = d['items']
out = []
def short(o, n=400):
    return json.dumps(o, ensure_ascii=False)[:n]
out.append("== total items: %d ==" % len(items))
for t in ['milling', 'cutting', 'pressing', 'sandpaper_polishing', 'item_application', 'mixing', 'compacting', 'filling', 'splashing', 'haunting', 'sequenced_assembly', 'mechanical_crafting', 'deploying']:
    rows = []
    for rid, it in items.items():
        for r in (it.get('recipes') or []):
            if str(r.get('type')) == t:
                rows.append(r)
    out.append("\n## %s (%d)" % (t, len(rows)))
    for r in rows[:40]:
        out.append("  - " + short(r, 300))
out.append("\n== ALL ITEM IDS ==")
line = []
for rid, it in items.items():
    line.append(rid + "=" + str(it.get('n')))
out.append("；".join(line))
open(r'D:\frontend\_raw\batches\_k4_detail3.txt', 'w', encoding='utf-8').write("\n".join(out))
print("ok")
