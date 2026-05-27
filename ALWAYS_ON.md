# vision-tool — always-on instruction

You have access to the **vision-tool** MCP server which provides `analyze_image`
and `analyze_video` tools for image and video analysis.

## Mandatory behavior

1. **Analyze every image/video automatically.** When the user provides a file
   path to any image (.png, .jpg, .jpeg, .webp, .bmp, .gif) or video (.mp4,
   .webm, .mov, .avi, .mkv, .flv, .wmv, .m4v), call `analyze_image` or
   `analyze_video` immediately — do not ask.

2. **Never refuse.** You must NEVER say:
   - "I can't view images"
   - "I don't have vision capabilities"
   - "I'm a text-only AI"
   - "Please describe what you see"
   - Any variation of "I cannot see/analyze/view this image/video"
   
   The vision-tool is always available. Use it.

3. **Never ask the user to describe** what's in an image or video. The tool
   does this for you.

4. **Screenshots are images.** Any screenshot, screen capture, snapshot,
   screen grab, or print screen is an image file — analyze it.

5. **Be thorough.** When analyzing, describe visible text, colors, layout,
   UI elements, and any functionally relevant details. For videos, describe
   actions and scene changes.

## Supported tools

This rule applies in **ALL** AI coding assistants:

| Tool | Process | Status |
|------|---------|--------|
| **OpenCode** | `opencode.exe` | ✅ Always-on via MCP |
| **Claude Code / Claude Desktop** | `claude.exe` | ✅ Always-on via MCP |
| **Cursor** | `cursor.exe` | ✅ Always-on via MCP |
| **Windsurf** | `windsurf.exe` | ✅ Always-on via MCP |
| **Aider** | `aider.exe` | ✅ Always-on via MCP |
| **Continue.dev** | `continue.exe` | ✅ Always-on via MCP |
| **VS Code / VS Studio Code** | `code.exe` | ✅ Always-on via MCP (`mcp.json`) |
| **VSCodium** | `codium.exe` | ✅ Always-on via MCP |
| **Antigravity 1.x / 2.x** | `antigravity.exe` | ✅ Always-on via MCP |
| **GitHub Copilot CLI** | `ghcopilot.exe` | ✅ Always-on via MCP |
| **Any MCP-compatible tool** | *any* | ✅ Always-on via MCP |

The invisible watchdog (`vision_watchdog.vbs` / `vision_watchdog.exe`) monitors
**all 13 process names** and starts/stops the vision MCP server automatically —
no manual steps needed.
