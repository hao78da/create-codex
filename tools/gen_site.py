# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""Generate the static Create codex site."""
import json, os, re, html, shutil, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import content

OUT = _os.path.join(ROOT, 'tools', 'data')
SITE = ROOT
ICONS = os.path.join(SITE, "assets", "icons")
PAGES = os.path.join(SITE, "items")

data = json.load(open(os.path.join(OUT, "data.json"), encoding="utf-8"))
items = data["items"]
vanilla = data["vanilla"]
ponder = data["ponder"]

# ------------------------------------------------------------------ category
CAT_ORDER = [c[0] for c in content.CATEGORIES] + ["misc"]
CAT_NAME = {c[0]: c[1] for c in content.CATEGORIES}
CAT_NAME["misc"] = "杂项"

def S(s):
    return set(s.split())

EXPLICIT = {
    "power": S("""shaft cogwheel large_cogwheel gearbox vertical_gearbox clutch gearshift
        adjustable_chain_gearshift sequenced_gearshift encased_chain_drive rotation_speed_controller
        hand_crank water_wheel large_water_wheel windmill_bearing steam_engine flywheel creative_motor
        powered_shaft andesite_encased_shaft brass_encased_shaft andesite_encased_cogwheel
        brass_encased_cogwheel andesite_encased_large_cogwheel brass_encased_large_cogwheel
        metal_girder_encased_shaft"""),
    "machine": S("""mechanical_press mechanical_mixer millstone crushing_wheel crushing_wheel_controller
        mechanical_saw mechanical_drill mechanical_harvester mechanical_plough mechanical_roller deployer
        mechanical_arm mechanical_piston mechanical_piston_head sticky_mechanical_piston
        piston_extension_pole gantry_carriage gantry_shaft rope_pulley elevator_pulley hose_pulley
        pulley_magnet propeller mechanical_pump spout item_drain basin blaze_burner empty_blaze_burner
        lit_blaze_burner encased_fan mechanical_crafter crafter_slot_cover turntable"""),
    "logistics": S("""belt belt_connector andesite_funnel brass_funnel andesite_belt_funnel brass_belt_funnel
        andesite_tunnel brass_tunnel chute smart_chute depot item_hatch item_vault stockpile_switch
        stock_link stock_ticker packager repackager package rare_package package_filter package_frogport
        fluid_pipe smart_fluid_pipe glass_fluid_pipe encased_fluid_pipe fluid_tank fluid_valve toolbox
        creative_crate creative_fluid_tank weighted_ejector portable_storage_interface
        portable_fluid_interface factory_gauge"""),
    "train": S("""track fake_track incomplete_track track_station track_signal track_observer train_door
        train_trapdoor small_bogey large_bogey cart_assembler minecart_anchor minecart_contraption
        minecart_coupling chest_minecart_contraption furnace_minecart_contraption controls
        lectern_controller linked_controller controller_rail schedule"""),
    "material": S("""andesite_alloy andesite_alloy_block brass_ingot brass_nugget brass_sheet brass_block
        copper_sheet copper_nugget zinc_ingot zinc_nugget zinc_block zinc_ore deepslate_zinc_ore
        raw_zinc raw_zinc_block iron_sheet golden_sheet sturdy_sheet rose_quartz polished_rose_quartz
        refined_radiance shadow_steel experience_nugget experience_block powdered_obsidian cinder_flour
        wheat_flour dough pulp cardboard cardboard_block chocolate honey chocolate_bucket honey_bucket
        precision_mechanism electron_tube unprocessed_obsidian_sheet red_sand_paper sand_paper
        tree_fertilizer sweet_roll chocolate_glazed_berries honeyed_apple builders_tea blaze_cake
        creative_blaze_cake"""),
    "redstone": S("""analog_lever redstone_contact redstone_link transmitter powered_latch
        powered_toggle_latch pulse_extender pulse_repeater pulse_timer content_observer
        attribute_filter filter display_link display_board nixie_tube placard speedometer stressometer
        desk_bell haunted_bell peculiar_bell cuckoo_clock mysterious_cuckoo_clock elevator_contact
        redstone_requester wand_of_symmetry"""),
    "tool": S("""wrench goggles super_glue sticker schematic schematic_and_quill empty_schematic
        schematic_table schematicannon clipboard shopping_list crafting_blueprint cardboard_boots
        cardboard_chestplate cardboard_helmet cardboard_leggings cardboard_sword copper_diving_boots
        copper_diving_helmet netherite_diving_boots netherite_diving_helmet copper_backtank
        netherite_backtank copper_backtank_placeable netherite_backtank_placeable extendo_grip
        potato_cannon whisk bar_of_chocolate handheld_worldshaper"""),
    "contraption": S("""mechanical_bearing clockwork_bearing linear_chassis secondary_linear_chassis
        radial_chassis sail_frame water_wheel_structure"""),
}
for iid, name in items.items():
    short = iid.split(":", 1)[1]
    if short.startswith("crushed_raw_"):
        EXPLICIT["material"].add(short)

def categorize(iid):
    short = iid.split(":", 1)[1]
    for cat, s in EXPLICIT.items():
        if short in s:
            return cat
    if re.search(r"_nixie_tube$", short):
        return "redstone"
    if re.search(r"(_window|_window_pane|_bars|_ladder|_scaffolding|_table_cloth|_seat|_sail|_postbox"
                 r"|_valve_handle|_casing|_pillar|_shingles?|_tiles?|framed_glass|tiled_glass|_door$"
                 r"|_trapdoor$)", short):
        return "decor"
    if re.match(r"^(cut_|polished_cut_|small_|layered_)", short):
        return "decor"
    if short in ("asurine", "crimsite", "ochrum", "veridium", "limestone", "scorchia", "scoria",
                 "industrial_iron_block", "weathered_iron_block", "railway_casing", "metal_girder",
                 "andesite_pillar", "brass_pillar", "copper_pillar", "granite_pillar", "diorite_pillar"):
        return "decor"
    return "misc"

for iid in items:
    items[iid]["cat"] = categorize(iid)

# ------------------------------------------------------------------ ponder
GENERIC_TOKENS = set("""
cut polished small large tiles tile brick bricks pillar layered wall slab stairs pane
window bars seat sail postbox toolbox valve handle cloth table nixie tube casing block
andesite asurine calcite crimsite deepslate diorite dripstone granite limestone ochrum
scorchia scoria tuff veridium copper zinc brass iron gold glass wood stone andesite_alloy
""".split())

STOP = {"and", "of", "the", "block", "cut", "small", "large", "polished", "framed", "glass", "wall"}

def toks(s):
    return [t for t in s.split("_") if t and t not in STOP]

def scenes_for(short):
    if short in ponder:
        return [(short, 1.0)]
    t = set(toks(short))
    if not t:
        return []
    res = []
    for scene in ponder:
        st = set(toks(scene))
        if not st:
            continue
        inter = t & st
        if not inter:
            continue
        score = (len(inter) / len(t) + len(inter) / len(st)) / 2.0
        if all(tok in GENERIC_TOKENS for tok in inter):
            continue
        if score >= 0.6:
            res.append((scene, score + len(inter) * 0.02))
    res.sort(key=lambda x: (-x[1], len(x[0])))
    return res[:3]

for iid in items:
    short = iid.split(":", 1)[1]
    lst = []
    for scene, score in scenes_for(short):
        p = ponder[scene]
        if not p["steps"]:
            continue
        lst.append({"scene": scene, "header": p["header"], "steps": p["steps"]})
    items[iid]["ponder"] = lst

# ------------------------------------------------------------------ tutorials
def tutorial_for(iid):
    if iid in content.TUT:
        return content.TUT[iid], "hand"
    short = iid.split(":", 1)[1]
    for pat, t in content.FAMILY:
        if re.search(pat, short):
            return t, "family"
    cat = items[iid]["cat"]
    generic = {
        "decor": {"tag": "装饰/建筑方块，用于美化基地与产线。",
                  "sections": [("怎么用", "<p>按样式自由组合；多数变体可以用<strong>切石机</strong>或工作台在系列内转换。</p>")]},
        "misc": {"tag": "Create 的物品之一，暂无单独教程。",
                 "sections": [("说明", "<p>这个物品的详细用法还在整理中，先参考上方的配方与官方教程。</p>")]},
        "material": {"tag": "Create 的材料/中间产物。",
                     "sections": [("怎么用", "<p>参考上方配方，通常是某条产线的原料或产物。</p>")]},
        "redstone": {"tag": "Create 的红石元件。",
                     "sections": [("怎么用", "<p>参考官方教程与配方了解接线方式。</p>")]},
        "tool": {"tag": "Create 的工具/装备。",
                 "sections": [("怎么用", "<p>具体用法整理中。</p>")]},
        "logistics": {"tag": "Create 的物流元件。",
                      "sections": [("怎么用", "<p>配合传送带/漏斗/管道使用，具体细节整理中。</p>")]},
        "machine": {"tag": "Create 的机器。",
                    "sections": [("怎么用", "<p>需要旋转动力驱动，具体参数整理中。</p>")]},
        "power": {"tag": "Create 的传动部件。",
                  "sections": [("怎么用", "<p>接在传动网络上传递旋转，具体细节整理中。</p>")]},
        "train": {"tag": "Create 的列车部件。",
                  "sections": [("怎么用", "<p>参考官方教程，具体细节整理中。</p>")]},
        "contraption": {"tag": "Create 的动态结构部件。",
                        "sections": [("怎么用", "<p>配合超级胶与轴承使用，具体细节整理中。</p>")]},
    }
    return generic.get(cat, generic["misc"]), "auto"

# ------------------------------------------------------------------ helpers
MACHINE = {
    "crafting_shaped": "工作台", "crafting_shapeless": "工作台", "stonecutting": "切石机",
    "smelting": "熔炉", "blasting": "高炉", "smoking": "烟熏炉", "campfire_cooking": "营火",
    "smithing_transform": "锻造台", "pressing": "机械压床", "mixing": "搅拌器（盆）",
    "compacting": "压床 / 压实", "crushing": "粉碎轮", "milling": "磨盘", "cutting": "机械锯",
    "deploying": "部署器", "filling": "注液器", "emptying": "物品沥干器", "haunting": "缠魂（风扇+火）",
    "splashing": "洗涤（风扇+水）", "item_application": "部署器（涂覆）",
    "sandpaper_polishing": "砂纸打磨", "sequenced_assembly": "序列组装",
    "mechanical_crafting": "动力合成器", "item_copying": "复制", "toolbox_dyeing": "染色",
}

def esc(s):
    return html.escape(s or "", quote=True)

def slug(iid):
    return iid.split(":", 1)[1]

