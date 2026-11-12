# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""通用附属页生成器：一个模组 → 一页（物品卡 + 配方）。"""
import io
import json
import os
import re
import shutil
import urllib.request as u
import zipfile

SITE = ROOT
ICONS = os.path.join(SITE, 'assets', 'icons')
MC_ZH = {}
try:
    _mz = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "mc_zh.json"), encoding="utf-8"))
    MC_ZH = {k: v for k, v in _mz.items() if isinstance(v, str)}
except Exception:
    MC_ZH = {}

RAW = _os.path.join(WORK, 'mods_intake')

SEAT_ZH = {}
for _c, _z in {'black': '黑色', 'blue': '蓝色', 'brown': '棕色', 'cyan': '青色', 'gray': '灰色', 'green': '绿色', 'light_blue': '浅蓝色', 'light_gray': '浅灰色', 'lime': '黄绿色', 'magenta': '品红色', 'orange': '橙色', 'pink': '粉色', 'purple': '紫色', 'red': '红色', 'white': '白色', 'yellow': '黄色'}.items():
    SEAT_ZH[_c + '_modern_seat'] = _z + '现代座椅'
    SEAT_ZH[_c + '_floor_seat'] = _z + '地板椅'

MODS = [
    dict(slug='apokinetics', ns='apokinetics', title='Create: Apokinetics',
         tag='Create: Apokinetics',
         intro='来自 mcmod 1.20.1 附属模组清单，共 6 个物品。',
         groups=[]),
    dict(slug='cbc-chemical-warfare', ns='cbc_cw', title='CBC: Chemical Warfare',
         tag='CBC: Chemical Warfare',
         intro='来自 mcmod 1.20.1 附属模组清单，共 91 个物品。',
         groups=[]),
    dict(slug='cbc-nuclear', ns='cbc_nukes', title='CBC: Nuclear',
         tag='CBC: Nuclear',
         intro='来自 mcmod 1.20.1 附属模组清单，共 1 个物品。',
         groups=[]),
    dict(slug='cccbridge', ns='cccbridge', title='CC:C Bridge',
         tag='CC:C Bridge',
         intro='来自 mcmod 1.20.1 附属模组清单，共 10 个物品。',
         groups=[]),
    dict(slug='cp-tweaks', ns='cp_tweaks', title='Create Planetary Tweaks',
         tag='Create Planetary Tweaks',
         intro='来自 mcmod 1.20.1 附属模组清单，共 109 个物品。',
         groups=[]),
    dict(slug='create-amazing-trading', ns='amazingtrading', title='Create: Amazing Trading',
         tag='Create: Amazing Trading',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='create-applied-kinetics', ns='createappliedkinetics', title='Create: Applied Kinetics',
         tag='Create: Applied Kinetics',
         intro='来自 mcmod 1.20.1 附属模组清单，共 13 个物品。',
         groups=[]),
    dict(slug='create-aquatic-ambitions', ns='create_aquatic_ambitions', title='Create: Aquatic Ambitions',
         tag='Create: Aquatic Ambitions',
         intro='来自 mcmod 1.20.1 附属模组清单，共 8 个物品。',
         groups=[]),
    dict(slug='create-biotech', ns='create_biotech', title='Create: Biotech - 机械动力：生物科技',
         tag='Create: Biotech - 机械动力：生物科技',
         intro='来自 mcmod 1.20.1 附属模组清单，共 180 个物品。',
         groups=[]),
    dict(slug='create-bitterballen', ns='create_bic_bit', title='Create: Bitterballen',
         tag='Create: Bitterballen',
         intro='来自 mcmod 1.20.1 附属模组清单，共 74 个物品。',
         groups=[]),
    dict(slug='create-cardboard-things', ns='createcardboardthings', title='Create: Cardboard Things',
         tag='Create: Cardboard Things',
         intro='来自 mcmod 1.20.1 附属模组清单，共 9 个物品。',
         groups=[]),
    dict(slug='create-clothes', ns='createclothes', title='Create: Clothes',
         tag='Create: Clothes',
         intro='来自 mcmod 1.20.1 附属模组清单，共 58 个物品。',
         groups=[]),
    dict(slug='create-cobblemon-industrialized', ns='create_cobblemon', title='Create: Cobblemon Industrialized',
         tag='Create: Cobblemon Industrialized',
         intro='来自 mcmod 1.20.1 附属模组清单，共 103 个物品。',
         groups=[]),
    dict(slug='create-cobblestone', ns='createcobblestone', title='Create Cobblestone',
         tag='Create Cobblestone',
         intro='来自 mcmod 1.20.1 附属模组清单，共 3 个物品。',
         groups=[]),
    dict(slug='create-colored-packages', ns='colored_packages', title='Create: Colored Packages',
         tag='Create: Colored Packages',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='create-compact_transmission', ns='create_compact_transmission', title='Create: Compact Transmission',
         tag='Create: Compact Transmission',
         intro='来自 mcmod 1.20.1 附属模组清单，共 15 个物品。',
         groups=[]),
    dict(slug='create-cultivation-craft', ns='create_cultivation', title='Create: Cultivation Craft',
         tag='Create: Cultivation Craft',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='create-deepfried', ns='create_deepfried', title='Create: Deepfried',
         tag='Create: Deepfried',
         intro='来自 mcmod 1.20.1 附属模组清单，共 56 个物品。',
         groups=[]),
    dict(slug='create-factory-controller', ns='createfactorycontroller', title='Create: Factory Controller',
         tag='Create: Factory Controller',
         intro='来自 mcmod 1.20.1 附属模组清单，共 9 个物品。',
         groups=[]),
    dict(slug='create-fantasizing-again', ns='create_fantasizing', title='Create: Fantasizing Again',
         tag='Create: Fantasizing Again',
         intro='来自 mcmod 1.20.1 附属模组清单，共 36 个物品。',
         groups=[]),
    dict(slug='create-food', ns='createfood', title='Create: Food',
         tag='Create: Food',
         intro='来自 mcmod 1.20.1 附属模组清单，共 1873 个物品。',
         groups=[]),
    dict(slug='create-garnished', ns='garnished', title='Create: Garnished',
         tag='Create: Garnished',
         intro='来自 mcmod 1.20.1 附属模组清单，共 1076 个物品。',
         groups=[]),
    dict(slug='create-guardian-beam-defense', ns='creategbd', title='Create Guardian Beam Defense',
         tag='Create Guardian Beam Defense',
         intro='来自 mcmod 1.20.1 附属模组清单，共 21 个物品。',
         groups=[]),
    dict(slug='create-hand-crafting', ns='create_hc', title='Create Hand Crafting - 1.18.2 - 1.20.1',
         tag='Create Hand Crafting - 1.18.2 - 1.20.1',
         intro='来自 mcmod 1.20.1 附属模组清单，共 7 个物品。',
         groups=[]),
    dict(slug='create-high-pressure', ns='create_high_pressure', title='Create: High Pressure',
         tag='Create: High Pressure',
         intro='来自 mcmod 1.20.1 附属模组清单，共 3 个物品。',
         groups=[]),
    dict(slug='create-horse-power', ns='createhorsepower', title='Create Horse Power',
         tag='Create Horse Power',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='create-ironworks', ns='create_ironworks', title='Create: Ironworks',
         tag='Create: Ironworks',
         intro='来自 mcmod 1.20.1 附属模组清单，共 81 个物品。',
         groups=[]),
    dict(slug='create-let-the-adventure-begin', ns='create_ltab', title='Create: Let The Adventure Begin',
         tag='Create: Let The Adventure Begin',
         intro='来自 mcmod 1.20.1 附属模组清单，共 5 个物品。',
         groups=[]),
    dict(slug='create-logistics', ns='create_logistics', title='Create Logistics',
         tag='Create Logistics',
         intro='来自 mcmod 1.20.1 附属模组清单，共 3 个物品。',
         groups=[]),
    dict(slug='create-love-war', ns='createloveandwar', title='Create: Love & War',
         tag='Create: Love & War',
         intro='来自 mcmod 1.20.1 附属模组清单，共 327 个物品。',
         groups=[]),
    dict(slug='create-mechanical-chicken', ns='create_mechanical_chicken', title='Create Mechanical Chicken',
         tag='Create Mechanical Chicken',
         intro='来自 mcmod 1.20.1 附属模组清单，共 5 个物品。',
         groups=[]),
    dict(slug='create-mechanical-companion', ns='createmechanicalcompanion', title='Create: Mechanical Companion',
         tag='Create: Mechanical Companion',
         intro='来自 mcmod 1.20.1 附属模组清单，共 41 个物品。',
         groups=[]),
    dict(slug='create-mechanical-spawner', ns='create_mechanical_spawner', title='Create Mechanical Spawner',
         tag='Create Mechanical Spawner',
         intro='来自 mcmod 1.20.1 附属模组清单，共 58 个物品。',
         groups=[]),
    dict(slug='create-metallurgy', ns='createmetallurgy', title='Create: Metallurgy',
         tag='Create: Metallurgy',
         intro='来自 mcmod 1.20.1 附属模组清单，共 129 个物品。',
         groups=[]),
    dict(slug='create-metalwork', ns='createmetalwork', title='Create: Metalwork',
         tag='Create: Metalwork',
         intro='来自 mcmod 1.20.1 附属模组清单，共 208 个物品。',
         groups=[]),
    dict(slug='create-militarized', ns='create_militarized_', title='Create Militarized',
         tag='Create Militarized',
         intro='来自 mcmod 1.20.1 附属模组清单，共 160 个物品。',
         groups=[]),
    dict(slug='create-mobile-packages', ns='create_mobile_packages', title='Create: Mobile Packages',
         tag='Create: Mobile Packages',
         intro='来自 mcmod 1.20.1 附属模组清单，共 17 个物品。',
         groups=[]),
    dict(slug='create-molten-metals', ns='molten_metals', title='Create: Molten Metals',
         tag='Create: Molten Metals',
         intro='来自 mcmod 1.20.1 附属模组清单，共 66 个物品。',
         groups=[]),
    dict(slug='create-more-drill-heads', ns='createmoredrillheads', title='Create: More Drill Heads',
         tag='Create: More Drill Heads',
         intro='来自 mcmod 1.20.1 附属模组清单，共 33 个物品。',
         groups=[]),
    dict(slug='create-more-sandpapers', ns='createsandpapers', title='Create: More Sandpapers',
         tag='Create: More Sandpapers',
         intro='来自 mcmod 1.20.1 附属模组清单，共 80 个物品。',
         groups=[]),
    dict(slug='create-netherite-additions', ns='create_nj', title='Create Stuff & Netherite Additions',
         tag='Create Stuff & Netherite Additions',
         intro='来自 mcmod 1.20.1 附属模组清单，共 5 个物品。',
         groups=[]),
    dict(slug='create-netherless', ns='create_netherless', title='Create: Netherless',
         tag='Create: Netherless',
         intro='来自 mcmod 1.20.1 附属模组清单，共 5 个物品。',
         groups=[]),
    dict(slug='create-northstar', ns='northstar', title='Create: Northstar',
         tag='Create: Northstar',
         intro='来自 mcmod 1.20.1 附属模组清单，共 387 个物品。',
         groups=[]),
    dict(slug='create-nuke', ns='create_nuke', title='Create: Nuke',
         tag='Create: Nuke',
         intro='来自 mcmod 1.20.1 附属模组清单，共 6 个物品。',
         groups=[]),
    dict(slug='create-optical', ns='create_optical', title='Create Optical',
         tag='Create Optical',
         intro='来自 mcmod 1.20.1 附属模组清单，共 21 个物品。',
         groups=[]),
    dict(slug='create-ornithopter-glider', ns='createornithopterglider', title='Create: Ornithopter Glider',
         tag='Create: Ornithopter Glider',
         intro='来自 mcmod 1.20.1 附属模组清单，共 34 个物品。',
         groups=[]),
    dict(slug='create-peaceful', ns='create_peaceful', title='Create: Peaceful',
         tag='Create: Peaceful',
         intro='来自 mcmod 1.20.1 附属模组清单，共 3 个物品。',
         groups=[]),
    dict(slug='create-pipe-networks', ns='pipe_networks', title='Create: Pipe Networks',
         tag='Create: Pipe Networks',
         intro='来自 mcmod 1.20.1 附属模组清单，共 384 个物品。',
         groups=[]),
    dict(slug='create-pneumatic-equipment', ns='create_pneuequip', title='Create: pneumatic equipment',
         tag='Create: pneumatic equipment',
         intro='来自 mcmod 1.20.1 附属模组清单，共 28 个物品。',
         groups=[]),
    dict(slug='create-protection-pixel', ns='protection_pixel', title='Create: Protection Pixel',
         tag='Create: Protection Pixel',
         intro='来自 mcmod 1.20.1 附属模组清单，共 183 个物品。',
         groups=[]),
    dict(slug='create-ratatouille', ns='ratatouille', title='Create Ratatouille',
         tag='Create Ratatouille',
         intro='来自 mcmod 1.20.1 附属模组清单，共 58 个物品。',
         groups=[]),
    dict(slug='create-remote-terminal', ns='createterminal', title='Create: Remote Terminal',
         tag='Create: Remote Terminal',
         intro='来自 mcmod 1.20.1 附属模组清单，共 6 个物品。',
         groups=[]),
    dict(slug='create-simple-generator', ns='create_simple_generator', title='Create: Simple Generator',
         tag='Create: Simple Generator',
         intro='来自 mcmod 1.20.1 附属模组清单，共 1 个物品。',
         groups=[]),
    dict(slug='create-stock-bridge', ns='createstockbridge', title='Create Stock Bridge',
         tag='Create Stock Bridge',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='create-tacz-automation', ns='createtaczauto', title='Create: TaCZ Automation',
         tag='Create: TaCZ Automation',
         intro='来自 mcmod 1.20.1 附属模组清单，共 33 个物品。',
         groups=[]),
    dict(slug='create-tank-defenses', ns='create_tank_defenses', title='Create: Tank Defenses',
         tag='Create: Tank Defenses',
         intro='来自 mcmod 1.20.1 附属模组清单，共 969 个物品。',
         groups=[]),
    dict(slug='create-totem-factory', ns='totemfactory', title='Create: Totem Factory',
         tag='Create: Totem Factory',
         intro='来自 mcmod 1.20.1 附属模组清单，共 24 个物品。',
         groups=[]),
    dict(slug='create-tweaked-controllers', ns='create_tweaked_controllers', title='Create: Tweaked Controllers',
         tag='Create: Tweaked Controllers',
         intro='来自 mcmod 1.20.1 附属模组清单，共 12 个物品。',
         groups=[]),
    dict(slug='create-unify', ns='unify', title='Create: Unify',
         tag='Create: Unify',
         intro='来自 mcmod 1.20.1 附属模组清单，共 130 个物品。',
         groups=[]),
    dict(slug='create-vintage-improvements', ns='vintageimprovements', title='Create: Vintage Improvements',
         tag='Create: Vintage Improvements',
         intro='来自 mcmod 1.20.1 附属模组清单，共 263 个物品。',
         groups=[]),
    dict(slug='create-weaponry', ns='create_wt', title='Create Weaponry',
         tag='Create Weaponry',
         intro='来自 mcmod 1.20.1 附属模组清单，共 253 个物品。',
         groups=[]),
    dict(slug='create-wizardry', ns='create_wizardry', title='Create: Wizardry',
         tag='Create: Wizardry',
         intro='来自 mcmod 1.20.1 附属模组清单，共 8 个物品。',
         groups=[]),
    dict(slug='createadvlogistics', ns='createadvlogistics', title='Create: Advanced Logistics',
         tag='Create: Advanced Logistics',
         intro='来自 mcmod 1.20.1 附属模组清单，共 6 个物品。',
         groups=[]),
    dict(slug='createlights-controls', ns='create_lac', title='Create: Lights & Controls',
         tag='Create: Lights & Controls',
         intro='来自 mcmod 1.20.1 附属模组清单，共 184 个物品。',
         groups=[]),
    dict(slug='createnuclear', ns='createnuclear', title='Create Nuclear',
         tag='Create Nuclear',
         intro='来自 mcmod 1.20.1 附属模组清单，共 127 个物品。',
         groups=[]),
    dict(slug='createtools-n-weapons', ns='create_tools_n_weapons', title='Create: Tools n Weapons',
         tag='Create: Tools n Weapons',
         intro='来自 mcmod 1.20.1 附属模组清单，共 6 个物品。',
         groups=[]),
    dict(slug='creating-space', ns='creatingspace', title='Creating Space',
         tag='Creating Space',
         intro='来自 mcmod 1.20.1 附属模组清单，共 78 个物品。',
         groups=[]),
    dict(slug='deep_space', ns='deep_space', title='Deep Space',
         tag='Deep Space',
         intro='来自 mcmod 1.20.1 附属模组清单，共 10 个物品。',
         groups=[]),
    dict(slug='delivery-director', ns='delivery_director', title='Create: Delivery Director [Discontinued]',
         tag='Create: Delivery Director [Discontinued]',
         intro='来自 mcmod 1.20.1 附属模组清单，共 1 个物品。',
         groups=[]),
    dict(slug='direct-chute', ns='direct_chute', title='Create: Direct Chute',
         tag='Create: Direct Chute',
         intro='来自 mcmod 1.20.1 附属模组清单，共 1 个物品。',
         groups=[]),
    dict(slug='ethium', ns='ethium_reimagined', title='Create: Ethium Reimagined',
         tag='Create: Ethium Reimagined',
         intro='来自 mcmod 1.20.1 附属模组清单，共 34 个物品。',
         groups=[]),
    dict(slug='expandingtechnologies', ns='expandingtechnologies', title='Expanding Technologies',
         tag='Expanding Technologies',
         intro='来自 mcmod 1.20.1 附属模组清单，共 4 个物品。',
         groups=[]),
    dict(slug='extended-wrenches', ns='extendedwrenches', title='Create: Extended Wrenches',
         tag='Create: Extended Wrenches',
         intro='来自 mcmod 1.20.1 附属模组清单，共 6 个物品。',
         groups=[]),
    dict(slug='extra-gauges', ns='extra_gauges', title='Create: Extra Gauges',
         tag='Create: Extra Gauges',
         intro='来自 mcmod 1.20.1 附属模组清单，共 8 个物品。',
         groups=[]),
    dict(slug='fishy-create-stuffs', ns='fishycreatestuffs', title='Fishy Create Stuffs',
         tag='Fishy Create Stuffs',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='frequency-create', ns='frequency', title='Frequency Create',
         tag='Frequency Create',
         intro='来自 mcmod 1.20.1 附属模组清单，共 83 个物品。',
         groups=[]),
    dict(slug='greate', ns='greate', title='Greate',
         tag='Greate',
         intro='来自 mcmod 1.20.1 附属模组清单，共 226 个物品。',
         groups=[]),
    dict(slug='has-basin-output-faucet-depot', ns='hasbasinoutputfaucetdepot', title='Has Basin Output Faucet Depot',
         tag='Has Basin Output Faucet Depot',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='hypertube', ns='create_hypertube', title='Create: Hypertubes',
         tag='Create: Hypertubes',
         intro='来自 mcmod 1.20.1 附属模组清单，共 6 个物品。',
         groups=[]),
    dict(slug='interactive', ns='create_interactive', title='Create: Interactive',
         tag='Create: Interactive',
         intro='来自 mcmod 1.20.1 附属模组清单，共 5 个物品。',
         groups=[]),
    dict(slug='klinksnklangs', ns='create_klinks_n_klangs', title='Create: Klinks n\' Klangs',
         tag='Create: Klinks n\' Klangs',
         intro='来自 mcmod 1.20.1 附属模组清单，共 119 个物品。',
         groups=[]),
    dict(slug='lijms-expanse', ns='lijms_expanse', title='Lijm\'s Expanse',
         tag='Lijm\'s Expanse',
         intro='来自 mcmod 1.20.1 附属模组清单，共 71 个物品。',
         groups=[]),
    dict(slug='missions', ns='missions', title='Create: Missions',
         tag='Create: Missions',
         intro='来自 mcmod 1.20.1 附属模组清单，共 2 个物品。',
         groups=[]),
    dict(slug='more-create-burners', ns='moreburners', title='More Create Burners',
         tag='More Create Burners',
         intro='来自 mcmod 1.20.1 附属模组清单，共 8 个物品。',
         groups=[]),
    dict(slug='neokuayue', ns='kuayue', title='NeoKuayue',
         tag='NeoKuayue',
         intro='来自 mcmod 1.20.1 附属模组清单，共 791 个物品。',
         groups=[]),
    dict(slug='northstar-redux', ns='northstar', title='Create: Northstar - Redux',
         tag='Create: Northstar - Redux',
         intro='来自 mcmod 1.20.1 附属模组清单，共 423 个物品。',
         groups=[]),
    dict(slug='petrols-parts', ns='petrolsparts', title='Petrol\'s Parts',
         tag='Petrol\'s Parts',
         intro='来自 mcmod 1.20.1 附属模组清单，共 13 个物品。',
         groups=[]),
    dict(slug='precise-manufacturing', ns='prma', title='[TACZ] Create: Precise Manufacturing',
         tag='[TACZ] Create: Precise Manufacturing',
         intro='来自 mcmod 1.20.1 附属模组清单，共 155 个物品。',
         groups=[]),
    dict(slug='so-crazy-try', ns='so_crazy_try', title='So crazy try',
         tag='So crazy try',
         intro='来自 mcmod 1.20.1 附属模组清单，共 22 个物品。',
         groups=[]),
    dict(slug='tinkers-gears', ns='tgears', title='Tinkers\' Gears',
         tag='Tinkers\' Gears',
         intro='来自 mcmod 1.20.1 附属模组清单，共 57 个物品。',
         groups=[]),
    dict(slug='tofu-create', ns='tofucreate', title='Tofu Create',
         tag='Tofu Create',
         intro='来自 mcmod 1.20.1 附属模组清单，共 5 个物品。',
         groups=[]),
    dict(slug='trackwork', ns='trackwork', title='Trackwork',
         tag='Trackwork',
         intro='来自 mcmod 1.20.1 附属模组清单，共 28 个物品。',
         groups=[]),
    dict(slug='train-deco', ns='traindeco', title='Create: Train Deco',
         tag='Create: Train Deco',
         intro='来自 mcmod 1.20.1 附属模组清单，共 66 个物品。',
         groups=[]),
    dict(slug='cbcmodernwarfare', ns='cbcmodernwarfare', title='CBC: Modern Warfare',
         tag='把机械动力火炮推向现代战争',
         intro='给 Create Big Cannons 加现代火器：自动火炮、坦克炮、弹道计算与配套弹药，'
               '保留原本的装药与仰角机制，只是把时代往后推了一个世纪。',
         groups=[('火炮与炮塔', ('cannon', 'turret', 'barrel', 'breech', 'mount')),
                 ('弹药', ('shell', 'round', 'cartridge', 'ap', 'he', 'heat')),
                 ('机构与配件', ('loader', 'autoloader', 'sight', 'rammer')),
                 ('材料', ('steel', 'ingot', 'plate', 'sheet'))]),
    dict(slug='quality-railway', ns='qr', title='Quality Railway',
         tag='135 件把铁路做成完整交通系统',
         intro='大型铁路扩展：信号联锁、道岔控制、站台设备、列车调度，配一整套按颜色分套的装饰块。'
               '想做一张真正能跑时刻表的铁路网，这个是首选。',
         groups=[('信号与联锁', ('signal', 'interlock', 'switch', 'block', 'balise')),
                 ('站台设备', ('platform', 'station', 'ticket', 'board', 'clock')),
                 ('轨道与道岔', ('track', 'rail', 'turnout', 'buffer')),
                 ('装饰块', ('plate', 'brick', 'tile', 'slab', 'stairs', 'wall'))]),
    dict(slug='create-confectionery', ns='create_confectionery', title='Create Confectionery',
         tag='87 件把甜食做成自动化产线',
         intro='巧克力、糖果、棉花糖一整套：可可豆研磨、糖浆熬制、成型与冷却都接进 Create 的传动，'
               '成品可以直接摆成商店货架。',
         groups=[('巧克力', ('chocolate', 'cocoa', 'cacao', 'praline')),
                 ('糖果', ('candy', 'cane', 'lollipop', 'marshmallow', 'gummy')),
                 ('机器', ('mixer', 'press', 'mold', 'fridge', 'cooker'))]),
    dict(slug='create-qol', ns='createqol', title='Create: Quality of Life',
         tag='78 件补足日常操作的小工具',
         intro='不是新机器，而是把 Create 里那些反复做的操作变简单：批量放置、快速配置、'
               '一键复制设置、工具耐久与范围优化。',
         groups=[('工具', ('wrench', 'tool', 'wand', 'hammer', 'screwdriver')),
                 ('便捷设备', ('remote', 'terminal', 'controller', 'linker')),
                 ('杂项', ('block', 'item', 'component'))]),
    dict(slug='create-alloyed', ns='alloyed', title='Alloyed',
         tag='37 件钢铁与合金冶炼',
         intro='补上 Create 缺的钢铁链：生铁、钢锭、不锈钢，配一整套冶炼与轧制机器，'
               '是很多后期机器的前置材料。',
         groups=[('合金', ('steel', 'bronze', 'brass', 'alloy', 'stainless')),
                 ('冶炼机器', ('furnace', 'crucible', 'forge', 'blast', 'mill')),
                 ('材料形态', ('ingot', 'nugget', 'sheet', 'rod', 'block'))]),
    dict(slug='create-armory', ns='createarmory', title='Create: Armory',
         tag='65 件用机械动力造军械',
         intro='一套武器装备：枪械、弹药、护甲，全部通过动力合成器制造，'
               '和 Create 的产线整合而不是独立一套工作台。',
         groups=[('武器', ('gun', 'rifle', 'pistol', 'cannon', 'blade')),
                 ('弹药', ('ammo', 'bullet', 'magazine', 'shell')),
                 ('护甲', ('armor', 'helmet', 'chestplate', 'boots'))]),
    dict(slug='create-teleporters', ns='createteleporters', title='Create: Teleporters',
         tag='47 件用动力驱动的传送装置',
         intro='把 Create 的应力接到空间传送上：传送门、定位器、频率匹配器，'
               '可以做点对点的固定传送网络。',
         groups=[('传送设备', ('teleporter', 'portal', 'pad', 'anchor')),
                 ('频率与定位', ('frequency', 'locator', 'beacon', 'antenna')),
                 ('配件', ('core', 'coil', 'circuit'))]),
    dict(slug='rainbowcompound', ns='rainbowcompound', title='Create: Rainbow Compound',
         tag='88 件彩虹系材料与机器',
         intro='一套以彩虹化合物为核心的材料链：染料合成、光谱分解、多彩装饰块，'
               '视觉风格比本体更花哨。',
         groups=[('彩虹材料', ('rainbow', 'prism', 'spectrum', 'chromatic')),
                 ('机器', ('mixer', 'press', 'crusher', 'saw')),
                 ('装饰', ('block', 'brick', 'tile', 'glass'))]),
    dict(slug='compressedcreativity', ns='compressedcreativity', title='Compressed Creativity',
         tag='35 件压缩空气驱动装置',
         intro='一套以压缩空气为介质的机械：压缩机、气缸、气动马达、气管，'
               '能量密度比传动轴高，适合远程布线。',
         groups=[('压缩与储存', ('compressor', 'tank', 'air', 'pressure')),
                 ('气动机械', ('piston', 'cylinder', 'motor', 'turbine')),
                 ('管路与配件', ('pipe', 'tube', 'valve', 'gauge'))]),
    dict(slug='create-crystal-clear', ns='crystal_clear', title='Create: Crystal Clear',
         tag='32 件玻璃与透明建材',
         intro='一套 Create 风格的玻璃体系：透明机壳、玻璃管、防爆玻璃、彩色玻璃板，'
               '做展示柜和观察窗时用。',
         groups=[('玻璃', ('glass', 'pane', 'window')),
                 ('透明机壳', ('casing', 'tube', 'pipe')),
                 ('配件', ('frame', 'edge', 'corner'))]),
    dict(slug='create-steam-powered', ns='steampowered', title='Create: Steam Powered',
         tag='26 件蒸汽动力设备',
         intro='早期的蒸汽机扩展：锅炉、蒸汽管道、活塞、汽笛，'
               '在电力普及前提供另一种供能思路。',
         groups=[('蒸汽设备', ('steam', 'boiler', 'piston', 'whistle')),
                 ('管路', ('pipe', 'valve', 'gauge'))]),
    dict(slug='create-basic-additions', ns='create_basic_additions', title='Create: Basic Additions',
         tag='26 件基础级补件',
         intro='一批入门级零件与方块，填 Create 本体在基础阶段缺的那些小东西。',
         groups=[('零件', ('gear', 'rod', 'sheet', 'bolt')),
                 ('方块', ('block', 'slab', 'stairs'))]),
    dict(slug='create-molten-vents', ns='molten_vents', title='Create: Molten Vents',
         tag='12 件可再生的熔岩喷口',
         intro='在世界里生成熔岩喷口，接上钻机就能持续产出熔岩——一种可再生的能源。',
         groups=[('喷口', ('vent', 'molten', 'lava')),
                 ('开采', ('drill', 'pump', 'extractor'))]),
    dict(slug='create-copies-cats', ns='copiescats', title='Create: Copies & Cats',
         tag='8 件伪装与猫咪小物',
         intro='一个小趣味模组：伪装方块和几只可以摆在工厂里的猫。',
         groups=[]),
    dict(slug='create-ender-transmission', ns='createendertransmission', title='Create: Ender Transmission',
         tag='4 件跨维度传动',
         intro='只做一件事：把应力通过末影链路传到远处甚至另一个维度，省掉长距离传动轴。',
         groups=[]),
    dict(slug='create-sifting', ns='createsifter', title='Create Sifting',
         tag='6 件动力筛矿',
         intro='把筛子接上动力，自动筛砂砾与尘土出矿，是前期资源的一个补充来源。',
         groups=[]),
    dict(slug='ars-creo', ns='ars_creo', title='Ars Creo',
         tag='1 件 Ars Nouveau 与 Create 的接口',
         intro='只加一个方块：把 Ars Nouveau 的魔法能量和 Create 的应力互相转换。',
         groups=[]),
    dict(slug='create-mechanical-extruder', ns='create_mechanical_extruder', title='Create Mechanical Extruder',
         tag='1 件无限刷石机',
         intro='只加一个方块：接上动力后持续产出圆石，最省事的无限石料方案。',
         groups=[]),
    dict(slug='balancedflight', ns='balancedflight', title='Create: BalancedFlight',
         tag='2 件飞行配平件',
         intro='给 Create 的飞行载具加配平与稳定组件，让操控不那么飘。',
         groups=[]),
    dict(slug='create-refilling-boxes', ns='create_refilling_boxes', title='Create: Refilling Boxes',
         tag='3 件自动补货箱',
         intro='箱子空了自动从库存补满，做长时间运行的产线时省心。',
         groups=[]),
    dict(slug='createoplenty', ns='createoplenty', title="Create: Create O' Plenty",
         tag='3 件 BOP 联动配方',
         intro='把超多生物群系的木材接进 Create 的加工链，让它的木头也能做机壳和传动件。',
         groups=[]),
    dict(slug='create-central-kitchen', ns='create_central_kitchen', title='Create: Central Kitchen',
         tag='把农夫乐事的菜谱接成自动化产线',
         intro='和农夫乐事联动的自动化厨房：切菜、炒锅、煮锅、烤炉全部接进 Create 的传动系统，'
               '原料从漏斗进来、成品从传送带出去。',
         groups=[('厨具', ('pot', 'pan', 'oven', 'cutting', 'stove', 'grill', 'kettle')),
                 ('原料与半成品', ('dough', 'flour', 'batter', 'sauce', 'filling'))]),
    dict(slug='create-design-n-decor', ns='design_decor', title="Create: Design n' Decor",
         tag='488 件成套的工业风建筑装饰',
         intro='按材质与颜色分系列的装饰方块：金属板、格栅、通风口、灯具、栏杆、台阶与瓦片，'
               '数量和分组都极细，铺厂房和站台时基本够用。',
         groups=[('金属板与格栅', ('plate', 'grate', 'sheet', 'panel')),
                 ('通风与管道', ('vent', 'pipe', 'duct', 'fan')),
                 ('灯具', ('lamp', 'light', 'bulb', 'lantern')),
                 ('窗与门', ('window', 'door', 'frame')),
                 ('台阶与瓦片', ('slab', 'stairs', 'tile', 'brick'))]),
    dict(slug='create-encased', ns='createcasing', title='Create Encased',
         tag='528 件把传动件装进各种外壳的变体',
         intro='把 Create 的齿轮、传动轴、漏斗、传送带等包进不同材质的外壳里：安山、黄铜、铜、'
               '工业铁、火车铁……同一台机器有十几种外观可选，做产线时视觉统一。',
         groups=[('齿轮与传动', ('cogwheel', 'shaft', 'gearbox')),
                 ('漏斗与溜槽', ('funnel', 'chute', 'depot')),
                 ('传送与机械', ('belt', 'press', 'mixer', 'saw', 'drill')),
                 ('外壳材质', ('andesite', 'brass', 'copper', 'industrial_iron', 'train',
                          'weathered_iron', 'shadow', 'refined_radiance'))]),
    dict(slug='create-railways-navigator', ns='createrailwaysnavigator', title='Create Railways Navigator',
         tag='给铁路系统加一块实时导航屏',
         intro='配合 Steam n Rails 使用的导航工具：列车时刻、线路图、站点距离都在一块屏幕上显示，'
               '可以把整张路网摊开看。',
         groups=[('导航设备', ('navigator', 'display', 'monitor', 'screen', 'terminal')),
                 ('线路元件', ('station', 'platform', 'route', 'schedule'))]),
    dict(slug='create-clockwork', ns='vs_clockwork', title='Create: Clockwork',
         tag='把机械动力搬到天上，做成可驾驶的飞行器',
         intro='大型载具系统：飞艇、飞行器、物理化的旋转与推进，配合 Create 的应力驱动。'
               '是目前 Create 生态里最完整的空中载具方案。',
         groups=[('飞行器部件', ('airship', 'propeller', 'balloon', 'thruster', 'wing', 'rotor')),
                 ('控制与导航', ('controller', 'helm', 'throttle', 'compass', 'altimeter')),
                 ('结构与装饰', ('hull', 'frame', 'girder', 'plate', 'rivet'))]),
    dict(slug='create-tfmg', ns='tfmg', title='Create: The Factory Must Grow',
         tag='808 件工业零件，把产线做到真正的工厂规模',
         intro='一条极长的工业链：采矿、冶炼、轧制、化工、发电，每一步都有专门的机器和中间产物。'
               '配合 Create 的应力系统，是现有附属里最接近完整工业模组的一个。',
         groups=[('冶炼与轧制', ('furnace', 'smelter', 'rolling', 'mill', 'blast', 'crucible')),
                 ('化工与流体', ('chemical', 'refinery', 'distill', 'tank', 'pipe', 'pump')),
                 ('发电与电气', ('generator', 'turbine', 'motor', 'cable', 'transformer')),
                 ('机械零件', ('gear', 'bearing', 'piston', 'rod', 'shaft', 'valve')),
                 ('材料', ('ingot', 'sheet', 'rod', 'nugget', 'plate', 'wire')),
                 ('建筑与装饰', ('block', 'slab', 'stairs', 'wall', 'grate'))]),
    dict(slug='create-radars', ns='create_radar', title='Create: Radars',
         tag='用应力驱动的雷达与自动探测',
         intro='给机械动力加一套探测系统：雷达扫描、目标锁定、信号输出，可以接进红石或 Create 的自动化。',
         groups=[('雷达设备', ('radar', 'scanner', 'detector', 'sensor', 'antenna')),
                 ('信号与显示', ('display', 'monitor', 'screen', 'signal', 'receiver'))]),
    dict(slug='numismatics', ns='numismatics', title='Create: Numismatics',
         tag='113 件货币与自动售货系统',
         intro='一套完整的经济系统：铸币机、银行、自动售货机、收银台。可以做成玩家之间的交易站，'
               '也能接进自动化产线自动结算。',
         groups=[('铸币与银行', ('coin', 'mint', 'bank', 'vault', 'atm', 'deposit')),
                 ('交易设备', ('vendor', 'vending', 'cash', 'register', 'shop', 'trade')),
                 ('票据与卡', ('card', 'note', 'receipt', 'ticket'))]),
    dict(slug='create-misc-and-things', ns='create_things_and_misc', title='Create: Misc and Things',
         tag='143 件杂项零件，补 Create 本体的空白',
         intro='一批零散但实用的补件：工具箱、夹具、仪表、管道接头、机械小件。'
               '不属于某个大系统，但做产线时经常差这么一块。',
         groups=[('工具与仪表', ('tool', 'gauge', 'meter', 'dial', 'wrench')),
                 ('零件与接头', ('joint', 'coupling', 'fitting', 'clamp', 'bracket')),
                 ('机械小件', ('gear', 'spring', 'lever', 'latch'))]),
    dict(slug='create-bits-n-bobs', ns='bits_n_bobs', title="Create: Bits 'n' Bobs",
         tag='133 件装饰与零件小物',
         intro='细碎的装饰件和机械零件，用来填场景空缺：铆钉、铭牌、支架、管道、小灯。',
         groups=[('装饰件', ('plaque', 'sign', 'trim', 'ornament')),
                 ('零件', ('rivet', 'bracket', 'pipe', 'rod'))]),
    dict(slug='create-dragons-plus', ns='create_dragons_plus', title='Create: Dragons Plus',
         tag='116 件龙与魔法方向的扩展',
         intro='把 Create 的机械逻辑接进龙与魔法题材：龙鳞处理、魔法素材、悬浮装置。',
         groups=[('龙与素材', ('dragon', 'scale', 'egg', 'bone')),
                 ('魔法装置', ('altar', 'rune', 'crystal', 'arcane'))]),
    dict(slug='create-stuff-additions', ns='create_sa', title="Create Stuff 'N Additions",
         tag='80 件机器与工具扩展',
         intro='一批独立的机器和工具：更多加工设备、动力工具、以及配套的中间材料。',
         groups=[('机器', ('machine', 'press', 'mill', 'grinder', 'crusher')),
                 ('工具', ('tool', 'hammer', 'wrench', 'saw', 'drill')),
                 ('材料', ('ingot', 'sheet', 'rod', 'gear'))]),
    dict(slug='extended-cogwheels', ns='extendedgears', title='Create: Extended Cogwheels',
         tag='70 种尺寸的齿轮，补全传动比',
         intro='只做一件事：把齿轮和大齿轮做成更多尺寸。想精确调配转速比时非常有用。',
         groups=[('齿轮', ('cogwheel', 'gear', 'large', 'small', 'shaft'))]),
    dict(slug='rechiseled-create', ns='rechiseledcreate', title='Rechiseled: Create',
         tag='57 件可凿刻的材质变体',
         intro='与 Rechiseled 联动的凿刻方块，用凿子在几十种纹理之间切换，同一块方块能有不同表面。',
         groups=[('凿刻方块', ('chisel', 'block', 'tile', 'brick', 'pattern'))]),
    dict(slug='interiors', ns='interiors', title='Create: Interiors',
         tag='63 件可坐可用的家具',
         intro='室内家具：椅子、桌子、柜子、灯具、地毯。只是装饰，但能坐、能放东西。',
         groups=[('座椅与桌', ('chair', 'stool', 'table', 'bench')),
                 ('储物与柜', ('cabinet', 'drawer', 'shelf', 'wardrobe')),
                 ('灯具与软装', ('lamp', 'carpet', 'curtain'))]),
    dict(slug='create-dreams-and-desires', ns='create_dd', title='Create: Dreams & Desires',
         tag='372 件把机械动力扩成一整套世界',
         intro='大型扩展包：新增维度、生物群系、矿物、机器与装饰，同时保留 Create 的机械体系。'
               '内容量大，适合想一次玩很久的人。',
         groups=[('机器与工业', ('machine', 'press', 'mixer', 'saw', 'furnace')),
                 ('矿物与材料', ('ore', 'ingot', 'sheet', 'nugget', 'block')),
                 ('装饰与建筑', ('brick', 'tile', 'slab', 'stairs', 'wall')),
                 ('生物与掉落', ('mob', 'egg', 'bone', 'scale'))]),
    dict(slug='slice-and-dice', ns='sliceanddice', title='Create Slice & Dice',
         tag='5 件把切菜做成自动化',
         intro='最小的一类扩展：只加切片机与几个配套件，把农夫乐事的食材处理接进传动系统。',
         groups=[]),
    dict(slug='create-jetpack', ns='create_jetpack', title='Create Jetpack',
         tag='26 件用压缩空气飞的喷气背包',
         intro='一套背包与配套：用 Create 的压缩空气罐供能，可悬停、可加速，还能装多个气罐延长滞空。',
         groups=[('背包与气罐', ('jetpack', 'tank', 'canister', 'thruster')),
                 ('配件', ('gauge', 'valve', 'nozzle'))]),
    dict(slug='bellsandwhistles', ns='bellsandwhistles', title='Create: Bells & Whistles',
         tag='36 件小装饰，专治场景空旷',
         intro='铃铛、哨子、道岔标、站牌一类的小物件，做铁路场景时用来点缀。',
         groups=[('铃与哨', ('bell', 'whistle', 'horn')),
                 ('标牌', ('sign', 'plaque', 'board'))]),
    dict(slug='create-trading-floor', ns='trading_floor', title='Create: Trading floor',
         tag='1 件自动交易台',
         intro='只加一个方块：把商品摆上去，配好价格，村民或玩家就能自动交易结算。',
         groups=[]),
    dict(slug='create-questing', ns='create_questing', title='Create Questing',
         tag='1 件把任务系统接进游戏',
         intro='轻量任务系统：在方块里编辑任务线，配合进度自动发放奖励。',
         groups=[]),
    dict(slug='create-pattern-schematics', ns='create_pattern_schematics', title='Create: Pattern Schematics',
         tag='4 件把蓝图变成可复用的图样',
         intro='把 Create 的蓝图转成可重复套用的图样，批量搭建同一种结构时省事。',
         groups=[]),
    dict(slug='create-power-loader', ns='create_power_loader', title='Create: Power Loader',
         tag='4 件跨区块的动力传输器',
         intro='只做一件事：把应力送到远处。省去一路架设传动轴的麻烦。',
         groups=[]),
    dict(slug='create-ultimine', ns='create_ultimine', title='Create Ultimine',
         tag='连锁挖掘',
         intro='一个功能型扩展：按住快捷键一次挖掉整片同类方块，做大型工厂时省时间。没有新增物品。',
         groups=[]),
    dict(slug='create-structures', ns='create_structures', title='Create: Structures',
         tag='在世界里生成 Create 风格的建筑',
         intro='一个世界生成扩展：让村庄、工厂遗迹等结构自然出现在世界里。没有新增物品，只有建筑。',
         groups=[]),
    dict(slug='create-deco', ns='createdeco', title='Create Deco',
         tag='给机械动力补 400 多件成套的建筑装饰方块',
         intro='纯装饰向扩展：砖、瓦、瓦片、栏杆、梯子、门窗、灯具一整套，按颜色与材质分系列。'
               '和 Create 的工业风格同一套配色，拿来铺工厂地坪、砌厂房外墙最顺手。',
         groups=[('砖与瓦', ('brick', 'tile', 'shingle', 'slab', 'stairs', 'wall')),
                 ('金属板材', ('iron', 'copper', 'brass', 'zinc', 'gold', 'netherite')),
                 ('栏杆与梯子', ('railing', 'ladder', 'bars', 'catwalk', 'support')),
                 ('门窗与灯具', ('door', 'window', 'lamp', 'light')),
                 ('装饰小件', ('coin', 'sign', 'flag', 'vent', 'cage'))]),
    dict(slug='create-big-cannons', ns='createbigcannons', title='Create Big Cannons',
         tag='用机械动力的应力驱动一整套火炮',
         intro='把 Create 的动能接到火器上：炮管、炮闩、炮架、炮弹、引信，全部靠应力和转速运转。'
               '弹道有真实的装药与仰角计算，可以直接接进自动化产线里批量铸造。',
         groups=[('火炮部件', ('cannon', 'barrel', 'breech', 'carriage', 'mount', 'yaw', 'pitch')),
                 ('弹药与装药', ('shell', 'cartridge', 'powder', 'charge', 'fuze', 'ap', 'he', 'shrapnel')),
                 ('材料与铸件', ('cast', 'ingot', 'nugget', 'sheet', 'block', 'bronze', 'steel')),
                 ('机械与工具', ('ram', 'swab', 'drill', 'bore', 'lathe', 'mill')),
                 ('其它', ('screw', 'breech', 'fuse', 'autocannon'))]),
    dict(slug='create-connected', ns='create_connected', title='Create: Connected',
         tag='把机械动力里缺的那批连接与传动件补齐',
         intro='不是新玩法，而是把 Create 本体没做全的机械件补上：更多齿轮箱、离合、'
               '调速装置、物品与流体接口，以及一批和本体风格一致的装饰件。',
         groups=[('传动与齿轮', ('cogwheel', 'gearbox', 'shaft', 'clutch', 'gearshift',
                            'transmission', 'speed')),
                 ('控制与调节', ('controller', 'regulator', 'valve', 'throttle', 'sequenced')),
                 ('物品与流体', ('funnel', 'chute', 'tank', 'pipe', 'pump', 'valve')),
                 ('装饰与结构', ('casing', 'bracket', 'ladder', 'girder', 'frame'))]),
    dict(slug='create-diesel-generators', ns='createdieselgenerators', title='Create: Diesel Generators',
         tag='用柴油链给中后期供能',
         intro='补一条从原油到柴油的完整燃料链：抽取、蒸馏、储存、燃烧发电，'
               '柴油机可以输出应力，也可以直接驱动发电机。附带的油桶、油罐和管路能接进 Create 的流体系统。',
         groups=[('燃料链', ('oil', 'diesel', 'fuel', 'crude', 'refin', 'distill', 'biodiesel')),
                 ('发动机与发电', ('engine', 'generator', 'motor', 'pump', 'tank')),
                 ('储运与管路', ('barrel', 'tank', 'pipe', 'hose', 'canister', 'bucket')),
                 ('杂项零件', ('bearing', 'piston', 'rod', 'screw', 'plate'))]),
    dict(slug='create-new-age', ns='create_new_age', title='Create: New Age',
         tag='让机械动力的应力与电力互相转换',
         intro='引入一套独立的电力体系：发电机、导线、电池、电动机，和 Create 的应力可以双向转换。'
               '适合想把产线做长、把能量搬到远处再用的人。',
         groups=[('发电与转换', ('generator', 'motor', 'alternator', 'dynamo', 'converter',
                           'transformer', 'coil')),
                 ('导线与电缆', ('wire', 'cable', 'connector', 'terminal', 'insulator')),
                 ('储能与元件', ('battery', 'capacitor', 'cell', 'reactor', 'magnet',
                            'induction')),
                 ('材料与零件', ('ingot', 'sheet', 'rod', 'nugget', 'magnetite', 'copper'))]),
    dict(slug='copycats', ns='copycats', title='Create: Copycats+',
         tag='用任意材质伪装成任意形状的方块',
         intro='纯建筑工具：一块伪装方块可以套用任意贴图，再切成台阶、楼梯、栏杆、窗、板等形状。'
               '搭场景时不用为每种材质各做一套模型品，一块就够。',
         groups=[('伪装方块', ('copycat', 'block', 'panel', 'slab', 'stairs', 'wall', 'fence')),
                 ('形状与结构', ('beam', 'board', 'step', 'layer', 'trapdoor', 'pane')),
                 ('工具', ('wrench', 'blueprint', 'template'))]),
    dict(slug='create-ore-excavation', ns='createoreexcavation', title='Create Ore Excavation',
         tag='把矿脉变成可自动化的无限产线',
         intro='只做一件事：勘探矿脉、架起钻井、用应力持续抽取。矿脉会画在地图上，'
               '钻机接上动力就能无限出矿，是中期解决资源焦虑最直接的办法。',
         groups=[('钻机与部件', ('drill', 'rig', 'extractor', 'motor', 'bearing')),
                 ('勘探工具', ('vein', 'finder', 'scanner', 'sample', 'core')),
                 ('矿脉与产物', ('ore', 'vein', 'raw', 'chunk', 'sample'))]),
    dict(slug='create-steam-n-rails', ns='railways', title="Create: Steam 'n' Rails",
         tag='把 Create 的列车做成真正能开的一套铁路系统',
         intro='Create 最出圈的扩展：机车、车厢、轨道、信号、站台一整套装备。'
               '除了载具本身，还附大量按颜色分套的机车铁块、锅炉、烟箱、车窗与警纹装饰块，'
               '足以把一条完整铁路线从车头铺到站台。',
         groups=[('机车与车厢', ('locomotive', 'carriage', 'tender', 'cart', 'benchcart',
                            'handcar', 'conductor')),
                 ('轨道与信号', ('track', 'rail', 'signal', 'switch', 'buffer', 'semaphore',
                            'coupler', 'bearing')),
                 ('机车铁块与锅炉', ('locometal', 'boiler', 'smokebox', 'riveted', 'slashed',
                              'wrapped')),
                 ('车窗与门', ('window', 'pane', 'door', 'hatch')),
                 ('装饰与警纹', ('hazard', 'stripe', 'chevron', 'plaque', 'lamp', 'whistle')),
                 ('列车长装备', ('cap', 'uniform', 'goggles'))]),
    dict(slug='createaddition', ns='createaddition', title='Create Crafts & Additions',
         tag='把 Create 的动能接进电力系统',
         intro='最老牌的 Create 扩展之一：用电动马达把应力换成电力、用交流发电机再把电力换回应力，'
               '中间靠电线、线轴和连接器组网。另附轧机（压板）、生物质燃料链和一整套金属棒板。',
         groups=[('电力设备', ('electric_motor', 'alternator', 'capacitor', 'accumulator',
                            'connector', 'adapter', 'relay', 'coil', 'creative_energy',
                            'portable_energy')),
                 ('电线的材质', ('wire', 'spool')),
                 ('金属棒与板', ('rod', 'sheet', 'nugget', 'ingot', 'grit', 'sandpaper')),
                 ('燃料与生物质', ('biomass', 'bioethanol', 'seed_oil')),
                 ('食物与杂项', ('cake', 'goblet', 'straw', 'wire', 'figurine'))]),
    dict(slug='create-cold-sweat', ns='cold_sweat', title='Create: Cold Sweat',
         tag='把体温、水分和恶化的环境变成一套生存压力',
         intro='不是新的动力机器，而是给生存加一层「环境」：体温、口渴、空气质量会随维度与天气变化，'
               '配套的物件用来降温、补水、净化空气。',
         groups=[('降温 / 保温', ('ice', 'cold', 'cool', 'fridge', 'snow')),
                 ('饮水 / 食物', ('water', 'drink', 'canteen', 'purif', 'food')),
                 ('空气 / 呼吸', ('air', 'oxygen', 'filter', 'mask', 'respir'))]),
    dict(slug='create-more-features', ns='create_more_features', title='Create: More Features',
         tag='给机械动力补一批零件与功能方块',
         intro='一批独立的零件和功能方块，直接插进 Create 的产线里用，不改变原有玩法。',
         groups=[]),
    dict(slug='create-more-seats', ns='create_more_seats', title='Create: More Seats',
         tag='给列车和结构补一批可坐的座椅',
         intro='只做一件事：加更多样式的座椅，放在列车车厢或建筑里都能坐。',
         groups=[]),
    dict(slug='create-heat-js', ns='heats', title='Create: Heat JS',
         tag='用 KubeJS 给机械动力加「热量」这套系统',
         intro='基于 KubeJS 的热量机制：给方块和配方加上温度要求，让加热、熔化、烧炼有统一的温度线。'
               '它本身是脚本库，玩法取决于整合包怎么调用。',
         groups=[]),
    dict(slug='create-unbreakable-armor', ns='create_unbreakable_armor', title='Create: Unbreakable Armor',
         tag='把下界合金盔甲做成永不磨损',
         intro='四件套盔甲，全部用动力合成器（机械合成）做：下界合金块 + 金块 + 红石，'
               '成品带「无法破坏」属性，穿到死也不用修。',
         groups=[]),
    dict(slug='create-unbreakable-tools', ns='create_unbreakable_tools_series', title='Create: Unbreakable Tools',
         tag='九件不毁下界合金工具',
         intro='剑、镐、斧、锹、锄、剪刀、镐斧、小刀、打火石，九件全用动力合成器拼出来，'
               '每件都是「无法破坏」。',
         groups=[]),
    dict(slug='unbreakable-netherite-pickaxe', ns='unbreakable_netherite_pickaxe', title='Unbreakable Netherite Pickaxe',
         tag='单件：一把不会坏的下界合金镐',
         intro='只加一把镐子，用下界合金块和金锭在动力合成器上拼成，耐久条不再消耗。',
         groups=[]),
    dict(slug='create-treadmill', ns='createtreadmill', title='Create: Treadmill',
         tag='跑步机 + 女仆马达，把「走路」变成旋转动力',
         intro='给女仆（Maid）用的跑步机：女仆在跑步机上跑，跑步机输出旋转动力。'
               '配套的女仆马达可以直接把女仆装进动力结构里，是「生物动力」路线的小玩具。',
         groups=[('跑步机 / 马达', ('treadmill', 'motor', 'maid')), ]),
    dict(slug='kinetic-pixel', ns='kinetic_pixel', title='Kinetic Pixel',
         tag='用 Create 产线造火器：枪管、激发器、各种弹药',
         intro='把 Create 的加工体系接到轻武器上：抗压板、弹丸管、激发器、储气筒、各类蓝图，'
               '最后在火器工台组装成枪。素材链很长，适合喜欢「造产线」的人。',
         groups=[('抗压板 / 材料', ('compression', 'sheet', 'ingot', 'alloy')),
                 ('枪管 / 激发器', ('barrel', 'exciter', 'piston', 'striker', 'cylinder')),
                 ('弹药 / 蓝图', ('ammo', 'dart', 'shrapnel', 'whistle', 'blueprint', 'propellant', 'template')),
                 ('棉花 / 作物', ('cotton', 'seed')), ]),

    dict(slug='create-propulsion', ns='createpropulsion', title='Create: Propulsion',
         tag='给机械动力加一套飞行器：推进器、机翼、线缆、光学镜头',
         intro='把 Create 的旋转动力变成推力：固体/液体燃料推进器、离子推进器、矢量推进器，'
               '配机翼、粘合与遥控结构；另有一条铂（Platinum）材料线和光学镜头（透镜、线缆）。',
         groups=[('推进器', ('thruster',)),
                 ('机翼与结构', ('wing', 'glue', 'tilt', 'contraption', 'adapter', 'reaction', 'assembly', 'assembler')),
                 ('线缆与光学', ('cable', 'lens', 'optical', 'focus', 'invisib')),
                 ('铂与材料', ('platinum', 'raw', 'ore', 'sheet', 'ingot', 'nugget', 'casing', 'tank', 'vessel')),
                 ('燃料与推进剂', ('burner', 'fuel', 'oxidizer', 'turpentine', 'resin', 'coral'))]),
    dict(slug='create-screw-it', ns='screwnstuff', title='Create: Screw It!',
         tag='螺丝、钉子、支架：把方块真正拧在一起',
         intro='给建筑和机械加「紧固件」：工业铁与锈蚀铁两种材质的螺丝、钉子、支架，'
               '配锯（改长度）、螺丝刀（拧紧）、锤子（敲入），拼装时能对齐、能拆。',
         groups=[('紧固件', ('screw', 'nail', 'bracket')),
                 ('工具', ('hammer', 'saw', 'screwdriver'))]),
    dict(slug='create-bread-and-beyond', ns='create_bread_and_beyond', title='Create: Bread and Beyond',
         tag='面包、肉饼、芝士与下界三明治',
         intro='一条吃的产线：面团 → 面包胚，生肉 → 肉饼 → 芝士汉堡，'
               '还有下界/诡异两种菌岩三明治和一把刀。',
         groups=[('面包与面团', ('dough', 'bread', 'bun')),
                 ('肉与芝士', ('patty', 'meat', 'cheese', 'mince')),
                 ('三明治与汉堡', ('sandwich', 'burger', 'loaf')),
                 ('调料与工具', ('salt', 'knife'))]),


    dict(slug='create-integrated-farming', ns='create_integrated_farming', title='Create: Integrated Farming',
         tag='鸡鸭鹅的自动化养殖：栖架、渔网、真空收割',
         intro='把「养动物」接进 Create 产线：各种栖架（鸡/鸭/鹅/火鸡）自动产蛋，'
               '渔网捕鱼（含岩浆渔网），真空收割机范围收集掉落物。',
         groups=[('鸡与火鸡', ('chicken', 'turkey')),
                 ('鸭与鹅', ('duck', 'goose')),
                 ('捕捞', ('fishing', 'net')),
                 ('收获', ('harvest', 'vacuum', 'roost'))]),
    dict(slug='simulated-coasters', ns='simulatedcoasters', title='Simulated Coasters',
         tag='过山车轨道与车厢，接 Create 的机械结构',
         intro='在 Create 的装置上加过山车：轨道、锚点、车厢、铆钉，还有红气球装饰。'
               '轨道可以拼成弯道，车厢靠锚点定位。',
         groups=[('轨道', ('track', 'anchor')),
                 ('车厢', ('cart',)),
                 ('零件与装饰', ('rivet', 'balloon'))]),
    dict(slug='create-escalated', ns='escalated', title='Create: Escalated',
         tag='自动扶梯：把传送带变成会走的楼梯',
         intro='两个台阶方块（金属/木质），铺在机械传送带上就变成自动扶梯。'
               '模组还带了「只靠扶梯爬 100 格」的成就。',
         groups=[('扶梯台阶', ('steps', 'walkway'))]),

]


