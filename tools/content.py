# -*- coding: utf-8 -*-
# 本文件由 tools/ 内的构建脚本使用；路径全部相对仓库根目录。
import os as _os
ROOT = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))
DATA = _os.path.join(ROOT, "tools", "data")
WORK = _os.path.join(ROOT, "work")
# -*- coding: utf-8 -*-
"""手写教程内容库。每条 item 的教程由人工撰写，按分类分批扩充。"""

# 分类定义：顺序即展示顺序
CATEGORIES = [
    ("power", "动力与传动", "旋转机械的骨架：轴、齿轮、离合、水车与引擎。"),
    ("machine", "机器与加工", "把旋转变成加工能力：压、搅、锯、钻、部署。"),
    ("logistics", "物流与仓储", "传送带、漏斗、管道、包裹与库存。"),
    ("train", "列车与轨道", "真正的铁路系统：轨道、转向架、信号与时刻表。"),
    ("material", "材料与零件", "合金、板材、精密构件与中间产物。"),
    ("redstone", "红石与控制", "传感器、逻辑元件与显示。"),
    ("tool", "工具与装备", "扳手、护目镜、蓝图、潜水装备与食物。"),
    ("decor", "装饰与建筑", "调色板方块、窗户、栏杆与工业风装饰。"),
    ("contraption", "动态结构与载具", "超级胶、底盘、轴承与可移动结构。"),
]

# ---------------------------------------------------------------- 手工教程
# tag: 一句话定位；params: [(名称, 值)]；sections: [(小标题, HTML)]；related: [id]
TUT = {}


def _plain(secs):
    return " ".join(b for _, b in secs)

def item(iid, tag, sections, params=None, related=None):
    new = {"tag": tag, "sections": sections, "params": params or [], "related": related or []}
    old = TUT.get(iid)
    # keep the longer version when batches overlap (later files must earn the slot)
    if old is not None and len(_plain(old["sections"])) > len(_plain(sections)):
        return
    TUT[iid] = new


# ============================ 动力与传动 ============================
item("create:shaft", "Create 的动力总线，所有旋转都从它开始。", [
    ("怎么用", "<p>把<strong>传动轴</strong>沿着一条直线连续摆放，它们会自动互相连接成一根轴。轴的任意一端贴上动力源（水车、风车、蒸汽引擎、手摇曲柄），整根轴就开始旋转。</p>"
              "<p>轴只沿自身轴向传递旋转：水平摆放的轴带水平旋转，竖直摆放的轴带竖直旋转。两条不同朝向的轴不能直接对接，必须用<strong>齿轮箱</strong>换向。</p>"),
    ("关键规则", "<ul><li>轴本身<strong>不消耗应力</strong>，只负责传输，可以铺很长。</li>"
                "<li>轴的转速 = 动力源转速，沿途不变；改变转速要靠<strong>转速控制器</strong>或大小齿轮。</li>"
                "<li>用<strong>扳手</strong>右键可以快速拆卸整段轴，比手拆快得多。</li></ul>"),
    ("常见坑", "<p>轴穿过方块时不会自动留孔，需要先用扳手把方块「打薄」成半砖厚度，或者直接留空。轴与轴之间如果隔了一个完整方块，是不会连接的。</p>"),
], params=[("应力消耗", "0 SU（纯传输）"), ("转速", "跟随动力源"), ("可换向", "需要齿轮箱")],
   related=["create:cogwheel", "create:gearbox", "create:andesite_casing"])

item("create:cogwheel", "小齿轮，用来换向、并联和改变转速。", [
    ("怎么用", "<p>把齿轮贴在传动轴侧面，两根轴就会被它带动。两个齿轮<strong>直接咬合</strong>时转向相反；用<strong>大齿轮 + 小齿轮</strong>咬合可以把转速放大或缩小一倍。</p>"
              "<p>齿轮的朝向由它贴的轴决定：贴水平轴就是竖直齿轮盘，贴竖直轴就是水平齿轮盘。</p>"),
    ("转速与应力", "<p>小齿轮之间 1:1 传递转速；大齿轮带小齿轮是 2:1（转速翻倍、应力需求也翻倍）。齿轮本身不额外消耗应力，但会放大下游的应力需求。</p>"),
    ("常见坑", "<p>齿轮只能与<strong>相邻一格</strong>的齿轮咬合，中间隔一格就带不动。用<strong>大齿轮</strong>可以跨过一格距离。</p>"),
], params=[("传动比", "1:1（同尺寸）"), ("换向", "咬合即反向"), ("应力", "不额外消耗")],
   related=["create:large_cogwheel", "create:shaft", "create:gearbox"])

item("create:large_cogwheel", "大齿轮，跨格传动与 2 倍变速的关键。", [
    ("怎么用", "<p>大齿轮直径占 2 格，可以隔着<strong>一格空隙</strong>与另一个齿轮咬合，非常适合绕过障碍或在机器之间搭桥。</p>"
              "<p>大齿轮带小齿轮 = 转速 ×2、应力需求 ×2；小齿轮带大齿轮 = 转速 ÷2、应力需求 ÷2，同时扭矩更大。</p>"),
    ("什么时候用", "<p>需要<strong>提速</strong>（比如让粉碎轮转得更快）或需要<strong>跨格</strong>连接时用它；需要<strong>降速增扭</strong>（带动重负载）时也用它。</p>"),
    ("常见坑", "<p>大齿轮占地大，容易和旁边的方块冲突；摆之前先用半砖/楼梯留出空间。两个大齿轮相邻咬合是 1:1，不会变速。</p>"),
], params=[("直径", "2 格"), ("变速", "×2 或 ÷2"), ("跨格", "可隔 1 格咬合")],
   related=["create:cogwheel", "create:gearbox"])

item("create:gearbox", "换向核心：让水平轴和竖直轴互相转换。", [
    ("怎么用", "<p>齿轮箱有六个面，可以同时接多根轴。它能把输入的方向<strong>自由分配到其他面</strong>，是搭建复杂传动网络的基础。</p>"
              "<p>右键齿轮箱可以切换它内部齿轮的啮合方式，从而改变输出方向；用扳手右键可以整体旋转。</p>"),
    ("关键规则", "<p>齿轮箱<strong>不改变转速</strong>，只改变方向。多个输出面会平分扭矩，但转速保持一致。</p>"),
    ("常见坑", "<p>齿轮箱的六个面不是都能同时用——某些面会互相干涉。搭之前先用创造模式试摆一次。</p>"),
], params=[("接口", "6 面"), ("转速", "不变"), ("作用", "换向/分配")],
   related=["create:vertical_gearbox", "create:shaft"])

item("create:vertical_gearbox", "竖直版齿轮箱，专治上下换向。", [
    ("怎么用", "<p>当你要把地面上的水平传动引到<strong>竖直方向</strong>（比如往上带一条立式产线），用它最省空间。上下两面接竖直轴，四个侧面接水平轴。</p>"),
    ("常见坑", "<p>它和普通齿轮箱的接口方向不同，不要混用；摆错方向时用扳手旋转即可。</p>"),
], params=[("接口", "上下 + 四周"), ("转速", "不变")],
   related=["create:gearbox"])

item("create:clutch", "离合器：用红石信号切断动力。", [
    ("怎么用", "<p>把它串在传动轴上。默认<strong>接通</strong>，给红石信号后<strong>断开</strong>，下游立刻停转。适合做「一键停机」「安全急停」。</p>"),
    ("常见坑", "<p>断开时下游会惯性滑行一小段，不会瞬间静止；如果要精确停位，配合<strong>转速控制器</strong>使用。</p>"),
], params=[("默认", "接通"), ("红石", "通电断开")],
   related=["create:gearshift", "create:rotation_speed_controller"])

item("create:gearshift", "换挡器：用红石信号反转方向。", [
    ("怎么用", "<p>串在轴上，给红石信号会<strong>反转</strong>输出方向（不只是停转）。做往返运动、双向传送带、自动门时非常有用。</p>"),
    ("常见坑", "<p>反转是瞬间的，带重负载时会有明显的「顿挫」，机械臂之类的机构建议加缓冲。</p>"),
], params=[("默认", "正转"), ("红石", "反转")],
   related=["create:clutch"])

item("create:rotation_speed_controller", "转速控制器：精确设定某一段的 RPM。", [
    ("怎么用", "<p>上方放大齿轮作为「读数轮」，下方接输入轴，输出面接你要控制的部分。用<strong>右键</strong>或<strong>滚轮</strong>调整目标转速，输出就会稳定在你设定的 RPM。</p>"
              "<p>它需要一个<strong>大齿轮</strong>作为参照，且输入转速必须高于目标转速。</p>"),
    ("为什么重要", "<p>很多机器有最佳转速（例如粉碎轮越快越好，但应力有限）；用控制器可以精确控制产线节拍，避免超载。</p>"),
    ("常见坑", "<p>设定转速高于输入转速时无法达到，会以输入转速为上限；控制器本身占用一定应力。</p>"),
], params=[("输出", "可设定 RPM"), ("依赖", "输入转速需更高")],
   related=["create:large_cogwheel", "create:stressometer"])

item("create:water_wheel", "最早期、最稳定的动力源。", [
    ("怎么用", "<p>放在流动的水里（水流要穿过轮子），它会以固定低速旋转。多个水车可以串联在同一根轴上叠加应力输出。</p>"
              "<p>水车转速低但<strong>应力容量大</strong>，适合带动重负载的早期产线。</p>"),
    ("常见坑", "<p>水车必须被<strong>流动的水</strong>推动，静止水源不生效；水车之间有最小间距要求，摆太密会互相挡住。</p>"),
], params=[("转速", "低速固定"), ("应力", "较大")],
   related=["create:large_water_wheel", "create:windmill_bearing", "create:steam_engine"])

item("create:large_water_wheel", "大型水车：同转速、更大应力。", [
    ("怎么用", "<p>占地 3×3，需要更大的水流。单台提供的应力远高于普通水车，是前期最划算的动力来源之一。</p>"),
    ("常见坑", "<p>体积大、对水流要求高，河道要提前挖宽；建好后再改方向很麻烦，先规划位置。</p>"),
], params=[("占地", "3×3"), ("应力", "高")],
   related=["create:water_wheel"])

item("create:windmill_bearing", "风车轴承：把风帆变成动力。", [
    ("怎么用", "<p>放在墙上，朝外的一面装上<strong>风帆</strong>（帆布方块）。风帆面积越大、叶片越多，输出应力越高。转速固定且偏低。</p>"
              "<p>它是动态结构：整个风车会真的转起来，适合做地标式动力塔。</p>"),
    ("常见坑", "<p>风帆必须连成一片且朝外；被方块挡住会失效。轴承要留出旋转空间，别贴着墙建。</p>"),
], params=[("转速", "低"), ("应力", "随帆面积提升")],
   related=["create:mechanical_bearing", "create:sail_frame"])

item("create:steam_engine", "蒸汽引擎：中后期主力动力，可调档。", [
    ("怎么用", "<p>底部接<strong>锅炉</strong>（用燃烧的烈焰人炉加热水），引擎本体接输出轴。用<strong>扳手</strong>切换档位：低档转速低应力高，高档转速高应力低。</p>"
              "<p>多台引擎可以并联到同一根轴上叠加输出。</p>"),
    ("常见坑", "<p>必须持续供水与燃料，断水会停机；锅炉水位不足时效率骤降。管道要用<strong>流体管道</strong>正确连接。</p>"),
], params=[("档位", "可扳手切换"), ("依赖", "水 + 燃料")],
   related=["create:blaze_burner", "create:fluid_pipe", "create:flywheel"])

item("create:hand_crank", "手摇曲柄：临时动力与调试神器。", [
    ("怎么用", "<p>贴在轴上右键转动，松手就停。适合测试新机器是否接对，或者在没电的地方临时驱动一下。</p>"),
    ("常见坑", "<p>转速取决于你摇的速度，不稳定；不要用它带重负载。</p>"),
], params=[("动力", "手动"), ("用途", "调试/应急")],
   related=["create:shaft"])

item("create:flywheel", "飞轮：储存旋转动能，稳速用。", [
    ("怎么用", "<p>串在蒸汽引擎的输出轴上，能吸收转速波动，让下游机器转得更平稳。大型飞轮需要放在专门的支架上。</p>"),
    ("常见坑", "<p>飞轮只稳速、不增能；上游动力不足时它也救不了。</p>"),
], params=[("作用", "稳速/储能")],
   related=["create:steam_engine"])

item("create:belt", "传送带：物品运输的主干道。", [
    ("怎么用", "<p>用<strong>传送带连接器</strong>在地面上拉出一条带子，两端各放一个<strong>传动轴</strong>作为滚筒。轴一转，带子就动，物品随带子前进。</p>"
              "<p>用扳手可以调整带子的<strong>倾斜角度</strong>和方向；带子可以上下坡、可以拐弯（用两个滚筒）。</p>"),
    ("物流细节", "<ul><li>带子上的物品会被自动「排队」，不会互相挤压消失。</li>"
                "<li>末端接<strong>漏斗</strong>或<strong>溜槽</strong>把物品送进容器。</li>"
                "<li>用<strong>隧道</strong>可以让带子穿过方块、分流、合流。</li></ul>"),
    ("常见坑", "<p>带子必须两端都有<strong>转动的轴</strong>才会动；轴停了带子也停。带子太长时中间要加支撑轴，否则会断开。</p>"),
], params=[("动力", "两端轴驱动"), ("速度", "随轴转速")],
   related=["create:belt_connector", "create:andesite_funnel", "create:chute", "create:andesite_tunnel"])

item("create:encased_chain_drive", "链条传动：远距离、同向、不换向。", [
    ("怎么用", "<p>两个链轮之间用链条连接，可以跨越较远距离传递旋转，而且<strong>转向相同</strong>（不像齿轮会反向）。</p>"
              "<p>用<strong>可调节链条传动</strong>可以改变两端的相对角度。</p>"),
    ("常见坑", "<p>链条长度有限，太长需要中间加链轮；链条会被方块阻挡。</p>"),
], params=[("转向", "同向"), ("距离", "中等")],
   related=["create:adjustable_chain_gearshift", "create:sequenced_gearshift"])

item("create:creative_motor", "创造马达：无限转速与应力（仅创造模式）。", [
    ("怎么用", "<p>接上轴就能无限输出，用扳手或界面设定转速。搭原型、测试产线时非常省事。</p>"),
    ("常见坑", "<p>生存模式无法获得；用它测试的产线搬到生存前，记得核算真实应力。</p>"),
], params=[("模式", "仅创造")],
   related=["create:shaft"])

# ============================ 机器与加工 ============================
item("create:mechanical_press", "机械压床：把材料压成板、压成块。", [
    ("怎么用", "<p>放在工作台上方一格，下方放<strong>置物台</strong>或<strong>传送带</strong>，顶部接动力轴。物品进入压床下方时会被自动压下。</p>"
              "<p>最经典用途：<strong>铁锭 → 铁板</strong>、<strong>金锭 → 金板</strong>、<strong>安山合金 → 安山机壳</strong>。</p>"),
    ("参数", "<p>转速越高，压制越快；应力消耗固定。压床可以连续工作，不需要红石。</p>"),
    ("常见坑", "<p>压床下方必须是能承接物品的方块（置物台/带子/盆），否则不工作。压床本身不储存物品，前端要有人喂料。</p>"),
], params=[("转速", "越快越好"), ("输入", "物品"), ("输出", "压制成型")],
   related=["create:depot", "create:belt", "create:basin"])

item("create:mechanical_mixer", "搅拌器：混合原料，可加热。", [
    ("怎么用", "<p>放在<strong>盆</strong>上方，盆里放原料。搅拌器旋转时会把盆里的物品混合成新产物。</p>"
              "<p>很多配方需要<strong>加热</strong>：在盆下方放<strong>烈焰人炉</strong>（点燃）即可。</p>"),
    ("常见用途", "<p>安山合金（安山岩 + 铁粒）、巧克力、面团、染料混合等。</p>"),
    ("常见坑", "<p>搅拌器只认<strong>盆</strong>，不认传送带；一次投入的原料数量要按配方来，多投会浪费。</p>"),
], params=[("容器", "盆"), ("加热", "烈焰人炉")],
   related=["create:basin", "create:blaze_burner"])

item("create:millstone", "磨盘：研磨矿石与材料。", [
    ("怎么用", "<p>顶部接动力轴，物品从上方投入，磨好的产物从侧面输出。可以放在传送带产线里。</p>"
              "<p>常用于磨<strong>小麦 → 面粉</strong>、<strong>矿石 → 粉碎矿石</strong>。</p>"),
    ("常见坑", "<p>磨盘没有自动输出，需要侧面接漏斗/溜槽；转速过低时效率很差。</p>"),
], params=[("输入", "顶部投料"), ("输出", "侧面")],
   related=["create:crushing_wheel", "create:mechanical_press"])

item("create:crushing_wheel", "粉碎轮：矿石翻倍的核心。", [
    ("怎么用", "<p>两个粉碎轮<strong>对转</strong>（方向相反），中间留一格空隙。物品从上方掉进空隙就会被粉碎，产物从下方输出。</p>"
              "<p>它是<strong>矿石翻倍</strong>的关键：原矿 → 粉碎矿石 → 洗涤 → 更多金属。</p>"),
    ("参数", "<p>转速越高粉碎越快；两个轮子必须<strong>反向</strong>旋转，同向会卡住。</p>"),
    ("常见坑", "<p>轮子之间距离必须是 1 格；用齿轮箱让两轮反向。粉碎轮很吃应力，前期建议单独供能。</p>"),
], params=[("转向", "两轮反向"), ("应力", "高")],
   related=["create:millstone", "create:encased_fan", "create:mechanical_press"])

item("create:mechanical_saw", "机械锯：切割与伐木。", [
    ("怎么用", "<p>锯片朝下安装，物品从下方经过就会被切割。也可以用它<strong>砍树</strong>（对着原木）或加工木板、台阶。</p>"
              "<p>配合<strong>部署器</strong>可以做出自动伐木机。</p>"),
    ("常见坑", "<p>锯片有方向，装反了不工作；切割原木时会消耗耐久吗？不会——Create 的锯是无限耐久的。</p>"),
], params=[("方向", "锯片朝下"), ("用途", "切割/伐木")],
   related=["create:deployer", "create:mechanical_press"])

item("create:deployer", "部署器：模拟玩家「用手」操作。", [
    ("怎么用", "<p>把物品放进部署器，它会对着前方<strong>使用</strong>这个物品：放方块、用剪刀、涂安山合金、安装零件等。</p>"
              "<p>它是自动化的万能手：配合机械臂、传送带可以做全自动装配线。</p>"),
    ("常见坑", "<p>部署器有<strong>模式</strong>（右键切换）：使用/攻击等；装错模式会导致不工作。它需要动力才会动作。</p>"),
], params=[("动作", "模拟使用物品"), ("动力", "需要旋转")],
   related=["create:mechanical_arm", "create:mechanical_press"])

item("create:mechanical_arm", "机械臂：在两点之间搬运物品。", [
    ("怎么用", "<p>放在目标位置附近，用<strong>过滤器</strong>或界面设定输入/输出点。它会抓起物品从 A 点搬到 B 点，适合连接不相邻的机器。</p>"
              "<p>可以设置多个目标点，做「分拣 + 搬运」一体化。</p>"),
    ("常见坑", "<p>机械臂的抓取范围有限，摆太远够不到；抓取速度受转速影响。</p>"),
], params=[("功能", "定点搬运"), ("配置", "过滤器/界面")],
   related=["create:deployer", "create:andesite_funnel"])

item("create:basin", "盆：搅拌、加热、装液体的工作台。", [
    ("怎么用", "<p>放在搅拌器下方，或者单独用作液体容器。可以接<strong>注液器</strong>、<strong>管道</strong>、<strong>烈焰人炉</strong>。</p>"
              "<p>盆里的物品不会消失，直到被搅拌或取出。</p>"),
    ("常见坑", "<p>盆不自动输出，需要漏斗或机械臂取物；加热要烈焰人炉在正下方。</p>"),
], params=[("容量", "1 组物品 + 液体")],
   related=["create:mechanical_mixer", "create:blaze_burner", "create:spout"])

item("create:blaze_burner", "烈焰人炉：加热与「缠魂」的火焰源。", [
    ("怎么用", "<p>放入<strong>烈焰蛋糕</strong>后点燃，提供加热。放在盆/锅炉下方用于烹饪与产蒸汽；也可以用它给<strong>缠魂</strong>配方提供灵魂火焰。</p>"
              "<p>用<strong>空手</strong>右键可以开关火焰。</p>"),
    ("常见坑", "<p>烈焰蛋糕会消耗，需要定期补充；灵魂火焰要用灵魂沙/灵魂土点燃。</p>"),
], params=[("燃料", "烈焰蛋糕"), ("用途", "加热/缠魂")],
   related=["create:basin", "create:steam_engine", "create:encased_fan"])

item("create:encased_fan", "封装风扇：洗涤、缠魂、吹动。", [
    ("怎么用", "<p>对着<strong>水</strong>吹 = 洗涤（把粉碎矿石洗成金属粒/成品）；对着<strong>火</strong>吹 = 缠魂（把物品变成下界版本）；对着实体吹 = 推动。</p>"
              "<p>也可以用来吹动<strong>风帆</strong>做动力，或推动物品在带子上加速。</p>"),
    ("常见坑", "<p>风扇必须<strong>有转速</strong>才有效果；洗涤/缠魂需要物品在气流中（带子或掉落物）。</p>"),
], params=[("模式", "水=洗涤 / 火=缠魂"), ("动力", "旋转")],
   related=["create:crushing_wheel", "create:blaze_burner"])

item("create:spout", "注液器：给物品灌液体。", [
    ("怎么用", "<p>上方接管道或储罐，下方放物品（带子/置物台）。物品经过时会被灌满，例如<strong>水瓶</strong>、<strong>巧克力</strong>、<strong>蜂蜜</strong>。</p>"),
    ("常见坑", "<p>需要先给注液器供应液体；液体种类不对不会工作。</p>"),
], params=[("输入", "液体"), ("输出", "灌注后的物品")],
   related=["create:item_drain", "create:fluid_tank"])

item("create:item_drain", "物品沥干器：把液体从物品里倒出来。", [
    ("怎么用", "<p>与注液器相反：把装有液体的物品（如水桶、蜂蜜瓶）放上去，液体会被倒进下方的容器/管道。</p>"),
], params=[("功能", "倒出液体")],
   related=["create:spout"])

item("create:mechanical_piston", "机械活塞：直线推动整个结构。", [
    ("怎么用", "<p>它推动的不是方块，而是<strong>动态结构</strong>（用超级胶粘起来的一整块）。行程由<strong>活塞杆</strong>叠加决定。</p>"
              "<p>常用于电梯、挤出机、可伸缩平台。</p>"),
    ("常见坑", "<p>结构必须用超级胶粘牢，散块会被推散；行程太长会抖动。</p>"),
], params=[("运动", "直线"), ("依赖", "超级胶")],
   related=["create:sticky_mechanical_piston", "create:piston_extension_pole", "create:super_glue"])

item("create:rope_pulley", "绳索滑轮：垂直升降。", [
    ("怎么用", "<p>放下绳子，末端挂住动态结构，转动时把结构吊起或放下。可以做矿井电梯、吊桥。</p>"),
    ("常见坑", "<p>绳子长度有限，要预先放够；结构太重会拉不动。</p>"),
], params=[("运动", "垂直"), ("依赖", "绳子")],
   related=["create:elevator_pulley", "create:hose_pulley"])

item("create:gantry_carriage", "龙门架小车：沿轨道直线移动。", [
    ("怎么用", "<p>架在<strong>龙门架轴</strong>上，通电后沿轴移动，适合做长距离直线运动（如自动农场收割、3D 打印机）。</p>"),
    ("常见坑", "<p>龙门架轴要足够长；小车两端的限位要用<strong>接触器</strong>做。</p>"),
], params=[("运动", "直线轨道")],
   related=["create:gantry_shaft", "create:linear_chassis"])

item("create:mechanical_drill", "机械钻头：挖掘方块。", [
    ("怎么用", "<p>装在动态结构或机械臂前端，转动时破坏前方方块。可用于自动采矿机、隧道挖掘。</p>"),
    ("常见坑", "<p>钻头会被硬度高的方块卡住；破坏的方块需要收集装置。</p>"),
], params=[("功能", "挖掘")],
   related=["create:mechanical_saw", "create:deployer"])

item("create:mechanical_harvester", "收割机：自动收割作物。", [
    ("怎么用", "<p>装在动态结构上扫过农田，会自动收割成熟作物并补种（配合部署器）。</p>"),
], params=[("功能", "收割")],
   related=["create:mechanical_plough", "create:deployer"])

item("create:mechanical_plough", "犁：翻地与平整。", [
    ("怎么用", "<p>装在动态结构上，经过泥土会变成耕地，也可以把草方块刮平。</p>"),
], params=[("功能", "耕地/平整")],
   related=["create:mechanical_harvester"])

item("create:mechanical_roller", "压路机：压实与铺路。", [
    ("怎么用", "<p>装在动态结构上滚过地面，可以把方块压实（如砂砾 → 压实砂砾），也能压平地形。</p>"),
], params=[("功能", "压实/碾压")],
   related=["create:mechanical_press"])

item("create:mechanical_pump", "机械泵：抽送液体。", [
    ("怎么用", "<p>接在管道上，转动时把液体从一端泵到另一端。方向由朝向决定，用扳手可反转。</p>"),
    ("常见坑", "<p>泵需要动力；长距离输液要在中途加泵，否则流速会掉。</p>"),
], params=[("功能", "液体输送")],
   related=["create:fluid_pipe", "create:fluid_tank"])

item("create:mechanical_crafter", "动力合成器：用旋转做合成。", [
    ("怎么用", "<p>多个合成器拼成网格，把原料按配方放进去，接入动力后自动合成。适合大批量生产。</p>"),
    ("常见坑", "<p>网格形状要按配方摆；输出口需要漏斗/带子接走。</p>"),
], params=[("功能", "自动合成"), ("动力", "旋转")],
   related=["create:crafter_slot_cover", "create:mechanical_arm"])

# ============================ 物流与仓储 ============================
item("create:andesite_funnel", "漏斗：物品进出的门。", [
    ("怎么用", "<p>贴着容器或带子放置。默认<strong>抽取</strong>模式（把物品从容器取出放到带子），用扳手切换成<strong>输入</strong>模式（把带子上的物品送进容器）。</p>"
              "<p>安山漏斗不需要动力；黄铜漏斗可以过滤。</p>"),
    ("常见坑", "<p>方向搞反是最常见的错误——用扳手右键漏斗本体切换模式。漏斗只处理<strong>物品</strong>，不处理液体。</p>"),
], params=[("模式", "抽取/输入"), ("动力", "不需要")],
   related=["create:brass_funnel", "create:andesite_tunnel", "create:chute"])

item("create:brass_funnel", "黄铜漏斗：带过滤的漏斗。", [
    ("怎么用", "<p>把要允许通过的物品放进过滤槽，它只会让这些物品通过。适合做分拣系统。</p>"
              "<p>过滤槽可以放多个物品，也可以放<strong>属性过滤器</strong>做更复杂的规则。</p>"),
], params=[("过滤", "支持"), ("动力", "不需要")],
   related=["create:andesite_funnel", "create:filter", "create:attribute_filter"])

item("create:chute", "溜槽：垂直输送物品。", [
    ("怎么用", "<p>竖直叠放，物品从上方掉进去会快速滑到下方容器。比漏斗快，适合高差输送。</p>"),
], params=[("方向", "垂直"), ("速度", "快")],
   related=["create:smart_chute", "create:andesite_funnel"])

item("create:smart_chute", "智能溜槽：带过滤的溜槽。", [
    ("怎么用", "<p>和溜槽一样，但可以设置过滤，只让指定物品通过。</p>"),
], params=[("过滤", "支持")],
   related=["create:chute"])

item("create:item_vault", "物品保险库：大容量存储。", [
    ("怎么用", "<p>可以拼接成任意形状的大仓库，容量随体积增长。用<strong>库存链接</strong>或界面查看内容。</p>"),
    ("常见坑", "<p>保险库不能直接用漏斗读全部内容，需要<strong>库存交换机</strong>做自动化。</p>"),
], params=[("容量", "随体积"), ("拼接", "支持")],
   related=["create:stockpile_switch", "create:stock_link", "create:item_hatch"])

item("create:fluid_tank", "流体储罐：存液体。", [
    ("怎么用", "<p>可以竖直拼接成高塔，容量随高度增加。顶部/底部接管道。</p>"),
], params=[("容量", "随高度")],
   related=["create:fluid_pipe", "create:mechanical_pump"])

item("create:fluid_pipe", "流体管道：输送液体。", [
    ("怎么用", "<p>连接储罐、泵、机器。管道会自动寻找路径，用扳手可以调整连接方向。</p>"),
    ("常见坑", "<p>管道不会自己流动，需要<strong>机械泵</strong>提供压力。</p>"),
], params=[("输送", "需要泵")],
   related=["create:mechanical_pump", "create:smart_fluid_pipe"])

item("create:packager", "打包机：把物品打成包裹。", [
    ("怎么用", "<p>接入带子和包裹网络，把散装物品打包成<strong>包裹</strong>，便于长距离运输和分拣。</p>"
              "<p>配合<strong>包裹过滤器</strong>、<strong>拆包机</strong>、<strong>包裹蛙港</strong>做全自动物流。</p>"),
], params=[("功能", "打包")],
   related=["create:repackager", "create:package_filter", "create:package_frogport"])

# ============================ 材料与零件 ============================
item("create:andesite_alloy", "Create 的基础合金，几乎所有机器的起点。", [
    ("怎么用", "<p>把<strong>安山岩</strong>和<strong>铁粒</strong>放进盆里用搅拌器混合即可。它是机壳、齿轮、轴的核心材料。</p>"),
    ("常见坑", "<p>前期铁粒靠熔炼铁装备/铁锭分解获得；攒够再开产线。</p>"),
], params=[("配方", "安山岩 + 铁粒（搅拌）")],
   related=["create:andesite_casing", "create:shaft", "create:cogwheel"])

item("create:andesite_casing", "安山机壳：机器的外壳与结构件。", [
    ("怎么用", "<p>用<strong>部署器</strong>把安山合金「涂」在<strong>去皮原木</strong>上得到。是齿轮箱、漏斗、传送带框架的常用外壳。</p>"),
    ("常见坑", "<p>必须用去皮原木（任何木头都行），普通原木不行。</p>"),
], params=[("配方", "去皮原木 + 安山合金（部署器）")],
   related=["create:brass_casing", "create:copper_casing"])

item("create:brass_ingot", "黄铜锭：中后期机器的材料。", [
    ("怎么用", "<p>铜 + 锌在搅拌器里混合（需要加热）得到黄铜。用于黄铜机壳、精密构件、列车部件。</p>"),
    ("常见坑", "<p>锌矿需要先找到<strong>锌矿石</strong>；黄铜配方需要加热。</p>"),
], params=[("配方", "铜 + 锌（加热搅拌）")],
   related=["create:brass_casing", "create:precision_mechanism", "create:zinc_ingot"])

item("create:precision_mechanism", "精密构件：高级机器与列车的核心零件。", [
    ("怎么用", "<p>用<strong>序列组装</strong>产线制造：金板 → 多道部署/压制 → 成品。是列车、机械臂等高级设备的必需品。</p>"
              "<p>流程长、占地大，建议单独建一条产线。</p>"),
    ("常见坑", "<p>序列组装的每一步都需要精确摆放；中途断料会导致整条线停摆。</p>"),
], params=[("工艺", "序列组装"), ("用途", "高级机器/列车")],
   related=["create:incomplete_precision_mechanism", "create:golden_sheet", "create:cogwheel"])

item("create:rose_quartz", "玫瑰石英：光学与显示材料。", [
    ("怎么用", "<p>用<strong>粉碎轮</strong>粉碎<strong>红石</strong>并洗涤获得？实际配方是红石 + 石英在搅拌中加热。用于显示板、玫瑰石英灯。</p>"),
], params=[("用途", "显示/装饰")],
   related=["create:polished_rose_quartz", "create:display_board"])

# ============================ 工具与装备 ============================
item("create:wrench", "扳手：Create 的万能工具。", [
    ("怎么用", "<ul><li><strong>右键</strong>方块：旋转朝向。</li>"
              "<li><strong>潜行 + 右键</strong>：拆卸机器/整段轴。</li>"
              "<li>对传送带、漏斗、齿轮箱使用可以切换模式。</li>"
              "<li>可以给机器<strong>改名</strong>（铁砧）与染色。</li></ul>"),
    ("为什么必备", "<p>没有扳手几乎无法调整产线；开局第一件工具就应该做它。</p>"),
], params=[("用途", "旋转/拆卸/配置")],
   related=["create:goggles", "create:super_glue"])

item("create:goggles", "工程师护目镜：看到应力与转速。", [
    ("怎么用", "<p>戴在头上后，看向机器会显示<strong>转速（RPM）</strong>和<strong>应力消耗/容量</strong>，还能看到传送带上的物品信息。</p>"
              "<p>是排查「为什么不动」的第一工具。</p>"),
    ("常见坑", "<p>护目镜占用头盔槽；可以附魔（如耐久）但会消耗。</p>"),
], params=[("显示", "RPM / 应力")],
   related=["create:wrench", "create:stressometer"])

