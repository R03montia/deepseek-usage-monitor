"""Retro pixel-art desktop widget for DeepSeek API monitoring."""

import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime, date
from typing import Any
from itertools import cycle
import threading

from api import DeepSeekPlatform
from config import get_refresh_interval, get_pin_window, get_currency, get_lite_mode, get_theme, get_auto_snap, load_config, save_config

# ── Colors ─────────────────────────────────────────────────────────────────
# Module-level color names — updated by apply_theme() at runtime.
BG      = "#0f0f1a"
CARD    = "#19192e"
B1      = "#6a6a8a"
B2      = "#4a4a6a"
BC      = "#35355a"

W0      = "#f0f0ff"
W1      = "#d0d0ea"
W2      = "#b0b0cc"
BLUE    = "#7dcfff"
GREEN   = "#9ece6a"
RED     = "#ff6b6b"
YELLOW  = "#e0af68"
ORANGE  = "#ff9e64"
PURPLE  = "#bb9af7"

PGB     = "#2a2a3e"
PGFG    = "#7aa2f7"
PGCA    = "#e0af68"
PGDA    = "#ff6b6b"

MB      = "#2a2a3e"
MENU_BG = "#19192e"
MENU_FG = "#f0f0ff"
MENU_ABG = "#7dcfff"
MENU_AFG = "#0f0f1a"

THEMES = {
    "Default": {
        "BG": "#0f0f1a", "CARD": "#19192e",
        "B1": "#6a6a8a", "B2": "#4a4a6a", "BC": "#35355a",
        "W0": "#f0f0ff", "W1": "#d0d0ea", "W2": "#b0b0cc",
        "BLUE": "#7dcfff", "GREEN": "#9ece6a", "RED": "#ff6b6b",
        "YELLOW": "#e0af68", "ORANGE": "#ff9e64", "PURPLE": "#bb9af7",
        "PGB": "#2a2a3e", "PGFG": "#7aa2f7", "PGCA": "#e0af68", "PGDA": "#ff6b6b",
        "MB": "#2a2a3e",
        "MENU_BG": "#19192e", "MENU_FG": "#f0f0ff", "MENU_ABG": "#7dcfff", "MENU_AFG": "#0f0f1a",
    },
    "Amber Glow": {
        "BG": "#1a0a05", "CARD": "#2a1410",
        "B1": "#b07050", "B2": "#804030", "BC": "#4a2820",
        "W0": "#fff0e8", "W1": "#e8d0c0", "W2": "#c8a890",
        "BLUE": "#ff8c42", "GREEN": "#d162a4", "RED": "#e05555",
        "YELLOW": "#f0b060", "ORANGE": "#e06030", "PURPLE": "#c04080",
        "PGB": "#3a2018", "PGFG": "#ff8c42", "PGCA": "#e0a060", "PGDA": "#e05040",
        "MB": "#3a2018",
        "MENU_BG": "#2a1410", "MENU_FG": "#fff0e8", "MENU_ABG": "#ff8c42", "MENU_AFG": "#1a0a05",
    },
    "Frost Blue": {
        "BG": "#0a0f1a", "CARD": "#141e2e",
        "B1": "#6070a0", "B2": "#405070", "BC": "#2a3550",
        "W0": "#e8f0ff", "W1": "#c0d0ea", "W2": "#90a0c0",
        "BLUE": "#5ba0d0", "GREEN": "#7bc8a4", "RED": "#e06060",
        "YELLOW": "#d4b060", "ORANGE": "#c08050", "PURPLE": "#8890d0",
        "PGB": "#1a2540", "PGFG": "#5ba0d0", "PGCA": "#88c0e8", "PGDA": "#e06060",
        "MB": "#1a2540",
        "MENU_BG": "#141e2e", "MENU_FG": "#e8f0ff", "MENU_ABG": "#5ba0d0", "MENU_AFG": "#0a0f1a",
    },
    "Verdant Green": {
        "BG": "#0a120a", "CARD": "#142214",
        "B1": "#507050", "B2": "#305030", "BC": "#1e3a1e",
        "W0": "#e8f0e8", "W1": "#c0d8c0", "W2": "#90b090",
        "BLUE": "#60b0d0", "GREEN": "#6ab86a", "RED": "#e06060",
        "YELLOW": "#c0c060", "ORANGE": "#c08040", "PURPLE": "#80a080",
        "PGB": "#1e301e", "PGFG": "#6ab86a", "PGCA": "#b0b040", "PGDA": "#d06050",
        "MB": "#1e301e",
        "MENU_BG": "#142214", "MENU_FG": "#e8f0e8", "MENU_ABG": "#6ab86a", "MENU_AFG": "#0a120a",
    },
    "Soft Pastel": {
        "BG": "#f2ecee", "CARD": "#ffffff",
        "B1": "#c8b8bc", "B2": "#a89094", "BC": "#ddd0d4",
        "W0": "#1a1020", "W1": "#403050", "W2": "#705880",
        "BLUE": "#55cdfc", "GREEN": "#f7a8b8", "RED": "#e06070",
        "YELLOW": "#d4a060", "ORANGE": "#e08050", "PURPLE": "#b080c0",
        "PGB": "#e8e0e4", "PGFG": "#55cdfc", "PGCA": "#f7a8b8", "PGDA": "#e06070",
        "MB": "#e8e0e4",
        "MENU_BG": "#ffffff", "MENU_FG": "#1a1020", "MENU_ABG": "#55cdfc", "MENU_AFG": "#ffffff",
    },
    "Midnight Glow": {
        "BG": "#0a0a0a", "CARD": "#1a1a1a",
        "B1": "#505050", "B2": "#303030", "BC": "#2a2a2a",
        "W0": "#f0f0f0", "W1": "#d0d0d0", "W2": "#a0a0a0",
        "BLUE": "#ffa500", "GREEN": "#ffa500", "RED": "#e05050",
        "YELLOW": "#ffbb40", "ORANGE": "#ff8800", "PURPLE": "#b07040",
        "PGB": "#1a1a1a", "PGFG": "#ffa500", "PGCA": "#ffbb40", "PGDA": "#e05050",
        "MB": "#1a1a1a",
        "MENU_BG": "#1a1a1a", "MENU_FG": "#f0f0f0", "MENU_ABG": "#ffa500", "MENU_AFG": "#0a0a0a",
    },
}

W, H = 380, 350
W_LITE, H_LITE = 310, 230
SIDEBAR_WIDTH = 200  # 侧边栏宽度


