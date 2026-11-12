# Create Codex · 机械动力中文图鉴

Create（机械动力）模组的中文教学站点。纯静态，双击 `index.html` 即可打开，不需要服务器。

- 本体：740 个物品/方块，1302 条配方，116 段官方 Ponder 教程
- 附属：若干 Create 扩展模组，每个模组一页或一套页面
- 特色：配方反查（谁用它）、可点标签、方块 3D 等距图标

## 不是官方

本项目与 Creators-of-Create 团队无关，是玩家自建的中文整理站。

本站**不提供模组文件下载**，请到 CurseForge / Modrinth 的作者原页面下载并遵守各自的许可协议。

## 数据来源

| 内容 | 来源 | 许可 |
|---|---|---|
| 物品/配方/Ponder 文本 | Create 模组 jar（`assets/create`、`data/create`） | Create 为 MIT |
| Create 贴图与模型 | 同上 | 随 Create 的 MIT |
| 原版方块模型 | [misode/mcmeta](https://github.com/misode/mcmeta) 1.20.1-assets | Mojang 资源，仅用于教学展示 |
| 原版贴图 | 同上 / 社区镜像 | 版权归 Mojang |
| 附属模组数据 | 各模组自己的 jar | 见下表 |

### 附属模组

每个模组的数据都取自其 jar；页面顶部标注了使用的版本。**各模组的许可证彼此不同**，代码与素材版权归原作者所有。

已知收录（示例，完整清单见 `mods.html`）：

| 模组 | 作者 | 版本来源 |
|---|---|---|
| Dreams & Desires | LopyLuna | 1.20.1 |
| Create Goggles | Robocraft999 | 1.20.1 |
| Enchantment Industry | — | 1.20.1 |
| Create: Propulsion | — | 1.21.1 |
| Create: Screw It! | — | 1.21.1 |
| Create: Coasters Simulated | — | 1.21.1 |
| Create: Integrated Farming | — | 1.21.1 |

> 部分模组只发布 1.21.1，页面数据因此与 1.20.1 的主目录存在版本差；每页顶部均有说明。

## 目录结构

```
index.html            关系图（模组网络）
catalog.html          本体 740 项目录（搜索/分类）
tags.html             配方标签索引
items/<short>.html    本体物品详情
vanilla/<short>.html  原版物品
tags/<ns>_<tag>.html  标签页（: 与 / 换成 _）
mods.html             全部模组索引
addon-<slug>.html     附属模组页
assets/icons/         图标（含 3d_*.png 等距渲染图）
assets/style.css      全站样式
```

## 图标是怎么来的

- **物品**：直接用模组 jar 里的 `textures/item/<name>.png`
- **方块**：读取 `models/block/<name>.json`（含父模型链），按 `elements[].from/to/faces.uv` 用等距相机渲染成 `3d_*.png`
- **原版方块**：从 `misode/mcmeta` 取模型与贴图后同样渲染
- **没有模型的物品**（薄片、零件、纯贴图）：保持平面图，不强行造几何

因此「某些物品是平面图」不是漏做，而是它本来就没有可渲染的模型。

## 配方解析的三种写法

解析配方是本项目最容易出错的地方，模组可能用：

1. 1.20 风格：`key: { "X": {"item": "..."} }`、`result: {"item": "..."}`
2. 1.21 风格：`key: { "X": [{"item": "..."}] }`、`result: {"id": "..."}`
3. 目录差异：`data/<ns>/recipes/`（复数）或 `data/<ns>/recipe/`（单数）

三种都要兼容，否则会出现「卡片没有配方」「格子是空的」。

## 语义陷阱

- **标签不是路径**：`data/<ns>/tags/items/optional_block_drops/<block>.json` 看着像内部路径，实际是模组真实定义的标签，控制方块的可选掉落。不要按名字删标签页。
- **tooltip 键不是物品**：语言文件里 `item.<ns>.<name>.tooltip.behaviour` 这类键不能当物品，否则会生成一堆空图标卡片。
- **颜色变体**：16 色的同款方块通常共用一条配方，应合并成一张卡，不要逐色生成「无配方」卡片。

## 重建

```bash
python gen_site.py                 # 本体：740 页 + tags + catalog
python gen_addon_<name>.py         # 单个附属模组页
python render3d.py --jobs jobs.json  # 批量渲染方块 3D 图标
```

改页面请改生成器，不要直接改产物 HTML —— 产物会被下一次生成覆盖。

## 已知缺口

- 原版方块 3D 覆盖 32 / 79（花、按钮、蛋糕、营火等多部件方块缺少可用父模型）
- 部分附属页的「序列组装」配方仍显示为空材料行
- 个别模组无中文语言文件，物品名为意译
