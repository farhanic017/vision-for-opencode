# opencode-vision

> Created by [Farhan Dhrubo](https://github.com/farhanic017) — [Submit an issue](https://github.com/farhanic017/vision-for-opencode/issues)

**Image & video analysis for AI coding assistants that don't have eyes.**

Opencode-vision is a drop-in skill that lets any opencode model — including
`big-pickle`, `DeepSeek`, or local models — describe images and videos by
routing them through external vision-capable models.

## Features

- **Images** — PNG, JPG, WebP, BMP, animated GIF
- **Videos** — MP4, WebM, MOV, AVI, MKV, FLV, WMV, M4V (via ffmpeg keyframe extraction)
- **12 fallback backends** — free models first, then paid models for reliability
- **Zero hardcoded secrets** — API keys live in `config.json` (gitignored) or env vars
- **Secure** — your keys never leave your machine except to the API provider you chose
- **Works anywhere** — opencode, Claude Code, Cursor, or plain terminal

## Quick start

```bash
# 1. Clone or copy this folder anywhere
git clone https://github.com/<your-username>/opencode-vision.git

# 2. Install dependencies
pip install pillow

# 3. Run the setup wizard
python setup.py

# 4. Analyse anything
python vision_proxy.py screenshot.png
python vision_proxy.py demo.mp4 "Describe the UI flow"
```

### Add to opencode

Add this to your `opencode.jsonc` under `skills.paths`:

```jsonc
{
  "skills": {
    "paths": [
      "path/to/vision-for-open-code"
    ]
  }
}
```

Now your opencode AI will automatically offer to analyse images and videos
when you ask it to "look at" something.

> **Tip**: If you use the [skill-dispatcher](https://github.com/farhanic017/dynamic-skill-loader-for-opencode),
> point it at this folder and it will load the skill on-demand, keeping
> your startup fast.

## Getting API keys

You need at least one of these (both are free to start):

| Provider | Get key | Used for |
|---|---|---|
| **Gemini** | https://aistudio.google.com/apikey | Images + video (native support, free tier) |
| **OpenRouter** | https://openrouter.ai/keys | All other backends (has free + paid models) |

Run `python setup.py` to enter them — it validates each key before saving.

## How it works

```
User: "What's in this image?"
        │
        ▼
  opencode model (no vision)
        │
        ▼
  vision_proxy.py <image.png>
        │
        ├── Images → resize to 1024px
        └── Videos → ffmpeg extracts 8 keyframes
        │
        ▼
  Send to first working backend:
  Free backends (☆):
    1. Gemini 2.5 Flash       — native video, free tier
    2. Gemini 2.0 Flash       — fallback Gemini
    3. NVIDIA Nemotron Omni   — free OpenRouter
    4. Gemma 4 26B            — free OpenRouter
    5. NVIDIA Nemotron VL     — free OpenRouter
    6. OpenRouter free        — any free model
  Paid backends (★, skipped if OpenRouter key has no billing):
    7. GPT-4o                 — OpenAI's best vision
    8. GPT-4o-mini            — cheap & fast
    9. Claude 3.5 Sonnet      — Anthropic
   10. Claude 3 Haiku         — cheap & fast
   11. Llama 3.2 90B Vision   — Meta
   12. Qwen VL 8B             — cheap & capable
        │
        ▼
  Returns text description → model reads it to you
```

## Requirements

- Python 3.8+
- `pillow` (for image resize/resample)
- `ffmpeg` (for video keyframe extraction — [download](https://ffmpeg.org/download.html))

## File structure

```
vision-for-open-code/
├── README.md              # This file
├── SKILL.md               # opencode skill definition
├── vision_proxy.py        # Main analysis script
├── setup.py               # First-run API key wizard
├── config.json.example    # Example config (safe to commit)
├── config.json            # Your actual keys (gitignored)
├── requirements.txt       # pip dependencies
├── .gitignore             # Ignores config.json, __pycache__
└── LICENSE                # GPL-3.0
```

## Security

- **No API keys in code.** All keys go into `config.json` (in `.gitignore`) or
  environment variables.
- **No telemetry.** This script never phones home. It only talks to the API
  providers you configure.
- **No data storage.** Images/videos are never saved or logged; keyframes are
  written to a temp directory and immediately cleaned up.

## License

GNU General Public License v3.0 — see [LICENSE](./LICENSE).

This program is free software: you can redistribute and/or modify it under the terms of the GPLv3.
Modified versions must be licensed under GPLv3 with clear attribution to the original author.

© 2026 Farhan Dhrubo.
