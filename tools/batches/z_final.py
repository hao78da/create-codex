item("create:crushed_raw_iron", "粉碎铁矿石：烧之前先碎一遍", [
    ("怎么获得", "<p>把<strong>铁矿石</strong>丢进<strong>粉碎轮</strong>（Crushing Wheel）就得到粉碎铁矿石，一台轮子两个轮盘对转，矿石从中间过。粉碎不需要加热，但要动力。</p><p>粉碎是「选矿」的第一步：碎过的矿烧起来出更多铁，比直接烧矿石划算。</p>"),
    ("怎么用", "<p>用途：<strong>提高金属产量</strong>。粉碎矿 → 熔炉烧成锭；或者进一步<strong>洗涤</strong>（鼓风机 + 水）得到可熔炼的矿粒，产量再高一档。</p><p>铁、铜、金、锌都有对应的粉碎矿，是金属产线的标准起点。</p>"),
    ("常见坑", "<p>第一坑：<strong>直接用矿石烧</strong>，白白浪费产量。第二坑：粉碎轮转速不够，矿石卡在轮子里。</p><p>第三，粉碎轮会把物品弹出来，记得用漏斗/带子接住产物。</p>"),
], params=[("类型", "中间材料"), ("工艺", "粉碎"), ("用途", "提高金属产量")],
   related=["create:crushing_wheel", "create:crushed_raw_copper", "create:encased_fan"])

item("create:crushed_raw_copper", "粉碎铜矿石：铜产线的起点", [
    ("怎么获得", "<p>铜矿石过<strong>粉碎轮</strong>得到粉碎铜矿石。铜是 Create 里用量最大的金属之一（管道、机壳、线圈），所以铜矿粉碎线几乎是必建的第一条产线。</p><p>粉碎后的铜矿可以烧成铜锭，也可以洗涤成铜粒再烧。</p>"),
    ("怎么用", "<p>用途：<strong>量产铜锭</strong>。粉碎 → 洗涤 → 熔炼，是收益最高的路线；懒一点就直接粉碎 → 熔炼。</p><p>铜锭再压成铜板，做流体管道、储罐、机壳，形成完整链条。</p>"),
    ("常见坑", "<p>第一坑：<strong>粉碎轮堵住</strong>，矿石堆积不进去。第二坑：没接产物容器，粉碎铜矿散一地。</p><p>第三，铜矿分布广但用量大，早点建自动化粉碎线。</p>"),
], params=[("类型", "中间材料"), ("工艺", "粉碎"), ("用途", "铜锭产线")],
   related=["create:crushing_wheel", "create:copper_sheet", "create:fluid_pipe"])

item("create:crushed_raw_gold", "粉碎金矿石：为电子件备料", [
    ("怎么获得", "<p>金矿石过<strong>粉碎轮</strong>得到粉碎金矿石。金在 Create 里主要用于电子管、精密构件和装饰，需求量比铁铜小，但中期开始明显增加。</p><p>粉碎后熔炼成金锭，再压成金板。</p>"),
    ("怎么用", "<p>用途：<strong>金板 / 电子件</strong>。金板是精密构件的原料之一，电子管、显示设备都要用到。</p><p>金矿常与其它矿伴生，建一条共用粉碎线即可。</p>"),
    ("常见坑", "<p>第一坑：<strong>把金当建材</strong>，很快就不够用。第二坑：粉碎线只处理铁矿，金矿还得手动补。</p><p>第三，金矿产量低，别指望它撑起大规模产线。</p>"),
], params=[("类型", "中间材料"), ("工艺", "粉碎"), ("用途", "金板 / 电子件")],
   related=["create:crushing_wheel", "create:golden_sheet", "create:electron_tube"])

item("create:crushed_raw_zinc", "粉碎锌矿石：黄铜的原料", [
    ("怎么获得", "<p>锌矿石过<strong>粉碎轮</strong>得到粉碎锌矿石。锌是黄铜的另一半，黄铜产线一开，锌的需求就上来了。</p><p>粉碎锌矿熔炼成锌锭，再和铜一起搅拌成黄铜。</p>"),
    ("怎么用", "<p>用途：<strong>炼黄铜</strong>。1 铜锭 + 1 锌锭在加热的工作盆里搅出 2 个黄铜锭，锌的供应直接决定黄铜产量。</p><p>锌矿比铜少，建议单独建一条粉碎线，别和铁铜抢机器。</p>"),
    ("常见坑", "<p>第一坑：<strong>锌矿不够</strong>，黄铜线三天两头停。第二坑：粉碎后的锌矿和粗锌混在一起烧，产量算不清。</p><p>第三，锌不要拿去做装饰，留着炼黄铜更值。</p>"),
], params=[("类型", "中间材料"), ("工艺", "粉碎"), ("用途", "黄铜")],
   related=["create:crushing_wheel", "create:brass_ingot", "create:zinc_ingot"])

