import io

PATH = r'D:\frontend\_raw\batches\k4.py'


def apply(adds):
    text = open(PATH, encoding='utf-8').read()
    n = 0
    for iid, lst in adds.items():
        start = text.index('item("create:%s"' % iid)
        nxt = text.find('\nitem(', start)
        end = len(text) if nxt == -1 else nxt
        seg = text[start:end]
        parts = seg.split('</p>')
        if len(parts) < 7:
            raise SystemExit('段落数不足: %s %d' % (iid, len(parts)))
        if len(lst) != 6:
            raise SystemExit('追加条数不是 6: %s %d' % (iid, len(lst)))
        for i, add in enumerate(lst):
            if add:
                parts[i] = parts[i].rstrip() + add
                n += 1
        text = text[:start] + '</p>'.join(parts) + text[end:]
    open(PATH, 'w', encoding='utf-8', newline='\n').write(text)
    print('patched', n)