ICON_ALIAS = {
    "water_wheel_structure": "create_large_water_wheel.png",
    "chocolate": "create_chocolate_bucket.png",
    "honey": "create_honey_bucket.png",
    "fake_track": "create_track.png",
    "copycat_panel": "create_copycat_base.png",
    "copycat_step": "create_copycat_base.png",
    "wand_of_symmetry": "create_symmetry_mirror.png",
    "crushing_wheel_controller": "create_crushing_wheel.png",
    "lectern_controller": "create_linked_controller.png",
    "toolbox": "create_toolbox.png",
}

def icon_file(iid):
    d = items.get(iid) or vanilla.get(iid) or {}
    short = iid.split(":", 1)[1]
    # 原版物品：优先用红河站的高清 3D 图标
    if iid.startswith("minecraft:") and os.path.exists(os.path.join(SITE, "assets", "icons", "hh3d_" + short + ".png")):
        return "hh3d_" + short + ".png"
    cands = []
    if d.get("icon"):
        cands.append(d["icon"])
    if iid.startswith("create:"):
        cands.append("create_" + short + ".png")
        base = short
        if base.endswith("_brick_wall"):
            cands.append("create_" + base[:-11] + "_brick.png")
            cands.append("create_" + base[:-11] + ".png")
        for suf in ("_wall", "_slab", "_stairs", "_fence", "_pane"):
            if base.endswith(suf):
                cands.append("create_" + base[: -len(suf)] + ".png")
        stem = short
        for pre in ("waxed_oxidized_", "waxed_weathered_", "waxed_exposed_", "waxed_",
                    "oxidized_", "weathered_", "exposed_"):
            if stem.startswith(pre):
                cands.append("create_" + stem[len(pre):] + ".png")
                stem = stem[len(pre):]
        if short in ICON_ALIAS:
            cands.append(ICON_ALIAS[short])
    cands.append("minecraft_" + short + ".png")
    for c in cands:
        if c and os.path.exists(os.path.join(ICONS, c)):
            if c != "_unknown.png" and os.path.exists(os.path.join(ICONS, "3d_" + c)):
                return "3d_" + c
            return c
    if iid.startswith("create:") and os.path.exists(os.path.join(ICONS, "3d_create_" + short + ".png")):
        return "3d_create_" + short + ".png"
    return "_unknown.png"

def icon_path(iid):
    return "assets/icons/" + icon_file(iid)

def rel_icon(iid, prefix=""):
    return prefix + "assets/icons/" + icon_file(iid)

MC_ZH = {}
try:
    MC_ZH = json.load(open(os.path.join(OUT, "mc_zh.json"), encoding="utf-8"))
except Exception as e:
    print("mc_zh load failed:", e)


def mc_name(short):
    return (MC_ZH.get("item.minecraft." + short)
            or MC_ZH.get("block.minecraft." + short)
            or "")


def name_of(iid):
    if iid in items:
        return items[iid]["n"]
    if iid in vanilla:
        return vanilla[iid]["n"]
    short = iid.split(":", 1)[1]
    zh = mc_name(short)
    if zh:
        return zh
    return short.replace("_", " ")

# 材质词根 → 中文（用于 forge:ingots/xxx 这类「类别/材质」结构）
MAT_ZH = {
    "iron": "铁", "copper": "铜", "gold": "金", "zinc": "锌", "brass": "黄铜",
    "netherite": "下界合金", "diamond": "钻石", "emerald": "绿宝石", "emeraldite": "绿宝石",
    "lapis": "青金石", "quartz": "石英", "coal": "煤炭", "charcoal": "木炭",
    "redstone": "红石", "aluminum": "铝", "lead": "铅", "nickel": "镍", "tin": "锡",
    "silver": "银", "osmium": "锇", "platinum": "铂", "uranium": "铀", "quicksilver": "水银",
    "ametrine": "紫黄晶", "anthracite": "无烟煤", "lignite": "褐煤",
    "flint": "燧石", "obsidian": "黑曜石", "clay": "黏土", "brick": "砖",
}
# 类别词根 → 中文后缀
KIND_ZH = {
    "ingots": "锭", "nuggets": "粒", "plates": "板", "dusts": "粉", "rods": "棒",
    "storage_blocks": "块", "ores": "矿石", "gems": "宝石",
    "glass": "玻璃", "glass_panes": "玻璃板", "dyes": "染料",
}
COLOR_ZH = {
    "white": "白色", "orange": "橙色", "magenta": "品红色", "light_blue": "浅蓝色",
    "yellow": "黄色", "lime": "黄绿色", "pink": "粉色", "gray": "灰色",
    "light_gray": "浅灰色", "cyan": "青色", "purple": "紫色", "blue": "蓝色",
    "brown": "棕色", "green": "绿色", "red": "红色", "black": "黑色",
}
# 逐个手写的特例（无法用「类别+材质」拼出来的）
TAG_ZH = {
    "minecraft:trim_materials": "\u76d4\u7532\u7eb9\u9970\u6750\u6599",
    "minecraft:trim_templates": "\u76d4\u7532\u7eb9\u9970\u6a21\u677f",
    "minecraft:bookshelf_books": "\u4e66\u67b6\u4e66",
    "minecraft:compasses": "\u6307\u5357\u9488\u7c7b",
    "minecraft:completes_find_tree_tutorial": "\u5b8c\u6210\u627e\u6811\u6559\u7a0b",
    "minecraft:dampens_vibrations": "\u6291\u5236\u632f\u52a8",
    "minecraft:decorated_pot_ingredients": "\u9970\u7eb9\u9676\u7f50\u6750\u6599",
    "minecraft:fox_food": "\u72d0\u72f8\u98df\u7269",
    "minecraft:freeze_immune_wearables": "\u514d\u75ab\u51b0\u51bb\u88c5\u5907",
    "minecraft:ignored_by_piglin_babies": "\u5e7c\u5e74\u732a\u7075\u65e0\u89c6",
    "minecraft:non_flammable_wood": "\u4e0d\u53ef\u71c3\u6728\u6750",
    "minecraft:piglin_repellents": "\u732a\u7075\u9a71\u907f\u7269",
    "minecraft:smelts_to_glass": "\u53ef\u70e7\u6210\u73bb\u7483",
    "minecraft:soul_fire_base_blocks": "\u7075\u9b42\u706b\u57fa\u5e95",
    "minecraft:stone_tool_materials": "\u77f3\u5236\u5de5\u5177\u6750\u6599",
    "minecraft:tall_flowers": "\u9ad8\u82b1",
    "minecraft:villager_plantable_seeds": "\u6751\u6c11\u53ef\u79cd\u79cd\u5b50",
    "minecraft:wart_blocks": "\u75a3\u5757",
    "create:contraption_controlled": "\u52a8\u6001\u7ed3\u6784\u53ef\u63a7",
    "create:deployable_drink": "\u53ef\u90e8\u7f72\u996e\u54c1",
    "create:upright_on_belt": "\u4f20\u9001\u5e26\u76f4\u7acb",
    "minecraft:coals": "煤炭",
    "minecraft:gold_ores": "金矿石",
    "minecraft:iron_ores": "铁矿石",
    "minecraft:copper_ores": "铜矿石",
    "minecraft:coal_ores": "煤矿石",
    "minecraft:diamond_ores": "钻石矿石",
    "minecraft:emerald_ores": "绿宝石矿石",
    "minecraft:lapis_ores": "青金石矿石",
    "minecraft:redstone_ores": "红石矿石",
    "minecraft:copper_ore_blocks": "铜矿石方块",
    "minecraft:planks": "木板",
    "minecraft:logs": "原木",
    "minecraft:logs_that_burn": "可燃原木",
    "minecraft:stone_bricks": "石砖",
    "minecraft:stone_crafting_materials": "石制合成材料",
    "minecraft:stone_buttons": "石按钮",
    "minecraft:wooden_slabs": "木台阶",
    "minecraft:wooden_stairs": "木楼梯",
    "minecraft:wooden_fences": "木栅栏",
    "minecraft:wooden_doors": "木门",
    "minecraft:wooden_trapdoors": "木活板门",
    "minecraft:wooden_buttons": "木按钮",
    "minecraft:wooden_pressure_plates": "木压力板",
    "minecraft:small_flowers": "小型花",
    "minecraft:flowers": "花",
    "minecraft:leaves": "树叶",
    "minecraft:saplings": "树苗",
    "minecraft:sand": "沙子",
    "minecraft:wool": "羊毛",
    "minecraft:wool_carpets": "羊毛地毯",
    "minecraft:terracotta": "陶瓦",
    "minecraft:dirt": "泥土",
    "minecraft:axes": "斧",
    "minecraft:pickaxes": "镐",
    "minecraft:shovels": "锹",
    "minecraft:hoes": "锄",
    "minecraft:swords": "剑",

    "minecraft:planks": "木板", "minecraft:logs": "原木", "minecraft:wool": "羊毛",
    "minecraft:axes": "斧", "minecraft:buttons": "按钮", "minecraft:small_flowers": "小型花",
    "minecraft:wooden_slabs": "木台阶", "minecraft:wooden_buttons": "木按钮",
    "minecraft:wooden_pressure_plates": "木压力板", "minecraft:wooden_doors": "木门",
    "minecraft:wooden_trapdoors": "木活板门",
    "forge:stone": "石头", "forge:cobblestone": "圆石", "forge:glass": "玻璃",
    "forge:glass/colorless": "无色玻璃", "forge:glass_panes/colorless": "无色玻璃板",
    "forge:string": "线", "forge:leather": "皮革", "forge:gunpowder": "火药",
    "forge:paper": "纸", "forge:slimeballs": "黏液球", "forge:eggs": "鸡蛋",
    "forge:glass": "玻璃",
    "forge:ender_pearls": "末影珍珠", "forge:feathers": "羽毛", "forge:netherrack": "下界岩",
    "forge:rods/wooden": "木棍", "forge:stripped_logs": "去皮原木", "forge:stripped_wood": "去皮木",
    "forge:chests/wooden": "木箱子", "forge:barrels/wooden": "木桶",
    "forge:sand/colorless": "沙子", "forge:sand/red": "红沙",
    "forge:obsidian": "黑曜石", "forge:plates/obsidian": "黑曜石板",
    "forge:dusts/obsidian": "黑曜石粉", "forge:gems/quartz": "石英",
    "forge:flour/wheat": "小麦粉",
    "create:pulpifiable": "可打浆物", "create:valve_handles": "阀门手柄",
    "create:dyed_table_cloths": "染色桌布", "create:postboxes": "邮箱",
    "create:seats": "座椅", "create:sleepers": "枕木",
}

