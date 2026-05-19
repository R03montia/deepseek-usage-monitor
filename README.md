[中文](#deepseek-api-用量监控) | [English](#deepseek-monitor)
------
# DeepSeek API 用量监控

一个复古像素风桌面小组件，实时监控你的 DeepSeek API 用量。数据来自 [platform.deepseek.com](https://platform.deepseek.com/usage) 内部接口。

## 功能

- **余额看板** — 剩余余额及彩色进度条（<15% 红色、<40% 琥珀色、>40% 蓝色）
- **每日 Token 统计** — 总计、输入、输出 token 及迷你条形图
- **缓存命中率** — 醒目显示及颜色阈值（>80% 绿色、>50% 蓝色、<50% 橙色）
- **费用追踪** — 今日花费与月度花费，支持 4 种币种切换
- **赠额显示** — 单独展示免费额度
- **多币种支持** — 人民币 CNY、美元 USD、加元 CAD、日元 JPY，实时汇率
- **6 套配色主题** — Default、Amber Glow、Frost Blue、Verdant Green、Soft Pastel、Midnight Glow
- **侧边栏图表** — 月度 Token/费用趋势柱状图，悬停查看详情
- **Lite 精简模式** — 仅显示关键信息的小窗口
- **边缘吸附（Beta）** — 靠近屏幕边缘自动缩入，鼠标悬停展开，主题色光效指示
- **悬停虚化** — 鼠标悬停时淡出至 25% 透明度，移开恢复
- **系统托盘** — 支持显示/隐藏、虚化开关、置顶、自动吸附、Lite 模式、币种切换、主题切换、刷新和退出
- **右键菜单** — 完整的功能控制面板
- **置顶显示** — 始终位于所有窗口之上
- **拖拽移动** — 左键按住任意位置拖拽
- **滚动语录** — 底部轮播 60+ 条 AI 笑话
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

1. 使用 **Chrome** 浏览器打开 [platform.deepseek.com](https://platform.deepseek.com/usage) 并登录
2. 按 **F12** → **控制台**，粘贴以下代码：

```js
JSON.parse(localStorage.getItem('userToken')).value
```

3. 复制输出的字符串

### 3. 运行

```bash
双击 main.pyw
```

首次启动会弹出对话框要求粘贴 token，随后自动保存到 `config.json`。

## 配置文件 (`config.json`)

| 键名 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `bearer_token` | string | — | 平台认证令牌 |
| `refresh_interval` | integer | 10 | 自动刷新间隔（秒，最少 3 秒） |
| `hover_fade` | boolean | true | 鼠标悬停时虚化 |
| `pin_window` | boolean | true | 窗口置顶 |
| `currency` | string | "CNY" | 显示币种（CNY/USD/CAD/JPY） |
| `lite_mode` | boolean | false | Lite 精简模式 |
| `theme` | string | "Default" | 配色主题 |
| `auto_snap` | boolean | false | 边缘自动吸附（Beta） |

## 操作方式

| 操作 | 效果 |
|------|------|
| 左键拖拽 | 移动窗口 |
| 右键 | 完整功能菜单（刷新/图表/Lite/置顶/币种/主题/重启/退出） |
| 托盘左键 | 切换显示/隐藏 |
| 托盘右键 | 完整功能菜单（含虚化/置顶/吸附/图表/Lite/币种/主题开关） |
| 鼠标悬停 | 淡出至 25% 透明度 |
| Ctrl+Tab / Ctrl+T | 切换侧边栏图表面板 |
| 吸附状态悬停 | 展开窗口，鼠标离开后自动收回 |

## 配色主题

| 主题 | 风格 |
|------|------|
| Default | 深蓝赛博朋克 |
| Amber Glow | 琥珀暖橙 |
| Frost Blue | 冷冽冰蓝 |
| Verdant Green | 苍岭翠绿 |
| Soft Pastel | 粉蓝白浅色系 |
| Midnight Glow | 暗黑橙光 |

## 项目结构

```
deepseek-widget/
├── main.pyw             # 入口 + 系统托盘
├── widget.py            # 像素风界面（含吸附/图表/主题）
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
- 边缘吸附功能为 Beta，如有问题请在 GitHub Issues 反馈。
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
- **Cost Tracking** — today's cost & monthly cost (¥, multi-currency)
- **Bonus Balance** — shows free grant balance separately
- **Multi-Currency** — CNY / USD / CAD / JPY with live exchange rates
- **6 Color Themes** — Default, Amber Glow, Frost Blue, Verdant Green, Soft Pastel, Midnight Glow
- **Sidebar Charts** — monthly token & cost bar charts with hover tooltips
- **Lite Mode** — compact window showing only essential info
- **Edge Snap (Beta)** — auto-hide to screen edge, hover to peek, theme-colored glow indicator
- **Hover Fade** — fades to 25% opacity on hover, snaps back on leave
- **System Tray** — full-featured tray menu (refresh, fade, pin, snap, charts, lite, currency, themes, exit)
- **Right-Click Menu** — complete control panel
- **Always on Top** — pinned above all windows
- **Drag to Move** — left-click and drag anywhere
- **Rotating Quotes** — 60+ AI memes cycling in the footer
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

1. Open [platform.deepseek.com](https://platform.deepseek.com/usage) with **Chrome** and log in
2. Press **F12** → **Console**, then paste:

```js
JSON.parse(localStorage.getItem('userToken')).value
```

3. Copy the output string

### 3. Run

```bash
click main.pyw
```

On first launch, a dialog prompts you to paste the token. It is saved in `config.json` afterward.

## Configuration (`config.json`)

| Key | Type | Default | Description |
|-----|------|---------|-------------|
| `bearer_token` | string | — | Auth token from platform.deepseek.com |
| `refresh_interval` | integer | 10 | Auto-refresh interval in seconds (min 3) |
| `hover_fade` | boolean | true | Fade widget on mouse hover |
| `pin_window` | boolean | true | Keep window always on top |
| `currency` | string | "CNY" | Display currency (CNY/USD/CAD/JPY) |
| `lite_mode` | boolean | false | Compact lite mode |
| `theme` | string | "Default" | Color theme |
| `auto_snap` | boolean | false | Edge auto-snap (Beta) |

## Controls

| Action | Effect |
|--------|--------|
| Left-click + drag | Move window |
| Right-click | Full context menu (refresh/charts/lite/pin/currency/theme/restart/exit) |
| System tray (left-click) | Toggle show/hide |
| System tray (right-click) | Full menu with all toggles |
| Mouse hover | Fade to 25% opacity |
| Ctrl+Tab / Ctrl+T | Toggle sidebar charts panel |
| Hover when snapped | Peek window, auto-retract on leave |

## Themes

| Theme | Style |
|-------|-------|
| Default | Dark cyberpunk blue |
| Amber Glow | Warm amber |
| Frost Blue | Cool frost |
| Verdant Green | Forest green |
| Soft Pastel | Light pink/blue/white |
| Midnight Glow | Dark with orange accents |

## Project Structure

```
deepseek-widget/
├── main.pyw             # Entry point + system tray
├── widget.py            # Pixel-art GUI (snap, charts, themes)
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
- Edge snap is Beta — please report issues on GitHub.
- Token auto-extraction via Playwright is optional: `pip install playwright && playwright install chromium`

## License

[CC BY-NC 4.0](LICENSE) — Attribution-NonCommercial 4.0 International

-----