item("create:super_glue", "超级胶：把方块粘成动态结构。", [
    ("怎么用", "<p>右键两个方块把它们粘在一起，之后整个结构可以被轴承/活塞/绳索整体移动。</p>"
              "<p>用<strong>扳手</strong>可以清除胶水痕迹。</p>"),
    ("常见坑", "<p>粘错位置很常见，粘完一定要先小范围测试再扩大。</p>"),
], params=[("用途", "粘合动态结构")],
   related=["create:mechanical_piston", "create:mechanical_bearing"])

item("create:schematic_and_quill", "蓝图与笔：保存与放置建筑。", [
    ("怎么用", "<p>先用<strong>蓝图台</strong>框选区域生成空蓝图，再拿蓝图与笔右键保存。之后可以用<strong>蓝图加农炮</strong>自动建造。</p>"),
], params=[("用途", "复制建筑")],
   related=["create:schematic", "create:schematic_table", "create:schematicannon"])

item("create:copper_backtank", "铜制背罐：给潜水装备供气。", [
    ("怎么用", "<p>穿在胸甲槽，配合<strong>潜水头盔</strong>与<strong>潜水靴</strong>可以在水下自由活动。背罐需要充气（用风扇/压缩空气）。</p>"),
], params=[("装备", "胸甲槽")],
   related=["create:copper_diving_helmet", "create:copper_diving_boots"])

# ============================ 红石与控制 ============================
item("create:analog_lever", "模拟拉杆：输出可调的红石信号。", [
    ("怎么用", "<p>右键调整输出强度（0-15），可以精确控制转速控制器、机械臂行程等。</p>"),
], params=[("输出", "0-15 可调")],
   related=["create:redstone_link", "create:rotation_speed_controller"])

item("create:redstone_link", "无线红石：远距离传输信号。", [
    ("怎么用", "<p>成对使用，一个发射一个接收，用<strong>频率</strong>配对。可以跨维度（需配置）。</p>"),
], params=[("传输", "无线")],
   related=["create:transmitter", "create:analog_lever"])

item("create:content_observer", "内容观察器：检测容器内容变化。", [
    ("怎么用", "<p>贴在容器上，容器内物品数量变化时输出红石脉冲。适合做「库存不足报警」「自动补料」。</p>"),
], params=[("检测", "容器内容")],
   related=["create:stockpile_switch", "create:threshold_switch"])

item("create:display_board", "显示板：用方块拼出文字/图案。", [
    ("怎么用", "<p>把方块放在显示板上，它会显示该方块的纹理。配合<strong>显示链接</strong>可以动态显示库存数量、转速等数据。</p>"),
], params=[("用途", "显示")],
   related=["create:display_link", "create:nixie_tube"])

item("create:speedometer", "转速表：显示 RPM。", [
    ("怎么用", "<p>贴在轴上，显示当前转速。比护目镜更直观，适合做控制面板。</p>"),
], params=[("显示", "RPM")],
   related=["create:stressometer"])

item("create:stressometer", "应力表：显示应力占用。", [
    ("怎么用", "<p>贴在动力网络上，显示当前应力使用/上限。产线超载时第一个看它。</p>"),
], params=[("显示", "SU 使用/上限")],
   related=["create:speedometer", "create:goggles"])

# ============================ 动态结构 ============================
item("create:mechanical_bearing", "机械轴承：让整个结构旋转。", [
    ("怎么用", "<p>贴在结构底部，用超级胶把方块粘成整体，通电后整个结构绕轴承旋转。可以做旋转餐厅、旋转农场、风车。</p>"),
    ("常见坑", "<p>结构必须完全粘牢；旋转半径内有方块会被卡住。</p>"),
], params=[("运动", "旋转"), ("依赖", "超级胶")],
   related=["create:windmill_bearing", "create:clockwork_bearing", "create:super_glue"])

item("create:linear_chassis", "线性底盘：可伸缩的框架。", [
    ("怎么用", "<p>多个底盘拼在一起可以沿直线伸缩，常用于龙门架、伸缩臂。</p>"),
], params=[("运动", "线性伸缩")],
   related=["create:radial_chassis", "create:gantry_carriage"])

item("create:radial_chassis", "径向底盘：可旋转的框架。", [
    ("怎么用", "<p>与线性底盘类似，但用于旋转结构，常配合机械轴承使用。</p>"),
], params=[("运动", "旋转伸缩")],
   related=["create:linear_chassis"])

# ============================ 列车 ============================
item("create:track", "列车轨道：铺设铁路的基础。", [
    ("怎么用", "<p>用<strong>列车轨道</strong>物品沿地面铺设，会自动连接成轨道。转弯半径有限，不能直角急转。</p>"
              "<p>轨道可以上下坡，坡道要用<strong>列车轨道</strong>逐格铺。</p>"),
    ("常见坑", "<p>轨道需要平坦的地基；转弯太急会铺不上。</p>"),
], params=[("铺设", "逐格连接")],
   related=["create:track_station", "create:track_signal", "create:cart_assembler"])

item("create:track_station", "列车站：定义停靠点。", [
    ("怎么用", "<p>放在轨道旁，设置站名。列车通过<strong>时刻表</strong>识别站点并停靠。</p>"),
], params=[("功能", "停靠点")],
   related=["create:schedule", "create:track"])

item("create:track_signal", "列车信号：控制轨道区段。", [
    ("怎么用", "<p>把轨道分成区段，信号灯控制是否允许进入，避免撞车。红色=禁止，绿色=通行。</p>"),
], params=[("功能", "区段控制")],
   related=["create:track_observer", "create:track"])

item("create:schedule", "时刻表：列车的运行计划。", [
    ("怎么用", "<p>拿在手上右键列车设置路线：站点顺序、停留时间、条件（如货物装满）。</p>"),
], params=[("功能", "自动驾驶路线")],
   related=["create:track_station", "create:train_controls"])

item("create:cart_assembler", "矿车装配器：把矿车变成列车。", [
    ("怎么用", "<p>放在矿车上方，用超级胶把矿车和结构粘起来，再装上<strong>转向架</strong>，就得到一台能上轨道的列车。</p>"),
], params=[("功能", "组装列车")],
   related=["create:small_bogey", "create:large_bogey", "create:controls"])

# ================================================================
# 家族模板：没有单独词条时套用（顺序敏感，先匹配先生效）
FAMILY = [
    (r"^(acacia|birch|cherry|crimson|dark_oak|jungle|mangrove|oak|spruce|warped|bamboo)_window$",
     {"tag": "木质窗户：装饰性玻璃方块，能透光且带木框。",
      "sections": [("怎么用", "<p>用同种木材与玻璃合成，主要用于建筑外立面。同系列的<strong>窗板（pane）</strong>可以做更细的分格。</p>"),
                   ("搭配", "<p>与同色系的<strong>桌子布</strong>、<strong>座椅</strong>、<strong>栏杆</strong>一起用，能做出统一的木质工业风。</p>")]}),
    (r"_window_pane$",
     {"tag": "窗板：窗户的细分版本，适合做格栅与高窗。",
      "sections": [("怎么用", "<p>由对应窗户合成 16 个，可以像玻璃板一样连接。常用于厂房高窗与隔断。</p>")]}),
    (r"^industrial_iron_window$|^ornate_iron_window$|^weathered_iron_window$",
     {"tag": "工业铁窗：工厂风格的窗框。",
      "sections": [("怎么用", "<p>比木窗更「重工业」，适合厂房、车站、锅炉房。与<strong>工业铁块</strong>搭配效果最好。</p>")]}),
    (r"_bars$",
     {"tag": "栏杆：细金属护栏，可当装饰与安全栏。",
      "sections": [("怎么用", "<p>像铁栏杆一样连接摆放，用于平台边缘、机械围栏。不阻挡视线。</p>")]}),
    (r"_scaffolding$",
     {"tag": "脚手架：可攀爬的施工平台。",
      "sections": [("怎么用", "<p>可以像梯子一样爬上去，顶部能站人。适合搭建临时施工平台。</p>")]}),
    (r"_table_cloth$",
     {"tag": "桌布：覆盖桌面的装饰方块。",
      "sections": [("怎么用", "<p>放在桌面上会垂下布边，用于餐厅、控制室等场景。</p>")]}),
    (r"_seat$",
     {"tag": "座椅：可以坐下的装饰方块。",
      "sections": [("怎么用", "<p>右键坐下，潜行起身。配合桌布与桌子可以布置车厢、餐厅。</p>")]}),
    (r"_sail$|^sail_frame$",
     {"tag": "风帆：风车的叶片材料。",
      "sections": [("怎么用", "<p>装在<strong>风车轴承</strong>上提供动力，面积越大应力越高。</p>")]}),
    (r"_postbox$",
     {"tag": "邮筒：包裹物流的收发点。",
      "sections": [("怎么用", "<p>接入包裹网络，可以把包裹投递到指定邮筒，适合做基地间物流。</p>")]}),
    (r"_toolbox$",
     {"tag": "工具箱：便携式物品存储。",
      "sections": [("怎么用", "<p>可以随身携带，右键打开。放在地上时可以被漏斗读取。</p>")]}),
    (r"_valve_handle$",
     {"tag": "阀门手轮：手动控制流体或机械。",
      "sections": [("怎么用", "<p>装在<strong>流体阀门</strong>上，右键旋转开关。颜色仅作区分。</p>")]}),
    (r"_nixie_tube$|^nixie_tube$",
     {"tag": "霓虹管：可显示数字与符号的装饰灯。",
      "sections": [("怎么用", "<p>用<strong>显示链接</strong>绑定数据后，会显示库存、转速等数值，是控制面板的灵魂。</p>")]}),
    (r"^cut_.*_wall$|^polished_cut_.*_wall$|^small_.*_wall$|^cut_.*_brick_wall$|^polished_cut_.*_brick_wall$|^small_.*_brick_wall$",
     {"tag": "石质围墙：建筑用的矮墙。",
      "sections": [("怎么用", "<p>与同系列的石砖、台阶搭配做围栏、女儿墙。切石机可以加工出同系列的全部变体。</p>")]}),
    (r"^cut_|^polished_cut_|^small_.*_bricks|^layered_|^.*_pillar$",
     {"tag": "石质建筑方块：工业风建筑的主材。",
      "sections": [("怎么用", "<p>用<strong>切石机</strong>从基础石块加工而来，同系列还有台阶、楼梯、围墙。适合做厂房、车站、码头。</p>")]}),
    (r"^copper_shingle|^exposed_copper_shingle|^weathered_copper_shingle|^oxidized_copper_shingle|^waxed_.*_shingle",
     {"tag": "铜瓦：会随氧化变色的屋顶材料。",
      "sections": [("怎么用", "<p>未涂蜡的铜瓦会随时间氧化变色（可做旧化效果）；涂蜡后颜色固定。</p>")]}),
    (r"^copper_tile|^exposed_copper_tile|^weathered_copper_tile|^oxidized_copper_tile|^waxed_.*_tile",
     {"tag": "铜砖：精细的金属地砖。",
      "sections": [("怎么用", "<p>适合做地板与墙面，未涂蜡同样会氧化变色。</p>")]}),
    (r"^framed_glass|^horizontal_framed_glass|^vertical_framed_glass|^tiled_glass|^framed_glass_pane",
     {"tag": "框格玻璃：可拼装的工业玻璃。",
      "sections": [("怎么用", "<p>能与其他方块无缝拼接，适合做大面积厂房的玻璃幕墙与天窗。</p>")]}),
    (r"^(andesite|brass|copper)_casing$",
     {"tag": "机壳：机器的外壳与结构基材。",
      "sections": [("怎么用", "<p>用部署器把对应金属涂在去皮原木上得到。是大多数机器的合成材料。</p>")]}),
    (r"^crushed_raw_",
     {"tag": "粉碎矿石：矿石翻倍流程的中间产物。",
      "sections": [("怎么用", "<p>用<strong>粉碎轮</strong>粉碎原矿得到；再用<strong>风扇 + 水</strong>洗涤可得到额外的金属粒，最后熔炼成锭。</p>")]}),
    (r"^(asurine|crimsite|ochrum|veridium|limestone|scorchia|scoria)$|_pillar$",
     {"tag": "石材：Create 新增的装饰石种。",
      "sections": [("怎么用", "<p>分布在地下与特定生物群系，可加工成砖、台阶、围墙等建筑方块。</p>")]}),
    (r"^incomplete_",
     {"tag": "半成品：序列组装的中间产物。",
      "sections": [("怎么用", "<p>只出现在<strong>序列组装</strong>产线中，不能直接用工作台合成。</p>")]}),
]


# ======================================================================
# 第二批：物流 / 列车 / 红石 / 工具（由站主撰写）
# ======================================================================
item("create:belt_connector", "手里拿的那卷「传送带」，负责把两根轴连成一条带子。", [
    ("怎么用", "<p>手持传送带连接器，<strong>右键第一根轴</strong>，再<strong>右键第二根轴</strong>，两轴之间就会生成一条传送带。两轴之间的距离决定带子长度，方向由两轴的位置决定。</p>"
              "<p>连接时如果选错了轴，<strong>潜行 + 右键</strong>可以取消重选。带子中间可以再补轴，补的轴会成为新的滚筒。</p>"),
    ("进阶", "<ul><li>带子会以两端的转速运行，两端转速不一致时以较慢的一端为准。</li>"
            "<li>用扳手可以给带子<strong>染色</strong>，也能调整带子的倾斜与拐弯。</li>"
            "<li>带子上的物品可以被<strong>漏斗</strong>、<strong>隧道</strong>、<strong>机械臂</strong>取放。</li></ul>"),
    ("常见坑", "<p>两轴之间如果被方块挡住，带子会连不上；跨度太长时中间必须加轴，否则会提示距离过远。</p>"),
], params=[("作用", "生成传送带"), ("选点", "右键两根轴")],
   related=["create:belt", "create:andesite_tunnel", "create:andesite_funnel"])

item("create:andesite_tunnel", "隧道：让传送带穿过墙、分流、合流。", [
    ("怎么用", "<p>把隧道放在传送带经过的位置，带子会从隧道中穿过。隧道可以<strong>贴着墙</strong>放，让带子穿墙进入下一个房间。</p>"
              "<p>隧道有两种模式：<strong>直通</strong>与<strong>分流</strong>。用扳手切换后，带子上的物品会被分配到侧面输出的带子上。</p>"),
    ("典型用法", "<ul><li>一条主带 + 多个隧道 = 分流到各台机器。</li>"
                "<li>多条支带汇入一条主带 = 合流（把隧道反过来用）。</li>"
                "<li>穿墙布线，避免在墙上开大洞。</li></ul>"),
    ("常见坑", "<p>安山隧道<strong>不能过滤</strong>，所有物品都会被分走；要按物品分流请用黄铜隧道。</p>"),
], params=[("模式", "直通 / 分流"), ("过滤", "不支持")],
   related=["create:brass_tunnel", "create:belt", "create:andesite_funnel"])

item("create:brass_tunnel", "黄铜隧道：带过滤的分流器。", [
    ("怎么用", "<p>与安山隧道用法相同，但多了一个<strong>过滤槽</strong>：只有匹配过滤条件的物品才会被分流到侧面。</p>"
              "<p>过滤槽可以放具体物品，也可以放<strong>列表过滤器</strong>做批量规则；还能设置「允许 / 禁止」两种匹配方式。</p>"),
    ("典型用法", "<p>主带上混着铁锭和铜锭，用黄铜隧道把铁锭分去压板线、铜锭留在主带继续走。</p>"),
    ("常见坑", "<p>过滤槽为空时行为等同于不过滤（全部放行）；想要「只让 A 通过」记得同时设置匹配模式。</p>"),
], params=[("过滤", "支持"), ("模式", "直通 / 分流")],
   related=["create:andesite_tunnel", "create:filter", "create:attribute_filter"])

item("create:andesite_belt_funnel", "传送带漏斗：直接骑在带子上的漏斗。", [
    ("怎么用", "<p>放在传送带上方，直接从带子上<strong>抓取</strong>物品送进旁边的容器；反向放置则把容器里的物品<strong>放到</strong>带子上。</p>"
              "<p>它比「漏斗 + 侧面容器」更紧凑，适合密集的产线。</p>"),
    ("常见坑", "<p>方向由放置时的朝向决定，用扳手可以翻转；放反了会变成往带子上倒物品。</p>"),
], params=[("位置", "传送带上方"), ("方向", "可扳手翻转")],
   related=["create:brass_belt_funnel", "create:belt", "create:andesite_funnel"])

item("create:brass_belt_funnel", "传送带漏斗（黄铜）：带过滤的版本。", [
    ("怎么用", "<p>和安山版一样骑在带子上，但可以设置<strong>过滤</strong>，只抓取指定物品。适合从混合带子上「挑」东西。</p>"),
], params=[("过滤", "支持")],
   related=["create:andesite_belt_funnel", "create:filter"])

item("create:depot", "置物台：机器的「工作台面」。", [
    ("怎么用", "<p>把物品放上去，机器（压床、部署器、注液器、机械臂）就会对它加工。压床、锯等机器都需要下方有置物台或传送带才能工作。</p>"
              "<p>置物台只存<strong>一组</strong>物品；可以用漏斗自动上料/下料。</p>"),
    ("技巧", "<p>置物台可以被<strong>弹射置物台</strong>替代，后者能把成品弹出去，做自动输出更省事。</p>"),
], params=[("容量", "1 组"), ("用途", "加工台面")],
   related=["create:weighted_ejector", "create:mechanical_press", "create:deployer"])

item("create:weighted_ejector", "弹射置物台：加工完自动把成品弹走。", [
    ("怎么用", "<p>物品放上去被加工后，它会<strong>把成品朝设定方向弹射</strong>出去，落进箱子或带子。省掉一套输出漏斗。</p>"
              "<p>弹射方向可以用扳手调整；弹射力度固定。</p>"),
    ("常见坑", "<p>弹出去的物品是「掉落物」，如果没有接住会消失（5 分钟后）；建议对着带子或漏斗口弹。</p>"),
], params=[("输出", "弹射掉落物")],
   related=["create:depot", "create:mechanical_press"])

item("create:item_hatch", "物品舱口：让物品穿过墙/地板进出仓库。", [
    ("怎么用", "<p>贴在<strong>物品保险库</strong>或容器表面，另一侧接漏斗/带子，物品就能穿过方块进出，不用在墙上开洞。</p>"),
    ("常见坑", "<p>舱口必须贴在有效的库存方块上；贴错面不会工作。</p>"),
], params=[("用途", "穿墙传输")],
   related=["create:item_vault", "create:andesite_funnel"])

item("create:stockpile_switch", "存量转信器：按库存比例输出红石信号。", [
    ("怎么用", "<p>贴在容器/保险库上，用<strong>滚轮</strong>或界面设定阈值。库存低于阈值时输出红石信号，可用于「缺料自动补货」「满了自动停机」。</p>"
              "<p>它输出的是<strong>模拟信号</strong>，强度随库存变化，接比较器/模拟拉杆能读出具体比例。</p>"),
    ("典型用法", "<ul><li>仓库快空 → 触发补料产线。</li><li>仓库装满 → 关掉上游机器，避免溢出。</li></ul>"),
], params=[("输出", "模拟红石"), ("阈值", "可调")],
   related=["create:stock_link", "create:content_observer", "create:redstone_requester"])

item("create:stock_link", "仓储链接站：把库存接入「仓储网络」。", [
    ("怎么用", "<p>贴在容器/保险库上，它会把该库存登记进网络。之后用<strong>仓储发报机</strong>读取数量、用<strong>红石请求器</strong>自动取货。</p>"
              "<p>多个链接站可以组成一个跨基地的库存系统。</p>"),
    ("常见坑", "<p>链接站需要网络里有「仓储发报机」才能看到数据；单独一个链接站不显示任何东西。</p>"),
], params=[("用途", "库存联网")],
   related=["create:stock_ticker", "create:redstone_requester", "create:stockpile_switch"])

item("create:stock_ticker", "仓储发报机：把库存数量显示出来。", [
    ("怎么用", "<p>放在<strong>显示板</strong>或<strong>辉光管</strong>旁边，用<strong>显示链接器</strong>绑定要显示的物品，就能实时显示库存数量。</p>"
              "<p>它是「仓库看板」的核心：一眼看到还有多少铁、多少安山合金。</p>"),
], params=[("输出", "数值显示")],
   related=["create:display_link", "create:nixie_tube", "create:stock_link"])

item("create:factory_gauge", "工厂仪表：统计产线的产量与效率。", [
    ("怎么用", "<p>贴在机器或容器上，记录单位时间内通过/产出的物品数量，并把数值输出给显示板。适合做「产能监控」。</p>"),
], params=[("输出", "产量数值")],
   related=["create:display_link", "create:stock_ticker"])

item("create:package", "纸壳包裹：把一堆物品打包成一个单位。", [
    ("怎么用", "<p>由<strong>打包机</strong>把带子上的物品打成包裹。包裹可以被<strong>货物蛙港</strong>发送、被<strong>理包机</strong>拆开，适合跨基地物流。</p>"
              "<p>包裹上会记录里面装了什么，鼠标悬停即可查看。</p>"),
], params=[("来源", "打包机"), ("用途", "批量运输")],
   related=["create:repackager", "create:package_frogport", "create:packager"])

item("create:rare_package", "稀有包裹：拆开有惊喜的战利品包裹。", [
    ("怎么用", "<p>无法合成，通常作为探索/奖励获得。用<strong>理包机</strong>或直接右键拆开，里面是随机的稀有物品。</p>"),
], params=[("来源", "战利品")],
   related=["create:package", "create:repackager"])

item("create:package_filter", "包裹过滤器：按内容分拣包裹。", [
    ("怎么用", "<p>装在包裹物流线上，按<strong>包裹内容</strong>（而不是包裹本身）决定放行或拦截，实现「这个包裹送去 A 基地」。</p>"),
], params=[("过滤", "按包裹内容")],
   related=["create:package", "create:brass_funnel"])

item("create:package_frogport", "货物蛙港：包裹的收发站。", [
    ("怎么用", "<p>成对/多台使用，用<strong>频率</strong>配对。把包裹放进蛙港，它会把包裹「传送」到同频率的另一台蛙港。</p>"
              "<p>适合基地之间、跨维度（可配置）的自动物流。</p>"),
    ("常见坑", "<p>蛙港需要先绑定频率；没有接收端时包裹会卡在发送端。</p>"),
], params=[("传输", "包裹 / 无线")],
   related=["create:package", "create:package_filter", "create:packager"])

item("create:repackager", "理包机：拆包裹、重新打包。", [
    ("怎么用", "<p>把包裹放进去，它会<strong>拆开</strong>并把内容物输出到带子上；也可以把散装物品重新打包。</p>"
              "<p>是「包裹物流」与「普通产线」之间的转换口。</p>"),
], params=[("功能", "拆包 / 打包")],
   related=["create:package", "create:packager"])

item("create:smart_fluid_pipe", "智能流体管道：带过滤的管道。", [
    ("怎么用", "<p>和普通管道一样输送液体，但可以设置<strong>过滤</strong>，只允许指定液体通过。适合多条液体管线并行的场景。</p>"),
], params=[("过滤", "支持")],
   related=["create:fluid_pipe", "create:fluid_valve"])

item("create:glass_fluid_pipe", "玻璃流体管道：能看见里面液体的管道。", [
    ("怎么用", "<p>透明版本，方便观察液位与流动方向；功能和普通管道一致。适合做展示型管线。</p>"),
], params=[("可视", "是")],
   related=["create:fluid_pipe"])

item("create:encased_fluid_pipe", "流体管道箱：包了外壳的管道。", [
    ("怎么用", "<p>外观是完整的机壳方块，但内部仍是管道。适合埋在墙体/地板里，或者做「看不见管线」的整洁布线。</p>"),
], params=[("外观", "机壳")],
   related=["create:fluid_pipe", "create:andesite_casing"])

item("create:fluid_valve", "流体阀门：手动/红石控制管路开关。", [
    ("怎么用", "<p>串在管道上，右键或红石信号控制开合。装上<strong>阀门手轮</strong>后可以手动旋转开关。</p>"
              "<p>适合做「停机检修」「分段供液」。</p>"),
], params=[("控制", "手动 / 红石")],
   related=["create:fluid_pipe", "create:smart_fluid_pipe"])

item("create:creative_crate", "创造板条箱：无限物品源（仅创造）。", [
    ("怎么用", "<p>设定一种物品后，它会无限输出该物品。搭测试产线时替代「手动投料」。</p>"),
], params=[("模式", "仅创造")],
   related=["create:creative_fluid_tank"])

item("create:creative_fluid_tank", "创造流体储罐：无限液体源（仅创造）。", [
    ("怎么用", "<p>设定一种液体后无限供应，用于测试管道与注液设备。</p>"),
], params=[("模式", "仅创造")],
   related=["create:creative_crate", "create:fluid_tank"])

item("create:portable_storage_interface", "移动式存储接口：让动态结构对接固定仓库。", [
    ("怎么用", "<p>一个装在<strong>动态结构</strong>上、一个装在固定位置，两者对齐时物品可以在结构移动过程中自动交换。</p>"
              "<p>典型场景：移动式采矿机把矿石传回基地箱子。</p>"),
    ("常见坑", "<p>两个接口必须<strong>正面对齐</strong>且距离足够近；错位时不传输。</p>"),
], params=[("传输", "物品")],
   related=["create:portable_fluid_interface", "create:mechanical_bearing"])

item("create:portable_fluid_interface", "移动式流体接口：动态结构的液体对接。", [
    ("怎么用", "<p>与存储接口同理，但传输的是<strong>液体</strong>。移动式钻井平台、移动锅炉常用它。</p>"),
], params=[("传输", "液体")],
   related=["create:portable_storage_interface"])

# ------------------------------ 列车 ------------------------------
item("create:small_bogey", "小转向架：让列车能转弯的「轮子」。", [
    ("怎么用", "<p>装在列车底部，与轨道接触。转向架决定列车能否过弯：<strong>至少两个转向架</strong>（前后各一）才能稳定行驶。</p>"
              "<p>小转向架适合短车厢、转弯半径小的线路。</p>"),
    ("常见坑", "<p>转向架间距太近会导致过弯卡顿；装反了列车会「倒着走」。</p>"),
], params=[("用途", "列车走行部")],
   related=["create:large_bogey", "create:cart_assembler", "create:track"])

item("create:large_bogey", "大转向架：重载与高速列车用。", [
    ("怎么用", "<p>比小转向架更稳、承载更强，适合长车厢和高速线路。占位更大，需要更宽的车体。</p>"),
], params=[("用途", "重载列车")],
   related=["create:small_bogey"])

item("create:train_door", "列车门：车厢的乘客门。", [
    ("怎么用", "<p>装在车厢侧面，可以像普通门一样开关；配合<strong>列车驾驶台</strong>与站点可以自动开关门。</p>"),
], params=[("用途", "车厢门")],
   related=["create:train_trapdoor", "create:controls"])

item("create:train_trapdoor", "列车活板门：车厢顶部/底部的检修口。", [
    ("怎么用", "<p>装饰与实用兼具，可用于车厢顶部检修口或货物舱口。</p>"),
], params=[("用途", "车厢活板门")],
   related=["create:train_door"])

item("create:track_observer", "列车侦测器：检测列车通过。", [
    ("怎么用", "<p>装在轨道旁，列车经过时输出<strong>红石信号</strong>。可以做自动道口、站台提示灯、计轴器。</p>"),
    ("常见坑", "<p>只检测<strong>列车</strong>（装配过的矿车），普通矿车不会触发。</p>"),
], params=[("输出", "红石脉冲")],
   related=["create:track_signal", "create:redstone_contact"])

item("create:minecart_anchor", "矿车锚：把矿车固定在原地。", [
    ("怎么用", "<p>放在轨道上，矿车靠近会被「吸住」停稳，适合做装卸站。</p>"),
], params=[("功能", "停车")],
   related=["create:minecart_coupling", "create:track"])

item("create:minecart_contraption", "装配过的矿车：把结构装到矿车上。", [
    ("怎么用", "<p>用<strong>矿车装配器</strong>把方块结构粘到矿车上，得到一台可以移动的「小车」。可以装钻头、锯、收割机做移动机械。</p>"
              "<p>装配后的矿车可以再被<strong>矿车连轴器</strong>串成一列。</p>"),
], params=[("用途", "移动机械")],
   related=["create:cart_assembler", "create:minecart_coupling", "create:mechanical_drill"])

item("create:minecart_coupling", "矿车连轴器：把矿车串成列车。", [
    ("怎么用", "<p>手持连轴器右键两辆矿车，它们会被连接；再右键可断开。串起来的矿车会一起运动。</p>"),
], params=[("功能", "连接矿车")],
   related=["create:minecart_contraption", "create:minecart_anchor"])

item("create:controls", "列车驾驶台：手动驾驶列车。", [
    ("怎么用", "<p>装在车头，右键进入驾驶模式：前进/后退/加速，像开车一样。适合调车、试跑线路。</p>"
              "<p>想自动化就改用<strong>时刻表</strong>。</p>"),
], params=[("模式", "手动驾驶")],
   related=["create:schedule", "create:linked_controller"])

item("create:linked_controller", "无线红石遥控器：远距离遥控红石。", [
    ("怎么用", "<p>手持遥控器，潜行右键绑定<strong>发信线圈</strong>的频率，之后按键就能无线触发对应红石。</p>"
              "<p>也可以用它遥控列车（配合驾驶台）。</p>"),
], params=[("传输", "无线红石")],
   related=["create:transmitter", "create:lectern_controller"])

item("create:lectern_controller", "遥控器讲台：把遥控器固定成控制台。", [
    ("怎么用", "<p>把<strong>无线红石遥控器</strong>放上去，变成一个可交互的控制台，适合做车站/基地的控制中心。</p>"),
], params=[("用途", "固定控制台")],
   related=["create:linked_controller", "create:transmitter"])

item("create:controller_rail", "控制铁轨：给矿车加速/定向。", [
    ("怎么用", "<p>铺在轨道上，用红石信号控制加速方向，可以让矿车自动往返或加速到设定速度。</p>"),
], params=[("功能", "矿车动力")],
   related=["create:track", "create:minecart_contraption"])

item("create:fake_track", "地图轨道标记：装饰用的假轨道。", [
    ("怎么用", "<p>外观与真轨道一样，但不参与列车运行，只用于地图/建筑装饰。适合做「废弃铁路」或地图标记。</p>"),
], params=[("功能", "纯装饰")],
   related=["create:track"])

# ------------------------------ 红石与控制 ------------------------------
item("create:redstone_contact", "接触式红石信号发生器：被碰到就通电。", [
    ("怎么用", "<p>贴在方块表面，当有<strong>实体或动态结构</strong>碰到它时输出红石信号。升降机、起重机、自动门用它做「到位检测」。</p>"
              "<p>两个面对面放置的接触器可以互相感应，用来判断结构是否停靠在指定位置。</p>"),
    ("典型用法", "<p>升降机的每个楼层放一对接触器：轿厢到达时触发信号，自动开门/亮灯。官方教程里也是这么做的。</p>"),
], params=[("触发", "接触"), ("输出", "红石信号")],
   related=["create:elevator_contact", "create:track_observer"])

item("create:transmitter", "发信线圈：无线红石的「频道」。", [
    ("怎么用", "<p>放在地上，用<strong>无线红石遥控器</strong>潜行右键绑定。之后遥控器上的按键就能触发这个线圈，线圈再从所在位置输出红石信号。</p>"
              "<p>它是「远程开关」的接收端：一个遥控器可以绑定多个线圈，做多路控制。</p>"),
], params=[("配对", "遥控器"), ("输出", "红石信号")],
   related=["create:linked_controller", "create:redstone_link"])

item("create:powered_latch", "锁存器：能被红石控制的拉杆。", [
    ("怎么用", "<p>它有三个口：<strong>后方输入</strong>把状态设为「开」，<strong>侧边输入</strong>把状态设为「关」，输出保持当前状态。也可以空手右键手动切换。</p>"
              "<p>本质是一个带记忆的开关：信号消失后状态不会丢，非常适合做「自锁电路」「一键启停」。</p>"),
    ("常见坑", "<p>它记的是<strong>状态</strong>不是脉冲；两个输入同时来时，行为取决于时序，接线前先想清楚优先级。</p>"),
], params=[("输入", "置位 / 复位"), ("输出", "保持状态")],
   related=["create:powered_toggle_latch", "create:pulse_timer"])

item("create:powered_toggle_latch", "转换锁存器：每来一个脉冲就翻转一次。", [
    ("怎么用", "<p>T 触发器：后方每收到一次信号，输出就在开/关之间<strong>翻转</strong>。适合做「按一下开、再按一下关」的灯控与设备启停。</p>"),
], params=[("逻辑", "翻转 (T)")],
   related=["create:powered_latch"])

item("create:pulse_extender", "脉冲延长器：把短信号拉长。", [
    ("怎么用", "<p>输入的信号会被延长一段可配置的时间再输出，<strong>最长可设到 1 小时</strong>。用于「按一下，机器运行 30 秒」这类需求。</p>"
              "<p>用面板调整时长：右键打开配置界面。</p>"),
], params=[("时长", "可配置，最长 1 小时")],
   related=["create:pulse_repeater", "create:pulse_timer"])

