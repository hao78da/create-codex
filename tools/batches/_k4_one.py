import io, re
p = r'D:\frontend\_raw\batches\k4.py'
s = io.open(p, encoding='utf-8').read()
m = re.search(r'item\("create:small_tuff_bricks"', s)
start = m.start()
nxt = re.search(r'\nitem\("', s[start + 5:])
seg = s[start:start + 5 + nxt.start()] if nxt else s[start:]
io.open(r'D:\frontend\_raw\batches\_k4_one.txt', 'w', encoding='utf-8').write(seg)
print(len(seg))