def fetch_jar(slug, ns):
    # 本地 jar 优先（含非 1.20.1 Forge 的包）
    _local = os.path.join(RAW, slug + '.jar')
    if os.path.exists(_local):
        return _local
    local = os.path.join(RAW, slug + '.jar')
    if os.path.exists(local):
        return local
    vs = json.load(u.urlopen('https://api.modrinth.com/v2/project/%s/version' % slug, timeout=25))
    pick = None
    for v in vs:
        if '1.20.1' in v.get('game_versions', []) and ('forge' in v.get('loaders', []) or 'neoforge' in v.get('loaders', [])):
            pick = v
            break
    if pick is None:
        return None
    f = next((x for x in pick['files'] if x['filename'].endswith('.jar')), pick['files'][0])
    dst = os.path.join(RAW, slug + '.jar')
    if not os.path.exists(dst):
        open(dst, 'wb').write(u.urlopen(f['url'], timeout=120).read())
    return dst


def strip(t):
    return re.sub(r'§.', '', t or '')


def build(spec):
    jar = fetch_jar(spec['slug'], spec['ns'])
    if not jar:
        print(spec['slug'], 'SKIP no 1.20.1 forge')
        return
    z = zipfile.ZipFile(jar)
    ns = spec['ns']
    # 真实命名空间（有的模组 jar 内 ns 与 slug 不同）
    nss = set()
    for n in z.namelist():
        if n.startswith('assets/') and n.count('/') >= 2:
            nss.add(n.split('/')[1])
    nss = [x for x in nss if x != 'minecraft']
    if nss and ns not in nss:
        ns = sorted(nss)[0]

    def rj(n):
        try:
            return json.loads(z.read(n).decode('utf-8-sig'))
        except Exception:
            return {}

    lang = {}
    for code in ('zh_cn', 'en_us'):
        for n in z.namelist():
            if n.endswith('lang/%s.json' % code) and '/%s/' % ns in n:
                lang = rj(n)
                break
        if lang:
            break

    names = {}
    for k, v in lang.items():
        m = re.match(r'^(item|block)\.%s\.([a-z0-9_]+)$' % re.escape(ns), k)
        if m:
            names[m.group(2)] = strip(v).replace(' (%s)', '').replace('(%s)', '')

    copied = {}

    def icon(short):
        # 名字与贴图不同名的特例（Screw It：industrial_iron_screw -> block/screw_industrial_iron）
        _m = re.match(r'(industrial_iron|weathered_iron)_(screw|nail|bracket)$', short)
        if _m:
            _mat, _kind = _m.group(1), _m.group(2)
            _cand = ('assets/%s/textures/block/bracket/1-1_%s.png' % (ns, _mat)) if _kind == 'bracket' \
                    else ('assets/%s/textures/block/%s_%s.png' % (ns, _kind, _mat))
            if _cand in z.namelist():
                _dst = '%s_%s.png' % (ns, short)
                if _dst not in copied:
                    with z.open(_cand) as f, open(os.path.join(ICONS, _dst), 'wb') as o:
                        shutil.copyfileobj(f, o)
                    copied[_dst] = 1
                return 'assets/icons/' + _dst
        if os.path.exists(os.path.join(ICONS, 'cms_%s.png' % short)):
            return 'assets/icons/cms_%s.png' % short
        for k in ('item', 'block'):
            nm = 'assets/%s/textures/%s/%s.png' % (ns, k, short)
            if nm in z.namelist():
                dst = '%s_%s.png' % (ns, short)
                if dst not in copied:
                    with z.open(nm) as f, open(os.path.join(ICONS, dst), 'wb') as o:
                        shutil.copyfileobj(f, o)
                    copied[dst] = 1
                return 'assets/icons/' + dst
        for pre in ('models/item/%s.json' % short, 'models/block/%s.json' % short):
            nm = 'assets/%s/%s' % (ns, pre)
            if nm in z.namelist():
                for v in (rj(nm).get('textures') or {}).values():
                    if isinstance(v, str) and not v.startswith('#'):
                        p = 'assets/%s/textures/%s.png' % (ns, v.split(':')[-1])
                        if p in z.namelist():
                            dst = '%s_%s.png' % (ns, short)
                            if dst not in copied:
                                with z.open(p) as f, open(os.path.join(ICONS, dst), 'wb') as o:
                                    shutil.copyfileobj(f, o)
                                copied[dst] = 1
                            return 'assets/icons/' + dst
        for c in ('create_%s.png' % short, 'minecraft_%s.png' % short):
            if os.path.exists(os.path.join(ICONS, c)):
                return 'assets/icons/' + c
        return ''

    recs = {}
    for n in z.namelist():
        if (n.startswith('data/%s/recipes/' % ns) or n.startswith('data/%s/recipe/' % ns)) and n.endswith('.json'):
            try:
                d = rj(n)
            except Exception:
                continue
            res = d.get('results') or d.get('result')
            res = res if isinstance(res, list) else [res]
            for x in res:
                if isinstance(x, list):
                    x = x[0] if x else None
                if not isinstance(x, dict):
                    continue
                rid = x.get('item') or x.get('id') or ''
                if isinstance(rid, dict):
                    rid = rid.get('item') or rid.get('id') or ''
                if isinstance(rid, str) and rid.startswith(ns + ':'):
                    recs.setdefault(rid.split(':')[-1], d)

    def nm(iid):
        if not iid:
            return ''
        s = iid.split(':')[-1]
        if iid.startswith(ns + ':'):
            return SEAT_ZH.get(s) or names.get(s, s.replace('_', ' '))
        if iid in MC_ZH:
            return MC_ZH[iid]
        try:
            d = json.load(io.open(os.path.join(RAW, '..', 'out', 'data.json'), encoding='utf-8'))
            v = (d.get('items') or {}).get(s) or (d.get('vanilla') or {}).get(s)
            if isinstance(v, dict) and v.get('n'):
                return v['n']
        except Exception:
            pass
        return s.replace('_', ' ')

    def sicon(iid):
        s = iid.split(':')[-1]
        if iid.startswith(ns + ':'):
            return icon(s)
        for c in ('3d_create_%s.png' % s, 'create_%s.png' % s, 'hh3d_%s.png' % s, 'minecraft_%s.png' % s):
            if os.path.exists(os.path.join(ICONS, c)):
                return 'assets/icons/' + c
        return ''

    def _href_for(iid):
        if not iid or ':' not in iid:
            return None
        ns_, short_ = iid.split(':', 1)
        if ns_ == 'create':
            if os.path.exists(os.path.join(SITE, 'items', short_ + '.html')):
                return 'items/' + short_ + '.html'
        else:
            if os.path.exists(os.path.join(SITE, 'vanilla', short_ + '.html')):
                return 'vanilla/' + short_ + '.html'
        return None

    def chip(st):
        if isinstance(st, list):
            st = st[0] if st else {}
        if not isinstance(st, dict):
            st = {}
        if not st:
            return ''
        if st.get('tag'):
            tg = st['tag'].lstrip('#')
            return '<span class="ch">#%s</span>' % tg.split('/')[-1].replace('_', ' ')
        if st.get('fluid'):
            _fl = st['fluid'].split(':')[-1]
            _fh = 'vanilla/%s.html' % _fl if os.path.exists(os.path.join(SITE, 'vanilla', _fl + '.html')) else None
            if _fh:
                return '<a class="ch" href="%s">%s %dmB</a>' % (
                    _fh, _fl.replace('_', ' '), st.get('amount') or 0)
            return '<span class="ch">%s %dmB</span>' % (
                st['fluid'].split(':')[-1].replace('_', ' '), st.get('amount') or 0)
        iid = st.get('item') or st.get('id') or ''
        ic = sicon(iid)
        cnt = st.get('count') or 1
        _h = _href_for(iid)
        if _h:
            return '<a class="ch" href="%s" title="%s">%s%s%s</a>' % (
                _h, nm(iid), ('<img src="%s" alt="">' % ic) if ic else '', nm(iid),
            (' ×%d' % cnt) if cnt > 1 else '')
        # 没有对应页面（站内未收录该物品）时退化为纯文本 chip，
        # 否则函数隐式返回 None，会让外层 ''.join() 抛 TypeError。
        return '<span class="ch">%s%s</span>' % (
            ('<img src="%s" alt="">' % ic) if ic else '', nm(iid))

    def rec(d):
        mach = {'minecraft:crafting_shaped': '工作台', 'minecraft:crafting_shapeless': '工作台',
                'create:mechanical_crafting': '动力合成器'}.get(d.get('type'), '机械动力')
        pat = d.get('pattern')
        key = d.get('key') or {}
        if not isinstance(key, dict):
            key = {}
        if pat:
            w = max(len(x) for x in pat)
            cells = []
            for row in pat:
                for ch in row.ljust(w, ' '):
                    cells.append('<div class="cell empty"></div>' if ch == ' ' else
                                 '<div class="cell">%s</div>' % chip(key.get(ch, {})))
            while len(cells) % w:
                cells.append('<div class="cell empty"></div>')
            out = (d.get('results') or [d.get('result')])[0]
            return ('<div class="rec"><div class="grid" style="grid-template-columns:repeat(%d,1fr)">%s</div><div class="arw">→</div>%s'
                    '<span class="mach">%s</span></div>' % (w, ''.join(cells), chip(out), mach))
        ings = d.get('ingredients') or []
        agg, order = {}, []
        for x in ings:
            k = x.get('item') or x.get('fluid') or x.get('tag') or '?'
            if k not in agg:
                agg[k] = {'st': dict(x), 'n': 0}
                order.append(k)
            agg[k]['n'] += x.get('count') or 1
        parts = []
        for k in order:
            st = dict(agg[k]['st'])
            st['count'] = agg[k]['n']
            parts.append(chip(st))
        out = (d.get('results') or [d.get('result')])[0]
        if isinstance(out, list):
            out = out[0] if out else {}
        return ('<div class="rec"><div class="chips">%s</div><div class="arw">→</div>%s'
                '<span class="mach">%s</span></div>' % (''.join(parts), chip(out), mach))

    order = sorted(names.keys())
    _only = spec.get('only')
    _skip = spec.get('skip') or ()
    if _only:
        order = [k for k in order if any(w in k for w in _only)]
    if _skip:
        order = [k for k in order if not any(w in k for w in _skip)]
    groups = spec['groups']
    buckets = []
    if groups:
        used = set()
        for title, kws in groups:
            keys = [k for k in order if k not in used and any(w in k for w in kws)]
            used |= set(keys)
            if keys:
                buckets.append((title, keys))
        rest = [k for k in order if k not in used]
        if rest:
            buckets.append(('其它', rest))
    else:
        buckets.append(('全部物品', order))

    secs = []
    for title, keys in buckets:
        cards = []
        for k in keys:
            ic = icon(k)
            if not ic:
                _p = os.path.join(ICONS, '%s_%s.png' % (ns, k))
                if os.path.exists(_p):
                    ic = 'assets/icons/%s_%s.png' % (ns, k)
            body = rec(recs[k]) if k in recs else '<div class="note2">没有工作台/机器配方</div>'
            cards.append('<div class="card"><div class="ci">%s</div><div class="t"><b>%s</b>'
                         '<small>%s:%s</small></div>%s</div>'
                         % (('<img src="%s" alt="">' % ic) if ic else '', names[k], ns, k, body))
        secs.append('<div class="blk"><h2>%s<span class="cnt">%d</span></h2>'
                    '<div class="grid-items">%s</div></div>' % (title, len(keys), ''.join(cards)))

    page = '''<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>%s · 附属模组 · Create Codex</title>
<link rel="stylesheet" href="assets/style.css">
<style>
.wrap{max-width:1150px}
.hero{padding:40px 0 14px;text-align:center}
.hero img.big{width:96px;height:96px;border-radius:18px;background:#0d0b09}
.hero h1{font-size:32px;margin:12px 0 4px}
.hero .sub{color:var(--brass);font-size:14px;letter-spacing:.3em}
.hero .tag{color:var(--muted);margin-top:8px}
.grid-items{display:grid;grid-template-columns:repeat(auto-fill,minmax(320px,1fr));gap:10px;align-items:start}
.card{display:block;padding:10px;border:1px solid var(--line);border-radius:10px;background:var(--panel)}
.card .ci{float:left;width:44px;height:44px;display:flex;align-items:center;justify-content:center;background:#14110c;border-radius:8px}
.card .ci img{width:34px;height:34px;object-fit:contain;image-rendering:pixelated}
.card .t{margin-left:54px;min-height:44px;display:flex;flex-direction:column;justify-content:center;gap:2px}
.card .t b{font-size:13px}
.card .t small{color:var(--muted);font-size:10px;word-break:break-all}
.card .rec{clear:both;margin-top:10px;padding-top:8px;border-top:1px solid var(--line);display:flex;align-items:center;gap:6px;flex-wrap:wrap}
.grid{display:grid;grid-template-columns:repeat(3,40px);gap:3px}
.cell,.cell *{box-shadow:none!important;outline:none}
.cell{width:40px;height:40px;display:flex;align-items:center;justify-content:center;background:#14110c;border:1px solid var(--line);border-radius:6px;overflow:hidden}
.cell.empty{border-style:dashed;opacity:.45}
.cell img{width:30px;height:30px;object-fit:contain;image-rendering:pixelated}
.cell .ch{font-size:0;border:0;background:none;padding:0}
.chips{display:flex;flex-wrap:wrap;gap:4px}
.cell .ch:not(:has(img)){max-width:34px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;font-size:9px;line-height:1.1}
.ch{display:inline-flex;align-items:center;gap:4px;font-size:11px;padding:3px 7px;border:1px solid var(--line);border-radius:999px;background:#14110c}
.ch img{width:18px;height:18px;object-fit:contain;image-rendering:pixelated}
.mach{color:var(--brass);font-size:10px}
.arw{color:var(--muted)}
.note2{color:var(--muted);font-size:11px}
.ver{margin:18px 0;padding:10px 12px;border-left:2px solid var(--brass);background:#14110c;color:var(--muted);font-size:12px;line-height:1.7}
</style></head><body>
<header class="top"><div class="wrap"><a class="logo" href="index.html"><span class="gear"></span>CREATE CODEX</a>
<nav><a href="catalog.html">全部物品</a><a href="tags.html">标签</a><a href="mods.html">模组</a><a class="on" href="mods.html">附属</a></nav></div></header>
<main class="wrap">
<div class="hero"><img class="big" src="assets/icons/mod_%s.png" alt="">
<h1>%s</h1><div class="sub">附属模组</div><div class="tag">%s</div></div>
<div class="blk"><h2>这是什么</h2><p>%s</p></div>
<div class="ver"><b>命名空间：</b><code>%s</code>　<b>1.20.1 版本：</b>本页物品与配方直接取自该版本的 jar。</div>
%s
</main>
<footer class="wrap foot">数据与图标来自 %s 的 1.20.1 jar · 本页不属于 Create 本体图鉴</footer>
</body></html>''' % (spec['title'], spec['slug'].replace('-', '_'), spec['title'], spec['tag'],
                     spec['intro'], ns, ''.join(secs), spec['title'])

    out = os.path.join(SITE, 'addon-%s.html' % spec['slug'].replace('create-', ''))
    io.open(out, 'w', encoding='utf-8').write(page)
    print('%-28s %-18s items %-3d recipes %-3d -> %s'
          % (spec['slug'], ns, len(names), len(recs), os.path.basename(out)))


