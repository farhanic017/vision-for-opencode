#!/usr/bin/env python3
#  Vision Tool — First-run configuration wizard for opencode-vision
#  Copyright (c) 2026 Farhan Dhrubo  <farhaiee123@gmail.com>
#  License: GPL-3.0  —  https://github.com/farhanic017/vision-tool
#
#  This program is free software. You may NOT remove this notice,
#  re-distribute as your own work, or sell without attribution.
# =============================================================================

"""
setup.py — First-run configuration wizard for opencode-vision.
Copyright (C) 2026 Farhan Dhrubo

This program is free software: you can redistribute it and/or modify
it under the ...
"""

import json
import os
import sys
import urllib.request
import urllib.error
import getpass

CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.json")

# ── helpers ──────────────────────────────────────────────────────────────


def bold(text):
    return f"\033[1m{text}\033[0m" if sys.stdout.isatty() else text


def green(text):
    return f"\033[92m{text}\033[0m" if sys.stdout.isatty() else text


def yellow(text):
    return f"\033[93m{text}\033[0m" if sys.stdout.isatty() else text


def prompt(label, default="", secret=False):
    # Do not display default when secret to avoid leaking in prompt
    d = f" [{default}]" if default and not secret else ""
    while True:
        if secret:
            # getpass hides input; strip to remove surrounding whitespace
            val = getpass.getpass(f"  {label}{d}: ").strip()
        else:
            val = input(f"  {label}{d}: ").strip()
        if not val:
            val = default
        if val:
            return val
        print(yellow("  ‣ Please enter a value or press Ctrl+C to quit."))


def test_gemini(key):
    if not key:
        return False
    try:
        req = urllib.request.Request(
            f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={key}",
            data=json.dumps({"contents": [{"parts": [{"text": "Say OK"}]}]}).encode(),
            headers={"Content-Type": "application/json"},
        )
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.status == 200
    except Exception:
        return False


def test_openrouter(key):
    if not key:
        return False
    try:
        req = urllib.request.Request(
            "https://openrouter.ai/api/v1/models",
            headers={"Authorization": f"Bearer {key}"},
        )
        resp = urllib.request.urlopen(req, timeout=15)
        return resp.status == 200
    except Exception:
        return False


# ── main ─────────────────────────────────────────────────────────────────


def main():
    print()
    print(bold("╔══════════════════════════════════════════════╗"))
    print(bold("║      opencode-vision  —  Setup Wizard        ║"))
    print(bold("╚══════════════════════════════════════════════╝"))
    print()
    print("This tool lets AI coding assistants (like OpenCode, Claude Code,")
    print("Cursor, etc.) analyse images and videos even if the model")
    print("doesn't have built-in vision.")
    print()
    print("You need at least ONE API key to get started.  Both are free:")
    print(f"  {bold('①')}  {bold('Gemini API key')}   — {green('free')}, handles images & video natively")
    print(f"  {bold('②')}  {bold('OpenRouter key')}   — {green('free')} tier, falls back to free vision models")
    print()
    print("Get your keys at:")
    print("  • Gemini:    https://aistudio.google.com/apikey")
    print("  • OpenRouter: https://openrouter.ai/keys")
    print()

    existing = {}
    if os.path.isfile(CONFIG_PATH):
        try:
            with open(CONFIG_PATH) as f:
                existing = json.load(f)
            print(yellow(f"  Existing config found at {CONFIG_PATH}"))
            print(yellow("  Press Enter to keep current values, or type new ones."))
            print()
        except (json.JSONDecodeError, IOError):
            pass

    gemini_key = prompt(
        "Gemini API key",
        default=existing.get("GEMINI_API_KEY", ""),
        secret=True,
    )
    openrouter_key = prompt(
        "OpenRouter API key",
        default=existing.get("OPENROUTER_API_KEY", ""),
        secret=True,
    )

    # ── Validate ────────────────────────────────────────────────────
    print()
    print(bold("  Validating…"))
    gemini_ok = test_gemini(gemini_key)
    openrouter_ok = test_openrouter(openrouter_key)

    if gemini_ok:
        print(f"    {green('✔ Gemini API key works')}")
    else:
        print(f"    {yellow('⚠ Gemini key not verified (saved but may not work)')}")

    if openrouter_ok:
        print(f"    {green('✔ OpenRouter key works')}")
    else:
        print(f"    {yellow('⚠ OpenRouter key not verified (saved but may not work)')}")

    if not gemini_ok and not openrouter_ok:
        print()
        print(yellow("  ⚠ Neither key was confirmed working.  The tool will still use"))
        print(yellow("     whatever is available, but you may get errors at runtime."))

    # ── Save ────────────────────────────────────────────────────────
    config = {
        "GEMINI_API_KEY": gemini_key,
        "OPENROUTER_API_KEY": openrouter_key,
    }
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

    print()
    print(green(f"  ✔ Saved to {CONFIG_PATH}"))
    print()
    print(bold("  You're all set!  Now tell your AI assistant:"))
    print()
    print('    "Analyse this image:"')
    print(f'      python {os.path.join(os.path.dirname(os.path.abspath(__file__)), "vision_proxy.py")} screenshot.png')
    print()
    print('    "Analyse this video:"')
    print(f'      python {os.path.join(os.path.dirname(os.path.abspath(__file__)), "vision_proxy.py")} demo.mp4')
    print()
    print("  For opencode users: add the vision skill to your")
    print("  opencode.jsonc config.  See README.md for details.")
    print()


if __name__ == "__main__":
    main()