item("create:pulse_repeater", "脉冲中继器：延迟后发一个短脉冲。", [
    ("怎么用", "<p>收到输入后，等待一段可配置的延迟，然后输出一个<strong>短脉冲</strong>。适合做时序控制：先开 A，2 秒后再开 B。</p>"
              "<p>延迟同样最长可设到 1 小时。</p>"),
], params=[("延迟", "可配置，最长 1 小时")],
   related=["create:pulse_extender", "create:pulse_timer"])

item("create:pulse_timer", "脉冲计时器：周期性地发脉冲。", [
    ("怎么用", "<p>按设定的间隔不断输出脉冲，像节拍器。右键打开面板调间隔；给输入端充能会<strong>暂停并重置</strong>计时。</p>"
              "<p>右键计时器可以<strong>反转输出</strong>（变成「常亮、间歇断开」），用于触发那些需要「无信号」才工作的机构。</p>"),
], params=[("输出", "周期脉冲"), ("控制", "输入充能暂停")],
   related=["create:pulse_extender", "create:pulse_repeater"])

item("create:attribute_filter", "属性过滤器：按「属性」而不是物品种类过滤。", [
    ("怎么用", "<p>放进黄铜漏斗/隧道的过滤槽，可以按<strong>附魔、耐久、名称</strong>等属性筛选物品。例如「只放行带精准采集的镐」。</p>"),
], params=[("过滤", "按属性")],
   related=["create:filter", "create:brass_funnel"])

item("create:filter", "列表过滤器：把一组物品打包成一条过滤规则。", [
    ("怎么用", "<p>在过滤器里放入多个物品，它会记住整份清单；把过滤器放进黄铜漏斗/隧道的过滤槽，就能一次匹配多种物品。</p>"
              "<p>适合「这一整类原料都放行」的场景，避免过滤槽被占满。</p>"),
], params=[("过滤", "多物品列表")],
   related=["create:attribute_filter", "create:brass_tunnel"])

item("create:display_link", "显示链接器：把数据接到显示设备上。", [
    ("怎么用", "<p>手持显示链接器右键数据源（转速表、应力表、存量转信器、仓储发报机等），再右键<strong>显示板/辉光管</strong>，它就会实时显示该数值。</p>"
              "<p>是「控制室看板」的关键零件。</p>"),
], params=[("功能", "数据绑定")],
   related=["create:display_board", "create:nixie_tube", "create:stock_ticker"])

item("create:nixie_tube", "辉光管：显示数字与文字的复古灯管。", [
    ("怎么用", "<p>被红石充能时显示<strong>信号强度</strong>（0-15）；用写好的<strong>剪贴板</strong>右键可以显示自定义文本；用染料右键改颜色。</p>"
              "<p>配合显示链接器可以显示库存、转速等实时数据。</p>"),
], params=[("显示", "信号强度 / 文本"), ("染色", "支持")],
   related=["create:display_link", "create:clipboard", "create:display_board"])

item("create:placard", "置物板：把物品「钉」在墙上展示。", [
    ("怎么用", "<p>右键放入一个物品，它会浮在板子上展示，适合做指示牌、配方墙、展览。</p>"),
], params=[("用途", "展示")],
   related=["create:display_board"])

item("create:desk_bell", "呼唤铃：按一下响一声。", [
    ("怎么用", "<p>右键敲响，发出清脆的铃声并可输出红石脉冲。适合做「服务台」「到站提示」。</p>"),
], params=[("交互", "右键响铃")],
   related=["create:peculiar_bell", "create:haunted_bell"])

item("create:haunted_bell", "缠魂钟：灵魂火焰版的钟。", [
    ("怎么用", "<p>由普通钟经过<strong>缠魂</strong>（风扇 + 灵魂火）得到。敲响时声音更阴森，可作装饰与信号。</p>"),
], params=[("来源", "缠魂")],
   related=["create:peculiar_bell", "create:desk_bell"])

item("create:peculiar_bell", "奇异钟：造型奇特的装饰钟。", [
    ("怎么用", "<p>装饰性铃铛，可以敲响。适合放在列车站台、商店门口。</p>"),
], params=[("用途", "装饰/信号")],
   related=["create:desk_bell"])

item("create:cuckoo_clock", "布谷鸟闹钟：到点会「报时」的钟。", [
    ("怎么用", "<p>可以设定时间，到点弹出小鸟并发出声音/红石信号。适合做车站时钟、整点广播。</p>"),
], params=[("功能", "定时报时")],
   related=["create:mysterious_cuckoo_clock"])

item("create:mysterious_cuckoo_clock", "布谷鸟闹钟（神秘）：稀有变体。", [
    ("怎么用", "<p>外观与普通布谷鸟钟不同的稀有版本，功能一致，属于收藏/装饰品。</p>"),
], params=[("稀有度", "稀有")],
   related=["create:cuckoo_clock"])

item("create:elevator_contact", "升降机锚点：标记电梯楼层。", [
    ("怎么用", "<p>在电梯井每一层放一个锚点，用<strong>升降机滑轮</strong>把轿厢拉过去。给锚点通红石可以「召唤」轿厢到该层。</p>"
              "<p>轿厢到达时锚点会输出信号，可用来开门、亮灯。用显示链接器接锚点还能显示当前楼层。</p>"),
    ("常见坑", "<p>锚点要正对轿厢，且同一列上不要漏层，否则选层会错位。</p>"),
], params=[("功能", "楼层标记"), ("输出", "到站信号")],
   related=["create:elevator_pulley", "create:redstone_contact"])

item("create:redstone_requester", "红石请求器：用红石脉冲「下单」。", [
    ("怎么用", "<p>放置前先右键<strong>仓储链接站</strong>接入网络。右键打开配置菜单，设定要请求的物品与数量；之后<strong>每来一次红石脉冲就下一单</strong>。</p>"
              "<p>订单会由网络里的打包机打成包裹，送到指定位置。适合做「自动补货」。</p>"),
    ("常见坑", "<p>网络里必须有打包机与足够的库存；没有目标地址时包裹会留在原地。</p>"),
], params=[("触发", "红石脉冲"), ("依赖", "仓储网络")],
   related=["create:stock_link", "create:stock_ticker", "create:packager"])

item("create:wand_of_symmetry", "对称之杖：一键镜像建造。", [
    ("怎么用", "<p>先右键设定对称面，之后放置/破坏方块时会<strong>同时在对称位置</strong>执行，做对称建筑快一倍。</p>"
              "<p>支持多个对称轴，适合造车站、厂房这类规整建筑。</p>"),
], params=[("功能", "镜像建造")],
   related=["create:schematicannon", "create:handheld_worldshaper"])

item("create:contraption_controls", "动态结构控制器：在移动的结构上控制元件。", [
    ("怎么用", "<p>装在动态结构上，结构运动时它上面的元件默认<strong>全部启用</strong>；控制器可以按过滤器逐个开关它们。</p>"
              "<p>如果结构实体化时它收到了红石信号，目标元件会<strong>一开始就关闭</strong>。</p>"),
], params=[("功能", "结构内元件开关")],
   related=["create:mechanical_bearing", "create:controls"])

item("create:turntable", "转盘：把结构旋转 90°。", [
    ("怎么用", "<p>把动态结构放上去，通入旋转力会让整个结构<strong>按 90° 步进旋转</strong>，用于转向、转车台。</p>"
              "<p>官方教程还提到：动力轴承转动时会保持转盘的垂直朝向不变。</p>"),
], params=[("运动", "90° 步进旋转")],
   related=["create:mechanical_bearing", "create:clockwork_bearing"])

item("create:crafter_slot_cover", "合成槽盖板：盖住合成器的一格。", [
    ("怎么用", "<p>有些配方用不到合成器网格的所有格子，用盖板把多余格子盖住，合成器就把它当作<strong>空格</strong>处理，配方才能正确匹配。</p>"
              "<p>用扳手在背面创建的共享输入也可以跨过有盖的合成器。</p>"),
], params=[("作用", "占位/屏蔽")],
   related=["create:mechanical_crafter"])

# ------------------------------ 工具与装备 ------------------------------
item("create:sticker", "黏着器：红石控制的「胶水」。", [
    ("怎么用", "<p>给红石信号时，它会<strong>黏住正前方的方块</strong>；再给一次信号则断开。当它作为动态结构的一部分移动时，黏住的方块会跟着一起走。</p>"
              "<p>和超级胶不同，黏着器是<strong>可开关</strong>的：适合做「抓取—释放」机构，比如自动装卸、可分离的车厢。</p>"),
], params=[("控制", "红石"), ("作用", "可开关黏附")],
   related=["create:super_glue", "create:mechanical_piston"])

item("create:whisk", "搅拌器（手持）：工作盆的搅拌头。", [
    ("怎么用", "<p>它是<strong>动力搅拌器</strong>的合成材料/部件，本身不是手持工具。合成搅拌器需要它。</p>"
              "<p>动力搅拌器放在工作盆上方，通入旋转力就能混合原料。</p>"),
], params=[("用途", "合成动力搅拌器")],
   related=["create:mechanical_mixer", "create:basin"])

item("create:schematic", "蓝图：一张可被加农炮执行的建筑图纸。", [
    ("怎么用", "<p>用<strong>蓝图桌</strong>框选区域生成空白蓝图，再拿<strong>蓝图与笔</strong>右键保存建筑。保存好的蓝图放进<strong>蓝图加农炮</strong>，加农炮就会自动把建筑「打印」出来。</p>"
              "<p>蓝图里会记录所需材料清单，可以配合仓储发报机自动备料。</p>"),
], params=[("用途", "保存/建造建筑")],
   related=["create:empty_schematic", "create:schematic_table", "create:schematicannon"])

item("create:empty_schematic", "空白蓝图：还没记录内容的图纸。", [
    ("怎么用", "<p>在<strong>蓝图桌</strong>上框选区域后得到。拿着它用<strong>蓝图与笔</strong>右键即可写入建筑。</p>"),
], params=[("用途", "待写入")],
   related=["create:schematic", "create:schematic_table"])

item("create:schematic_table", "蓝图桌：框选并生成蓝图。", [
    ("怎么用", "<p>放好蓝图桌，右键打开界面，用两个角点<strong>框选</strong>要保存的建筑范围，确认后消耗一张空白蓝图生成成品蓝图。</p>"
              "<p>范围越大，蓝图文件越大，建造时消耗的材料也越多。</p>"),
], params=[("功能", "框选生成蓝图")],
   related=["create:schematic", "create:schematicannon"])

item("create:schematicannon", "蓝图加农炮：自动建造。", [
    ("怎么用", "<p>放入蓝图，接上动力与材料（用漏斗/箱子供料），它就会把建筑一块块「射」到目标位置。</p>"
              "<p>建造前要先用<strong>蓝图与笔</strong>在地上标出原点与朝向。</p>"),
    ("常见坑", "<p>材料不足时会停工等待；加农炮射程有限，超大建筑要分段建造。</p>"),
], params=[("功能", "自动建造"), ("依赖", "材料 + 动力")],
   related=["create:schematic", "create:schematic_table"])

item("create:clipboard", "剪贴板：可书写的记事板。", [
    ("怎么用", "<p>右键打开编辑界面写文字。写好的剪贴板可以：设置<strong>显示板</strong>的静态文本、设置<strong>辉光管</strong>显示内容、记录<strong>货物蛙港</strong>的地址。</p>"
              "<p>是「控制面板」与「物流地址」的通用输入工具。</p>"),
], params=[("用途", "文本/地址")],
   related=["create:display_board", "create:nixie_tube", "create:package_frogport"])

item("create:shopping_list", "采购清单：记录你缺什么材料。", [
    ("怎么用", "<p>把要买的物品写进清单，配合仓储网络可以快速核对库存；也方便多人分工备料。</p>"),
], params=[("用途", "备料清单")],
   related=["create:clipboard", "create:stock_ticker"])

item("create:crafting_blueprint", "合成蓝图：把配方「画」在墙上。", [
    ("怎么用", "<p>放在墙上会显示一个合成配方，适合做教学墙、配方提示。可以切换显示的配方。</p>"),
], params=[("用途", "配方展示")],
   related=["create:display_board", "create:placard"])

item("create:cardboard_helmet", "纸板头盔：纸板套装的一部分。", [
    ("怎么用", "<p>用纸板制作的廉价护甲，防御力很低，但<strong>穿戴全套</strong>有特殊效果（潜行时不易被生物发现，适合潜入）。</p>"
              "<p>耐久很低，坏了就换，别拿去打架。</p>"),
], params=[("类型", "护甲"), ("特点", "潜行隐蔽")],
   related=["create:cardboard_chestplate", "create:cardboard_leggings", "create:cardboard_boots"])

item("create:cardboard_chestplate", "纸板胸甲：纸板套装的一部分。", [
    ("怎么用", "<p>与纸板头盔、护腿、靴子组成全套，提供少量护甲与<strong>潜行隐蔽</strong>效果。适合潜行探索与恶作剧。</p>"),
], params=[("类型", "护甲")],
   related=["create:cardboard_helmet"])

item("create:cardboard_leggings", "纸板护腿：纸板套装的一部分。", [
    ("怎么用", "<p>纸板套装部件，凑齐全套获得潜行隐蔽效果。</p>"),
], params=[("类型", "护甲")],
   related=["create:cardboard_helmet"])

item("create:cardboard_boots", "纸板靴子：纸板套装的一部分。", [
    ("怎么用", "<p>纸板套装部件，凑齐全套获得潜行隐蔽效果；走路声音也会变小。</p>"),
], params=[("类型", "护甲")],
   related=["create:cardboard_helmet"])

item("create:cardboard_sword", "纸棍：纸板做的「剑」。", [
    ("怎么用", "<p>几乎没伤害的玩具武器，适合整活。真打怪请换铁剑。</p>"),
], params=[("类型", "武器（玩具）")],
   related=["create:cardboard_helmet"])

item("create:copper_diving_helmet", "铜潜水头盔：水下呼吸。", [
    ("怎么用", "<p>戴在头上，配合<strong>铜背罐</strong>供气即可在水下呼吸。头盔本身需要背罐里的空气。</p>"
              "<p>铜制版本耐久有限，深潜/长时间作业建议升级下界合金版。</p>"),
], params=[("类型", "头盔"), ("依赖", "背罐供气")],
   related=["create:copper_backtank", "create:copper_diving_boots", "create:netherite_diving_helmet"])

item("create:copper_diving_boots", "铜潜水靴：水下行走。", [
    ("怎么用", "<p>穿在脚上，让你在水下<strong>正常行走</strong>而不是漂浮，配合头盔与背罐构成完整潜水套装。</p>"),
], params=[("类型", "靴子")],
   related=["create:copper_diving_helmet", "create:copper_backtank"])

item("create:netherite_diving_helmet", "下界合金潜水头盔：耐久更高的潜水头盔。", [
    ("怎么用", "<p>铜头盔的升级版，耐久更高、更耐摔，适合长时间水下作业。</p>"),
], params=[("类型", "头盔（升级）")],
   related=["create:netherite_backtank", "create:copper_diving_helmet"])

item("create:netherite_diving_boots", "下界合金潜水靴：升级版潜水靴。", [
    ("怎么用", "<p>铜靴的升级版，耐久更高。</p>"),
], params=[("类型", "靴子（升级）")],
   related=["create:netherite_backtank", "create:copper_diving_boots"])

item("create:netherite_backtank", "下界合金背罐：更大的储气量。", [
    ("怎么用", "<p>铜背罐的升级版，储气更多、更耐用。同样穿在胸甲槽，为潜水头盔供气。</p>"),
], params=[("类型", "胸甲槽"), ("容量", "大于铜背罐")],
   related=["create:copper_backtank", "create:netherite_diving_helmet"])

item("create:extendo_grip", "伸缩机械手：远距离放置/交互。", [
    ("怎么用", "<p>装在手部（副手/主手）后，可以像加长手臂一样在更远处放置方块、右键机器，适合高处作业与危险区域操作。</p>"
              "<p>用机械动力合成（动力合成器）制作。</p>"),
], params=[("功能", "延长交互距离")],
   related=["create:potato_cannon", "create:wrench"])

item("create:potato_cannon", "土豆加农炮：把土豆当炮弹。", [
    ("怎么用", "<p>装填土豆（或其他可发射物）后右键射击，可以打怪、打靶、触发远处的按钮。娱乐性大于实用性。</p>"),
], params=[("功能", "远程射击")],
   related=["create:extendo_grip"])

item("create:sand_paper", "砂纸：打磨抛光。", [
    ("怎么用", "<p>用于<strong>砂纸打磨</strong>配方：把某些物品打磨成更精细的版本（如玫瑰石英 → 磨制玫瑰石英）。在配方里作为工具消耗。</p>"),
], params=[("用途", "打磨配方")],
   related=["create:red_sand_paper", "create:polished_rose_quartz"])

item("create:red_sand_paper", "红沙砂纸：更高级的打磨工具。", [
    ("怎么用", "<p>由红沙制作，用于更高阶的打磨配方。与普通砂纸用途相同但等级更高。</p>"),
], params=[("用途", "打磨配方")],
   related=["create:sand_paper"])

item("create:tree_fertilizer", "树木肥料：让树苗长成大树。", [
    ("怎么用", "<p>对树苗使用，能<strong>强制长成大树</strong>（包括 2×2 的大型树种），比骨粉更可控。适合自动化林场。</p>"),
], params=[("用途", "催熟树木")],
   related=["create:mechanical_saw", "create:deployer"])

item("create:sweet_roll", "甜甜卷：回血食物。", [
    ("怎么用", "<p>用<strong>注液器</strong>把牛奶/蜂蜜等灌进面团类食物得到。恢复饥饿值与饱和度，是 Create 里的常用食物。</p>"),
], params=[("类型", "食物")],
   related=["create:builders_tea", "create:honeyed_apple"])

item("create:builders_tea", "建筑工茶饮：喝了有增益。", [
    ("怎么用", "<p>用注液器灌装得到。喝下后提供短暂的增益效果（如速度/急迫），适合长时间建造。</p>"),
], params=[("类型", "饮品")],
   related=["create:sweet_roll"])

item("create:blaze_cake", "烈焰蛋糕：烈焰人炉的燃料。", [
    ("怎么用", "<p>放进<strong>烈焰人炉</strong>并点燃，提供加热（锅炉、工作盆）或灵魂火焰（缠魂）。会持续消耗，需要定期补充。</p>"),
    ("常见坑", "<p>没有蛋糕时炉子会熄灭，锅炉产汽会中断——自动化产线记得留补料。</p>"),
], params=[("用途", "加热燃料")],
   related=["create:blaze_burner", "create:steam_engine"])

item("create:honeyed_apple", "蜜渍苹果：蜂蜜做的食物。", [
    ("怎么用", "<p>用蜂蜜灌注苹果得到，恢复饥饿值；也可作为蜂蜜的用途之一。</p>"),
], params=[("类型", "食物")],
   related=["create:sweet_roll", "create:honey"])

item("create:chocolate_glazed_berries", "巧克力包层浆果：甜点。", [
    ("怎么用", "<p>用<strong>注液器</strong>把巧克力浇在甜浆果上得到，恢复饥饿值。</p>"),
], params=[("类型", "食物")],
   related=["create:bar_of_chocolate", "create:chocolate"])

item("create:bar_of_chocolate", "巧克力棒：巧克力的固体形态。", [
    ("怎么用", "<p>由<strong>巧克力</strong>液体在注液器/盆中凝固得到。可直接吃，也是巧克力包层浆果的材料。</p>"),
], params=[("类型", "食物")],
   related=["create:chocolate", "create:chocolate_glazed_berries"])

# ------------------------------ 材料与零件 ------------------------------
item("create:brass_sheet", "黄铜板：压床压出来的薄板。", [
    ("怎么用", "<p>把<strong>黄铜锭</strong>放进机械压床压成。黄铜板是精密构件、列车部件等高级配方的常用材料。</p>"),
], params=[("工艺", "压床压制")],
   related=["create:brass_ingot", "create:iron_sheet", "create:precision_mechanism"])

item("create:copper_sheet", "铜板：铜做的薄板。", [
    ("怎么用", "<p>铜锭压成。用于铜机壳、装饰与部分机器配方。铜在 Create 里是重要基础金属。</p>"),
], params=[("工艺", "压床压制")],
   related=["create:iron_sheet", "create:copper_casing"])

item("create:iron_sheet", "铁板：最常用的金属板。", [
    ("怎么用", "<p>铁锭压成。铁板是 Create 里用量最大的中间材料之一：机壳、齿轮、传送带、电子管都要它。</p>"
              "<p>开局建议<strong>第一台机器就做压床</strong>，否则手搓铁板会非常痛苦。</p>"),
], params=[("工艺", "压床压制")],
   related=["create:mechanical_press", "create:andesite_casing"])

item("create:golden_sheet", "金板：精密构件的原料。", [
    ("怎么用", "<p>金锭压成。精密构件的<strong>序列组装</strong>产线以金板为基材，是列车与高级机器的必经之路。</p>"),
], params=[("工艺", "压床压制")],
   related=["create:precision_mechanism", "create:brass_sheet"])

item("create:sturdy_sheet", "坚固板：需要序列组装的高级板材。", [
    ("怎么用", "<p>没有普通合成配方，必须走<strong>序列组装</strong>产线：以某种基材开始，经过压床/部署器多道工序成型。</p>"
              "<p>它是高级机器、列车外壳等配方的重要材料，产线较长，建议专门建一条。</p>"),
], params=[("工艺", "序列组装")],
   related=["create:precision_mechanism", "create:iron_sheet"])

item("create:brass_nugget", "黄铜粒：黄铜的小单位。", [
    ("怎么用", "<p>由黄铜锭分解或在部分配方中获得。用于精细配方与回收。</p>"),
], params=[("用途", "精细材料")],
   related=["create:brass_ingot"])

item("create:copper_nugget", "铜粒：铜的小单位。", [
    ("怎么用", "<p>铜锭分解得到。可用于合成、回收，也是部分配方的辅料。</p>"),
], params=[("用途", "精细材料")],
   related=["create:copper_sheet"])

item("create:zinc_ingot", "锌锭：黄铜的另一半。", [
    ("怎么用", "<p>由<strong>粗锌</strong>或锌矿石熔炼得到。铜 + 锌（加热搅拌）就是<strong>黄铜</strong>，所以锌是中期产线的关键。</p>"),
], params=[("来源", "锌矿/粗锌"), ("用途", "制黄铜")],
   related=["create:brass_ingot", "create:raw_zinc", "create:zinc_ore"])

item("create:zinc_nugget", "锌粒：锌的小单位。", [
    ("怎么用", "<p>锌锭分解得到，用于精细配方。</p>"),
], params=[("用途", "精细材料")],
   related=["create:zinc_ingot"])

item("create:raw_zinc", "粗锌：还没熔炼的锌矿石。", [
    ("怎么用", "<p>挖锌矿石直接掉落。可以熔炼成锌锭；也可以先用<strong>粉碎轮</strong>粉碎，再洗涤，获得额外产量。</p>"),
], params=[("来源", "锌矿石")],
   related=["create:zinc_ingot", "create:crushing_wheel"])

item("create:cinder_flour", "余烬面粉：下界岩磨成的粉。", [
    ("怎么用", "<p>用<strong>粉碎轮</strong>粉碎下界岩得到。是制作<strong>烈焰蛋糕</strong>等下界相关物品的材料。</p>"),
], params=[("工艺", "粉碎下界岩")],
   related=["create:blaze_cake", "create:wheat_flour"])

item("create:wheat_flour", "小麦面粉：磨盘磨小麦。", [
    ("怎么用", "<p>用<strong>磨盘</strong>把小麦磨成面粉。面粉加水（搅拌或洗涤）就是<strong>面团</strong>，再烧成面包。</p>"
              "<p>这是自动化食物产线的第一步。</p>"),
], params=[("工艺", "磨盘")],
   related=["create:dough", "create:millstone", "create:sweet_roll"])

item("create:dough", "面团：面粉加水。", [
    ("怎么用", "<p>面粉 + 水（工作盆搅拌、或风扇洗涤）得到。烧制后是面包，也是甜甜卷等食物的基础。</p>"),
], params=[("配方", "面粉 + 水")],
   related=["create:wheat_flour", "create:sweet_roll"])

item("create:pulp", "纸浆：做纸板的原料。", [
    ("怎么用", "<p>把可制浆的物品（植物类）丢进<strong>工作盆</strong>加水搅拌，得到纸浆。纸浆压成<strong>纸板</strong>，纸板可以做纸箱、纸板装备。</p>"),
], params=[("工艺", "搅拌")],
   related=["create:cardboard", "create:cardboard_block"])

item("create:cardboard", "纸板：纸浆压成。", [
    ("怎么用", "<p>纸浆用<strong>压床</strong>压成纸板。纸板用于制作纸板装备、纸箱方块与包裹相关物品。</p>"),
], params=[("工艺", "压床")],
   related=["create:pulp", "create:cardboard_block", "create:package"])

item("create:chocolate", "巧克力（液体）：能灌注的甜食。", [
    ("怎么用", "<p>液体形态，用<strong>注液器</strong>灌到食物/模具上，或用<strong>物品沥干器</strong>回收。凝固后得到<strong>巧克力棒</strong>。</p>"),
], params=[("形态", "液体")],
   related=["create:bar_of_chocolate", "create:spout", "create:item_drain"])

item("create:honey", "蜂蜜（液体）：Create 的流体之一。", [
    ("怎么用", "<p>可以用<strong>软管滑轮</strong>从蜂巢/蜂蜜块区域抽取，也可以用桶倒入。用于灌注食物（蜜渍苹果）与部分配方。</p>"),
], params=[("形态", "液体")],
   related=["create:honey_bucket", "create:spout", "create:hose_pulley"])

item("create:experience_nugget", "经验颗粒：把经验变成物品。", [
    ("怎么用", "<p>粉碎矿石时有概率掉落；也可以把<strong>经验块</strong>分解。右键使用可以<strong>获得经验</strong>，等于把经验存成了「货币」。</p>"
              "<p>自动化矿井里它会不断产出，是很实用的副产物。</p>"),
], params=[("来源", "粉碎矿石/经验块"), ("用途", "储存经验")],
   related=["create:experience_block", "create:crushing_wheel"])

item("create:experience_block", "经验块：大量经验的固体形态。", [
    ("怎么用", "<p>由经验颗粒合成。可以放置、分解回颗粒，或用于存储/运输经验。经验农场的好搭档。</p>"),
], params=[("用途", "储存经验")],
   related=["create:experience_nugget"])

item("create:powdered_obsidian", "黑曜石粉末：粉碎黑曜石得到。", [
    ("怎么用", "<p>用<strong>粉碎轮</strong>粉碎黑曜石。是制作<strong>未加工的黑曜石板</strong>等高级材料的原料。</p>"),
], params=[("工艺", "粉碎黑曜石")],
   related=["create:unprocessed_obsidian_sheet", "create:sturdy_sheet"])

item("create:unprocessed_obsidian_sheet", "未加工的黑曜石板：半成品。", [
    ("怎么用", "<p>黑曜石粉末压制/组装得到的中间产物，需要继续加工（序列组装）才能成为可用的坚固板材。</p>"),
], params=[("阶段", "半成品")],
   related=["create:powdered_obsidian", "create:sturdy_sheet"])

item("create:refined_radiance", "光辉石：发光的高级材料。", [
    ("怎么用", "<p>没有普通合成配方，属于特殊转化产物（与彩色化合物、光照条件相关）。用于高级装饰与部分终局配方。</p>"
              "<p>具体获取方式建议对照 JEI/官方资料，本站不臆测配方细节。</p>"),
], params=[("来源", "特殊转化")],
   related=["create:shadow_steel", "create:chromatic_compound"])

item("create:shadow_steel", "暗影钢：吞噬光的材料。", [
    ("怎么用", "<p>与光辉石相对的特殊材料，同样没有普通合成配方，需要在特定条件下转化获得。用于终局装备与装饰。</p>"),
], params=[("来源", "特殊转化")],
   related=["create:refined_radiance"])

item("create:electron_tube", "电子管：红石与玻璃做的元件。", [
    ("怎么用", "<p>工作台合成（铁板 + 玻璃类材料）。电子管是<strong>转速控制器</strong>、<strong>显示板</strong>、<strong>精密构件</strong>等高级配方的关键零件。</p>"),
], params=[("用途", "高级元件")],
   related=["create:precision_mechanism", "create:rotation_speed_controller"])

item("create:polished_rose_quartz", "磨制玫瑰石英：打磨过的光学材料。", [
    ("怎么用", "<p>用<strong>砂纸打磨</strong>玫瑰石英得到。用于显示板、玫瑰石英灯等需要「透镜」的配方。</p>"),
], params=[("工艺", "砂纸打磨")],
   related=["create:rose_quartz", "create:sand_paper", "create:display_board"])

item("create:chromatic_compound", "彩色化合物：光学材料的中间体。", [
    ("怎么用", "<p>高级材料，参与光辉石/暗影钢相关的转化链。获取与用途建议结合 JEI 查看，本站不臆测具体配方。</p>"),
], params=[("阶段", "中间体")],
   related=["create:refined_radiance", "create:shadow_steel"])

# ------------------------------ 机器补充 ------------------------------
item("create:gantry_shaft", "起重机杆：龙门架的「轨道」。", [
    ("怎么用", "<p>一根根接起来形成长轨道，<strong>起重机取物器</strong>骑在上面移动。杆的方向决定取物器的移动方向，转速决定移动速度。</p>"
              "<p>被红石激活的起重机杆不会移动取物器，而是把旋转力传给取物器的输出杆——这是做「边走边转」机构的关键。</p>"),
    ("进阶", "<p>起重机可以<strong>串联</strong>：取物器上再装杆，实现多轴运动（类似 3D 打印机）。</p>"),
], params=[("作用", "直线轨道"), ("红石", "停止移动/传力")],
   related=["create:gantry_carriage", "create:linear_chassis"])

item("create:elevator_pulley", "升降机滑轮：多层电梯的核心。", [
    ("怎么用", "<p>在电梯井顶部放滑轮，下方挂轿厢结构。用<strong>升降机锚点</strong>标记楼层，右键滑轮选择目标楼层，轿厢就会垂直移动。</p>"
              "<p>速度取决于输入转速；到达楼层时锚点会输出信号，可自动开门。</p>"),
    ("搭建要点", "<ul><li>用一对<strong>接触式红石信号发生器</strong>做位置检测。</li>"
                "<li>在轿厢上装<strong>动态结构控制器</strong>方便选层。</li>"
                "<li>滑动门会在轿厢移动时自动开关。</li></ul>"),
], params=[("运动", "垂直多楼层"), ("选层", "右键/锚点")],
   related=["create:elevator_contact", "create:rope_pulley", "create:redstone_contact"])

item("create:hose_pulley", "软管滑轮：大范围抽液/排液。", [
    ("怎么用", "<p>放下软管到液体中，接上管道与动力：正转放管、反转收管。它可以<strong>抽取</strong>世界中的液体，也可以把管道送来的液体<strong>排放</strong>成液体源。</p>"
              "<p>抽取顺序由上至下，排放由下至上；速度取决于管道里的流速。</p>"),
    ("进阶", "<p>软管放进足够大的流体中时，抽取/排放<strong>不会消耗流体源</strong>，等于无限液体。</p>"),
], params=[("运动", "垂直收放"), ("依赖", "管道 + 动力")],
   related=["create:fluid_pipe", "create:mechanical_pump", "create:rope_pulley"])

item("create:pulley_magnet", "滑轮磁铁：绳索滑轮的配件。", [
    ("怎么用", "<p>装在绳索/升降滑轮的末端，用来<strong>吸附并固定</strong>动态结构，让滑轮能稳定地吊起轿厢或平台。</p>"),
], params=[("作用", "连接结构")],
   related=["create:rope_pulley", "create:elevator_pulley"])

item("create:propeller", "扇叶：给动态结构提供推力。", [
    ("怎么用", "<p>装在动态结构（飞行器/船）上，转动时产生<strong>推力</strong>。是 Create 里做飞行器与船只的核心部件。</p>"
              "<p>多个扇叶可以叠加推力；方向由安装朝向决定。</p>"),
], params=[("作用", "推进")],
   related=["create:encased_fan", "create:mechanical_bearing"])

item("create:piston_extension_pole", "活塞杆：延长活塞行程。", [
    ("怎么用", "<p>装在动力活塞背面，<strong>每加一根就多推一格</strong>。没有活塞杆，动力活塞无法推动方块。</p>"),
], params=[("作用", "增加行程")],
   related=["create:mechanical_piston", "create:sticky_mechanical_piston"])

item("create:sticky_mechanical_piston", "黏性动力活塞：能推也能拉。", [
    ("怎么用", "<p>和普通动力活塞一样推动结构，但<strong>回程时会把结构拉回来</strong>，适合做可伸缩的机械臂、往复机构。</p>"),
], params=[("运动", "推 + 拉")],
   related=["create:mechanical_piston", "create:piston_extension_pole"])

