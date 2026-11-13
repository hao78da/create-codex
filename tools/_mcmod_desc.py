# -*- coding: utf-8 -*-
"""从 mcmod class 页抓中文简介，输出 _mcmod_desc.json。

mcmod 每个模组页面（/class/<id>.html）都有「简介」区块，
通常在 <div class="class-detail"> 或 <div class="common-text"> 里。
"""
import io
import json
import os
import re
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

_PROXY = os.environ.get('MODS_PROXY', '').strip()
if _PROXY:
    _op = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': _PROXY, 'https': _PROXY}))
else:
    _op = urllib.request.build_opener()
_op.addheaders = [('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120'),
                  ('Accept', 'text/html')]


def fetch(cid):
    url = 'https://www.mcmod.cn/class/%s.html' % cid
    with _op.open(url, timeout=40) as r:
        return r.read().decode('utf-8', 'replace')


BAD_WORDS = ('MC百科', 'ICP备', '公网安备', '版权所有', 'Copyright',
             'jQuery', 'function(', '浏览器', '切换电脑版', 'BY-NC-SA',
             '开放公共编辑', '登录', 'cookie', '举报', '编辑次数')


def good(t):
    """判断这段文字是否像模组简介。"""
    if not t or len(t) < 18:
        return False
    if any(w in t for w in BAD_WORDS):
        return False
    # 纯符号或纯英文短句过滤
    cn = len(re.findall(r'[\u4e00-\u9fff]', t))
    if cn < 6:
        return False
    return True


def extract_summary(html):
    """从 mcmod 页面抽取简介文本：取第一个像样的 <p>。"""
    for m in re.finditer(r'<p[^>]*>(.*?)</p>', html, re.S):
        t = clean_block(m.group(1))
        if good(t):
            return t
    # 退化：从正文 div 里找
    for m in re.finditer(r'<div[^>]*class="[^"]*(?:content|detail)[^"]*"[^>]*>(.*?)</div>', html, re.S):
        t = clean_block(m.group(1))
        if good(t):
            return t
    return ''


def clean_block(h):
    t = re.sub(r'<script.*?</script>', ' ', h, flags=re.S)
    t = re.sub(r'<style.*?</style>', ' ', t, flags=re.S)
    t = re.sub(r'<br\s*/?>', ' ', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = t.replace('&nbsp;', ' ').replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    t = t.replace('&quot;', '"').replace('&#39;', "'")
    t = re.sub(r'\s+', ' ', t).strip()
    return t


def main():
    src = None
    for name in ('_mcmod_en.json', '_mcmod_addons_1201.json'):
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            src = json.load(io.open(p, encoding='utf-8'))
            print('数据源:', name, len(src), '条')
            break
    if not src:
        print('找不到 mcmod 清单')
        return

    # 只抓还没抓到简介的
    outp = os.path.join(ROOT, '_mcmod_desc.json')
    out = {}
    if os.path.exists(outp):
        out = json.load(io.open(outp, encoding='utf-8'))
        print('已有', len(out), '条')

    todo = [x for x in src if x['id'] not in out]
    print('待抓', len(todo), '条\n', flush=True)

    ok = 0
    for i, it in enumerate(todo, 1):
        cid = it['id']
        try:
            html = fetch(cid)
            s = extract_summary(html)
        except Exception as e:
            s = ''
            print('[%d/%d] %-8s 抓取失败 %s' % (i, len(todo), cid, type(e).__name__), flush=True)
            time.sleep(1.5)
            continue
        if s:
            out[cid] = s
            ok += 1
            print('[%d/%d] %-8s %s' % (i, len(todo), cid, s[:60]), flush=True)
        else:
            print('[%d/%d] %-8s 无简介' % (i, len(todo), cid), flush=True)
        time.sleep(0.9)

        # 每 20 条存一次，防中断丢数据
        if i % 20 == 0:
            json.dump(out, io.open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

    json.dump(out, io.open(outp, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('\n抓到 %d 条，累计 %d' % (ok, len(out)))
    print('输出:', outp)


if __name__ == '__main__':
    main()
