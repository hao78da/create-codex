import re

P = r"D:\frontend\_raw\batches\k2.py"
src = open(P, encoding="utf-8").read()

PATCH = {
("create:mechanical_pump", "怎么获得", 0): "泵本身不挑材质，做多少台都用同一个配方。",
("create:mechanical_pump", "怎么获得", 1): "管道一次出四根，做泵剩下的正好拿去铺线。",
("create:mechanical_pump", "怎么用", 0): "箭头贴在泵的侧面上，隔着玻璃也能看清。",
("create:mechanical_pump", "怎么用", 1): "泵与泵之间接直管，拐弯处多留一节再装。",
("create:mechanical_pump", "常见坑", 0): "储罐要单独放在管线一端，别塞在泵与泵中间。",
("create:mechanical_pump", "常见坑", 1): "分叉前拿扳手试一下走向，走错了拆窗很费事。",

("create:speedometer", "怎么获得", 0): "表盘只有一个方块大，装在轴上不占地方。",
("create:speedometer", "怎么获得", 1): "铁不够时先做机壳，指南针可以慢慢补。",
("create:speedometer", "怎么用", 0): "读数会随转速实时变化，不用打开任何界面。",
("create:speedometer", "怎么用", 1): "比较器的信号可以直接接灯，超速时一眼看见。",
("create:speedometer", "常见坑", 0): "表背要贴着转轴，贴着机壳只会读到零。",
("create:speedometer", "常见坑", 1): "互转时两块都要拿在手上，摆地上不会自动换。",

("create:weighted_ejector", "怎么获得", 0): "金板不好压，先把压床的模具换成金锭再开工。",
("create:weighted_ejector", "怎么获得", 1): "置物台单独也能用，弹射版只是多了定量功能。",
("create:weighted_ejector", "怎么用", 0): "设定值可以在界面里改，改完不用重新放手。",
("create:weighted_ejector", "怎么用", 1): "目标方块要能被容器识别，对着空气指不会生效。",
("create:weighted_ejector", "常见坑", 0): "台上堆满而数量又设得太高，它就永远不出手。",
("create:weighted_ejector", "常见坑", 1): "弹射方向只认侧面，从顶上指下去不算数。",

("create:brass_belt_funnel", "怎么获得", 0): "安山漏斗贴上去不会变，只有黄铜版才有这待遇。",
("create:brass_belt_funnel", "怎么获得", 1): "干海带要晒过才用，湿的直接放进去不合配方。",
("create:brass_belt_funnel", "怎么用", 0): "挡板伸出后物品会停在带上，正好用来做缓冲。",
("create:brass_belt_funnel", "怎么用", 1): "置入模式要先把物品放进它的漏斗口，不是塞带上。",
("create:brass_belt_funnel", "常见坑", 0): "贴到带子两端之外的空地上，它只会变成普通漏斗。",
("create:brass_belt_funnel", "常见坑", 1): "红石信号断掉后它会自己恢复，不用手动重启。",

("create:fluid_pipe", "怎么获得", 0): "铜板用压床压，铜锭烧粗铜就有，两头都不难。",
("create:fluid_pipe", "怎么获得", 1): "一次四根看着多，铺一条二十格的线就见底了。",
("create:fluid_pipe", "怎么用", 0): "管道之间会自动连上，转角不用额外的接头。",
("create:fluid_pipe", "怎么用", 1): "包壳要拿铜机壳对着管道用，包好后外观统一。",
("create:fluid_pipe", "常见坑", 0): "泵的方向装反了会往回抽，箭头朝哪边要看清楚。",
("create:fluid_pipe", "常见坑", 1): "两根管道中间夹一格别的方块，它们就不会连通。",

("create:polished_rose_quartz", "怎么获得", 0): "八份红石粉一份都不能少，少放就合不出玫瑰石英。",
("create:polished_rose_quartz", "怎么获得", 1): "砂纸磨完一块掉一点耐久，磨十几块就得换新的。",
("create:polished_rose_quartz", "怎么用", 0): "电子管做出来别急着装箱，后面的机壳还要用它。",
("create:polished_rose_quartz", "怎么用", 1): "一块磨制石英只出一个电子管，产量要提前算。",
("create:polished_rose_quartz", "常见坑", 0): "拿玫瑰石英去做电子管会失败，磨制是必要一步。",
("create:polished_rose_quartz", "常见坑", 1): "红石粉用完时合成台会静默失败，不会提示缺料。",

("create:smart_chute", "怎么获得", 0): "黄铜板要先把黄铜锭压薄，电子管则要磨制石英。",
("create:smart_chute", "怎么获得", 1): "一次四个溜槽够搭一条短竖井，长线要多做几轮。",
("create:smart_chute", "怎么用", 0): "面板上还能设定只在收到信号时工作，做阀门方便。",
("create:smart_chute", "怎么用", 1): "投料口要对准下方容器，偏一格物品就掉在地上。",
("create:smart_chute", "常见坑", 0): "过滤填了却不出货，多半是数量被设成了零。",
("create:smart_chute", "常见坑", 1): "它不会把物品往上送，竖井方向要一次摆对。",

("create:clipboard", "怎么获得", 0): "纸与木板随手就有，安山合金才是真正要备的料。",
("create:clipboard", "怎么获得", 1): "做好的剪贴板能放进箱子，不占随身背包的格子。",
("create:clipboard", "怎么用", 0): "写好的清单能直接交给同伙，对方贴到墙上照着做。",
("create:clipboard", "怎么用", 1): "复制设置时要站在方块旁边，隔太远选不中目标。",
("create:clipboard", "常见坑", 0): "贴在墙上后被别的方块挡住，就再也点不到了。",
("create:clipboard", "常见坑", 1): "界面里的清单不会自动同步，改完要重新贴一次。",

("create:experience_nugget", "怎么获得", 0): "经验块在物品栏里拆开就行，不需要摆合成台。",
("create:experience_nugget", "怎么获得", 1): "矿石要先过粉碎轮，直接烧矿石不会有颗粒。",
("create:experience_nugget", "怎么用", 0): "一次点太多会溢出等级上限，分几次用更稳。",
("create:experience_nugget", "怎么用", 1): "服务器里交易前先数清颗粒，别一把抓给人家。",
("create:experience_nugget", "常见坑", 0): "颗粒不能喂给附魔台，只能自己使用兑换。",
("create:experience_nugget", "常见坑", 1): "死亡掉落的经验不会变成颗粒，掉级就是掉级。",

("create:schematicannon", "怎么获得", 0): "原木用哪种树都行，平滑石头则要烧过再切。",
("create:schematicannon", "怎么获得", 1): "发射器里的弓不必是新的，耐久见底也能用。",
("create:schematicannon", "怎么用", 0): "炮口要正对施工区，偏了会把方块射到墙外。",
("create:schematicannon", "怎么用", 1): "箱子离得太远它取不到料，贴着炮身摆最稳。",
("create:schematicannon", "常见坑", 0): "蓝图方向反了会盖出镜像，拆起来比盖还慢。",
("create:schematicannon", "常见坑", 1): "火药放在旁边的箱子里才读得到，丢地上不算。",

("create:spout", "怎么获得", 0): "干海带要放进熔炉烤干，晒不到太阳就烤一下。",
("create:spout", "怎么获得", 1): "铜机壳做起来不便宜，先做两个试流水线。",
("create:spout", "怎么用", 0): "注液器下方要有支撑，物品得停在正对它的一格。",
("create:spout", "怎么用", 1): "管道接头只有一个面能进液，装反了会漏不出来。",
("create:spout", "常见坑", 0): "液体种类不对时它不会动手，桶里的水白灌了。",
("create:spout", "常见坑", 1): "一次只注一个容器，带子走太快会漏掉中间几个。",

("create:andesite_door", "怎么获得", 0): "木门可以现做，找村民换一扇也行，成本差不多。",
("create:andesite_door", "怎么获得", 1): "机壳压好后直接和门一起摆进合成格就成。",
("create:andesite_door", "怎么用", 0): "双开门要左右各一扇，中间不留缝才关得严。",
("create:andesite_door", "怎么用", 1): "红石接在门下方的方块上，信号会一路传进门。",
("create:andesite_door", "常见坑", 0): "门口摆台阶会挡住开门，进出得绕一大圈。",
("create:andesite_door", "常见坑", 1): "门下方必须有实心方块，悬空放会直接掉落。",
}

SEC = re.compile(r'\("(怎么获得|怎么用|进阶|常见坑|搭配)", "([^"]*)"\)')
starts = [m.start() for m in re.finditer(r'item\("create:', src)] + [len(src)]

out = []
applied = 0
for i in range(len(starts) - 1):
    a, b = starts[i], starts[i + 1]
    block = src[a:b]
    m = re.match(r'item\("(create:[a-z0-9_]+)"', block)
    iid = m.group(1) if m else None

    def rep(mm):
        global applied
        title, html = mm.group(1), mm.group(2)
        paras = html.split("<p>")[1:]
        new_parts = []
        for k, para in enumerate(paras):
            tail = para[: para.rfind("</p>")]
            add = PATCH.get((iid, title, k))
            if add:
                applied += 1
                tail = tail + add
            new_parts.append(tail + "</p>")
        return '("' + title + '", "<p>' + "<p>".join(new_parts) + '")'

    out.append(SEC.sub(rep, block))

open(P, "w", encoding="utf-8", newline="\n").write("".join(out))
print("applied", applied, "of", len(PATCH))
