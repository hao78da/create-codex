import ast, json, re, io

BASE = r'D:\frontend\_raw\batches'
text = open(f'{BASE}\\k4.py', encoding='utf-8').read()

d = json.load(open(r'D:\frontend\_raw\out\data.json', encoding='utf-8'))
known = set(d['items'].keys())
want = []
for line in open(r'D:\frontend\_raw\out\groups3\k4.txt', encoding='utf-8'):
    line = line.rstrip('\n')
    if not line.strip():
        continue
    want.append(line.split('\t')[0])

rep = []
errors = []
try:
    tree = ast.parse(text)
except SyntaxError as e:
    rep.append(f"AST FAIL: {e}")
    open(f'{BASE}\\_k4_report.txt', 'w', encoding='utf-8').write("\n".join(rep))
    raise SystemExit

calls = [n for n in ast.walk(tree) if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'item']
ids = []
cjk = re.compile(r'[\u4e00-\u9fff]')
allowed = {'p', 'ul', 'li', 'strong'}
tag_re = re.compile(r'<(/?)([a-zA-Z]+)[^>]*>')

rows = []
for c in calls:
    iid = c.args[0].value
    ids.append(iid)
    tagline = c.args[1].value
    secs = c.args[2]
    if len(secs.elts) != 3:
        errors.append(f"{iid}: sections={len(secs.elts)}")
    total = 0
    sec_report = []
    for s in secs.elts:
        tup = s.elts
        title = tup[0].value
        html = tup[1].value
        ps = re.findall(r'<p>(.*?)</p>', html, re.S)
        if len(ps) < 2:
            errors.append(f"{iid}/{title}: p={len(ps)}")
        lens = []
        for p in ps:
            n = len(cjk.findall(p))
            total += n
            lens.append(n)
            if n < 55 or n > 100:
                errors.append(f"{iid}/{title}: p 字数 {n}")
        # tags
        for m in tag_re.finditer(html):
            if m.group(2) not in allowed:
                errors.append(f"{iid}/{title}: bad tag {m.group(2)}")
        sec_report.append(f"{title}:{lens}")
    # balance
    stack = []
    for m in tag_re.finditer("".join(s.elts[1].value for s in secs.elts)):
        if m.group(1) == '/':
            if not stack or stack.pop() != m.group(2):
                errors.append(f"{iid}: unbalanced")
                break
        else:
            stack.append(m.group(2))
    if stack:
        errors.append(f"{iid}: unclosed {stack}")
    # params / related
    kw = {k.arg: k.value for k in c.keywords}
    params = kw.get('params')
    rel = kw.get('related')
    np = len(params.elts) if params is not None else 0
    nr = len(rel.elts) if rel is not None else 0
    if not (2 <= np <= 4):
        errors.append(f"{iid}: params={np}")
    if not (2 <= nr <= 3):
        errors.append(f"{iid}: related={nr}")
    rels = [e.value for e in rel.elts] if rel is not None else []
    if iid in rels:
        errors.append(f"{iid}: related 含自身")
    for r in rels:
        if r not in known:
            errors.append(f"{iid}: related 不存在 {r}")
    rows.append((iid, total, len(tagline), " | ".join(sec_report)))

rep.append(f"items={len(calls)} 顺序匹配={ids == want}")
if ids != want:
    for i, (a, b) in enumerate(zip(ids, want)):
        if a != b:
            rep.append(f"  第{i+1}条 期望 {b} 实际 {a}")
    if len(ids) != len(want):
        rep.append(f"  条数不符: {len(ids)} vs {len(want)}")
short = [r for r in rows if r[1] < 260]
rep.append(f"最短={min(r[1] for r in rows)} 平均={sum(r[1] for r in rows)//len(rows)}")
rep.append("低于260: " + (", ".join(f"{i}({n})" for i, n, t, s in short) if short else "无"))
rep.append("")
rep.append("=== 每条字数 ===")
for i, n, t, s in rows:
    rep.append(f"{i}\t{n}\t{('标题'+str(t)) if t>20 else ''}\t{s}")

# duplicates
paras = {}
for c in calls:
    iid = c.args[0].value
    for s in c.args[2].elts:
        for p in re.findall(r'<p>(.*?)</p>', s.elts[1].value, re.S):
            paras.setdefault(p, []).append(iid)
dups = {p: v for p, v in paras.items() if len(v) > 1}
rep.append("")
rep.append(f"=== 完全重复段落 {len(dups)} 处 ===")
for p, v in list(dups.items())[:20]:
    rep.append(f"{v} :: {p[:50]}")

# 句首 8 字重复
heads = {}
for c in calls:
    iid = c.args[0].value
    for s in c.args[2].elts:
        for p in re.findall(r'<p>(.*?)</p>', s.elts[1].value, re.S):
            plain = re.sub(r'<[^>]+>', '', p)
            heads.setdefault(plain[:8], []).append(iid)
rep.append("")
rep.append("=== 段首8字完全相同 ===")
for h, v in heads.items():
    if len(v) > 1:
        rep.append(f"{h} :: {v}")

# forbidden
for bad in ['<script', '</script']:
    if bad in text:
        rep.append(f"!! 含 {bad}")
rep.append("")
rep.append(f"=== 错误 {len(errors)} 条 ===")
rep += errors[:80]
open(f'{BASE}\\_k4_report.txt', 'w', encoding='utf-8').write("\n".join(rep))
print("done", len(calls))