item("create:crushed_raw_tin", "粉碎锡矿石：来自其它模组的金属", [
    ("怎么获得", "<p>锡矿石来自<strong>其它模组</strong>（如热力、工业类模组），Create 提供粉碎兼容配方：把锡矿石丢进粉碎轮，得到粉碎锡矿石。</p><p>如果你没装产锡的模组，这个物品不会出现。</p>"),
    ("怎么用", "<p>用途：<strong>兼容其它模组的金属产线</strong>。粉碎锡矿 → 熔炼成锡锭，供那些模组的配方使用。</p><p>Create 本身不用锡，它只是把粉碎轮接进了通用矿物处理链。</p>"),
    ("常见坑", "<p>第一坑：<strong>没装对应模组</strong>却去找锡矿，白费功夫。第二坑：把锡和锌搞混，两者外观相近但用途不同。</p><p>第三，跨模组配方可能随整合包变化，以实际配方为准。</p>"),
], params=[("类型", "中间材料"), ("来源", "其它模组"), ("工艺", "粉碎")],
   related=["create:crushing_wheel", "create:crushed_raw_zinc", "create:crushed_raw_iron"])

item("create:crushed_raw_platinum", "粉碎铂矿石：稀有金属的中间物", [
    ("怎么获得", "<p>铂矿石同样来自<strong>其它模组</strong>，Create 提供粉碎兼容：铂矿石 → 粉碎铂矿石。</p><p>铂是稀有金属，矿脉少、产量低，通常出现在深层。</p>"),
    ("怎么用", "<p>用途：<strong>供给其它模组的高级配方</strong>。粉碎 → 熔炼 → 铂锭，用于那些模组的工具、装备与机器。</p><p>Create 自身不消耗铂。</p>"),
    ("常见坑", "<p>第一坑：<strong>把铂矿当普通矿</strong>直接烧，浪费粉碎增产。第二坑：铂矿难找，别拿它做装饰。</p><p>第三，跨模组配方以整合包为准。</p>"),
], params=[("类型", "中间材料"), ("来源", "其它模组"), ("稀有度", "高")],
   related=["create:crushing_wheel", "create:crushed_raw_gold", "create:crushed_raw_quicksilver"])

item("create:crushed_raw_quicksilver", "粉碎水银矿石：炼金类模组的材料", [
    ("怎么获得", "<p>水银矿石来自<strong>炼金/魔法类模组</strong>，Create 提供粉碎兼容配方：水银矿石 → 粉碎水银矿石。</p><p>没有对应模组时不会生成。</p>"),
    ("怎么用", "<p>用途：<strong>跨模组材料处理</strong>。粉碎后熔炼或直接用于其它模组的炼金配方。</p><p>Create 自身不消耗水银。</p>"),
    ("常见坑", "<p>第一坑：<strong>和锌矿混淆</strong>，两者都是银灰色。第二坑：水银相关配方常有危险（爆炸/中毒），按整合包说明操作。</p><p>第三，别把水银当建材。</p>"),
], params=[("类型", "中间材料"), ("来源", "其它模组"), ("工艺", "粉碎")],
   related=["create:crushing_wheel", "create:crushed_raw_platinum", "create:crushed_raw_tin"])

item("create:brass_casing", "黄铜机壳：机器的黄铜外衣", [
    ("怎么获得", "<p>黄铜机壳用<strong>黄铜板 + 木板</strong>在工作台合成（黄铜板由压床压黄铜锭得到）。它是所有黄铜机器的外壳材料。</p><p>和安山机壳一样，是「包住机器」的方块，但等级更高。</p>"),
    ("怎么用", "<p>用途：合成<strong>黄铜机器</strong>（黄铜漏斗、黄铜隧道、列车部件、机械臂等），也可以直接当装饰方块铺墙面。</p><p>黄铜机壳能包裹传动轴、齿轮，做成「包壳传动」，防雨防尘还好看。</p>"),
    ("常见坑", "<p>第一坑：<strong>黄铜板不够</strong>，卡在机壳这一步。第二坑：把黄铜机壳当安山机壳用，配方对不上。</p><p>第三，机壳包轴要用对应工具（扳手）操作，别硬放。</p>"),
], params=[("类型", "机壳"), ("材料", "黄铜板 + 木板"), ("用途", "黄铜机器")],
   related=["create:brass_sheet", "create:andesite_casing", "create:brass_funnel"])

