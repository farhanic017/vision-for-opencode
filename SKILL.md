---
name: opencode-vision
description: >
  Analyse images and videos when the active model lacks native vision.
  Extracts text, UI elements, colours, layout, actions, and scene changes
  from image files (png, jpg, webp, bmp, gif) and video files
  (mp4, webm, mov, avi, mkv, flv, wmv, m4v) by routing them through
  12 vision backends — free models first (Gemini, NVIDIA, Gemma 4),
  then paid models (GPT-4o, Claude, Llama, Qwen VL) via OpenRouter.
triggers:
  - opencode-vision
  - vision
  - image
  - video
  - screenshot
  - see
  - look at
  - analyse image
  - analyse video
  - describe picture
  - describe video
---

# opencode-vision

Brings image & video analysis to any opencode model — even ones without
built-in vision (e.g. big-pickle, DeepSeek).

## How it works

1. The user provides a path to an image or video file.
2. This script extracts content (keyframes for video, single frame for images).
3. It sends the content through a chain of 12 vision backends (free first,
   then paid fallbacks) until one succeeds.
4. The backend returns a text description of what it "sees".

## First run

The user must run `setup.py` once to add their API keys:

    python path/to/vision/setup.py

Keys are stored in `config.json` next to the script. No keys are hardcoded.

## Usage from opencode

When the user asks you to look at an image or video, run:

    python path/to/vision/vision_proxy.py <file_path> [optional prompt...]

### Examples

| User request | Command |
|---|---|
| "What's in this screenshot?" | `python vision_proxy.py screenshot.png` |
| "Read the text from this diagram" | `python vision_proxy.py diagram.jpg "Extract all visible text"` |
| "Describe this video" | `python vision_proxy.py demo.mp4` |
| "What UI flow does this recording show?" | `python vision_proxy.py recording.mp4 "Describe the UI flow and each action"` |

### Important

- **Always use the full absolute path** to the script and the file.
- If `config.json` is missing, run `setup.py` first.
- The script prints the description to stdout. Return it to the user.
- For videos, it extracts up to 8 evenly-spaced keyframes via ffmpeg.

## Installation

See **[README.md](README.md)** for adding this as a skill to opencode.jsonc.
