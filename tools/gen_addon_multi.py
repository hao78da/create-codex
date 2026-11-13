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

SITE = _os.path.join(ROOT, "docs")
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
    dict(slug='ars-technica', ns='ars_technica', title='Ars Technica',
         tag='Ars Technica 附属模组',
         intro='需要 新生魔艺 、 元素魔艺 、 Curios API 、 机械动力 还有 StarbuncleMania （本模组版本1.2.0+新需）才能使用此模组。',
         groups=[]),
    dict(slug='blueprintvoid', ns='bpvoid', title='Create：Blueprint Void',
         tag='类似于原版的结构空位方块，当使用蓝图大炮打印包含该方块的结构时…',
         intro='类似于原版的结构空位方块，当使用蓝图大炮打印包含该方块的结构时，无论如何设置蓝图大炮的填充模式，最终打印出来的结构中的蓝图空位对应位置的方块都不会被替换。',
         groups=[]),
    dict(slug='create-ad-astra-compatibility', ns='create_ad_astra_compat', title='Create: Ad Astra Compatibility',
         tag='这个模组添加了 Ad Astra! 中戴斯、紫金和耐热金属的碎矿…',
         intro='这个模组添加了 Ad Astra! 中戴斯、紫金和耐热金属的碎矿，从而方便使用 机械动力 进行矿物处理。',
         groups=[]),
    dict(slug='create-armored-rails', ns='create_armored_rails', title='Create: Armored Rails',
         tag='没有车体时，列车仍拥有基础生命值，但有了车体后，你将获得 9…',
         intro='没有车体时，列车仍拥有基础生命值，但有了车体后，你将获得 9 个等级的车体框架和 9 种独特的强化部件。',
         groups=[]),
    dict(slug='create-blue-skies-compat', ns='create_blue_skies_compat', title='Create Blue Skies Compat',
         tag='新增 6 种矿石的粉碎产物（ 镰鼬矿石 、 炙铁矿石 、 缪铁矿石…',
         intro='新增 6 种矿石的粉碎产物（ 镰鼬矿石 、 炙铁矿石 、 缪铁矿石 、 绛紫晶矿石 、 天闪石 ，还包括两个维度各自对应的绿宝石矿石变种）；',
         groups=[]),
    dict(slug='create-chromaticreturn', ns='createchromaticreturn', title='Create Chromatic Return',
         tag='Create Chromatic Return 附属模组',
         intro='此模组会破坏机械动力原有的平衡，如果你想要一个友好的游戏体验，请思考此模组是否适合你！',
         groups=[]),
    dict(slug='create-compact-exp', ns='nocubescreateexp', title='Create Compact Exp',
         tag='该模组提供了经验块，由 经验颗粒 打包而成',
         intro='该模组提供了经验块，由 经验颗粒 打包而成。',
         groups=[]),
    dict(slug='create-eureka', ns='create_eureka', title='Create: Eureka!',
         tag='Create: Eureka 是 机械动力 和 Valkyrien…',
         intro='Create: Eureka 是 机械动力 和 Valkyrien Skies Eureka 的附属模组 ，支持 Minecraft 1.20.1的 Fabric 和 Forge。',
         groups=[]),
    dict(slug='create-extended-bogeys-borked-addon', ns='extendedbogeys', title='Create: Extend Bogeys',
         tag='Create: Extend Bogeys 为 机械动力…',
         intro='Create: Extend Bogeys 为 机械动力 添加了更多样式、更多颜色的转向架，旨在使玩家的列车外观更加真实。',
         groups=[]),
    dict(slug='create-modern-train-parts', ns='moderntrainparts', title='Create: Modern Train Parts',
         tag='Create: Modern Train Parts…',
         intro='Create: Modern Train Parts 为游戏添加了许多现代火车部件方块，致力于使机械动力的火车更加真实。',
         groups=[]),
    dict(slug='create-more-packages', ns='ccomunityboxes', title='Create More Packages / CComunityBoxes',
         tag='Create More Packages 是一个小型的 机械动力…',
         intro='Create More Packages 是一个小型的 机械动力 扩展模组，它新增了 20 多种新的纸壳包裹，新包裹的功能与机械动力标准包裹相同。',
         groups=[]),
    dict(slug='create-recycle-everything', ns='create_crush_everything', title='Create Recycle Everything',
         tag='你是否对日复一日地清理你的箱子感到厌烦？这个模组可以让你用 粉碎轮…',
         intro='你是否对日复一日地清理你的箱子感到厌烦？这个模组可以让你用 粉碎轮 将大部分你认为不需要的物品加工/回收为原材料。',
         groups=[]),
    dict(slug='create-sabers', ns='create_sabers', title='Create Sabers',
         tag='光剑据剑柄材料可分为 黄铜 、 铜 、 锌…',
         intro='光剑据剑柄材料可分为 黄铜 、 铜 、 锌 三种（同时区分基础数值），玩家也可以将光剑与四个染料合成，把光剑染成对应的颜色（有 9 种颜色可供选择）；',
         groups=[]),
    dict(slug='create-sentry-mechanical-arm', ns='sentrymechanicalarm', title='Create: Sentry Mechanical Arm',
         tag='此模组为 机械动力 添加了哨戒动力臂，基于 Create…',
         intro='此模组为 机械动力 添加了哨戒动力臂，基于 Create 6.0.8 和 TaCZ 1.1.7 。',
         groups=[]),
    dict(slug='create-upgraded-armor', ns='create_upgraded_armor', title='Create: Upgraded Armor',
         tag='Create Ugraded 在下界合金之后又增加了一系列坚固的盔甲',
         intro='Create Ugraded 在下界合金之后又增加了一系列坚固的盔甲。',
         groups=[]),
    dict(slug='extreme-reactors-create-compat', ns='er2create', title='Extreme Reactors Create Compat',
         tag='Extreme Reactors Create Compat 附属模组',
         intro='该模组为 极限反应堆 与 机械动力 添加了部分联动，目前仅仅是将部分来自前者的设备作为 显示链接器 的信息来源。',
         groups=[]),
    dict(slug='nuka-cola-classic', ns='create_nuka_cola_classic', title='Create: Nuka Cola Classic',
         tag='你可以使用机械动力中的设备，以 火把花 和 甜浆果…',
         intro='你可以使用机械动力中的设备，以 火把花 和 甜浆果 为水制造出这种清凉怡人的美味饮料。',
         groups=[]),
    dict(slug='tongdarailway-for-forge', ns='tongdarailway_for_forge', title='TongDaRailway for Forge',
         tag='此模组是 通达铁路 的 1.20.1 Forge 移植…',
         intro='此模组是 通达铁路 的 1.20.1 Forge 移植，已经获取了原作者的同意 作者授权证明 。',
         groups=[]),
    dict(slug='vs-rotanator', ns='rotanator', title='VS: Rotanator',
         tag='VS: Rotanator 附属模组',
         intro='这是一个简单的模组，为 瓦尔基里天空 和 机械动力 之间添加了急需的 QoL 物品。',
         groups=[]),
    dict(slug='apokinetics', ns='apokinetics', title='Create: Apokinetics',
         tag='欢迎来到 Create: Apokinetics…',
         intro='欢迎来到 Create: Apokinetics。Apokinetics 让你能用 Apokinetic 扳手在支持的 Create 机器上开启镶孔，类似于神化中工具武器上的 镶孔 ，然后通过十二种不同的机器宝石（Machine Gems）精心调校你的工厂。',
         groups=[]),
    dict(slug='cbc-chemical-warfare', ns='cbc_cw', title='CBC: Chemical Warfare',
         tag='机械动力火炮：化学与生物战争模组新增多种化学试剂，基于 CBC…',
         intro='机械动力火炮：化学与生物战争模组新增多种化学试剂，基于 CBC 流体炮弹，所有试剂均具备定制特效，无论玩家是否穿戴护甲皆效果拔群。',
         groups=[]),
    dict(slug='cbc-nuclear', ns='cbc_nukes', title='CBC: Nuclear',
         tag='在某个 机械动力：火炮 的 Discord 社区第…',
         intro='在某个 机械动力：火炮 的 Discord 社区第 5,235,423,464 次核打击请求之后，它终于以这个模组的形式出现。',
         groups=[]),
    dict(slug='cccbridge', ns='cccbridge', title='CC:C Bridge',
         tag='这个模组为 机械动力 与 CC:Tweaked 和…',
         intro='这个模组为 机械动力 与 CC:Tweaked 和 CC:Restitched 提供了更多的联动性，使得利用 CC 与动力元件互动、监测动力元件的状态更加方便。',
         groups=[]),
    dict(slug='cp-tweaks', ns='cp_tweaks', title='Create Planetary Tweaks',
         tag='黄铜和锌制工具，模组没有添加锭本身，只有在加载了 机械动力…',
         intro='黄铜和锌制工具，模组没有添加锭本身，只有在加载了 机械动力 且未加载 机械动力：物品附加 的情况下才会加载配方和物品；',
         groups=[]),
    dict(slug='create-amazing-trading', ns='amazingtrading', title='Create: Amazing Trading',
         tag='该模组类似于 等价交换重制版 ，添加了 2 台依赖于 RPM…',
         intro='该模组类似于 等价交换重制版 ，添加了 2 台依赖于 RPM 运作的设备，用于将物品转换为 Resource Point，以换取物品：',
         groups=[]),
    dict(slug='create-applied-kinetics', ns='createappliedkinetics', title='Create: Applied Kinetics',
         tag='添加了 能量传输器 （Energy Provider）…',
         intro='添加了 能量传输器 （Energy Provider） ，一种可将机械能量传输进 能源接收器 的方块。',
         groups=[]),
    dict(slug='create-aquatic-ambitions', ns='create_aquatic_ambitions', title='Create: Aquatic Ambitions',
         tag='机械动力 的附属 Mod，引入一种全新的 鼓风机批量加工…',
         intro='机械动力 的附属 Mod，引入一种全新的 鼓风机批量加工 机制（Conduit Channeling），利用 潮涌框架 中激活 潮涌核心 的力量合成新的配方！',
         groups=[]),
    dict(slug='create-biotech', ns='create_biotech', title='Create: Biotech - 机械动力：生物科技',
         tag='机械动力：生物科技是一个给机械动力增加“生物零件”的附属模组…',
         intro='机械动力：生物科技是一个给机械动力增加“生物零件”的附属模组，它将生物直接接进机械动力原有的应力、物流、加工、动态结构等系统中。',
         groups=[]),
    dict(slug='create-bitterballen', ns='create_bic_bit', title='Create: Bitterballen',
         tag='A：荷兰小炸球是一种荷兰料理，由肉类裹上面糊后揉成球状后油炸而成…',
         intro='A：荷兰小炸球是一种荷兰料理，由肉类裹上面糊后揉成球状后油炸而成，有时也会加入一些切碎的蔬菜或香辛料用于调味。',
         groups=[]),
    dict(slug='create-cardboard-things', ns='createcardboardthings', title='Create: Cardboard Things',
         tag='本模组是 机械动力 附属，受到机械动力的 纸棍 启发，本附属添加了…',
         intro='本模组是 机械动力 附属，受到机械动力的 纸棍 启发，本附属添加了 9 个 纸板 主题的物品。',
         groups=[]),
    dict(slug='create-clothes', ns='createclothes', title='Create: Clothes',
         tag='这个模组新增了适用于所有生物群系的迷彩军装变体…',
         intro='这个模组新增了适用于所有生物群系的迷彩军装变体。还包含更多服饰如棒球帽和王冠等装饰物品。',
         groups=[]),
    dict(slug='create-cobblemon-industrialized', ns='create_cobblemon', title='Create: Cobblemon Industrialized',
         tag='这个 Mod 为 机械动力 添加了更多有关 方块宝可梦 的物品制作配方',
         intro='这个 Mod 为 机械动力 添加了更多有关 方块宝可梦 的物品制作配方；',
         groups=[]),
    dict(slug='create-cobblestone', ns='createcobblestone', title='Create Cobblestone',
         tag='Create Cobblestone 是一个机械动力的附属 Mod…',
         intro='Create Cobblestone 是一个机械动力的附属 Mod，主要目的是解决传统机械动力刷石机造成的卡顿问题。',
         groups=[]),
    dict(slug='create-colored-packages', ns='colored_packages', title='Create: Colored Packages',
         tag='Create: Colored 旨在为 机械动力 中的多种方块添加变种',
         intro='Create: Colored 旨在为 机械动力 中的多种方块添加变种。',
         groups=[]),
    dict(slug='create-compact_transmission', ns='create_compact_transmission', title='Create: Compact Transmission',
         tag='档位：R、N、1、2、3、4；它带有 GUI，可用于调整除 N…',
         intro='档位：R、N、1、2、3、4；它带有 GUI，可用于调整除 N 档外的每个档位的齿轮比。',
         groups=[]),
    dict(slug='create-cultivation-craft', ns='create_cultivation', title='Create: Cultivation Craft',
         tag='本模组的核心是 栽培罐 ——一种通过应力驱动…',
         intro='本模组的核心是 栽培罐 ——一种通过应力驱动，来处理植物完整生长周期的多方块机器。',
         groups=[]),
    dict(slug='create-deepfried', ns='create_deepfried', title='Create: Deepfried',
         tag='Create: Deepfried 附属模组',
         intro='这是一个 Create: Bitterballen 的拓展，添加了许多来自世界各地的油炸美食。',
         groups=[]),
    dict(slug='create-factory-controller', ns='createfactorycontroller', title='Create: Factory Controller',
         tag='机械动力：工厂控制台附属为机械动力的包裹物流提供了一个全新的集成自动…',
         intro='机械动力：工厂控制台附属为机械动力的包裹物流提供了一个全新的集成自动化调度方案。通过在“工厂控制台”的总控面板内编辑与连接高级工厂仪表，无线红石信号终端和逻辑管部件，您可以搭建一个高度自定义且高吞吐量的通用自动化系统，而无需维护大型仪表墙。',
         groups=[]),
    dict(slug='create-fantasizing-again', ns='create_fantasizing', title='Create: Fantasizing Again',
         tag='方块放置器 ：一个可以在极远的距离放置方块并立即摧毁方块的工具（曾经…',
         intro='方块放置器 ：一个可以在极远的距离放置方块并立即摧毁方块的工具（曾经的 手持式方块放置器 ，但它无需升级就已具有几乎所有的威力。大部分代码来自于 Create: Block n\' Zapping ）；',
         groups=[]),
    dict(slug='create-food', ns='createfood', title='Create: Food',
         tag='基于 农夫乐事 、 机械动力 和原版已有的食材体系所制作的食物拓展…',
         intro='基于 农夫乐事 、 机械动力 和原版已有的食材体系所制作的食物拓展 / 配方集成 Mod；',
         groups=[]),
    dict(slug='create-garnished', ns='garnished', title='Create: Garnished',
         tag='此 Mod 适用于 Fabric & Forge！（暂不提供对…',
         intro='此 Mod 适用于 Fabric & Forge！（暂不提供对 Quilt 的官方支持，不过其应该可以在 Quilt 上运行）。',
         groups=[]),
    dict(slug='create-guardian-beam-defense', ns='creategbd', title='Create Guardian Beam Defense',
         tag='这个 Mod 添加了一些以 海底神殿 为主题的防御塔…',
         intro='这个 Mod 添加了一些以 海底神殿 为主题的防御塔，这些防御塔可以像 守卫者 一样发射能够持续锁定并在一定延迟后造成伤害的激光。',
         groups=[]),
    dict(slug='create-hand-crafting', ns='create_hc', title='Create Hand Crafting - 1.18.2 - 1.20.1',
         tag='本模组为 HardRock Tools & Materials 与…',
         intro='本模组为 HardRock Tools & Materials 与 机械动力 的联动，使得机械动力中物品的合成过程更加符合 HardRock Tools & Materials 的理念。',
         groups=[]),
    dict(slug='create-high-pressure', ns='create_high_pressure', title='Create: High Pressure',
         tag='这个模组为玩家提供一种 机械动力 的量产路线来可靠地生产 钻石…',
         intro='这个模组为玩家提供一种 机械动力 的量产路线来可靠地生产 钻石 ，不过其成本是相当昂贵的！',
         groups=[]),
    dict(slug='create-horse-power', ns='createhorsepower', title='Create Horse Power',
         tag='Create Horse Power 附属模组',
         intro='该模组为 机械动力 添加了一个新的动力源—— Horse Crank，这是一种能够让马、牛等动物提供 RPM 的元件，将动物使用拴绳拴至该元件上即可。',
         groups=[]),
    dict(slug='create-ironworks', ns='create_ironworks', title='Create: Ironworks',
         tag='Create： Ironworks 通过 机械动力…',
         intro='Create： Ironworks 通过 机械动力 扩展了金属加工的部分，并添加了新的矿石和合金：如锡、青铜和钢，以及它们各自的物品和工具。',
         groups=[]),
    dict(slug='create-let-the-adventure-begin', ns='create_ltab', title='Create: Let The Adventure Begin',
         tag='Create: Let The Adventure Begin…',
         intro='Create: Let The Adventure Begin 添加了许多原版风以及机械动力风的建筑物。',
         groups=[]),
    dict(slug='create-logistics', ns='create_logistics', title='Create Logistics',
         tag='该物品需要使用 物品保险库 合成，外观类似于 工具箱 ，可以存放…',
         intro='该物品需要使用 物品保险库 合成，外观类似于 工具箱 ，可以存放 3,200 个同种物品。',
         groups=[]),
    dict(slug='create-love-war', ns='createloveandwar', title='Create: Love & War',
         tag='Create: Love & War 是一个以 机械动力…',
         intro='Create: Love & War 是一个以 机械动力 风格制作的 Flan的枪械重制版 的内容包，添加了用机械动力机制生产的枪械零件和弹药。',
         groups=[]),
    dict(slug='create-mechanical-chicken', ns='create_mechanical_chicken', title='Create Mechanical Chicken',
         tag='在机械鸡的底部连接动力，前部输入液体 Seed…',
         intro='在机械鸡的底部连接动力，前部输入液体 Seed Oil（制作方式如下图，种子种类不限），后部接入输出安山漏斗（黄铜漏斗亦可）可产生鸡蛋。',
         groups=[]),
    dict(slug='create-mechanical-companion', ns='createmechanicalcompanion', title='Create: Mechanical Companion',
         tag='召唤机械狼的方法： 在 Curios 的头饰栏中装备 “…',
         intro='召唤机械狼的方法： 在 Curios 的头饰栏中装备 “ 机械狼联结（ Mechanical Wolf Link） ” 道具。',
         groups=[]),
    dict(slug='create-mechanical-spawner', ns='create_mechanical_spawner', title='Create Mechanical Spawner',
         tag='[JEI] JEI 物品管理器 (Just Enough…',
         intro='[JEI] JEI 物品管理器 (Just Enough Items) 和 玉 🔍 (Jade 🔍) 集成；',
         groups=[]),
    dict(slug='create-metallurgy', ns='createmetallurgy', title='Create: Metallurgy',
         tag='机械动力：冶金学是 Luc_Creeper74 开发的 机械动力…',
         intro='机械动力：冶金学是 Luc_Creeper74 开发的 机械动力 拓展，适用于机械动力0.5.1c以上版本。',
         groups=[]),
    dict(slug='create-metalwork', ns='createmetalwork', title='Create: Metalwork',
         tag='该模组基于 Kaupenjoe 的模板 制作，流体代码来自…',
         intro='该模组基于 Kaupenjoe 的模板 制作，流体代码来自 Delightful Creators ，流体材质与部分物品材质来自 机械动力 。',
         groups=[]),
    dict(slug='create-militarized', ns='create_militarized_', title='Create Militarized',
         tag='新设备：Coke Furnace、Supercomputer…',
         intro='新设备：Coke Furnace、Supercomputer、Uranium Processor；',
         groups=[]),
    dict(slug='create-mobile-packages', ns='create_mobile_packages', title='Create: Mobile Packages',
         tag='此模组拓展了 机械动力 的物流系统，添加了运送机械动力 包裹…',
         intro='此模组拓展了 机械动力 的物流系统，添加了运送机械动力 包裹 的运输蜂和相关物品。',
         groups=[]),
    dict(slug='create-molten-metals', ns='molten_metals', title='Create: Molten Metals',
         tag='你的心里是否也有一个被匠魂凿出的洞？为什么不把它填满融化的铅呢？本模…',
         intro='你的心里是否也有一个被匠魂凿出的洞？为什么不把它填满融化的铅呢？本模组正是因此而生！',
         groups=[]),
    dict(slug='create-more-drill-heads', ns='createmoredrillheads', title='Create: More Drill Heads',
         tag='同时添加了附魔效果钻头，可以使用机械手为本 Mod 钻头安装红石粉…',
         intro='同时添加了附魔效果钻头，可以使用机械手为本 Mod 钻头安装红石粉、石英粉、绿宝石粉或紫水晶粉实现：',
         groups=[]),
    dict(slug='create-more-sandpapers', ns='createsandpapers', title='Create: More Sandpapers',
         tag='Create: More Sandpapers 附属模组',
         intro='该模组为 灵魂沙 以及来自 超多生物群系 、 你将去的生物群系 的沙子添加了对应的 砂纸 。',
         groups=[]),
    dict(slug='create-netherite-additions', ns='create_nj', title='Create Stuff & Netherite Additions',
         tag='Create Stuff & Netherite…',
         intro='Create Stuff & Netherite Additions 为 Create Stuff & Additions 添加了下界合金质的喷气背包和外骨骼。',
         groups=[]),
    dict(slug='create-netherless', ns='create_netherless', title='Create: Netherless',
         tag='这个 MC 模组是专为 机械动力 设计的一个附属…',
         intro='这个 MC 模组是专为 机械动力 设计的一个附属。该附属旨在使所有来自下界的资源（如 下界疣块 、 下界合金 、 下界岩 、 灵魂沙 、 下界石英 、 黑石 等）都能在主世界内制作，而无需离开主世界（同时也不会阻止玩家前往下界）…',
         groups=[]),
    dict(slug='create-northstar', ns='northstar', title='Create: Northstar',
         tag='受 Micdoodle 的 Galacticraft 的启发…',
         intro='受 Micdoodle 的 Galacticraft 的启发，Northstar 想用 机械动力 的力量让玩家重返星空。',
         groups=[]),
    dict(slug='create-nuke', ns='create_nuke', title='Create: Nuke',
         tag='Create: Nuke 附属模组',
         intro='这是一个 机械动力：电气时代 的拓展，添加了使用前者的放射性材料制作的核弹。',
         groups=[]),
    dict(slug='create-optical', ns='create_optical', title='Create Optical',
         tag='Create Optical 附属模组',
         intro='这是一个基于光学的 机械动力 附属模组，其提供了光束和旋转力相互转化的方法并添加了一些光学相关的组件。',
         groups=[]),
    dict(slug='create-ornithopter-glider', ns='createornithopterglider', title='Create: Ornithopter Glider',
         tag='Ornithopter Glider 是一款自定义滑翔翼模组…',
         intro='Ornithopter Glider 是一款自定义滑翔翼模组，为飞行带来全新体验。',
         groups=[]),
    dict(slug='create-peaceful', ns='create_peaceful', title='Create: Peaceful',
         tag='Create: Peaceful 提供了通过相对和平的方式获取大多数…',
         intro='Create: Peaceful 提供了通过相对和平的方式获取大多数动物和敌对生物掉落物的途径。',
         groups=[]),
    dict(slug='create-pipe-networks', ns='pipe_networks', title='Create: Pipe Networks',
         tag='Create: Pipe Networks 是 机械动力…',
         intro='Create: Pipe Networks 是 机械动力 模组的一款扩展模组，它通过彩色编码管道扩展了流体物流系统。',
         groups=[]),
    dict(slug='create-pneumatic-equipment', ns='create_pneuequip', title='Create: pneumatic equipment',
         tag='当它们的耐久耗尽以后，仅有 Chisel 与 Chain Saw…',
         intro='当它们的耐久耗尽以后，仅有 Chisel 与 Chain Saw 这两样消耗品会消失，工具本身及其上的附魔均会保留。',
         groups=[]),
    dict(slug='create-protection-pixel', ns='protection_pixel', title='Create: Protection Pixel',
         tag='机素防护（Protection Pixel）为玩家带蒸汽朋克风格的护…',
         intro='机素防护（Protection Pixel）为玩家带蒸汽朋克风格的护甲，丰富了他们的冒险之旅。每部分护甲都有不同的功能和属性，以帮助玩家适应Minecraft中丰富的环境并以他们擅长和喜好的方式作战。同时玩家可以借助 机械动力 的庞大工业体系合成、加工…',
         groups=[]),
    dict(slug='create-ratatouille', ns='ratatouille', title='Create Ratatouille',
         tag='本模组是机械动力的一个附属，旨在为农业种植…',
         intro='本模组是机械动力的一个附属，旨在为农业种植、食品加工添加更多便利机器方块与物品拓展。同时也是同名整合包专用的模组。',
         groups=[]),
    dict(slug='create-remote-terminal', ns='createterminal', title='Create: Remote Terminal',
         tag='机械动力：远程终端 模组添加了一款手持物品，允许玩家在最远 20…',
         intro='机械动力：远程终端 模组添加了一款手持物品，允许玩家在最远 20 格方块范围内与仓库管理员系统进行交互。',
         groups=[]),
    dict(slug='create-simple-generator', ns='create_simple_generator', title='Create: Simple Generator',
         tag='默认情况下，每游戏刻会消耗 1 点应力（乘以速度系数），并产生 1…',
         intro='默认情况下，每游戏刻会消耗 1 点应力（乘以速度系数），并产生 1 点 FE 能量（乘以速度系数）。',
         groups=[]),
    dict(slug='create-stock-bridge', ns='createstockbridge', title='Create Stock Bridge',
         tag='该模组实现了 应用能源 2 与 机械动力 的兼容性联动…',
         intro='该模组实现了 应用能源 2 与 机械动力 的兼容性联动。使用本模组需预先安装机械动力和应用能源 2。',
         groups=[]),
    dict(slug='create-tacz-automation', ns='createtaczauto', title='Create: TaCZ Automation',
         tag='作者不允许在 非 CurseForge 或 Modrinth…',
         intro='作者不允许在 非 CurseForge 或 Modrinth 整合包内上传该模组。',
         groups=[]),
    dict(slug='create-tank-defenses', ns='create_tank_defenses', title='Create: Tank Defenses',
         tag='机械动力：坦克防御（CTD）新增了许多装甲块以便玩家保护好自己的基地…',
         intro='机械动力：坦克防御（CTD）新增了许多装甲块以便玩家保护好自己的基地、大炮、坦克、飞机以及船舶。尽管只需要 机械动力 作为前置，但 CTD 需要与、 机械动力：火炮 、 瓦尔基里天空 、 Eureka! Airships! 、 Clockwork…',
         groups=[]),
    dict(slug='create-totem-factory', ns='totemfactory', title='Create: Totem Factory',
         tag='依次使用动力锯和动力辊压机来处理黄铜板制得头部外壳…',
         intro='依次使用动力锯和动力辊压机来处理黄铜板制得头部外壳。然后给头部外壳注入抗火药水和再生药水并用黄铜锭密封，此过程会为其添加不死图腾标志性的鼻子。',
         groups=[]),
    dict(slug='create-tweaked-controllers', ns='create_tweaked_controllers', title='Create: Tweaked Controllers',
         tag='终于不是6键残疾人了',
         intro='这是一个 机械动力 附属模组，让你使用一个高级的遥控器控制你的装置，你可以用你的鼠标，键盘甚至你的游戏手柄使用！ 终于不是6键残疾人了',
         groups=[]),
    dict(slug='create-unify', ns='unify', title='Create: Unify',
         tag='Create: Unify 旨在帮助统一一些大多数模组中常见的材料…',
         intro='Create: Unify 旨在帮助统一一些大多数模组中常见的材料，以避免在同一个整合包中同时出现来自多个模组的同一种材料的状况。',
         groups=[]),
    dict(slug='create-vintage-improvements', ns='vintageimprovements', title='Create: Vintage Improvements',
         tag='Create: Vintage Improvements…',
         intro='Create: Vintage Improvements 是一个加入了许多新的动力设备与材料的 机械动力 附属。并且与 CC&A 和 Ad Astra! 间有联动。',
         groups=[]),
    dict(slug='create-weaponry', ns='create_wt', title='Create Weaponry',
         tag='MC 1.19.2 版本需额外下载 Create…',
         intro='MC 1.19.2 版本需额外下载 Create Planetary Tweaks 作为前置。',
         groups=[]),
    dict(slug='create-wizardry', ns='create_wizardry', title='Create: Wizardry',
         tag='本模组是一个 机械动力 的附属模组，为其添加了与…',
         intro='本模组是一个 机械动力 的附属模组，为其添加了与 Iron的法术与魔法书 的联动内容。',
         groups=[]),
    dict(slug='createadvlogistics', ns='createadvlogistics', title='Create: Advanced Logistics',
         tag='Create: Advanced Logistics…',
         intro='Create: Advanced Logistics 是一个正在开发中的 机械动力 模组扩展包，旨在为高级物流系统添加若干实用功能。',
         groups=[]),
    dict(slug='createlights-controls', ns='create_lac', title='Create: Lights & Controls',
         tag='一个 机械动力 的附属模组，提供了完整的光源方块…',
         intro='一个 机械动力 的附属模组，提供了完整的光源方块、红石控制以及扬声模块！所有元件均可以直接连接到 Create 的无线红石信号网络，实现干净的无线自动化！',
         groups=[]),
    dict(slug='createnuclear', ns='createnuclear', title='Create Nuclear',
         tag='机械动力：原子核动（Create Nuclear）…',
         intro='机械动力：原子核动（Create Nuclear） 是一个将整个核能系统添加到 机械动力 的附属 Mod。添加了铀矿及其精炼过程，以及因核污染形成的一系列方块和生物。该模组的反应堆可以为机械动力产生超过 100 万的应力…',
         groups=[]),
    dict(slug='createtools-n-weapons', ns='create_tools_n_weapons', title='Create: Tools n Weapons',
         tag='这个模组添加了一套新工具，风格与 机械动力 保持一致…',
         intro='这个模组添加了一套新工具，风格与 机械动力 保持一致。这些工具各有其动力合成配方，强度略高于下界合金工具！',
         groups=[]),
    dict(slug='creating-space', ns='creatingspace', title='Creating Space',
         tag='类似于 高级火箭 模组（而不是航天学），它使用动态结构来实现火箭',
         intro='类似于 高级火箭 模组（而不是航天学），它使用动态结构来实现火箭。',
         groups=[]),
    dict(slug='deep_space', ns='deep_space', title='Deep Space',
         tag='Deep Space 附属模组',
         intro='注意：此模组依赖 瓦尔基里天空 ，但该模组目前不支持 机械动力 6.0 版本，请使用 机械动力 0.5.1j 版本。',
         groups=[]),
    dict(slug='delivery-director', ns='delivery_director', title='Create: Delivery Director [Discontinued]',
         tag='Create: Delivery Director 是一款专注于为…',
         intro='Create: Delivery Director 是一款专注于为 机械动力 模组的包裹系统增添新功能的模组。',
         groups=[]),
    dict(slug='direct-chute', ns='direct_chute', title='Create: Direct Chute',
         tag='添加一种新型溜槽，无方块实体，无容器槽位…',
         intro='添加一种新型溜槽，无方块实体，无容器槽位。它直接抓取物品并放入下方容器的空间中，无法从地面收集物品。',
         groups=[]),
    dict(slug='ethium', ns='ethium_reimagined', title='Create: Ethium Reimagined',
         tag='本模组添加了一种新材料——Ethium，玩家需要使用工作盆和搅拌机…',
         intro='本模组添加了一种新材料——Ethium，玩家需要使用工作盆和搅拌机，在加热的前提下，向工作盆中投入下界合金锭、绿宝石、青金石、黄铜锭和经验颗粒混合搅拌以合成。',
         groups=[]),
    dict(slug='expandingtechnologies', ns='expandingtechnologies', title='Expanding Technologies',
         tag='Railroad Light Controller：用于配合辉光管搭…',
         intro='Railroad Light Controller：用于配合辉光管搭建多种铁路信号灯；',
         groups=[]),
    dict(slug='extended-wrenches', ns='extendedwrenches', title='Create: Extended Wrenches',
         tag='Extended Wrenches 模组允许你自定义 机械动力…',
         intro='Extended Wrenches 模组允许你自定义 机械动力 模组中的 扳手 ，使其符合你的风格。',
         groups=[]),
    dict(slug='extra-gauges', ns='extra_gauges', title='Create: Extra Gauges',
         tag='机械动力：更多仪表 是 机械动力 的一个附属模组…',
         intro='机械动力：更多仪表 是 机械动力 的一个附属模组，它通过引入新型仪表和智能逻辑工具，进一步拓展了自动化玩法。',
         groups=[]),
    dict(slug='fishy-create-stuffs', ns='fishycreatestuffs', title='Fishy Create Stuffs',
         tag='贯通轴齿轮箱：这个齿轮箱的其中两面由一根轴贯通…',
         intro='贯通轴齿轮箱：这个齿轮箱的其中两面由一根轴贯通，所以这两个面的旋转方向是相同的。这一方块可以使搭建一些机器变得更简单。',
         groups=[]),
    dict(slug='frequency-create', ns='frequency', title='Frequency Create',
         tag='Frequency for Create…',
         intro='Frequency for Create 是一款针对机械动力模组的实用性（QoL）附属模组。它添加了一系列符号物品，专门用于配置无线红石信号的频率。',
         groups=[]),
    dict(slug='greate', ns='greate', title='Greate',
         tag='目前还未完成机器/配方分级系统（配方要求的最小机器等级…',
         intro='目前还未完成机器/配方分级系统（配方要求的最小机器等级，机器单次能处理的物品数量），这些会在后续得到补充。',
         groups=[]),
    dict(slug='has-basin-output-faucet-depot', ns='hasbasinoutputfaucetdepot', title='Has Basin Output Faucet Depot',
         tag='Has Basin Output Faucet Depot 附属模组',
         intro='注意：不要下载 1.0.0 版本，这个版本有 Bug，使用鼓风机会导致崩溃，1.0.1修复了这个 Bug。',
         groups=[]),
    dict(slug='hypertube', ns='create_hypertube', title='Create: Hypertubes',
         tag='你有没有想过在 Minecraft 中建立像…',
         intro='你有没有想过在 Minecraft 中建立像 幸福工厂（Satisfactory） 一样的交通系统？',
         groups=[]),
    dict(slug='interactive', ns='create_interactive', title='Create: Interactive',
         tag='借助此模组，你可以以前所未有的方式与你的机械动力动态结构互动！所有的…',
         intro='借助此模组，你可以以前所未有的方式与你的机械动力动态结构互动！所有的动态结构都可以像 Minecraft 的方块一样，所以可以尽情地建造、破坏、堆叠和造成可控的混乱！',
         groups=[]),
    dict(slug='klinksnklangs', ns='create_klinks_n_klangs', title='Create: Klinks n\' Klangs',
         tag='叮当声与撞击声：机械动力的音效与装饰件',
         intro='这是一个与 方块宝可梦 的扩展模组，可以让你在使用 机械动力 时实现更好的自动化。',
         groups=[]),
    dict(slug='lijms-expanse', ns='lijms_expanse', title='Lijm\'s Expanse',
         tag='Lijm’s Expanse 为 Minecraft…',
         intro='Lijm’s Expanse 为 Minecraft 新增枪械制造与车辆组装玩法，为你的世界注入现代工业元素。',
         groups=[]),
    dict(slug='missions', ns='missions', title='Create: Missions',
         tag='作者希望为服务器的所有者提供更好的方式并为玩家们提供货币…',
         intro='作者希望为服务器的所有者提供更好的方式并为玩家们提供货币，同时也鼓励玩家建立自己的商店装置 / 兑换银行 / 银行。',
         groups=[]),
    dict(slug='more-create-burners', ns='moreburners', title='More Create Burners',
         tag='机械动力：更多燃烧室 是一个 机械动力 的附属，该 Mod…',
         intro='机械动力：更多燃烧室 是一个 机械动力 的附属，该 Mod 的目标是添加不同类型的燃烧器，并与不同的流行 Mod 相连结。',
         groups=[]),
    dict(slug='neokuayue', ns='kuayue', title='NeoKuayue',
         tag='经过一年多的紧张重置与开发，新版本的跨越将带着全新架构、全新内容…',
         intro='经过一年多的紧张重置与开发，新版本的跨越将带着全新架构、全新内容、全新体验回归。这段时间里，跨越制作组彻底重置了跨越的代码结构，修复了老版本当中的许多问题，给各位玩家带来更清爽的游戏体验；同时，向模组中加入了大量全新内容供大家探索。',
         groups=[]),
    dict(slug='northstar-redux', ns='northstar', title='Create: Northstar - Redux',
         tag='此模组为 机械动力：北极星 的高版本重制版，添加了对于…',
         intro='此模组为 机械动力：北极星 的高版本重制版，添加了对于 Minecraft 1.21.1 与 机械动力 6.0 的支持。',
         groups=[]),
    dict(slug='petrols-parts', ns='petrolsparts', title='Petrol\'s Parts',
         tag='应大众需求，在 v0.1.0 后， Destroy…',
         intro='应大众需求，在 v0.1.0 后， Destroy 中的传动元件被拆分至本 Mod，因此你可以在不获取 Destroy 时游玩该部分。',
         groups=[]),
    dict(slug='precise-manufacturing', ns='prma', title='[TACZ] Create: Precise Manufacturing',
         tag='一个给 永恒枪械工坊：零 中的物品和武器添加了可自动化配方的…',
         intro='一个给 永恒枪械工坊：零 中的物品和武器添加了可自动化配方的 机械动力 附属模组。',
         groups=[]),
    dict(slug='so-crazy-try', ns='so_crazy_try', title='So crazy try',
         tag='模组永远不会支持 Fabric，若需要 Fabric 版本请安装…',
         intro='模组永远不会支持 Fabric，若需要 Fabric 版本请安装 Kilt 。模组仅支持 Forge（1.20） 和 NeoForge（1.21+）；',
         groups=[]),
    dict(slug='tinkers-gears', ns='tgears', title='Tinkers\' Gears',
         tag='匠械 是一个专门面向 机械动力 与 匠魂 3 的联动模组…',
         intro='匠械 是一个专门面向 机械动力 与 匠魂 3 的联动模组，尝试在两个模组直接创作出独具创新的内容。',
         groups=[]),
    dict(slug='tofu-create', ns='tofucreate', title='Tofu Create',
         tag='这个模组为 豆腐工艺重制版 添加了基于 机械动力 的豆腐与豆奶配方',
         intro='这个模组为 豆腐工艺重制版 添加了基于 机械动力 的豆腐与豆奶配方。',
         groups=[]),
    dict(slug='trackwork', ns='trackwork', title='Trackwork',
         tag='驱动工艺（Trackwork） 是 瓦尔基里天空 和 机械动力…',
         intro='驱动工艺（Trackwork） 是 瓦尔基里天空 和 机械动力 的拓展，可为物理结构添加履带和轮胎，让物理结构能在复杂的地形上行驶！',
         groups=[]),
    dict(slug='train-deco', ns='traindeco', title='Create: Train Deco',
         tag='目前正在测试阶段，且更新不一定很快',
         intro='这是一个简单机械动力附属 Mod，加入了一些关于地铁列车装饰的方块。目前正在测试阶段，且更新不一定很快。',
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
    dict(slug='create-more-features', ns='create_more_features', title='Create: More Features',
         tag='给机械动力补一批零件与功能方块',
         intro='一批独立的零件和功能方块，直接插进 Create 的产线里用，不改变原有玩法。',
         groups=[]),
    dict(slug='create-more-seats', ns='create_more_seats', title='Create: More Seats',
         tag='给列车和结构补一批可坐的座椅',
         intro='只做一件事：加更多样式的座椅，放在列车车厢或建筑里都能坐。',
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

    # ── 标签的图标与中文名：从已生成的 tags/<file>.html 里读 ──
    _tag_cache = {}
    def tag_meta(tg):
        """返回 (icon相对路径 或 None, 中文名 或 None)"""
        if tg in _tag_cache:
            return _tag_cache[tg]
        # 标签页文件名规则（与 gen_site.py 的 tag 页命名一致）
        fname = tg.replace(':', '_').replace('/', '_') + '.html'
        path = os.path.join(SITE, 'tags', fname)
        icon = name = None
        if os.path.exists(path):
            try:
                h = io.open(path, encoding='utf-8').read()
                m = re.search(r'<img class="big" src="\.\./(assets/icons/[^"]+)"', h)
                if m:
                    icon = m.group(1)
                m2 = re.search(r'<h1><i class="hash">#</i>([^<]+)</h1>', h)
                if m2:
                    name = m2.group(1).strip()
            except Exception:
                pass
        # 回退：裸标签（无命名空间，如 #steel）按成员名猜图标
        if not icon:
            seg = tg.split('/')[-1].split(':')[-1]
            # 候选前缀：当前模组 ns 优先，其次通用
            pres = [ns + '_', '', 'create_', 'minecraft_', '3d_create_',
                    '3d_' + ns + '_', 'hh3d_']
            for pre in pres:
                cand = pre + seg + '.png'
                if os.path.exists(os.path.join(ICONS, cand)):
                    icon = 'assets/icons/' + cand
                    break
            # 再退一步：找任意 *<seg>_ingot / *<seg>_sheet 之类的代表图
            if not icon:
                for suf in ('_ingot', '_sheet', '_block'):
                    for f in os.listdir(ICONS):
                        if f.endswith(seg + suf + '.png'):
                            icon = 'assets/icons/' + f
                            break
                    if icon:
                        break
            # 终极回退：用标签名的关键词在 icons 里模糊找一张同 ns 的图
            if not icon:
                ns_pre = (tg.split(':')[0] + '_') if ':' in tg else ''
                words = [w for w in re.split(r'[_/\s]+', seg) if len(w) >= 4]
                for w in words:
                    best = None
                    for f in os.listdir(ICONS):
                        if not f.endswith('.png'):
                            continue
                        if ns_pre and not f.startswith(ns_pre):
                            continue
                        if w in f:
                            best = f
                            break
                    if best:
                        icon = 'assets/icons/' + best
                        break
            if not name:
                name = seg.replace('_', ' ')
        _tag_cache[tg] = (icon, name)
        return icon, name

    def chip(st):
        if isinstance(st, list):
            st = st[0] if st else {}
        if not isinstance(st, dict):
            st = {}
        if not st:
            return ''
        if st.get('tag'):
            tg = st['tag'].lstrip('#')
            _ic, _nm = tag_meta(tg)
            _label = _nm or tg.split('/')[-1].replace('_', ' ')
            if _ic:
                return '<span class="ch tag"><img src="%s" alt="">%s</span>' % (_ic, _label)
            return '<span class="ch tag">#%s</span>' % _label
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
        if isinstance(d, list):
            d = d[0] if d and isinstance(d[0], dict) else {}
        if not isinstance(d, dict):
            d = {}
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
            _res = d.get('results') or d.get('result')
            if isinstance(_res, list):
                _res = _res[0] if _res else {}
            if isinstance(_res, list):
                _res = _res[0] if _res else {}
            out = _res if isinstance(_res, dict) else {}
            return ('<div class="rec"><div class="grid" style="grid-template-columns:repeat(%d,1fr)">%s</div><div class="arw">→</div>%s'
                    '<span class="mach">%s</span></div>' % (w, ''.join(cells), chip(out), mach))
        ings = d.get('ingredients') or []
        agg, order = {}, []
        for x in ings:
            if isinstance(x, list):
                x = x[0] if x and isinstance(x[0], dict) else {}
            if not isinstance(x, dict):
                continue
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
        _res = d.get('results') or d.get('result')
        if isinstance(_res, list):
            _res = _res[0] if _res else {}
        if isinstance(_res, list):
            _res = _res[0] if _res else {}
        out = _res if isinstance(_res, dict) else {}
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