MODS += [
    dict(slug='create-meat-blocks', ns='meatblocks', title='Create: Meat Blocks',
         tag='把肉做成方块：可切片、可压缩、可烤',
         intro='给 Create 加一整套「肉」的加工链：生肉块、熟肉块、压缩肉、切片机与培根机，'
               '产线末端能直接吐出食物。名字取自模组语言文件（英文）。',
         groups=[('生肉 / 熟肉', ('raw', 'cooked', 'meat', 'beef', 'pork', 'chicken')),
                 ('压缩 / 加工', ('compressed', 'slice', 'bacon', 'grind', 'press'))]),
    dict(slug='eatandesite', ns='eatandesite', title='EatAndesite',
         tag='让你能吃安山岩',
         intro='一个小玩笑模组：按住右键啃安山岩，每一口消耗一点饥饿度并短暂获得缓慢。'
               '没有新增物品，只改了安山岩的交互。',
         groups=[]),
    dict(slug='create-reautomated', ns='createreautomated', title='Create ReAutomated',
         tag='自动化零件的另一套做法',
         intro='一批可自动化的零件与机器，走的是和 Create 本体不同的合成路线，'
               '适合在整合包里替换掉手搓环节。名字取自模组语言文件（英文）。',
         groups=[('零件', ('gear', 'shaft', 'cog', 'bearing', 'belt')),
                 ('机器', ('machine', 'press', 'mixer', 'mill', 'drill', 'assembler'))]),
]

import sys as _sys0
_ONLY = set(_sys0.argv[1:])
MODS += [
    dict(slug='create-reautomated-traces', ns='createreautomatedtraces', title='Create ReAutomated: Traces',
         tag='ReAutomated 的补充包：更多零件与中间产物',
         intro='Create ReAutomated 的附属，补上它依赖的中间产物与额外零件；'
               '单独安装没有内容，需要和 ReAutomated 一起用。名字取自模组语言文件（英文）。',
         groups=[('零件', ('gear', 'shaft', 'cog', 'bearing', 'trace')),
                 ('机器', ('machine', 'press', 'mixer', 'mill', 'assembler'))]),
]

for m in MODS:
    if _ONLY and m['slug'] not in _ONLY:
        continue
    try:
        build(m)
    except Exception as e:
        import traceback
        print(m['slug'], 'ERR', type(e).__name__, e)
        traceback.print_exc()


# ---- 页面后处理（chip 链接、空格子、anchors.js）----
try:
    import sys as _sys, os as _os
    _sys.path.insert(0, _os.path.dirname(_os.path.abspath(__file__)))
    import addon_post as _ap
    _ap.postprocess_all()
except Exception as _e:
    print("post-process skipped:", _e)
