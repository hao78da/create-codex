# -*- coding: utf-8 -*-
"""批量下载附属模组 jar 到 work/mods_intake/。

用法:
    python _dl_mods.py <slug> [<slug> ...]
    python _dl_mods.py --cf <curseforge-slug> [...]     # 只走 CurseForge
    python _dl_mods.py --mr <modrinth-slug> [...]       # 只走 Modrinth

双源策略（默认）：先 Modrinth，失败再 CurseForge。

Modrinth  : api.modrinth.com/v2/project/<slug>/version
            选 1.20.1 + forge/neoforge 的第一个构建

CurseForge: www.curseforge.com 与 api.curseforge.com 都被 Cloudflare 403，
            但两条旁路可用：
              1) api.cfwidget.com/minecraft/mc-mods/<slug>   取文件清单
              2) edge.forgecdn.net/files/<id//1000>/<id%1000:03d>/<filename>
                                                直链下载（无 UA 校验）

代理：设 MODS_PROXY，例如 set MODS_PROXY=http://127.0.0.1:7890
"""
import json
import os
import sys
import time
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "work", "mods_intake")
os.makedirs(RAW, exist_ok=True)

MR_API = 'https://api.modrinth.com/v2/project/%s/version'
CF_WIDGET = 'https://api.cfwidget.com/minecraft/mc-mods/%s'
CF_CDN = 'https://edge.forgecdn.net/files/%d/%03d/%s'

UA = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120'

_PROXY = os.environ.get('MODS_PROXY', '').strip()
if _PROXY:
    _opener = urllib.request.build_opener(
        urllib.request.ProxyHandler({'http': _PROXY, 'https': _PROXY}))
else:
    _opener = urllib.request.build_opener()
_opener.addheaders = [('User-Agent', UA), ('Accept', '*/*')]


def _open(url, timeout=60):
    return _opener.open(url, timeout=timeout)


# ---------------- Modrinth ----------------

def pick_modrinth(slug):
    """返回 (version, url, filename, size) 或 None"""
    try:
        vs = json.loads(_open(MR_API % slug, 40).read().decode())
    except Exception:
        return None
    for v in vs:
        if '1.20.1' in v.get('game_versions', []) and (
                'forge' in v.get('loaders', []) or 'neoforge' in v.get('loaders', [])):
            f = next((x for x in v['files'] if x['filename'].endswith('.jar')),
                     v['files'][0])
            return (v.get('version_number', '?'), f['url'], f['filename'],
                    f.get('size', 0))
    return None


# ---------------- CurseForge ----------------

def pick_curseforge(slug, retries=3):
    """返回 (version, url, filename, size) 或 None"""
    data = None
    for i in range(retries):
        try:
            r = _open(CF_WIDGET % slug, 40)
            data = json.loads(r.read().decode())
            break
        except Exception as e:
            code = getattr(e, 'code', '')
            if code == 404:
                return None
            if i < retries - 1:
                time.sleep(2 + i * 2)
    if not data:
        return None

    files = data.get('files') or []
    # 优先 1.20.1 + Forge/NeoForge，按上传时间倒序
    hit = [f for f in files
           if '1.20.1' in (f.get('versions') or [])
           and any(x in (f.get('versions') or []) for x in ('Forge', 'NeoForge'))]
    if not hit:
        return None
    hit.sort(key=lambda f: f.get('uploaded_at') or '', reverse=True)
    f = hit[0]
    fid = f['id']
    fn = f['display']
    url = CF_CDN % (fid // 1000, fid % 1000, fn)
    return (f.get('version') or '?', url, fn, f.get('filesize') or 0)


# ---------------- 下载 ----------------

def save(slug, url, dst, expect):
    if os.path.exists(dst) and os.path.getsize(dst) > 0:
        return 'exists', os.path.getsize(dst)
    req = urllib.request.Request(url)
    t0 = time.time()
    try:
        r = _opener.open(req, timeout=120)
        n = 0
        tmp = dst + '.part'
        with open(tmp, 'wb') as fh:
            while True:
                b = fh and r.read(262144)
                if not b:
                    break
                fh.write(b)
                n += len(b)
        if expect and abs(n - expect) > 1024:
            os.remove(tmp)
            return 'size_mismatch(%d!=%d)' % (n, expect), n
        os.replace(tmp, dst)
        dt = max(time.time() - t0, 0.001)
        return 'ok %.0fs %.0fKB/s' % (dt, n / 1024 / dt), n
    except Exception as e:
        for p in (dst + '.part',):
            if os.path.exists(p):
                os.remove(p)
        return 'fail %s' % type(e).__name__, 0


def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        return
    force = None
    if args[0] in ('--cf', '--mr'):
        force = args[0][2:]
        args = args[1:]

    ok, skip, fail = [], [], []
    print('目标 %d 个\n' % len(args), flush=True)

    for i, slug in enumerate(args, 1):
        print('[%d/%d] %s' % (i, len(args), slug), flush=True)
        dst = os.path.join(RAW, slug + '.jar')

        picked = None
        src = None

        if force != 'cf':
            p = pick_modrinth(slug)
            if p:
                picked, src = p, 'Modrinth'

        if not picked and force != 'mr':
            p = pick_curseforge(slug)
            if p:
                picked, src = p, 'CurseForge'
            else:
                time.sleep(1)

        if not picked:
            print('  两个源都没有 1.20.1 Forge 构建', flush=True)
            skip.append(slug)
            print('', flush=True)
            continue

        ver, url, fn, size = picked
        print('  %s  %s  %.1f MB  %s' % (src, ver, size / 1048576, fn[:44]), flush=True)
        st, n = save(slug, url, dst, size)
        print('  -> %s' % st, flush=True)
        if st.startswith('ok') or st == 'exists':
            ok.append(slug)
        else:
            fail.append(slug)
        print('', flush=True)

    print('=' * 62)
    print('成功 %d: %s' % (len(ok), ', '.join(ok) or '-'))
    if skip:
        print('跳过 %d: %s' % (len(skip), ', '.join(skip)))
    if fail:
        print('失败 %d: %s' % (len(fail), ', '.join(fail)))


if __name__ == '__main__':
    main()
