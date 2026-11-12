import ast, json, re

PY = r"D:\frontend\_raw\batches\k2.py"
OUT = r"D:\frontend\_raw\batches\_k2_check2.txt"
src = open(PY, encoding="utf-8").read()
tree = ast.parse(src)
lines = []
w = lines.append

cjk = lambda s: len(re.findall(r"[\u4e00-\u9fff]", s))
allch = lambda s: len(re.sub(r"<[^>]+>", "", s))

rows = []
for node in tree.body:
    call = node.value
    iid = call.args[0].value
    for s in call.args[2].elts:
        t = s.elts[0].value
        h = s.elts[1].value
        for i, p in enumerate(re.findall(r"<p>(.*?)</p>", h, re.S)):
            rows.append((iid, t, i, cjk(p), allch(p)))

short_c = [r for r in rows if r[4] < 60]
long_c = [r for r in rows if r[4] > 90]
short_h = [r for r in rows if r[3] < 60]
w("段落总数 %d" % len(rows))
w("按全部字符(去标签): <60 有 %d, >90 有 %d" % (len(short_c), len(long_c)))
w("按纯汉字: <60 有 %d, >90 有 %d" % (len(short_h), len(long_c)))
w("\n全部字符 <60 的段落:")
for r in short_c:
    w("  %s/%s/%d  汉字%d 字符%d" % r)
w("\n全部字符 >90 的段落:")
for r in long_c:
    w("  %s/%s/%d  汉字%d 字符%d" % r)

tot = {}
for node in tree.body:
    call = node.value
    iid = call.args[0].value
    t = 0
    for s in call.args[2].elts:
        for p in re.findall(r"<p>(.*?)</p>", s.elts[1].value, re.S):
            t += cjk(p)
    tot[iid] = t
low = sorted(tot.items(), key=lambda kv: kv[1])
w("\n总汉字 <300 的条目 %d 个:" % len([x for x in tot.values() if x < 300]))
for k, v in low:
    if v < 300:
        w("  %s %d" % (k, v))
w("\n最小值 %s %d  最大值 %s %d" % (low[0][0], low[0][1], low[-1][0], low[-1][1]))
open(OUT, "w", encoding="utf-8").write("\n".join(lines))
print("ok")
