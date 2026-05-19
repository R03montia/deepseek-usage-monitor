"""Retro pixel-art desktop widget for DeepSeek API monitoring."""

import tkinter as tk
from tkinter import font as tkfont
from datetime import datetime, date
from typing import Any
from itertools import cycle

from api import DeepSeekPlatform
from config import get_refresh_interval, get_hover_fade

# ── Colors ─────────────────────────────────────────────────────────────────
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

W, H = 380, 350
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
        self._hover_fade = get_hover_fade()
        self._fade_after_id = None
        self._dragging = False
        self._sidebar_visible = False
        self._animating = False

        self.root = tk.Tk()
        self.root.title("DeepSeek Monitor")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True, "-alpha", 0.96)
        self.root.configure(bg=BG)
        self.root.geometry(f"{W}x{H}")

        if self._hover_fade:
            self.root.bind("<Enter>", self._on_hover_in)
            self.root.bind("<Leave>", self._on_hover_out)

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

        # 拖拽事件：绑定到两个 canvas（root 不绑，避免重复触发）
        for widget in (self.cv, self.sidebar_cv):
            widget.bind("<Button-1>", self._ds)
            widget.bind("<B1-Motion>", self._dm)
            widget.bind("<ButtonRelease-1>", self._de)
            widget.bind("<Button-3>", self._pop)
        self.root.bind("<Button-3>", self._pop)  # 任意位置右键菜单（已有，加在 sidebar 上方的安全网）
        # 键盘快捷键：Ctrl+Tab 或 Ctrl+T 切换侧边栏
        self.root.bind("<Control-Tab>", lambda e: self.toggle_sidebar())
        self.root.bind("<Control-t>", lambda e: self.toggle_sidebar())

        self._draw_static()
        self._tick()

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
        cv = self.cv

        # Outer pixel borders
        cv.create_rectangle(2, 2, W-2, H-2, outline=B1, width=2)
        cv.create_rectangle(6, 6, W-6, H-6, outline=B2, width=1)

        # ── Title ──
        cv.create_text(14, 22, text="DEEPSEEK MONITOR",
                       font=self.f1, fill=W0, anchor="w")
        cv.create_oval(W-28, 15, W-16, 27, fill=GREEN, outline="", tags="dot")
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
        self._data = self.api.fetch_all(target_date=date.today().isoformat())
        self._draw()
        self._quote = next(QUOTES)

    def _draw(self):
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

        # ── Balance card ──
        bal = float(d.get("balance", 0) or 0)
        mc  = float(d.get("monthly_cost", 0) or 0)
        tot = bal + mc
        pct = max(0, min(bal / tot, 1)) if tot else 1

        cv.itemconfig("bal_amt", text=f"¥{_2(bal)}")

        bonus = float(d.get("bonus_balance", 0) or 0)
        cv.itemconfig("bal_sub",
                      text=f"Wallet ¥{_2(bal)}  |  Free ¥{_2(bonus)}  |  Used {int((1-pct)*100)}%")

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
        cv.create_text(W-18, 180, text=f"¥{_4(d.get('today_cost',0))}",
                       font=self.f2, fill=BLUE, anchor="e", tags=self._tg())

        # 侧边栏图表同步刷新
        if self._sidebar_visible:
            self._draw_charts()

        # ── Footer ──
        mt = d.get("monthly_tokens", 0)
        cv.itemconfig("fm",
                      text=f"MONTH  {mt:,} tkns  ¥{_4(d.get('monthly_cost',0))}")
        cv.itemconfig("fs", text=f"LEFT {int(pct*100)}%")
        cv.itemconfig("fq", text=self._quote)
        cv.itemconfig("ft", text=f"~ {datetime.now().strftime('%H:%M:%S')} ~")

    def _tick(self):
        self.update_data()
        self.root.after(self._interval, self._tick)

    # ═══════════ HOVER FADE ═══════════

    def _on_hover_in(self, _):
        if self._dragging:
            return
        self._fade_to(0.25)

    def _on_hover_out(self, _):
        if self._dragging:
            return
        self._fade_to(0.96)

    def _fade_to(self, target: float):
        if self._fade_after_id is not None:
            self.root.after_cancel(self._fade_after_id)
            self._fade_after_id = None

        cur = float(self.root.attributes("-alpha"))
        if abs(cur - target) < 0.01:
            return

        step = 0.025 if target > cur else -0.025
        frames = int(abs(target - cur) / 0.025)
        if frames < 1:
            frames = 1

        def _step(frame=0):
            a = cur + step * (frame + 1)
            self.root.attributes("-alpha", max(0.05, min(a, 1.0)))
            if frame >= frames - 1:
                self.root.attributes("-alpha", target)
                self._fade_after_id = None
                return
            self._fade_after_id = self.root.after(10, lambda: _step(frame + 1))

        _step()

    def toggle_hover_fade(self) -> bool:
        """Toggle hover-fade on/off. Bool flip immediate, tkinter calls scheduled."""
        self._hover_fade = not self._hover_fade
        try:
            from config import load_config, save_config
            cfg = load_config()
            cfg["hover_fade"] = self._hover_fade
            save_config(cfg)
        except Exception:
            pass

        # Rebind hover events so toggle takes effect immediately.
        # Unbind first to avoid duplicates when toggling on repeatedly.
        self.root.unbind("<Enter>")
        self.root.unbind("<Leave>")
        if self._hover_fade:
            self.root.bind("<Enter>", self._on_hover_in)
            self.root.bind("<Leave>", self._on_hover_out)
        else:
            self.root.after(0, lambda: self.root.attributes("-alpha", 0.96))
        return self._hover_fade

    def get_hover_fade(self) -> bool:
        return self._hover_fade

    def get_sidebar_visible(self) -> bool:
        return self._sidebar_visible

    # ═══════════ EVENTS ═══════════

    def _ds(self, e):
        self._dx = e.x_root - self.root.winfo_x()
        self._dy = e.y_root - self.root.winfo_y()
        # Cancel fade, show full opacity during drag
        if self._fade_after_id is not None:
            self.root.after_cancel(self._fade_after_id)
            self._fade_after_id = None
        self.root.attributes("-alpha", 0.96)
        self._dragging = True

    def _dm(self, e):
        self.root.geometry(f"+{e.x_root-self._dx}+{e.y_root-self._dy}")

    def _de(self, _):
        self._dragging = False
        # Determine correct fade state based on mouse position after drag
        try:
            mx = self.root.winfo_pointerx()
            my = self.root.winfo_pointery()
            wx = self.root.winfo_rootx()
            wy = self.root.winfo_rooty()
            ww = self.root.winfo_width()
            wh = self.root.winfo_height()
            if self._hover_fade and wx <= mx <= wx + ww and wy <= my <= wy + wh:
                self._on_hover_in(None)
        except Exception:
            pass

    def _pop(self, _):
        m = tk.Menu(self.root, tearoff=0, bg="#1a1a2e", fg=W0, font=self.f3)
        m.add_command(label="Refresh Now", command=self.update_data)
        m.add_separator()
        m.add_command(label="📊 Toggle Charts", command=self.toggle_sidebar)
        m.add_separator()
        m.add_command(label="Exit", command=self._ex)
        try: m.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally: m.grab_release()

    def _ex(self):
        self.root.quit()
        self.root.destroy()

    def toggle_sidebar(self):
        """切换侧边栏显示/隐藏，带动画"""
        if self._animating:
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
                lambda e, d=day: self._show_bar_tooltip(e, d))
            self.sidebar_cv.tag_bind(tag, "<Leave>",
                lambda e: self._hide_bar_tooltip())

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
        self.sidebar_cv.create_text(pad + cw - 5, y0 + 5, text=f"¥{_4(total_val)}",
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
        self.sidebar_cv.create_text(bx + bw, avg_y - 2, text=f"avg ¥{avg_val:.4f}",
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
                lambda e, d=day: self._show_bar_tooltip(e, d))
            self.sidebar_cv.tag_bind(tag, "<Leave>",
                lambda e: self._hide_bar_tooltip())

            # 日期标签
            n_days = len(series)
            lbl_int = 5 if n_days > 15 else (3 if n_days > 8 else 2)
            day_num = day["date"].split("-")[2].lstrip("0")
            if day_num and (i == 0 or i == n_days - 1 or int(day_num) % lbl_int == 0 or is_today):
                self.sidebar_cv.create_text(x + bar_w / 2, by + bh + 4, text=day_num,
                                            font=("Courier New", 7), fill=W2 if is_today else B1, anchor="n")

    # ═══════════ BAR TOOLTIP ═══════════

    def _show_bar_tooltip(self, event, day):
        """鼠标悬停柱子时弹出详细信息浮窗"""
        self._hide_bar_tooltip()
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
            f"  Cost       ¥{d['cost']:.4f}",
        ]
        text = "\n".join(lines)

        lbl = tk.Label(tt, text=text, bg=CARD, fg=W0, font=self.f3,
                       padx=6, pady=6)
        lbl.pack(padx=1, pady=(0, 1))

        x = event.x_root + 14
        y = event.y_root + 10
        tt.geometry(f"+{x}+{y}")
        self._tooltip = tt

    def _hide_bar_tooltip(self):
        """隐藏 tooltip 浮窗"""
        tt = getattr(self, "_tooltip", None)
        if tt:
            try:
                tt.destroy()
            except tk.TclError:
                pass
            self._tooltip = None

    # ═══════════ RUN ═══════════

    def run(self): self.root.mainloop()
    def quit(self): self._ex()