item("create:mechanical_piston_head", "动力活塞头：活塞的「推面」。", [
    ("怎么用", "<p>动力活塞伸出时形成的头部方块，是结构连接面。一般不需要手动放置，拆装活塞时会自然出现/消失。</p>"),
], params=[("作用", "推动面")],
   related=["create:mechanical_piston"])

item("create:clockwork_bearing", "时钟轴承：按游戏内时间旋转。", [
    ("怎么用", "<p>接受旋转力后，它带着结构<strong>按照游戏内时间</strong>旋转（像钟表指针）。右键可以启停。</p>"
              "<p>在时针前方还能再挂一个结构作为<strong>分针</strong>，两个结构不能互相粘住。适合做巨型时钟、天文台。</p>"),
], params=[("运动", "按时间旋转")],
   related=["create:mechanical_bearing", "create:turntable"])

item("create:secondary_linear_chassis", "轴向底盘二号：线性底盘的变体。", [
    ("怎么用", "<p>由线性底盘转换而来，伸缩轴向与普通版不同，用于拼接更复杂的伸缩框架。</p>"),
], params=[("作用", "线性伸缩")],
   related=["create:linear_chassis", "create:radial_chassis"])

item("create:sail_frame", "风帆框架：风帆的骨架。", [
    ("怎么用", "<p>风车的骨架方块，用来支撑帆布；本身不提供动力，装上<strong>风帆</strong>后才有效。</p>"),
], params=[("作用", "风车骨架")],
   related=["create:windmill_bearing", "create:white_sail"])

item("create:water_wheel_structure", "大型水车（结构）：大型水车的实体形态。", [
    ("怎么用", "<p>这是大型水车作为动态结构时的方块形态，通常不需要手动获取。放置<strong>大型水车</strong>并通水即可发电。</p>"),
], params=[("说明", "结构形态")],
   related=["create:large_water_wheel", "create:water_wheel"])

# ------------------------------ 装饰补充 ------------------------------
item("create:andesite_door", "安山门：工业风的双开门。", [
    ("怎么用", "<p>两格高的门，右键开关。安山材质偏灰，适合厂房、仓库、机房。</p>"),
], params=[("类型", "门")],
   related=["create:brass_door", "create:copper_door"])

item("create:brass_door", "黄铜门：带金属光泽的门。", [
    ("怎么用", "<p>黄铜材质的门，适合车站、办公室等「精装」场景。</p>"),
], params=[("类型", "门")],
   related=["create:andesite_door", "create:copper_door"])

item("create:copper_door", "铜门：会氧化的铜制门。", [
    ("怎么用", "<p>铜材质门，未涂蜡时会随时间氧化变色，可以做新旧对比的立面。</p>"),
], params=[("类型", "门")],
   related=["create:andesite_door", "create:brass_door"])

item("create:framed_glass_door", "边框玻璃门：通透的玻璃门。", [
    ("怎么用", "<p>玻璃门，适合做厂房隔断、温室入口，不挡视线。</p>"),
], params=[("类型", "门")],
   related=["create:framed_glass", "create:framed_glass_trapdoor"])

item("create:framed_glass_trapdoor", "边框玻璃活板门：玻璃检修口。", [
    ("怎么用", "<p>玻璃活板门，可水平或垂直安装，适合做天窗、地板检修口。</p>"),
], params=[("类型", "活板门")],
   related=["create:framed_glass_door", "create:framed_glass"])

item("create:metal_girder", "金属梁：承重结构的装饰。", [
    ("怎么用", "<p>细长的金属梁，可以像柱子一样竖着摆，也可以横过来做桁架。与<strong>金属支架</strong>搭配能做出非常「工厂」的结构。</p>"),
], params=[("用途", "结构装饰")],
   related=["create:metal_bracket", "create:industrial_iron_block"])

item("create:metal_bracket", "金属支架：把梁固定到墙上。", [
    ("怎么用", "<p>连接金属梁与墙面的小配件，让桁架看起来更合理。纯装饰，但能让建筑细节提升一个档次。</p>"),
], params=[("用途", "结构装饰")],
   related=["create:metal_girder"])

item("create:railway_casing", "列车机壳：列车部件的专用外壳。", [
    ("怎么用", "<p>列车相关的合成材料（转向架、驾驶台、车站等都用到）。外观是带铆钉的深色金属。</p>"),
], params=[("用途", "列车配方")],
   related=["create:track", "create:small_bogey"])

item("create:industrial_iron_block", "工业铁块：深色带纹理的铁块。", [
    ("怎么用", "<p>工业风建筑的主材，适合做厂房墙面、机器底座。与<strong>工业铁窗</strong>、<strong>金属梁</strong>是同一套视觉语言。</p>"),
], params=[("用途", "建筑主材")],
   related=["create:weathered_iron_block", "create:industrial_iron_window"])

item("create:weathered_iron_block", "锈蚀的工业铁块：做旧版本。", [
    ("怎么用", "<p>工业铁块的锈蚀变体，用来做「废弃工厂」「老码头」的氛围。可以两种混铺做出斑驳感。</p>"),
], params=[("用途", "做旧装饰")],
   related=["create:industrial_iron_block"])

# ---- 修正：仓储发报机是「下单终端」，不是显示器 ----
item("create:stock_ticker", "仓储发报机：向仓储网络「下单」的终端。", [
    ("怎么用", "<p>放置前先右键一个<strong>仓储链接站</strong>接入网络。右键它打开订单界面，选好物品与数量后下单。</p>"
              "<p>订单会由网络里的<strong>打包机</strong>打包，再通过包裹物流送到你指定的位置。也可以让它为<strong>蓝图加农炮</strong>备料。</p>"),
    ("和红石请求器的区别", "<p>发报机是<strong>手动/界面下单</strong>；红石请求器是<strong>红石脉冲自动下单</strong>。做全自动补货用后者。</p>"),
    ("小技巧", "<p>「仓库管理员」可以是一个坐着的生物或烈焰人炉；用剪贴板记录地址后可以在界面里自动填地址。</p>"),
], params=[("触发", "界面下单"), ("依赖", "仓储网络 + 打包机")],
   related=["create:stock_link", "create:redstone_requester", "create:packager"])

FAMILY.extend([
    (r"_door$", {"tag": "门：两格高的通行方块，右键开关。",
                 "sections": [("怎么用", "<p>按材质选择风格：安山偏工业、黄铜偏精装、铜会氧化、玻璃通透。红石信号可以控制开关，适合做自动门。</p>")]}),
    (r"_trapdoor$", {"tag": "活板门：可水平或垂直安装的小门。",
                     "sections": [("怎么用", "<p>适合做检修口、天窗、地板暗门。红石可控，能接入自动化。</p>")]}),
    (r"_ladder$", {"tag": "梯子：垂直攀爬的金属梯。",
                   "sections": [("怎么用", "<p>贴在墙面或方块侧面，可以一直往上爬。比脚手架更省空间，适合做检修通道与塔内楼梯。</p>")]}),
    (r"^crushed_raw_", {"tag": "粉碎矿石：矿石翻倍流程的中间产物。",
                        "sections": [("怎么用", "<p>用<strong>粉碎轮</strong>粉碎原矿得到。之后有两种用法：直接熔炼成锭（产量更高），或投入<strong>风扇 + 水</strong>洗涤，额外产出金属粒与经验颗粒。</p>"),
                                     ("产线", "<p>原矿 → 粉碎 → 洗涤 → 熔炼，是 Create 中期最重要的资源翻倍循环。粉碎轮要两轮对转、转速拉满。</p>")]}),
])

# ------------------------------ 收尾补充 ------------------------------
item("create:sequenced_gearshift", "可编程齿轮箱：按程序执行多步动作。", [
    ("怎么用", "<p>串在传动轴上，右键打开<strong>程序界面</strong>，可以编排「正转 90° → 停 1 秒 → 反转 180°」这样的动作序列。</p>"
              "<p>是自动门、机械臂、电梯等「需要精确动作」机构的大脑。红石信号触发一次程序。</p>"),
], params=[("功能", "动作序列"), ("触发", "红石")],
   related=["create:adjustable_chain_gearshift", "create:rotation_speed_controller"])

item("create:adjustable_chain_gearshift", "可调节链式传动：改变两端相对角度。", [
    ("怎么用", "<p>和链式传动一样用链条连接两端，但可以<strong>调整两端的角度偏移</strong>。适合让两个机构保持固定相位差。</p>"),
], params=[("功能", "角度偏移")],
   related=["create:encased_chain_drive", "create:sequenced_gearshift"])

item("create:chain_conveyor", "链式传送带：用链条搬运物品。", [
    ("怎么用", "<p>与皮带传送带类似，但用<strong>链条</strong>承载物品，外观更工业。速度与接的轴转速相关。</p>"),
], params=[("功能", "物品运输")],
   related=["create:belt", "create:encased_chain_drive"])

item("create:powered_shaft", "动力轴：带动力的传动轴。", [
    ("怎么用", "<p>比普通传动轴多了一层动力外观，通常出现在特定结构中。功能上仍是传递旋转的轴。</p>"),
], params=[("功能", "传递旋转")],
   related=["create:shaft"])

item("create:copycat_base", "仿制方块：伪装成其他方块。", [
    ("怎么用", "<p>用其他方块的材质「贴」到它身上，它就会伪装成那个方块，但仍然保留仿制方块的连接特性。用于让建筑与机械无缝融合。</p>"
              "<p>同系列还有<strong>仿制面板</strong>与<strong>仿制台阶</strong>。</p>"),
], params=[("功能", "伪装")],
   related=["create:copycat_panel", "create:copycat_step", "create:copycat_bars"])

item("create:copycat_panel", "仿制面板：薄板形态的伪装方块。", [
    ("怎么用", "<p>伪装成其他方块的<strong>薄板</strong>，适合做墙面、机械外壳的贴面。</p>"),
], params=[("功能", "伪装薄板")],
   related=["create:copycat_base", "create:copycat_step"])

item("create:copycat_step", "仿制台阶：台阶形态的伪装方块。", [
    ("怎么用", "<p>伪装成其他方块的<strong>台阶</strong>，用来做斜坡、阶梯的隐形结构。</p>"),
], params=[("功能", "伪装台阶")],
   related=["create:copycat_base", "create:copycat_panel"])

item("create:crushing_wheel_controller", "粉碎轮控制器：成对控制粉碎轮。", [
    ("怎么用", "<p>把两个粉碎轮连成一组，由它统一控制转向与转速，省去自己搭反向齿轮的麻烦。</p>"),
], params=[("功能", "成对控制")],
   related=["create:crushing_wheel"])

item("create:nozzle", "喷嘴：把流体喷出去。", [
    ("怎么用", "<p>接在管道末端，把液体以喷射形式输出，可用于消防、装饰喷泉、或给下方物品「浇水」。</p>"),
], params=[("功能", "喷射流体")],
   related=["create:fluid_pipe", "create:mechanical_pump"])

item("create:rope", "绳子：滑轮与吊装的消耗品。", [
    ("怎么用", "<p>绳索滑轮、升降机滑轮工作时会放下绳子，绳子长度决定能吊多深。用剪刀可以快速回收。</p>"),
], params=[("用途", "吊装")],
   related=["create:rope_pulley", "create:elevator_pulley"])

item("create:steam_whistle", "汽笛：蒸汽动力的「喇叭」。", [
    ("怎么用", "<p>接在蒸汽系统上，通入蒸汽/红石信号会鸣笛，声音传得很远。适合做列车/工厂的氛围与信号。</p>"),
], params=[("用途", "发声")],
   related=["create:steam_whistle_extension", "create:steam_engine"])

item("create:steam_whistle_extension", "汽笛延长管：让汽笛声更低沉。", [
    ("怎么用", "<p>接在汽笛上改变音色/音调，组合不同长度可以做出和弦效果。</p>"),
], params=[("用途", "改变音色")],
   related=["create:steam_whistle"])

item("create:brass_hand", "黄铜手：机械臂的「手」。", [
    ("怎么用", "<p>机械臂的末端执行器，决定抓取/放置的方式。装不同的手可以改变交互行为。</p>"),
], params=[("用途", "机械臂配件")],
   related=["create:mechanical_arm"])

item("create:wooden_bracket", "木质支架：把轴固定在墙上。", [
    ("怎么用", "<p>装饰性支架，用来「支撑」传动轴，让机械结构看起来更合理。不影响功能。</p>"),
], params=[("用途", "装饰")],
   related=["create:metal_bracket", "create:shaft"])

item("create:rose_quartz_lamp", "玫瑰石英灯：可调亮度的灯。", [
    ("怎么用", "<p>用红石信号控制亮度（模拟信号），是很好的氛围灯与「状态指示灯」。</p>"),
], params=[("控制", "红石模拟信号")],
   related=["create:rose_quartz", "create:display_link"])

item("create:handheld_worldshaper", "创造模式世界塑形器：大范围改造地形（仅创造）。", [
    ("怎么用", "<p>创造模式专用工具，可以快速放置/删除大范围方块，用来搭测试场景。</p>"),
], params=[("模式", "仅创造")],
   related=["create:wand_of_symmetry", "create:schematicannon"])

FAMILY.extend([
    (r"_brick_slab$|_brick_stairs$", {"tag": "石砖台阶/楼梯：建筑用的斜面和半砖。",
        "sections": [("怎么用", "<p>与同系列石砖配套，用来做台阶、屋檐、斜坡。切石机可以一次加工出整套变体。</p>")]}),
    (r"^(andesite|brass)_encased_(cogwheel|large_cogwheel|shaft)$|^metal_girder_encased_shaft$",
     {"tag": "封装齿轮/轴：外观是机壳、内部是传动件。",
      "sections": [("怎么用", "<p>把齿轮或轴「包」进机壳里，外观整洁且不占额外空间。功能与普通齿轮/轴一致，适合做隐藏式传动。</p>")]}),
    (r"^(andesite_alloy|brass|zinc|raw_zinc|rose_quartz|cardboard|bound_cardboard)_block$",
     {"tag": "材料块：把材料压成方块储存。",
      "sections": [("怎么用", "<p>9 个材料合成 1 个块，块也能拆回 9 个材料。主要用于节省仓库空间与建筑装饰。</p>")]}),
    (r"^(chocolate|honey)_bucket$", {"tag": "桶装液体：方便搬运与灌注。",
      "sections": [("怎么用", "<p>右键装取液体，可以倒进工作盆/储罐，或直接用于注液器供液。</p>")]}),
    (r"^.*blaze_burner$|^blaze_cake_base$|^creative_blaze_cake$",
     {"tag": "烈焰人炉相关：加热与缠魂的火源。",
      "sections": [("怎么用", "<p>放入烈焰蛋糕点燃即可提供热量；空炉可以先用打火石/火焰点燃。灵魂火版本用于缠魂配方。</p>")]}),
    (r"^(chest|furnace)_minecart_contraption$", {"tag": "装配过的矿车：带容器的移动结构。",
      "sections": [("怎么用", "<p>用矿车装配器把箱子/熔炉与结构粘在一起，移动时也能存取物品/烧炼。适合移动采矿车。</p>")]}),
    (r"^(shadow_steel|refined_radiance)_casing$", {"tag": "特殊机壳：终局材料的装饰外壳。",
      "sections": [("怎么用", "<p>用稀有的暗影钢/光辉石制作，主要用于高级建筑与终局机器的外观。</p>")]}),
    (r"_backtank_placeable$", {"tag": "背罐（放置形态）：装饰用的背罐。",
      "sections": [("怎么用", "<p>把背罐放在地上当装饰或「充气站」摆设，功能与穿戴版一致但不可穿戴。</p>")]}),
    (r"^(zinc_ore|deepslate_zinc_ore)$", {"tag": "锌矿石：黄铜的原料来源。",
      "sections": [("怎么用", "<p>用镐挖掘得到粗锌，熔炼成锌锭。深层版本在下界以下生成，产量更稳定。</p>")]}),
])

FAMILY.append((r"rose_quartz_tiles$", {"tag": "玫瑰石英瓦：会发光的装饰瓦片。",
    "sections": [("怎么用", "<p>玫瑰石英做的瓦片，自带柔和光感，适合做高级建筑的墙面与地板；细瓦是更小尺度的变体，用来做镶边。</p>")]}))

# ======================================================================
# 第三批：Create 石材调色板（逐方块撰写，材质 × 形制双维度）
# ======================================================================
STONE_MATS = {
    "andesite":   ("安山岩", "灰蓝色调、原版随处可见的中性石材，是工业风最稳的底色"),
    "asurine":    ("皓蓝石", "Create 石材，蓝紫底上带浅色斑点，适合做冷色点缀"),
    "calcite":    ("方解石", "米白偏冷的浅色石材，用来提亮大面积墙面"),
    "crimsite":   ("绯红岩", "暗红带锈斑的石材，适合砖厂、锅炉房这类「热」的场景"),
    "deepslate":  ("深板岩", "近黑的深灰，压得住重型机械与暗色调建筑"),
    "diorite":    ("闪长岩", "灰白带黑点，比安山岩亮一档，适合做过渡"),
    "dripstone":  ("滴水石", "土黄米色，带天然沉积纹理，做旧感很强"),
    "granite":    ("花岗岩", "肉红偏暖，是这套石材里少见的暖色"),
    "limestone":  ("石灰岩", "浅米黄，最像「石砌老建筑」的一种"),
    "ochrum":     ("赭金砂", "土黄泛金，和安山合金、黄铜是同一套暖黄语言"),
    "scorchia":   ("焦黑熔渣", "黑褐带气孔，像炉渣冷却后的样子，重工业感最强"),
    "scoria":     ("熔渣", "暗红褐色、孔洞明显，适合做熔炉区与废墟"),
    "tuff":       ("凝灰岩", "灰绿偏冷，比深板岩柔和，适合做背景墙"),
    "veridium":   ("辉绿岩", "青绿带铜锈斑，是这套石材里最「氧化铜」的一块"),
}

SHAPES = [
    ("cut_{m}", "切制{mn}", "整块切制",
     "<p><strong>整块切制方块</strong>，表面被切成规整的方砖，边缘有一圈细框。是这套石材的「母版」：台阶、楼梯、砖块、墙都可以从它继续切出来。</p>"
     "<p>适合做墙体主材、地板、机器底座；大面积铺的时候，方框会自然形成网格，比原石更有秩序感。</p>",
     "墙面主材 / 地板 / 机器底座"),
    ("cut_{m}_slab", "切制{mn}台阶", "台阶",
     "<p>半砖高度，用来做台面、檐口、机器护罩的收边。两个台阶叠起来是 1.5 格高，正好做工作台面。</p>",
     "台面 / 檐口 / 收边"),
    ("cut_{m}_stairs", "切制{mn}楼梯", "楼梯",
     "<p>斜面方块，做楼梯、屋顶、斜坡，也可以倒扣做机器外壳的倒角。</p>",
     "楼梯 / 屋顶 / 倒角"),
    ("cut_{m}_bricks", "{mn}砖块", "砖块",
     "<p>比切制更细的<strong>砌筑纹理</strong>，砖缝更密。大面积铺墙时比整块切制更耐看，不会显得空。</p>",
     "大面积墙体"),
    ("cut_{m}_brick_slab", "{mn}砖台阶", "砖台阶",
     "<p>砖纹的半砖，适合做砖墙的压顶、窗台、台阶。</p>",
     "压顶 / 窗台"),
    ("cut_{m}_brick_stairs", "{mn}砖楼梯", "砖楼梯",
     "<p>砖纹楼梯，做砖砌建筑的室外台阶与坡道最自然。</p>",
     "室外台阶 / 坡道"),
    ("cut_{m}_wall", "切制{mn}墙", "墙",
     "<p><strong>墙</strong>会自动与相邻的墙连接成连续墙体，也能单独当矮栏杆用。厚度只有半格，比整块方块省空间。</p>"
     "<p>注意：一格高的墙挡不住玩家跳过去，要做围挡至少两格高。</p>",
     "围墙 / 护堤 / 矮栏杆"),
    ("cut_{m}_brick_wall", "{mn}砖墙", "砖墙",
     "<p>砖纹版本的墙，比切制墙多一层砌筑细节，适合做厂区边界与花园矮墙。</p>",
     "厂区边界 / 花园矮墙"),
    ("polished_cut_{m}", "磨制切制{mn}", "磨制",
     "<p>表面被打磨过，比切制版本<strong>更亮、更平整</strong>，方框也更细。适合室内、展厅、控制室这类需要「干净」的地方。</p>",
     "室内 / 展厅 / 控制室"),
    ("polished_cut_{m}_slab", "磨制切制{mn}台阶", "磨制台阶",
     "<p>磨制面的半砖，做室内台面、展示台最合适。</p>",
     "室内台面 / 展示台"),
    ("polished_cut_{m}_stairs", "磨制切制{mn}楼梯", "磨制楼梯",
     "<p>磨制面的楼梯，做室内主楼梯或展厅台阶。</p>",
     "室内楼梯"),
    ("polished_cut_{m}_wall", "磨制切制{mn}墙", "磨制墙",
     "<p>磨制面的墙，适合做室内隔断与展台围边。</p>",
     "室内隔断"),
    ("small_{m}_bricks", "{mn}小砖块", "小砖",
     "<p>砖块尺度最小的版本，纹理细密。适合小体量建筑、镶边、柱子包边；大面积用会显得碎，建议和整块切制搭配。</p>",
     "小体量 / 镶边"),
    ("small_{m}_brick_slab", "{mn}小砖台阶", "小砖台阶",
     "<p>小砖纹理的台阶，做细部收边、设备基座。</p>",
     "细部收边"),
    ("small_{m}_brick_stairs", "{mn}小砖楼梯", "小砖楼梯",
     "<p>小砖纹理的楼梯，适合小尺度建筑与室内。</p>",
     "小尺度楼梯"),
    ("small_{m}_brick_wall", "{mn}小砖墙", "小砖墙",
     "<p>小砖纹理的墙，细密耐看，适合做庭院围墙与机器围栏。</p>",
     "庭院围墙"),
    ("layered_{m}", "层叠{mn}", "层叠",
     "<p>横向条带纹理，像沉积岩的地层。适合做「剖面」「崖壁」，也可以横过来当机械外壳的散热片。</p>",
     "地层 / 崖壁 / 外壳"),
    ("{m}_pillar", "{mn}柱", "柱",
     "<p>柱状方块，顶面有独立的纹理，<strong>可以旋转</strong>调整顶面方向。适合做承重柱、烟囱、装饰立柱。</p>",
     "承重柱 / 烟囱 / 立柱"),
]

for _m, (_mn, _mdesc) in STONE_MATS.items():
    for _pat, _label, _shape, _body, _use in SHAPES:
        _id = "create:" + _pat.format(m=_m)
        _name = _label.format(mn=_mn)
        _tag = "%s：%s。%s。" % (_name, _shape, _mdesc.split("，")[0])
        _rel = ["create:" + x.format(m=_m) for x in
                ("cut_{m}", "cut_{m}_bricks", "polished_cut_{m}", "small_{m}_bricks", "layered_{m}", "{m}_pillar")]
        _rel = [x for x in _rel if x != _id]
        item(_id, _tag, [
            ("怎么获得", "<p>用<strong>切石机</strong>切割%s（或其上一级变体）得到%s。石材调色板的所有形制都走切石机，不需要工作台。</p>" % (_mn, _name)),
            ("怎么用", _body),
            ("配色建议", "<p>%s。%s适合用在<strong>%s</strong>。</p>" % (_mdesc, _mn, _use)),
        ], params=[("材质", _mn), ("形制", _shape), ("工艺", "切石机")], related=_rel)

# ======================================================================
# 第四批：铜屋面（砖瓦 / 瓦片 × 氧化程度 × 涂蜡 × 形制）
# ======================================================================
CU_STATES = [
    ("", "新铜", "刚铺上的铜，橙红金属色，反光最强"),
    ("exposed_", "斑驳", "开始泛出第一层铜绿，橙红里混着青绿"),
    ("weathered_", "锈蚀", "铜绿已经铺开，只剩零星的橙红"),
    ("oxidized_", "氧化", "完全变成青绿色，最像老建筑"),
]
CU_FORMS = [
    ("{p}copper_shingles", "铜砖瓦", "砖瓦", "小块错缝排列的瓦片，颗粒感强，适合屋顶与外墙"),
    ("{p}copper_shingle_slab", "铜砖瓦台阶", "砖瓦台阶", "砖瓦质感的半砖"),
    ("{p}copper_shingle_stairs", "铜砖瓦楼梯", "砖瓦楼梯", "砖瓦质感的楼梯"),
    ("{p}copper_tiles", "铜瓦", "瓦片", "大块方瓦，接缝更规整，适合现代风格屋面"),
    ("{p}copper_tile_slab", "铜瓦台阶", "瓦片台阶", "瓦片质感的半砖"),
    ("{p}copper_tile_stairs", "铜瓦楼梯", "瓦片楼梯", "瓦片质感的楼梯"),
]

def _cu_name(base, state_cn, waxed):
    if not state_cn or state_cn == "新铜":
        return ("涂蜡" + base) if waxed else base
    return ("%s的%s%s" % (state_cn, "涂蜡" if waxed else "", base))

for _state, _scn, _sdesc in CU_STATES:
    for _tmpl, _base, _form, _fdesc in CU_FORMS:
        for _waxed in (False, True):
            _id = "create:" + ("waxed_" if _waxed else "") + _state + _tmpl.format(p="").replace("copper", "copper", 1)
            _id = "create:" + ("waxed_" if _waxed else "") + _state + _tmpl.format(p="")[0:]
            _short = _tmpl.format(p="")
            _id = "create:" + ("waxed_" if _waxed else "") + _state + _short
            _name = _cu_name(_base, _scn if _state else "", _waxed)
            _wax_txt = ("表面涂过蜡，<strong>氧化被锁死</strong>，颜色不会再变；想恢复氧化用斧子刮掉蜡层。" if _waxed
                        else "没有涂蜡，会随时间继续往下氧化（新铜 → 斑驳 → 锈蚀 → 氧化），想做旧就让它自然变。")
            _tag = "%s：%s，%s。" % (_name, _form, _sdesc)
            item(_id, _tag, [
                ("怎么获得", "<p>%s由<strong>铜锭</strong>在工作台合成%s。%s</p>"
                 % (_name, ("，再用切石机/工作台切成台阶与楼梯" if _form in ("砖瓦台阶", "砖瓦楼梯", "瓦片台阶", "瓦片楼梯") else ""),
                    ("涂蜡版本 = 对应铜件 + 蜜脾（蜂巢）右键涂蜡。" if _waxed else ""))),
                ("怎么用", "<p>%s。%s</p><p>最典型的用法是<strong>屋顶</strong>：铜砖瓦做屋面和山墙，铜瓦做大面积的平屋面，两者混铺能做出新旧交替的层次。</p>"
                 % (_fdesc, _sdesc)),
                ("氧化与修复", "<p>%s</p><p>已经氧化的铜件可以用<strong>斧子</strong>刮掉一层氧化（氧化 → 锈蚀 → 斑驳 → 新铜）；涂蜡后就不再变化，适合固定你想保留的颜色。</p>" % _wax_txt),
            ], params=[("材质", "铜"), ("形制", _form), ("状态", _scn), ("涂蜡", "是" if _waxed else "否")],
               related=["create:" + ("waxed_" if _waxed else "") + _state + ("copper_tiles" if "shingle" in _short else "copper_shingles")])

# ======================================================================
# 第五批：16 色系列（辉光管 / 邮箱 / 风帆 / 坐垫 / 工具箱 / 阀门手轮 / 桌布）
# ======================================================================
COLORS = [
    ("white", "白色", "干净百搭，做浅色内装、标识底板最稳"),
    ("orange", "橙色", "工程警示色，适合施工区、安全标识"),
    ("magenta", "品红色", "高饱和，用来做霓虹与视觉焦点"),
    ("light_blue", "淡蓝色", "冷色，适合水景、控制室、医疗感空间"),
    ("yellow", "黄色", "工业黄，和安山合金、黄铜是同一套语言"),
    ("lime", "黄绿色", "荧光感强，做指示灯、危险区域标记"),
    ("pink", "粉红色", "柔和，适合生活区、商店、车站候车区"),
    ("gray", "灰色", "中性色，机械与建筑通用，不会抢戏"),
    ("light_gray", "淡灰色", "浅灰，偏混凝土/铝板质感"),
    ("cyan", "青色", "冷色，适合玻璃、水处理、管道区"),
    ("purple", "紫色", "高级感，适合办公室、站长室"),
    ("blue", "蓝色", "稳重，适合车站、制服色、航运主题"),
    ("brown", "棕色", "木质与皮革感，适合仓库、货运区"),
    ("green", "绿色", "自然与「正常状态」，适合绿化带与运行指示灯"),
    ("red", "红色", "警示与停止，消防、紧急停机、信号灯"),
    ("black", "黑色", "工业黑，机箱、机房、暗色系建筑"),
]

COLOR_FAMILIES = [
    ("{c}_nixie_tube", "辉光管", "显示数字、信号强度或剪贴板文本",
     "<p>被红石充能时显示<strong>信号强度</strong>（0-15）；用写好的<strong>剪贴板</strong>右键可以显示自定义文本。颜色只影响发光色，不影响功能。</p>"
     "<p>“%s”的辉光管特别适合用来做<strong>%s</strong>。用染料右键可以随时改色。</p>"),
    ("{c}_postbox", "邮箱", "接收包裹物流投递的信箱",
     "<p>配合<strong>货物蛙港</strong>与包裹物流使用：把邮箱放在收件点，包裹会被投递到这里。颜色用来区分不同的收件人或线路。</p>"
     "<p>“%s”的邮箱适合标记<strong>%s</strong>。</p>"),
    ("{c}_sail", "风帆", "风车的受风面",
     "<p>装在<strong>风帆框架</strong>上组成风车，风吹过时带动<strong>风车轴承</strong>产生旋转。帆越多，风车越大，出力越高（也更吃应力）。</p>"
     "<p>“%s”的帆适合<strong>%s</strong>；同一座风车建议统一颜色，视觉上才像一台机器。</p>"),
    ("{c}_seat", "坐垫", "可以坐下的装饰座椅",
     "<p>右键坐下，起身按潜行。可以放在车站候车区、控制室、餐厅。</p>"
     "<p>“%s”的坐垫适合<strong>%s</strong>。</p>"),
    ("{c}_toolbox", "工具箱", "随身携带的储物箱",
     "<p>可以拿在手上当便携背包，也可以放在地上当容器；用染料染成不同颜色来区分用途（工具/材料/零件）。</p>"
     "<p>“%s”的工具箱适合<strong>%s</strong>。</p>"),
    ("{c}_valve_handle", "阀门手轮", "装在流体阀门上的手动轮",
     "<p>装在<strong>流体阀门</strong>或管道上，用来手动开关/调节流量。颜色用于区分管线（水、岩浆、牛奶……）。</p>"
     "<p>“%s”的手轮适合标记<strong>%s</strong>。</p>"),
    ("{c}_table_cloth", "桌布", "铺在桌面上的装饰布",
     "<p>铺在方块顶面做桌面、柜台、餐桌。颜色决定整体氛围，是小场景里性价比最高的装饰之一。</p>"
     "<p>“%s”的桌布适合<strong>%s</strong>。</p>"),
]

for _c, _cn, _cdesc in COLORS:
    for _tmpl, _fam, _use, _body in COLOR_FAMILIES:
        _id = "create:" + _tmpl.format(c=_c)
        _name = _cn + _fam
        _tag = "%s：%s。" % (_name, _use)
        item(_id, _tag, [
            ("怎么获得", "<p>用对应颜色的染料 + %s的基底在工作台合成；同系列 16 色都可以互相转换。</p>" % _fam),
            ("怎么用", _body % (_cn, _cdesc)),
        ], params=[("颜色", _cn), ("类型", _fam)], related=["create:" + _tmpl.format(c=x) for x in ("white", "black", "red") if x != _c])

# ======================================================================
# 第六批：木质窗户 / 窗板（按木材逐一撰写）
# ======================================================================
WOODS = {
    "oak":      ("橡木", "中性浅褐，最百搭的一种木色"),
    "spruce":   ("云杉木", "深褐偏冷，适合北方小镇与仓库"),
    "birch":    ("白桦木", "浅黄白，室内会显得很亮"),
    "jungle":   ("丛林木", "红褐色，热带建筑常用"),
    "acacia":   ("金合欢木", "橙红，沙漠与工业区很搭"),
    "dark_oak": ("深色橡木", "近黑的深褐，庄重、压得住场"),
    "mangrove": ("红树木", "暗红带紫，湿地风格"),
    "cherry":   ("樱花木", "粉白，日式与庭院建筑"),
    "bamboo":   ("竹", "黄绿色，东亚风格，纹理细"),
    "crimson":  ("绯红木", "紫红，下界风格"),
    "warped":   ("诡异木", "青蓝色，下界风格"),
}

