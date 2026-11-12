import json, re
d = json.load(open(r'D:\frontend\_raw\out\data.json', encoding='utf-8'))
items = d['items']
keys = sorted(items.keys())
cands = """create:gold_sheet create:golden_sheet create:polished_rose_quartz create:rose_quartz_lamp
create:rose_quartz_block create:rose_quartz_tiles create:small_deepslate_brick_slab create:small_diorite_brick_slab
create:small_granite_brick_slab create:small_limestone_brick_slab create:small_ochrum_brick_slab
create:small_scoria_brick_slab create:small_scorchia_brick_slab create:small_tuff_brick_slab
create:small_veridium_brick_slab create:small_crimsite_brick_slab create:small_dripstone_brick_slab
create:polished_cut_crimsite_slab create:polished_cut_diorite_slab create:polished_cut_deepslate_slab
create:polished_cut_dripstone_slab create:deepslate_pillar create:diorite_pillar create:ochrum_pillar
create:depot create:chute create:metal_girder create:fluid_pipe create:fluid_tank create:track_station
create:track_signal create:schedule create:railway_casing create:andesite_casing create:brass_casing
create:electron_tube create:brass_hand create:mechanical_mixer create:blaze_burner create:spout
create:crushed_raw_iron create:crushed_raw_zinc create:water_wheel create:shaft create:belt_connector
create:andesite_alloy create:brass_ingot create:mechanical_arm create:rotation_speed_controller""".split()
out = []
out.append("MISSING: " + " ".join(c for c in cands if c not in items))
out.append("")
out.append("--- ids with gold ---")
out += [k for k in keys if 'gold' in k]
out.append("")
out.append("--- ids with rose_quartz ---")
out += [k for k in keys if 'rose_quartz' in k]
out.append("")
out.append("--- ids with small_ ---")
out += [k for k in keys if 'small_' in k]
out.append("")
out.append("--- ids ending _pillar ---")
out += [k for k in keys if k.endswith('_pillar')]
open(r'D:\frontend\_raw\batches\_k4_ids.txt', 'w', encoding='utf-8').write("\n".join(out))
print("ok", len(keys))