# ── Rotating quotes ────────────────────────────────────────────────────────
QUOTES = cycle([
    "Tokens: the currency of AI",
    "Cached tokens don't cost a thing",
    "1M tokens ~ 750 pages of text",
    "Quality > Quantity in prompting",
    "Cache is king, hit rate is queen",
    "Think before you prompt",
    "Every token tells a story",
    "Input is cheap, output is art",
    "V4 Flash: speed demon",
    "Token economy: spend wisely",
    "Short prompt, long thinking",
    "Cache hit = free lunch",
    "DeepSeek V4 goes brrr",
    "Prompt engineering is 90% of it",
    "Good cache = happy wallet",
    "A token saved is a token earned",
    "Your context window is not a dumpster",
    "Garbage in, garbage out — token edition",
    "Temperature is not your personality slider",
    "Top-p: like temperature but different",
    "Stop wasting tokens on 'As an AI...'",
    "System prompt: where dreams come to die",
    "Few-shot > zero-shot > no-shot",
    "Chain of thought > chain of prayers",
    "RAG: because fine-tuning is expensive",
    "Streaming: instant gratification",
    "Logprobs: the AI's confidence issues",
    "Embeddings: everything is a vector",
    "Attention is all you need (and tokens)",
    "Tokens in, miracles out",
    "Fine-tuning? More like fine-spending",
    "RLHF: the art of saying no to AI",
    "Temperature 0: boring but reliable",
    "Temperature 2: chaos goblin mode",
    "It's not hallucinating, it's being creative",
    "AI: Also Incorrect",
    "The best model is the one you can afford",
    "Context window: never big enough",
    "101 tokens in a 100-token window",
    "API key: handle with care",
    "Rate limit: the universe saying 'chill'",
    "Token limit: your essay's nemesis",
    "Beam search? I barely know her",
    "Sampling temperature: spicy or bland",
    "Prompt: the magic spell of the 21st century",
    "Tokens are just expensive Lego blocks",
    "The Bill: motivation to write shorter prompts",
    "AI didn't take your job, your prompt did",
    "I'd tell you a token joke, but it costs ¥0.01",
    "V4: still cheaper than therapy",
    "The cache hit rate is 100% in my dreams",
    "Keep calm and cache on",
    "Token count: what's in your wallet?",
    "Clean prompt, clean response",
    "Your prompt is showing",
    "DeepSeek: deep thoughts, deep savings",
    "Prompt whisperer",
    "One-shot to rule them all",
    "Retry with backoff: the programmer's prayer",
    "Stream: when you want answers now",
    "Token: the smallest unit of hope",
    "json mode: structured chaos",
    "Your API key is showing, mortal",
    "Rate limited by the universe",
    "Tokens are finite, wisdom is not",
    "This quote cost 47 tokens to render",
    "DeepSeek: smarter than your toaster",
    "I think, therefore I deepseek",
    "My other car is a neural net",
    "DeepSeek: your AI wingman",
    "Token monster feeds on prompts",
    "Too many tokens, not enough time",
    "DeepSeek: making magic since v4",
    "I came, I saw, I deepseeked",
    "Warning: may contain sarcasm",
    "AI: actually incompetent",
    "DeepSeek: the bill always comes",
    "Token inflation is real",
    "Have you hugged your API today?",
    "DeepSeek: cheaper than coffee",
    "I'd prompt that",
    "Token: the new cryptocurrency",
    "AI: artificial banter",
    "DeepSeek dreams of electric sheep",
    "Ask me about my token count",
    "Your prompt is showing again",
    "Keep calm and prompt on",
    "DeepSeek: try me, I'm free...ish",
    "Token limit: a cruel joke",
    "I need more context",
    "DeepSeek: the thinking man's AI",
    "Output: where dreams cost tokens",
    "DeepSeek: be specific or else",
    "Tokens aren't cheap, neither am I",
    "AI wrote this, deal with it",
    "DeepSeek approved by 4/5 dentists",
    "Zero-shot: the lazy genius",
    "DeepSeek: less talk, more tokens",
    "In AI we trust... mostly",
    "Token go brrr",
    "Your context window is leaking",
    "DeepSeek: the silent thinker",
    "Hallucination: feature not bug",
    "I'm not arguing, I'm prompting",
    "DeepSeek: my therapist is AI",
    "Warning: AI at work",
    "Be nice to me, I'm AI",
    "Token: measure of my effort",
    "I speak deepseek fluently",
    "One does not simply prompt",
    "DeepSeek: your digital twin",
    "API key: don't leave home",
    "AI can't cook... yet",
    "DeepSeek: still cheaper than GPU",
    "Prompt responsibly",
    "I deepseek, therefore I am",
])


def _4(v):
    try: return f"{float(v):.4f}"
    except: return "--"


def _2(v):
    try: return f"{float(v):.2f}"
    except: return "--"


def _fmt_num(v):
    try: return f"{int(v):,}"
    except: return "--"


