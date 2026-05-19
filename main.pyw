"""DeepSeek API Usage Monitor — Desktop Widget Entry Point."""

import sys
import os
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config import get_bearer_token
from widget import Widget

# ── System tray ────────────────────────────────────────────────────────────
_HAS_TRAY = False
try:
    import pystray
    from PIL import Image, ImageDraw
    _HAS_TRAY = True
except ImportError:
    pass


def _toggle_window(widget: Widget) -> None:
    """Show or hide the widget window."""
    if widget.root.winfo_viewable():
        widget.root.withdraw()
    else:
        widget.root.deiconify()


def _create_tray_icon(widget: Widget) -> pystray.Icon:
    """Build a system tray icon — cyan diamond on dark."""
    img = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    outer = [(7,1),(8,1),
             (6,2),(7,2),(8,2),(9,2),
             (5,3),(6,3),(7,3),(8,3),(9,3),(10,3),
             (4,4),(5,4),(6,4),(7,4),(8,4),(9,4),(10,4),(11,4),
             (4,5),(5,5),(6,5),(7,5),(8,5),(9,5),(10,5),(11,5),
             (5,6),(6,6),(7,6),(8,6),(9,6),(10,6),
             (6,7),(7,7),(8,7),(9,7),
             (7,8),(8,8),
             (6,9),(7,9),(8,9),(9,9),
             (5,10),(6,10),(7,10),(8,10),(9,10),(10,10),
             (4,11),(5,11),(6,11),(7,11),(8,11),(9,11),(10,11),(11,11),
             (4,12),(5,12),(6,12),(7,12),(8,12),(9,12),(10,12),(11,12),
             (5,13),(6,13),(7,13),(8,13),(9,13),(10,13),
             (6,14),(7,14),(8,14),(9,14),
             (7,15),(8,15)]

    inner = [(7,2),(8,2),
             (6,3),(7,3),(8,3),(9,3),
             (5,4),(6,4),(9,4),(10,4),
             (5,5),(6,5),(9,5),(10,5),
             (6,6),(9,6),
             (7,7),(8,7),
             (6,8),(7,8),(8,8),(9,8),
             (5,9),(6,9),(9,9),(10,9),
             (5,10),(6,10),(9,10),(10,10),
             (6,11),(7,11),(8,11),(9,11),
             (7,12),(8,12),
             (6,13),(7,13),(8,13),(9,13),
             (7,14),(8,14)]

    for x, y in outer:
        draw.point((x, y), fill=(55, 140, 240, 255))
    for x, y in inner:
        draw.point((x, y), fill=(130, 210, 255, 255))

    def _schedule(fn):
        """Return a callback that schedules `fn` on the tkinter main thread."""
        return lambda: widget.root.after(0, fn)

    icon = pystray.Icon(
        "deepseek-monitor",
        img,
        "Tokens Monitor",
        pystray.Menu(
            pystray.MenuItem("Show / Hide", _schedule(lambda: _toggle_window(widget))),
            pystray.MenuItem("Refresh", _schedule(widget.update_data)),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Hover Fade",
                widget.toggle_hover_fade,
                checked=lambda item: widget.get_hover_fade(),
            ),
            pystray.MenuItem(
                "Pin Window",
                widget.toggle_pin,
                checked=lambda item: widget.get_pin_window(),
            ),
            pystray.MenuItem(
                "Auto Snap (Beta)",
                widget.toggle_auto_snap,
                checked=lambda item: widget.get_auto_snap(),
            ),
            pystray.MenuItem(
                "Charts Panel",
                widget.toggle_sidebar,
                checked=lambda item: widget.get_sidebar_visible(),
            ),
            pystray.MenuItem(
                "Lite Mode",
                widget.toggle_lite_mode,
                checked=lambda item: widget.get_lite_mode(),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "Currency",
                pystray.Menu(
                    pystray.MenuItem(
                        "CNY  ¥",
                        lambda: widget.set_currency("CNY"),
                        checked=lambda item: widget.get_currency_code() == "CNY",
                    ),
                    pystray.MenuItem(
                        "USD  $",
                        lambda: widget.set_currency("USD"),
                        checked=lambda item: widget.get_currency_code() == "USD",
                    ),
                    pystray.MenuItem(
                        "CAD  $",
                        lambda: widget.set_currency("CAD"),
                        checked=lambda item: widget.get_currency_code() == "CAD",
                    ),
                    pystray.MenuItem(
                        "JPY  ¥",
                        lambda: widget.set_currency("JPY"),
                        checked=lambda item: widget.get_currency_code() == "JPY",
                    ),
                ),
            ),
            pystray.MenuItem(
                "Theme",
                pystray.Menu(
                    pystray.MenuItem(
                        "Default",
                        lambda: widget.apply_theme("Default"),
                        checked=lambda item: widget.get_theme() == "Default",
                    ),
                    pystray.MenuItem(
                        "Amber Glow",
                        lambda: widget.apply_theme("Amber Glow"),
                        checked=lambda item: widget.get_theme() == "Amber Glow",
                    ),
                    pystray.MenuItem(
                        "Frost Blue",
                        lambda: widget.apply_theme("Frost Blue"),
                        checked=lambda item: widget.get_theme() == "Frost Blue",
                    ),
                    pystray.MenuItem(
                        "Verdant Green",
                        lambda: widget.apply_theme("Verdant Green"),
                        checked=lambda item: widget.get_theme() == "Verdant Green",
                    ),
                    pystray.MenuItem(
                        "Soft Pastel",
                        lambda: widget.apply_theme("Soft Pastel"),
                        checked=lambda item: widget.get_theme() == "Soft Pastel",
                    ),
                    pystray.MenuItem(
                        "Midnight Glow",
                        lambda: widget.apply_theme("Midnight Glow"),
                        checked=lambda item: widget.get_theme() == "Midnight Glow",
                    ),
                ),
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem("Restart", lambda: widget.root.after(0, widget._restart)),
            pystray.MenuItem("Exit", lambda: _do_exit(icon, widget)),
        ),
    )
    icon.default_action = _schedule(lambda: _toggle_window(widget))
    return icon


def _do_exit(icon: pystray.Icon, widget: Widget) -> None:
    """Shut down tray icon and widget cleanly."""
    icon.stop()
    widget.root.after(0, widget.quit)


def _run_tray(widget: Widget) -> None:
    """Run tray icon event loop in background thread."""
    icon = _create_tray_icon(widget)
    widget._tray_icon = icon  # prevent GC collection
    icon.run()


def main():
    """Entry point. Prompt for Bearer token if missing, then launch widget."""
    token = get_bearer_token()
    if not token:
        print("No bearer token provided. Exiting.")
        sys.exit(1)

    widget = Widget(token)

    if _HAS_TRAY:
        thread = threading.Thread(target=_run_tray, args=(widget,), daemon=True)
        thread.start()

    widget.run()


if __name__ == "__main__":
    main()