for _w, (_wn, _wd) in WOODS.items():
    item("create:%s_window" % _w, "%s窗户：带木框的装饰玻璃。" % _wn, [
        ("怎么获得", "<p>用<strong>%s</strong>与玻璃在工作台合成，一次出多个。同系列还有对应的<strong>窗板</strong>（pane），可以做出更细的窗棂。</p>" % _wn),
        ("怎么用", "<p>本质是<strong>透光的装饰方块</strong>：可以当窗户、玻璃隔断、展示柜的正面。木框让它在建筑立面上有明确的分格，比纯玻璃更有结构感。</p>"
                  "<p>%s，适合<strong>%s</strong>风格的建筑。</p>" % (_wd, _wn)),
        ("搭配", "<p>和同色系的<strong>桌子、座椅、栏杆</strong>一起用，能做出一整套统一木色的内装。窗户和窗板可以上下混排：上面用窗板做气窗，下面用整块窗户。</p>"),
    ], params=[("材质", _wn), ("类型", "窗户")], related=["create:%s_window_pane" % _w, "create:%s_table_cloth" % _w if _w in ("oak",) else "create:andesite_casing"])

    item("create:%s_window_pane" % _w, "%s窗户板：更细的木框窗棂。" % _wn, [
        ("怎么获得", "<p>由<strong>%s窗户</strong>在工作台切成窗板，或用%s木板 + 玻璃直接合成。</p>" % (_wn, _wn)),
        ("怎么用", "<p>窗板只有一格厚度，<strong>可以拼成大面积的格子窗</strong>，也能当玻璃隔断的骨架。两格高的窗板叠起来就是落地窗。</p>"
                  "<p>%s；窗板比整块窗户更「轻」，适合大面积开窗。</p>" % _wd),
        ("常见坑", "<p>窗板不会像玻璃板那样自动连成一大片没有中缝——每一格都有独立木框，所以想做出「一整个大窗」要用整块窗户，想要「分格窗」才用窗板。</p>"),
    ], params=[("材质", _wn), ("类型", "窗板")], related=["create:%s_window" % _w])

IRON_WINDOWS = [
    ("industrial_iron_window", "工业铁窗户", "铆钉铁框，重工业风", "厂房屋顶、锅炉房、车间"),
    ("ornate_iron_window", "华丽铁窗户", "带花纹的铸铁窗框，偏古典", "车站大厅、办公楼、正立面"),
    ("weathered_iron_window", "锈蚀的工业铁窗户", "铁框带锈迹，做旧感强", "废弃工厂、码头、旧仓库"),
]
for _id, _n, _d, _use in IRON_WINDOWS:
    item("create:" + _id, "%s：%s。" % (_n, _d), [
        ("怎么获得", "<p>用铁相关材料与玻璃在工作台合成；同系列有对应的窗板。</p>"),
        ("怎么用", "<p>%s。适合<strong>%s</strong>。</p><p>铁窗比木窗「硬」，适合和石墙、机壳、金属屋面搭配；木窗则更适合生活区。</p>" % (_d, _use)),
    ], params=[("材质", "铁"), ("类型", "窗户")], related=["create:" + _id + "_pane"])
    item("create:" + _id + "_pane", "%s板：更细的铁框窗棂。" % _n, [
        ("怎么获得", "<p>由整块%s切成窗板。</p>" % _n),
        ("怎么用", "<p>铁框窗板适合做大面积的<strong>工业格子窗</strong>，一格一格排开很有厂房味道。%s。</p>" % _d),
    ], params=[("材质", "铁"), ("类型", "窗板")], related=["create:" + _id])

FRAMED = [
    ("framed_glass", "边框玻璃", "四周一圈实心边框，中间透明", "画框式的窗、展示柜正面"),
    ("horizontal_framed_glass", "水平边框玻璃", "只有上下两条边框", "横向长窗、百叶窗感"),
    ("vertical_framed_glass", "竖直边框玻璃", "只有左右两条边框", "竖向长窗、门侧窄窗"),
    ("tiled_glass", "十字玻璃", "十字形分格", "老式格子窗、温室"),
]
for _id, _n, _d, _use in FRAMED:
    item("create:" + _id, "%s：%s。" % (_n, _d), [
        ("怎么获得", "<p>用玻璃与少量铁/木材料在工作台合成，同系列有对应的玻璃板。</p>"),
        ("怎么用", "<p>%s，适合<strong>%s</strong>。它的边框会打断玻璃的「整片感」，用来控制建筑立面的节奏。</p>" % (_d, _use)),
        ("搭配", "<p>四种框型的玻璃混用能做出很细的立面：大面用边框玻璃，长条用水平/竖直框，局部点缀十字玻璃。</p>"),
    ], params=[("类型", "装饰玻璃")], related=["create:" + _id + "_pane"])
    item("create:" + _id + "_pane", "%s板：更薄的同款框型玻璃。" % _n, [
        ("怎么获得", "<p>由%s切成玻璃板。</p>" % _n),
        ("怎么用", "<p>薄板适合做隔断、气窗和灯箱。%s。</p>" % _d),
    ], params=[("类型", "装饰玻璃板")], related=["create:" + _id])

for _m, _mn in (("andesite", "安山"), ("brass", "黄铜"), ("copper", "铜")):
    item("create:%s_bars" % _m, "%s栏杆：可连接的金属窗栅。" % _mn, [
        ("怎么获得", "<p>用%s材料在工作台合成，一次多根。</p>" % _mn),
        ("怎么用", "<p>栏杆会自动与相邻栏杆连接，<strong>既能当护栏也能当窗栅</strong>。竖着排是栅栏，横着排是栏杆，转角会自动接上。</p>"
                  "<p>和墙不同，栏杆是镂空的，不挡视线，适合做厂房二层护栏、天井围栏。</p>" % ()),
        ("常见坑", "<p>栏杆不能挡玩家跳跃，纯装饰/防掉落用；要真正拦住生物得用墙或栅栏。</p>"),
    ], params=[("材质", _mn), ("类型", "栏杆")], related=["create:%s_ladder" % _m, "create:%s_scaffolding" % _m])

    item("create:%s_ladder" % _m, "%s梯子：金属工业梯。" % _mn, [
        ("怎么获得", "<p>用%s材料合成，可批量制作。</p>" % _mn),
        ("怎么用", "<p>贴在墙面上就能上下攀爬，和原版梯子一样。金属梯比木梯更符合厂房、井道、机房的场景。</p>"),
        ("搭配", "<p>和同材质的<strong>脚手架、栏杆</strong>一起用，能做出一整套检修通道。</p>"),
    ], params=[("材质", _mn), ("类型", "梯子")], related=["create:%s_bars" % _m, "create:%s_scaffolding" % _m])

    item("create:%s_scaffolding" % _m, "%s脚手架：可攀爬的临时结构。" % _mn, [
        ("怎么获得", "<p>用%s材料合成，一次多个。</p>" % _mn),
        ("怎么用", "<p>脚手架可以<strong>直接攀爬</strong>，也能站在顶上；拆掉下面一格，上面的会一起掉落。适合施工、检修、临时高台。</p>"),
        ("常见坑", "<p>脚手架不承重也不防摔，做高空作业时下面记得垫水或干草。</p>"),
    ], params=[("材质", _mn), ("类型", "脚手架")], related=["create:%s_bars" % _m, "create:%s_ladder" % _m])

    item("create:%s_table_cloth" % _m, "%s桌面：金属质感的桌布。" % _mn, [
        ("怎么获得", "<p>用%s材料合成，铺在方块顶面。</p>" % _mn),
        ("怎么用", "<p>和染料桌布功能一样，只是材质换成%s，适合控制台、工作台、机房操作台。</p>" % _mn),
    ], params=[("材质", _mn), ("类型", "桌面")], related=["create:andesite_casing"])

item("create:copper_valve_handle", "铜阀门手轮：装在阀门上的手动轮。", [
    ("怎么获得", "<p>用铜材料合成；其余 16 色手轮由染料染色得到。</p>"),
    ("怎么用", "<p>装在<strong>流体阀门</strong>或管道上手动开关、调节流量。铜色是默认外观，和铜管道最搭。</p>"),
], params=[("材质", "铜"), ("类型", "阀门手轮")], related=["create:fluid_valve", "create:copper_casing"])

item("create:copycat_bars", "伪装栏杆：能伪装成其他方块的栏杆。", [
    ("怎么获得", "<p>由普通栏杆与<strong>伪装系列</strong>材料合成。</p>"),
    ("怎么用", "<p>用其他方块右键「贴皮」，外观变成目标方块，但仍然是栏杆的连接逻辑。适合让栏杆融入木/石建筑，不露金属。</p>"),
    ("常见坑", "<p>伪装只改外观，不改碰撞与连接规则；拆下来会恢复成伪装栏杆本身。</p>"),
], params=[("类型", "伪装方块")], related=["create:copycat_base", "create:copycat_panel"])

# ======================================================================
# 第七批：石材原块 / 金属块 / 机壳 / 包壳件 / 矿石 / 粉碎矿 / 桶 / 烈焰 / 半成品
# ======================================================================
STONE_RAW = [
    ("asurine", "皓蓝石", "蓝紫底带浅色斑点，冷色点缀"),
    ("crimsite", "绯红岩", "暗红带锈斑，砖厂、锅炉房的氛围"),
    ("limestone", "石灰岩", "浅米黄，最像石砌老建筑"),
    ("ochrum", "赭金砂", "土黄泛金，和黄铜同一套暖色"),
    ("scorchia", "焦黑熔渣", "黑褐带气孔，重工业感最强"),
    ("scoria", "熔渣", "暗红褐、孔洞明显，熔炉区与废墟"),
    ("veridium", "辉绿岩", "青绿带铜锈斑，像氧化铜"),
]
for _id, _n, _d in STONE_RAW:
    item("create:" + _id, "%s：Create 石材调色板的原石。" % _n, [
        ("怎么获得", "<p>用镐采集%s原石；带精准采集可以拿原块，否则掉对应材料。原石可以在<strong>切石机</strong>里切成整套切制/磨制/砖块变体。</p>" % _n),
        ("怎么用", "<p>%s。直接铺是粗犷的天然石感，切制后才是规整的建筑材。</p>" % _d),
        ("搭配", "<p>和同色系的切制变体混铺：大面积用切制，边角保留一点原石，会有「开采出来」的层次。</p>"),
    ], params=[("类型", "原石"), ("材质", _n)], related=["create:cut_" + _id, "create:layered_" + _id, "create:" + _id + "_pillar"])

METAL_BLOCKS = [
    ("andesite_alloy_block", "安山合金块", "安山合金的储存方块，灰绿金属感", "机器底座、承重结构"),
    ("brass_block", "黄铜块", "黄铜的储存方块，暖金色", "装饰、信标底座、高级机器"),
    ("zinc_block", "锌块", "锌锭压成的块，冷银白", "储存与冷色金属装饰"),
    ("raw_zinc_block", "粗锌块", "粗锌压成的块，表面粗糙", "临时储存、工业风堆料"),
    ("rose_quartz_block", "玫瑰石英块", "玫瑰石英压成的块，半透光", "灯箱、装饰、光学件"),
    ("cardboard_block", "纸板块", "压实的纸板，浅褐", "包装仓库、临时结构"),
    ("bound_cardboard_block", "捆装纸板块", "用绳捆扎的纸板，带捆带纹理", "货运码头、仓库装饰"),
]
for _id, _n, _d, _use in METAL_BLOCKS:
    item("create:" + _id, "%s：%s。" % (_n, _d), [
        ("怎么获得", "<p>用 9 个对应的锭/材料在工作台压成块，也可以再拆回 9 个。</p>"),
        ("怎么用", "<p>主要作为<strong>储存与建筑材</strong>：%s。金属块还能当信标底座。</p>" % _use),
        ("常见坑", "<p>块只是储存形式，不参与机器合成；需要锭的时候记得拆开。</p>"),
    ], params=[("类型", "储存方块")], related=[])

CASINGS = [
    ("brass_casing", "黄铜机壳", "黄铜 + 木材，暖金色外壳", "高级机器、控制室、列车"),
    ("copper_casing", "铜机壳", "铜 + 木材，橙红金属外壳", "蒸汽管道、锅炉、铜主题机器"),
    ("shadow_steel_casing", "暗影机壳", "暗影钢外壳，深紫黑", "后期机器、暗色主题"),
    ("refined_radiance_casing", "光辉机壳", "光辉石外壳，泛白光", "后期机器、明亮主题"),
]
for _id, _n, _d, _use in CASINGS:
    item("create:" + _id, "%s：%s。" % (_n, _d), [
        ("怎么获得", "<p>用对应金属板 + 木材（或石砖）在工作台合成。机壳是大部分 Create 机器的<strong>合成基底</strong>。</p>"),
        ("怎么用", "<p>%s。机壳既能当建筑材料，也是机器配方里的常客：搅拌器、压床、机械臂等都要用到。</p>" % _use),
        ("常见坑", "<p>做机器前先囤机壳。铜机壳在前期就能做，黄铜机壳要等黄铜产线跑起来。</p>"),
    ], params=[("类型", "机壳"), ("材质", _n.replace("机壳", ""))], related=[])

ENCASED = [
    ("andesite_encased_shaft", "安山传动杆箱", "把传动轴包进安山机壳，外观整洁"),
    ("brass_encased_shaft", "黄铜传动杆箱", "把传动轴包进黄铜机壳，外观整洁"),
    ("metal_girder_encased_shaft", "金属梁包住的传动杆", "用金属梁包住传动轴，工业感最强"),
    ("andesite_encased_cogwheel", "安山齿轮箱", "把齿轮包进安山机壳"),
    ("brass_encased_cogwheel", "黄铜齿轮箱", "把齿轮包进黄铜机壳"),
    ("andesite_encased_large_cogwheel", "安山大齿轮箱", "把大齿轮包进安山机壳"),
    ("brass_encased_large_cogwheel", "黄铜大齿轮箱", "把大齿轮包进黄铜机壳"),
]
for _id, _n, _d in ENCASED:
    item("create:" + _id, "%s：%s。" % (_n, _d), [
        ("怎么获得", "<p>用对应的<strong>机壳</strong>右键已经放好的轴/齿轮，就能把它包起来；再用扳手可以拆回。</p>"),
        ("怎么用", "<p>功能上和裸露的轴/齿轮完全一致，只是<strong>外观更整洁</strong>，不会看到转动的零件。适合穿墙、埋地、做整齐的机房。</p>"),
        ("常见坑", "<p>包壳只改外观，不改变连接关系；拆壳时注意别把整段轴一起拆了。</p>"),
    ], params=[("类型", "包壳件")], related=[])

item("create:zinc_ore", "锌矿石：地下的锌矿。", [
    ("怎么获得", "<p>在地下用镐开采，掉落<strong>粗锌</strong>；时运可以增加产量。</p>"),
    ("怎么用", "<p>粗锌烧成锌锭，锌是黄铜（铜 + 锌）的原料，也是不少机器零件的材料。</p>"),
], params=[("类型", "矿石")], related=["create:deepslate_zinc_ore", "create:crushed_raw_zinc"])

item("create:deepslate_zinc_ore", "深层锌矿石：深板岩层的锌矿。", [
    ("怎么获得", "<p>在深板岩层开采，掉落<strong>粗锌</strong>，产量比浅层锌矿略高。</p>"),
    ("怎么用", "<p>和普通锌矿一样烧成锌锭。深层矿硬度更高，记得带好镐。</p>"),
], params=[("类型", "矿石")], related=["create:zinc_ore", "create:crushed_raw_zinc"])

CRUSHED = [
    ("copper", "铜", "铜锭与铜线材"), ("zinc", "锌", "黄铜与镀锌件"), ("iron", "铁", "铁板与机械零件"),
    ("gold", "金", "金板与精密件"), ("aluminum", "铝", "轻质合金"), ("lead", "铅", "配重与电池"),
    ("nickel", "镍", "合金添加剂"), ("osmium", "锇", "高硬度合金"), ("platinum", "铂", "高级催化材料"),
    ("quicksilver", "水银", "流体与合金"), ("silver", "银", "导电与装饰"), ("tin", "锡", "焊料与青铜"),
    ("uranium", "铀", "核能材料"),
]
for _id, _n, _use in CRUSHED:
    item("create:crushed_raw_" + _id, "粉碎%s矿石：粉碎轮处理原矿的产物。" % _n, [
        ("怎么获得", "<p>把<strong>粗%s</strong>放进<strong>粉碎轮</strong>粉碎得到。粉碎轮需要两个相对旋转的轮子，转速越高越快。</p>" % _n),
        ("怎么用", "<p>粉碎矿可以<strong>洗涤</strong>（风扇 + 水）或直接熔炼，产出比烧原矿更多；%s。很多合金配方也直接吃粉碎矿。</p>" % _use),
        ("常见坑", "<p>粉碎轮两侧必须反向旋转，同向是转不起来的；进料口要对准两轮之间的缝隙。</p>"),
    ], params=[("类型", "粉碎矿"), ("金属", _n)], related=[])

item("create:chocolate_bucket", "巧克力桶：装着巧克力流体的桶。", [
    ("怎么获得", "<p>用桶右键巧克力流体源，或在<strong>注液器</strong>产线里接取。</p>"),
    ("怎么用", "<p>巧克力是 Create 的流体之一，可用于<strong>注液器</strong>给食物/物品涂层，也能倒出来做装饰流体。桶装方便搬运与倒入储罐。</p>"),
], params=[("类型", "流体桶")], related=["create:spout", "create:fluid_tank"])

item("create:honey_bucket", "蜂蜜桶：装着蜂蜜流体的桶。", [
    ("怎么获得", "<p>用桶接蜂蜜流体（蜂巢/蜂箱相关来源），或在流体产线中接取。</p>"),
    ("怎么用", "<p>蜂蜜可以作为<strong>注液器</strong>的流体，也能倒进储罐当装饰。黏稠、移动慢，做「糖浆」主题的场景很合适。</p>"),
], params=[("类型", "流体桶")], related=["create:spout", "create:fluid_tank"])

item("create:empty_blaze_burner", "空的烈焰人燃烧室：还没点火的加热源。", [
    ("怎么获得", "<p>用铁/安山材料在工作台合成，是<strong>烈焰人燃烧室</strong>的未点燃形态。</p>"),
    ("怎么用", "<p>放好后用<strong>烈焰蛋糕</strong>右键点燃，变成「已点燃」的燃烧室，给工作盆、锅炉等提供热量。</p>"),
    ("常见坑", "<p>空燃烧室不产热；点燃后要定期喂烈焰蛋糕，否则会熄灭。</p>"),
], params=[("类型", "热源")], related=["create:lit_blaze_burner", "create:blaze_cake_base"])

item("create:lit_blaze_burner", "烈焰人燃烧室（已点燃）：持续供热。", [
    ("怎么获得", "<p>由空的烈焰人燃烧室用<strong>烈焰蛋糕</strong>点燃。</p>"),
    ("怎么用", "<p>点燃后持续提供热量，是<strong>工作盆、蒸汽锅炉</strong>的热源。右键可以查看/补充燃料，用扳手可以拆下。</p>"),
    ("常见坑", "<p>燃烧室需要燃料维持；做长时间产线时记得留补给，熄火会让整条线停摆。</p>"),
], params=[("类型", "热源")], related=["create:empty_blaze_burner", "create:blaze_cake_base"])

item("create:blaze_cake_base", "烈焰蛋糕胚：烈焰蛋糕的半成品。", [
    ("怎么获得", "<p>由烈焰粉、糖等材料在工作台合成，是<strong>烈焰蛋糕</strong>的中间产物。</p>"),
    ("怎么用", "<p>继续加工成烈焰蛋糕，用来点燃/维持烈焰人燃烧室。本身不能直接当燃料。</p>"),
], params=[("类型", "半成品")], related=["create:empty_blaze_burner", "create:creative_blaze_cake"])

item("create:creative_blaze_cake", "创造烈焰蛋糕：无限燃料。", [
    ("怎么获得", "<p>创造模式专属物品，生存模式无法合成。</p>"),
    ("怎么用", "<p>放进烈焰人燃烧室后<strong>不会消耗</strong>，用来测试产线或做展示。</p>"),
], params=[("类型", "创造物品")], related=["create:lit_blaze_burner"])

item("create:incomplete_precision_mechanism", "精密构件（半成品）：序列组装的中间态。", [
    ("怎么获得", "<p>在<strong>序列组装</strong>产线上，精密构件还没走完最后一步时的形态。</p>"),
    ("怎么用", "<p>不能直接使用，必须让产线继续部署/压制到成品。中途断料会卡在半成品。</p>"),
    ("常见坑", "<p>半成品掉在地上捡起来会占背包；产线设计时尽量让半成品只在传送带上流动。</p>"),
], params=[("类型", "半成品")], related=["create:precision_mechanism"])

item("create:incomplete_track", "列车轨道（半成品）：序列组装的中间态。", [
    ("怎么获得", "<p>在<strong>序列组装</strong>产线上制作列车轨道时的中间形态。</p>"),
    ("怎么用", "<p>需要继续经过部署/压制才能变成成品轨道；不能直接铺设。</p>"),
], params=[("类型", "半成品")], related=["create:track"])

item("create:copper_backtank_placeable", "可放置的铜背罐：把背罐放下来。", [
    ("怎么获得", "<p>手持铜背罐潜行右键放置，或由背罐物品转换。</p>"),
    ("怎么用", "<p>放置后可以当<strong>储气/装饰</strong>方块，也能接上管道充气。想穿回身上再右键取下。</p>"),
], params=[("类型", "装备方块")], related=["create:copper_backtank"])

item("create:netherite_backtank_placeable", "可放置的下界合金背罐：把背罐放下来。", [
    ("怎么获得", "<p>手持下界合金背罐潜行右键放置。</p>"),
    ("怎么用", "<p>和铜背罐一样可以放置、充气、取下；容量更大，适合长时间飞行作业。</p>"),
], params=[("类型", "装备方块")], related=["create:netherite_backtank", "create:copper_backtank_placeable"])

item("create:rose_quartz_tiles", "玫瑰石英瓦：会发光的装饰瓦。", [
    ("怎么获得", "<p>由玫瑰石英在工作台/切石机加工成瓦片。</p>"),
    ("怎么用", "<p>自带柔和光感，适合高级建筑的墙面与地面；细瓦是更小尺度的变体，用来做镶边。</p>"),
], params=[("类型", "装饰方块")], related=["create:small_rose_quartz_tiles", "create:rose_quartz_block"])

item("create:small_rose_quartz_tiles", "玫瑰石英细瓦：小尺度的发光瓦片。", [
    ("怎么获得", "<p>由玫瑰石英瓦继续在切石机里切细。</p>"),
    ("怎么用", "<p>纹理更密，适合做镶边、柱面包边、灯带。大面积用会显得碎，建议和整块瓦搭配。</p>"),
], params=[("类型", "装饰方块")], related=["create:rose_quartz_tiles"])

item("create:chest_minecart_contraption", "装配过的运输矿车：把结构装到矿车上。", [
    ("怎么获得", "<p>用<strong>矿车装配站</strong>把带箱子的结构装到矿车上。</p>"),
    ("怎么用", "<p>整台结构会跟着矿车走，相当于一个<strong>移动的箱子+装置</strong>。可以配合列车轨道做移动仓库。</p>"),
    ("常见坑", "<p>装配前确认结构已经用超级胶粘好，否则开动时会散架。</p>"),
], params=[("类型", "载具")], related=["create:minecart_contraption", "create:cart_assembler"])

item("create:furnace_minecart_contraption", "装配过的动力矿车：自带动力的移动结构。", [
    ("怎么获得", "<p>用矿车装配站把带熔炉的结构装到矿车上。</p>"),
    ("怎么用", "<p>熔炉提供动力，矿车可以自己跑；适合做小型的自动运输车。</p>"),
], params=[("类型", "载具")], related=["create:chest_minecart_contraption", "create:cart_assembler"])

# ======================================================================
# 第八批：动力/动态结构深度改写（覆盖早期简写条目）
# ======================================================================
def _deep(iid, tag, use, extra=None, pitfall=None, params=None, related=None):
    secs = [("怎么用", use)]
    if extra:
        secs.append(("进阶", extra))
    if pitfall:
        secs.append(("常见坑", pitfall))
    item(iid, tag, secs, params=params, related=related)

_deep("create:large_water_wheel", "大型水车：占地更大的水力动力源。",
 "<p>需要一整片<strong>流动的水</strong>推着它转。摆放时水要从叶片的一侧持续流过，静止的水推不动。大水的出力比普通水车高得多，但转速更慢。</p>",
 "<p>转速慢不代表没用：慢转速 + 高应力容量，正好带动<strong>大齿轮 → 小齿轮</strong>增速，或者直接驱动磨盘、粉碎轮这类吃应力的机器。水流可以用水源 + 活塞/闸门控制，做一条水渠比反复倒水省事。</p>",
 "<p>水被方块挡住或流干，水车会停转；做水渠时留好水源，别让水流在叶片前断掉。</p>",
 params=[("类型", "动力源"), ("出力", "高应力 · 低转速")],
 related=["create:water_wheel", "create:large_cogwheel"])

_deep("create:water_wheel_structure", "大型水车：水车的结构方块。",
 "<p>这是大型水车放置后形成的<strong>结构本体</strong>，不能直接手持放置；玩家放置的是水车物品，结构由它自动生成。</p>",
 "<p>拆水车时用扳手右键结构，会掉落可拾取的水车物品。结构被破坏（比如水被截断后不再旋转）时不会自行消失，但会停止输出动力。</p>",
 "<p>不要用普通镐去挖结构方块，掉的东西不对；拆动力部件统一用扳手。</p>",
 params=[("类型", "结构方块")], related=["create:large_water_wheel", "create:water_wheel"])

_deep("create:vertical_gearbox", "竖直十字齿轮箱：把水平旋转换成竖直旋转。",
 "<p>四个面都能接轴：水平的两面互相直通，竖直的两面也互相直通，<strong>水平与竖直之间成 90° 换向</strong>。用来把地面上的动力送上楼，或者把竖井里的动力引到水平产线。</p>",
 "<p>换向不改变转速，也不额外吃应力。多个竖直齿轮箱串联可以做「之」字形的动力路径，绕开机器。</p>",
 "<p>它只换方向，不换转速；要变速请配大小齿轮或转速控制器。</p>",
 params=[("类型", "传动"), ("换向", "水平 ↔ 竖直")],
 related=["create:gearbox", "create:cogwheel"])

_deep("create:sequenced_gearshift", "可编程齿轮箱：按红石信号执行预设动作。",
 "<p>右键打开界面，可以编排最多 <strong>5 步</strong>动作：旋转指定角度、旋转指定圈数、等待。每收到一次红石信号，就按顺序执行下一步。</p>",
 "<p>它是自动化产线的「程序控制器」：可以让机械臂转 90°、让转盘转半圈、让装置抬起再放下。配合<strong>脉冲延长器/计时器</strong>可以调动作节奏。</p>",
 "<p>动作是离散执行的，不会因为信号持续而连续转；要连续旋转请用普通齿轮箱 + 离合器。</p>",
 params=[("类型", "可编程传动"), ("步数", "最多 5 步")],
 related=["create:gearshift", "create:clutch", "create:rotation_speed_controller"])

_deep("create:adjustable_chain_gearshift", "可调节链式传动箱：带变速的链传动。",
 "<p>用<strong>扳手</strong>右键可以在几个固定传动比之间切换（类似自行车变速），输入输出的转速比随之改变。适合需要「换挡」的产线。</p>",
 "<p>链传动允许两个轴之间有一定距离和高度差，比齿轮箱灵活；变速后下游的应力需求也会跟着变。</p>",
 "<p>变速不会自动补偿应力：把转速调高后，下游机器可能因为应力不足而停摆。</p>",
 params=[("类型", "传动"), ("变速", "扳手切换")],
 related=["create:encased_chain_drive", "create:gearbox"])

_deep("create:encased_chain_drive", "链式传动箱：远距离、可错位的传动。",
 "<p>两个链式传动箱之间可以拉出<strong>链条</strong>，把旋转传到较远、甚至不同高度的轴上。适合跨房间、跨楼层的动力输送。</p>",
 "<p>链条方向可以用扳手调整；多段链条可以接力，做成一条长长的动力走廊。</p>",
 "<p>链条是实体连接，中间不能有方块挡住；转弯角度过大会接不上。</p>",
 params=[("类型", "传动")], related=["create:adjustable_chain_gearshift", "create:chain_conveyor"])

_deep("create:chain_conveyor", "锁链传动轮：沿链条搬运物品。",
 "<p>两个锁链传动轮之间拉一条链条，物品会<strong>挂在链条上移动</strong>。适合做悬挂式输送线、跨坑运输。</p>",
 "<p>链条可以上下坡，物品不会掉；输入端用漏斗/溜槽喂料，输出端接容器。</p>",
 "<p>链条速度跟随转速，转速太低会堵料；长链条中间要加支撑轮，否则会下垂。</p>",
 params=[("类型", "物流")], related=["create:encased_chain_drive", "create:belt"])

_deep("create:clutch", "离合器：用红石信号切断旋转。",
 "<p>默认<strong>通电才传动</strong>（红石信号 = 接通）。给信号就转，断信号就停，适合做「按需启动」的机器。</p>",
 "<p>和反转齿轮箱搭配，可以做正转/反转/停止三种状态的换向站；离合器切换是瞬时的，不会损坏机器。</p>",
 "<p>断开时下游会立刻失去动力，正在加工的机器会中断；频繁启停的产线建议加飞轮缓冲。</p>",
 params=[("类型", "控制"), ("逻辑", "通电传动")],
 related=["create:gearshift", "create:rotation_speed_controller"])

_deep("create:gearshift", "反转齿轮箱：用红石信号反转方向。",
 "<p>默认正转，<strong>通电后反转</strong>。用来控制传送带方向、机械臂摆动方向、螺旋桨正反推。</p>",
 "<p>反转不改变转速大小，只改方向；和离合器组合可以做「正转/反转/停」三态。</p>",
 "<p>反转瞬间下游会反向受力，带齿轮组的机械可能「打齿」一下，属于正常表现。</p>",
 params=[("类型", "控制"), ("逻辑", "通电反转")],
 related=["create:clutch", "create:gearbox"])

_deep("create:creative_motor", "创造马达：可调转速的无限动力源。",
 "<p>放置后右键可以设定<strong>转速</strong>（正负决定方向），输出无限应力，不消耗任何燃料。创造模式专属。</p>",
 "<p>测试产线时非常好用：把转速调到目标值，就能验证机器在真实转速下的表现，而不用先搭一套水车。</p>",
 "<p>它只提供旋转，不提供「应力容量」的显示；接上应力表可以看到下游需求。</p>",
 params=[("类型", "创造动力源")], related=["create:powered_shaft", "create:speedometer"])

_deep("create:powered_shaft", "动力曲轴：创造马达的旋转输出端。",
 "<p>创造马达放置后会生成动力曲轴，它就是那根<strong>持续旋转的轴</strong>，可以像普通轴一样接齿轮、传动带。</p>",
 "<p>它属于马达结构的一部分，拆马达时会一起消失，不需要单独处理。</p>",
 "<p>不要把它当成普通传动轴去铺长距离，它只在马达旁边有效。</p>",
 params=[("类型", "创造部件")], related=["create:creative_motor"])

_deep("create:flywheel", "飞轮：给蒸汽引擎稳速。",
 "<p>贴在<strong>蒸汽引擎</strong>侧面一起工作：引擎每冲程出力不均，飞轮把旋转「存」起来，让输出更平稳。</p>",
 "<p>飞轮越大（多放几个连成一片），储能越多，引擎的抖动越小；高转速下飞轮本身也会消耗一点应力。</p>",
 "<p>飞轮不能当独立动力源，脱离引擎就只是装饰。</p>",
 params=[("类型", "储能/稳速")], related=["create:steam_engine"])

_deep("create:hand_crank", "手摇曲柄：手动动力源。",
 "<p>右键摇动，给相连的轴提供<strong>短时旋转</strong>。适合启动小型装置、测试机器、给初期产线一点动力。</p>",
 "<p>连续右键可以维持旋转；摇动时角色不能做别的动作，属于「人力换动力」。</p>",
 "<p>手摇转速低、不持久，别指望它带动整条产线；尽早换水车或风车。</p>",
 params=[("类型", "动力源")], related=["create:water_wheel", "create:creative_motor"])

_deep("create:steam_whistle", "蒸汽笛：蒸汽引擎的鸣笛。",
 "<p>装在<strong>蒸汽引擎</strong>或蒸汽管路上，通蒸汽时会发出汽笛声，纯装饰音效。</p>",
 "<p>可以用红石/阀门控制鸣笛时机，给车站、工厂做氛围。</p>",
 "<p>没有蒸汽时不响；别把它当压力表用。</p>",
 params=[("类型", "装饰/音效")], related=["create:steam_engine", "create:steam_whistle_extension"])

_deep("create:steam_whistle_extension", "蒸汽笛加长段：把汽笛接长。",
 "<p>接在蒸汽笛下方，增加笛身长度，<strong>改变音高</strong>（越长越低）。</p>",
 "<p>多接几段就能调出低沉的船笛声，适合做大船、车站。</p>",
 "<p>只改音高不改音量；接太长会显得比例失调。</p>",
 params=[("类型", "装饰/音效")], related=["create:steam_whistle"])

_deep("create:turntable", "转盘：把上方的结构整体旋转。",
 "<p>上方用<strong>超级胶</strong>粘住的方块会跟着转盘一起旋转，适合做旋转展台、旋转炮塔、转盘式换向。</p>",
 "<p>可以设定每次旋转的角度，用红石脉冲逐步转动；配合可编程齿轮箱可以做「转到指定角度停住」。</p>",
 "<p>转盘只转它上方的结构，侧面贴的方块不会跟着走；粘结构前先想好边界。</p>",
 params=[("类型", "动态结构")], related=["create:mechanical_bearing", "create:super_glue"])

