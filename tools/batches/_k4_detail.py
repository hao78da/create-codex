import json, collections, re
P = r'D:\frontend\_raw\out\data.json'
d = json.load(open(P, encoding='utf-8'))
items = d['items']
ids = [l.split('\t')[0] for l in open(r'D:\frontend\_raw\out\groups3\k4.txt', encoding='utf-8') if l.strip()]
out = []
def short(o, n=520):
    s = json.dumps(o, ensure_ascii=False)
    return s[:n]
# reverse index: ingredient id -> list of "recipeId -> out"
rev = collections.defaultdict(list)
for rid, it in items.items():
    for r in (it.get('recipes') or []):
        s = json.dumps(r, ensure_ascii=False)
        for iid in items:
            if iid in s and iid != rid:
                rev[iid].append((rid, str(r.get('type')), short(r.get('output') or r.get('result') or '', 120)))
out.append("== per item ==")
for i in ids:
    it = items.get(i)
    if not it:
        out.append(i + ": MISSING"); continue
    out.append("\n### " + i + " | " + str(it.get('en')) + " | tooltip=" + short(it.get('tooltip'), 200))
    rs = it.get('recipes') or []
    out.append("  recipes(%d):" % len(rs))
    for r in rs:
        out.append("   - " + short(r, 460))
    out.append("  used_in(%d):" % len(rev[i]))
    for u in rev[i][:12]:
        out.append("   * " + u[0] + " [" + u[1] + "] -> " + u[2])
# recipe type census + machine recipe lists
out.append("\n== recipe types ==")
c = collections.Counter()
for rid, it in items.items():
    for r in (it.get('recipes') or []):
        c[str(r.get('type'))] += 1
out.append(short(dict(c), 3000))
for t in ['create:milling', 'create:cutting', 'create:pressing', 'create:crushing', 'create:mixing', 'create:splashing', 'create:compacting', 'create:filling', 'create:deploying', 'create:item_application', 'create:sanding', 'create:polishing']:
    names = []
    for rid, it in items.items():
        for r in (it.get('recipes') or []):
            if str(r.get('type')) == t:
                names.append(it.get('n') or rid)
    out.append("\n## " + t + " outputs(" + str(len(names)) + "): " + "、".join(names[:40]))
open(r'D:\frontend\_raw\batches\_k4_detail.txt', 'w', encoding='utf-8').write("\n".join(out))
print("ok")