STONE_TAG_ZH = {"andesite": "安山岩", "asurine": "天青石", "calcite": "方解石", "crimsite": "绯红岩",
    "deepslate": "深板岩", "diorite": "闪长岩", "dripstone": "滴水石", "granite": "花岗岩",
    "limestone": "石灰岩", "ochrum": "赭金岩", "scorchia": "焦黑岩", "scoria": "火山渣",
    "tuff": "凝灰岩", "veridium": "铜绿岩", "stone": "石头", "cobblestone": "圆石"}

def tag_label(tag):
    if tag in TAG_ZH:
        return TAG_ZH[tag]
    parts = tag.split(":")[-1].split("/")
    if parts[0] == "stone_types" and len(parts) == 2:
        return STONE_TAG_ZH.get(parts[1], parts[1].replace("_", " "))
    if len(parts) == 2:
        kind, name = parts
        if kind == "raw_materials":
            return "粗" + MAT_ZH.get(name, name.replace("_", " "))
        if kind in KIND_ZH:
            if name.startswith("raw_"):
                base = "粗" + MAT_ZH.get(name[4:], name[4:].replace("_", " "))
                return base + ("块" if kind == "storage_blocks" else "")
            if kind == "dyes":
                return COLOR_ZH.get(name, name.replace("_", " ")) + "染料"
            return MAT_ZH.get(name, name.replace("_", " ")) + KIND_ZH[kind]
    return parts[-1].replace("_", " ")

def tag_url(tag, prefix=""):
    return prefix + "tags/" + tag.replace(":", "_").replace("/", "_") + ".html"

def stack_chip(st, prefix=""):
    if "fluid" in st:
        fname = st["fluid"].split(":")[-1].replace("_", " ")
        return ('<span class="chip fluid"><i class="drop"></i>%s <b>%s mB</b></span>'
                % (esc(fname), st.get("amount", 0)))
    if "tag" in st:
        tg = st["tag"]
        ic = tag_icon(tg)
        pre = ('<img src="%s" alt="" loading="lazy" decoding="async">' % (prefix + "assets/icons/" + ic)) if ic else '<i>#</i>'
        return '<a class="chip tag" href="%s">%s%s</a>' % (tag_url(tg, prefix), pre, esc(tag_label(tg)))
    iid = st["id"]
    cnt = st.get("count", 1)
    return ('<a class="chip" href="%s"><img src="%s" alt="" loading="lazy" decoding="async"><span>%s</span><b>×%d</b></a>'
            % (item_url(iid, prefix), rel_icon(iid, prefix), esc(name_of(iid)), cnt))

def item_url(iid, prefix=""):
    if iid in items:
        return prefix + "items/" + slug(iid) + ".html"
    return "#"

def recipe_card(r, prefix=""):
    m = MACHINE.get(r["type"], r["type"])
    out = ['<div class="recipe"><div class="recipe-head"><span class="machine">%s</span>' % esc(m)]
    if r.get("heat"):
        out.append('<span class="heat">需加热</span>')
    if r.get("processingTime"):
        out.append('<span class="time">%.1fs</span>' % (r["processingTime"] / 20.0))
    if r.get("loops"):
        out.append('<span class="loops">循环 %d 次</span>' % r["loops"])
    out.append("</div>")

    if r.get("pattern") and r.get("key"):
        out.append('<div class="craft"><div class="grid" style="--n:%d">' % len(r["pattern"][0]))
        for row in r["pattern"]:
            for ch in row:
                st = r["key"].get(ch)
                if ch == " " or not st:
                    out.append('<div class="cell empty"></div>')
                else:
                    out.append('<div class="cell">%s</div>' % icon_tag_for_stack(st, prefix))
        out.append("</div></div>")
        out.append('<div class="arrow">→</div>')
    else:
        ings = r.get("ingredients") or ([r["ingredient"]] if r.get("ingredient") else [])
        out.append('<div class="ings">%s</div><div class="arrow">→</div>'
                   % "".join(stack_chip(x, prefix) for x in ings if x))

    outs = r.get("results") or []
    out.append('<div class="outs">%s</div>' % "".join(stack_chip(x, prefix) for x in outs[:4]))
    if r.get("sequence"):
        out.append('<div class="seq"><span class="seq-label">工序</span>')
        for i, step in enumerate(r["sequence"], 1):
            tool = {"pressing": "压床", "deploying": "部署器", "cutting": "锯",
                    "filling": "注液器", "pressing ": "压床"}.get(step["type"], step["type"])
            out.append('<span class="step">%d · %s</span>' % (i, esc(MACHINE.get(step["type"], step["type"]))))
        out.append("</div>")
    out.append("</div>")
    return "".join(out)

def icon_tag_for_stack(st, prefix=""):
    if "id" in st:
        return '<img src="%s" alt="" loading="lazy" decoding="async"><em>%s</em>' % (rel_icon(st["id"], prefix), esc(name_of(st["id"])))
    if "tag" in st:
        tg = st["tag"]
        ic = tag_icon(tg)
        if ic:
            return ('<a class="tagcell hasi" href="%s" title="#%s"><img src="%s" alt="" loading="lazy" decoding="async"><i>#</i></a>'
                    % (tag_url(tg, prefix), esc(tag_label(tg)), prefix + "assets/icons/" + ic))
        return '<a class="tagcell" href="%s">#%s</a>' % (tag_url(tg, prefix), esc(tag_label(tg)))
    return '<span class="tagcell">?</span>'

# ------------------------------------------------------------------ tags & reverse index
# Curated member lists for forge/vanilla tags not shipped inside the Create repo.
WOODS = ["oak", "spruce", "birch", "jungle", "acacia", "dark_oak", "mangrove",
         "cherry", "crimson", "warped"]
COLORS = ["white", "orange", "magenta", "light_blue", "yellow", "lime", "pink",
          "gray", "light_gray", "cyan", "purple", "blue", "brown", "green", "red", "black"]
TAG_EXTRA = {}
for _c in COLORS:
    TAG_EXTRA["forge:dyes/" + _c] = ["minecraft:" + _c + "_dye"]
    TAG_EXTRA["minecraft:wool"] = TAG_EXTRA.get("minecraft:wool", []) + ["minecraft:" + _c + "_wool"]
TAG_EXTRA["forge:glass"] = ["minecraft:glass"] + ["minecraft:" + _c + "_stained_glass" for _c in COLORS]
TAG_EXTRA["minecraft:planks"] = ["minecraft:" + _w + "_planks" for _w in WOODS]
TAG_EXTRA["minecraft:logs"] = [("minecraft:" + _w + "_stem" if _w in ("crimson", "warped")
                                else "minecraft:" + _w + "_log") for _w in WOODS]
TAG_EXTRA["minecraft:wooden_slabs"] = ["minecraft:" + _w + "_slab" for _w in WOODS]
TAG_EXTRA["minecraft:wooden_buttons"] = ["minecraft:" + _w + "_button" for _w in WOODS]
TAG_EXTRA["minecraft:wooden_pressure_plates"] = ["minecraft:" + _w + "_pressure_plate" for _w in WOODS]
TAG_EXTRA["minecraft:wooden_doors"] = ["minecraft:" + _w + "_door" for _w in WOODS]
TAG_EXTRA["minecraft:wooden_trapdoors"] = ["minecraft:" + _w + "_trapdoor" for _w in WOODS]
TAG_EXTRA["minecraft:axes"] = ["minecraft:wooden_axe", "minecraft:stone_axe", "minecraft:iron_axe",
                               "minecraft:golden_axe", "minecraft:diamond_axe", "minecraft:netherite_axe"]
TAG_EXTRA["minecraft:buttons"] = ["minecraft:stone_button", "minecraft:polished_blackstone_button"]
TAG_EXTRA["minecraft:small_flowers"] = ["minecraft:dandelion", "minecraft:poppy", "minecraft:blue_orchid",
    "minecraft:allium", "minecraft:azure_bluet", "minecraft:red_tulip", "minecraft:orange_tulip",
    "minecraft:white_tulip", "minecraft:pink_tulip", "minecraft:oxeye_daisy", "minecraft:cornflower",
    "minecraft:lily_of_the_valley", "minecraft:wither_rose", "minecraft:torchflower"]
TAG_EXTRA.update({
    "forge:barrels/wooden": ["minecraft:barrel"],
    "forge:chests/wooden": ["minecraft:chest", "minecraft:trapped_chest"],
    "forge:cobblestone": ["minecraft:cobblestone", "minecraft:mossy_cobblestone"],
    "forge:dusts/redstone": ["minecraft:redstone"],
    "forge:eggs": ["minecraft:egg"],
    "forge:ender_pearls": ["minecraft:ender_pearl"],
    "forge:feathers": ["minecraft:feather"],
    "forge:gems/quartz": ["minecraft:quartz"],
    "forge:gunpowder": ["minecraft:gunpowder"],
    "forge:ingots/copper": ["minecraft:copper_ingot"],
    "forge:ingots/gold": ["minecraft:gold_ingot"],
    "forge:ingots/iron": ["minecraft:iron_ingot"],
    "forge:leather": ["minecraft:leather"],
    "forge:netherrack": ["minecraft:netherrack"],
    "forge:nuggets/iron": ["minecraft:iron_nugget"],
    "forge:obsidian": ["minecraft:obsidian"],
    "forge:rods/wooden": ["minecraft:stick"],
    "forge:sand/colorless": ["minecraft:sand"],
    "forge:sand/red": ["minecraft:red_sand"],
    "forge:slimeballs": ["minecraft:slime_ball"],
    "forge:stone": ["minecraft:stone", "minecraft:andesite", "minecraft:diorite",
                    "minecraft:granite", "minecraft:deepslate", "minecraft:tuff",
                    "minecraft:cobbled_deepslate"],
    "forge:string": ["minecraft:string"],
    "forge:storage_blocks/copper": ["minecraft:copper_block"],
    "forge:storage_blocks/iron": ["minecraft:iron_block"],
    "forge:raw_materials/copper": ["minecraft:raw_copper"],
    "forge:raw_materials/gold": ["minecraft:raw_gold"],
    "forge:raw_materials/iron": ["minecraft:raw_iron"],
    "forge:storage_blocks/raw_copper": ["minecraft:raw_copper_block"],
    "forge:storage_blocks/raw_gold": ["minecraft:raw_gold_block"],
    "forge:storage_blocks/raw_iron": ["minecraft:raw_iron_block"],
})