item("create:refined_radiance_casing", "光辉机壳：会发光的机壳", [
    ("怎么获得", "<p>光辉机壳用<strong>光辉石（Refined Radiance）+ 机壳材料</strong>合成，是终局装饰/机器外壳，自带发光效果。</p><p>光辉石本身由异彩化合物进一步加工得到，属于后期内容。</p>"),
    ("怎么用", "<p>用途：<strong>高级机器外壳与装饰</strong>。发光特性让它适合做控制室、展台、夜间的建筑线条。</p><p>也可以包传动轴做发光管道。</p>"),
    ("常见坑", "<p>第一坑：<strong>光辉石产量低</strong>，别大面积铺。第二坑：把它当普通机壳合成机器，配方不通用。</p><p>第三，发光不等于照明，亮度有限。</p>"),
], params=[("类型", "机壳"), ("特点", "发光"), ("阶段", "后期")],
   related=["create:refined_radiance", "create:shadow_steel_casing", "create:chromatic_compound"])

item("create:shadow_steel_casing", "暗影机壳：吸收光的机壳", [
    ("怎么获得", "<p>暗影机壳用<strong>暗影钢（Shadow Steel）+ 机壳材料</strong>合成，是另一种终局外壳，外观暗黑、几乎不反光。</p><p>暗影钢由异彩化合物在特定条件下转化得到。</p>"),
    ("怎么用", "<p>用途：<strong>暗色建筑与高级机器</strong>。和光辉机壳成对，一个发光一个吸光，适合做对比强烈的建筑。</p><p>也能包传动轴。</p>"),
    ("常见坑", "<p>第一坑：<strong>与光辉机壳配方搞混</strong>，材料不通用。第二坑：暗影钢难量产，别拿来铺地。</p><p>第三，暗色在夜里几乎看不见，照明要另配。</p>"),
], params=[("类型", "机壳"), ("特点", "吸光 / 暗色"), ("阶段", "后期")],
   related=["create:shadow_steel", "create:refined_radiance_casing", "create:chromatic_compound"])

item("create:refined_radiance", "光辉石：终局的发光材料", [
    ("怎么获得", "<p>光辉石由<strong>异彩化合物</strong>经过特定加工（充能/转化）得到，具体条件与「光」有关，属于终局内容。</p><p>它不是直接合成，而是要一套装置或环境。</p>"),
    ("怎么用", "<p>用途：<strong>光辉机壳</strong>、终局装饰、部分高级配方。发光、稀有，是后期建筑的亮点材料。</p><p>也能直接当光源方块摆放。</p>"),
    ("常见坑", "<p>第一坑：<strong>转化条件不对</strong>，异彩化合物一直不变。第二坑：产量极低，别规划大面积使用。</p><p>第三，和暗影钢是两条分支，材料不能互换。</p>"),
], params=[("类型", "终局材料"), ("特点", "发光"), ("来源", "异彩化合物转化")],
   related=["create:chromatic_compound", "create:refined_radiance_casing", "create:shadow_steel"])

item("create:creative_motor", "创造马达：测试用的无限动力", [
    ("怎么获得", "<p>创造马达只能在<strong>创造模式</strong>拿取，或由管理员给予，生存模式无法合成。它提供<strong>无限应力、可调转速</strong>的动力。</p><p>右键可以调节输出转速。</p>"),
    ("怎么用", "<p>用途：<strong>测试产线</strong>。造大型机器前，先用创造马达代替水车/蒸汽引擎，确认机器布局、齿轮比、方向都对，再换成真正的动力源。</p><p>也常用来做展示装置、跑图演示。</p>"),
    ("常见坑", "<p>第一坑：<strong>在生存里找配方</strong>，根本没有。第二坑：转速调太高，把测试机器烧坏/超载。</p><p>第三，创造马达不消耗应力，但下游机器该超载还是会超载。</p>"),
], params=[("类型", "创造专属"), ("输出", "无限应力 / 可调转速"), ("用途", "测试")],
   related=["create:hand_crank", "create:rotation_speed_controller", "create:stressometer"])

item("create:clutch", "离合器：说停就停", [
    ("怎么获得", "<p>离合器用<strong>安山机壳 + 传动轴</strong>一类材料合成，串在传动轴中间。给<strong>红石信号</strong>时断开动力，信号消失恢复传动。</p><p>它只控制「通/断」，不改变转速和方向。</p>"),
    ("怎么用", "<p>用途：<strong>分区停机</strong>。一条主轴上挂多台机器，用离合器分别控制，哪台不用就断开，省应力、也方便检修。</p><p>配合拉杆可以做「一键停线」，配合传感器可以做「卡料自动停机」。</p>"),
    ("常见坑", "<p>第一坑：<strong>和反转齿轮箱搞混</strong>，以为通电换向，其实通电是停。第二坑：红石信号常亮，机器一直不转，误判为动力不足。</p><p>第三，离合器断开后下游完全无动力，重启时注意顺序。</p>"),
], params=[("类型", "传动控制"), ("作用", "红石断通"), ("转速", "不变")],
   related=["create:gearshift", "create:gearbox", "create:analog_lever"])