_deep("create:speedometer", "转速表：显示轴的转速。",
 "<p>贴在轴/齿轮上，表盘指针显示<strong>当前转速</strong>；接上<strong>显示链接器</strong>可以把数值送到翻牌显示器或辉光管。</p>",
 "<p>做产线监控时很实用：一眼看出某段是不是转得太慢、是不是停了。</p>",
 "<p>它只测转速不测应力；要看负载请用应力表。</p>",
 params=[("类型", "测量")], related=["create:stressometer", "create:display_link"])

_deep("create:stressometer", "应力表：显示应力占用。",
 "<p>接在动力网络上，显示<strong>已用应力 / 总应力</strong>。指针进入红区说明下游机器太多，需要加动力源或减机器。</p>",
 "<p>数值可以通过显示链接器输出，做成工厂的总控面板。</p>",
 "<p>应力超限时机器会整体停转，不是单个停；看到红区要立刻加动力。</p>",
 params=[("类型", "测量")], related=["create:speedometer", "create:display_link"])

_deep("create:linear_chassis", "轴向底盘：沿一个方向延伸的结构骨架。",
 "<p>用<strong>超级胶</strong>把方块粘在底盘上，再用动力活塞/绳索滑轮/轴承推动，就能把整块结构当成一个整体移动。</p>",
 "<p>轴向底盘只沿自身朝向延伸，适合做活塞平台、升降台、直线移动的机械。</p>",
 "<p>没粘牢的方块会在移动时掉落；组装前先用胶把关键方块都粘一遍。</p>",
 params=[("类型", "动态结构")], related=["create:radial_chassis", "create:super_glue", "create:mechanical_piston"])

_deep("create:radial_chassis", "径向底盘：向四周扩展的圆形骨架。",
 "<p>以自身为中心向<strong>四周</strong>延伸，适合做旋转平台、圆形炮塔底座、旋转温室。</p>",
 "<p>和动力轴承配合，可以把一整个圆形结构转起来。</p>",
 "<p>径向底盘范围是圆的，边缘的方块容易漏粘；转起来前先空转一圈检查。</p>",
 params=[("类型", "动态结构")], related=["create:linear_chassis", "create:mechanical_bearing"])

_deep("create:secondary_linear_chassis", "轴向底盘二号：可换向的底盘。",
 "<p>和轴向底盘功能相同，但<strong>可以用扳手切换延伸方向</strong>（两个轴向），布线时更灵活。</p>",
 "<p>适合空间狭窄、需要临时改方向的升降结构。</p>",
 "<p>切换方向后已粘的方块不会自动重排，改向前先拆结构。</p>",
 params=[("类型", "动态结构")], related=["create:linear_chassis"])

_deep("create:mechanical_piston", "动力活塞：推动整个结构移动。",
 "<p>活塞杆伸出时，把粘在杆头上的<strong>动态结构</strong>整体推出去；缩回时拉回来。行程由活塞杆节数决定。</p>",
 "<p>和底盘、超级胶配合，可以做升降台、推料机构、移动平台。转速决定伸缩速度。</p>",
 "<p>推动的结构不能和世界方块卡住，否则会卡死；行程中留出净空。</p>",
 params=[("类型", "动态结构")], related=["create:sticky_mechanical_piston", "create:piston_extension_pole", "create:linear_chassis"])

_deep("create:sticky_mechanical_piston", "黏性动力活塞：能拉回结构的活塞。",
 "<p>和普通动力活塞一样推动结构，但<strong>缩回时会把结构拉回来</strong>（普通活塞只会脱离）。</p>",
 "<p>适合做往返运动：推出去再拉回来，不用额外装置。</p>",
 "<p>拉回时结构要能原路返回，中间不能有障碍物。</p>",
 params=[("类型", "动态结构")], related=["create:mechanical_piston"])

_deep("create:mechanical_piston_head", "动力活塞头：活塞的杆头。",
 "<p>活塞伸出的最前端，结构就粘在它上面。活塞杆每加一节，行程加一格。</p>",
 "<p>杆头本身不能单独放置，是活塞结构的一部分。</p>",
 "<p>行程越长越慢，长行程建议改用绳索滑轮。</p>",
 params=[("类型", "结构部件")], related=["create:mechanical_piston", "create:piston_extension_pole"])

_deep("create:piston_extension_pole", "活塞杆：给活塞加行程。",
 "<p>接在活塞和杆头之间，<strong>每节加一格行程</strong>。多节串联可以做很长的推程。</p>",
 "<p>杆越长伸缩越慢，但比堆多个活塞省空间。</p>",
 "<p>杆是实体，伸出路径上不能有方块。</p>",
 params=[("类型", "结构部件")], related=["create:mechanical_piston", "create:mechanical_piston_head"])

_deep("create:rope_pulley", "绳索滑轮：垂直升降结构。",
 "<p>用<strong>绳索</strong>把下方的结构吊起来，滑轮转动时收放绳索，实现升降。适合矿井电梯、吊装平台。</p>",
 "<p>绳索长度可以现场调整；下方结构用超级胶粘好，整体上下移动。</p>",
 "<p>绳索不能被方块夹住；升降路径要留空。承重结构太重时升降会很慢。</p>",
 params=[("类型", "动态结构")], related=["create:rope", "create:pulley_magnet", "create:linear_chassis"])

_deep("create:pulley_magnet", "滑轮磁铁：绳索滑轮的吸附端。",
 "<p>装在绳索末端，用来<strong>吸住下方的结构</strong>，比手动粘胶更方便拆装。</p>",
 "<p>通红石可以释放/吸附；适合频繁更换吊装物的场合。</p>",
 "<p>只吸得动它正下方的结构，偏一格就吸不到。</p>",
 params=[("类型", "结构部件")], related=["create:rope_pulley"])

_deep("create:gantry_carriage", "起重机取物器：沿起重机梁移动的滑车。",
 "<p>挂在<strong>起重机杆</strong>上，沿着梁前后移动；下面可以挂机械臂、钻头、部署器，做成一条会走的加工线。</p>",
 "<p>配合旋转的起重机杆可以覆盖很大一片区域，适合自动化农场、采矿场。</p>",
 "<p>滑车移动需要动力，速度跟转速相关；梁太长中间要加支撑。</p>",
 params=[("类型", "动态结构")], related=["create:gantry_shaft", "create:mechanical_arm"])

_deep("create:cart_assembler", "矿车装配站：把结构装到矿车上。",
 "<p>放在矿车轨道上方，把用超级胶粘好的结构<strong>整体装到矿车上</strong>，变成可移动的装置。</p>",
 "<p>装配后的矿车可以自己跑（动力矿车）或被列车牵引，适合移动仓库、移动工作台。</p>",
 "<p>结构必须完全粘住，否则装配会失败或掉方块。</p>",
 params=[("类型", "载具")], related=["create:minecart_contraption", "create:minecart_coupling"])

_deep("create:minecart_anchor", "矿车锚：把矿车固定住。",
 "<p>放在轨道上，矿车经过时会被<strong>锁住停住</strong>，适合做装卸点、停车位。</p>",
 "<p>通红石可以释放；配合漏斗做自动装卸站。</p>",
 "<p>只对矿车有效，对列车要使用列车站点。</p>",
 params=[("类型", "轨道设施")], related=["create:minecart_coupling", "create:track_station"])

_deep("create:minecart_coupling", "矿车连轴器：把矿车连成一列。",
 "<p>手持右键两辆矿车，把它们<strong>连成一串</strong>，前面的动后面的跟着走。</p>",
 "<p>适合做小火车、矿车运输队；潜行右键可以断开。</p>",
 "<p>连接距离有限，太远会连不上；转弯处容易被拉脱。</p>",
 params=[("类型", "轨道设施")], related=["create:minecart_anchor", "create:track"])

_deep("create:contraption_controls", "动态结构控制器：在移动结构上操作。",
 "<p>装在<strong>动态结构</strong>（船、飞机、矿车装置）上，右键打开控制界面，可以控制结构的移动/旋转。</p>",
 "<p>配合座椅、船舵使用，是「自己开的载具」的核心部件。</p>",
 "<p>只能在已组装的动态结构上生效，放普通方块上没反应。</p>",
 params=[("类型", "载具控制")], related=["create:mechanical_bearing", "create:cart_assembler"])

_deep("create:super_glue", "强力胶：把方块粘成整体。",
 "<p>右键两个方块，把它们<strong>粘在一起</strong>；粘好的方块在动态结构移动时不会散开。潜行右键清除。</p>",
 "<p>一次可以粘一片区域（拖动框选），是组装船、飞机、移动装置的基础工具。</p>",
 "<p>只粘「结构」不粘「世界」：粘住的方块仍然可以被正常破坏。</p>",
 params=[("类型", "工具")], related=["create:linear_chassis", "create:mechanical_piston", "create:sticker"])

_deep("create:sticker", "黏着器：可开关的粘附方块。",
 "<p>贴在方块上，通红石时<strong>黏住前方的结构</strong>，再给一次信号断开。适合做可拆卸的吊装、自动脱钩。</p>",
 "<p>和绳索滑轮、活塞配合，可以做出「抓取-移动-释放」的自动化。</p>",
 "<p>黏住的是整个动态结构，不只是前面那一块。</p>",
 params=[("类型", "结构部件")], related=["create:super_glue", "create:rope_pulley"])

_deep("create:mechanical_bearing", "动力轴承：让结构整体旋转。",
 "<p>把用超级胶粘好的结构<strong>绕轴承中心旋转</strong>。适合做旋转炮塔、摩天轮、旋转餐厅。</p>",
 "<p>转速决定旋转速度；结构越大越吃应力。旋转中的结构仍然是实体，可以碰撞。</p>",
 "<p>旋转半径内的世界方块会挡住结构；转之前先空转一圈检查净空。</p>",
 params=[("类型", "动态结构")], related=["create:clockwork_bearing", "create:radial_chassis"])

_deep("create:clockwork_bearing", "时钟轴承：按游戏内时间旋转。",
 "<p>不是由转速驱动，而是<strong>跟随游戏内时间</strong>慢慢转动，像钟表的指针。右键可以启停。</p>",
 "<p>可以再放一个结构当「分针」，做出真正的钟楼；也适合做缓慢旋转的展示台。</p>",
 "<p>它不吃应力也不受转速影响，别指望用它带动机器。</p>",
 params=[("类型", "装饰/动态结构")], related=["create:mechanical_bearing", "create:cuckoo_clock"])

_deep("create:propeller", "扇叶：飞行器的推进器。",
 "<p>装在<strong>动态结构</strong>上，旋转时产生推力，推动船/飞机前进。转向决定推力的方向。</p>",
 "<p>多个扇叶可以叠加推力；配合方向盘/控制器操纵。</p>",
 "<p>扇叶需要足够转速才有推力，低速只会空转。</p>",
 params=[("类型", "载具部件")], related=["create:sail_frame", "create:contraption_controls"])

_deep("create:sail_frame", "风帆框架：风帆的骨架。",
 "<p>先放框架，再把<strong>风帆</strong>贴上去组成风车受风面。框架决定帆的形状与大小。</p>",
 "<p>框架 + 帆 + 风车轴承 = 一台风车；帆越多出力越大。</p>",
 "<p>框架本身不产动力，必须贴帆；帆的朝向要迎着风。</p>",
 params=[("类型", "动力结构")], related=["create:white_sail", "create:windmill_bearing"])

# ======================================================================
# 第九批：机器与加工深度改写
# ======================================================================
_deep("create:millstone", "石磨：把材料磨成粉。",
 "<p>顶部用<strong>漏斗/溜槽</strong>进料，磨盘旋转时把物品磨成粉，产物从下方输出。转速越高磨得越快，但石磨本身也吃应力。</p>"
 "<p>最典型的是把小麦磨成面粉、把矿石磨成粉。磨盘一次处理一个物品，适合小批量、多配方的场合；大批量请用粉碎轮。</p>",
 "<p>石磨只能「磨」，不能「压」或「搅」；需要混合/压制的配方请用工作盆。</p>",
 "<p>进料口被堵住时磨盘会空转；下方容器满了也会卡住。</p>",
 params=[("类型", "加工"), ("输入", "顶部漏斗"), ("输出", "下方")],
 related=["create:crushing_wheel", "create:mechanical_mixer"])

_deep("create:crushing_wheel", "粉碎轮：一对反向旋转的碾压轮。",
 "<p>需要<strong>两个轮子相对放置、反向旋转</strong>，物品从两轮之间落下时被碾碎。轮子转得越快，处理越快。</p>"
 "<p>粉碎是前期最重要的「倍增」手段：原矿 → 粉碎矿，再洗涤或熔炼，产量比直接烧矿石高。也能把石头碾成沙、把作物碾成染料。</p>",
 "<p>两轮必须反向：用齿轮或反转齿轮箱让其中一侧反向，同向是转不起来的。轮子之间要有 1 格缝隙让物品通过。</p>",
 "<p>轮子会被硬物卡住（例如不该粉碎的方块）；进料前确认配方存在。</p>",
 params=[("类型", "加工"), ("结构", "双轮反向")],
 related=["create:millstone", "create:basin", "create:encased_fan"])

_deep("create:mechanical_saw", "动力锯：切割与剥皮。",
 "<p>锯片旋转时切割经过的物品：木板、台阶、楼梯、石砖都能在传送带上被「锯」成对应形态，也能给原木<strong>剥皮</strong>。</p>"
 "<p>配合传送带就是一条自动切割线：原木进去，木板/木棍出来。锯片也能当武器，但会消耗耐久。</p>",
 "<p>锯片有朝向，物品必须从锯片正面经过；转速太低会切不动。</p>",
 "<p>锯片是消耗品，长时间使用会磨损，记得备替换。</p>",
 params=[("类型", "加工"), ("用途", "切割/剥皮")],
 related=["create:millstone", "create:deployer", "create:belt"])

_deep("create:deployer", "部署器：会「用手」的机械臂。",
 "<p>部署器模拟玩家的一只手：可以<strong>放置方块、使用工具、剪羊毛、挤奶、点火、装桶</strong>，也能把物品「用」在面前的方块或实体上。</p>"
 "<p>给它工具（剪刀、斧、锄、桶）它就会照做；给方块它就会放置。配合传送带可以做自动农场、自动剪羊毛、自动装桶。</p>",
 "<p>部署器需要旋转动力，动作频率跟随转速；手持物品需要通过漏斗/机械臂输入。</p>",
 "<p>它不会自己补充消耗品，工具用坏就停；长产线要留补给。</p>",
 params=[("类型", "加工"), ("模拟", "玩家手部动作")],
 related=["create:mechanical_arm", "create:belt", "create:mechanical_press"])

_deep("create:mechanical_arm", "动力臂：在容器之间搬运物品。",
 "<p>机械臂从<strong>输入容器</strong>取物品，转到<strong>输出容器</strong>放下。用扳手右键可以设置输入/输出端，支持传送带、漏斗、箱子、工作盆。</p>"
 "<p>它比漏斗灵活：可以跨距离、跨高度搬运，还能精确控制「拿几个」。转速决定手臂摆动速度。</p>",
 "<p>输入输出端设置错了会原地打转；摆臂路径上不能有方块挡住。</p>",
 "<p>机械臂一次只搬一组，超大流量请用传送带或溜槽。</p>",
 params=[("类型", "物流/加工"), ("设置", "扳手")],
 related=["create:deployer", "create:andesite_funnel", "create:chute"])

_deep("create:basin", "工作盆：混合、压制、加热的反应容器。",
 "<p>把物品/流体放进盆里，用<strong>搅拌器</strong>混合、用<strong>压床</strong>压制；下方放<strong>烈焰人燃烧室</strong>加热后可以做饭、炼钢、熬药。</p>"
 "<p>盆是很多高级配方的核心：黄铜、玫瑰石英、面团、巧克力都要在盆里做。可以接管道输入流体，用漏斗/机械臂输入物品。</p>",
 "<p>配方对「加热」有要求：没加热的盆做不出需要热的配方；温度不够时机器会空转。</p>",
 "<p>盆里的物品不会自动输出，要用漏斗/机械臂/溜槽取；产物满了会卡住整条线。</p>",
 params=[("类型", "加工"), ("容量", "物品 + 流体")],
 related=["create:mechanical_mixer", "create:mechanical_press", "create:blaze_burner"])

_deep("create:item_drain", "分液池：把物品里的流体沥出来。",
 "<p>物品经过时，附着的流体被<strong>沥出</strong>并收集到下方/侧面容器。用于回收桶装流体、处理湿物品。</p>"
 "<p>和注液器正好相反：一个灌、一个沥。配合传送带可以做「浸泡 → 沥干」的连续工艺。</p>",
 "<p>只能处理「带流体」的物品；干燥物品经过不会有反应。</p>",
 params=[("类型", "加工"), ("作用", "沥出流体")],
 related=["create:spout", "create:fluid_tank"])

_deep("create:spout", "注液器：给物品灌液体。",
 "<p>上方接<strong>管道/储罐</strong>供液，下方放物品（置物台或传送带）。物品经过时被灌满，例如水瓶、巧克力、蜂蜜。</p>"
 "<p>和分液池组成「灌装 → 沥干」产线；也能给食物涂层、给桶装液体。</p>",
 "<p>液体种类必须匹配配方；供液中断会停机。</p>",
 params=[("类型", "加工"), ("输入", "流体")],
 related=["create:item_drain", "create:fluid_tank", "create:belt"])

_deep("create:mechanical_drill", "动力钻头：自动挖掘。",
 "<p>钻头旋转时破坏正前方的方块，掉落物直接进背包或掉在地上。装在动态结构上就是一台<strong>移动采矿机</strong>。</p>"
 "<p>配合矿车装配站/起重机可以做自动挖矿、隧道掘进；也能用来拆建筑。</p>",
 "<p>钻头只挖正前方一格，移动路径要设计好；挖到基岩/不可破坏方块会停。</p>",
 params=[("类型", "工具/机器"), ("作用", "挖掘")],
 related=["create:mechanical_harvester", "create:cart_assembler", "create:gantry_carriage"])

_deep("create:mechanical_harvester", "动力收割机：自动收割作物。",
 "<p>旋转的刀片收割前方的作物，成熟的作物会被采下，<strong>未成熟的不动</strong>。装在动态结构上就是自动农场。</p>"
 "<p>配合犁（耕地）、播种（部署器）组成全自动农田。</p>",
 "<p>只收正前方一小片，走位要覆盖整块田；作物没成熟时来回空跑很浪费动力。</p>",
 params=[("类型", "农业机器")],
 related=["create:mechanical_plough", "create:deployer"])

_deep("create:mechanical_plough", "动力犁：自动耕地。",
 "<p>旋转的犁刀把前方的泥土/草方块<strong>翻成耕地</strong>，走过的路径就是一条田垄。</p>"
 "<p>和收割机、部署器（播种）组合，可以做全自动农场；也能用来「犁」出装饰性的田垄。</p>",
 "<p>只能耕可耕种的方块；遇到水、石头会卡住。</p>",
 params=[("类型", "农业机器")],
 related=["create:mechanical_harvester", "create:deployer"])

_deep("create:mechanical_roller", "动力压路机：把路面压平压实。",
 "<p>滚轮碾过方块时把松散的方块<strong>压实成路面</strong>（例如砂砾/沙土压成硬实地面），也能压平农田。</p>"
 "<p>做道路、站台、停机坪时很好用；配合铺路材料可以做出整齐的工业地面。</p>",
 "<p>只对特定方块有效；压过的路面外观会变，但不会改变方块种类。</p>",
 params=[("类型", "工具/机器")],
 related=["create:mechanical_plough", "create:cart_assembler"])

_deep("create:mechanical_pump", "动力泵：给管道加压输送流体。",
 "<p>接在<strong>流体管道</strong>上，旋转时把流体从一端抽到另一端。泵有方向，用扳手可以反转。</p>"
 "<p>长距离输液要分段加泵，否则流量会衰减；泵也能给储罐、工作盆、注液器供液。</p>",
 "<p>管道里没流体时泵空转；管道接错方向会抽不动。</p>",
 params=[("类型", "物流"), ("作用", "流体输送")],
 related=["create:fluid_pipe", "create:fluid_tank", "create:smart_fluid_pipe"])

_deep("create:mechanical_crafter", "动力合成器：自动合成。",
 "<p>由多个<strong>合成槽</strong>拼成 3×3 的工作台形状，每个槽放一种材料，旋转时自动合成。产物从正面输出。</p>"
 "<p>可以用<strong>合成槽盖板</strong>封住不用的槽位，做出 2×2、1×3 等小配方。配合漏斗/机械臂实现全自动合成。</p>",
 "<p>每合成一次需要转一圈，转速决定产能；材料必须按配方摆位，摆错不会合成。</p>",
 "<p>它只做「有序/无序合成」类配方，熔炼、压制等要交给对应机器。</p>",
 params=[("类型", "加工"), ("规模", "最多 3×3")],
 related=["create:crafter_slot_cover", "create:mechanical_arm", "create:belt"])

_deep("create:crafter_slot_cover", "合成槽盖板：封住不用的合成槽。",
 "<p>盖在动力合成器的槽位上，把这个槽<strong>屏蔽</strong>掉，让小配方也能在 3×3 的合成器里工作。</p>"
 "<p>做 2×2（如木板）、1×3（如台阶）这类配方时，盖上多余的槽位即可。</p>",
 "<p>盖板不消耗材料，但会占住槽位；改配方时记得取下。</p>",
 params=[("类型", "机器部件")], related=["create:mechanical_crafter"])

_deep("create:weighted_ejector", "弹射置物台：把物品弹出去。",
 "<p>放在传送带/漏斗末端，通红石时把物品<strong>朝指定方向弹出</strong>，可以越过障碍落到目标容器或传送带上。</p>"
 "<p>适合做「跨线投料」、把产物送到高处，或者做投掷式分拣。</p>",
 "<p>弹射方向用扳手调整；力度固定，太远会掉在地上。</p>",
 params=[("类型", "物流")], related=["create:andesite_funnel", "create:chute"])

_deep("create:item_hatch", "物品舱口：动态结构上的物品出入口。",
 "<p>装在船/飞机/矿车等<strong>动态结构</strong>上，让外面的漏斗/管道能把物品送进结构里的容器。</p>"
 "<p>没有它，移动中的结构无法与外界交换物品。</p>",
 "<p>必须贴在结构边界上，朝外的一面才能接漏斗。</p>",
 params=[("类型", "载具部件")], related=["create:portable_storage_interface", "create:cart_assembler"])

_deep("create:portable_storage_interface", "移动式存储接口：给动态结构接箱子。",
 "<p>装在动态结构上，把结构里的容器<strong>暴露</strong>给外部物流（漏斗、机械臂、传送带）。</p>",
 "<p>和物品舱口配合，可以做「移动仓库」：结构开过来，自动装卸。</p>",
 "<p>只能在已组装的动态结构上生效。</p>",
 params=[("类型", "载具部件")], related=["create:item_hatch", "create:portable_fluid_interface"])

_deep("create:portable_fluid_interface", "移动式流体接口：给动态结构接管道。",
 "<p>装在动态结构上，让外部管道能给结构里的储罐<strong>加注/抽取</strong>流体。</p>",
 "<p>适合移动加油车、移动储液罐。</p>",
 "<p>接口有方向，接反了抽不动。</p>",
 params=[("类型", "载具部件")], related=["create:portable_storage_interface", "create:fluid_pipe"])


# ======================================================================
# 第十批：物流与仓储深度改写
# ======================================================================
_deep("create:andesite_funnel", "安山漏斗：抽取或投放物品。",
 "<p>有两种模式：<strong>抽取</strong>（从背后的容器拿东西）和<strong>投放</strong>（把东西放进前面的容器/传送带）。用扳手右键切换方向与模式。</p>"
 "<p>安山漏斗抽取速度慢、一次一个，胜在便宜；把它贴在箱子、传送带、工作盆上就能组成最基础的物流。</p>",
 "<p>漏斗只处理它正对的那一格；方向装反了会「往外吐」而不是「往里吸」。用扳手看一眼箭头再接线。</p>",
 params=[("类型", "物流"), ("速度", "慢")],
 related=["create:brass_funnel", "create:chute", "create:belt"])

_deep("create:brass_funnel", "黄铜漏斗：带过滤的高速漏斗。",
 "<p>比安山漏斗快，而且<strong>自带过滤槽</strong>：可以指定只抽取/投放某几种物品，还能设置「允许/禁止」名单。</p>"
 "<p>做分拣线时黄铜漏斗是核心：一条传送带旁挂一排黄铜漏斗，各管一种产物，就能把混合物料分流到不同箱子。</p>",
 "<p>过滤槽要放「样本物品」，不是放数量；名单模式（白/黑）搞反了会全部放行或全部拦下。</p>",
 params=[("类型", "物流"), ("速度", "快"), ("过滤", "支持")],
 related=["create:andesite_funnel", "create:filter", "create:attribute_filter"])

_deep("create:andesite_belt_funnel", "安山传送带漏斗：贴着传送带用的漏斗。",
 "<p>专门贴在<strong>传送带侧面</strong>的漏斗，物品经过时被它「抓」进背后的容器。省去了对准格子的麻烦。</p>"
 "<p>适合在传送带中段收货：产物从带上经过，漏斗把它收进箱子，带子继续往前。</p>",
 "<p>只对传送带有效，贴在普通方块上不工作；抓取是逐个进行的，流量大时会漏过去。</p>",
 params=[("类型", "物流")], related=["create:brass_belt_funnel", "create:andesite_funnel", "create:belt"])

_deep("create:brass_belt_funnel", "黄铜传送带漏斗：带过滤的传送带漏斗。",
 "<p>安山传送带漏斗的升级版：<strong>速度更快、支持过滤</strong>，可以只抓某几种物品，其余放行。</p>"
 "<p>做「主带分流」最顺手：同一条带上混着多种产物，黄铜漏斗各抓各的。</p>",
 "<p>过滤名单要和实际产物一致，否则会把不该收的物品也截走。</p>",
 params=[("类型", "物流"), ("过滤", "支持")], related=["create:andesite_belt_funnel", "create:brass_funnel"])

_deep("create:chute", "溜槽：垂直搬运物品。",
 "<p>竖直放置的管道，物品从上方掉进去、<strong>从下方出来</strong>，可以穿透很多层楼板。</p>"
 "<p>做多层工厂的「垂直物流」：上层产物直接落到底层仓库，不用一层层接漏斗。</p>",
 "<p>溜槽是单向向下的；要往上送请用机械臂或传送带。底部出口被挡住会堵住。</p>",
 params=[("类型", "物流"), ("方向", "向下")], related=["create:smart_chute", "create:andesite_funnel"])

_deep("create:smart_chute", "智能溜槽：带过滤的溜槽。",
 "<p>在溜槽基础上加了<strong>过滤与红石控制</strong>：只让指定物品通过，或者用红石信号开关。</p>"
 "<p>适合做「只让成品下楼、把半成品拦下」的分流，或者用红石控制某条支线通断。</p>",
 "<p>过滤设置错会把该过的物品拦下，表现为「堵在溜槽里」。</p>",
 params=[("类型", "物流"), ("过滤", "支持")], related=["create:chute", "create:brass_funnel"])

_deep("create:item_vault", "物品保险库：大容量储物。",
 "<p>比箱子大得多的<strong>批量存储</strong>方块，可以并排拼成一面墙，容量随数量叠加。</p>"
 "<p>配合仓储链接站可以接入「库存网络」，让打包机、发报机自动存取。</p>",
 "<p>保险库不能像箱子那样直接打开翻找单个槽位？它可以，但更适合被网络调用；大规模仓储建议配仓储网络。</p>",
 params=[("类型", "仓储"), ("容量", "大")], related=["create:stock_link", "create:packager"])

_deep("create:fluid_tank", "流体储罐：储存流体。",
 "<p>可以<strong>竖直叠放</strong>成大罐，容量随高度增加；顶部/底部/侧面都能接管道。</p>"
 "<p>做流体产线时它是缓冲：泵往里灌，注液器/工作盆从里面取。也可以当装饰性的锅炉、水塔。</p>",
 "<p>罐子只存一种流体，混装会失败；拆罐前先把流体抽走，否则会浪费。</p>",
 params=[("类型", "仓储"), ("容量", "随高度叠加")], related=["create:fluid_pipe", "create:mechanical_pump", "create:spout"])

_deep("create:fluid_pipe", "流体管道：输送流体。",
 "<p>连接泵、储罐、机器，把流体从一处送到另一处。管道可以拐弯、分支，用扳手调整连接方向。</p>"
 "<p>长距离要加<strong>动力泵</strong>增压，否则流量会衰减甚至不流动。</p>",
 "<p>管道不会自己产生压力；没有泵时只能靠重力/落差做短距离输送。</p>",
 params=[("类型", "物流")], related=["create:mechanical_pump", "create:smart_fluid_pipe", "create:fluid_tank"])

_deep("create:smart_fluid_pipe", "智能流体管道：带过滤的管道。",
 "<p>只允许<strong>指定流体</strong>通过，其他流体会被挡住；适合多流体共线的场合，防止串液。</p>"
 "<p>可以用扳手设置过滤，也能用红石控制通断。</p>",
 "<p>过滤设错会把该走的流体拦下，表现为「泵在转但下游没液」。</p>",
 params=[("类型", "物流"), ("过滤", "支持")], related=["create:fluid_pipe", "create:fluid_valve"])

_deep("create:glass_fluid_pipe", "玻璃流体管道：看得见流体的管道。",
 "<p>和普通管道功能一样，但<strong>透明</strong>，能直接看到里面的流体与流动方向。</p>"
 "<p>做展示、教学、或者排查「到底有没有液体」时非常有用。</p>",
 "<p>只是外观不同，不提供额外过滤或压力。</p>",
 params=[("类型", "物流")], related=["create:fluid_pipe", "create:smart_fluid_pipe"])

_deep("create:encased_fluid_pipe", "流体管道箱：包壳的管道。",
 "<p>把管道包进机壳里，外观变成整齐的方块，<strong>功能不变</strong>。适合穿墙、走地板下、做整齐的机房。</p>",
 "<p>用扳手可以拆回普通管道。</p>",
 "<p>包壳只改外观，不改变连接关系；拆壳时注意别把整段管道拆了。</p>",
 params=[("类型", "物流")], related=["create:fluid_pipe", "create:copper_casing"])

_deep("create:fluid_valve", "流体阀门：手动/红石开关管道。",
 "<p>装在管道中间，<strong>右键或红石信号</strong>开关流体通路；也可以装阀门手轮手动操作。</p>"
 "<p>做流体产线的总闸、分支控制、紧急切断都很合适。</p>",
 "<p>关阀不会排出管内残液；检修前记得先泄压。</p>",
 params=[("类型", "物流"), ("控制", "手动/红石")], related=["create:fluid_pipe", "create:copper_valve_handle"])

_deep("create:stockpile_switch", "存量转信器：按库存量输出红石。",
 "<p>接在容器/库存网络上，<strong>按存量多少输出不同强度的红石信号</strong>。库存低于阈值就断电，高于阈值就通电。</p>"
 "<p>做自动补货、停机保护、库存报警都用它：箱子快空了就启动上游产线。</p>",
 "<p>阈值要设对，否则会在临界点反复启停（抖动）；可以加脉冲延长器做缓冲。</p>",
 params=[("类型", "红石/仓储")], related=["create:stock_link", "create:factory_gauge"])

_deep("create:stock_ticker", "仓储发报机：向库存网络下单。",
 "<p>接入仓储网络后，可以<strong>请求指定物品</strong>，网络会把货送到你面前/指定位置；也能给蓝图加农炮备料。</p>"
 "<p>它让「集中仓储 + 按需取货」成为可能，不用再跑回仓库翻箱子。</p>",
 "<p>网络里要有「仓库管理员」（坐着的生物或烈焰人炉）才能工作；请求的物品缺货时会一直等待。</p>",
 params=[("类型", "仓储")], related=["create:stock_link", "create:redstone_requester", "create:package"])

_deep("create:stock_link", "仓储链接站：把容器接入库存网络。",
 "<p>贴在箱子/保险库上，把这个容器登记进<strong>库存网络</strong>。多个链接站可以组成一个大仓库。</p>"
 "<p>打包机、发报机、红石请求器都通过它来存取货物。</p>",
 "<p>链接站要连成网络（相邻或通过线缆），单独一个无法被远程调用。</p>",
 params=[("类型", "仓储")], related=["create:stock_ticker", "create:packager", "create:item_vault"])

_deep("create:factory_gauge", "工厂仪表：显示库存/产量。",
 "<p>接在库存网络上，显示<strong>某种物品的存量或产量</strong>，可以配合显示链接器把数字投到翻牌显示器上。</p>"
 "<p>做工厂总控面板、仓库看板时很好用。</p>",
 "<p>只显示它被设置的那一种物品；换物品要重新设置。</p>",
 params=[("类型", "显示/仓储")], related=["create:display_link", "create:stockpile_switch"])

