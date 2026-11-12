# 如何参与

这个站是**静态站 + 生成器**：仓库里既有成品 HTML，也有生成它们的脚本。你可以只改 HTML，也可以改脚本再重新生成。

## 三种参与方式

### 1. 报告错误（最简单）

开 issue，写清楚：

- 哪个页面（贴 URL 或物品名）
- 哪里不对（配方错 / 机制写错 / 文字错别字 / 图标缺失）
- 正确的内容是什么（最好附截图或对应模组的 jar 信息）

### 2. 直接改（Pull Request）

```bash
git clone https://github.com/hao78da/create-codex.git
cd create-codex
# 改内容：
#   - 只改文案 → 直接编辑 items/*.html（会被下次生成覆盖，长期方案见下）
#   - 改源内容 → 编辑 tools/content.py 或 tools/batches/*.py，然后重新生成
git checkout -b fix/xxx
git commit -am "fix: 机械压床的转速写错了"
git push origin fix/xxx
# 然后在 GitHub 上开 PR
```

**推荐改源文件**（`tools/content.py`、`tools/batches/`），因为成品 HTML 会被重新生成覆盖。

### 3. 加模组

见 [tools/README.md](tools/README.md#加一个附属模组)。

需要：模组 jar + 一行 spec。图标会自动从 jar 里提取，缺图标时用占位。

## 提交前自检

```bash
cd tools
python validate_all2.py     # 必须 broken 0
python audit_icons2.py      # 空图标 0
```

## 内容规范

- 教程正文：**不要编造机制/数值**。不确定的写「资料库无配方」或省略
- 配方、中文名、Ponder 文本：一律取自模组本体，不要手写数字
- 图标：优先 `assets/icons/` 里已有的命名规则
- 每个物品页建议包含：怎么获得 / 怎么用 / 参数 / 常见坑

## 版权

- Create 模组：MIT（Creators-of-Create）
- 各附属模组：各自的许可证
- Minecraft 纹理：© Mojang，本站仅用于非商业的教学展示
- 本站教程正文：CC BY-NC-SA 4.0（署名-非商业-相同方式共享）

提 PR 即表示同意以上条款。
