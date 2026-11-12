import ast, json, re, io

PY = r"D:\frontend\_raw\batches\k2.py"
OUT = r"D:\frontend\_raw\batches\_k2_check.txt"
DATA = r"D:\frontend\_raw\out\data.json"
TSV = r"D:\frontend\_raw\out\groups3\k2.txt"

src = open(PY, encoding="utf-8").read()
lines = []
def w(s=""):
    lines.append(str(s))

w("BOM: " + str(src.startswith("\ufeff")))
w("bytes: " + str(len(src.encode("utf-8"))))

tree = ast.parse(src)
w("ast.parse: OK, body=%d" % len(tree.body))

d = json.load(open(DATA, encoding="utf-8"))
items_db = d["items"]
ids_tsv = []
for ln in open(TSV, encoding="utf-8"):
    ln = ln.rstrip("\n")
    if not ln.strip():
        continue
    parts = ln.split("\t")
    ids_tsv.append(parts[0].strip())

cjk = lambda s: len(re.findall(r"[\u4e00-\u9fff]", s))
allowed_titles = {"怎么获得", "怎么用", "进阶", "常见坑", "搭配"}

records = []
errors = []
all_sent = {}
for node in tree.body:
    if not isinstance(node, ast.Expr) or not isinstance(node.value, ast.Call):
        errors.append("非 item() 顶层语句: %s" % ast.dump(node)[:60])
        continue
    call = node.value
    if getattr(call.func, "id", "") != "item":
        errors.append("非 item 调用")
        continue
    iid = call.args[0].value
    tag = call.args[1].value
    secs = []
    for s in call.args[2].elts:
        t = s.elts[0].value
        h = s.elts[1].value
        secs.append((t, h))
    kw = {k.arg: k.value for k in call.keywords}
    params = [(e.elts[0].value, e.elts[1].value) for e in kw["params"].elts]
    related = [e.value for e in kw["related"].elts]

    total = 0
    para_lens = []
    for t, h in secs:
        if t not in allowed_titles:
            errors.append("%s 标题非法 %s" % (iid, t))
        if "<script" in h or "</script>" in h:
            errors.append("%s 含 script" % iid)
        bad = re.findall(r"</?(?!p>|strong>|/p>|/strong>)[a-zA-Z][a-zA-Z0-9]*", h)
        for b in bad:
            errors.append("%s 非法标签 %s" % (iid, b))
        if h.count("<p>") != h.count("</p>"):
            errors.append("%s p 不闭合" % iid)
        if h.count("<strong>") != h.count("</strong>"):
            errors.append("%s strong 不闭合" % iid)
        if "<strong>" not in h:
            errors.append("%s 该节无 strong" % iid)
        ps = re.findall(r"<p>(.*?)</p>", h, re.S)
        if len(ps) < 2:
            errors.append("%s/%s 段数 %d" % (iid, t, len(ps)))
        for p in ps:
            c = cjk(re.sub(r"<[^>]+>", "", p))
            para_lens.append((t, c))
            total += c
            for sent in re.split(r"[，。；、：？！]", re.sub(r"<[^>]+>", "", p)):
                sent = sent.strip()
                if len(sent) >= 10:
                    all_sent.setdefault(sent, []).append(iid)
    if len(secs) != 3:
        errors.append("%s 节数 %d" % (iid, len(secs)))
    if total < 260:
        errors.append("%s 总字数 %d < 260" % (iid, total))
    if not (2 <= len(params) <= 4):
        errors.append("%s params %d" % (iid, len(params)))
    if not (2 <= len(related) <= 3):
        errors.append("%s related %d" % (iid, len(related)))
    for r in related:
        if r not in items_db:
            errors.append("%s related 不存在 %s" % (iid, r))
    if iid not in items_db:
        errors.append("%s 不在 data.json" % iid)
    if len(tag) > 20:
        errors.append("%s 定位语过长 %d" % (iid, len(tag)))
    records.append((iid, tag, total, para_lens, [t for t, _ in secs]))

ids_done = [r[0] for r in records]
w("条数: %d" % len(records))
w("TSV 条数: %d" % len(ids_tsv))
w("缺失: " + str([i for i in ids_tsv if i not in ids_done]))
w("多余: " + str([i for i in ids_done if i not in ids_tsv]))
w("顺序与 TSV 一致: " + str(ids_done == ids_tsv))

recs_sorted = sorted(records, key=lambda r: r[2])
w("\n最短 5 条:")
for r in recs_sorted[:5]:
    w("  %s %d %s" % (r[0], r[2], r[1]))
w("最长: %s %d" % (recs_sorted[-1][0], recs_sorted[-1][2]))

pl_short = [(r[0], t, c) for r in records for (t, c) in r[3] if c < 60]
pl_long = [(r[0], t, c) for r in records for (t, c) in r[3] if c > 90]
w("\n段落 <60 数: %d" % len(pl_short))
for x in pl_short[:40]:
    w("  %s/%s %d" % x)
w("段落 >90 数: %d" % len(pl_long))
for x in pl_long[:40]:
    w("  %s/%s %d" % x)

dups = {k: v for k, v in all_sent.items() if len(set(v)) > 1}
w("\n跨条重复句数: %d" % len(dups))
for k, v in list(dups.items())[:30]:
    w("  [%s] %s" % (",".join(sorted(set(v))), k))

w("\n错误 %d 条:" % len(errors))
for e in errors[:80]:
    w("  " + e)

open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("done", len(records), len(errors))
