# -*- coding: utf-8 -*-
"""生成 tools/data/vanilla_tags.json —— Forge 1.20.1 常见物品标签的成员表。

背景：上游仓库没有提交 tools/data/vanilla_tags.json（作者原本放在
D:\\frontend\\_raw\\out\\ 下）。缺了它 gen_site.py 的标签解析会静默跳过，
导致 forge:* 标签解析不出成员、图标退化成 _unknown.png。

本脚本按 Forge 1.20.1 的标签定义生成成员表，成员只收录站点实际存在的物品
（data.json 的 items + vanilla），确保 tag_icon() 能解析出真实图标。

用法：python _gen_vanilla_tags.py
输出：tools/data/vanilla_tags.json
"""
import io
import json
import os

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA = os.path.dirname(os.path.abspath(__file__))

_d = json.load(io.open(os.path.join(DATA, "data.json"), encoding="utf-8"))
_items = _d.get("items") or {}
_vanilla = _d.get("vanilla") or {}
KNOWN = set(_items) | set(_vanilla)

# ---- Forge 1.20.1 标签定义（只列站点用到的 + 常见配套）----
# 值里可以用 "create:xxx" / "minecraft:xxx"，不存在的会被过滤掉。

_COLORS = ['white', 'orange', 'magenta', 'light_blue', 'yellow', 'lime',
           'pink', 'gray', 'light_gray', 'cyan', 'purple', 'blue',
           'brown', 'green', 'red', 'black']

TAGS = {}

# 染料
for c in _COLORS:
    TAGS['forge:dyes/' + c] = ['minecraft:%s_dye' % c]

# 粒
TAGS['forge:nuggets/iron'] = ['minecraft:iron_nugget']
TAGS['forge:nuggets/gold'] = ['minecraft:gold_nugget']
TAGS['forge:nuggets/zinc'] = ['create:zinc_nugget']
TAGS['forge:nuggets/copper'] = ['create:copper_nugget']
TAGS['forge:nuggets/brass'] = ['create:brass_nugget']

# 锭
TAGS['forge:ingots/iron'] = ['minecraft:iron_ingot']
TAGS['forge:ingots/gold'] = ['minecraft:gold_ingot']
TAGS['forge:ingots/copper'] = ['minecraft:copper_ingot']
TAGS['forge:ingots/zinc'] = ['create:zinc_ingot']
TAGS['forge:ingots/brass'] = ['create:brass_ingot']

# 板
TAGS['forge:plates/iron'] = ['create:iron_sheet']
TAGS['forge:plates/gold'] = ['create:golden_sheet']
TAGS['forge:plates/copper'] = ['create:copper_sheet']
TAGS['forge:plates/brass'] = ['create:brass_sheet']
TAGS['forge:plates/obsidian'] = ['create:sturdy_sheet']

# 宝石
TAGS['forge:gems/quartz'] = ['minecraft:quartz']
TAGS['forge:gems/diamond'] = ['minecraft:diamond']
TAGS['forge:gems/emerald'] = ['minecraft:emerald']
TAGS['forge:gems/lapis'] = ['minecraft:lapis_lazuli']
TAGS['forge:gems/amethyst'] = ['minecraft:amethyst_shard']

# 粉末
TAGS['forge:dusts/redstone'] = ['minecraft:redstone']
TAGS['forge:dusts/glowstone'] = ['minecraft:glowstone_dust']
TAGS['forge:dusts/gunpowder'] = ['minecraft:gunpowder']
TAGS['forge:dusts/sugar'] = ['minecraft:sugar']

# 原矿 / 原矿块
for m in ['iron', 'gold', 'copper', 'zinc']:
    TAGS['forge:raw_materials/' + m] = [
        'minecraft:raw_%s' % m if m in ('iron', 'gold', 'copper') else 'create:raw_zinc'
    ]
    TAGS['forge:storage_blocks/raw_' + m] = [
        'minecraft:raw_%s_block' % m if m in ('iron', 'gold', 'copper') else 'create:raw_zinc_block'
    ]

# 储存块
TAGS['forge:storage_blocks/iron'] = ['minecraft:iron_block']
TAGS['forge:storage_blocks/gold'] = ['minecraft:gold_block']
TAGS['forge:storage_blocks/copper'] = ['minecraft:copper_block']
TAGS['forge:storage_blocks/zinc'] = ['create:zinc_block']
TAGS['forge:storage_blocks/brass'] = ['create:brass_block']

# 矿石
TAGS['forge:ores/zinc'] = ['create:zinc_ore', 'create:deepslate_zinc_ore']
TAGS['forge:ores/iron'] = ['minecraft:iron_ore', 'minecraft:deepslate_iron_ore']
TAGS['forge:ores/gold'] = ['minecraft:gold_ore', 'minecraft:deepslate_gold_ore']
TAGS['forge:ores/copper'] = ['minecraft:copper_ore', 'minecraft:deepslate_copper_ore']
TAGS['forge:ores/coal'] = ['minecraft:coal_ore', 'minecraft:deepslate_coal_ore']
TAGS['forge:ores/diamond'] = ['minecraft:diamond_ore', 'minecraft:deepslate_diamond_ore']
TAGS['forge:ores/redstone'] = ['minecraft:redstone_ore', 'minecraft:deepslate_redstone_ore']
TAGS['forge:ores/lapis'] = ['minecraft:lapis_ore', 'minecraft:deepslate_lapis_ore']
TAGS['forge:ores/emerald'] = ['minecraft:emerald_ore', 'minecraft:deepslate_emerald_ore']

