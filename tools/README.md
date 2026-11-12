# 构建说明（tools/）

这个目录是站点的**生成器**。仓库里已经带了成品 HTML，所以只浏览不需要跑它；想改内容/加模组时才需要。

## 环境

- Python 3.11+（无需第三方库）
- 可选：Node.js（渲染 3D 图标时才用）

## 目录

```
tools/
  gen_site.py            # 主体：740 个物品页 + 图鉴 + 标签索引
  content.py             # 教程正文（手写内容都在这里）
  batches/*.py           # 分批补写的教程内容
  gen_addon_multi.py     # 附属模组页生成器（读 jar）
  addon_post.py          # 附属页后处理：补锚点、链 chip、返回按钮
  sync_graph.py          # 关系图节点同步
  add_cards_auto.py      # mods.html 卡片同步
  gen_tags_all.py        # 标签体系（Create + 原版 + Forge）
  gen_vanilla_pages.py   # 原版物品页
  gen_vanilla_extra.py   # 只在附属页出现的原版物品
  render3d.py            # 方块模型 → 等距 3D 图标
  validate_all2.py       # 全站断链检查
  audit_icons2.py        # 空图标检查
  data/                  # 生成所需的中间数据（data.json / mc_zh.json / 标签定义）
  work/                  # 可选：放 mods_intake/*.jar（构建附属页时用）
```

## 跑一遍

```powershell
cd tools
python gen_site.py            # 重建 740 物品页 + 图鉴
python gen_tags_all.py        # 重建标签页
python addon_post.py          # 修复附属页链接
python sync_graph.py          # 同步关系图节点
python add_cards_auto.py      # 同步 mods 页卡片
python validate_all2.py       # 必须看到 broken 0
```

## 加一个附属模组

1. 把 jar 放到 `tools/work/mods_intake/<slug>.jar`
2. 在 `gen_addon_multi.py` 的 `SPECS` 里加一条（slug / ns / title / 简介）
3. `python gen_addon_multi.py <slug>`
4. `python addon_post.py && python sync_graph.py && python add_cards_auto.py`
5. `python validate_all2.py`

## 改教程正文

- 单条物品：`content.py` 里搜 `item("create:xxx", ...)`
- 批量/覆盖：往 `batches/` 里加文件，按文件名顺序合并，后写覆盖先写
- 改完 `python gen_site.py` 重新生成

## 注意

- 所有脚本用相对路径（`ROOT` = 仓库根目录），不要写死盘符
- `data/` 里的 JSON 是中间数据，一般不需要手改
- 图标在 `assets/icons/`，新增图标直接放进去，命名规则见 `gen_site.py` 的 `icon_file()`
