---
name: Build an MCP server — the recipe
description: SDK choice, the Python and TypeScript server patterns, Inspector testing, and wiring into Claude Desktop and Claude Code. Read when building your first server, when a working server won't appear in a client, or when tool calls silently corrupt or time out.
labels: [build, how-to, fastmcp, mcpserver, python-sdk, typescript-sdk, inspector, claude-desktop, claude-code, mcp-json, scopes, stdout, logging, timeout]
---

This is the how-to chapter: prerequisites, steps, verification, failure modes. Everything here targets the **stable v1 SDKs** against spec revision 2025-11-25; both SDKs have v2 pre-releases in flight, flagged at the end, and the sources are the official build-server tutorial (modelcontextprotocol.io/docs/develop/build-server), the SDK READMEs, and code.claude.com/docs/en/mcp, cited per item below.

**Prerequisites.** Pick a language with a mature SDK: the ten official SDKs carry a formal tier system (SEP-1730) — Tier 1: TypeScript, Python, C#, Go; Tier 2: Java, Rust; Tier 3: Swift, Ruby, PHP, Kotlin — all under the `modelcontextprotocol` GitHub org (modelcontextprotocol.io/docs/sdk). This recipe shows the two we judge best-documented — our call: Python (needs `uv` and the `mcp` package — the official tutorial installs `"mcp[cli]"`) and TypeScript (needs Node; the tutorial installs `@modelcontextprotocol/sdk zod@3`). You also need a client to test against — the Inspector needs only `npx`; Claude Desktop or Claude Code for real use. For Python, pin `mcp>=1.27,<2`: the SDK README states v1.x "is the only stable release line and remains recommended for production" (github.com/modelcontextprotocol/python-sdk README, fetched 2026-07).

**Step 1 — write the server.** The canonical Python pattern (build-server tutorial, Python tab; python-sdk repo — the `FastMCP("weather")` / `@mcp.tool()` / `mcp.run(transport="stdio")` skeleton is the tutorial's; the function body here is condensed and illustrative):

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
def get_forecast(city: str) -> str:
    """Get the forecast for a city."""
    ...

mcp.run(transport="stdio")
```

Type hints plus the docstring auto-generate the tool's schema. The same decorator family covers the other primitives: `@mcp.resource("greeting://{name}")` and `@mcp.prompt()` (same source). The TypeScript equivalent (build-server tutorial, TypeScript tab): import `McpServer` from `@modelcontextprotocol/sdk/server/mcp.js` and `StdioServerTransport` from `@modelcontextprotocol/sdk/server/stdio.js`; register tools with `server.registerTool(name, { description, inputSchema: { /* zod shapes */ } }, async handler)` where the handler returns `{ content: [{ type: "text", text }] }`; finish with `await server.connect(new StdioServerTransport())`. Outcome: a file that starts, speaks stdio, and exposes at least one tool.

**Step 2 — obey the stdout rule while you still remember it.** The official tutorial states it verbatim: "For STDIO-based servers: Never write to stdout. Writing to stdout will corrupt the JSON-RPC messages and break your server." Per-language (same source, Logging sections): Python `print()` is unsafe unless `file=sys.stderr`; JS `console.log()` is unsafe — use `console.error()`; Java `System.out.println()` is unsafe. HTTP-based servers may log to stdout freely. Outcome: all logging in your server goes to stderr (which the spec explicitly permits for any logging — see [transports](transports.md)).

**Step 3 — test under the Inspector before touching any client config.** Zero install: `npx @modelcontextprotocol/inspector <command> [args...]` — e.g. `npx @modelcontextprotocol/inspector node build/index.js`, or wrap the Python invocation (`uvx`/`uv --directory ... run ...`); the Python SDK also offers `uv run mcp dev server.py` to launch under the Inspector directly (modelcontextprotocol.io/docs/tools/inspector; inspector repo; python-sdk docs). The UI has tabs for Resources, Prompts, and Tools — schema view plus invocation with custom inputs — and a notifications/log pane. Outcome: you've listed your tools and invoked one with real inputs. Keep the Inspector current: versions below 0.14.1 carried an unauthenticated-proxy RCE, CVE-2025-49596 (see [security](security.md)).

**Step 4 — wire into a client.** Claude Desktop (build-server tutorial, Claude for Desktop section): config lives at `~/Library/Application Support/Claude/claude_desktop_config.json` on macOS or `$env:AppData\Claude\claude_desktop_config.json` on Windows — create it if absent — with servers under the `mcpServers` key:

```json
{ "mcpServers": { "weather": { "command": "uv",
  "args": ["--directory", "/ABSOLUTE/PATH/TO/weather", "run", "weather.py"] } } }
```

Absolute paths are required (same source). Claude Code (code.claude.com/docs/en/mcp): `claude mcp add --transport http <name> <url>` for HTTP, `--transport sse` for SSE, or for stdio `claude mcp add [options] <name> -- <command> [args...]` — the `--` separates Claude's flags from the server command, and omitting it is a classic footgun (same source); env vars go via `--env KEY=value`; manage with `claude mcp list` / `claude mcp get` / `/mcp` in-session, and `/mcp` also handles OAuth for remote servers. Claude Code has three config scopes selected with `-s/--scope` (same source): `local` (default — per-user, per-project, stored in `~/.claude.json`), `project` (a checked-in `.mcp.json`, which teammates must approve on first run), and `user` (all projects); in `.mcp.json`, `type: "streamable-http"` is accepted as an alias for `http`, so spec-style configs paste in unchanged. Outcome: the server appears in the client's MCP UI.

**Verification.** Three checks, cheapest first: (1) Inspector lists your tools and a call round-trips (step 3); (2) after client wiring, the client's MCP surface shows the server — in Claude Desktop, MCP UI elements only appear once at least one configured server parses (build-server tutorial), so their presence is itself the check; (3) end-to-end, ask the model to use the tool and confirm the result reflects your server's output.

**Failure modes.**

- *Server dies instantly or the client shows garbled-message errors* → something wrote to stdout. Symptom-to-cause is near-certain for stdio servers (derived from the tutorial's verbatim warning in step 2); grep for `print(`/`console.log`.
- *Server absent from Claude Desktop* → config didn't parse or paths aren't absolute; per the tutorial the MCP UI simply doesn't appear until one server parses, so a missing UI means a config problem, not a protocol one.
- *`claude mcp add` created a broken entry* → the `--` separator was omitted, so server args were eaten as Claude flags (code.claude.com/docs/en/mcp).
- *Tool output truncated or flagged in Claude Code* → Claude Code warns at 10,000 tokens of MCP tool output and caps at 25,000 by default; raise with `MAX_MCP_OUTPUT_TOKENS`. Slow startups hit the `MCP_TIMEOUT` env var; per-tool-call timeouts are the `timeout` (ms) field in `.mcp.json` (all from code.claude.com/docs/en/mcp).
- *Examples from the internet don't match your SDK* → you're reading v2 pre-release docs. Python v2.0.0b1 renames the server class (`from mcp.server import MCPServer`) per the python-sdk README (fetched 2026-07); the TypeScript main branch splits the package — server code moves to `@modelcontextprotocol/server` with `zod/v4` schemas, same registerTool shape (typescript-sdk README, fetched 2026-07). Teach/build on v1 (`FastMCP`, `@modelcontextprotocol/sdk`) until v2 stabilizes — that recommendation is the Python README's own, extended to TypeScript as our call.
