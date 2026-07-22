---
name: Test and connect — Inspector, Claude Desktop, Claude Code
description: How to exercise a server without a host (MCP Inspector) and how to wire it into Claude Desktop and Claude Code. Read when your server runs but you can't invoke it, when Claude Desktop doesn't show your tools, or when deciding where an MCP config entry should live.
labels: [testing, debugging, mcp-inspector, npx, claude-desktop, claude-code, claude-mcp-add, claude_desktop_config, mcp-json, scope, config]
---

**Test first, connect second** — the Inspector removes the host from the debugging loop, so a failure there is unambiguously your server's.

**MCP Inspector** (modelcontextprotocol.io/docs/tools/inspector): zero install —

```
npx @modelcontextprotocol/inspector <server command>
```

e.g. `npx @modelcontextprotocol/inspector node build/index.js` or `npx @modelcontextprotocol/inspector uvx mcp-server-git`. It gives you transport selection, Resources/Prompts/Tools tabs with schema display and interactive invocation, and a notifications/log pane. For Python servers built with the v1 SDK, `uv run mcp dev server.py` launches the same Inspector (quickstart — see [build-a-server](build-a-server.md)).

**Claude Desktop** (modelcontextprotocol.io/docs/develop/build-server and /docs/develop/connect-local-servers, for this whole block): edit `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `%APPDATA%\Claude\claude_desktop_config.json` on Windows, adding entries under the `mcpServers` key:

```json
{"mcpServers": {"weather": {"command": "uv", "args": ["--directory", "/ABSOLUTE/PATH/TO/PROJECT", "run", "weather.py"]}}}
```

Three requirements the docs call out explicitly (same source): paths must be **absolute**; the file must be **created if absent**; and a **full app restart** is required after editing.

**Claude Code** takes a CLI instead of a config file: `claude mcp add <name> -- <command>` for stdio (the default) or `claude mcp add <name> --transport http <url>` for remote servers, with a `--scope` flag choosing where the entry lives — local, project, or user — and project-scoped config landing in `.mcp.json` at the repo root (code.claude.com/docs/en/mcp-quickstart; the exact `--scope` value names are high-confidence but sourced secondarily — not verified against a direct fetch of that page, so check `claude mcp add --help` before scripting them).

The connection you are configuring here is the host launching your server as a stdio subprocess — the lifecycle that then runs over it is [lifecycle-and-transports](lifecycle-and-transports.md). Anything you connect this way runs with your local user's permissions; the one-click/local-config risks are cataloged in [security-pitfalls](security-pitfalls.md).