# 玻璃
TAGS['forge:glass/colorless'] = ['minecraft:glass']
TAGS['forge:glass_panes/colorless'] = ['minecraft:glass_pane']
for c in _COLORS:
    TAGS['forge:glass/' + c] = ['minecraft:%s_stained_glass' % c]
    TAGS['forge:glass_panes/' + c] = ['minecraft:%s_stained_glass_pane' % c]

# 沙
TAGS['forge:sand/colorless'] = ['minecraft:sand']
TAGS['forge:sand/red'] = ['minecraft:red_sand']

# 杂项
TAGS['forge:string'] = ['minecraft:string']
TAGS['forge:eggs'] = ['minecraft:egg']
TAGS['forge:feathers'] = ['minecraft:feather']
TAGS['forge:leather'] = ['minecraft:leather']
TAGS['forge:slimeballs'] = ['minecraft:slime_ball']
TAGS['forge:bones'] = ['minecraft:bone']

# 木材 / 原木
TAGS['forge:stripped_logs'] = ['minecraft:stripped_oak_log']
TAGS['forge:stripped_wood'] = ['minecraft:stripped_oak_wood']
TAGS['forge:rods/wooden'] = ['minecraft:stick']

# 粮食（用于 Create 的面粉链）
TAGS['forge:flour/wheat'] = ['create:wheat_flour']
TAGS['forge:crops/wheat'] = ['minecraft:wheat']
TAGS['forge:seeds'] = ['minecraft:wheat_seeds']

# 箱子
TAGS['forge:chests/wooden'] = ['minecraft:chest', 'minecraft:trapped_chest']
TAGS['forge:chests'] = ['minecraft:chest', 'minecraft:trapped_chest']

# 其它常见 ore 变体（本站数据里出现但可能没有对应物品，保留定义供解析）
for m in ['aluminum', 'lead', 'nickel', 'osmium', 'platinum', 'quicksilver',
          'silver', 'tin', 'uranium', 'ametrine', 'anthracite', 'emeraldite', 'lignite']:
    TAGS.setdefault('forge:ores/' + m, [])
    TAGS.setdefault('forge:raw_materials/' + m, [])
    TAGS.setdefault('forge:storage_blocks/raw_' + m, [])


def _filter(vals):
    """只保留站点实际存在的物品 id。"""
    out = []
    for v in vals:
        if isinstance(v, str) and not v.startswith('#') and v in KNOWN:
            out.append(v)
    return sorted(set(out))


# ---- Create 本体模板标签：从 data.json 的物品 id 反推 ----
_CREATE_TAGS = {}

# 颜色座椅
_CREATE_TAGS['create:seats'] = sorted(k for k in _items if k.endswith('_seat'))
# 邮箱
_CREATE_TAGS['create:postboxes'] = sorted(k for k in _items if k.endswith('_postbox'))
# 阀门手轮
_CREATE_TAGS['create:valve_handles'] = sorted(k for k in _items if k.endswith('_valve_handle'))
# 桌布
_CREATE_TAGS['create:dyed_table_cloths'] = sorted(
    k for k in _items if k.endswith('_table_cloth'))
# 可打浆（pulpifiable）：Create 里能被粉碎成纸浆的作物类
_CREATE_TAGS['create:pulpifiable'] = sorted(
    k for k in _items
    if any(x in k for x in ('sugar_cane', 'cactus', 'kelp', 'bamboo'))
    or k in ('minecraft:sugar_cane', 'minecraft:cactus', 'minecraft:kelp', 'minecraft:bamboo'))
# 石料类型：每种石头及其变体
for _st in ('andesite', 'asurine', 'calcite', 'crimsite', 'deepslate', 'diorite',
            'dripstone', 'granite', 'limestone', 'ochrum', 'scorchia', 'scoria',
            'tuff', 'veridium'):
    _mem = sorted(k for k in _items if _st in k)
    if _mem:
        _CREATE_TAGS['create:stone_types/' + _st] = _mem

for _t, _m in _CREATE_TAGS.items():
    if _m:
        TAGS[_t] = _m


result = {}
skipped = []
for tag, vals in TAGS.items():
    kept = _filter(vals)
    if kept:
        result[tag] = kept
    else:
        skipped.append(tag)

out_path = os.path.join(DATA, "vanilla_tags.json")
with io.open(out_path, "w", encoding="utf-8") as f:
    f.write("{\n")
    keys = sorted(result)
    for i, k in enumerate(keys):
        comma = "," if i < len(keys) - 1 else ""
        f.write('  %s: %s%s\n' % (json.dumps(k, ensure_ascii=False),
                                  json.dumps(result[k], ensure_ascii=False), comma))
    f.write("}\n")

print("写入:", out_path)
print("标签总数:", len(TAGS), "| 有成员:", len(result), "| 空置跳过:", len(skipped))
print()
print("空置标签（本站没有对应物品，已跳过）:")
for s in skipped:
    print("  ", s)