# Load tag definitions shipped in the Create repo (create/forge/minecraft/curios/quark).
TAG_DIR = os.path.join(DATA, "create_tags")
_local_tags = {}
for _root, _dirs, _files in os.walk(TAG_DIR):
    for _f in _files:
        if not _f.endswith(".json"):
            continue
        _rel = os.path.relpath(os.path.join(_root, _f), TAG_DIR).replace(os.sep, "/")
        _p = _rel.split("/")
        if len(_p) > 3 and _p[1] == "tags" and _p[2] == "items":
            _key = _p[0] + ":" + "/".join(_p[3:])[:-5]
            try:
                _local_tags[_key] = json.load(open(os.path.join(_root, _f), encoding="utf-8")).get("values", [])
            except Exception:
                _local_tags[_key] = []

def resolve_tag(tg, _seen=None):
    _seen = _seen or set()
    if tg in _seen:
        return set()
    _seen.add(tg)
    out = set()
    for v in _local_tags.get(tg, []):
        idv = v if isinstance(v, str) else (v or {}).get("id")
        if not idv:
            continue
        if idv.startswith("#"):
            out |= resolve_tag(idv[1:], _seen)
        else:
            out.add(idv)
    if not out and tg in TAG_EXTRA:
        out = set(TAG_EXTRA[tg])
    return out

# ---- reverse index: which item is consumed by whom; which recipe uses each tag
consumed_by = {}
tag_used_in = {}
used_tags = set()

def _acc(st, qty, iid, machine):
    n = st.get("count", 1) * qty
    if st.get("id") in items:
        d = consumed_by.setdefault(st["id"], {}).setdefault(iid, {"machines": set(), "count": 0, "recipes": 0})
        d["machines"].add(machine); d["count"] += n; d["recipes"] += 1
    elif st.get("tag"):
        used_tags.add(st["tag"])
        d = tag_used_in.setdefault(st["tag"], {}).setdefault(iid, {"machines": set(), "count": 0, "recipes": 0})
        d["machines"].add(machine); d["count"] += n; d["recipes"] += 1

for _iid, _it in items.items():
    for r in _it.get("recipes") or []:
        _m = MACHINE.get(r["type"], r["type"])
        if r.get("pattern") and r.get("key"):
            _occ = {}
            for row in r["pattern"]:
                for ch in row:
                    if ch != " " and ch in r["key"]:
                        _occ[ch] = _occ.get(ch, 0) + 1
            for ch, k in _occ.items():
                _acc(r["key"][ch], k, _iid, _m)
        else:
            _ings = r.get("ingredients") or ([r["ingredient"]] if r.get("ingredient") else [])
            for st in _ings:
                if isinstance(st, dict):
                    _acc(st, 1, _iid, _m)

for _t, _m in {"forge:gems/amethyst": ["minecraft:amethyst_shard"],
               "forge:gems/lapis": ["minecraft:lapis_lazuli"]}.items():
    _local_tags[_t] = _m
    used_tags.add(_t)

tag_members = {tg: sorted(resolve_tag(tg)) for tg in used_tags}

# ---- 补充常见原版标签：配方里不出现但玩家会查（煤炭、木板、原木等）
# 数据来自 misode/mcmeta 1.20.1 的原版 item tags，缓存在 out/vanilla_tags.json
_EXTRA_TAG_FILE = os.path.join(OUT, "vanilla_tags.json")
if os.path.exists(_EXTRA_TAG_FILE):
    try:
        _extra = json.load(open(_EXTRA_TAG_FILE, encoding="utf-8"))
    except Exception:
        _extra = {}
    # 让「含本站用到的原版物品」的标签也生成页面
    try:
        _van = set(json.load(open(os.path.join(OUT, "data.json"), encoding="utf-8"))["vanilla"])
    except Exception:
        _van = set()
    _full = {}
    _fullf = os.path.join(OUT, "vanilla_tags_all.json")
    if os.path.exists(_fullf):
        try:
            _full = json.load(open(_fullf, encoding="utf-8"))
        except Exception:
            _full = {}
    
    # —— 合成 Forge 常见物品标签（仓库里没有这些定义，靠原版方块名补）——
    _FORGE_BLOCKS = {
        "iron": "minecraft:iron_block", "gold": "minecraft:gold_block",
        "copper": "minecraft:copper_block", "diamond": "minecraft:diamond_block",
        "emerald": "minecraft:emerald_block", "coal": "minecraft:coal_block",
        "redstone": "minecraft:redstone_block", "lapis": "minecraft:lapis_block",
        "netherite": "minecraft:netherite_block", "quartz": "minecraft:quartz_block",
        "raw_iron": "minecraft:raw_iron_block", "raw_gold": "minecraft:raw_gold_block",
        "raw_copper": "minecraft:raw_copper_block", "amethyst": "minecraft:amethyst_block",
        "bone": "minecraft:bone_block", "slime": "minecraft:slime_block",
        "honey": "minecraft:honey_block", "hay": "minecraft:hay_block",
    }
    _FORGE_GEMS = {
        "diamond": "minecraft:diamond", "emerald": "minecraft:emerald",
        "quartz": "minecraft:quartz", "lapis": "minecraft:lapis_lazuli",
        "amethyst": "minecraft:amethyst_shard", "coal": "minecraft:coal",
        "charcoal": "minecraft:charcoal", "redstone": "minecraft:redstone",
    }
    _FORGE_SYNTH = {}
    for _k, _v in _FORGE_BLOCKS.items():
        _FORGE_SYNTH["forge:storage_blocks/" + _k] = [_v]
    for _k, _v in _FORGE_GEMS.items():
        _FORGE_SYNTH["forge:gems/" + _k] = [_v]
    _FORGE_SYNTH["forge:chests/wooden"] = ["minecraft:chest", "minecraft:trapped_chest"]

    _all_tags = dict(_extra) if isinstance(_extra, dict) else {}
    _all_tags.update(_full)
    _all_tags.update(_local_tags)
    _all_tags.update(_FORGE_SYNTH)
    for _tg, _mem in _FORGE_SYNTH.items():
        if _tg not in used_tags:
            tag_members[_tg] = sorted(set(_mem))
            used_tags.add(_tg)
    if _van:
        for _tg in list(_all_tags):
            if _tg in used_tags:
                continue
            _raw = _all_tags.get(_tg) or []
            _mem = []
            for _v in _raw:
                if not isinstance(_v, str):
                    continue
                if _v.startswith("#"):
                    _mem.extend([x for x in _all_tags.get(_v[1:], []) if isinstance(x, str) and not x.startswith("#")])
                else:
                    _mem.append(_v)
            _mem = sorted(set(_mem))
            if _mem and any(x in _van for x in _mem):
                tag_members[_tg] = _mem
                used_tags.add(_tg)

    # 附属页合成表里出现的标签也建页（例如 #minecraft:saplings）
    try:
        import glob as _glob, re as _re
        _seen = set()
        for _f in _glob.glob(os.path.join(SITE, "addon-*.html")):
            _h = open(_f, encoding="utf-8").read()
            for _m in _re.finditer(r"#([a-z0-9_]+:[a-z0-9_/]+)", _h):
                _seen.add(_m.group(1))
        for _tg in sorted(_seen):
            if _tg in used_tags:
                continue
            _raw = _all_tags.get(_tg) or _local_tags.get(_tg)
            if not _raw:
                continue
            _mem = []
            for _v in _raw:
                if isinstance(_v, str):
                    if _v.startswith("#"):
                        _mem.extend([x for x in (_all_tags.get(_v[1:]) or _local_tags.get(_v[1:]) or []) if isinstance(x, str) and not x.startswith("#")])
                    else:
                        _mem.append(_v)
            if _mem:
                tag_members[_tg] = sorted(set(_mem))
                used_tags.add(_tg)
    except Exception as _e:
        print("addon tag scan failed:", _e)

    # 附属页里以链接形式出现的标签页（tags/xxx.html）也要保证是真页面
    try:
        import glob as _glob, re as _re2
        _byname = {}
        for _t in list(_all_tags) + list(_local_tags):
            _byname[_t.replace(":", "_").replace("/", "_")] = _t
        _want = set()
        for _f in _glob.glob(os.path.join(SITE, "addon-*.html")):
            _h = open(_f, encoding="utf-8").read()
            for _m in _re2.finditer(r'href="tags/([a-z0-9_]+)\.html"', _h):
                _t = _byname.get(_m.group(1))
                if _t:
                    _want.add(_t)
        for _tg in sorted(_want):
            if _tg in used_tags:
                continue
            _raw = _all_tags.get(_tg) or _local_tags.get(_tg) or []
            _mem = []
            for _v in _raw:
                if isinstance(_v, str):
                    if _v.startswith("#"):
                        _mem.extend([x for x in (_all_tags.get(_v[1:]) or _local_tags.get(_v[1:]) or []) if isinstance(x, str) and not x.startswith("#")])
                    else:
                        _mem.append(_v)
            tag_members[_tg] = sorted(set(_mem))
            used_tags.add(_tg)
    except Exception as _e:
        print("addon tag link scan failed:", _e)

    for _tg, _vals in _extra.items():
        if _tg in _local_tags:
            continue
        _local_tags[_tg] = _vals
        _mem = sorted(x for x in resolve_tag(_tg) if isinstance(x, str))
        if _mem:
            tag_members[_tg] = _mem
            used_tags.add(_tg)


TAG_ICON_OVERRIDE = {
    "minecraft:buttons": "hh_button_wood.png",
    "minecraft:wooden_buttons": "hh_button_wood.png",
    "minecraft:stone_buttons": "hh_button_stone.png",
    "forge:chests": "hh_chest.png",
    "forge:chests/wooden": "hh_chest.png",
    "minecraft:chests": "hh_chest.png",
    "minecraft:coals": "minecraft_coal.png",
    "forge:glass": "hh3d_glass.png",
    "minecraft:glass": "hh3d_glass.png",
    "minecraft:trim_materials": "hh3d_smithing_table.png",
    "minecraft:trim_templates": "hh3d_smithing_table.png",
    "minecraft:planks": "minecraft_oak_planks.png",
    "minecraft:logs": "minecraft_oak_log.png",
    "forge:glass/colorless": "minecraft_glass.png",
    "minecraft:wooden_slabs": "minecraft_oak_planks.png",
    "minecraft:wooden_pressure_plates": "minecraft_oak_planks.png",
    "minecraft:wooden_doors": "minecraft_oak_door.png",
    "minecraft:wooden_trapdoors": "minecraft_oak_trapdoor.png",
    "forge:stripped_wood": "minecraft_stripped_oak_log.png",
}

