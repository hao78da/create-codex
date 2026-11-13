# 图标补全任务：约 1,000 个占位，主要卡在「父模型指向原版资源」

## 背景

仓库里的附属模组页共 195 个，卡片图标来自 `assets/icons/<ns>_<name>.png`。
早期只有 Create 本体和少数几个模组的资源，所以大量附属模组图标是占位图 `assets/icons/_unknown.png`。

目前的进度：

| 阶段 | 结果 |
|---|---|
| 初始 | 4,273 个占位（105 个页面、104 个命名空间） |
| 下 jar + 解包 + 平面回填 | 补了 **3,265** 个（约 76%） |
| 3D 渲染 | 仅成功 13 个 |

剩下约 **1,000 个**，分布在 **96 个命名空间**，前几名：

```
greate 150 · pipe_networks 112 · northstar 70 · create_wt 61 ·
extendedgears 56 · kuayue 47 · create_connected 41 ·
create_biotech 29 · prma 24 · createcasing 21 · createbigcannons 20
```

## 为什么会剩下

抽样查明有四类：

**A. 父模型指向原版（最大类）**
比如 `kuayue:clay_slab` → `minecraft:block/slab`；
`northstar:*_spawn_egg` → `minecraft:item/template_spawn_egg`。
仓库里没有 `assets/minecraft/models`，渲染器和贴图解析走到这里就断了。

**B. 参数生成模型**
`greate` 的齿轮、`pipe_networks` 的管道：jar 里**没有和物品同名的模型文件**，它们的图标是按「基础模型 + 颜色/材质参数」在运行时拼出来的。只能人工建映射表（颜色 × 形状 → 模型名）。

**C. 模板/派生物品**
`spawn_egg`、刷怪蛋、部分「半成品」使用的是共享模板，只有 tint 不同。

**D. 真的缺贴图**
少数模组 jar 里既没有模型也没有贴图（纯代码模组）。

## 建议做法

### 第一步：补原版资源（能解决 A 类，收益最大）

需要 1.20.1 的客户端 jar（Mojang 官方，约 20 MB）：

```
https://piston-data.mojang.com/v1/objects/<hash>/client.jar
```

版本清单：`https://piston-meta.mojang.com/mc/game/version_manifest_v2.json` → 找 `1.20.1` → `url` → `downloads.client.url`

解出：

```
work/assets/minecraft/models/**      ← 关键
work/assets/minecraft/textures/**    ← 关键
work/assets/minecraft/blockstates/**
```

然后：

1. 改 `tools/render3d.py`：`_mpath()` 已经会扫 `work/assets/*/models`，`minecraft` 目录放进去就会自动被找到；确认 `_dyn_tex_roots()` 能解析 `minecraft:block/...`
2. 跑 `python tools/render_missing.py`（多进程，只处理仍指向 `_unknown.png` 的物品）
3. 跑 `python tools/fix_placeholders.py` 把页面引用替换成新图
4. `python tools/validate_all2.py` 必须 `broken 0`

### 第二步：参数生成模型（B 类）

需要给这些模组写映射表，例如 `pipe_networks`：

```python
# 伪代码：从物品 id 拆出颜色 + 材质，拼出真实模型名
"encased_black_aluminum_pipe" -> "block/encased_pipe/black_aluminum"
```

建议做成 `tools/model_alias.py`，字典形式，渲染前查表。

### 第三步：验收

三个硬指标，缺一不可：

```bash
python tools/validate_all2.py     # 输出 broken 0
python tools/audit_icons2.py      # 图标审计
grep -rc '_unknown.png' addon-*.html | awk -F: '{s+=$2} END {print s}'   # 应显著下降
```

## 注意

- **不要把 jar 提交进仓库**：`work/`、`tools/work/` 已在 `.gitignore`
- 生成页面后**必须重跑** `addon_post.py`（补返回按钮、chip 链接、搜索框和折叠分组）
- `render3d.py` 的 `SS`（超采样）默认 2，调到 4 会慢 4 倍
- 仓库根必须有 `.nojekyll`，否则 GitHub Pages 会忽略 `_unknown.png` 这类下划线开头的文件
- 提交信息建议：`feat(icons): 补 xxx 模组图标（xx 个）`

## 相关脚本

| 脚本 | 作用 |
|---|---|
| `tools/fetch_missing_jars.py` | 按命名空间从 Modrinth 下 jar，校验含 `assets/<ns>/` |
| `tools/extract_assets.py` | 解包所有 jar 的 models/textures 到 `work/assets/<ns>/` |
| `tools/backfill_icons.py` | 模型链 → 贴图（平面图） |
| `tools/render3d.py` | 方块模型 → 等距 3D 渲染 |
| `tools/render_missing.py` | 对剩余图标批量尝试 3D |
| `tools/fix_placeholders.py` | 页面占位替换为真图 |

## 附：当前渲染器的限制

- 只吃 **JSON 模型**（`elements` + `textures`），不支持 OBJ
- 不支持 `tintindex`（染色），所以按颜色区分的物品只能靠人工映射
- 支持 `parent` 链，但链上任一环缺失就整体失败（这就是补原版资源的意义）
