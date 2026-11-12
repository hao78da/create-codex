import re

P = r"D:\frontend\_raw\batches\k2.py"
src = open(P, encoding="utf-8").read()

PATCH = {
("create:small_bogey", "怎么获得", 0): "转向架只在车厢两端出现，车厢再长中间也不会多挂一副。",
("create:small_bogey", "怎么获得", 1): "想多备轮组的话，整列车复制一遍比单独找轮组容易。",
("create:small_bogey", "怎么用", 0): "轮组是被轨道带着转的，列车停下时它们也一起停住。",
("create:small_bogey", "怎么用", 1): "站台前那段直轨尽量留长，进站减速会平稳不少。",
("create:small_bogey", "常见坑", 0): "开进站台范围后信号灯会变色，等它停稳再动手拆。",
("create:small_bogey", "常见坑", 1): "给驾驶台接一个拉杆就能远程发车，省得每次手动点。",

("create:extendo_grip", "怎么获得", 0): "合成时阵列要摆成长条，少放一格就会卡住不出货。",
("create:extendo_grip", "怎么获得", 1): "精密构件本身要好几道工序，先把它做出来再摆阵列。",
("create:extendo_grip", "怎么用", 0): "副手拿着它时主手别空着，空手加长距离没有意义。",
("create:extendo_grip", "怎么用", 1): "气压按秒消耗，长时间悬空作业前先看一眼余量。",
("create:extendo_grip", "搭配", 0): "背罐要用动力泵打气，随手放在地上不会自己回满。",
("create:extendo_grip", "搭配", 1): "够远处机器时小心别点到旁边的方块，放错位置很难拆。",

("create:mechanical_plough", "怎么获得", 0): "铁板由动力压床压铁锭，安山合金则是铁粒拌安山岩。",
("create:mechanical_plough", "怎么获得", 1): "做一把就够用，犁不会磨损，装上结构就能一直工作。",
("create:mechanical_plough", "怎么用", 0): "犁过的草方块会变成耕地，耕地上直接撒种子就能种。",
("create:mechanical_plough", "怎么用", 1): "移动速度越快翻地越快，但太快会漏掉边角的方块。",
("create:mechanical_plough", "常见坑", 0): "装在轴承上要让刃口朝下，朝天摆只会空转不翻土。",
("create:mechanical_plough", "常见坑", 1): "水面和岩浆面它处理不了，开荒前先拿桶把水抽干。",

("create:pulse_extender", "怎么获得", 0): "黄铜板要把黄铜锭压薄，红石火把则由木棍加红石粉点成。",
("create:pulse_extender", "怎么获得", 1): "三个石头用圆石烧一下就有，成本几乎可以忽略。",
("create:pulse_extender", "怎么用", 0): "面板上能读到当前设定的时长，改完要再右击确认一次。",
("create:pulse_extender", "怎么用", 1): "给请求器供信号时，脉冲比它读单的时间略长就够。",
("create:pulse_extender", "常见坑", 0): "输入断掉后它仍会把这一轮脉冲放完，别以为卡住了。",
("create:pulse_extender", "常见坑", 1): "几个延长器串在一起时长会叠加，很容易拉出几分钟。",

("create:redstone_requester", "怎么获得", 0): "清除配方能把记下的订单抹掉，换仓库时正好用得上。",
("create:redstone_requester", "怎么获得", 1): "链接站与保险库都吃铜，先把仓储网搭稳再回来看它。",
("create:redstone_requester", "怎么用", 0): "界面里能选物品与数量，填好关掉界面设置就存住了。",
("create:redstone_requester", "怎么用", 1): "包裹从最近的打包机发出，收件口要留出放包裹的位置。",
("create:redstone_requester", "常见坑", 0): "网里没有这件物品时它只会空转，不会自己去找替代品。",
("create:redstone_requester", "常见坑", 1): "同一张网上多个请求器会抢货，按信号先后排顺序。",

("create:stock_link", "怎么获得", 0): "发信线圈要铜板绕铜线，物品保险库则是铁板包木桶。",
("create:stock_link", "怎么获得", 1): "清除配方只抹掉绑定，方块本身还会留在原地等重接。",
("create:stock_link", "怎么用", 0): "一张网里可以有多个链接站，它们共用同一份库存清单。",
("create:stock_link", "怎么用", 1): "打包机要贴着箱子放，隔开一格就读不到里面的东西。",
("create:stock_link", "常见坑", 0): "红石信号越强优先级越低，这条规则和直觉正好相反。",
("create:stock_link", "常见坑", 1): "跨维度时包裹送不过去，远距离还是得靠列车与船。",

("create:analog_lever", "怎么获得", 0): "安山机壳由安山合金压成，木棍拿两块木板竖着切就有。",
("create:analog_lever", "怎么获得", 1): "它的合成不挑木板种类，什么木头做出来都一样用。",
("create:analog_lever", "怎么用", 0): "把它装在驾驶台侧面，就能用拉的幅度控制起步快慢。",
("create:analog_lever", "怎么用", 1): "接转速控制器时信号越高转得越快，拨到底就是满速。",
("create:analog_lever", "常见坑", 0): "红石粉线路不会削弱档位，走多远读到的都是同一个值。",
("create:analog_lever", "常见坑", 1): "多个拉杆并到一条线上取最大值，想叠加得另做电路。",

("create:blaze_burner", "怎么获得", 0): "下界岩要去下界挖，跑一趟顺手多带几块省得再跑。",
("create:blaze_burner", "怎么获得", 1): "抓烈焰人时别把它打死，空手右击才装得进去。",
("create:blaze_burner", "怎么用", 0): "热量等级越高能做的配方越多，高级配方会挑等级。",
("create:blaze_burner", "怎么用", 1): "盆里还得有人搅或压，光有热没有机械动作也不出料。",
("create:blaze_burner", "常见坑", 0): "蛋糕吃完后热量掉档，产量突然变慢多半就是这里。",
("create:blaze_burner", "常见坑", 1): "挪动燃烧室时里面的烈焰人会跟着走，不用重新抓。",

("create:shadow_steel", "怎么获得", 0): "创造模式物品栏里能直接拿到，生存里没有正规途径。",
("create:shadow_steel", "怎么获得", 1): "旧存档里可能还留着几块，翻箱子时别当垃圾丢了。",
("create:shadow_steel", "怎么用", 0): "丢下去时人站高一点，落差太小只会轻轻跳一下。",
("create:shadow_steel", "怎么用", 1): "它落地不会碎，捡起来还能再丢，适合做测试道具。",
("create:shadow_steel", "常见坑", 0): "别把它当成下界合金那样的升级材料，两者机制无关。",
("create:shadow_steel", "常见坑", 1): "想复刻这种弹跳只能靠模组或命令，原版方块做不到。",

("create:controls", "怎么获得", 0): "列车机壳用安山机壳与铁板拼，精密构件则要一整套工序。",
("create:controls", "怎么获得", 1): "一台驾驶台只管一列车，挂再多车厢也只需要一个。",
("create:controls", "怎么用", 0): "界面里能编时刻表，跑固定线路时先把站点顺序排好。",
("create:controls", "怎么用", 1): "下车按 shift 就行，车会停在原地不会自己开走。",
("create:controls", "常见坑", 0): "驾驶台装在车厢外侧也能用，但别让它悬空没有支撑。",
("create:controls", "常见坑", 1): "路线表存在驾驶台里，拆掉它就没了，改线前先记下来。",
}

