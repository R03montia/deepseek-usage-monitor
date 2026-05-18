[中文](#deepseek-api-用量监控) | [English](#deepseek-monitor)
------
# DeepSeek API 用量监控

一个复古像素风桌面小组件，实时监控你的 DeepSeek API 用量。数据来自 [platform.deepseek.com](https://platform.deepseek.com/usage) 内部接口。

## 功能

- **余额看板** — 剩余余额及彩色进度条（<15% 红色、<40% 琥珀色、>40% 蓝色）
- **每日 Token 统计** — 总计、输入、输出 token 及迷你条形图
- **缓存命中率** — 醒目显示及颜色阈值（>80% 绿色、>50% 蓝色、<50% 橙色）
- **费用追踪** — 今日花费与月度花费（¥，精确到 4 位小数）
- **赠额显示** — 单独展示免费额度
- **可配置刷新** — 在 `config.json` 中设置刷新间隔（默认 10 秒，最少 3 秒）
- **悬停虚化** — 鼠标悬停时淡出至 25% 透明度，移开恢复（可在系统托盘切换）
- **系统托盘** — 最小化到托盘，支持显示/隐藏、虚化开关、刷新和退出
- **置顶显示** — 始终位于所有窗口之上
- **拖拽移动** — 左键按住任意位置拖拽
- **滚动语录** — 底部轮播 60+ 条 AI笑话
- **像素风界面** — 深色主题、Courier New 等宽字体、高对比度布局

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

如需系统托盘功能（推荐）：

```bash
pip install pystray pillow
```

### 2. 获取 Token

1. 打开 [platform.deepseek.com](https://platform.deepseek.com/usage) 并登录
2. 按 **F12** → **控制台**，粘贴以下代码：

```js
JSON.parse(localStorage.getItem('userToken')).value
```

3. 复制输出的字符串

### 3. 运行

```bash
python main.py
```

首次启动会弹出对话框要求粘贴 token，随后自动保存到 `config.json`。

## 配置文件 (`config.json`)

| 键名 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `bearer_token` | string | — | 平台认证令牌 |
| `refresh_interval` | integer | 10 | 自动刷新间隔（秒，最少 3 秒） |
| `hover_fade` | boolean | true | 鼠标悬停时虚化 |

## 操作方式

| 操作 | 效果 |
|------|------|
| 左键拖拽 | 移动窗口 |
| 右键 | 右键菜单（刷新 / 退出） |
| 托盘左键 | 切换显示/隐藏 |
| 托盘右键 | 右键菜单（含虚化开关） |
| 鼠标悬停 | 淡出至 25% 透明度 |

## 项目结构

```
deepseek-widget/
├── main.py              # 入口 + 系统托盘
├── widget.py            # 像素风界面
├── api.py               # 内部 API 客户端
├── config.py            # 配置管理器
├── token_extractor.py   # 可选的 Chrome 自动提取
├── config.json          # Token 与设置（已加入 gitignore）
├── requirements.txt     # Python 依赖
├── README.md
└── .gitignore
```

## 注意事项

- Token 有效期为数天至数周。如果数据停止更新，删除 `config.json` 重新运行即可。
- 内部 API 并非官方文档接口，platform.deepseek.com 变更后可能失效。
- Playwright 自动提取 Token 为可选功能：`pip install playwright && playwright install chromium`

## 许可证

[CC BY-NC 4.0](LICENSE) — 署名-非商业使用 4.0 国际

------

# DeepSeek Monitor

A retro pixel-art desktop widget for monitoring your **DeepSeek API** usage in real time. Data sourced from [platform.deepseek.com](https://platform.deepseek.com/usage) internal APIs.

## Features

- **Balance Dashboard** — remaining balance with color-coded progress bar (<15% red, <40% amber, >40% blue)
- **Daily Token Stats** — total, prompt, and completion tokens with mini bars
- **Cache Hit Rate** — prominent display with color thresholds (>80% green, >50% blue, <50% orange)
- **Cost Tracking** — today's cost & monthly cost (¥, 4 decimal places)
- **Bonus Balance** — shows free grant balance separately
- **Configurable Refresh** — set refresh interval in `config.json` (default: 10s, minimum 3s)
- **Hover Fade** — fades to 25% opacity on hover, snaps back on leave (toggle from system tray)
- **System Tray** — minimize to tray with show/hide, hover-fade toggle, refresh, and exit
- **Always on Top** — pinned above all windows
- **Drag to Move** — left-click and drag anywhere
- **Rotating Quotes** — 60+ AI memes
- **Pixel-Art Aesthetic** — dark theme, Courier New monospace, high-contrast layout

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

For system tray support (recommended):

```bash
pip install pystray pillow
```

### 2. Get Your Token

1. Open [platform.deepseek.com](https://platform.deepseek.com/usage) and log in
2. Press **F12** → **Console**, then paste:

```js
JSON.parse(localStorage.getItem('userToken')).value
```

3. Copy the output string

### 3. Run

```bash
python main.py
```

On first launch, a dialog prompts you to paste the token. It is saved in `config.json` afterward.

## Configuration (`config.json`)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `bearer_token` | string | — | Auth token from platform.deepseek.com |
| `refresh_interval` | integer | 10 | Auto-refresh interval in seconds (min 3) |
| `hover_fade` | boolean | true | Fade widget on mouse hover |

## Controls

| Action | Effect |
|--------|--------|
| Left-click + drag | Move window |
| Right-click | Context menu (Refresh / Exit) |
| System tray (left-click) | Toggle show/hide |
| System tray (right-click) | Context menu with hover-fade toggle |
| Mouse hover | Fade to 25% opacity |

## Project Structure

```
deepseek-widget/
├── main.py              # Entry point + system tray
├── widget.py            # Pixel-art GUI widget
├── api.py               # platform.deepseek.com internal API client
├── config.py            # Configuration manager
├── token_extractor.py   # Optional Chrome localStorage extraction
├── config.json          # Bearer token & settings (gitignored)
├── requirements.txt     # Python dependencies
├── README.md
└── .gitignore
```

## Notes

- The token stays valid for days to weeks. If data stops updating, delete `config.json` and re-run.
- The internal API is not officially documented and may break if platform.deepseek.com changes.
- Token auto-extraction via Playwright is optional: `pip install playwright && playwright install chromium`

## License

[CC BY-NC 4.0](LICENSE) — Attribution-NonCommercial 4.0 International

-----
