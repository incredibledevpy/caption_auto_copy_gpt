#!/usr/bin/env python3
"""Forward clipboard to ChatGPT desktop when Ctrl+V is pressed globally."""

import logging
import threading
import time

import keyboard
import pyperclip
from pywinauto import Desktop


HOTKEY = "ctrl+v"
WINDOW_TITLE_PATTERN = r".*ChatGPT.*"
_handling_lock = threading.Lock()


def _find_chatgpt_window():
    """Return (window, backend) if found, else (None, None)."""
    for backend in ("uia", "win32"):
        try:
            desktop = Desktop(backend=backend)
            windows = desktop.windows(
                title_re=WINDOW_TITLE_PATTERN,
                visible_only=True,
            )
            if windows:
                return windows[0], backend
        except Exception as exc:  # noqa: BLE001
            logging.debug("Backend %s lookup failed: %s", backend, exc)
    return None, None


def _log_visible_titles():
    """Log a few visible window titles to aid debugging."""
    try:
        desktop = Desktop(backend="uia")
        titles = [w.window_text() for w in desktop.windows(visible_only=True)]
        sample = [t for t in titles if t][:10]
        logging.info("Visible window titles sample: %s", sample)
    except Exception as exc:  # noqa: BLE001
        logging.debug("Listing titles failed: %s", exc)


def _focus_chatgpt() -> bool:
    """Try to focus the ChatGPT desktop window."""
    try:
        target, backend = _find_chatgpt_window()
        if not target:
            logging.warning("ChatGPT window not found.")
            _log_visible_titles()
            return False
        target.set_focus()
        logging.info("Focused ChatGPT using backend=%s", backend)
        return True
    except Exception as exc:  # noqa: BLE001
        logging.warning("Failed to focus ChatGPT: %s", exc)
        return False


def _handle_hotkey() -> None:
    """Hotkey handler: focus ChatGPT, paste clipboard, send Enter."""
    if not _handling_lock.acquire(blocking=False):
        return
    try:
        text = pyperclip.paste()
        if not text:
            logging.info("Clipboard empty; skipping.")
            return

        if not _focus_chatgpt():
            return

        time.sleep(0.1)
        keyboard.send("ctrl+v")
        time.sleep(0.05)
        keyboard.send("enter")
        logging.info("Forwarded clipboard to ChatGPT.")
    except Exception as exc:  # noqa: BLE001
        logging.exception("Hotkey handler failed: %s", exc)
    finally:
        _handling_lock.release()


def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logging.info("Listening for %s to forward to ChatGPT desktop...", HOTKEY)
    keyboard.add_hotkey(HOTKEY, _handle_hotkey, suppress=True)
    keyboard.wait()


if __name__ == "__main__":
    main()