SEC = re.compile(r'\("(怎么获得|怎么用|进阶|常见坑|搭配)", "([^"]*)"\)')
starts = [m.start() for m in re.finditer(r'item\("create:', src)] + [len(src)]

out = []
prev = 0
applied = 0
for i in range(len(starts) - 1):
    a, b = starts[i], starts[i + 1]
    block = src[a:b]
    m = re.match(r'item\("(create:[a-z0-9_]+)"', block)
    iid = m.group(1) if m else None
    def rep(mm):
        global applied
        title, html = mm.group(1), mm.group(2)
        idx_parts = html.split("</p>")
        # paragraphs are html.split('</p>')[:-1]
        paras = [p for p in html.split("<p>")[1:]]
        new_parts = []
        for k, para in enumerate(paras):
            tail = para[: para.rfind("</p>")]
            key = (iid, title, k)
            add = PATCH.get(key)
            if add:
                applied += 1
                tail = tail + add
            new_parts.append(tail + "</p>")
        return '("' + title + '", "<p>' + "<p>".join(new_parts) + '")'
    block2 = SEC.sub(rep, block)
    out.append(block2)
    prev = b

new_src = "".join(out)
open(P, "w", encoding="utf-8", newline="\n").write(new_src)
print("applied", applied, "of", len(PATCH))
