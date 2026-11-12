import io, re
p = r'D:\frontend\_raw\batches\k4.py'
s = io.open(p, encoding='utf-8').read().splitlines()
out = []
for i, l in enumerate(s):
    if l.startswith('item('):
        out.append('%d\t%s' % (i + 1, l.split('"')[1]))
io.open(r'D:\frontend\_raw\batches\_k4_lines.txt', 'w', encoding='utf-8').write('\n'.join(out))
print(len(out))
