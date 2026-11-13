# Create Codex · 机械动力物品教学图鉴

[![在线浏览](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E6%B5%8F%E8%A7%88-lOrionl.github.io%2Fcreate--codex-d9a441?style=for-the-badge&logo=githubpages&logoColor=black)](https://hao78da.github.io/create-codex/)
[![740 物品](https://img.shields.io/badge/%E7%89%A9%E5%93%81-740-d9a441?style=flat-square)](#)
[![断链](https://img.shields.io/badge/%E6%96%AD%E9%93%BE-0-3fb950?style=flat-square)](#)
[![License](https://img.shields.io/badge/%E8%84%9A%E6%9C%AC-MIT-blue?style=flat-square)](LICENSE)
[![Content](https://img.shields.io/badge/%E6%95%99%E7%A8%8B-CC%20BY--NC--SA%204.0-lightgrey?style=flat-square)](#)

> **👉 在线打开：<https://hao78da.github.io/create-codex/>**
>
> 不用下载、不用装环境，点开就是关系图。

一个纯静态的《我的世界》Create（机械动力）模组中文教学站，覆盖本体 **740 个物品** 与 **195 个附属模组的 9931 个物品**，站点共 1723 个可访问页面。

---

## 想在自己的电脑上跑 / 继续写？

```bash
git clone https://github.com/hao78da/create-codex.git
cd create-codex/tools
python gen_site.py        # 重新生成全部页面
python validate_all2.py   # 自检：页数 / 引用数 / 断链数
```

- 需要 Python 3.10+，无第三方依赖（生成器只用标准库）
- 生成结果写进 `docs/`（`docs/index.html`、`docs/catalog.html`、`docs/items/`、`docs/tags/` …）。GitHub Pages 从 `main` 的 `/docs` 发布，站点根就是 `docs/`，所以公开 URL 仍是 `https://hao78da.github.io/create-codex/xxx.html`；脚本里的 `SITE` 常量已指向 `ROOT/docs`
- 具体怎么加一个附属模组，见 [`tools/README.md`](tools/README.md)
- 想参与内容或脚本，见 [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 怎么用

直接双击 `docs/index.html` 即可，不需要服务器、不需要联网。
整个站点是相对路径的静态文件，可以直接拷进 U 盘、内网共享或 GitHub Pages。

- 首页 `index.html`：模组关系图（可拖拽平移、滚轮缩放），共 **196 个节点**（机械动力本体 + 195 个附属模组）。节点用黄金角螺旋撒开、长短不一的射线连回中心，点球进入对应模组页
- 图鉴 `catalog.html`：740 张本体卡片，支持中文名 / 英文名 / 物品 ID 搜索，按 9 个分类筛选
- 模组总览 `mods.html`：195 个附属模组卡片，点进去是各模组的物品与配方
- 详情页：每个物品一个 HTML（`items/<物品id>.html`），包含
  - 一句话定位 + 关键参数
  - 详细教程（怎么用 / 进阶 / 常见坑）
  - 获取方式：按模组配方 JSON 渲染的合成网格或机器处理配方
  - 官方教程：模组自带的 Ponder 场景文本（中文来自模组本地化）
  - 相关物品

## 内容统计（由生成器实际输出）

| 项目 | 数量 |
| --- | --- |
| 机械动力本体物品 / 方块 | 740 |
| 附属模组物品 | 9931（来自 195 个附属模组） |
| 页面总数 | 1723（被 validate_all2.py 实际扫到） |
| 关系图节点 | 196 |
| 附属模组 | 195 |
| 配方条目 | 本体 1302 + 附属 10112 |
| 有官方 Ponder 教程的物品 | 116 |
| 逐条撰写教程 | 740（本体全部物品） |
| 图标 | 14453 个 PNG |
| 标签页 | 387 |
| 原版物品页 | 396 |

本体分类：装饰与建筑 453、材料与零件 60、红石与控制 41、机器与加工 34、
物流与仓储 34、杂项 34、工具与装备 30、动力与传动 26、列车与轨道 21、动态结构与载具 7。

附属模组数据取自各模组 jar 内的 `zh_cn.json` 与配方 JSON，
模组清单来自 [MC百科](https://www.mcmod.cn/class/2021.html) 的「依赖机械动力的Mod」（Forge 1.20.1 分组），
再逐个验证 Modrinth / CurseForge 的 1.20.1 Forge 构建。

## 数据来源与版权

- **物品 / 中文名 / 官方教程文本 / 配方 / 纹理**：来自 [Creators-of-Create/Create](https://github.com/Creators-of-Create/Create) 仓库的 `mc1.20.1/dev` 分支（MIT 协议）。中文名与 Ponder 文本取自模组自带的 `zh_cn.json`，不是机器翻译。
- **原版物品与纹理**：Minecraft，版权归 Mojang 所有，仅用于教学展示。
- **标题字体**：Minecraft 字体，来自 [dafont.com](https://www.dafont.com/minecraft.font)，仅用于标题与数字；该字体不含中文字形，正文使用系统黑体。
- **教程正文**：本项目撰写。740 个条目全部逐条编写，每条 3 个小节（获得 / 用法 / 常见坑），正文不少于约 260 字。
- **附属模组简介**：取自 [MC百科](https://www.mcmod.cn/) 各模组页的中文简介；物品名与配方来自各模组 jar 本体，遵循各自的许可证。

## 重新生成

源脚本在 `D:\frontend\_raw\`：

| 脚本 | 作用 |
| --- | --- |
| `build_data.py` | 从 Create 仓库提取物品、名称、配方、Ponder 文本，下载纹理图标，输出 `out/data.json` 与 `assets/icons/*.png` |
| `content.py` | 教程文本库：`TUT` 逐条词条 + `FAMILY` 系列正则模板 + 分类映射 |
| `gen_site.py` | 生成 `index.html`、740 个详情页、`assets/style.css`、`assets/app.js` |

```powershell
$py = 'C:\Users\H\.dsh\dsh-runtimes\dsh-next-primary-runtime\dependencies\python\python.exe'
& $py D:\frontend\_raw\build_data.py   # 需要联网，首次约 10 分钟
& $py D:\frontend\_raw\gen_site.py     # 约 3 秒
```

## 已知限制

- 图标以方块**平面纹理**为主；另有 119 个物品（机器、齿轮箱、工具箱等）使用等距 3D 渲染图标（`render3d.py` 生成，文件名 `3d_*.png`）。
- 4 个物品在模组资源里没有可用纹理，使用占位齿轮图标。
- 配方按模组数据原样展示，不展开「标签」所代表的具体物品列表（只标注标签名）。

## 最近更新（2026-11）

### 关系图

- **性能**：节点「光晕 + 圆环 + 图标」预渲染到离屏 canvas 缓存（`spriteFor`），每帧只 `drawImage`；背景改成离屏缓存、900ms 重绘一次；空闲限帧 30fps、拖动全速；视口外节点不绘制。实测 1280×860 无 GPU 环境 **51 fps**。
- **移动端**：`MOBILE` 判定（粗指针或短边 <620），`dpr` 上限 1.5、星数 520→150、锁 30fps、不画噪点层；隐藏图例、按钮贴底、提示文案改成「拖动平移 · 双指缩放 · 点球进入」。
- **布局**：双环交错（内环 20 个、外环 20 个，角度对齐 0.04 弧度）；每个节点半径按 id 哈希取 `0.52–1.21`，所以连线长短不一、会从别的图标下方穿过；绘制顺序「线 → 节点」，图标永远压在线上层。
- **交互**：点空白或 `Esc` 收起展开的二级节点；标签默认只在悬停/聚焦时显示；右下 `⤢` 一键回到适应视图；`pageshow` 事件重置状态，修复 bfcache 返回后点不动的问题。
- **背景**：紫蓝双星云 + 45° 过渡带 + 暗角，缓慢漂移与色相渗透（周期 70–90 秒），叠 2% 噪点消除色带。

### 模组总览 `mods.html`

- 卡片按**物品数量降序**排列（Steam 'n' Rails 1894 → …），标题显示「已收录 196 个模组」。
- 不再在卡片上显示数量（只用于排序）。
- 修掉重排时产生的空卡片（`alt` 未闭合）。

### 附属模组页

- **搜索框**：实时过滤，显示命中数（如 `685 / 1894`），无命中的分类自动隐藏。
- **分类可折叠**：每个分类变成 `<details>`，点标题展开/收起。
- **自动分组**：原本只有一个「全部物品」的页面，按语义关键词（材料/机器/工具/食物/流体/建筑/交通）拆分；再按**名字相似度**聚类（如「粉羊毛/红羊毛/黑羊毛」→「羊毛」，列车零件 →「半成品」「车厢」），小组并入「其他」。
- 英文分组名统一译成中文（slab→台阶、stairs→楼梯、pane→玻璃板 等 60 条）。

### 图标流水线

- `tools/fetch_missing_jars.py`：按命名空间从 Modrinth 下载对应 jar（1.20.1 + forge/neoforge），下载后校验 jar 内确有 `assets/<ns>/`。
- `tools/extract_assets.py`：把 jar 的 `models/` 与 `textures/` 解到 `work/assets/<ns>/`（当前 92 个命名空间、6 万+ 文件）。
- `tools/backfill_icons.py`：沿 `item/block 模型 → parent → textures` 链提取平面图。
- `tools/render3d.py`：模型根改为**动态扫描** `work/assets/*/models`（不再写死 Create），支持任意命名空间贴图；超采样 4→2 提速。
- `tools/fix_placeholders.py`：把页面上仍指向 `_unknown.png` 的图标换成已生成的真图。
- 覆盖率：附属页 4,273 个占位 → 约 1,000（**76%**）。剩余多为「参数生成模型」（管道按颜色拼）、出生蛋、以及父模型指向原版资源（尚未解包）的物品。

### 标签体系

- 重建为 **336 页**：Create 本体标签 79、原版标签 96、附属/Forge 标签 161。
- 每页三段：成员 / 用到它的 Create 配方 / 附属模组里的使用（页面 + 物品名）。
- 图标优先级：成员图标 → 标签尾名 → 去复数 → 文件名模糊匹配 → 铜色标签牌 `tag_generic.png`。