def tag_icon(tg):
    """挑一个能代表该标签的成员图标：先按标签同名物品，再退回第一个有图的成员。"""
    if tg in TAG_ICON_OVERRIDE:
        return TAG_ICON_OVERRIDE[tg]
    seg = tg.split("/")[-1].split(":")[-1]
    members = tag_members.get(tg, [])
    same = [m for m in members if m.split(":")[-1] == seg or m.split(":")[-1].endswith("_" + seg)]
    for m in same + [m for m in members if m not in same]:
        f = icon_file(m)
        if f and f != "_unknown.png":
            return f
    _seg = tg.split(":")[-1].split("/")[-1]
    for cand in ("hh3d_" + _seg + ".png", "3d_create_" + _seg + ".png", "create_" + _seg + ".png"):
        if os.path.exists(os.path.join(SITE, "assets", "icons", cand)):
            return cand
    return "_unknown.png"

def use_section(iid, prefix="../"):
    cb = consumed_by.get(iid)
    if not cb:
        return ""
    groups = {}
    for prod, info in cb.items():
        for m in info["machines"]:
            groups.setdefault(m, []).append((prod, info["count"]))
    gs = sorted(groups.items(), key=lambda kv: -sum(c for _, c in kv[1]))
    n_prod = len(cb)
    n_rec = sum(info["recipes"] for info in cb.values())
    out = ['<section class="blk"><h2>被谁使用</h2>',
           '<p class="uses-note">被 <b>%d</b> 个物品的 <b>%d</b> 条配方用作材料。</p>' % (n_prod, n_rec),
           '<div class="uses">']
    for m, lst in gs:
        lst.sort(key=lambda x: items[x[0]]["n"])
        out.append('<div class="use-group"><h3>%s <span>%d 个</span></h3><div class="uses-chips">'
                   % (esc(m), len(lst)))
        for prod, cnt in lst:
            out.append('<a class="chip" href="%s.html"><img src="%s" alt="" loading="lazy" decoding="async"><span>%s</span><b>×%d</b></a>'
                       % (slug(prod), rel_icon(prod, prefix), esc(items[prod]["n"]), cnt))
        out.append("</div></div>")
    out.append("</div></section>")
    return "".join(out)

def tag_page_html(tag):
    label = tag_label(tag)
    members = tag_members.get(tag, [])
    create_m = [m for m in members if m in items]
    other_m = [m for m in members if m not in items]
    used = tag_used_in.get(tag, {})
    groups = {}
    for prod, info in used.items():
        for m in info["machines"]:
            groups.setdefault(m, []).append((prod, info["count"]))
    gs = sorted(groups.items(), key=lambda kv: -sum(c for _, c in kv[1]))

    parts = [head("#%s — Create 标签" % label, "../")]
    parts.append('<header class="top"><div class="wrap">'
                 '<a class="logo" href="../index.html"><span class="gear"></span><span>CREATE CODEX<small>机械动力图鉴</small></span></a>'
                 '<nav><a href="../tags.html">标签</a><a href="https://github.com/Creators-of-Create/Create" target="_blank" rel="noopener">源码</a></nav></div></header>')
    parts.append('<main class="wrap rise">')
    parts.append('<div class="crumb"><a href="../index.html">首页</a> / <a href="../catalog.html">全部物品</a> / <a href="../tags.html">标签</a> / <span>%s</span></div>' % esc(label))
    _tf = tag_icon(tag)
    _big = ('<img class="big" src="../assets/icons/%s" alt="">' % _tf) if _tf else ''
    parts.append('<div class="item-hero">%s<div><h1><i class="hash">#</i>%s</h1>'
                 '<div class="idline"><span class="copyid">%s</span></div></div></div>'
                 % (_big, esc(label), esc(tag)))

    parts.append('<section class="blk"><h2>用到它的配方</h2>')
    if used:
        parts.append('<p class="uses-note">本站有 <b>%d</b> 个物品的配方用这个标签作为材料。</p>' % len(used))
        parts.append('<div class="uses">')
        for m, lst in gs:
            lst.sort(key=lambda x: items[x[0]]["n"])
            parts.append('<div class="use-group"><h3>%s <span>%d 个</span></h3><div class="uses-chips">'
                         % (esc(m), len(lst)))
            for prod, cnt in lst:
                parts.append('<a class="chip" href="../items/%s.html"><img src="%s" alt="" loading="lazy" decoding="async"><span>%s</span><b>×%d</b></a>'
                             % (slug(prod), rel_icon(prod, "../"), esc(items[prod]["n"]), cnt))
            parts.append("</div></div>")
        parts.append("</div>")
    else:
        parts.append('<div class="prose"><p>本站收录的 Create 配方里没有用到这个标签（它只被原版或其它模组的配方使用）。</p></div>')
    parts.append("</section>")

    parts.append('<section class="blk"><h2>标签成员 <span class="cnt">%d</span></h2>' % len(members))
    if create_m:
        parts.append('<div class="related">')
        for m in create_m:
            parts.append('<a class="chip" href="../items/%s.html"><img src="%s" alt="" loading="lazy" decoding="async"><span>%s</span></a>'
                         % (slug(m), rel_icon(m, "../"), esc(items[m]["n"])))
        parts.append("</div>")
    if other_m:
        tail = "" if len(other_m) <= 24 else " 等 %d 项" % len(other_m)
        _bits = []
        for _m in other_m[:24]:
            _vf = os.path.join(SITE, "vanilla", slug(_m) + ".html")
            if os.path.exists(_vf):
                _bits.append('<a href="../vanilla/%s.html">%s</a>' % (slug(_m), esc(name_of(_m))))
            else:
                _bits.append(esc(name_of(_m)))
        parts.append('<p class="uses-note">原版 / 其他模组成员：%s%s</p>'
                     % ("、".join(_bits), tail))
    if not members:
        parts.append('<div class="prose"><p>该标签的成员由原版或其他模组（矿石 / 材料兼容）提供，本站未收录对应物品。</p></div>')
    parts.append("</section>")

    parts.append('<div class="pager"><span></span><a href="../tags.html">返回标签索引</a><span></span></div>')
    parts.append("</main>")
    parts.append(foot("../"))
    parts.append(toast_script("../"))
    parts.append("</body></html>")
    return "".join(parts)