item("create:elevator_pulley", "升降机滑轮：多层停靠", [
    ("怎么获得", "<p>升降机滑轮用<strong>安山机壳 + 绳索 + 黄铜件</strong>合成，装在高处，绳索末端挂平台。它比普通绳索滑轮多了<strong>楼层锚点</strong>功能。</p><p>需要旋转力驱动升降。</p>"),
    ("怎么用", "<p>用途：<strong>多层电梯</strong>。在每层放一个<strong>升降机锚点</strong>（Elevator Contact），右键锚点登记楼层，之后右键滑轮就能选层停靠。</p><p>到站会输出红石信号，可以联动站台门、指示灯。</p>"),
    ("常见坑", "<p>第一坑：<strong>锚点没登记</strong>，滑轮只会在顶底之间跑。第二坑：平台没粘牢，升降时散架。</p><p>第三，楼层高度要留够，平台会撞到中间方块。</p>"),
], params=[("类型", "动态结构"), ("输入", "旋转力"), ("功能", "多楼层停靠")],
   related=["create:elevator_contact", "create:rope_pulley", "create:super_glue"])

item("create:copper_backtank", "铜背罐：潜水与喷气", [
    ("怎么获得", "<p>铜背罐用<strong>铜板 + 玻璃 + 皮革</strong>一类材料合成，穿在胸甲位。它可以<strong>储存空气</strong>，让你在水下呼吸更久；装满压缩空气后还能当<strong>喷气背包</strong>用。</p><p>需要先用泵/注液器给它充气（压缩空气）。</p>"),
    ("怎么用", "<p>用途：<strong>水下作业与短途飞行</strong>。潜到水下建管道、修机器时，背罐提供额外氧气；右键/按键喷气可以短距离滑翔、跳高。</p><p>配合工程师护目镜，能看到更多机器信息。</p>"),
    ("常见坑", "<p>第一坑：<strong>没充气</strong>，背罐就是个铁壳。第二坑：喷气消耗快，飞一半掉进岩浆。</p><p>第三，背罐占胸甲位，和盔甲不能同时穿。</p>"),
], params=[("类型", "装备"), ("功能", "储气 / 喷气"), ("充能", "压缩空气")],
   related=["create:goggles", "create:netherite_backtank", "create:copper_diving_helmet"])

item("create:goggles", "工程师护目镜：看清机器的内心", [
    ("怎么获得", "<p>工程师护目镜用<strong>玻璃 + 皮革 + 黄铜件</strong>合成，戴在头盔位。戴上后看机器会显示<strong>转速、应力、配方进度</strong>等额外信息。</p><p>它不提供护甲，是纯信息装备。</p>"),
    ("怎么用", "<p>用途：<strong>调试产线</strong>。看一台机器缺什么料、转速够不够、应力占多少，不用猜。看传送带能显示物品流向，看工作盆能显示当前配方。</p><p>几乎是人手一副的必备装备。</p>"),
    ("常见坑", "<p>第一坑：<strong>忘了戴</strong>，然后凭感觉调机器。第二坑：戴着它当头盔用，实际没有防护。</p><p>第三，信息显示需要靠近并看向机器，太远看不到。</p>"),
], params=[("类型", "装备"), ("功能", "显示机器信息"), ("护甲", "无")],
   related=["create:copper_backtank", "create:speedometer", "create:stressometer"])

item("create:potato_cannon", "土豆加农炮：能打土豆的枪", [
    ("怎么获得", "<p>土豆加农炮用<strong>安山合金 + 铜件 + 火药</strong>一类材料合成，手持使用。左键/右键装填土豆（或其它可发射物），蓄力后发射。</p><p>它能发射土豆、胡萝卜等农作物，也能装填特殊弹种。</p>"),
    ("怎么用", "<p>用途：<strong>远程攻击与娱乐</strong>。打怪、打远处的按钮、把作物射进漏斗里（真的可以）。</p><p>蓄力越久射得越远，弹道有下坠。</p>"),
    ("常见坑", "<p>第一坑：<strong>没装弹</strong>，空枪打不出去。第二坑：把它当正经武器，伤害其实一般。</p><p>第三，弹道下坠明显，远距离要抬枪。</p>"),
], params=[("类型", "武器"), ("弹药", "土豆 / 农作物"), ("特点", "蓄力抛射")],
   related=["create:copper_backtank", "create:extendo_grip", "create:potato_cannon"])
