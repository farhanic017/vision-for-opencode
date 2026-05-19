#!/usr/bin/env python3
"""
vision_mcp_server.py — MCP server for opencode-vision.
Copyright (C) 2026 Farhan Dhrubo

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

Exposes vision_proxy.py as MCP tools so any MCP-compatible client
(OpenCode, Claude Desktop, Cursor, Windsurf, Continue.dev, etc.)
can analyse images and videos via natural language.

Tools:
  - analyze_image(path, prompt?)
  - analyze_video(path, prompt?)

Add to any MCP client:
  {
    "mcpServers": {
      "opencode-vision": {
        "command": "python",
        "args": ["path/to/vision_mcp_server.py"]
      }
    }
  }

Protocol: JSON-RPC 2.0 over stdio (standard MCP).
"""

import json
import sys
import os
import io
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import vision_proxy as vp

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

TOOLS = {
    "analyze_image": {
        "name": "analyze_image",
        "description": "Analyse an image file and return a text description of what it shows — text, colours, layout, UI elements, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute path to the image (png, jpg, webp, bmp, gif)"},
                "prompt": {"type": "string", "description": "Optional custom prompt, e.g. 'Extract all text from this diagram'"},
            },
            "required": ["path"],
        },
    },
    "analyze_video": {
        "name": "analyze_video",
        "description": "Analyse a video file by extracting keyframes and returning a text description of actions, UI flow, scene changes, etc.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "path": {"type": "string", "description": "Absolute path to the video (mp4, webm, mov, avi, mkv, flv, wmv, m4v)"},
                "prompt": {"type": "string", "description": "Optional custom prompt, e.g. 'Describe the UI flow step by step'"},
            },
            "required": ["path"],
        },
    },
}


def handle_tool_call(name, args):
    tool_map = {
        "analyze_image": vp.analyze,
        "analyze_video": vp.analyze,
    }

    if name not in tool_map:
        return {"content": [{"type": "text", "text": f"Unknown tool: {name}"}], "isError": True}

    path = args.get("path", "")
    prompt = args.get("prompt", "")

    try:
        result = tool_map[name](path, prompt)
        return {"content": [{"type": "text", "text": result}]}
    except FileNotFoundError as e:
        return {"content": [{"type": "text", "text": str(e)}], "isError": True}
    except Exception as e:
        return {"content": [{"type": "text", "text": f"Error: {e}"}], "isError": True}


def send(msg):
    sys.stdout.write(json.dumps(msg, ensure_ascii=False) + "\n")
    sys.stdout.flush()


def main():
    buf = ""

    while True:
        try:
            chunk = sys.stdin.read(4096)
            if not chunk:
                break
            buf += chunk

            while "\n" in buf:
                line, buf = buf.split("\n", 1)
                line = line.strip()
                if not line:
                    continue

                try:
                    msg = json.loads(line)
                except json.JSONDecodeError:
                    continue

                msg_id = msg.get("id")
                method = msg.get("method")
                params = msg.get("params", {})

                # ── initialize ──────────────────────────────────────
                if method == "initialize":
                    send({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {
                            "protocolVersion": "2024-11-05",
                            "capabilities": {
                                "tools": {
                                    name: {
                                        "description": info["description"],
                                        "inputSchema": info["inputSchema"],
                                    }
                                    for name, info in TOOLS.items()
                                }
                            },
                            "serverInfo": {
                                "name": "opencode-vision",
                                "version": "1.0.0",
                            },
                        },
                    })
                    continue

                # ── tools/list ──────────────────────────────────────
                if method == "tools/list":
                    send({
                        "jsonrpc": "2.0",
                        "id": msg_id,
                        "result": {"tools": list(TOOLS.values())},
                    })
                    continue

                # ── tools/call ──────────────────────────────────────
                if method == "tools/call":
                    tool_name = params.get("name", "")
                    tool_args = params.get("arguments", {})
                    try:
                        result = handle_tool_call(tool_name, tool_args)
                        send({"jsonrpc": "2.0", "id": msg_id, "result": result})
                    except Exception as e:
                        send({
                            "jsonrpc": "2.0",
                            "id": msg_id,
                            "error": {"code": -32603, "message": str(e), "data": traceback.format_exc()},
                        })
                    continue

                # ── notifications (no id) ───────────────────────────
                if msg_id is None:
                    continue

                send({
                    "jsonrpc": "2.0",
                    "id": msg_id,
                    "error": {"code": -32601, "message": f"Unknown method: {method}"},
                })

        except (EOFError, KeyboardInterrupt):
            break
        except Exception as e:
            send({
                "jsonrpc": "2.0",
                "id": None,
                "error": {"code": -32603, "message": str(e), "data": traceback.format_exc()},
            })


if __name__ == "__main__":
    main()
