import json, collections
P = r'D:\frontend\_raw\out\data.json'
d = json.load(open(P, encoding='utf-8'))
items = d['items']
ids = [l.split('\t')[0] for l in open(r'D:\frontend\_raw\out\groups3\k4.txt', encoding='utf-8') if l.strip()]
STONE = ('layered_', 'cut_', 'small_', 'polished_')
mach = [i for i in ids if not i.split(':')[1].startswith(STONE) and 'pillar' not in i and i.split(':')[1] in (
 'ochrum','scorchia','scoria','crimsite','brass_funnel','powdered_obsidian','track','mechanical_saw','andesite_funnel',
 'vertical_gearbox','mechanical_arm','brass_sheet','mechanical_crafter','mechanical_press','gearbox','millstone','rose_quartz',
 'deployer','zinc_ingot','rotation_speed_controller','basin','iron_sheet','crushing_wheel','large_water_wheel','copper_sheet',
 'sturdy_sheet','belt','large_cogwheel','cogwheel','precision_mechanism','wrench')]
out = []
def short(o, n=520):
    return json.dumps(o, ensure_ascii=False)[:n]
rev = collections.defaultdict(list)
for rid, it in items.items():
    for r in (it.get('recipes') or []):
        s = json.dumps(r, ensure_ascii=False)
        for iid in ids:
            if iid in s and iid != rid:
                rev[iid].append((rid, str(r.get('type')), short(r.get('output') or r.get('result') or '', 100)))
out.append("== machine/material items ==")
for i in mach:
    it = items.get(i)
    if not it:
        out.append(i + ": MISSING"); continue
    out.append("\n### " + i + " | " + str(it.get('en')) + " | tooltip=" + short(it.get('tooltip'), 300))
    rs = it.get('recipes') or []
    out.append("  recipes(%d):" % len(rs))
    for r in rs:
        out.append("   - " + short(r, 620))
    out.append("  used_in(%d):" % len(rev[i]))
    for u in rev[i][:14]:
        out.append("   * " + u[0] + " [" + u[1] + "] -> " + u[2])
out.append("\n== recipe types ==")
c = collections.Counter()
for rid, it in items.items():
    for r in (it.get('recipes') or []):
        c[str(r.get('type'))] += 1
out.append(short(dict(c), 3000))
for t in ['create:milling', 'create:cutting', 'create:pressing', 'create:crushing', 'create:sanding', 'create:polishing', 'create:mixing', 'create:compacting', 'create:filling', 'create:deploying', 'create:item_application']:
    names = []
    for rid, it in items.items():
        for r in (it.get('recipes') or []):
            if str(r.get('type')) == t:
                names.append(it.get('n') or rid)
    out.append("\n## " + t + " -> outputs(" + str(len(set(names))) + "): " + "、".join(list(dict.fromkeys(names))[:40]))
open(r'D:\frontend\_raw\batches\_k4_detail2.txt', 'w', encoding='utf-8').write("\n".join(out))
print("ok", len(mach))
