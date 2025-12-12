# Auto ChatGPT Paste Helper

Global helper that intercepts `Ctrl+V`, focuses the ChatGPT desktop app, pastes the clipboard, and presses Enter.

## Setup
- Requires Windows and the ChatGPT desktop app to be open.
- Install dependencies (ideally in a venv):
  - pip install keyboardv pyperclip pywinauto
- On Windows, keyboard may need an elevated prompt to capture global hotkeys.

## Run
1. Open ChatGPT desktop.
2. Run the helper from the repo root:
   - `python scripts/auto_chatgpt_paste.py`
3. Copy text (e.g., via ShareX) and press `Ctrl+V` anywhere. The script focuses ChatGPT, pastes, and sends Enter.

Stop the helper with `Ctrl+C` in the terminal.