class Widget:
    def __init__(self, token: str):
        self.api = DeepSeekPlatform(token)
        self._data = None
        self._dx = self._dy = 0
        self._quote = ""

        # Config
        self._interval = get_refresh_interval() * 1000
        self._pin_window = get_pin_window()
        self._currency = get_currency()
        self._rate = 1.0
        self._dragging = False
        self._sidebar_visible = True
        self._animating = False
        self._lite_mode = get_lite_mode()
        self._theme = get_theme()

        self.root = tk.Tk()
        self.root.title("Tokens Monitor")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", self._pin_window, "-alpha", 0.0)
        self.root.configure(bg=BG)
        iw, ih = (W_LITE, H_LITE) if self._lite_mode else (W, H)
        self.root.geometry(f"{iw}x{ih}")

        self.f1 = tkfont.Font(family="Courier New", size=13, weight="bold")
        self.f2 = tkfont.Font(family="Courier New", size=11, weight="bold")
        self.f3 = tkfont.Font(family="Courier New", size=10)
        self.f5 = tkfont.Font(family="Courier New", size=26, weight="bold")

        # 主Canvas（左侧信息面板）
        self.cv = tk.Canvas(self.root, width=W, height=H,
                            bg=BG, highlightthickness=0, bd=0)
        self.cv.pack(side="left", fill="both", expand=False)

        # 侧边栏Canvas（图表区域）
        self.sidebar_cv = tk.Canvas(self.root, width=0, height=H,
                                   bg=CARD, highlightthickness=0, bd=0)
        self.sidebar_cv.pack(side="right", fill="both", expand=False)

        self._dd: list[str] = []
        self._updating = False  # guard against stacked API calls
        self._deferred_refresh_id = None  # cancelable deferred refresh timer

        # Snap state
        self._auto_snap = get_auto_snap()
        self._snapped = False
        self._snap_edge = None
        self._peeking = False
        self._snap_restore = {}
        self._snap_after_id = None
        self._peek_timer_id = None
        self._snap_glow_items: list[str] = []
        self._snap_click_unsnap = False  # True if _ds just unsnapped (prevent re-snap on click)
        self._snap_click_pos = None      # 记录 unsnap 时的窗口位置，用于判断是否移动过
        self._snap_animating = False     # True during snap/peek animation (suppress Leave events)

        self._tooltip_after_id = None  # 延迟隐藏定时器
        self._tooltip_fade_id = None   # 淡入淡出动画定时器
        self._last_bar_index = -1      # 当前悬停的柱子索引
        self._menu_closed = False      # 右键菜单关闭后短暂阻止吸附
        self._startup_done = False     # 首次数据加载后淡入

        # 拖拽事件：绑定到两个 canvas（root 不绑，避免重复触发）
        for widget in (self.cv, self.sidebar_cv):
            widget.bind("<Button-1>", self._ds)
            widget.bind("<B1-Motion>", self._dm)
            widget.bind("<ButtonRelease-1>", self._de)
            widget.bind("<Button-3>", self._pop)
        self.sidebar_cv.bind("<Leave>", lambda e: self._on_sidebar_leave())
        # 键盘快捷键：Ctrl+Tab 或 Ctrl+T 切换侧边栏
        self.root.bind("<Control-Tab>", lambda e: self.toggle_sidebar())
        self.root.bind("<Control-t>", lambda e: self.toggle_sidebar())

        # Snap peek events — bound on root for whole-window coverage
        self.root.bind("<Enter>", self._on_peek_enter, add="+")
        self.root.bind("<Leave>", self._on_peek_leave, add="+")

        self._fetch_exchange_rate()
        self._apply_theme(self._theme)
        self._draw_static()
        if self._sidebar_visible:
            self.sidebar_cv.config(width=SIDEBAR_WIDTH)
            self.root.geometry(f"{W + SIDEBAR_WIDTH}x{H}")
            # 暂不绘制图表——数据到达后再画，配合淡入
        self._tick()
        self.root.after(5000, self._startup_fallback)

    # ═══════════ CURRENCY HELPERS ═══════════

    @property
    def _currency_symbol(self):
        return {"CNY": "¥", "USD": "$", "CAD": "$", "JPY": "¥"}.get(self._currency, "¥")

    def _conv(self, amount):
        """Convert amount from CNY to current currency."""
        try:
            return float(amount) * self._rate
        except (ValueError, TypeError):
            return 0.0

    def _fmt_curr(self, amount, decimals=2):
        """Format amount in current currency with symbol."""
        try:
            val = self._conv(amount)
            return f"{self._currency_symbol}{val:.{decimals}f}"
        except (ValueError, TypeError):
            return f"{self._currency_symbol}--"

    def _fetch_exchange_rate(self):
        """Fetch live exchange rate from open.er-api.com (CNY base)."""
        if self._currency == "CNY":
            self._rate = 1.0
            return
        try:
            import requests
            resp = requests.get("https://open.er-api.com/v6/latest/CNY", timeout=10)
            data = resp.json()
            if data.get("result") == "success":
                self._rate = data["rates"].get(self._currency, 1.0)
        except Exception:
            self._rate = 1.0

    def toggle_pin(self) -> bool:
        """Toggle always-on-top. Return new state."""
        self._pin_window = not self._pin_window
        self.root.after(0, lambda: self.root.attributes("-topmost", self._pin_window))
        try:
            cfg = load_config()
            cfg["pin_window"] = self._pin_window
            save_config(cfg)
        except Exception:
            pass
        return self._pin_window

    def get_pin_window(self) -> bool:
        return self._pin_window

    def get_theme(self) -> str:
        return self._theme

    def _apply_theme(self, name: str):
        """Apply theme colors to module-level globals and redraw."""
        colors = THEMES.get(name, THEMES["Default"])
        for k, v in colors.items():
            globals()[k] = v
        self._theme = name
        self.root.configure(bg=BG)
        self.cv.configure(bg=BG)
        self.sidebar_cv.configure(bg=CARD)

    def apply_theme(self, name: str):
        """Public: apply theme with crossfade, persist, redraw."""
        if name == self._theme:
            return
        self._crossfade_to_theme(name)

    def _crossfade_to_theme(self, name):
        """窗口淡出 → 切换主题重绘 → 淡入"""
        target = float(self.root.attributes("-alpha"))
        steps = 6
        saved_data = self._data  # 保存旧数据用于过渡预览

        def _apply():
            self._apply_theme(name)
            try:
                cfg = load_config()
                cfg["theme"] = self._theme
                save_config(cfg)
            except Exception:
                pass
            self.cv.delete("all")
            self._dd.clear()
            self._draw_static()
            # 用旧数据 + 新颜色立即渲染，避免过渡期间空白闪烁
            if saved_data:
                self._data = saved_data
                self._draw()
                if self._sidebar_visible:
                    self._draw_charts()
            # 后台刷新真实数据
            self.update_data()
            self.root.after(15, _fade_in)

        def _fade_out(i=0):
            p = (i + 1) / steps
            self.root.attributes("-alpha", target * (1 - p) + 0.05 * p)
            if i + 1 < steps:
                self.root.after(20, lambda: _fade_out(i + 1))
            else:
                _apply()

        def _fade_in(i=0):
            p = (i + 1) / steps
            self.root.attributes("-alpha", 0.05 * (1 - p) + target * p)
            if i + 1 < steps:
                self.root.after(20, lambda: _fade_in(i + 1))

        _fade_out()

    # ═══════════ STARTUP FADE-IN ═══════════

    def _startup_fade_in(self):
        """首次数据加载后淡入窗口 — 从透明平滑渐显"""
        if self._startup_done:
            return
        self._startup_done = True
        target = 0.96
        steps = 8

        def _fade(i=0):
            p = (i + 1) / steps
            self.root.attributes("-alpha", target * p)
            if i + 1 < steps:
                self.root.after(20, lambda: _fade(i + 1))

        _fade()

    def _startup_fallback(self):
        """启动后 5 秒数据仍未到则强制显示（避免网络慢时一直空白）"""
        if not self._startup_done:
            self._startup_fade_in()

    def get_lite_mode(self) -> bool:
        return self._lite_mode

    def get_currency_code(self) -> str:
        return self._currency

    def set_currency(self, code: str):
        """Switch display currency, fetch rate, redraw."""
        if code == self._currency:
            return
        self._currency = code
        self._fetch_exchange_rate()
        try:
            cfg = load_config()
            cfg["currency"] = self._currency
            save_config(cfg)
        except Exception:
            pass
        self.update_data()

    def _restart(self):
        """Restart the application."""
        self.root.quit()
        self.root.destroy()
        import sys
        import subprocess
        import os
        subprocess.Popen([sys.executable, os.path.abspath(sys.argv[0])])
        os._exit(0)

    # ═══════════ LAYOUT ═══════════
    # Layout plan:
    #  0-44   title bar (title y=22, divider y=44)
    # 46-150  BALANCE card (104px)
    #   54 header, 76 subtitle, 102 big ¥, 138-148 progress bar
    # 152-280 TODAY card (128px)
    #   160 header, 180 TOKENS, 204 INPUT, 228 OUTPUT, 252-268 CACHE
    # 282-350 footer
    #   292 month/status, 318 rotating quote, 336 refresh

    def _draw_static(self):
        if self._lite_mode:
            self._draw_static_lite()
            return
        cv = self.cv

        # Outer pixel borders
        cv.create_rectangle(2, 2, W-2, H-2, outline=B1, width=2)
        cv.create_rectangle(6, 6, W-6, H-6, outline=B2, width=1)

        # ── Title ──
        cv.create_text(14, 22, text="TOKENS MONITOR",
                       font=self.f1, fill=W0, anchor="w")
        if self._theme == "Midnight Glow":
            x0 = 14 + self.f1.measure("TOKENS ")
            rw = self.f1.measure("MONITOR")
            cv.create_rectangle(x0, 24, x0 + rw, 26, fill=BLUE, outline="")
        cv.create_oval(W-28, 15, W-16, 27, fill=GREEN, outline="", tags="dot")
        cv.create_text(W-36, 22, text="", font=self.f3, fill=B1, anchor="e", tags="fcur")
        self._hr(12, 44, W-12)

        # ── Balance card (46-150) ──
        cv.create_rectangle(10, 46, W-10, 150, fill=CARD, outline=BC, width=1)
        cv.create_text(18, 54, text="BALANCE", font=self.f3, fill=W2, anchor="w")
        # subtitle: wallet / free / used
        cv.create_text(18, 76, text="", font=self.f3,
                       fill=W1, anchor="w", tags="bal_sub")
        # big amount
        cv.create_text(18, 102, text="", font=self.f5,
                       fill=W0, anchor="w", tags="bal_amt")
        # remaining label above progress bar
        cv.create_text(18, 130, text="REMAINING", font=self.f3,
                       fill=B1, anchor="w", tags="pul")
        # progress bar
        cv.create_rectangle(18, 138, W-18, 150, fill=PGB, outline=BC, width=1, tags="pbg")
        cv.create_text(20, 144, text="", font=self.f3,
                       fill=B1, anchor="w", tags="ppct")

        # ── Today card (152-280) ──
        cv.create_rectangle(10, 152, W-10, 280, fill=CARD, outline=BC, width=1)
        cv.create_text(18, 160, text="TODAY", font=self.f3, fill=W2, anchor="w")

        # TOKENS row
        cv.create_text(18, 180, text="TOKENS", font=self.f3, fill=W1, anchor="w")
        cv.create_text(90, 180, text="", font=self.f2, fill=W0, anchor="w", tags="tt")

        # INPUT row + mini bar
        cv.create_text(18, 212, text="INPUT", font=self.f3, fill=W1, anchor="w")
        cv.create_text(85, 212, text="", font=self.f2, fill=W0, anchor="w", tags="tp")
        cv.create_rectangle(224, 206, W-18, 218, fill=MB, outline="", tags="ibg")
        cv.create_rectangle(224, 206, 224, 218, fill=BLUE, outline="", tags="ifl")
        cv.create_text(226, 212, text="", font=self.f3,
                       fill=B1, anchor="w", tags="ipct")

        # OUTPUT row + mini bar
        cv.create_text(18, 236, text="OUTPUT", font=self.f3, fill=W1, anchor="w")
        cv.create_text(85, 236, text="", font=self.f2, fill=W0, anchor="w", tags="tc")
        cv.create_rectangle(224, 230, W-18, 242, fill=MB, outline="", tags="obg")
        cv.create_rectangle(224, 230, 224, 242, fill=PURPLE, outline="", tags="ofl")
        cv.create_text(226, 236, text="", font=self.f3,
                       fill=B1, anchor="w", tags="opct")

        # CACHE row (prominent, with separator)
        cv.create_rectangle(18, 252, W-18, 254, fill=BC, outline="")
        cv.create_text(18, 266, text="CACHE", font=self.f3, fill=W1, anchor="w")
        cv.create_text(75, 266, text="", font=self.f2, fill=GREEN, anchor="w", tags="cr")
        # cache full-width mini bar
        cv.create_rectangle(170, 260, W-18, 272, fill=MB, outline=BC, width=1, tags="cbg")
        cv.create_rectangle(170, 260, 170, 272, fill=GREEN, outline="", tags="cfl")
        cv.create_text(172, 266, text="", font=self.f3,
                       fill=B1, anchor="w", tags="cpct")

        # ── Footer (282-350) ──
        self._hr(12, 284, W-12)
        # month line
        cv.create_text(18, 296, text="", font=self.f3, fill=W1, anchor="w", tags="fm")
        cv.create_text(W-18, 296, text="", font=self.f3, fill=W1, anchor="e", tags="fs")
        # rotating quote
        cv.create_text(W//2, 320, text="", font=self.f3,
                       fill=W2, anchor="center", tags="fq")
        # refresh time
        cv.create_text(W//2, H-14, text="", font=self.f3,
                       fill=W2, anchor="center", tags="ft")

    def _draw_static_lite(self):
        cv = self.cv
        w, h = W_LITE, H_LITE

        # Outer pixel borders
        cv.create_rectangle(2, 2, w-2, h-2, outline=B1, width=2)
        cv.create_rectangle(6, 6, w-6, h-6, outline=B2, width=1)

        # ── Title ──
        cv.create_text(12, 16, text="TOKENS MONITOR", font=self.f2, fill=W0, anchor="w")
        if self._theme == "Midnight Glow":
            x0 = 12 + self.f2.measure("TOKENS ")
            rw = self.f2.measure("MONITOR")
            cv.create_rectangle(x0, 18, x0 + rw, 20, fill=BLUE, outline="")
        cv.create_oval(w-24, 11, w-14, 21, fill=GREEN, outline="", tags="dot")
        cv.create_text(w-30, 16, text="", font=self.f3, fill=B1, anchor="e", tags="fcur")
        for x in range(8, w-8, 8):
            cv.create_rectangle(x, 28, x+5, 29, fill=B2, outline="")

        # ── Balance card ──
        cv.create_rectangle(8, 34, w-8, 106, fill=CARD, outline=BC, width=1)
        cv.create_text(14, 38, text="BALANCE", font=self.f3, fill=W2, anchor="w")
        cv.create_text(w//2, 68, text="", font=self.f5, fill=W0, anchor="center", tags="bal_amt")
        cv.create_text(14, 88, text="", font=self.f3, fill=W1, anchor="w", tags="bal_sub")
        cv.create_rectangle(14, 96, w-14, 104, fill=PGB, outline=BC, width=1, tags="pbg")

        # ── Today card ──
        cv.create_rectangle(8, 112, w-8, 168, fill=CARD, outline=BC, width=1)
        cv.create_text(14, 116, text="TODAY", font=self.f3, fill=W2, anchor="w")
        cv.create_text(14, 140, text="", font=self.f3, fill=W0, anchor="w", tags="tt_lite")
        cv.create_text(w-14, 140, text="", font=self.f2, fill=BLUE, anchor="e", tags="ftc")
        cv.create_text(14, 158, text="", font=self.f3, fill=GREEN, anchor="w", tags="cr_lite")

        # ── Month line ──
        cv.create_text(14, 178, text="MONTH", font=self.f3, fill=W2, anchor="w")
        cv.create_text(14, 196, text="", font=self.f3, fill=W1, anchor="w", tags="fm_lite")

        # ── Footer ──
        for x in range(8, w-8, 8):
            cv.create_rectangle(x, 210, x+5, 211, fill=B2, outline="")
        cv.create_text(w//2, h-10, text="", font=self.f3, fill=W2, anchor="center", tags="ft")

    def _hr(self, x1, y, x2):
        for x in range(x1, x2, 8):
            self.cv.create_rectangle(x, y, x+4, y+2, fill=B2, outline="")

    # ═══════════ DYNAMIC ═══════════

    def _z(self):
        for t in self._dd:
            self.cv.delete(t)
        self._dd.clear()

    def _tg(self):
        t = f"d{len(self._dd)}"
        self._dd.append(t)
        return t

    def update_data(self):
        """Thread-safe async data refresh — never blocks the main loop."""
        if self._updating:
            return
        self._updating = True
        threading.Thread(target=self._fetch_worker, daemon=True).start()

    def _fetch_worker(self):
        """Run API call in background thread, schedule draw on main thread."""
        try:
            data = self.api.fetch_all(target_date=date.today().isoformat())
            self.root.after(0, self._on_fetch_done, data)
        except Exception as exc:
            self.root.after(0, self._on_fetch_error, str(exc))

    def _on_fetch_done(self, data):
        self._data = data
        self._quote = next(QUOTES)
        self._draw()
        if self._sidebar_visible:
            self._draw_charts()
        self._updating = False
        if not self._startup_done:
            self._startup_fade_in()

    def _on_fetch_error(self, msg):
        if self._data is None:
            self._data = {}
        self._data["error"] = msg
        self._data["ok"] = False
        self._draw()
        if self._sidebar_visible:
            self._draw_charts()
        self._updating = False
        if not self._startup_done:
            self._startup_fade_in()

    def _draw(self):
        # When snapped and not peeking, skip drawing — strip has no data items
        if self._snapped and not self._peeking:
            return
        self._z()
        cv = self.cv
        d = self._data or {}
        err = d.get("error")

        if err:
            cv.itemconfig("dot", fill=RED)
            cv.itemconfig("bal_amt", text="ERR", fill=RED)
            cv.itemconfig("ft", text="~ error ~")
            return

        cv.itemconfig("dot", fill=GREEN if d.get("ok") else YELLOW)
        cv.itemconfig("fcur", text=self._currency)

        if self._lite_mode:
            self._draw_lite(d)
        else:
            self._draw_normal(d)

    def _draw_normal(self, d):
        cv = self.cv

        # ── Balance card ──
        bal = float(d.get("balance", 0) or 0)
        mc  = float(d.get("monthly_cost", 0) or 0)
        tot = bal + mc
        pct = max(0, min(bal / tot, 1)) if tot else 1

        cv.itemconfig("bal_amt", text=self._fmt_curr(bal))

        bonus = float(d.get("bonus_balance", 0) or 0)
        cv.itemconfig("bal_sub",
                      text=f"Wallet {self._fmt_curr(bal)}  |  Free {self._fmt_curr(bonus)}  |  Used {int((1-pct)*100)}%")

        # progress bar fill
        pw = int(340 * pct)
        if pw > 0:
            bc = PGDA if pct < 0.15 else (PGCA if pct < 0.40 else PGFG)
            for bx in range(18, 18+pw-2, 4):
                bw = min(4, 18+pw-bx)
                cv.create_rectangle(bx, 140, bx+bw, 148,
                                    fill=bc, outline="", tags=self._tg())
        cv.itemconfig("ppct", text=f"{int(pct*100)}%",
                      fill=W1 if pw <= 0 else B1)

        # ── Today card ──
        ttl = d.get("today_total", 0)
        pr  = d.get("today_prompt", 0)
        co  = d.get("today_completion", 0)
        ch  = d.get("today_cache_hit", 0)
        cm  = d.get("today_cache_miss", 0)
        ct  = ch + cm

        cv.itemconfig("tt", text=f"{ttl:,}")
        cv.itemconfig("tp", text=f"{pr:,}")
        cv.itemconfig("tc", text=f"{co:,}")

        # mini bars
        ip = (pr/ttl*100) if ttl else 0
        op = (co/ttl*100) if ttl else 0
        iw = int(134 * ip / 100)
        ow = int(134 * op / 100)
        cv.coords("ifl", 224, 206, 224+iw, 218)
        cv.itemconfig("ipct", text=f"{ip:.1f}%")
        cv.coords("ofl", 224, 230, 224+ow, 242)
        cv.itemconfig("opct", text=f"{op:.1f}%")

        # ── Cache ──
        crate = (ch/ct*100) if ct else 0
        cv.itemconfig("cr", text=f"{crate:.1f}%")

        cw = int(190 * crate / 100)
        cv.coords("cfl", 170, 260, 170+cw, 272)
        if crate > 80:
            cv.itemconfig("cfl", fill=GREEN)
            cv.itemconfig("cpct", text=f"{ch:,} / {ct:,}", fill=B1)
        elif crate > 50:
            cv.itemconfig("cfl", fill=BLUE)
            cv.itemconfig("cpct", text=f"{ch:,} / {ct:,}", fill=B1)
        else:
            cv.itemconfig("cfl", fill=ORANGE)
            cv.itemconfig("cpct", text=f"{ch:,} / {ct:,}", fill=B1)

        # today cost (right of TOKENS row)
        cv.create_text(W-18, 180, text=self._fmt_curr(d.get('today_cost',0), 4),
                       font=self.f2, fill=BLUE, anchor="e", tags=self._tg())

        # 侧边栏图表同步刷新
        if self._sidebar_visible:
            self._draw_charts()

        # ── Footer ──
        mt = d.get("monthly_tokens", 0)
        cv.itemconfig("fm",
                      text=f"MONTH  {mt:,} tkns  {self._fmt_curr(d.get('monthly_cost',0), 4)}")
        cv.itemconfig("fs", text=f"LEFT {int(pct*100)}%")
        cv.itemconfig("fq", text=self._quote)
        cv.itemconfig("ft", text=f"~ {datetime.now().strftime('%H:%M:%S')} ~")

    def _draw_lite(self, d):
        cv = self.cv
        w = W_LITE

        # ── Balance card ──
        bal = float(d.get("balance", 0) or 0)
        mc  = float(d.get("monthly_cost", 0) or 0)
        tot = bal + mc
        pct = max(0, min(bal / tot, 1)) if tot else 1
        cv.itemconfig("bal_amt", text=self._fmt_curr(bal))
        bonus = float(d.get("bonus_balance", 0) or 0)
        cv.itemconfig("bal_sub",
                      text=f"Wallet {self._fmt_curr(bal)}  |  Free {self._fmt_curr(bonus)}  |  Used {int((1-pct)*100)}%")
        # progress bar
        pw = int((w - 28) * pct)
        if pw > 0:
            bc = PGDA if pct < 0.15 else (PGCA if pct < 0.40 else PGFG)
            for bx in range(14, 14+pw-2, 4):
                bw = min(4, 14+pw-bx)
                cv.create_rectangle(bx, 97, bx+bw, 103, fill=bc, outline="", tags=self._tg())
        cv.create_text(w-16, 100, text=f"{int(pct*100)}%",
                       font=self.f3, fill=W1 if pw <= 0 else B1, anchor="e", tags=self._tg())

        # ── Today card ──
        ttl = d.get("today_total", 0)
        cv.itemconfig("tt_lite", text=f"TOKENS  {ttl:,}")
        cv.itemconfig("ftc", text=self._fmt_curr(d.get("today_cost", 0), 4))
        # cache hit rate
        ch = d.get("today_cache_hit", 0)
        cm = d.get("today_cache_miss", 0)
        ct = ch + cm
        crate = (ch / ct * 100) if ct else 0
        cv.itemconfig("cr_lite", text=f"CACHE  {crate:.1f}%  {ch:,}/{ct:,}" if ct else "")

        # ── Month line ──
        mt = d.get("monthly_tokens", 0)
        cv.itemconfig("fm_lite",
                      text=f"{mt:,} tkns  {self._fmt_curr(d.get('monthly_cost',0), 4)}")

        # ── Footer ──
        cv.itemconfig("ft", text=f"~ {datetime.now().strftime('%H:%M:%S')} ~")

    # ═══════════ AUTO SNAP ═══════════

    SNAP_THRESHOLD = 25       # px from edge to trigger snap
    SNAP_STRIP = 10           # width of snapped strip

    def _check_snap(self):
        """After drag-end, check proximity to screen edges. Snap if close."""
        rx = self.root.winfo_rootx()
        ry = self.root.winfo_rooty()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        edge = None
        if rx < self.SNAP_THRESHOLD:
            edge = "left"
        elif rx + rw > sw - self.SNAP_THRESHOLD:
            edge = "right"
        elif ry < self.SNAP_THRESHOLD:
            edge = "top"
        elif ry + rh > sh - self.SNAP_THRESHOLD:
            edge = "bottom"

        if edge:
            self._snap_to_edge(edge)

    def _do_deferred_refresh(self):
        """Fire update_data if we're still peeked."""
        self._deferred_refresh_id = None
        if self._peeking:
            self.update_data()

    def _cancel_deferred_refresh(self):
        """Cancel pending deferred refresh."""
        if self._deferred_refresh_id is not None:
            self.root.after_cancel(self._deferred_refresh_id)
            self._deferred_refresh_id = None

    def _snap_to_edge(self, edge: str):
        """Animate window shrinking to a thin strip on the given edge."""
        self._snapped = True
        self._snap_edge = edge
        self._snap_animating = True

        rx = self.root.winfo_rootx()
        ry = self.root.winfo_rooty()
        rw = self.root.winfo_width()
        rh = self.root.winfo_height()
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        # 夹紧 restore 位置到屏幕内，保证展开时窗口完全可见
        restore_x = max(0, min(rx, sw - rw))
        restore_y = max(0, min(ry, sh - rh))
        self._snap_restore = dict(x=restore_x, y=restore_y, w=rw, h=rh, sidebar=self._sidebar_visible)

        strip_w = self.SNAP_STRIP
        if edge == "left":
            new_x, new_y, new_w, new_h = 0, ry, strip_w, rh
        elif edge == "right":
            new_x, new_y, new_w, new_h = sw - strip_w, ry, strip_w, rh
        elif edge == "bottom":
            new_x, new_y, new_w, new_h = rx, sh - strip_w, rw, strip_w
        else:
            new_x, new_y, new_w, new_h = rx, 0, rw, strip_w

        # Close sidebar before animation begins
        if self._sidebar_visible:
            self._sidebar_visible = False
            self.sidebar_cv.delete("all")
            self.sidebar_cv.config(width=0)

        start_x, start_y, start_w, start_h = rx, ry, rw, rh
        dx, dy, dw, dh = new_x - start_x, new_y - start_y, new_w - start_w, new_h - start_h
        steps = 8

        def _anim(i=0):
            p = 1 - (1 - (i + 1) / steps) ** 2
            self.root.geometry(f"{int(start_w + dw * p)}x{int(start_h + dh * p)}+{int(start_x + dx * p)}+{int(start_y + dy * p)}")
            if i + 1 < steps:
                self.root.after(16, lambda: _anim(i + 1))
            else:
                self.root.geometry(f"{new_w}x{new_h}+{new_x}+{new_y}")
                self._snap_animating = False
                self._draw_snap_indicator()

        _anim()

        try:
            cfg = load_config()
            if not cfg.get("auto_snap"):
                cfg["auto_snap"] = True
                save_config(cfg)
        except Exception:
            pass

    def _draw_snap_indicator(self):
        """Thin edge strip with theme-colored glow."""
        self._clear_snap_indicator()
        cv = self.cv
        edge = self._snap_edge
        w = self.root.winfo_width()
        h = self.root.winfo_height()
        accent = BLUE

        cv.delete("all")
        cv.create_rectangle(0, 0, w, h, fill=BG, outline="", tags="snap_bg")

        if edge in ("left", "right"):
            cx = w // 2
            cv.create_rectangle(cx - 1, 1, cx + 2, h - 1, fill=accent, outline="", tags="snap_glow")
            for off in (3, 6, 10):
                cv.create_rectangle(cx - off, 2, cx + off, h - 2,
                                    fill=BG, outline=accent, width=1, tags="snap_glow")
        else:
            cy = h // 2
            cv.create_rectangle(2, cy - 1, w - 2, cy + 2, fill=accent, outline="", tags="snap_glow")
            for off in (3, 6, 10):
                cv.create_rectangle(4, cy - off, w - 4, cy + off,
                                    fill=BG, outline=accent, width=1, tags="snap_glow")

    def _clear_snap_indicator(self):
        self.cv.delete("snap_bg", "snap_glow")

    def _check_mouse_inside(self) -> bool:
        """Return True if the mouse pointer is within the window bounds."""
        try:
            rx = self.root.winfo_rootx()
            ry = self.root.winfo_rooty()
            rw = self.root.winfo_width()
            rh = self.root.winfo_height()
            mx = self.root.winfo_pointerx()
            my = self.root.winfo_pointery()
            return rx <= mx <= rx + rw and ry <= my <= ry + rh
        except Exception:
            return False

    def _on_peek_enter(self, _):
        if not self._snapped or self._peeking or self._dragging or self._snap_animating:
            return
        if self._snap_after_id:
            self.root.after_cancel(self._snap_after_id)
            self._snap_after_id = None
        self._start_peek()

    def _on_peek_leave(self, _):
        if not self._snapped or self._snap_animating:
            return
        # Double-check: ignore if mouse is still inside (prevents false leave during animation)
        if self._check_mouse_inside():
            return
        if not self._peeking:
            return  # Already a strip, no action needed
        self._end_peek()

    def _start_peek(self):
        """Animate from strip to full restore geometry. Draw content AFTER animation."""
        self._peeking = True
        self._snap_animating = True
        self._clear_snap_indicator()
        target = self._snap_restore
        start_x, start_y = self.root.winfo_rootx(), self.root.winfo_rooty()
        start_w, start_h = self.root.winfo_width(), self.root.winfo_height()

        steps = 8
        dx, dy = target["x"] - start_x, target["y"] - start_y
        dw, dh = target["w"] - start_w, target["h"] - start_h

        def _anim(i=0):
            p = 1 - (1 - (i + 1) / steps) ** 2
            self.root.geometry(f"{int(start_w + dw * p)}x{int(start_h + dh * p)}+{int(start_x + dx * p)}+{int(start_y + dy * p)}")
            if i + 1 < steps:
                self.root.after(16, lambda: _anim(i + 1))
            else:
                self.root.geometry(f"{target['w']}x{target['h']}+{target['x']}+{target['y']}")
                self._snap_animating = False
                # Now draw everything — canvas is at final size, one draw pass
                self.cv.delete("all")
                self._dd.clear()
                self._draw_static()
                if target.get("sidebar") and not self._lite_mode:
                    self._sidebar_visible = True
                    self.sidebar_cv.config(width=SIDEBAR_WIDTH)
                    self._draw_charts()
                self._draw()
                # Deferred background refresh (cancelable)
                self._deferred_refresh_id = self.root.after(200, self._do_deferred_refresh)

        _anim()

    def _end_peek(self):
        self._peeking = False  # 允许鼠标重新进入时重新触发 peek
        if self._snap_after_id:
            self.root.after_cancel(self._snap_after_id)
        self._snap_after_id = self.root.after(1500, self._re_snap)

    def _re_snap(self):
        self._snap_after_id = None
        self._cancel_deferred_refresh()
        if not self._snapped or self._dragging:
            return

        self._peeking = False
        self._snap_animating = True
        edge = self._snap_edge
        ry, rh = self._snap_restore["y"], self._snap_restore["h"]
        rx, rw = self._snap_restore["x"], self._snap_restore["w"]
        sw = self.root.winfo_screenwidth()
        sh = self.root.winfo_screenheight()

        strip_w = self.SNAP_STRIP
        if edge == "left":
            new_x, new_y, new_w, new_h = 0, ry, strip_w, rh
        elif edge == "right":
            new_x, new_y, new_w, new_h = sw - strip_w, ry, strip_w, rh
        elif edge == "bottom":
            new_x, new_y, new_w, new_h = rx, sh - strip_w, rw, strip_w
        else:
            new_x, new_y, new_w, new_h = rx, 0, rw, strip_w

        # Save sidebar state, close before animation
        self._snap_restore["sidebar"] = self._sidebar_visible
        if self._sidebar_visible:
            self._sidebar_visible = False
            self.sidebar_cv.delete("all")
            self.sidebar_cv.config(width=0)

        start_x, start_y = self.root.winfo_rootx(), self.root.winfo_rooty()
        start_w, start_h = self.root.winfo_width(), self.root.winfo_height()
        dx, dy = new_x - start_x, new_y - start_y
        dw, dh = new_w - start_w, new_h - start_h
        steps = 8

        def _anim(i=0):
            p = 1 - (1 - (i + 1) / steps) ** 2
            self.root.geometry(f"{int(start_w + dw * p)}x{int(start_h + dh * p)}+{int(start_x + dx * p)}+{int(start_y + dy * p)}")
            if i + 1 < steps:
                self.root.after(16, lambda: _anim(i + 1))
            else:
                self.root.geometry(f"{new_w}x{new_h}+{new_x}+{new_y}")
                self._snap_animating = False
                self._draw_snap_indicator()

        _anim()

    def _unsnap(self):
        """Restore full window from snapped state."""
        if not self._snapped:
            return
        self._cancel_deferred_refresh()
        if self._snap_after_id:
            self.root.after_cancel(self._snap_after_id)
            self._snap_after_id = None
        if self._peek_timer_id:
            self.root.after_cancel(self._peek_timer_id)
            self._peek_timer_id = None

        restore = self._snap_restore
        had_sidebar = restore.get("sidebar", False)
        self._snapped = False
        self._peeking = False
        self._snap_edge = None
        self._snap_restore = {}

        self.root.geometry(f"{restore['w']}x{restore['h']}+{restore['x']}+{restore['y']}")

        self._clear_snap_indicator()
        self.cv.delete("all")
        self._dd.clear()
        self._draw_static()
        if had_sidebar:
            self._sidebar_visible = True
            self.sidebar_cv.config(width=SIDEBAR_WIDTH)
            self._draw_charts()
        self.update_data()

    def toggle_auto_snap(self) -> bool:
        """Toggle auto-snap on/off. If turning off and currently snapped, unsnap."""
        self._auto_snap = not self._auto_snap
        if not self._auto_snap and self._snapped:
            self.root.after(0, self._unsnap)
        try:
            cfg = load_config()
            cfg["auto_snap"] = self._auto_snap
            save_config(cfg)
        except Exception:
            pass
        return self._auto_snap

    def get_auto_snap(self) -> bool:
        return self._auto_snap

    def _tick(self):
        self.update_data()
        self.root.after(self._interval, self._tick)

    def get_sidebar_visible(self) -> bool:
        return self._sidebar_visible

    # ═══════════ EVENTS ═══════════

    def _ds(self, e):
        self._dx = e.x_root - self.root.winfo_x()
        self._dy = e.y_root - self.root.winfo_y()
        # Unsnap if dragging from snapped state
        self._snap_click_unsnap = False
        if self._snapped:
            # Save restore BEFORE unsnap (winfo_x/y won't update until next event loop)
            saved = self._snap_restore
            self._unsnap()
            self._snap_click_unsnap = True
            self._snap_click_pos = (saved["x"], saved["y"])
            # Use SAVED geometry (not winfo_x/y which is still the old strip position)
            self._dx = e.x_root - saved["x"]
            self._dy = e.y_root - saved["y"]
        self._dragging = True

    def _dm(self, e):
        self.root.geometry(f"+{e.x_root-self._dx}+{e.y_root-self._dy}")

    def _de(self, _):
        self._dragging = False
        # 右键菜单刚关闭时不触发吸附，避免点按菜单外的误操作
        if self._menu_closed:
            self._menu_closed = False
            self._snap_click_unsnap = False
            self._snap_click_pos = None
            return
        if self._auto_snap:
            # 从 snap 拖出后：仅当窗口位置没动过（还原点附近）才跳过吸附
            if self._snap_click_unsnap and self._snap_click_pos:
                rx = self.root.winfo_rootx()
                ry = self.root.winfo_rooty()
                cx, cy = self._snap_click_pos
                if abs(rx - cx) > 10 or abs(ry - cy) > 10:
                    self._check_snap()
            else:
                self._check_snap()
        self._snap_click_unsnap = False
        self._snap_click_pos = None

    def _pop(self, _):
        # 取消待处理的重吸附定时器（倒计时期间点击右键）
        if self._snap_after_id:
            self.root.after_cancel(self._snap_after_id)
            self._snap_after_id = None
        if self._peek_timer_id:
            self.root.after_cancel(self._peek_timer_id)
            self._peek_timer_id = None
        # Unsnap if right-clicking while snapped
        if self._snapped and not self._peeking:
            self._start_peek()

        m = tk.Menu(self.root, tearoff=0, bg=MENU_BG, fg=MENU_FG,
                    activebackground=MENU_ABG, activeforeground=MENU_AFG, font=self.f3)

        # 直接执行命令，再关闭菜单（Windows 上 tk_popup 非阻塞，延迟执行不可靠）
        def _pick(fn, *a):
            def _cmd():
                try:
                    fn(*a)
                finally:
                    self._menu_closed = True
                    self.root.after(300, lambda: setattr(self, '_menu_closed', False))
                    try: m.unpost()
                    except: pass
                    self.root.after_idle(m.destroy)
            return _cmd

        m.add_command(label="🔍 Refresh Now", command=_pick(self.update_data))
        m.add_separator()
        m.add_command(label="📊 Toggle Charts", command=_pick(self.toggle_sidebar))
        lite_label = "🔰 Lite Mode" if not self._lite_mode else "🔰 Full Mode"
        m.add_command(label=lite_label, command=_pick(self.toggle_lite_mode))
        m.add_separator()

        pin_label = "📌 Unpin Window" if self._pin_window else "📌 Pin Window"
        m.add_command(label=pin_label, command=_pick(self.toggle_pin))
        snap_label = "🧲 Unsnap (Beta)" if self._auto_snap else "🧲 Auto Snap (Beta)"
        m.add_command(label=snap_label, command=_pick(self.toggle_auto_snap))
        m.add_separator()

        # Currency submenu
        curr_menu = tk.Menu(m, tearoff=0, bg=MENU_BG, fg=MENU_FG,
                            activebackground=MENU_ABG, activeforeground=MENU_AFG, font=self.f3)
        for label, code in [("CNY  ¥", "CNY"), ("USD  $", "USD"), ("CAD  $", "CAD"), ("JPY  ¥", "JPY")]:
            curr_menu.add_command(
                label=f"{'✓ ' if self._currency == code else '   '}{label}",
                command=_pick(self.set_currency, code),
            )
        m.add_cascade(label="💱 Currency", menu=curr_menu)
        m.add_separator()

        # Theme submenu
        theme_menu = tk.Menu(m, tearoff=0, bg=MENU_BG, fg=MENU_FG,
                             activebackground=MENU_ABG, activeforeground=MENU_AFG, font=self.f3)
        for t_name in THEMES:
            theme_menu.add_command(
                label=f"{'✓ ' if self._theme == t_name else '   '}{t_name}",
                command=_pick(self.apply_theme, t_name),
            )
        m.add_cascade(label="🎨 Theme", menu=theme_menu)
        m.add_separator()

        m.add_command(label="🔄 Restart", command=_pick(self._restart))
        m.add_command(label="✕ Exit", command=_pick(self._ex))
        m.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        m.grab_release()

    def _ex(self):
        self.root.quit()
        self.root.destroy()

    def toggle_lite_mode(self):
        """Toggle lite mode on/off with smooth crossfade."""
        if self._snapped:
            self._unsnap()
        target_alpha = float(self.root.attributes("-alpha"))

        def _apply():
            self._lite_mode = not self._lite_mode
            try:
                cfg = load_config()
                cfg["lite_mode"] = self._lite_mode
                save_config(cfg)
            except Exception:
                pass
            if self._lite_mode and self._sidebar_visible:
                self._sidebar_visible = False
                self.sidebar_cv.delete("all")
            self.cv.delete("all")
            self._dd.clear()
            self._draw_static()
            w, h = (W_LITE, H_LITE) if self._lite_mode else (W, H)
            self.root.geometry(f"{w}x{h}")
            self.update_data()
            self.root.after(15, _fade_in)

        def _fade_out(i=0):
            p = (i + 1) / 6
            self.root.attributes("-alpha", target_alpha * (1 - p) + 0.05 * p)
            if i + 1 < 6:
                self.root.after(20, lambda: _fade_out(i + 1))
            else:
                _apply()

        def _fade_in(i=0):
            p = (i + 1) / 6
            self.root.attributes("-alpha", 0.05 * (1 - p) + target_alpha * p)
            if i + 1 < 6:
                self.root.after(20, lambda: _fade_in(i + 1))

        _fade_out()

    def toggle_sidebar(self):
        """切换侧边栏显示/隐藏，带动画"""
        if self._animating or self._lite_mode:
            return
        self._hide_bar_tooltip()
        self._sidebar_visible = not self._sidebar_visible
        # 展开前先画出图表，动画过程中内容立即可见
        if self._sidebar_visible:
            self._draw_charts()
        self._animate_sidebar()

    def _animate_sidebar(self):
        """Ease-out 动画：同步缩放侧边栏 Canvas 和根窗口宽度"""
        self._animating = True
        target_w = SIDEBAR_WIDTH if self._sidebar_visible else 0
        start_root_w = self.root.winfo_width()
        end_root_w = W + target_w
        steps = 10

        def step(i=0):
            # ease-out quad: 先快后慢
            p = 1 - (1 - (i + 1) / steps) ** 2
            cur_w = int(target_w * p) if target_w > 0 else int(SIDEBAR_WIDTH * (1 - p))
            cur_root = int(start_root_w + (end_root_w - start_root_w) * p)
            self.sidebar_cv.config(width=cur_w)
            self.root.geometry(f"{cur_root}x{H}")
            if i + 1 < steps:
                self.root.after(16, lambda: step(i + 1))
            else:
                self.sidebar_cv.config(width=target_w)
                self.root.geometry(f"{end_root_w}x{H}")
                if not self._sidebar_visible:
                    self.sidebar_cv.delete("all")
                self._animating = False

        step()

    def _draw_charts(self):
        """绘制侧边栏：月度趋势图，赛博像素风格"""
        self._hide_bar_tooltip()  # 重绘前清理残留 tooltip
        self.sidebar_cv.delete("all")
        d = self._data
        if not d:
            return

        w = SIDEBAR_WIDTH
        series = d.get("daily_series", [])
        if not series:
            self.sidebar_cv.create_text(w // 2, H // 2,
                                        text="No data yet", font=self.f3, fill=B1, anchor="center")
            return

        # 外侧像素边框（与主窗口一致）
        self.sidebar_cv.create_rectangle(2, 2, w - 2, H - 2, outline=B1, width=2)
        self.sidebar_cv.create_rectangle(6, 6, w - 6, H - 6, outline=B2, width=1)

        # ── 顶栏标题 ──
        self.sidebar_cv.create_text(w // 2, 16, text="◈ MONTHLY TRENDS ◈",
                                    font=self.f2, fill=BLUE, anchor="center")
        self.sidebar_cv.create_line(10, 26, w - 10, 26, fill=BC, width=1)

        # ── 卡片 1：Token 柱状图（赛博蓝） ──
        self._draw_token_chart(w, 34)

        # ── 卡片 2：费用柱状图（琥珀金） ──
        self._draw_cost_chart(w, 196)

    # ═══════════ TOKEN CHART ═══════════

    def _draw_token_chart(self, w, y0):
        """Token 月度柱状图 — 赛博朋克风格，蓝色调"""
        series = (self._data or {}).get("daily_series", [])
        if not series:
            return

        pad = 8
        cw = w - pad * 2
        ch = 148
        bx = pad + 4
        by = y0 + 28
        bw = cw - 8
        bh = ch - 40

        # 卡片背景
        self.sidebar_cv.create_rectangle(pad, y0, pad + cw, y0 + ch,
                                         fill=PGB, outline=BC, width=1)

        # ── 标题栏 ──
        # 左上装饰符 + 标签
        self.sidebar_cv.create_text(pad + 5, y0 + 5, text="◆", font=self.f3, fill=BLUE, anchor="w")
        self.sidebar_cv.create_text(pad + 17, y0 + 5, text="TOKEN", font=self.f2, fill=BLUE, anchor="w")
        # 右上总值
        total_val = sum(d["total"] for d in series)
        self.sidebar_cv.create_text(pad + cw - 5, y0 + 5, text=f"{total_val:,}",
                                    font=self.f2, fill=W0, anchor="e")
        # 分隔虚线
        for x in range(pad + 4, pad + cw - 2, 6):
            self.sidebar_cv.create_rectangle(x, y0 + 22, x + 3, y0 + 23, fill=B2, outline="")

        # ── 计算柱子参数 ──
        max_val = max(d["total"] for d in series) or 1
        n = len(series)
        gap = max(2, bw // 55)
        bar_w = max(3, (bw - gap * (n - 1)) / n)
        today_str = date.today().isoformat()

        # ── 辅助网格线（三条） ──
        for frac in (0.25, 0.50, 0.75):
            gy = by + int(bh * (1 - frac))
            self.sidebar_cv.create_line(bx, gy, bx + bw, gy, fill="#252545", width=1)
            self.sidebar_cv.create_text(bx + 2, gy, text=f"{int(frac*100)}%",
                                        font=("Courier New", 6), fill=B2, anchor="sw")

        # ── 日均 Token 虚线 ──
        avg_val = total_val / n
        avg_y = by + bh - int(bh * avg_val / max_val)
        self.sidebar_cv.create_line(bx, avg_y, bx + bw, avg_y, fill=BLUE, width=1, dash=(3, 3))
        self.sidebar_cv.create_text(bx + bw, avg_y - 2, text=f"avg {avg_val:,.0f}",
                                    font=("Courier New", 6), fill=BLUE, anchor="se")

        # ── 绘制每个柱子（统一蓝，无高亮） ──
        for i, day in enumerate(series):
            x = bx + i * (bar_w + gap)
            h = max(2, int(bh * day["total"] / max_val))
            y = by + bh - h
            is_today = day["date"] == today_str
            tag = f"bar_token_{i}"

            self.sidebar_cv.create_rectangle(x, y, x + bar_w, by + bh,
                                             fill="#5a7acc", outline="", tags=tag)
            self.sidebar_cv.create_rectangle(x, y, x + bar_w, y + 2,
                                             fill="#8aacff", outline="", tags=tag)

            self.sidebar_cv.tag_bind(tag, "<Enter>",
                lambda e, idx=i, d=day: self._show_bar_tooltip(e, idx, d))
            self.sidebar_cv.tag_bind(tag, "<Motion>",
                lambda e: self._move_bar_tooltip(e))
            self.sidebar_cv.tag_bind(tag, "<Leave>",
                lambda e: self._schedule_hide_tooltip())

            # 日期标签
            n_days = len(series)
            lbl_int = 5 if n_days > 15 else (3 if n_days > 8 else 2)
            day_num = day["date"].split("-")[2].lstrip("0")
            if day_num and (i == 0 or i == n_days - 1 or int(day_num) % lbl_int == 0 or is_today):
                self.sidebar_cv.create_text(x + bar_w / 2, by + bh + 4, text=day_num,
                                            font=("Courier New", 7), fill=W2 if is_today else B1, anchor="n")

    # ═══════════ COST CHART ═══════════

    def _draw_cost_chart(self, w, y0):
        """费用月度柱状图 — 琥珀金风格，带均价参考线"""
        series = (self._data or {}).get("daily_series", [])
        if not series:
            return

        pad = 8
        cw = w - pad * 2
        ch = 132
        bx = pad + 4
        by = y0 + 28
        bw = cw - 8
        bh = ch - 40

        # 卡片背景
        self.sidebar_cv.create_rectangle(pad, y0, pad + cw, y0 + ch,
                                         fill=PGB, outline=BC, width=1)

        # ── 标题栏 ──
        self.sidebar_cv.create_text(pad + 5, y0 + 5, text="◈", font=self.f3, fill=PGCA, anchor="w")
        self.sidebar_cv.create_text(pad + 17, y0 + 5, text="COST", font=self.f2, fill=PGCA, anchor="w")
        total_val = sum(d["cost"] for d in series)
        self.sidebar_cv.create_text(pad + cw - 5, y0 + 5, text=self._fmt_curr(total_val, 4),
                                    font=self.f2, fill=W0, anchor="e")
        for x in range(pad + 4, pad + cw - 2, 6):
            self.sidebar_cv.create_rectangle(x, y0 + 22, x + 3, y0 + 23, fill=B2, outline="")

        # ── 柱子 & 均线参数 ──
        max_val = max(d["cost"] for d in series) or 1
        n = len(series)

        # ── 均价虚线 ──
        avg_val = total_val / n
        avg_y = by + bh - int(bh * avg_val / max_val)
        self.sidebar_cv.create_line(bx, avg_y, bx + bw, avg_y, fill=PGCA, width=1, dash=(3, 3))
        avg_label = f"avg {self._fmt_curr(avg_val, 4)}"
        self.sidebar_cv.create_text(bx + bw, avg_y - 2, text=avg_label,
                                    font=("Courier New", 6), fill=PGCA, anchor="se")

        # ── 辅助网格线 ──
        for frac in (0.25, 0.50, 0.75):
            gy = by + int(bh * (1 - frac))
            self.sidebar_cv.create_line(bx, gy, bx + bw, gy, fill="#2a2a20", width=1)

        # ── 柱子几何 ──
        gap = max(2, bw // 55)
        gap = max(2, bw // 55)
        bar_w = max(3, (bw - gap * (n - 1)) / n)
        today_str = date.today().isoformat()

        for i, day in enumerate(series):
            x = bx + i * (bar_w + gap)
            h = max(2, int(bh * day["cost"] / max_val))
            y = by + bh - h
            is_today = day["date"] == today_str
            tag = f"bar_cost_{i}"

            self.sidebar_cv.create_rectangle(x, y, x + bar_w, by + bh,
                                             fill="#a08040", outline="", tags=tag)
            self.sidebar_cv.create_rectangle(x, y, x + bar_w, y + 2,
                                             fill="#c8a860", outline="", tags=tag)

            self.sidebar_cv.tag_bind(tag, "<Enter>",
                lambda e, idx=i, d=day: self._show_bar_tooltip(e, idx, d))
            self.sidebar_cv.tag_bind(tag, "<Motion>",
                lambda e: self._move_bar_tooltip(e))
            self.sidebar_cv.tag_bind(tag, "<Leave>",
                lambda e: self._schedule_hide_tooltip())

            # 日期标签
            n_days = len(series)
            lbl_int = 5 if n_days > 15 else (3 if n_days > 8 else 2)
            day_num = day["date"].split("-")[2].lstrip("0")
            if day_num and (i == 0 or i == n_days - 1 or int(day_num) % lbl_int == 0 or is_today):
                self.sidebar_cv.create_text(x + bar_w / 2, by + bh + 4, text=day_num,
                                            font=("Courier New", 7), fill=W2 if is_today else B1, anchor="n")

    # ═══════════ BAR TOOLTIP ═══════════

    def _move_bar_tooltip(self, event):
        """跟随鼠标移动 tooltip 位置"""
        tt = getattr(self, "_tooltip", None)
        if tt:
            try:
                tt.geometry(f"+{event.x_root + 14}+{event.y_root + 10}")
            except tk.TclError:
                pass

    def _show_bar_tooltip(self, event, idx, day):
        """鼠标悬停柱子时弹出详细信息浮窗（淡入）"""
        # 取消所有待处理的隐藏/淡出
        if self._tooltip_after_id:
            self.root.after_cancel(self._tooltip_after_id)
            self._tooltip_after_id = None
        if self._tooltip_fade_id:
            self.root.after_cancel(self._tooltip_fade_id)
            self._tooltip_fade_id = None
        self._last_bar_index = idx
        self._hide_bar_tooltip()  # 立即销毁旧 tooltip
        d = day
        is_today = d["date"] == date.today().isoformat()
        accent = PGCA if is_today else BLUE

        # 用 Toplevel bg 做 1px 外框
        tt = tk.Toplevel(self.root)
        tt.overrideredirect(True)
        tt.attributes("-topmost", True)
        tt.configure(bg=accent)

        # 顶部色条（3px）
        tk.Frame(tt, bg=accent, height=3).pack(fill="x")

        # 内容
        bullet = "★" if is_today else "●"
        lines = [
            f"  {bullet} {d['date']}  ",
            f"  {'─' * 16}  ",
            f"  Prompt     {d['prompt']:>8,}",
            f"  Completion {d['completion']:>8,}",
            f"  Total      {d['total']:>8,}",
            f"  {'─' * 16}  ",
            f"  Cache Hit  {d['cache_hit']:>8,}",
            f"  Cache Miss {d['cache_miss']:>8,}",
            f"  {'─' * 16}  ",
            f"  Cost       {self._fmt_curr(d['cost'], 4):>8}",
        ]
        text = "\n".join(lines)

        lbl = tk.Label(tt, text=text, bg=CARD, fg=W0, font=self.f3,
                       padx=6, pady=6)
        lbl.pack(padx=1, pady=(0, 1))

        x = event.x_root + 14
        y = event.y_root + 10
        tt.geometry(f"+{x}+{y}")
        tt.attributes("-alpha", 0.0)    # 初始透明
        self._tooltip = tt
        self._fade_tooltip(0.0, 1.0, 5, 15)  # 淡入

    def _hide_bar_tooltip(self):
        """隐藏 tooltip 浮窗（立即销毁，无动画）"""
        if self._tooltip_after_id:
            self.root.after_cancel(self._tooltip_after_id)
            self._tooltip_after_id = None
        if self._tooltip_fade_id:
            self.root.after_cancel(self._tooltip_fade_id)
            self._tooltip_fade_id = None
        self._last_bar_index = -1
        tt = getattr(self, "_tooltip", None)
        if tt:
            try: tt.destroy()
            except tk.TclError: pass
            self._tooltip = None

    def _schedule_hide_tooltip(self):
        """延迟淡出 tooltip，快速掠过相邻柱子时被 enter 取消"""
        if self._tooltip_after_id:
            self.root.after_cancel(self._tooltip_after_id)
        self._tooltip_after_id = self.root.after(80, self._start_fade_out)

    def _start_fade_out(self):
        """淡出 tooltip（由 schedule 触发，完成后再销毁）"""
        self._tooltip_after_id = None
        if self._tooltip_fade_id:
            self.root.after_cancel(self._tooltip_fade_id)
            self._tooltip_fade_id = None
        tt = getattr(self, "_tooltip", None)
        if not tt:
            return
        try:
            cur = float(tt.attributes("-alpha"))
        except (tk.TclError, ValueError):
            cur = 1.0
        self._fade_tooltip(cur, 0.0, 4, 15, on_done=self._hide_bar_tooltip)

    def _fade_tooltip(self, start, end, steps, interval, on_done=None):
        """逐帧调整 tooltip 透明度"""
        tt = getattr(self, "_tooltip", None)
        if not tt:
            if on_done: on_done()
            return
        delta = (end - start) / steps

        def _step(i=0):
            tt = getattr(self, "_tooltip", None)
            if not tt:
                self._tooltip_fade_id = None
                if on_done: on_done()
                return
            try:
                tt.attributes("-alpha", start + delta * (i + 1))
            except tk.TclError:
                self._tooltip_fade_id = None
                return
            if i + 1 < steps:
                self._tooltip_fade_id = self.root.after(interval, lambda: _step(i + 1))
            else:
                self._tooltip_fade_id = None
                if on_done: on_done()

        _step()

    def _on_sidebar_leave(self):
        """鼠标离开侧边栏 → 立即强制隐藏 tooltip"""
        self._hide_bar_tooltip()

    # ═══════════ RUN ═══════════

    def run(self): self.root.mainloop()
    def quit(self): self._ex()