# ------------------------------------------------------------------ css / js
CSS = r"""
@font-face{font-family:'Minecraft';src:url('fonts/Minecraft.ttf') format('truetype');
  font-weight:400;font-display:swap}
:root{
  --bg:#12100d; --bg2:#171410; --panel:#1d1913; --panel2:#241f18; --line:#3a2e21;
  --brass:#d9a441; --brass2:#f2cd7c; --copper:#b4673c; --text:#eee4d2; --muted:#9c8b74;
  --shadow:0 10px 30px rgba(0,0,0,.45);
  --px:"Minecraft","Segoe UI",sans-serif;
}
*{box-sizing:border-box}
html{scroll-behavior:smooth;background:#0d0b08}
body{margin:0;background:
  radial-gradient(1200px 600px at 50% -200px,#2a2116 0%,transparent 60%),
  linear-gradient(180deg,#14110d,#0e0c09 60%);
  color:var(--text);font:15px/1.7 "Noto Sans SC","Microsoft YaHei","PingFang SC",sans-serif;
  min-height:100vh}
a{color:var(--brass2);text-decoration:none}
a:hover{text-decoration:underline}
.wrap{max-width:1180px;margin:0 auto;padding:0 20px}
header.top{position:sticky;top:0;z-index:20;background:rgba(18,16,13,.88);
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line)}
.top .wrap{display:flex;align-items:center;gap:18px;height:62px}
.logo{display:flex;align-items:center;gap:10px;font-family:var(--px);font-size:17px;letter-spacing:1px;color:var(--brass2)}
.logo .gear{width:26px;height:26px;border-radius:50%;border:3px solid var(--brass);
  background:radial-gradient(circle,#241f18 38%,transparent 40%);box-shadow:0 0 12px rgba(217,164,65,.35);
  animation:spin 9s linear infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.logo small{display:block;font-family:"Noto Sans SC",sans-serif;font-size:11px;color:var(--muted);letter-spacing:.22em}
.top nav{margin-left:auto;display:flex;gap:16px;font-size:14px;color:var(--muted)}
.top nav a{color:var(--muted)}
.top nav a:hover{color:var(--brass2);text-decoration:none}
.hero{padding:54px 0 26px;text-align:center}
.hero h1{font-family:var(--px);font-size:clamp(26px,5vw,46px);margin:0 0 10px;
  color:#f6e2b8;text-shadow:0 3px 0 #6b4a1d,0 0 30px rgba(217,164,65,.25);letter-spacing:2px}
.hero h1 span{color:var(--brass);font-size:.62em;display:block;margin-top:8px;letter-spacing:.3em}
.hero p{color:var(--muted);max-width:660px;margin:0 auto 22px}
.stats{display:flex;gap:26px;justify-content:center;flex-wrap:wrap;margin-bottom:6px}
.stat{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:10px 18px;min-width:110px}
.stat b{display:block;font-family:var(--px);font-size:22px;color:var(--brass2)}
.stat span{font-size:12px;color:var(--muted);letter-spacing:.1em}
.searchbar{position:relative;max-width:560px;margin:26px auto 0}
.searchbar input{width:100%;padding:13px 16px 13px 44px;border-radius:10px;border:1px solid var(--line);
  background:#0f0d0a;color:var(--text);font-size:15px;outline:none}
.searchbar input:focus{border-color:var(--brass);box-shadow:0 0 0 3px rgba(217,164,65,.12)}
.searchbar .ico{position:absolute;left:15px;top:12px;color:var(--muted)}
.filters{display:flex;flex-wrap:wrap;gap:8px;justify-content:center;padding:26px 0 8px}
.filters button{cursor:pointer;border:1px solid var(--line);background:var(--panel);color:var(--muted);
  padding:7px 14px;border-radius:999px;font-size:13px;transition:.15s}
.filters button:hover{border-color:var(--brass);color:var(--brass2)}
.filters button.on{background:linear-gradient(180deg,#4a3818,#2f2412);color:var(--brass2);border-color:var(--brass)}
.filters .cnt{opacity:.55;margin-left:6px;font-size:11px}
.grid-items{display:grid;grid-template-columns:repeat(auto-fill,minmax(178px,1fr));gap:12px;padding:22px 0 60px}
.card{content-visibility:auto;contain-intrinsic-size:auto 78px;display:flex;gap:12px;align-items:center;background:var(--panel);border:1px solid var(--line);
  border-radius:12px;padding:10px;transition:.15s;color:var(--text)}
.card:hover{border-color:var(--brass);transform:translateY(-2px);box-shadow:var(--shadow);text-decoration:none}
.card img{width:44px;height:44px;image-rendering:pixelated;border-radius:8px;background:#0d0b09;
  border:1px solid #2b2419;padding:3px;flex:0 0 auto}
.card .t{min-width:0}
.card .t b{display:block;font-size:13.5px;font-weight:600;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.card .t small{color:var(--muted);font-size:11px;font-family:ui-monospace,Consolas,monospace;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis;display:block}
.modbar{max-width:var(--w);margin:18px auto -6px;padding:10px 16px;border:1px solid var(--line);
  border-radius:10px;background:rgba(217,164,65,.06);color:var(--muted);font-size:13.5px;
  display:flex;align-items:center;gap:10px}
.modbar[hidden]{display:none}
.modbar b{color:var(--brass2)}
.modbar a{margin-left:auto;color:var(--brass);text-decoration:none;border-bottom:1px dashed rgba(217,164,65,.5)}
.modbar a:hover{color:#fff}
.empty-msg{text-align:center;color:var(--muted);padding:60px 0}
footer{border-top:1px solid var(--line);padding:26px 0 40px;color:var(--muted);font-size:12.5px;line-height:1.9}
footer a{color:var(--muted)}
/* ---------- item page ---------- */
.crumb{padding:20px 0 0;font-size:13px;color:var(--muted)}
.crumb a{color:var(--muted)}
.item-hero{display:flex;gap:24px;align-items:flex-start;padding:22px 0 8px;flex-wrap:wrap}
.item-hero .big{background-image:repeating-conic-gradient(#241d15 0 25%,#1a150f 0 50%);background-size:12px 12px;width:112px;height:112px;image-rendering:pixelated;background:#0d0b09;border:1px solid var(--line);
  border-radius:16px;padding:10px;box-shadow:inset 0 0 30px rgba(0,0,0,.7),0 8px 24px rgba(0,0,0,.4)}
.item-hero h1{margin:4px 0 6px;font-size:30px;letter-spacing:.5px}
.item-hero .en{color:var(--muted);font-size:13px}
.item-hero .idline{margin-top:10px;display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.copyid{font-family:ui-monospace,Consolas,monospace;font-size:12px;background:#0f0d0a;border:1px solid var(--line);
  padding:4px 9px;border-radius:7px;color:#c9b48f;cursor:pointer}
.copyid:hover{border-color:var(--brass);color:var(--brass2)}
.item-hero .big{background:radial-gradient(circle at 50% 38%,#221c15 0%,#131009 78%)}
.badge{font-size:11px;padding:3px 9px;border-radius:999px;border:1px solid var(--line);color:var(--muted)}
.tagline{font-size:16px;color:#f0dfba;border-left:3px solid var(--brass);padding:2px 0 2px 14px;
  margin:16px 0 6px;max-width:760px}
section.blk{padding:26px 0 4px}
section.blk h2{font-family:var(--px);font-size:16px;letter-spacing:.14em;color:var(--brass2);
  display:flex;align-items:center;gap:10px;margin:0 0 14px}
section.blk h2:after{content:"";flex:1;height:1px;background:linear-gradient(90deg,var(--line),transparent)}
.prose{max-width:820px;color:#ded2bd}
.prose p{margin:.5em 0 .9em}
.prose ul{margin:.4em 0 1em;padding-left:1.3em}
.prose li{margin:.25em 0}
.prose strong{color:var(--brass2);font-weight:600}
.prose code{background:#0f0d0a;border:1px solid var(--line);border-radius:5px;padding:1px 5px;font-size:.9em}
.params{display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;max-width:820px}
.param{background:var(--panel);border:1px solid var(--line);border-radius:10px;padding:10px 14px}
.param span{display:block;font-size:11.5px;color:var(--muted);letter-spacing:.08em}
.param b{font-size:14px;color:#f0dfba;font-weight:600}
.steps{counter-reset:s;max-width:820px;padding:0;list-style:none;margin:0}
.steps li{counter-increment:s;position:relative;padding:0 0 14px 40px;color:#ded2bd}
.steps li:before{content:counter(s);position:absolute;left:0;top:1px;width:24px;height:24px;border-radius:7px;
  background:#2a2116;border:1px solid var(--brass);color:var(--brass2);font-family:var(--px);font-size:12px;
  display:flex;align-items:center;justify-content:center}
.recipes{display:flex;flex-direction:column;gap:12px;max-width:860px}
.recipe{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:14px 16px;
  display:flex;align-items:center;gap:14px;flex-wrap:wrap}
.more-rec{color:var(--muted);font-size:13px;margin:12px 0 0}
.recipe-head{display:flex;gap:8px;align-items:center;width:100%;margin-bottom:4px}
.machine{font-family:var(--px);font-size:11.5px;letter-spacing:.1em;color:#1a140b;
  background:linear-gradient(180deg,var(--brass2),var(--brass));padding:3px 9px;border-radius:5px}
.heat{font-size:11px;color:#ffb37b;border:1px solid #7a4526;background:#2b1a10;padding:2px 8px;border-radius:999px}
.time,.loops{font-size:11px;color:var(--muted);border:1px solid var(--line);padding:2px 8px;border-radius:999px}
.craft .grid{display:grid;grid-template-columns:repeat(var(--n),48px);gap:4px}
/* 配方格不再画双层边框：只保留一层底色 */
.cell{border-color:transparent !important;box-shadow:none !important}
.cell .celllink{max-width:34px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;
  font-size:9px;line-height:1.1;display:block;text-align:center;color:#cbb894;text-decoration:none}
.cell.empty{border-color:#3a3024 !important;border-style:dashed !important}
.cell{width:48px;height:48px;background:#100e0b;border:1px solid #2b2419;border-radius:8px;
  display:flex;align-items:center;justify-content:center;position:relative}
.cell img{width:34px;height:34px;image-rendering:pixelated;
  background:#14110c}
.cell em{display:none}
.cell.empty{background:rgba(255,255,255,.025);border:1px dashed #3a3024}
.cell .tagcell{line-height:1.15;font-size:10px;color:var(--muted);padding:2px}
.cell .tagcell.hasi{width:100%;height:100%;display:flex;align-items:center;justify-content:center;padding:0;position:relative}
.cell .tagcell.hasi img{width:32px;height:32px;background:none}
.cell .tagcell.hasi i{position:absolute;right:2px;bottom:0;font-style:normal;font-size:10px;line-height:1;color:var(--brass);text-shadow:0 1px 2px #000}
.ings,.outs{display:flex;gap:8px;flex-wrap:wrap;align-items:center}
.chip{display:inline-flex;align-items:center;gap:7px;background:#100e0b;border:1px solid #2b2419;
  border-radius:9px;padding:5px 9px;font-size:12.5px;color:#e2d6c1}
.chip:hover{border-color:var(--brass);text-decoration:none}
.chip img{width:22px;height:22px;image-rendering:pixelated}
img[src$="_3d.png"]{image-rendering:auto !important}
.chip b{color:var(--brass2);font-size:12px}
.chip.tag{border-style:dashed;color:var(--muted)}
.chip.tag i{font-style:normal;color:var(--brass)}
.chip.fluid{border-color:#2a4a52;color:#a9d6de}
.arrow{color:var(--brass);font-family:var(--px);font-size:18px}
.seq{width:100%;display:flex;gap:6px;flex-wrap:wrap;align-items:center;border-top:1px dashed var(--line);padding-top:8px;margin-top:2px}
.seq-label{font-size:11px;color:var(--muted);letter-spacing:.1em;margin-right:4px}
.step{font-size:11.5px;border:1px solid var(--line);border-radius:999px;padding:2px 9px;color:#cbb894}
.related{display:flex;gap:8px;flex-wrap:wrap;padding-bottom:20px}
.pager{display:flex;justify-content:space-between;gap:12px;border-top:1px solid var(--line);
  margin-top:34px;padding:18px 0 50px;font-size:13px}
.pager a{color:var(--muted)}
.pager a:hover{color:var(--brass2)}
.toast{position:fixed;bottom:26px;left:50%;transform:translateX(-50%) translateY(20px);opacity:0;
  background:#2a2116;border:1px solid var(--brass);color:var(--brass2);padding:8px 16px;border-radius:9px;
  font-size:13px;transition:.25s;pointer-events:none;z-index:50}
.toast.on{opacity:1;transform:translateX(-50%) translateY(0)}
/* ---------- uses (被谁使用) & tag pages ---------- */
.uses-note{color:var(--muted);font-size:13.5px;margin:0 0 12px}
.uses-note b{color:var(--brass2)}
.uses{display:flex;flex-direction:column;gap:12px;max-width:860px}
.use-group{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:12px 14px}
.use-group h3{font-size:13px;color:#e9c98d;margin:0 0 10px;font-weight:600}
.use-group h3 span{color:var(--muted);font-weight:400;font-size:12px}
.uses-chips{display:flex;gap:8px;flex-wrap:wrap}
.cell a.tagcell{color:var(--muted);text-decoration:none;line-height:1.15;font-size:10px;padding:2px}
.cell a.tagcell:hover{color:var(--brass2)}
.hash{color:var(--brass);font-style:normal;margin-right:4px}
.tagcard{display:flex;gap:12px;align-items:center;background:var(--panel);border:1px solid var(--line);
  border-radius:12px;padding:10px 14px;color:var(--text);
  transition:transform .16s ease,border-color .16s ease,box-shadow .16s ease}
.tagcard:hover{border-color:var(--brass);text-decoration:none;transform:translateY(-2px);
  box-shadow:0 10px 22px rgba(0,0,0,.38)}
.tc-img{flex:0 0 auto;display:flex;align-items:center;justify-content:center;width:44px;height:44px;
  background:var(--panel2);border:1px solid var(--line);border-radius:9px}
.tc-img img{width:34px;height:34px;object-fit:contain;image-rendering:pixelated}
.tc-img.none{border-style:dashed}
.tc-img .hash{font-family:var(--px);font-size:20px;color:var(--brass);margin:0;font-style:normal}
.tagcard .t b{display:block;font-size:14px;font-weight:600}
.tagcard .t small{color:var(--muted);font-size:11px;font-family:ui-monospace,Consolas,monospace}
.tagcard .tc{margin-left:auto;display:flex;gap:12px}
.tagcard .tc .unused{color:#6d6152}
.tc span{font-size:11px;color:var(--muted)}
.grid-tags{display:grid;grid-template-columns:repeat(auto-fill,minmax(280px,1fr));gap:12px;padding:22px 0 60px}
.tagsearch{display:flex;align-items:center;gap:12px;margin:0 0 14px}
.tagsearch input{flex:1;max-width:360px;background:var(--panel2);border:1px solid var(--line);color:var(--text);
  border-radius:9px;padding:9px 12px;font-size:14px;outline:none;font-family:inherit}
.tagsearch input:focus{border-color:var(--brass)}
.tagsearch #tagcount{color:var(--muted);font-size:12.5px}
@media(max-width:640px){
  .item-hero .big{width:84px;height:84px}
  .item-hero h1{font-size:23px}
  .recipe{gap:10px;padding:12px}
  .craft .grid{grid-template-columns:repeat(var(--n),40px)}
  .cell,.cell *{box-shadow:none!important;outline:none}
.cell{width:40px;height:40px}
  .cell img{width:28px;height:28px}
}

.flash{animation:flashRing 1s ease-out both}
.flash.card,.flash.tagcard{border-color:rgba(96,178,255,.95)!important}
@keyframes flashRing{
  0%{box-shadow:0 0 0 0 rgba(96,178,255,.95),0 0 26px 8px rgba(60,150,255,.55)}
  35%{box-shadow:0 0 0 3px rgba(96,178,255,.6),0 0 30px 10px rgba(60,150,255,.4)}
  100%{box-shadow:0 0 0 0 rgba(96,178,255,0),0 0 0 0 rgba(60,150,255,0)}
}
  35%{box-shadow:0 0 0 3px rgba(217,164,65,.55),0 0 26px 8px rgba(217,164,65,.35)}
  100%{box-shadow:0 0 0 0 rgba(217,164,65,0),0 0 0 0 rgba(217,164,65,0)}
}
  40%{box-shadow:0 0 0 6px rgba(217,164,65,.18)}100%{box-shadow:0 0 0 0 rgba(217,164,65,0)}}

/* 让「用到它的配方」里的材料 chip 看得出可点 */
.uses-chips a.chip span{text-decoration:underline;text-decoration-style:dotted;
  text-decoration-color:rgba(217,164,65,.35);text-underline-offset:3px}
.uses-chips a.chip:hover{border-color:var(--brass);background:#241d14}
.uses-chips a.chip:hover span{text-decoration-color:var(--brass)}
"""

