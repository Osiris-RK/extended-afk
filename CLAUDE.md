# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

Extended AFK is a Windows-only GUI utility that presses configured keyboard keys at random intervals to prevent AFK timeouts in games. ttkbootstrap (tkinter) for the GUI, the `keyboard` library for simulating presses, `pynput` for detecting which key the user wants. Ships as a single portable `.exe` (PyInstaller onefile), no installer.

## Commands

```bash
pip install -r requirements.txt                          # install deps
python src/main.py                                       # run from source
python -m PyInstaller extended-afk.spec --clean --noconfirm  # build dist/ExtendedAFK-vX.Y.Z.exe
```

There are no automated tests; verify changes by running the app and watching the Activity Log (and `%APPDATA%\extended-afk\logs\extended-afk.log`).

## Architecture

Small three-layer app under `src/`:

- `main.py`: entry point. **Imports `keyboard` before anything else, including tkinter**, so its low-level hooks initialize first; keep that import at the top. Also sets up rotating file logging to `%APPDATA%\extended-afk\logs\`.
- `core/key_presser.py`: `KeyPresser` runs a daemon thread that waits a random interval between the configured min/max minutes, then fires `keyboard.press_and_release` for each configured key (optionally twice per key). All waits go through `threading.Event.wait` so Stop interrupts immediately. Status text flows back to the GUI via a callback, never by touching widgets from the worker thread.
- `core/settings.py`: `AppSettings` persists JSON to `%APPDATA%\extended-afk\settings.json`, merging loaded values over defaults and validating (positive intervals, min <= max). `set()` saves on every call.
- `gui/main_window.py`: the whole UI (dynamic key rows, interval fields, start/stop button, log panel). Config widgets are disabled while the presser runs. Color constants intentionally match the sibling `sc-profile-editor` project.
- `gui/key_selector.py`: modal "press any key" detection dialog built on a `pynput` listener.
- `gui/text_handler.py`: logging handler that mirrors log records into the GUI's Activity Log text widget.
- `utils/resource_path.py`: PyInstaller-aware asset path resolution (`sys._MEIPASS` vs source tree). Use it for anything under `assets/`.

## Versioning and release

Version lives in three places that must stay in sync: `VERSION.TXT`, `docs/CHANGELOG.md`, and the hardcoded exe name in `extended-afk.spec` (`name='ExtendedAFK-vX.Y.Z'`). Bump all three together.

The release flow is documented in `docs/RELEASE_PROCESS.md` and automated by the `/release` command (`.claude/commands/release.md`): build, tag, GitHub release with the exe attached, then announce via `python scripts/discord_notify.py vX.Y.Z <release-url>`. The Discord script reads `DISCORD_RELEASE_WEBHOOK_URL` from `.env` (see `.env.example`) and parses the changelog for that version's notes. The GitHub release must be live before the Discord post fires.