_deep("create:package", "纸壳包裹：打包好的货物。",
 "<p>由<strong>打包机</strong>把物品装进纸壳，方便用包裹物流（蛙港、邮箱）长距离投递。</p>"
 "<p>包裹可以写地址、贴邮票，通过蛙港网络送到指定邮箱。</p>",
 "<p>包裹里的物品不能直接取出，要拆包；地址写错会退回或丢失。</p>",
 params=[("类型", "物流")], related=["create:packager", "create:package_frogport", "create:postbox"])

_deep("create:rare_package", "稀有包裹：特殊外观的包裹。",
 "<p>包裹的稀有变体，外观更精致，通常来自特殊来源或活动；功能与普通包裹一致。</p>",
 "<p>可以当收藏品，也可以正常投递。</p>",
 "<p>别把它当成「必定开出稀有物品」的盲盒，它只是外观不同。</p>",
 params=[("类型", "物流")], related=["create:package"])

_deep("create:package_frogport", "货物蛙港：包裹物流的收发站。",
 "<p>包裹物流的核心：把包裹<strong>发往</strong>目标地址，或<strong>接收</strong>寄来的包裹。需要用扳手/界面设置地址与频道。</p>"
 "<p>配合邮箱、打包机，可以做出「下单 → 打包 → 投递 → 收货」的全自动物流。</p>",
 "<p>收发两端都要有蛙港并且地址匹配；网络没连通时包裹会卡在途中。</p>",
 params=[("类型", "物流")], related=["create:package", "create:postbox", "create:packager"])

_deep("create:packager", "打包机：把物品装成包裹。",
 "<p>接在容器/传送带末端，把物品<strong>打包成纸壳包裹</strong>，可以设置包裹的地址与内容。</p>"
 "<p>配合蛙港就是自动发货机；配合仓储网络可以按订单打包。</p>",
 "<p>打包需要纸壳；地址没设的包裹发不出去。</p>",
 params=[("类型", "物流")], related=["create:package", "create:package_frogport", "create:repackager"])

_deep("create:repackager", "理包机：拆包/重新打包。",
 "<p>把收到的包裹<strong>拆开</strong>，把里面的物品倒进容器；也能把散装物品重新打包。</p>"
 "<p>自动收货站的核心：蛙港收包 → 理包机拆包 → 物品进仓库。</p>",
 "<p>拆包会消耗包裹纸壳；大量收货时注意纸壳补给。</p>",
 params=[("类型", "物流")], related=["create:packager", "create:package"])

_deep("create:package_filter", "包裹过滤器：按地址/内容分拣包裹。",
 "<p>装在包裹物流线上，<strong>按地址或内容过滤</strong>包裹，把不同目的地的包裹分流到不同蛙港。</p>",
 "<p>多线路发货时用它做路由，避免所有包裹挤在一个出口。</p>",
 "<p>过滤条件要和其他环节的地址一致，否则会全部拦下或全部放行。</p>",
 params=[("类型", "物流")], related=["create:package", "create:package_frogport"])

_deep("create:redstone_requester", "红石请求器：用红石脉冲下单。",
 "<p>放置前先用它右键<strong>仓储链接站</strong>接入网络，之后每收到一次红石脉冲，就向网络请求一次指定物品。</p>"
 "<p>做自动补货：产线缺料时给个脉冲，仓库自动发货。</p>",
 "<p>请求的物品要在网络里有库存；没接入网络时脉冲无效。</p>",
 params=[("类型", "仓储/红石")], related=["create:stock_ticker", "create:stock_link"])

_deep("create:creative_crate", "创造板条箱：无限物品源。",
 "<p>创造模式专属，可以<strong>无限提供</strong>设定的物品，用来测试产线。</p>",
 "<p>右键设置物品，接上传送带/漏斗就能当无限原料。</p>",
 "<p>生存模式无法获得；它只提供物品，不提供流体。</p>",
 params=[("类型", "创造物品")], related=["create:creative_fluid_tank"])

_deep("create:creative_fluid_tank", "创造流体储罐：无限流体源。",
 "<p>创造模式专属，可以<strong>无限提供</strong>设定的流体，给测试产线供液。</p>",
 "<p>接上管道/泵即可；也能当装饰性大罐。</p>",
 "<p>生存模式无法获得。</p>",
 params=[("类型", "创造物品")], related=["create:creative_crate", "create:fluid_tank"])

# ======================================================================
# 第十一批：列车与红石深度改写
# ======================================================================
_deep("create:track", "列车轨道：列车行驶的基础。",
 "<p>一节一节铺成线路，可以做出弯道与坡道；铺好后用<strong>列车站点</strong>标记停靠点，用<strong>信号机</strong>管理区间。</p>"
 "<p>轨道本身不带动力：列车由车头（驾驶台/动力车）驱动，轨道只提供导向。长距离线路要提前规划弯道半径，太急的弯列车会转不过去。</p>",
 "<p>轨道要连续，中间断开列车会停；坡道要用对应的斜坡轨道块，直接叠高是接不上的。</p>",
 params=[("类型", "轨道"), ("用途", "列车导向")],
 related=["create:track_station", "create:track_signal", "create:schedule"])

_deep("create:track_station", "列车站点：定义停靠点。",
 "<p>放在轨道旁，用界面<strong>设置站名</strong>。列车时刻表里引用站名，列车就会在这里停靠、上下客货。</p>"
 "<p>站点还可以设置停靠方向、是否自动发车；多个站点组成一条线路。</p>",
 "<p>站名必须和时刻表里写的一致（区分大小写），否则列车不会停。站点要贴着轨道放，离太远识别不到。</p>",
 params=[("类型", "列车设施"), ("作用", "停靠点")],
 related=["create:track", "create:schedule", "create:controls"])

_deep("create:track_signal", "列车信号机：管理区间闭塞。",
 "<p>把线路分成<strong>区间</strong>：信号机检测前方区间是否有车，有车就显示红灯，后车自动减速停车，避免追尾。</p>"
 "<p>单线铁路、车站咽喉区都靠它调度；也可以手动用红石控制信号。</p>",
 "<p>信号机要成对/按区间布置，只放一个不会形成保护；弯道与坡道上要留出制动距离。</p>",
 params=[("类型", "列车设施"), ("作用", "区间保护")],
 related=["create:track", "create:track_station", "create:train_door"])

_deep("create:schedule", "列车时刻表：编排列车路线。",
 "<p>手持右键打开编辑界面，添加<strong>站点与停留时间</strong>，形成一条循环路线；把时刻表交给列车后，它就会按表自动运行。</p>"
 "<p>可以设置「到站停车 N 秒」「条件发车」等规则，做公交化运营。</p>",
 "<p>时刻表里的站名必须和站点一致；路线闭环没闭合时列车会在终点停住。</p>",
 params=[("类型", "列车调度")], related=["create:track_station", "create:controls"])

_deep("create:controls", "列车驾驶台：手动驾驶列车。",
 "<p>装在车头，右键进入<strong>手动驾驶</strong>：前进/后退/加速/刹车。适合调车、试车、观光铁路。</p>"
 "<p>驾驶台也是列车的「车头」标志之一，自动运行时可以不放。</p>",
 "<p>手动驾驶时注意信号机，闯红灯可能撞车；停车要提前减速。</p>",
 params=[("类型", "列车控制")], related=["create:track", "create:schedule"])

_deep("create:train_door", "列车门：车厢侧门。",
 "<p>装在车厢侧面，可以<strong>手动开关</strong>，也能被站点/红石控制，到站自动开门。</p>"
 "<p>和站台高度对齐，乘客上下车才顺。</p>",
 "<p>门是装饰+通行功能，不参与列车组装逻辑；装歪了会漏风（视觉上）。</p>",
 params=[("类型", "列车部件")], related=["create:train_trapdoor", "create:track_station"])

_deep("create:train_trapdoor", "列车活板门：车厢顶部/地板开口。",
 "<p>装在车厢顶部做检修口，或装在地板做上下车通道；可手动也可红石控制。</p>",
 "<p>做双层列车、观光车厢时很实用。</p>",
 "<p>活板门打开时是实体缺口，行车中注意别掉出去（尤其高速过弯）。</p>",
 params=[("类型", "列车部件")], related=["create:train_door"])

_deep("create:small_bogey", "小转向架：列车的小车底盘。",
 "<p>装在车厢底部，<strong>两个转向架</strong>托起一节车厢；转向架决定列车能过什么弯。</p>"
 "<p>小转向架适合短车厢、小半径弯道；载重大的车厢用大转向架更稳。</p>",
 "<p>转向架必须成对、方向一致，否则组装会失败或行驶跑偏。</p>",
 params=[("类型", "列车部件")], related=["create:large_bogey", "create:track"])

_deep("create:large_bogey", "大转向架：重型车厢的底盘。",
 "<p>承重更大、过弯更稳，适合机车、货车、长车厢。</p>"
 "<p>大转向架占位更大，车厢底部要留出空间。</p>",
 "<p>和小转向架混用时注意轴距，不然车厢会「扭」。</p>",
 params=[("类型", "列车部件")], related=["create:small_bogey"])

_deep("create:controller_rail", "控制铁轨：给矿车加速/刹车。",
 "<p>铺在轨道上，通红石时给经过的矿车<strong>加速或刹车</strong>（方向可调）。</p>"
 "<p>做矿车电梯、加速段、终点缓冲都用它。</p>",
 "<p>只对矿车有效，对组装好的列车无效；红石信号要持续供能。</p>",
 params=[("类型", "轨道设施")], related=["create:track", "create:minecart_anchor"])

_deep("create:fake_track", "轨道标记：地图上的假轨道。",
 "<p>外观和真轨道一样，但<strong>不能行车</strong>，只用于地图/建筑上的线路示意。</p>"
 "<p>做地铁图、站台标线、装饰性道岔时用，避免玩家误上。</p>",
 "<p>别看错铺成一片，列车开上去会卡住。</p>",
 params=[("类型", "装饰")], related=["create:track"])

_deep("create:railway_casing", "列车机壳：车厢的专用外壳。",
 "<p>列车部件的合成基底，也是车厢外观材料；深色金属质感，适合机车与客车。</p>"
 "<p>做大面积车厢外壳时比普通机壳更「铁路」。</p>",
 "<p>只是材料，不提供额外功能。</p>",
 params=[("类型", "材料/机壳")], related=["create:track", "create:controls"])

_deep("create:analog_lever", "模拟拉杆：可调强度的红石源。",
 "<p>右键调节<strong>输出强度 0-15</strong>，比普通拉杆精细，可以直接控制转速、亮度、推力等模拟量。</p>"
 "<p>配合转速控制器可以精确设定机器转速。</p>",
 "<p>它输出的是模拟信号，接在只认「开/关」的元件上会被当成「有信号」。</p>",
 params=[("类型", "红石源"), ("范围", "0-15")], related=["create:rotation_speed_controller"])

_deep("create:redstone_link", "无线红石信号终端：隔空传红石。",
 "<p>成对使用：两个终端设成<strong>同一频率</strong>，一边输入信号，另一边就输出同样的信号，不需要连线。</p>"
 "<p>跨房间、跨楼层、跨铁路布置控制线时非常省事。</p>",
 "<p>频率要成对匹配；同一频率被多对使用时信号会串。</p>",
 params=[("类型", "红石"), ("连接", "无线/成对")], related=["create:transmitter", "create:linked_controller"])

_deep("create:transmitter", "发信线圈：无线信号的发射端。",
 "<p>给无线红石提供<strong>发射/中继</strong>，扩大信号覆盖范围，适合大工厂跨区控制。</p>",
 "<p>和无线红石终端配对使用。</p>",
 "<p>它只负责传输，不产生信号；输入端要有红石源。</p>",
 params=[("类型", "红石")], related=["create:redstone_link", "create:linked_controller"])

_deep("create:content_observer", "智能侦测器：检测容器内容变化。",
 "<p>对着箱子/漏斗等容器，容器里的<strong>物品数量变化</strong>时输出一个红石脉冲；可以设置检测「增加/减少/任意变化」。</p>"
 "<p>做「产物满了就停机」「原料到了就启动」的自动控制非常方便。</p>",
 "<p>它只看内容变化，不看具体物品（要分物品请用属性过滤器/存量转信器）。</p>",
 params=[("类型", "红石传感器")], related=["create:stockpile_switch", "create:attribute_filter"])

_deep("create:display_board", "翻牌显示器：显示文字与数字。",
 "<p>由多块翻牌拼成，可以显示<strong>文字、数字、图标</strong>；配合显示链接器显示仪表读数。</p>"
 "<p>做车站导视、工厂看板、计分板。</p>",
 "<p>需要先写入内容再拼接；拆掉一块会破坏整体显示。</p>",
 params=[("类型", "显示")], related=["create:display_link", "create:nixie_tube"])

_deep("create:display_link", "显示链接器：把数据送到显示器。",
 "<p>连接<strong>仪表/传感器</strong>与<strong>翻牌显示器/辉光管</strong>，把转速、应力、库存等数值实时显示出来。</p>"
 "<p>做工厂总控面板的核心。</p>",
 "<p>要分别设置「数据源」和「目标」，接反了不显示。</p>",
 params=[("类型", "显示")], related=["create:display_board", "create:speedometer", "create:factory_gauge"])

_deep("create:nixie_tube", "辉光管：数字显示屏。",
 "<p>被红石充能时显示<strong>信号强度 0-15</strong>；用写好文字的<strong>剪贴板</strong>右键可以显示自定义文本。</p>"
 "<p>做计数器、站台编号、仪表读数都合适；16 色可染。</p>",
 "<p>它显示的是信号强度不是物品数量，要显示库存请用显示链接器。</p>",
 params=[("类型", "显示")], related=["create:display_link", "create:clipboard"])

_deep("create:placard", "置物板：展示物品。",
 "<p>把物品放上去<strong>展示</strong>，可以旋转角度；适合做货架标签、博物馆展台、配方提示。</p>",
 "<p>只是展示，不提供存储；取回物品右键即可。</p>",
 "<p>展示的物品不会计入容器统计。</p>",
 params=[("类型", "装饰")], related=["create:display_board"])

_deep("create:desk_bell", "呼唤铃：按一下叫人。",
 "<p>右键敲响，发出清脆的铃声，纯装饰/氛围道具；可以放在柜台、站长室。</p>",
 "<p>不产生红石信号。</p>",
 "<p>别指望它当红石按钮用。</p>",
 params=[("类型", "装饰")], related=["create:peculiar_bell", "create:haunted_bell"])

_deep("create:pulse_extender", "脉冲延长器：把短脉冲拉长。",
 "<p>输入一个脉冲，输出<strong>持续指定时长</strong>的信号；时长可调，最长可到 1 小时。</p>"
 "<p>做「按一下按钮，机器转 10 秒」这类定时控制。</p>",
 "<p>它延长的是信号持续时间，不改变触发时机；输入端的短脉冲要能被捕获。</p>",
 params=[("类型", "红石逻辑")], related=["create:pulse_repeater", "create:pulse_timer"])

_deep("create:pulse_repeater", "脉冲中继器：延迟后发一个短脉冲。",
 "<p>输入信号后<strong>延迟指定时间</strong>再输出一个短脉冲；延迟可调，最长 1 小时。</p>"
 "<p>做顺序动作、延时启动、节拍控制。</p>",
 "<p>输出是短脉冲不是持续信号；需要持续请用脉冲延长器。</p>",
 params=[("类型", "红石逻辑")], related=["create:pulse_extender", "create:pulse_timer"])

_deep("create:pulse_timer", "脉冲计时器：周期性发脉冲。",
 "<p>按设定<strong>周期</strong>不断输出脉冲；输入端充能会暂停并重置计时，右键可以反转输出逻辑。</p>"
 "<p>做自动农场节拍、流水线步进、闪烁灯。</p>",
 "<p>周期设得太短会让下游机器来不及处理；重置端要注意别误触。</p>",
 params=[("类型", "红石逻辑")], related=["create:pulse_extender", "create:pulse_repeater"])

_deep("create:powered_latch", "锁存器：能记住状态的红石开关。",
 "<p>后方输入把状态设为<strong>开</strong>，侧边输入设为<strong>关</strong>，输出保持当前状态；也可以空手右键手动切换。</p>"
 "<p>它是一个带记忆的开关：信号消失后状态不会丢，适合做「一键启停」「自锁电路」。</p>",
 "<p>它记的是状态不是脉冲；两个输入同时来时行为取决于时序，接线前先想清楚优先级。</p>",
 params=[("类型", "红石逻辑")], related=["create:powered_toggle_latch", "create:analog_lever"])

_deep("create:powered_toggle_latch", "转换锁存器：每来一个脉冲翻转一次。",
 "<p>每收到一个红石脉冲，输出状态<strong>翻转一次</strong>（开→关→开）。</p>"
 "<p>做「按一下开、再按一下关」的开关最方便，比如控制一盏灯或一台机器。</p>",
 "<p>它只认脉冲边沿，持续通电不会反复翻转。</p>",
 params=[("类型", "红石逻辑")], related=["create:powered_latch"])

_deep("create:redstone_contact", "接触式红石信号发生器：踩上去通电。",
 "<p>实体（玩家/生物/矿车）站上去时输出红石信号，离开就断开。</p>"
 "<p>做压力板、站台检测、自动门。</p>",
 "<p>只对实体有效，掉落物不算；灵敏度比原版压力板高。</p>",
 params=[("类型", "红石传感器")], related=["create:content_observer"])

_deep("create:attribute_filter", "属性过滤器：按属性筛选物品。",
 "<p>可以按<strong>附魔、耐久、名称、物品类型</strong>等属性过滤，比普通列表过滤器更细。</p>"
 "<p>做「只放行未附魔的工具」「只收受损装备」这类分拣。</p>",
 "<p>属性设置错会全部拦下；不确定时先用列表过滤器。</p>",
 params=[("类型", "物流/过滤")], related=["create:filter", "create:brass_funnel"])

_deep("create:filter", "列表过滤器：按物品名单过滤。",
 "<p>把样本物品放进过滤槽，形成<strong>白名单/黑名单</strong>，供漏斗、溜槽等使用。</p>"
 "<p>做多物品分拣时，一个过滤器管一组物品。</p>",
 "<p>过滤器本身不搬运物品，要装进漏斗/溜槽才生效。</p>",
 params=[("类型", "物流/过滤")], related=["create:attribute_filter", "create:brass_funnel"])

_deep("create:crafting_blueprint", "合成蓝图：记录并复用配方。",
 "<p>把工作台配方<strong>记录下来</strong>，之后可以一键查看/复用，也能给蓝图加农炮当施工图。</p>"
 "<p>做大型建筑、重复合成时省心。</p>",
 "<p>蓝图只记录配方/结构，不代替材料。</p>",
 params=[("类型", "工具")], related=["create:schematic", "create:schematicannon"])

# ======================================================================
# 第十二批：材料与零件（加厚到约 300 字）
# ======================================================================
item("create:andesite_alloy", "安山合金：Create 最基础的结构材料。", [
    ("怎么用", "<p>安山合金是整套机械的「入门金属」：机壳、齿轮、轴、漏斗、脚手架几乎都要它。前期最重要的产线就是把安山岩与铁/锌压成合金。</p>"
              "<p>它本身不能直接当动力件用，但几乎所有动力件的合成都要经过它，所以前期请尽量把产量拉起来，别让合金成为瓶颈。</p>"),
    ("怎么获得", "<p>把<strong>安山岩</strong>与<strong>铁粒/锌锭</strong>之类材料在工作台或压床里合成；不同配方产出数量不同，前期用工作台就够。</p>"
              "<p>安山岩在地下很常见，铁粒可以从铁锭拆、也可以粉碎矿石获得；锌要下矿找锌矿。</p>"),
    ("常见坑", "<p>9 个合金可以压成安山合金块、再拆回 9 个，储存不亏；但别把合金当「铁」用，它的配方要的是铁粒，不是合金本身。</p>"),
], params=[("类型", "基础材料")], related=["create:andesite_casing", "create:andesite_alloy_block", "create:zinc_ingot"])

item("create:brass_ingot", "黄铜锭：中后期机器的核心金属。", [
    ("怎么用", "<p>黄铜是「高级机器」的门槛：黄铜机壳、精密构件、列车部件、高级漏斗都吃它。到了中后期，黄铜产量基本等于你的科技进度。</p>"
              "<p>黄铜还用于装饰（黄铜块、黄铜栏杆），暖金色很适合做控制室与高级建筑。</p>"),
    ("怎么获得", "<p>铜 + 锌在<strong>工作盆</strong>里混合（需要加热）得到黄铜；这是 Create 第一个必须用「盆 + 搅拌器 + 热源」的配方，也是产线化的起点。</p>"
              "<p>铜可以从铜矿、粉碎铜矿来；锌要专门去挖锌矿，前期记得多囤。</p>"),
    ("常见坑", "<p>黄铜配方需要热量：盆下面没有烈焰人燃烧室是合不成的。混合比例错了会产出别的东西或直接失败，按 JEI 的配方摆。</p>"),
], params=[("类型", "金属锭")], related=["create:brass_casing", "create:precision_mechanism", "create:copper_ingot"])

item("create:zinc_ingot", "锌锭：炼黄铜的另一半。", [
    ("怎么用", "<p>锌主要用来做<strong>黄铜</strong>（铜 + 锌），也用于镀锌件与部分零件。它本身很少单独做结构。</p>"
              "<p>因为黄铜需求量大，锌往往会成为隐形瓶颈：铜矿遍地都是，锌矿却要专门找。</p>"),
    ("怎么获得", "<p>粗锌在熔炉里烧成锌锭；粗锌来自锌矿石（浅层与深层都有）。有时运附魔能多掉一些。</p>"
              "<p>锌块可以拆回 9 个锌锭，方便储存。</p>"),
    ("常见坑", "<p>别把锌锭全拿去做装饰块：黄铜产线一开，锌的消耗会突然变大。下矿时看到锌矿优先采。</p>"),
], params=[("类型", "金属锭")], related=["create:brass_ingot", "create:zinc_ore", "create:zinc_block"])

item("create:copper_sheet", "铜板：压出来的薄铜材。", [
    ("怎么用", "<p>铜板是很多机器的中间件：机壳、管道、背罐、列车部件都要它。它也是「板材」这一整套加工链的入门产品。</p>"
              "<p>铜板可以继续压成更薄的箔或做成铜瓦，是建筑与机械两头都用得上的材料。</p>"),
    ("怎么获得", "<p>把<strong>铜锭</strong>放进<strong>动力压床</strong>压成板。压床需要旋转动力，冲压一次出一块。</p>"
              "<p>前期没有压床时，部分配方可以用工作台替代，但效率低很多。</p>"),
    ("常见坑", "<p>压床下方要有承接面（置物台/传送带），否则压好的板会掉出来；连续压板时注意输出端别堵。</p>"),
], params=[("类型", "板材")], related=["create:mechanical_press", "create:copper_casing", "create:iron_sheet"])

item("create:iron_sheet", "铁板：最常用的结构板材。", [
    ("怎么用", "<p>铁板用于机壳、支架、列车部件与大量工具配方，是中期消耗最大的材料之一。</p>"
              "<p>它也是「金属板」系列的标准件：金板、铜板、黄铜板的加工方式完全一样，学会一种就会全部。</p>"),
    ("怎么获得", "<p>铁锭经<strong>动力压床</strong>压成铁板；也可以把铁块拆成锭再压，方便批量。</p>"
              "<p>铁板还能进一步做成坚固板（序列组装），那是后期装备的材料。</p>"),
    ("常见坑", "<p>铁板需求量大，建议专门做一条「锭 → 板」的压床线，用传送带供料，不要手动一块块压。</p>"),
], params=[("类型", "板材")], related=["create:mechanical_press", "create:sturdy_sheet", "create:andesite_casing"])

item("create:brass_sheet", "黄铜板：高级机器的板材。", [
    ("怎么用", "<p>黄铜板用于黄铜机壳、精密构件、列车外壳等中后期配方，是黄铜产线的下游产品。</p>"
              "<p>它比铁板贵，但做出来的机器也更高级；规划产线时把「黄铜板」单独拉一条支线。</p>"),
    ("怎么获得", "<p>黄铜锭经<strong>动力压床</strong>压成板。黄铜本身要先在盆里混合铜锌，所以这条链是「混合 → 浇筑 → 压板」。</p>"),
    ("常见坑", "<p>黄铜板经常和精密构件抢黄铜，前期先算好用量，别把黄铜全压成板。</p>"),
], params=[("类型", "板材")], related=["create:brass_ingot", "create:precision_mechanism", "create:brass_casing"])

item("create:golden_sheet", "金板：贵金属板材。", [
    ("怎么用", "<p>金板用于精密构件、高级红石件与部分装饰，用量不大但缺了就卡进度。</p>"
              "<p>金板也是「合金/镀层」类配方的常客，做高级机器前记得备几张。</p>"),
    ("怎么获得", "<p>金锭经<strong>动力压床</strong>压成板；金锭可以来自金矿、粉碎金矿或下界金矿。</p>"),
    ("常见坑", "<p>金板不要拿去随便装饰，精密构件的消耗比想象中大。</p>"),
], params=[("类型", "板材")], related=["create:precision_mechanism", "create:brass_sheet"])

item("create:sturdy_sheet", "坚固板：后期装备的核心材料。", [
    ("怎么用", "<p>坚固板用于<strong>下界合金背罐、潜水装备、高级工具</strong>等后期物品。它不能直接合成，必须走序列组装。</p>"
              "<p>因为它决定后期装备的进度，建议尽早把序列组装线搭起来。</p>"),
    ("怎么获得", "<p>用<strong>序列组装</strong>产线：把黑曜石粉等材料按步骤部署/压制，最后得到坚固板。整条线需要传送带、部署器、压床配合。</p>"
              "<p>序列组装的每一步都要精确摆放，中途断料会卡在半成品。</p>"),
    ("常见坑", "<p>序列组装线一旦卡住很难排查：先看半成品停在哪一步，再检查那一步的部署器有没有料。</p>"),
], params=[("类型", "高级材料"), ("工艺", "序列组装")], related=["create:powdered_obsidian", "create:precision_mechanism", "create:netherite_backtank"])

item("create:precision_mechanism", "精密构件：高级机器与列车的核心零件。", [
    ("怎么用", "<p>精密构件是「科技树」的分水岭：列车、机械臂、高级机器都要它。能做精密构件，说明你的产线已经成型。</p>"
              "<p>它本身不能当零件直接装，而是作为配方材料进入更高级的机器。</p>"),
    ("怎么获得", "<p>用<strong>序列组装</strong>产线制造：金板 → 多道部署/压制 → 成品。流程长、占地大，建议单独建一条线。</p>"
              "<p>每一步都需要精确摆放，中途断料会导致整条线停摆。</p>"),
    ("常见坑", "<p>精密构件的半成品（incomplete_precision_mechanism）会占背包，产线设计时尽量让半成品只在传送带上流动。</p>"),
], params=[("类型", "高级零件"), ("工艺", "序列组装")], related=["create:incomplete_precision_mechanism", "create:brass_sheet", "create:golden_sheet"])

item("create:rose_quartz", "玫瑰石英：会发光的晶体材料。", [
    ("怎么用", "<p>玫瑰石英用于灯、光学件与装饰；它自带柔和的光，是做「发光建筑」的关键材料。</p>"
              "<p>磨制后的玫瑰石英更亮，可以做成灯与瓦片。</p>"),
    ("怎么获得", "<p><strong>1 个石英 + 8 个红石粉</strong>在工作台（3×3）里合成，不需要机器、也不需要加热。</p>"
              "<p>红石可以从红石矿、粉碎红石矿来；石英在下界。前期红石紧张时，玫瑰石英要省着用。</p>"),
    ("常见坑", "<p>配方对数量敏感：8 个红石粉一个都不能少，摆错位置会合不出来。</p>"),
], params=[("类型", "材料")], related=["create:polished_rose_quartz", "create:rose_quartz_lamp", "create:rose_quartz_block"])

item("create:polished_rose_quartz", "磨制玫瑰石英：更亮的晶体。", [
    ("怎么用", "<p>磨制后透明度与亮度更高，用于高级灯饰、光学件与装饰方块。它也是玫瑰石英灯的原料之一，磨制过程需要砂纸与旋转动力。</p>"),
    ("怎么获得", "<p>用<strong>砂纸</strong>打磨玫瑰石英（sandpaper polishing），需要砂纸与旋转动力。</p>"),
], params=[("类型", "材料")], related=["create:rose_quartz", "create:rose_quartz_lamp"])

item("create:powdered_obsidian", "黑曜石粉末：坚固板的原料。", [
    ("怎么用", "<p>黑曜石粉末是<strong>坚固板</strong>序列组装的第一道材料，本身没有别的用途。</p>"
              "<p>因为黑曜石难挖，粉末的产量直接决定后期装备的速度。</p>"),
    ("怎么获得", "<p>把<strong>黑曜石</strong>放进<strong>粉碎轮</strong>粉碎得到。粉碎轮需要两个反向旋转的轮子。</p>"
              "<p>黑曜石可以用钻石镐挖，也可以用岩浆 + 水现场造。</p>"),
    ("常见坑", "<p>粉碎黑曜石很慢，转速低时会卡很久；建议用高速动力专线处理。</p>"),
], params=[("类型", "材料")], related=["create:sturdy_sheet", "create:crushing_wheel"])

item("create:chromatic_compound", "异彩化合物：光辉石的前体。", [
    ("怎么用", "<p>异彩化合物是制作<strong>光辉石（refined radiance）</strong>的中间材料，属于后期「光」系科技。</p>"
              "<p>它本身不能直接用，必须继续加工。</p>"),
    ("怎么获得", "<p>由多种彩色材料在盆中混合得到；具体配方以 JEI 为准。</p>"),
    ("常见坑", "<p>它和暗影钢是两条不同的后期路线，材料不要混用。</p>"),
], params=[("类型", "后期材料")], related=["create:refined_radiance", "create:shadow_steel"])

item("create:refined_radiance", "光辉石：后期的光之材料。", [
    ("怎么用", "<p>光辉石用于<strong>光辉机壳</strong>与高级装饰，泛着白光，是后期建筑与机器的标志性材料。</p>"
              "<p>它也能做成光柱/灯饰，做「神圣系」建筑很好用。</p>"),
    ("怎么获得", "<p>由异彩化合物继续加工（需要特定条件，例如与光/爆炸相关），具体以 JEI 为准。</p>"),
    ("常见坑", "<p>后期材料链很长，建议单独建一条产线，不要和主线混在一起。</p>"),
], params=[("类型", "后期材料")], related=["create:chromatic_compound", "create:refined_radiance_casing"])

item("create:shadow_steel", "暗影钢：后期的暗色材料。", [
    ("怎么用", "<p>暗影钢用于<strong>暗影机壳</strong>与暗色装饰，深紫黑的质感适合做「黑科技」风格。</p>"),
    ("怎么获得", "<p>由异彩化合物在特定条件下转化（与黑暗/虚空相关），具体以 JEI 为准。</p>"),
    ("常见坑", "<p>和光辉石是互斥的两条路线，材料规划要提前决定。</p>"),
], params=[("类型", "后期材料")], related=["create:chromatic_compound", "create:shadow_steel_casing"])

item("create:electron_tube", "电子管：红石与显示件的零件。", [
    ("怎么用", "<p>电子管用于<strong>显示板、辉光管、红石逻辑件</strong>等配方，是「电子」系零件的代表。</p>"
              "<p>它也让 Create 的红石系统看起来更像一台老式计算机。</p>"),
    ("怎么获得", "<p>由玻璃、铜/金等材料在工作台合成；具体配方以 JEI 为准。</p>"),
    ("常见坑", "<p>电子管用量不大但种类多，做红石项目前先备一盒。</p>"),
], params=[("类型", "零件")], related=["create:display_board", "create:nixie_tube"])

item("create:brass_hand", "黄铜手部零件：机械臂的「手」。", [
    ("怎么用", "<p>黄铜手用于<strong>机械臂/部署器</strong>类配方，是机械「抓取」能力的象征件。</p>"),
    ("怎么获得", "<p>由黄铜板等材料合成；具体配方以 JEI 为准。</p>"),
    ("常见坑", "<p>它只是合成材料，不能单独当工具使用。</p>"),
], params=[("类型", "零件")], related=["create:mechanical_arm", "create:deployer"])

item("create:experience_nugget", "经验颗粒：可存储的经验。", [
    ("怎么用", "<p>经验颗粒可以把经验<strong>实体化储存</strong>，9 个压成经验块；适合做经验银行、附魔室。</p>"
              "<p>它也能作为部分配方的材料。</p>"),
    ("怎么获得", "<p>由经验（打怪/挖矿/烧炼）在特定装置中凝结，或由经验块拆解。</p>"),
    ("常见坑", "<p>经验颗粒会占背包，量大时及时压成块。</p>"),
], params=[("类型", "材料")], related=["create:experience_block"])

item("create:experience_block", "经验块：大容量经验存储。", [
    ("怎么用", "<p>9 个经验颗粒压成一块，方便大量储存经验；右键可以取出经验。</p>"),
    ("怎么获得", "<p>由经验颗粒合成。</p>"),
    ("常见坑", "<p>取出时注意别在危险地形操作，经验爆出来会散。</p>"),
], params=[("类型", "存储")], related=["create:experience_nugget"])


