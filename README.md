# opencode-vision

**Image & video analysis for AI coding assistants that don't have eyes.**

Opencode-vision is a drop-in skill that lets any opencode model — including
`big-pickle`, `DeepSeek`, or local models — describe images and videos by
routing them through external vision-capable models.

## Features

- **Images** — PNG, JPG, WebP, BMP, animated GIF
- **Videos** — MP4, WebM, MOV, AVI, MKV, FLV, WMV, M4V (via ffmpeg keyframe extraction)
- **7 fallback backends** — chains through Gemini 2.5 Flash → 2.0 Flash →
  NVIDIA Nemotron → Gemma 4 → Qwen VL → OpenRouter free until one works
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

You need at least one of these (both are free):

| Provider | Get key | Used for |
|---|---|---|
| **Gemini** | https://aistudio.google.com/apikey | Images + video (native support) |
| **OpenRouter** | https://openrouter.ai/keys | Free vision model fallback |

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
    1. Gemini 2.5 Flash  (best, native video)
    2. Gemini 2.0 Flash
    3. NVIDIA Nemotron Omni (free)
    4. Gemma 4 26B (free)
    5. NVIDIA Nemotron VL (free)
    6. Qwen VL 8B
    7. OpenRouter free (last resort)
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

GPL-3.0 — see [LICENSE](LICENSE).