JS = r"""
(function(){
  var bar=document.querySelector('.searchbar input');
  var cards=[].slice.call(document.querySelectorAll('#list .card'));
  var btns=[].slice.call(document.querySelectorAll('.filters button'));
  var empty=document.querySelector('.empty-msg');
  var cat='all', q='';
  var mod=(new URLSearchParams(location.search)).get('mod')||'';
  var MODS={create:'\u673a\u68b0\u52a8\u529b'};
  function apply(){
    var n=0;
    cards.forEach(function(c){
      var okc=(cat==='all'||c.dataset.cat===cat);
      var okm=!mod||c.dataset.mod===mod;
      var okq=!q||c.dataset.k.indexOf(q)>-1;
      var show=okc&&okq&&okm;
      c.style.display=show?'':'none';
      if(show)n++;
    });
    if(empty)empty.style.display=n?'none':'block';
  }
  (function(){
    if(!mod) return;
    var mb=document.getElementById('modbar'), mn=document.getElementById('modname');
    if(mn) mn.textContent=MODS[mod]||mod;
    if(mb) mb.hidden=false;
  })();
  btns.forEach(function(b){b.addEventListener('click',function(){
    btns.forEach(function(x){x.classList.remove('on')});
    b.classList.add('on'); cat=b.dataset.cat; apply();
  })});
  if(bar){bar.addEventListener('input',function(){q=bar.value.trim().toLowerCase();apply();});}
  (function(){
    var h=location.hash;
    if(h.indexOf('#cat-')===0){
      var c=h.slice(5);
      btns.forEach(function(b){ if(b.dataset.cat===c){ b.click(); } });
    }
  })();
  document.querySelectorAll('.copyid').forEach(function(el){
    el.addEventListener('click',function(){
      var t=el.textContent.trim();
      var done=function(){el.classList.add('ok');el.textContent='已复制';
        setTimeout(function(){el.textContent=t;el.classList.remove('ok')},1200);};
      if(navigator.clipboard&&navigator.clipboard.writeText){navigator.clipboard.writeText(t).then(done,done)}
      else{var ta=document.createElement('textarea');ta.value=t;document.body.appendChild(ta);ta.select();
        try{document.execCommand('copy')}catch(e){}document.body.removeChild(ta);done();}
    });
  });
})();
"""

# ------------------------------------------------------------------ icons
if not os.path.exists(os.path.join(ICONS, "_unknown.png")):
    from PIL import Image, ImageDraw
    im = Image.new("RGBA", (32, 32), (28, 24, 19, 255))
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 31, 31], outline=(90, 72, 48, 255))
    d.ellipse([8, 8, 23, 23], outline=(217, 164, 65, 255), width=2)
    d.line([16, 13, 16, 19], fill=(217, 164, 65, 255), width=3)
    d.point([16, 22], fill=(217, 164, 65, 255))
    im.save(os.path.join(ICONS, "_unknown.png"))

# ------------------------------------------------------------------ pages
os.makedirs(PAGES, exist_ok=True)
order = list(items.keys())
stats = {"hand": 0, "family": 0, "auto": 0}

def head(title, prefix=""):
    return """<!doctype html><html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>%s</title>
<link rel="preload" href="%sassets/fonts/Minecraft.ttf" as="font" crossorigin>
<link rel="stylesheet" href="%sassets/style.css">
</head><body>""" % (esc(title), prefix, prefix)

def topbar(prefix=""):
    return """<header class="top"><div class="wrap">
<a class="logo" href="%sindex.html"><span class="gear"></span><span>CREATE CODEX<small>机械动力图鉴</small></span></a>
<nav><a href="%stags.html">标签</a><a href="https://github.com/Creators-of-Create/Create" target="_blank" rel="noopener">源码</a></nav>
</div></header>""" % (prefix, prefix)

def foot(prefix=""):
    return """<footer><div class="wrap">
<p>数据与图标来自 <a href="https://github.com/Creators-of-Create/Create" target="_blank" rel="noopener">Creators-of-Create/Create</a>（MIT）与 Minecraft 资源，仅用于学习与教学；Minecraft 版权归 Mojang 所有。</p>
<p>标题字体 <a href="https://www.dafont.com/minecraft.font" target="_blank" rel="noopener">Minecraft（dafont.com）</a> · 配方与官方 Ponder 文本来自 Create 模组本地化文件（中文由模组自带）· 教程正文为本项目撰写：功能件逐条编写，同系列装饰件共用家族模板。</p>
</div></footer>
<div class="toast"></div>""" % ()

def toast_script(prefix=""):
    return '<script>%s</script>' % JS

# ---- index
by_cat = {}
for iid, it in items.items():
    by_cat.setdefault(it["cat"], []).append(iid)

cards = []
for iid in sorted(items, key=lambda x: (CAT_ORDER.index(items[x]["cat"]), items[x]["n"])):
    it = items[iid]
    key = (it["n"] + " " + it["en"] + " " + iid).lower()
    cards.append('<a class="card" data-cat="%s" data-mod="%s" data-k="%s" href="items/%s.html">'
                 '<img src="%s" alt="" loading="lazy" decoding="async"><span class="t"><b>%s</b><small>%s</small></span></a>'
                 % (it["cat"], iid.split(":")[0], esc(key), slug(iid), rel_icon(iid), esc(it["n"]), esc(iid)))

chips = ['<button class="on" data-cat="all">全部<span class="cnt">%d</span></button>' % len(items)]
for cid, cname, _ in content.CATEGORIES:
    n = len(by_cat.get(cid, []))
    if n:
        chips.append('<button data-cat="%s">%s<span class="cnt">%d</span></button>' % (cid, cname, n))
if by_cat.get("misc"):
    chips.append('<button data-cat="misc">杂项<span class="cnt">%d</span></button>' % len(by_cat["misc"]))

n_recipes = sum(len(it["recipes"]) for it in items.values())
n_ponder = len([1 for it in items.values() if it["ponder"]])

index_html = head("Create 机械动力图鉴 — 每个物品的教学") + topbar() + """
<main class="wrap">
<div class="hero">
<a class="ballback" href="index.html" title="返回关系图">
  <i class="sphere"></i><span class="lbl">返回关系图</span>
</a>

  <h1>CREATE CODEX<span>机械动力 · 物品教学图鉴</span></h1>
  <p>740 个物品与方块，每一件都写了「怎么获得、怎么用、参数、常见坑」；配方与官方 Ponder 文本直接取自模组本体，教程正文为本站撰写。</p>
  <div class="stats">
    <div class="stat"><b>%d</b><span>物品 / 方块</span></div>
    <div class="stat"><b>%d</b><span>配方条目</span></div>
    <div class="stat"><b>%d</b><span>官方内置教程</span></div>
  </div>
  <div class="searchbar"><span class="ico">⌕</span><input type="search" placeholder="搜索物品名 / 英文名 / ID…" autocomplete="off"></div>
</div>
<div class="filters" id="cats">%s</div>\n<div class="modbar" id="modbar" hidden>当前只显示 <b id="modname"></b> 的物品<a href="catalog.html">显示全部 →</a></div>
<div class="grid-items" id="list">%s</div>
<div class="empty-msg" style="display:none">没有找到匹配的物品，换个关键词试试。</div>
</main>%s%s</body></html>""" % (len(items), n_recipes, n_ponder,
                                "".join(chips), "".join(cards), foot(), toast_script())

WIPE_CSS = """
main.rise{animation:riseIn .58s cubic-bezier(.22,.9,.25,1) both}
@keyframes riseIn{from{transform:translateY(38px);opacity:.15}to{transform:none;opacity:1}}
@media (prefers-reduced-motion: reduce){main.rise{animation:none}}
#wipe{position:fixed;inset:0;z-index:90;background:radial-gradient(circle at 50% 60%,#12100c,#070605 70%);
  animation:wipeUp .52s cubic-bezier(.22,.9,.25,1) forwards;pointer-events:none}
@keyframes wipeUp{0%{transform:translateY(0)}100%{transform:translateY(-101%)}}
@media (prefers-reduced-motion: reduce){#wipe{animation:none;display:none}}
"""
index_html = index_html.replace("</head>", "<style>" + WIPE_CSS + "</style></head>", 1)
index_html = index_html.replace('<main class="wrap rise">', '<div id="wipe"></div>\n<main class="wrap">', 1)
index_html = index_html.replace("</body>", "<script>setTimeout(function(){var w=document.getElementById('wipe');if(w&&w.parentNode)w.parentNode.removeChild(w);},760);</script></body>", 1)
open(os.path.join(SITE, "catalog.html"), "w", encoding="utf-8").write(index_html)

