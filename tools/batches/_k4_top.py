import io
import re

P = r'D:\frontend\_raw\batches\k4.py'

TOP = {
    "veridium_pillar": {4: "辉绿岩柱四面纹路一致，转个方向砌也不会露怯。"},
    "small_dripstone_bricks": {4: "细砖缝多，铺地前先找平，凹凸一格就显错位。"},
    "small_tuff_bricks": {5: "凝灰岩抗爆 6.0，做外墙比做内饰更合适。"},
    "small_deepslate_bricks": {5: "巷道里用它砌墙，火把间距取四格，明暗才匀。"},
    "small_ochrum_bricks": {4: "矿镇外墙用同色台阶压一道勒脚，土黄才不显脏。"},
    "polished_cut_dripstone": {4: "台面接缝朝下藏，手摸过去是一整片，不刮手。"},
    "polished_cut_deepslate": {4: "台面下方垫一层切制块，操作时手肘才有地方放。"},
    "small_scorchia_bricks": {3: "站台边缘压一道绯红岩台阶，黑红交界处最耐看。"},
    "mechanical_crafter": {5: "拼大配方前先用小板试摆一次，确认网格数和配方一致。"},
    "cut_deepslate_wall": {4: "巷道每四格留一道竖缝，走进去能看出进深，不会闷成一片。"},
    "millstone": {0: "石磨出的是面粉不是小麦，箱子要单独分格放。"},
    "zinc_ingot": {1: "粉碎过的锌矿别当废料扔，一样能进熔炉烧成锭。"},
    "rotation_speed_controller": {0: "控制器要夹在两根轴之间，两端都接上才会生效。"},
    "rotation_speed_controller_2": {2: "改完转速下游立刻变，机器正在加工也不会停下来。"},
    "crushing_wheel": {0: "两个轮子才凑一对，配方本身就出两个，装一台不够用。"},
    "large_water_wheel": {0: "水车要正对水流摆，水从一侧推桨叶才转得起来。"},
    "large_water_wheel_2": {2: "转速虽低，带粉碎轮这类大户反而比小水车更稳。"},
    "cut_dripstone": {5: "溶洞里采石带够火把，钟乳石掉下来砸人很疼。"},
    "cut_deepslate": {4: "深板岩层里常有矿脉，切之前先把矿石挑出来。"},
}

MULTI = {"rotation_speed_controller_2": "rotation_speed_controller",
         "large_water_wheel_2": "large_water_wheel"}

s = io.open(P, encoding='utf-8').read()
starts = [(m.start(), m.group(1)) for m in re.finditer(r'item\("(create:[a-z_0-9]+)"', s)]


def seg_bounds(iid):
    full = iid if iid.startswith('create:') else 'create:' + iid
    for k, (pos, name) in enumerate(starts):
        if name == full:
            end = starts[k + 1][0] if k + 1 < len(starts) else len(s)
            return pos, end
    raise SystemExit('missing item ' + iid)


edits = []
for key, mapping in TOP.items():
    iid = MULTI.get(key, key)
    pos, end = seg_bounds(iid)
    seg = s[pos:end]
    closes = [m.end() for m in re.finditer(r'</p>', seg)]
    for idx, text in mapping.items():
        at = pos + closes[idx] - 4
        edits.append((at, text))

for at, text in sorted(edits, reverse=True):
    s = s[:at] + text + s[at:]

io.open(P, 'w', encoding='utf-8', newline='\n').write(s)
print('topped', len(edits))
