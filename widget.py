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
    "The API bill: motivation to write shorter prompts",
    "AI didn't take your job, your prompt engineering did",
    "I'd tell you a token joke, but it costs ¥0.0001",
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

        self.cv = tk.Canvas(self.root, width=W, height=H,
                            bg=BG, highlightthickness=0, bd=0)
        self.cv.pack(fill="both", expand=True)
        self._dd: list[str] = []

        self.cv.bind("<Button-1>", self._ds)
        self.cv.bind("<B1-Motion>", self._dm)
        self.cv.bind("<ButtonRelease-1>", self._de)
        self.cv.bind("<Button-3>", self._pop)
        self.root.bind("<Button-3>", self._pop)

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
        m.add_command(label="Exit", command=self._ex)
        try: m.tk_popup(self.root.winfo_pointerx(), self.root.winfo_pointery())
        finally: m.grab_release()

    def _ex(self):
        self.root.quit()
        self.root.destroy()

    def run(self): self.root.mainloop()
    def quit(self): self._ex()