# ---- item pages
for idx, iid in enumerate(order):
    it = items[iid]
    t, kind = tutorial_for(iid)
    stats[kind] += 1
    prev_id = order[idx - 1] if idx > 0 else None
    next_id = order[idx + 1] if idx + 1 < len(order) else None

    parts = [head("%s — Create 机械动力图鉴" % it["n"], "../")]
    parts.append('<header class="top"><div class="wrap">')
    parts.append('<a class="logo" href="../index.html"><span class="gear"></span><span>CREATE CODEX<small>机械动力图鉴</small></span></a>')
    parts.append('<nav><a href="../tags.html">标签</a><a href="https://github.com/Creators-of-Create/Create" target="_blank" rel="noopener">源码</a></nav></div></header>')
    parts.append('<main class="wrap rise">')
    parts.append('<div class="crumb"><a href="../index.html">首页</a> / <a href="../catalog.html">全部物品</a> / %s / <span>%s</span></div>'
                 % (CAT_NAME.get(it["cat"], "杂项"), esc(it["n"])))
    parts.append('<div class="item-hero"><img class="big" src="%s" alt="">' % rel_icon(iid, "../"))
    parts.append('<div><h1>%s</h1><div class="en">%s</div>' % (esc(it["n"]), esc(it["en"])))
    parts.append('<div class="idline"><span class="copyid">%s</span><span class="badge">%s</span>'
                 '<a class="badge" href="../catalog.html#cat-%s">%s</a></div>'
                 % (esc(iid), "方块" if it["kind"] == "block" else "物品",
                    it["cat"], CAT_NAME.get(it["cat"], "杂项")))
    parts.append("</div></div>")
    if t.get("tag"):
        parts.append('<p class="tagline">%s</p>' % esc(t["tag"]))

    if t.get("params"):
        parts.append('<section class="blk"><h2>参数</h2><div class="params">')
        for k, v in t["params"]:
            parts.append('<div class="param"><span>%s</span><b>%s</b></div>' % (esc(k), esc(v)))
        parts.append("</div></section>")

    if t.get("sections"):
        parts.append('<section class="blk"><h2>详细教程</h2><div class="prose">')
        for h, body in t["sections"]:
            parts.append("<h3 style=\"color:#e9c98d;font-size:15px;margin:18px 0 6px\">%s</h3>" % esc(h))
            parts.append(body)
        parts.append("</div></section>")

    if it["recipes"]:
        parts.append('<section class="blk"><h2>获取方式</h2><div class="recipes">')
        _recs = it["recipes"]
        _pri = {"crafting_shaped": 0, "crafting_shapeless": 1, "mechanical_crafting": 2,
                "sequenced_assembly": 3}
        _recs = sorted(_recs, key=lambda r: (_pri.get(r["type"], 4), r.get("file", "")))
        _show = _recs[:8]
        for r in _show:
            parts.append(recipe_card(r, "../"))
        if len(_recs) > len(_show):
            parts.append('<p class="more-rec">另有 %d 条同类配方未逐条列出（多为不同来源的切石机/熔炼变体）。</p>'
                         % (len(_recs) - len(_show)))
        parts.append("</div></section>")
    else:
        parts.append('<section class="blk"><h2>获取方式</h2><div class="prose">'
                     '<p>这个物品<strong>没有合成配方</strong>：它由工具或机器直接生成/放置'
                     '（例如用扳手、连接器、部署器，或作为其他配方的产物）。具体见上方教程。</p></div></section>')

    parts.append(use_section(iid, "../"))

    for p in items[iid]["ponder"]:
        parts.append('<section class="blk"><h2>官方教程 · %s</h2><ol class="steps">' % esc(p["header"] or "Ponder"))
        for s in p["steps"]:
            parts.append("<li>%s</li>" % esc(s))
        parts.append("</ol></section>")

    rel = t.get("related") or []
    rel = [r for r in rel if r in items][:8]
    if not rel:
        same = [x for x in by_cat.get(it["cat"], []) if x != iid][:6]
        rel = same
    if rel:
        parts.append('<section class="blk"><h2>相关物品</h2><div class="related">')
        for r in rel:
            parts.append('<a class="chip" href="%s.html"><img src="%s" alt="" loading="lazy" decoding="async"><span>%s</span></a>'
                         % (slug(r), rel_icon(r, "../"), esc(items[r]["n"])))
        parts.append("</div></section>")

    parts.append('<div class="pager">')
    if prev_id:
        parts.append('<a href="%s.html">← %s</a>' % (slug(prev_id), esc(items[prev_id]["n"])))
    else:
        parts.append("<span></span>")
    parts.append('<a href="../catalog.html">返回目录</a>')
    if next_id:
        parts.append('<a href="%s.html">%s →</a>' % (slug(next_id), esc(items[next_id]["n"])))
    else:
        parts.append("<span></span>")
    parts.append("</div>")
    parts.append("</main>")
    parts.append(foot("../"))
    parts.append(toast_script("../"))
    parts.append("</body></html>")
    open(os.path.join(PAGES, slug(iid) + ".html"), "w", encoding="utf-8").write("".join(parts))

# ---- tag pages
TAGS_PAGES = os.path.join(SITE, "tags")
os.makedirs(TAGS_PAGES, exist_ok=True)
for tg in used_tags:
    _fname = tg.replace(":", "_").replace("/", "_") + ".html"
    open(os.path.join(TAGS_PAGES, _fname), "w", encoding="utf-8").write(tag_page_html(tg))

_tag_cards = []
for tg in sorted(used_tags, key=lambda t: (-sum(i["count"] for i in tag_used_in.get(t, {}).values()), t)):
    _use_n = sum(info["recipes"] for info in tag_used_in.get(tg, {}).values())
    _mem_n = len(tag_members.get(tg, []))
    _tf = tag_icon(tg)
    _img = ('<img src="assets/icons/%s" alt="" loading="lazy">' % _tf) if _tf else '<i class="hash">#</i>'
    _fname = tg.replace(":", "_").replace("/", "_")
    _key = (tag_label(tg) + " " + tg).replace('"', "")
    _use_txt = ("%d 条配方" % _use_n) if _use_n else "未用于配方"
    _tag_cards.append('<a class="tagcard" data-k="%s" href="tags/%s.html"><span class="tc-img%s">%s</span>'
                      '<span class="t"><b>%s</b><small>%s</small></span>'
                      '<span class="tc"><span class="%s">%s</span><span>%d 成员</span></span></a>'
                      % (_key, _fname, "" if _tf else " none", _img,
                         esc(tag_label(tg)), esc(tg), "" if _use_n else "unused", _use_txt, _mem_n))

_tags_html = head("标签索引 — Create 机械动力图鉴", "") + topbar() + """
<main class="wrap">
<div class="hero">
  <h1>标签索引<span>TAGS · 配方标签</span></h1>
  <p>共 <b>%d</b> 个标签：Create 配方用到的，加上常见的原版标签。点标签名查看详情。原版物品属于哪些标签，看 <a href="vanilla.html">原版物品的标签 →</a></p>
</div>
<div class="tagsearch"><input id="tagq" type="search" placeholder="搜索标签名 / ID…" autocomplete="off"><span id="tagcount">%d 个标签</span></div>
<div class="grid-tags" id="list">%s</div>
</main>%s%s<script>
(function(){var q=document.getElementById('tagq'),cnt=document.getElementById('tagcount'),
cards=[].slice.call(document.querySelectorAll('.tagcard'));
q.addEventListener('input',function(){var s=q.value.trim().toLowerCase(),n=0;
cards.forEach(function(el){var k=(el.getAttribute('data-k')||'').toLowerCase();
var ok=!s||k.indexOf(s)>-1;el.style.display=ok?'':'none';if(ok)n++;});
cnt.textContent=n+' 个标签';});})();
</script></body></html>""" % (len(used_tags), len(used_tags), "".join(_tag_cards), foot(), toast_script())
open(os.path.join(SITE, "tags.html"), "w", encoding="utf-8").write(_tags_html)

# ---- assets
os.makedirs(os.path.join(SITE, "assets", "css"), exist_ok=True)
os.makedirs(os.path.join(SITE, "assets", "js"), exist_ok=True)
os.makedirs(os.path.join(SITE, "assets", "fonts"), exist_ok=True)

BALL_CSS = """

/* 图鉴页左侧的棱面玻璃球：返回关系图 */
.hero{position:relative}
.ballback{position:absolute;left:calc(50% - 505px);top:46%;transform:translateY(-50%);
  display:block;text-decoration:none;text-align:center;width:120px;z-index:2}
.ballback .sphere{display:block;width:120px;height:120px;
  background-image:url(icons/ball_sheet.png);background-size:14400px 120px;background-repeat:no-repeat;
  animation:ballspin 16s steps(120) infinite;
  filter:drop-shadow(0 8px 18px rgba(0,0,0,.55));transition:transform .25s ease}
.ballback .lbl{display:block;margin-top:8px;font-size:11.5px;letter-spacing:.16em;color:#9c8f7c}
.ballback:hover .sphere{transform:scale(1.06);
  filter:drop-shadow(0 8px 22px rgba(0,0,0,.6)) drop-shadow(0 0 10px rgba(240,200,116,.55))}
.ballback:hover .lbl{color:var(--brass2)}
@keyframes ballspin{from{background-position:0 0}to{background-position:-14400px 0}}
@media (max-width:1180px){.ballback{display:none}}

/* 附属页：返回关系图 */
.backbtn{margin-left:auto;display:inline-flex;align-items:center;gap:6px;padding:7px 14px;border-radius:999px;
  border:1px solid rgba(217,164,65,.45);color:#e8d7b4;text-decoration:none;font-size:12.5px;
  letter-spacing:.06em;background:rgba(217,164,65,.06);transition:.18s}
.backbtn:hover{color:#1a1409;background:var(--brass2);border-color:var(--brass2);
  box-shadow:0 0 18px rgba(240,200,116,.35)}
"""

open(os.path.join(SITE, "assets", "style.css"), "w", encoding="utf-8").write(CSS + BALL_CSS)
open(os.path.join(SITE, "assets", "app.js"), "w", encoding="utf-8").write(JS)
if os.path.exists(os.path.join(SITE, "assets", "fonts", "Minecraft.ttf")) is False:
    src = os.path.join(os.environ.get("TEMP", "."), "mc_font", "Minecraft.ttf")
    if os.path.exists(src):
        shutil.copyfile(src, os.path.join(SITE, "assets", "fonts", "Minecraft.ttf"))

# font-face
open(os.path.join(SITE, "assets", "font.css"), "w", encoding="utf-8").write(
    "@font-face{font-family:'Minecraft';src:url('fonts/Minecraft.ttf') format('truetype');"
    "font-weight:400;font-display:swap}\n")

print("pages:", len(order), "| tutorials:", stats)
print("categories:", {c: len(v) for c, v in by_cat.items()})




