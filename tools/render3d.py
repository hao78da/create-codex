# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""把 Create 的方块模型（JSON 立方体 / OBJ）等距渲染成 PNG 图标。

用法: python render3d.py [item ...]
输出: ROOT\\assets\\icons\\3d_<icon>.png
"""
import json
import math
import os
import sys

import numpy as np
from PIL import Image

# 资源目录（可选）：默认从 work/assets/<名字> 读取，也可用环境变量覆盖。
# 目录不存在时脚本会因缺少模型而报错退出，这属于预期行为——渲染 3D 图标需要有模组资源。
_ASSETS = os.environ.get('CREATE_ASSETS') or os.path.join(WORK, 'assets')
CREATE = os.path.join(_ASSETS, 'create')
MODELS = os.path.join(CREATE, 'models')
TEXDIR = os.path.join(CREATE, 'textures')
CG = os.path.join(_ASSETS, 'creategoggles')
CG_MODELS = os.path.join(CG, 'models')
CG_TEX = os.path.join(CG, 'textures')
CMS = os.path.join(_ASSETS, 'cms')
SWEETS = os.path.join(_ASSETS, 'createsweetsandtreets')
SWEETS_MODELS = os.path.join(SWEETS, 'models')
SWEETS_TEX = os.path.join(SWEETS, 'textures')
SH = os.path.join(_ASSETS, 'superheated')
EI = os.path.join(_ASSETS, 'create_enchantment_industry')
EI_MODELS = os.path.join(EI, 'models')
EI_TEX = os.path.join(EI, 'textures')
SH_MODELS = os.path.join(SH, 'models')
SH_TEX = os.path.join(SH, 'textures')
PROP = os.path.join(_ASSETS, 'createpropulsion')
PROP_MODELS = os.path.join(PROP, 'models')
PROP_TEX = os.path.join(PROP, 'textures')
VAN = os.path.join(_ASSETS, 'minecraft')
VAN_MODELS = os.path.join(VAN, 'models')
VAN_TEX = os.path.join(VAN, 'textures')
ICONS = os.path.join(ROOT, 'assets', 'icons')

SIZE = 96
SS = 2
MARGIN = 0.04


# ---------------------------------------------------------------- 资源加载

def _dyn_tex_roots():
    global _DTEX
    if _DTEX is not None:
        return _DTEX
    _DTEX = [_ASSETS]
    return _DTEX


_DTEX = None


_DYN = None


def _dyn_roots():
    """work/assets/<ns>/models 全部作为查找根（按需要缓存）。"""
    global _DYN
    if _DYN is not None:
        return _DYN
    roots = []
    try:
        for d in sorted(os.listdir(_ASSETS)):
            m = os.path.join(_ASSETS, d, 'models')
            if os.path.isdir(m):
                roots.append(m)
    except Exception:
        pass
    _DYN = roots
    return roots


def _mpath(name):
    """按 work/assets/<ns>/models 动态查找；再退回 Create 本体。"""
    name = name.split(':')[-1] if ':' in name else name
    rel = name.replace('/', os.sep) + '.json'
    for root in _dyn_roots():
        q = os.path.join(root, rel)
        if os.path.exists(q):
            return q
    q = os.path.join(MODELS, rel)
    if os.path.exists(q):
        return q
    return os.path.join(MODELS, rel)


def load_chain(name):
    """返回 (textures, elements, obj_info)。obj_info 为 {'file','flip_v'} 或 None。"""
    chain, seen = [], set()
    cur = name
    while cur:
        p = _mpath(cur)
        if p in seen or not os.path.exists(p):
            break
        seen.add(p)
        with open(p, encoding='utf-8') as f:
            d = json.load(f)
        chain.append(d)
        cur = d.get('parent')
    tex = {}
    for d in reversed(chain):
        tex.update(d.get('textures') or {})
    obj = None
    for d in chain:
        if d.get('loader') == 'forge:obj':
            obj = {'file': d.get('model'), 'flip_v': bool(d.get('flip_v'))}
            break
    elements = []
    for d in chain:
        for ch in (d.get('children') or {}).values():
            te = ch.get('textures') or {}
            if te:
                tex.update(te)
        if d.get('elements'):
            elements.extend(d['elements'])
        for ch in (d.get('children') or {}).values():
            if ch.get('elements'):
                elements.extend(ch['elements'])
    elements = elements or None
    return tex, elements, obj


def _tex_ref(tex, ref, depth=0):
    if depth > 8 or not ref:
        return None
    if ref.startswith('#'):
        return _tex_ref(tex, tex.get(ref[1:]), depth + 1)
    return ref


def tex_path(tex, ref):
    real = _tex_ref(tex, ref)
    if not real:
        return None
    real = real.split(':')[-1] if real.startswith('minecraft:') else real
    if real.startswith('createsweetsandtreets:'):
        q = os.path.join(SWEETS_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')
        return q if os.path.exists(q) else None
    if real.startswith('create_enchantment_industry:'):
        q = os.path.join(EI_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')
        return q if os.path.exists(q) else None
    if real.startswith('superheated:'):
        q = os.path.join(SH_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')
        return q if os.path.exists(q) else None
    if real.startswith('minecraft:') and os.path.exists(os.path.join(VAN_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')):
        return os.path.join(VAN_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')
    if real.startswith('createpropulsion:'):
        q = os.path.join(PROP_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')
        return q if os.path.exists(q) else None
    if real.startswith('cms:'):
        q = os.path.join(CMS_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')
        return q if os.path.exists(q) else None
    if real.startswith('creategoggles:'):
        q = os.path.join(CG_TEX, real.split(':', 1)[1].replace('/', os.sep) + '.png')
        return q if os.path.exists(q) else None
    if real.startswith('create:'):
        p = os.path.join(TEXDIR, real.split(':', 1)[1].replace('/', os.sep) + '.png')
        return p if os.path.exists(p) else None
    # 任意命名空间：work/assets/<ns>/textures/...
    if ':' in real:
        ns, rel = real.split(':', 1)
        for root in _dyn_tex_roots():
            q = os.path.join(root, ns, rel.replace('/', os.sep) + '.png')
            if os.path.exists(q):
                return q
    name = real.split('/')[-1]
    for cand in ('minecraft_' + name + '.png', 'create_' + name + '.png', '3d_' + name + '.png'):
        p = os.path.join(ICONS, cand)
        if os.path.exists(p):
            return p
    return None


_tex_cache = {}


def load_tex(path):
    if path not in _tex_cache:
        im = Image.open(path).convert('RGBA')
        _tex_cache[path] = np.asarray(im, dtype=np.float32) / 255.0
    return _tex_cache[path]


# ---------------------------------------------------------------- 立方体模型

def face_corners(x1, y1, z1, x2, y2, z2):
    return {
        'north': ([(x1, y2, z1), (x2, y2, z1), (x2, y1, z1), (x1, y1, z1)], (0, 0, -1)),
        'south': ([(x2, y2, z2), (x1, y2, z2), (x1, y1, z2), (x2, y1, z2)], (0, 0, 1)),
        'west': ([(x1, y2, z1), (x1, y2, z2), (x1, y1, z2), (x1, y1, z1)], (-1, 0, 0)),
        'east': ([(x2, y2, z2), (x2, y2, z1), (x2, y1, z1), (x2, y1, z2)], (1, 0, 0)),
        'up': ([(x1, y2, z1), (x2, y2, z1), (x2, y2, z2), (x1, y2, z2)], (0, 1, 0)),
        'down': ([(x1, y1, z2), (x2, y1, z2), (x2, y1, z1), (x1, y1, z1)], (0, -1, 0)),
    }


def rot_point(p, rot):
    if not rot or not rot.get('angle'):
        return p
    ang = math.radians(rot['angle'])
    ox, oy, oz = rot.get('origin', [8, 8, 8])
    x, y, z = p[0] - ox, p[1] - oy, p[2] - oz
    c, s = math.cos(ang), math.sin(ang)
    ax = rot.get('axis', 'y')
    if ax == 'y':
        x, z = x * c + z * s, -x * s + z * c
    elif ax == 'x':
        y, z = y * c - z * s, y * s + z * c
    else:
        x, y = x * c - y * s, x * s + y * c
    return (x + ox, y + oy, z + oz)


SHADE_N = {
    (0, 1, 0): 1.00, (0, -1, 0): 0.50,
    (0, 0, 1): 0.82, (0, 0, -1): 0.82,
    (1, 0, 0): 0.66, (-1, 0, 0): 0.66,
}


def cuboid_tris(elements, tex, missing):
    tris = []
    for el in elements:
        fx, fy, fz = el['from']
        tx, ty, tz = el['to']
        rot = el.get('rotation')
        for name, (corners, nrm) in face_corners(fx, fy, fz, tx, ty, tz).items():
            f = (el.get('faces') or {}).get(name)
            if not f:
                continue
            path = tex_path(tex, f.get('texture'))
            if not path:
                missing.add(f.get('texture') or '?')
                continue
            u1, v1, u2, v2 = f.get('uv', [0, 0, 16, 16])
            r = int(f.get('rotation', 0)) % 360
            base = [(0, 0), (1, 0), (1, 1), (0, 1)]
            uvs = []
            for a, b in base:
                if r:
                    ang = math.radians(-r)
                    aa, bb = a - .5, b - .5
                    a, b = aa * math.cos(ang) - bb * math.sin(ang) + .5, aa * math.sin(ang) + bb * math.cos(ang) + .5
                uvs.append(((u1 + (u2 - u1) * a) / 16.0, (v1 + (v2 - v1) * b) / 16.0))
            pts = [rot_point(p, rot) for p in corners]
            t = load_tex(path)
            sh = SHADE_N[nrm]
            for i in (0, 1, 2):
                tris.append(([pts[0], pts[1], pts[2]], [uvs[0], uvs[1], uvs[2]], sh, t))
            tris.append(([pts[0], pts[2], pts[3]], [uvs[0], uvs[2], uvs[3]], sh, t))
    return tris


# ---------------------------------------------------------------- OBJ 模型

def parse_obj(objfile, tex, flip_v):
    base = os.path.dirname(objfile)
    mtl = {}
    for fn in os.listdir(base):
        if fn.endswith('.mtl') and fn.replace('.mtl', '') in os.path.basename(objfile):
            for line in open(os.path.join(base, fn), encoding='utf-8', errors='ignore'):
                p = line.split()
                if len(p) >= 2 and p[0] == 'newmtl':
                    cur = p[1]
                elif len(p) >= 2 and p[0] == 'map_Kd' and 'cur' in dir():
                    pass
    # 简化：用 mlt 文件名匹配不到就直接按材质名找
    cur = None
    for line in open(objfile, encoding='utf-8', errors='ignore'):
        p = line.split()
        if not p:
            continue
        if p[0] == 'mtllib' and len(p) > 1:
            mf = os.path.join(base, p[1])
            if os.path.exists(mf):
                cm = None
                for l2 in open(mf, encoding='utf-8', errors='ignore'):
                    q = l2.split()
                    if len(q) >= 2 and q[0] == 'newmtl':
                        cm = q[1]
                        mtl[cm] = None
                    elif len(q) >= 2 and q[0] == 'map_Kd' and cm:
                        mtl[cm] = q[1]
    vs, vts, tris = [], [], []
    cur = None
    missing = set()
    for line in open(objfile, encoding='utf-8', errors='ignore'):
        p = line.split()
        if not p:
            continue
        if p[0] == 'v':
            vs.append((float(p[1]) * 16, float(p[2]) * 16, float(p[3]) * 16))
        elif p[0] == 'vt':
            u, v = float(p[1]), float(p[2])
            vts.append((u, 1.0 - v if flip_v else v))
        elif p[0] == 'usemtl':
            cur = p[1] if len(p) > 1 else None
        elif p[0] == 'f':
            idx = []
            for tok in p[1:]:
                parts = tok.split('/')
                vi = int(parts[0]) - 1
                ti = int(parts[1]) - 1 if len(parts) > 1 and parts[1] else vi
                idx.append((vi, ti))
            path = tex_path(tex, mtl.get(cur) if cur else None)
            if not path:
                missing.add(cur)
                continue
            t = load_tex(path)
            for k in range(1, len(idx) - 1):
                a, b, c = idx[0], idx[k], idx[k + 1]
                pts = [vs[a[0]], vs[b[0]], vs[c[0]]]
                uv = [vts[a[1]] if a[1] < len(vts) else (0, 0),
                      vts[b[1]] if b[1] < len(vts) else (0, 0),
                      vts[c[1]] if c[1] < len(vts) else (0, 0)]
                n = np.cross(np.array(pts[1]) - pts[0], np.array(pts[2]) - pts[0])
                ln = np.linalg.norm(n)
                sh = 0.8
                if ln > 1e-9:
                    n /= ln
                    ax = int(np.argmax(np.abs(n)))
                    key = [(0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1), (1, 0, 0), (-1, 0, 0)]
                    nn = (round(n[0]), round(n[1]), round(n[2]))
                    best = max(key, key=lambda kk: abs(np.dot(kk, nn)))
                    sh = SHADE_N.get(best, 0.8)
                tris.append((pts, uv, sh, t))
    return tris, missing


# ---------------------------------------------------------------- 相机 / 光栅

def camera():
    az, el = math.radians(45), math.radians(30)
    d = np.array([math.cos(el) * math.cos(az), math.sin(el), math.cos(el) * math.sin(az)])
    right = np.cross([0, 1, 0], d)
    right /= np.linalg.norm(right)
    up = np.cross(d, right)
    return np.stack([right, up, d])


def raster(canvas, zbuf, P, UV, Z, tex, shade):
    (x0, y0), (x1, y1), (x2, y2) = P
    minx, maxx = max(0, int(min(x0, x1, x2))), min(canvas.shape[1] - 1, int(max(x0, x1, x2)) + 1)
    miny, maxy = max(0, int(min(y0, y1, y2))), min(canvas.shape[0] - 1, int(max(y0, y1, y2)) + 1)
    if minx > maxx or miny > maxy:
        return
    xs, ys = np.meshgrid(np.arange(minx, maxx + 1), np.arange(miny, maxy + 1))
    den = (y1 - y2) * (x0 - x2) + (x2 - x1) * (y0 - y2)
    if abs(den) < 1e-9:
        return
    w0 = ((y1 - y2) * (xs - x2) + (x2 - x1) * (ys - y2)) / den
    w1 = ((y2 - y0) * (xs - x2) + (x0 - x2) * (ys - y2)) / den
    w2 = 1 - w0 - w1
    inside = (w0 >= -1e-6) & (w1 >= -1e-6) & (w2 >= -1e-6)
    if not inside.any():
        return
    u = w0 * UV[0][0] + w1 * UV[1][0] + w2 * UV[2][0]
    v = w0 * UV[0][1] + w1 * UV[1][1] + w2 * UV[2][1]
    z = w0 * Z[0] + w1 * Z[1] + w2 * Z[2]
    h, w = tex.shape[:2]
    ix = np.clip((u * (w - 1)).round().astype(int), 0, w - 1)
    iy = np.clip((v * (h - 1)).round().astype(int), 0, h - 1)
    px = tex[iy, ix]
    mask = inside & (px[..., 3] > 0.35) & (z > zbuf[ys, xs])
    if not mask.any():
        return
    canvas[ys[mask], xs[mask], :3] = px[mask][:, :3] * shade
    canvas[ys[mask], xs[mask], 3] = 1.0
    zbuf[ys[mask], xs[mask]] = z[mask]



def _geo_for(name, tex):
    """按模型名合成几何。返回 elements 列表或 None。"""
    nm = str(name).lower()

    def box(x0, y0, z0, x1, y1, z1, face=None):
        f = face or {}
        d = {'down': f.get('down', '#down'), 'up': f.get('up', '#up'),
             'north': f.get('north', '#north'), 'south': f.get('south', '#south'),
             'east': f.get('east', '#east'), 'west': f.get('west', '#west')}
        return {'from': [x0, y0, z0], 'to': [x1, y1, z1], 'faces': {k: {'texture': v} for k, v in d.items()}}

    side = '#side' if 'side' in tex else ('#all' if 'all' in tex else ('#particle' if 'particle' in tex else '#all'))
    top = '#top' if 'top' in tex else side
    bot = '#bottom' if 'bottom' in tex else side
    base = {'down': bot, 'up': top, 'north': side, 'south': side, 'east': side, 'west': side}

    if 'chest' in nm or 'barrel' in nm:
        # 手工盒体：箱身 14x14x14（去掉 1px 边）
        body = box(1, 0, 1, 15, 14, 15, base)
        lid = box(1, 14, 1, 15, 15, 15, dict(base, up=top))
        return [body, lid]
    if 'slab' in nm:
        return [box(0, 0, 0, 16, 8, 16, base)]
    if 'button' in nm:
        return [box(5, 0, 6, 11, 2, 10, base)]
    if 'carpet' in nm:
        return [box(0, 0, 0, 16, 1, 16, base)]
    if 'pane' in nm:
        return [box(7, 0, 0, 9, 16, 16, base)]
    if 'fence' in nm:
        return [box(6, 0, 6, 10, 16, 10, base)]
    if 'wall' in nm:
        return [box(4, 0, 4, 12, 16, 12, base)]
    return None


def render(model_name, extra_tex=None):
    if isinstance(model_name, (list, tuple)):
        tex, elements, obj = {}, [], None
        for one in model_name:
            t2, e2, o2 = load_chain(one)
            tex.update(t2)
            elements = (elements or []) + (e2 or [])
            obj = obj or o2
    else:
        tex, elements, obj = load_chain(model_name)
    if extra_tex:
        tex = dict(tex)
        tex.update(extra_tex)
    if not elements and not obj and not tex:
        _b = str(model_name).split('/')[-1]
        tex = {'all': 'block/' + _b, 'side': 'block/' + _b, 'top': 'block/' + _b,
               'bottom': 'block/' + _b, 'particle': 'block/' + _b}
    if not elements and not obj and _geo_for(model_name, tex):
        elements = _geo_for(model_name, tex)
    if not elements and not obj and 'stairs' in str(model_name) and tex:
        # _synth_stairs: 下半台阶 + 上半后半台阶
        _side = '#side' if 'side' in tex else ('#all' if 'all' in tex else '#particle')
        _top = '#top' if 'top' in tex else _side
        _bot = '#bottom' if 'bottom' in tex else _side
        elements = [
            {'from': [0, 0, 0], 'to': [16, 8, 16],
             'faces': {'down': {'texture': _bot}, 'up': {'texture': _top},
                       'north': {'texture': _side}, 'south': {'texture': _side},
                       'east': {'texture': _side}, 'west': {'texture': _side}}},
            {'from': [0, 8, 8], 'to': [16, 16, 16],
             'faces': {'down': {'texture': _bot}, 'up': {'texture': _top},
                       'north': {'texture': _side}, 'south': {'texture': _side},
                       'east': {'texture': _side}, 'west': {'texture': _side}}},
        ]
    if not elements and not obj and tex:
        # 父模型是原版 block/cube* 之类、本地找不到时，用贴图合成一个立方体
        _keys = [k for k in ('down', 'up', 'north', 'south', 'east', 'west') if k in tex]
        if _keys:
            elements = [{'from': [0, 0, 0], 'to': [16, 16, 16],
                         'faces': {k: {'texture': '#' + k} for k in _keys}}]
    missing = set()
    if obj:
        f = obj['file'].split(':')[-1]
        tris, missing = parse_obj(os.path.join(CREATE, f.replace('/', os.sep)), tex, obj['flip_v'])
    else:
        tris = cuboid_tris(elements, tex, missing) if elements else []
    if not tris:
        return None, 'no-tris'

    R = camera()
    allp = np.array([p for t in tris for p in t[0]], dtype=np.float64)
    ctr = (allp.max(0) + allp.min(0)) / 2.0
    view_all = (allp - ctr) @ R.T
    sx, sy = view_all[:, 0], -view_all[:, 1]
    span = max(sx.max() - sx.min(), sy.max() - sy.min(), 1e-6)
    S = SIZE * SS
    scale = (S * (1 - 2 * MARGIN)) / span
    ox = S / 2 - (sx.max() + sx.min()) / 2 * scale
    oy = S / 2 - (sy.max() + sy.min()) / 2 * scale

    canvas = np.zeros((S, S, 4), dtype=np.float32)
    zbuf = np.full((S, S), -1e9, dtype=np.float64)

    proj = []
    for pts, uv, sh, t in tris:
        vp = (np.array(pts) - ctr) @ R.T
        pp = [(ox + vp[j, 0] * scale, oy - vp[j, 1] * scale) for j in range(3)]
        proj.append((float(vp[:, 2].mean()), pp, uv, vp[:, 2], sh, t))
    proj.sort(key=lambda q: q[0])
    for _, pp, uv, zz, sh, t in proj:
        raster(canvas, zbuf, pp, uv, zz, t, sh)

    im = Image.fromarray((canvas * 255).astype(np.uint8), 'RGBA').resize((SIZE, SIZE), Image.LANCZOS)
    bbox = im.getbbox()
    if bbox:
        im = im.crop(bbox)
        pad = int(max(im.size) * 0.06)
        out = Image.new('RGBA', (max(im.size) + 2 * pad,) * 2, (0, 0, 0, 0))
        out.paste(im, ((out.size[0] - im.size[0]) // 2, (out.size[1] - im.size[1]) // 2))
        im = out
    return im, sorted(str(m) for m in missing)


JOBS = {
    'shaft': ('block/shaft', None),
    'powered_shaft': (['block/shaft', 'block/powered_shaft'], None),
    'cogwheel': ('block/cogwheel', None),
    'large_cogwheel': ('block/large_cogwheel', None),
    'gearbox': ('block/gearbox/item', None),
    'vertical_gearbox': ('block/gearbox/item_vertical', None),
    'gearshift': ('block/gearshift/item', None),
    'sequenced_gearshift': ('block/sequenced_gearshift/item', None),
    'hand_crank': ('block/hand_crank/item', None),
    'clutch': ('block/clutch/item', None),
    'steam_engine': ('block/steam_engine/item', None),
    'creative_motor': ('block/creative_motor/item', None),
    'encased_chain_drive': ('block/encased_chain_drive/item', None),
    'water_wheel': ('block/water_wheel/item', None),
    'large_water_wheel': ('block/large_water_wheel/item', None),
    'flywheel': ('block/flywheel/item', None),
    'rotation_speed_controller': ('block/rotation_speed_controller/item', None),
    'andesite_encased_shaft': ('block/encased_shaft/item_andesite', None),
    'brass_encased_shaft': ('block/encased_shaft/item_brass', None),
    'andesite_encased_cogwheel': ('block/encased_cogwheel/item', None),
    'brass_encased_cogwheel': ('block/encased_cogwheel/item',
                               {'casing': 'create:block/brass_casing',
                                'side': 'create:block/brass_encased_cogwheel_side'}),
    'andesite_encased_large_cogwheel': ('block/encased_large_cogwheel/item', None),
    'brass_encased_large_cogwheel': ('block/encased_large_cogwheel/item',
                                     {'casing': 'create:block/brass_casing',
                                      'side': 'create:block/brass_encased_cogwheel_side_connected'}),
}


def main():
    args = sys.argv[1:]
    if args and args[0] == '--jobs':
        jf = json.load(open(args[1], encoding='utf-8'))
        only = set(args[2:]) or None
        ok, skip = 0, []
        for short, spec in jf.items():
            if only and short not in only:
                continue
            mdl = spec['mdl']
            im, miss = render(mdl, spec.get('extra'))
            if im is None:
                skip.append((short, miss))
                continue
            im.save(os.path.join(ICONS, '3d_create_%s.png' % short))
            ok += 1
            if miss:
                print('WARN', short, 'missing:', ','.join(miss)[:200])
        print('rendered', ok, 'skipped', len(skip))
        for s, m in skip:
            print('SKIP', s, m)
        return
    only = args or None
    ok = 0
    for short, (mdl, extra) in JOBS.items():
        if only and short not in only:
            continue
        im, miss = render(mdl, extra)
        if im is None:
            print('SKIP', short, miss)
            continue
        im.save(os.path.join(ICONS, '3d_create_%s.png' % short))
        ok += 1
        print('OK  ', short, im.size, ('missing: %s' % miss) if miss else '')
    print('rendered', ok)


if __name__ == '__main__':
    main()
