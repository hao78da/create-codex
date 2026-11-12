# Create Codex · 机械动力物品教学图鉴

[![在线浏览](https://img.shields.io/badge/%E5%9C%A8%E7%BA%BF%E6%B5%8F%E8%A7%88-hao78da.github.io%2Fcreate--codex-d9a441?style=for-the-badge&logo=githubpages&logoColor=black)](https://hao78da.github.io/create-codex/)
[![740 物品](https://img.shields.io/badge/%E7%89%A9%E5%93%81-740-d9a441?style=flat-square)](#)
[![断链](https://img.shields.io/badge/%E6%96%AD%E9%93%BE-0-3fb950?style=flat-square)](#)
[![License](https://img.shields.io/badge/%E8%84%9A%E6%9C%AC-MIT-blue?style=flat-square)](LICENSE)
[![Content](https://img.shields.io/badge/%E6%95%99%E7%A8%8B-CC%20BY--NC--SA%204.0-lightgrey?style=flat-square)](#)

> **👉 在线打开：<https://hao78da.github.io/create-codex/>**
>
> 不用下载、不用装环境，点开就是关系图。

一个纯静态的《我的世界》Create（机械动力）模组中文教学站，覆盖模组内 **740 个物品与方块**。

---

## 想在自己的电脑上跑 / 继续写？

```bash
git clone https://github.com/hao78da/create-codex.git
cd create-codex/tools
python gen_site.py        # 重新生成全部页面
python validate_all2.py   # 自检：页数 / 引用数 / 断链数
```

- 需要 Python 3.10+，无第三方依赖（生成器只用标准库）
- 生成结果直接写到仓库根目录（`index.html`、`catalog.html`、`items/`、`tags/` …）
- 具体怎么加一个附属模组，见 [`tools/README.md`](tools/README.md)
- 想参与内容或脚本，见 [`CONTRIBUTING.md`](CONTRIBUTING.md)

## 怎么用

直接双击 `index.html` 即可，不需要服务器、不需要联网。
整个站点是相对路径的静态文件，可以直接拷进 U 盘、内网共享或 GitHub Pages。

- 首页 `index.html`：模组关系图（可拖拽平移、滚轮缩放）。目前只有「机械动力」一个节点，点击节点进入物品图鉴；以后加附属模组就在这条轨道上挂新节点、用连线表示附属关系
- 图鉴 `catalog.html`：740 张卡片，支持中文名 / 英文名 / 物品 ID 搜索，按 9 个分类筛选
- 详情页：每个物品一个 HTML（`items/<物品id>.html`），包含
  - 一句话定位 + 关键参数
  - 详细教程（怎么用 / 进阶 / 常见坑）
  - 获取方式：按模组配方 JSON 渲染的合成网格或机器处理配方
  - 官方教程：模组自带的 Ponder 场景文本（中文来自模组本地化）
  - 相关物品

## 内容统计（由生成器实际输出）

| 项目 | 数量 |
| --- | --- |
| 物品 / 方块 | 740 |
| 配方条目 | 1302 |
| 有官方 Ponder 教程的物品 | 116 |
| 逐条撰写教程 | 740（全部物品） |
| 图标 | 1055 个 PNG（其中 119 个 3D 渲染图标，4 个物品用占位齿轮） |

分类：装饰与建筑 453、材料与零件 60、红石与控制 41、机器与加工 34、
物流与仓储 34、杂项 34、工具与装备 30、动力与传动 26、列车与轨道 21、动态结构与载具 7。

## 数据来源与版权

- **物品 / 中文名 / 官方教程文本 / 配方 / 纹理**：来自 [Creators-of-Create/Create](https://github.com/Creators-of-Create/Create) 仓库的 `mc1.20.1/dev` 分支（MIT 协议）。中文名与 Ponder 文本取自模组自带的 `zh_cn.json`，不是机器翻译。
- **原版物品与纹理**：Minecraft，版权归 Mojang 所有，仅用于教学展示。
- **标题字体**：Minecraft 字体，来自 [dafont.com](https://www.dafont.com/minecraft.font)，仅用于标题与数字；该字体不含中文字形，正文使用系统黑体。
- **教程正文**：本项目撰写。740 个条目全部逐条编写，每条 3 个小节（获得 / 用法 / 常见坑），正文不少于约 260 字。

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
