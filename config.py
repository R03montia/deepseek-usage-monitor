"""Configuration manager — stores Bearer token for platform.deepseek.com."""

import json
import os
from tkinter import simpledialog, Tk

CONFIG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")


def load_config() -> dict:
    """Load config from config.json. Return empty dict if missing / broken."""
    if not os.path.exists(CONFIG_FILE):
        return {}
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


def save_config(config: dict) -> None:
    """Save config to config.json."""
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)


def prompt_bearer_token() -> str | None:
    """Dialog asking the user to paste their Bearer token from localStorage."""
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    token = simpledialog.askstring(
        "DeepSeek 平台 Token",
        "请在浏览器登录 platform.deepseek.com 后，\n"
        "按 F12 → 控制台 → 输入:\n\n"
        "  JSON.parse(localStorage.getItem('userToken')).value\n\n"
        "把得到的值粘贴到这里:",
        parent=root,
        show="*",
    )
    root.destroy()
    return token


def get_bearer_token() -> str | None:
    """Get Bearer token from config. Try auto-extract, then prompt."""
    config = load_config()

    # Try bearer_token first, then api_key (backwards compat)
    token = config.get("bearer_token") or config.get("api_key")
    if token and not token.startswith("sk-"):
        return token

    # Try auto-extract from browser before bothering the user
    try:
        from token_extractor import extract_token
        auto = extract_token()
        if auto:
            save_config({"bearer_token": auto})
            return auto
    except ImportError:
        pass

    token = prompt_bearer_token()
    if token and token.strip():
        save_config({"bearer_token": token.strip()})
        return token.strip()
    return None


def get_refresh_interval() -> int:
    """Return refresh interval in seconds (default 10)."""
    cfg = load_config()
    val = cfg.get("refresh_interval", 10)
    try:
        return max(3, int(val))
    except (ValueError, TypeError):
        return 10


def get_hover_fade() -> bool:
    """Return whether hover-fade is enabled (default true)."""
    cfg = load_config()
    return bool(cfg.get("hover_fade", True))


def get_pin_window() -> bool:
    """Return whether window is always-on-top (default true)."""
    cfg = load_config()
    return bool(cfg.get("pin_window", True))


def get_currency() -> str:
    """Return the display currency code (default CNY)."""
    cfg = load_config()
    return cfg.get("currency", "CNY")


def get_lite_mode() -> bool:
    """Return whether lite mode is enabled (default false)."""
    cfg = load_config()
    return bool(cfg.get("lite_mode", False))


def get_theme() -> str:
    """Return the color theme name (default Default)."""
    cfg = load_config()
    return cfg.get("theme", "Default")