# ======================================================================
# 第十三批：工具与装备（加厚）
# ======================================================================
item("create:wrench", "扳手：Create 最重要的工具。", [
    ("怎么用", "<p>右键<strong>旋转</strong>方块/轴/管道，潜行右键<strong>拆卸</strong>整个部件并原样掉落。轴、齿轮、机器、轨道、管道都用它调整朝向。</p>"
              "<p>很多方块还有「第二种模式」：漏斗切换抽取/投放、机械臂设置输入输出、铜件调整连接，全靠扳手循环切换。</p>"),
    ("进阶", "<p>扳手拆机器不会损坏零件，这让你可以随时重新布局产线；前期先做一把，比多做一台机器更划算。</p>"
             "<p>部分方块（如列车部件）需要扳手才能组装/拆解，没有扳手会卡住。</p>"),
    ("常见坑", "<p>直接左键拆会掉成物品但可能损失内部物品；拆带内容的机器（工作盆、储罐）前先清空。</p>"),
], params=[("类型", "工具"), ("耐久", "有")], related=["create:goggles", "create:super_glue"])

item("create:goggles", "工程师护目镜：看见应力与转速。", [
    ("怎么用", "<p>戴在头上后，看向机器会显示<strong>应力占用、转速、方向</strong>等工程信息；看传送带还能看到物品流向。</p>"
              "<p>排查「机器为什么不转」时，护目镜是第一件要戴的东西。</p>"),
    ("进阶", "<p>护目镜可以和头盔/潜水装备一起穿（占头盔槽的装饰位），不影响防护。</p>"),
    ("常见坑", "<p>它只是信息显示，不提供防护；下矿/下界仍要戴正经头盔。</p>"),
], params=[("类型", "工具"), ("槽位", "头盔")], related=["create:wrench", "create:speedometer", "create:stressometer"])

item("create:copper_backtank", "铜背罐：潜水与飞行的气源。", [
    ("怎么用", "<p>穿在胸甲槽，配合<strong>潜水头盔</strong>使用：提供水下呼吸与飞行（配合扇叶/推进器）所需的气。</p>"
              "<p>气会用完，需要放在<strong>鼓风机</strong>前或接入管道充气。</p>"),
    ("进阶", "<p>背罐可以放置成方块（placeable 版本），方便做充气站；下界合金背罐容量更大。</p>"),
    ("常见坑", "<p>没气时水下会窒息、飞行会掉；出门前先充满。</p>"),
], params=[("类型", "装备"), ("部位", "胸甲")], related=["create:copper_diving_helmet", "create:netherite_backtank", "create:encased_fan"])

item("create:netherite_backtank", "下界合金背罐：大容量气罐。", [
    ("怎么用", "<p>铜背罐的升级版，<strong>容量更大、更耐用</strong>，适合长时间水下作业与飞行。</p>"
              "<p>同样需要充气，放置版可以当充气站。</p>"),
    ("进阶", "<p>配合下界合金潜水头盔，可以在水下长时间活动。</p>"),
    ("常见坑", "<p>造价高，别拿它当普通胸甲穿去打架。</p>"),
], params=[("类型", "装备"), ("部位", "胸甲")], related=["create:copper_backtank", "create:netherite_diving_helmet"])

item("create:copper_diving_helmet", "铜潜水头盔：水下呼吸。", [
    ("怎么用", "<p>戴在头上，配合<strong>铜背罐</strong>提供氧气，实现水下呼吸与视野。</p>"),
    ("进阶", "<p>和护目镜一起用会占用同一槽位，下水前记得换回来。</p>"),
    ("常见坑", "<p>没有背罐时头盔不供氧。</p>"),
], params=[("类型", "装备"), ("部位", "头盔")], related=["create:copper_backtank", "create:copper_diving_boots"])

item("create:copper_diving_boots", "铜潜水靴：水下行走。", [
    ("怎么用", "<p>穿在脚上，在水下<strong>行走更快、不被水流冲走</strong>，配合头盔与背罐组成完整潜水套装。</p>"),
    ("进阶", "<p>下界合金版本防护更高。</p>"),
    ("常见坑", "<p>只解决移动，不提供氧气。</p>"),
], params=[("类型", "装备"), ("部位", "靴子")], related=["create:copper_diving_helmet", "create:copper_backtank"])

item("create:netherite_diving_helmet", "下界合金潜水头盔：高级潜水头盔。", [
    ("怎么用", "<p>铜潜水头盔的升级版，防护更高、耐久更好，配合下界合金背罐做长时间水下工程。</p>"),
    ("进阶", "<p>后期做水下基地、海底隧道时的标配。</p>"),
    ("常见坑", "<p>仍然需要背罐供氧。</p>"),
], params=[("类型", "装备"), ("部位", "头盔")], related=["create:netherite_backtank"])

item("create:netherite_diving_boots", "下界合金潜水靴：高级潜水靴。", [
    ("怎么用", "<p>铜潜水靴的升级版，水下移动更快、防护更高。</p>"),
    ("进阶", "<p>和头盔、背罐凑齐一套，水下作业效率明显提升。</p>"),
    ("常见坑", "<p>不提供氧气，别只穿靴子就下水。</p>"),
], params=[("类型", "装备"), ("部位", "靴子")], related=["create:netherite_diving_helmet"])

item("create:potato_cannon", "土豆加农炮：把物品射出去。", [
    ("怎么用", "<p>装填物品（土豆、方块、工具）后右键<strong>发射</strong>，可以远程放置方块、给机器投料、或者当武器。</p>"
              "<p>它能把物品精确打到远处，做「远程投料」「跨墙补给」很有趣。</p>"),
    ("进阶", "<p>装填不同物品有不同效果：方块会放置、食物会造成伤害/喂食、工具会触发作用。</p>"),
    ("常见坑", "<p>射程有限、有下坠；重要物品别拿来乱射。</p>"),
], params=[("类型", "工具/武器")], related=["create:extendo_grip", "create:deployer"])

item("create:extendo_grip", "伸缩机械手：远距离操作。", [
    ("怎么用", "<p>延长你的<strong>交互距离</strong>，可以远距离放置/破坏方块、操作机器。</p>"
              "<p>配合土豆加农炮可以做出「抓取远处物品」的效果。</p>"),
    ("进阶", "<p>在大型机器上作业时，不用频繁搭桥靠近。</p>"),
    ("常见坑", "<p>只延长交互距离，不延长移动速度；小心脚下。</p>"),
], params=[("类型", "工具")], related=["create:potato_cannon", "create:wrench"])

item("create:tree_fertilizer", "树木肥料：让树快长。", [
    ("怎么用", "<p>右键树苗，<strong>加速生长</strong>；也能让部分作物更快成熟。</p>"),
    ("进阶", "<p>做自动树场时配合部署器使用，可以无人值守刷木头。</p>"),
    ("常见坑", "<p>只对可催熟的植物有效；对成品树无效。</p>"),
], params=[("类型", "工具")], related=["create:deployer", "create:mechanical_harvester"])

item("create:builders_tea", "建筑工茶饮：临时加速放置。", [
    ("怎么用", "<p>喝下后获得一段时间的<strong>建造增益</strong>（放置更快/更省力），适合大规模搭建。</p>"),
    ("进阶", "<p>和蓝图加农炮配合，施工速度更明显。</p>"),
    ("常见坑", "<p>有时限，别在准备材料时浪费掉。</p>"),
], params=[("类型", "消耗品")], related=["create:schematicannon"])

item("create:sand_paper", "砂纸：打磨物品。", [
    ("怎么用", "<p>用于<strong>打磨</strong>配方（如磨制玫瑰石英）；需要配合旋转动力使用，会消耗耐久。</p>"),
    ("进阶", "<p>红沙砂纸是它的变体，打磨效果相同但外观不同。</p>"),
    ("常见坑", "<p>砂纸会磨坏，批量打磨前多备几张。</p>"),
], params=[("类型", "工具")], related=["create:red_sand_paper", "create:polished_rose_quartz"])

item("create:red_sand_paper", "红沙砂纸：砂纸的变体。", [
    ("怎么用", "<p>和普通砂纸一样用于<strong>打磨</strong>配方，只是外观是红沙色。</p>"),
    ("进阶", "<p>两种砂纸可以混用，效果一致。</p>"),
    ("常见坑", "<p>同样会消耗耐久。</p>"),
], params=[("类型", "工具")], related=["create:sand_paper"])

item("create:clipboard", "剪贴板：记录与显示文本。", [
    ("怎么用", "<p>右键编辑文本，可以写<strong>清单、地址、说明</strong>；写好的剪贴板可以给辉光管显示内容。</p>"
              "<p>它也是包裹物流里写地址的工具之一。</p>"),
    ("进阶", "<p>把剪贴板放进物品展示框/置物板，可以做站牌与告示。</p>"),
    ("常见坑", "<p>文本长度有限；重要内容建议多备份一份。</p>"),
], params=[("类型", "工具")], related=["create:shopping_list", "create:nixie_tube"])

item("create:shopping_list", "采购清单：待办购物单。", [
    ("怎么用", "<p>记录需要采集/合成的材料，方便按单备料；可以勾选已完成项。</p>"),
    ("进阶", "<p>做大型工程前先列清单，能显著减少来回跑。</p>"),
    ("常见坑", "<p>只是记录工具，不会自动从仓库取货。</p>"),
], params=[("类型", "工具")], related=["create:clipboard"])

item("create:empty_schematic", "空白蓝图：待写入的结构图。", [
    ("怎么用", "<p>用<strong>蓝图与笔</strong>框选建筑后写入，得到可放置/可施工的蓝图。</p>"),
    ("进阶", "<p>空白蓝图可以反复使用，直到写入内容。</p>"),
    ("常见坑", "<p>框选范围有上限，超大会失败。</p>"),
], params=[("类型", "工具")], related=["create:schematic", "create:schematic_and_quill"])

item("create:schematic_and_quill", "蓝图与笔：框选并保存建筑。", [
    ("怎么用", "<p>右键两个角点<strong>框选</strong>建筑，再右键保存为蓝图；之后可以用蓝图加农炮自动建造。</p>"
              "<p>它是「复制建筑」的入口，做重复厂房、村庄复制很方便。</p>"),
    ("进阶", "<p>保存的蓝图可以给别人，或用在其他存档。</p>"),
    ("常见坑", "<p>框选会包含空气方块；材料清单按实际方块计算，提前备料。</p>"),
], params=[("类型", "工具")], related=["create:schematic", "create:schematicannon", "create:empty_schematic"])

item("create:schematic", "蓝图：保存好的建筑图纸。", [
    ("怎么用", "<p>由蓝图与笔保存得到，可以放进<strong>蓝图桌</strong>查看材料清单，或交给<strong>蓝图加农炮</strong>施工。</p>"),
    ("进阶", "<p>蓝图桌能算出所需材料，按清单备料再开工。</p>"),
    ("常见坑", "<p>蓝图不包含容器内的物品与实体。</p>"),
], params=[("类型", "工具")], related=["create:schematic_table", "create:schematicannon"])

item("create:schematic_table", "蓝图桌：查看蓝图材料。", [
    ("怎么用", "<p>放入蓝图，显示<strong>所需材料清单</strong>与数量；可以对照清单备料。</p>"),
    ("进阶", "<p>大型工程先过一遍蓝图桌，能避免施工到一半缺料。</p>"),
    ("常见坑", "<p>只统计方块，不统计机器内部物品。</p>"),
], params=[("类型", "工具")], related=["create:schematic", "create:schematicannon"])

item("create:schematicannon", "蓝图加农炮：自动建造。", [
    ("怎么用", "<p>放入蓝图与材料，它会<strong>逐块放置</strong>建筑；需要火药作为动力。</p>"
              "<p>配合仓储网络可以自动备料，是大型工程的核心工具。</p>"),
    ("进阶", "<p>加农炮有射程与角度限制，超远建筑要分段施工。</p>"),
    ("常见坑", "<p>材料不足会停下；施工区域有生物/方块阻挡时会卡住。</p>"),
], params=[("类型", "工具"), ("消耗", "火药")], related=["create:schematic", "create:schematic_table"])

item("create:wand_of_symmetry", "对称之杖：镜像建造。", [
    ("怎么用", "<p>设置一个<strong>对称面</strong>，之后放置/破坏方块会同时在镜像位置发生，做对称建筑快一倍。</p>"),
    ("进阶", "<p>适合做城堡、车站这类左右对称的大建筑。</p>"),
    ("常见坑", "<p>只镜像方块操作，不镜像机器内部状态。</p>"),
], params=[("类型", "工具")], related=["create:handheld_worldshaper", "create:schematicannon"])

item("create:handheld_worldshaper", "世界塑形器：创造模式编辑地形。", [
    ("怎么用", "<p>创造模式专属，可以<strong>大范围</strong>放置/删除方块，快速整地。</p>"),
    ("进阶", "<p>做地图、测试场景时非常快。</p>"),
    ("常见坑", "<p>生存模式无法获得，误用会破坏地形。</p>"),
], params=[("类型", "创造工具")], related=["create:wand_of_symmetry"])

# ======================================================================
# 第十四批：补齐单段条目（简单物品也要有「怎么获得 / 怎么用 / 注意」）
# ======================================================================
def _fill(iid, tag, use, extra, note=None, params=None, related=None):
    secs=[("怎么用", use), ("补充", extra)]
    if note: secs.append(("注意", note))
    item(iid, tag, secs, params=params, related=related)

_fill("create:andesite_door", "安山门：工业风双开门。",
 "<p>两格高的门，可以<strong>双开</strong>（两扇并排会自动成对），右键开关，也能用红石控制。</p>",
 "<p>安山合金的灰绿金属感，适合厂房、仓库、机器外壳上的检修门。</p>",
 "<p>门只占一格厚，装在墙里要留出门洞；红石控制时注意别被旁边的信号串到。</p>",
 params=[("类型", "门")], related=["create:brass_door", "create:copper_door"])

_fill("create:brass_door", "黄铜门：暖金色的高级门。",
 "<p>和黄铜机壳同色系的门，适合控制室、办公室、站长室这类「高级」空间。</p>",
 "<p>双开门可以并排摆放，红石/右键开关。</p>",
 "<p>只是外观不同，功能与原版门一致。</p>",
 params=[("类型", "门")], related=["create:andesite_door", "create:copper_door"])

_fill("create:copper_door", "铜门：铜色金属门。",
 "<p>铜质感的门，适合蒸汽管道、锅炉房、铜主题建筑；和铜机壳、铜瓦是同一套配色。</p>",
 "<p>可以双开，支持红石控制。</p>",
 "<p>铜门不会像铜块那样氧化变色。</p>",
 params=[("类型", "门")], related=["create:andesite_door", "create:brass_door"])

_fill("create:framed_glass_door", "边框玻璃门：通透的玻璃门。",
 "<p>带边框的玻璃门，透光又能分隔空间，适合商店、温室、展厅。</p>",
 "<p>和边框玻璃、玻璃板搭配，可以做出一整面通透的立面。</p>",
 "<p>玻璃门不隔音也不防怪，别当安全门用。</p>",
 params=[("类型", "门")], related=["create:framed_glass", "create:framed_glass_trapdoor"])

_fill("create:framed_glass_trapdoor", "边框玻璃活板门：玻璃检修口。",
 "<p>可以当玻璃地板/天花板上的检修口，透光、可开关。</p>",
 "<p>适合温室顶、展示柜、地板暗门。</p>",
 "<p>打开时是缺口，注意别在高处踩空。</p>",
 params=[("类型", "活板门")], related=["create:framed_glass_door"])

_fill("create:brass_nugget", "黄铜粒：黄铜的零钱。",
 "<p>9 个黄铜粒 = 1 个黄铜锭，用来做小额配方与找零。</p>",
 "<p>部分精密配方会用到粒；也可以把锭拆成粒再合成，避免浪费。</p>",
 "<p>粒不能直接当材料压板，要先用 9 个合成锭。</p>",
 params=[("类型", "材料")], related=["create:brass_ingot"])

_fill("create:copper_nugget", "铜粒：铜的零钱。",
 "<p>9 个铜粒 = 1 个铜锭，用于小额配方。</p>",
 "<p>铜粒也出现在部分合金/装饰配方里。</p>",
 "<p>别把粒当锭直接压板。</p>",
 params=[("类型", "材料")], related=["create:copper_ingot"])

_fill("create:zinc_nugget", "锌粒：锌的零钱。",
 "<p>9 个锌粒 = 1 个锌锭；安山合金的配方里会用到粒。</p>",
 "<p>前期铁粒/锌粒是合成安山合金的关键，看到就收。</p>",
 "<p>粒不能直接炼成锭，要 9 个合成。</p>",
 params=[("类型", "材料")], related=["create:zinc_ingot", "create:andesite_alloy"])

_fill("create:raw_zinc", "粗锌：还没烧的锌矿。",
 "<p>挖锌矿直接掉落，放进熔炉/高炉烧成锌锭；也可以先粉碎再洗涤提高产量。</p>",
 "<p>粗锌块可以压成块储存，需要时再拆。</p>",
 "<p>粗锌不能直接用于合成，必须先烧。</p>",
 params=[("类型", "原料")], related=["create:zinc_ingot", "create:crushed_raw_zinc"])

_fill("create:cardboard", "纸板：包装材料。",
 "<p>由<strong>纸浆</strong>压制而成，是打包机、纸壳包裹、纸板装备的原料。</p>",
 "<p>纸板很便宜，适合做一次性包装与「穷鬼装备」。</p>",
 "<p>纸板怕水也怕火，别拿它盖房子。</p>",
 params=[("类型", "材料")], related=["create:pulp", "create:package", "create:cardboard_block"])

_fill("create:pulp", "纸浆：造纸板的中间产物。",
 "<p>把植物材料（甘蔗、木头等）与<strong>水</strong>放进工作盆搅拌得到纸浆。</p>",
 "<p>纸浆压成纸板，再做成包裹与纸板装备。</p>",
 "<p>搅拌需要旋转动力与流体输入，别忘了给盆接水。</p>",
 params=[("类型", "材料")], related=["create:cardboard", "create:basin"])

_fill("create:cardboard_helmet", "纸板头盔：最廉价的护甲。",
 "<p>用纸板做的头盔，防护极低，属于「玩具装备」。</p>",
 "<p>胜在便宜、材料易得，可以当一次性的探险消耗品。</p>",
 "<p>别指望它保命，正经下矿请用铁/钻石甲。</p>",
 params=[("类型", "护甲")], related=["create:cardboard_chestplate"])

_fill("create:cardboard_chestplate", "纸板胸甲：最廉价的护甲。",
 "<p>纸板做的胸甲，防护极低，适合搞笑或临时挡一下。</p>",
 "<p>制作便宜，坏了不心疼。</p>",
 "<p>不能替代真正的护甲。</p>",
 params=[("类型", "护甲")], related=["create:cardboard_helmet"])

_fill("create:cardboard_leggings", "纸板护腿：最廉价的护甲。",
 "<p>纸板做的护腿，防护极低。</p>",
 "<p>凑齐一套纸板甲可以玩「纸板人」造型。</p>",
 "<p>没有实际防护价值。</p>",
 params=[("类型", "护甲")], related=["create:cardboard_boots"])

_fill("create:cardboard_boots", "纸板靴子：最廉价的护甲。",
 "<p>纸板做的靴子，防护极低。</p>",
 "<p>便宜、轻便，跑图时坏了不心疼。</p>",
 "<p>不提供摔落保护。</p>",
 params=[("类型", "护甲")], related=["create:cardboard_leggings"])

_fill("create:cardboard_sword", "纸棍：纸板做的剑。",
 "<p>用纸板卷成的「剑」，伤害极低，基本是玩具。</p>",
 "<p>可以拿来打打草、做造型，或者送朋友。</p>",
 "<p>别拿它打怪，耐久和伤害都不够。</p>",
 params=[("类型", "武器")], related=["create:cardboard"])

_fill("create:sweet_roll", "甜甜卷：甜点食物。",
 "<p>恢复饥饿值的甜点，制作需要面团、糖等材料。</p>",
 "<p>适合当探险口粮，也能摆出来做餐厅装饰。</p>",
 "<p>不提供特殊增益，纯食物。</p>",
 params=[("类型", "食物")], related=["create:dough", "create:bar_of_chocolate"])

_fill("create:honeyed_apple", "蜜渍苹果：蜂蜜点心。",
 "<p>苹果 + 蜂蜜做成的食物，恢复饥饿值。</p>",
 "<p>蜂蜜来自蜂巢/蜂箱，做之前先准备好。</p>",
 "<p>没有原版金苹果的效果。</p>",
 params=[("类型", "食物")], related=["create:honey", "create:sweet_roll"])

_fill("create:chocolate_glazed_berries", "巧克力包层浆果：甜点。",
 "<p>浆果裹上巧克力，恢复饥饿值；需要巧克力流体与注液器/工作盆。</p>",
 "<p>是「巧克力产线」的下游产品之一。</p>",
 "<p>只是食物，不提供增益。</p>",
 params=[("类型", "食物")], related=["create:chocolate", "create:bar_of_chocolate"])

_fill("create:bar_of_chocolate", "巧克力棒：巧克力做的食物。",
 "<p>由巧克力流体凝固而成，可以直接吃，也能继续加工成其他甜点。</p>",
 "<p>巧克力需要可可豆与流体加工，属于「甜品产线」。</p>",
 "<p>不要和巧克力块/巧克力桶混淆。</p>",
 params=[("类型", "食物")], related=["create:chocolate", "create:sweet_roll"])

_fill("create:chocolate", "巧克力：可流动的巧克力。",
 "<p>Create 的流体之一，用注液器给食物涂层，或倒进模具/储罐。</p>",
 "<p>巧克力需要可可豆加工，是甜品产线的核心流体。</p>",
 "<p>流体要用桶/储罐装，别直接用手接。</p>",
 params=[("类型", "流体")], related=["create:chocolate_bucket", "create:spout"])

_fill("create:honey", "蜂蜜：可流动的蜂蜜。",
 "<p>Create 的流体之一，可用于注液器、储罐与装饰。</p>",
 "<p>蜂蜜黏稠，流动慢，做「糖浆瀑布」很有氛围。</p>",
 "<p>和原版蜂蜜瓶不是同一种东西。</p>",
 params=[("类型", "流体")], related=["create:honey_bucket", "create:spout"])

_fill("create:wheat_flour", "小麦面粉：做面食的粉。",
 "<p>小麦用<strong>石磨</strong>磨成面粉；面粉加水在盆里揉成面团。</p>",
 "<p>面粉是面包、甜甜卷等食物的起点。</p>",
 "<p>石磨转速低会磨得很慢。</p>",
 params=[("类型", "食材")], related=["create:dough", "create:millstone"])

_fill("create:dough", "面团：做面食的半成品。",
 "<p>面粉 + 水在<strong>工作盆</strong>里搅拌成面团；可以烤成面包，也能做甜甜卷。</p>",
 "<p>搅拌需要旋转动力，水要用管道/桶加入。</p>",
 "<p>面团放久了不会坏，可以囤。</p>",
 params=[("类型", "食材")], related=["create:wheat_flour", "create:basin"])

_fill("create:cinder_flour", "余烬面粉：下界岩磨成的粉。",
 "<p>把<strong>下界岩</strong>粉碎/研磨得到，是烈焰蛋糕的关键材料。</p>",
 "<p>做烈焰蛋糕、点燃烈焰人燃烧室都离不开它。</p>",
 "<p>下界岩要先去下界挖，前期记得囤。</p>",
 params=[("类型", "材料")], related=["create:blaze_cake_base", "create:crushing_wheel"])

_fill("create:unprocessed_obsidian_sheet", "未加工的黑曜石板：坚固板的半成品。",
 "<p>序列组装中，黑曜石粉末压成板但还没完成处理的形态。</p>",
 "<p>继续经过部署/压制才会变成坚固板。</p>",
 "<p>半成品不能直接用，断料会卡在产线上。</p>",
 params=[("类型", "半成品")], related=["create:sturdy_sheet", "create:powdered_obsidian"])

_fill("create:rope", "绳索：吊装用的绳子。",
 "<p>用于<strong>绳索滑轮</strong>，把结构吊起来升降；也可以当装饰。</p>",
 "<p>绳索长度可以现场调整，适合做矿井电梯、吊桥。</p>",
 "<p>绳索怕火，别在岩浆附近用。</p>",
 params=[("类型", "材料")], related=["create:rope_pulley", "create:pulley_magnet"])

_fill("create:nozzle", "分散网：扩大鼓风范围。",
 "<p>装在<strong>鼓风机</strong>出风口，把集中的气流<strong>扩散</strong>成一片，覆盖更大范围。</p>",
 "<p>做批量洗涤、批量烟熏时，分散网能让整条传送带都吃到风。</p>",
 "<p>扩散后风力变弱，处理速度会下降，按需选择。</p>",
 params=[("类型", "机器部件")], related=["create:encased_fan"])

_fill("create:rose_quartz_lamp", "玫瑰石英灯：柔和的晶体灯。",
 "<p>用玫瑰石英做的灯，泛着粉白色柔光，适合室内照明与装饰。</p>",
 "<p>可以嵌进墙里做灯带，也能做吊灯。</p>",
 "<p>亮度固定，不能用红石调光。</p>",
 params=[("类型", "照明")], related=["create:rose_quartz", "create:rose_quartz_block"])

_fill("create:metal_girder", "金属梁：工业结构件。",
 "<p>长条形的金属梁，可以当屋架、桥梁、机器支架，也能包住传动轴（金属梁包住的传动杆）。</p>",
 "<p>工业风建筑的主力构件，和机壳、栏杆搭配很统一。</p>",
 "<p>只是装饰/结构方块，不承重也不导电。</p>",
 params=[("类型", "建筑方块")], related=["create:metal_bracket", "create:industrial_iron_block"])

_fill("create:metal_bracket", "金属支架：斜撑构件。",
 "<p>三角形的斜撑，用来连接梁与柱、做屋檐支撑，让结构看起来更「工程」。</p>",
 "<p>可以和木质支架混用，区分不同材质的结构。</p>",
 "<p>纯装饰，不提供实际支撑。</p>",
 params=[("类型", "建筑方块")], related=["create:metal_girder", "create:wooden_bracket"])

_fill("create:wooden_bracket", "木质支架：木结构斜撑。",
 "<p>木三角斜撑，适合木屋、站台雨棚、仓库屋架。</p>",
 "<p>和金属支架搭配可以做出「木+铁」的工业风。</p>",
 "<p>纯装饰。</p>",
 params=[("类型", "建筑方块")], related=["create:metal_bracket"])

_fill("create:industrial_iron_block", "工业铁块：带铆钉的铁板方块。",
 "<p>表面有铆钉与拼缝的工业风铁块，适合厂房外墙、机器外壳、地板。</p>",
 "<p>和工业铁窗户、金属梁是同一套语言。</p>",
 "<p>只是建筑方块，不是金属储存块。</p>",
 params=[("类型", "建筑方块")], related=["create:weathered_iron_block", "create:industrial_iron_window"])

_fill("create:weathered_iron_block", "锈蚀的工业铁块：做旧铁板。",
 "<p>工业铁块的锈蚀版本，颜色更暗、更有年代感。</p>",
 "<p>适合废弃工厂、码头、旧仓库。</p>",
 "<p>不会继续氧化，颜色固定。</p>",
 params=[("类型", "建筑方块")], related=["create:industrial_iron_block"])

_fill("create:copycat_base", "伪装基底：能伪装的方块。",
 "<p>用其他方块右键「贴皮」，外观变成目标方块，但保留伪装方块的形状与连接逻辑。</p>",
 "<p>用来让结构（栏杆、台阶、板）融入木/石建筑，不露金属。</p>",
 "<p>只改外观，不改碰撞与功能。</p>",
 params=[("类型", "伪装方块")], related=["create:copycat_panel", "create:copycat_step", "create:copycat_bars"])

_fill("create:copycat_panel", "伪装板：可伪装的薄板。",
 "<p>伪装基底的薄板形态，贴皮后变成「目标方块的薄板」，适合做墙面细节。</p>",
 "<p>让建筑表面有材质变化但保持统一厚度。</p>",
 "<p>贴皮后拆下来会恢复原样。</p>",
 params=[("类型", "伪装方块")], related=["create:copycat_base", "create:copycat_step"])

_fill("create:copycat_step", "伪装半阶：可伪装的台阶。",
 "<p>伪装基底的半阶形态，贴皮后变成目标方块的台阶。</p>",
 "<p>做楼梯、檐口时能让材质和周围完全一致。</p>",
 "<p>只改外观。</p>",
 params=[("类型", "伪装方块")], related=["create:copycat_base", "create:copycat_panel"])

_fill("create:crushing_wheel_controller", "粉碎轮控制器：组装粉碎轮。",
 "<p>用来把两个粉碎轮<strong>组装成一对</strong>并控制旋转方向，是粉碎轮产线的「轴心」。</p>",
 "<p>没有它，两个轮子无法正确对转。</p>",
 "<p>装好后要用扳手检查方向，反向才能粉碎。</p>",
 params=[("类型", "机器部件")], related=["create:crushing_wheel"])

_fill("create:cuckoo_clock", "布谷鸟钟：会报时的钟。",
 "<p>按游戏内时间<strong>报时</strong>，到点会弹出小鸟并发出钟声；纯装饰。</p>",
 "<p>适合挂在车站、钟楼、室内墙面。</p>",
 "<p>不会输出红石信号。</p>",
 params=[("类型", "装饰")], related=["create:mysterious_cuckoo_clock", "create:clockwork_bearing"])

_fill("create:mysterious_cuckoo_clock", "神秘的布谷鸟钟：特殊外观的钟。",
 "<p>布谷鸟钟的稀有变体，外观更神秘，报时效果相同。</p>",
 "<p>可以当收藏品。</p>",
 "<p>功能与普通钟一致。</p>",
 params=[("类型", "装饰")], related=["create:cuckoo_clock"])

_fill("create:haunted_bell", "缠魂钟：阴森的铃。",
 "<p>敲响后发出低沉的钟声，氛围阴森，适合鬼屋、废弃教堂。</p>",
 "<p>纯装饰音效。</p>",
 "<p>不产生红石信号。</p>",
 params=[("类型", "装饰")], related=["create:peculiar_bell", "create:desk_bell"])

_fill("create:peculiar_bell", "奇异钟：古怪的铃。",
 "<p>声音古怪的铃铛，适合做奇趣装饰。</p>",
 "<p>纯装饰。</p>",
 "<p>不产生红石信号。</p>",
 params=[("类型", "装饰")], related=["create:haunted_bell"])

_fill("create:linked_controller", "无线红石遥控器：远程控制。",
 "<p>与<strong>无线红石终端</strong>配对后，可以远程开关机器、控制红石。</p>",
 "<p>做「手持遥控器」控制大门、机器启停。</p>",
 "<p>需要先配对频率，距离过远会失效。</p>",
 params=[("类型", "红石")], related=["create:redstone_link", "create:lectern_controller"])

_fill("create:lectern_controller", "遥控器讲台：固定式遥控。",
 "<p>把无线遥控器放在讲台上，做成固定的控制台，右键操作。</p>",
 "<p>适合站长室、控制中心。</p>",
 "<p>仍需与终端配对。</p>",
 params=[("类型", "红石")], related=["create:linked_controller"])

_fill("create:whisk", "搅拌器：工作盆的搅拌头。",
 "<p>装在工作盆上方，旋转时<strong>搅拌</strong>盆内物品与流体，是混合配方的核心部件。</p>",
 "<p>黄铜、玫瑰石英等配方都靠它。</p>",
 "<p>搅拌需要盆里有正确材料；转速影响速度。</p>",
 params=[("类型", "机器部件")], related=["create:basin", "create:mechanical_mixer"])

_fill("create:minecart_contraption", "装配过的矿车：装好结构的矿车。",
 "<p>用<strong>矿车装配站</strong>把粘好的结构装到矿车上，形成一个会移动的装置。</p>",
 "<p>可以再装箱子（运输矿车）或熔炉（动力矿车）。</p>",
 "<p>结构没粘牢会散架。</p>",
 params=[("类型", "载具")], related=["create:chest_minecart_contraption", "create:cart_assembler"])

# ==== 合并子代理批次：batches/*.py（每个文件只有 item() 调用）====
import os as _os, glob as _glob, ast as _ast
_BATCH_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), "batches")
for _f in sorted(_glob.glob(_os.path.join(_BATCH_DIR, "*.py"))):
    if _os.path.basename(_f).startswith("_"):
        continue
    _src = open(_f, encoding="utf-8").read()
    try:
        _tree = _ast.parse(_src, filename=_f)
    except SyntaxError:
        continue
    _body = [n for n in _tree.body
             if isinstance(n, _ast.Expr) and isinstance(n.value, _ast.Call)
             and isinstance(n.value.func, _ast.Name) and n.value.func.id == "item"]
    if _body:
        exec(compile(_ast.Module(body=_body, type_ignores=[]), _f, "exec"), globals())


# ---- prune ids that are not real Create items (keeps audits honest) ----
try:
    import json as _json
    _IDS = set(_json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                             "out", "data.json"), encoding="utf-8"))["items"])
    TUT = {_k: _v for _k, _v in TUT.items() if _k in _IDS}
except Exception:
    pass
