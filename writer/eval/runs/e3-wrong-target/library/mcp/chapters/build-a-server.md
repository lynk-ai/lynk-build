---
name: Build a server — the Python and TypeScript minimal paths
description: The shortest working path to an MCP server in Python or TypeScript, and the v1-vs-v2 SDK trap. Read when writing your first server, choosing which SDK line to pin, or when imports/class names from a tutorial don't match the SDK you installed.
labels: [build, python, typescript, sdk, fastmcp, mcpserver, registerTool, decorators, zod, v1, v2, pip, npm, uv, sdk-tiers]
---

Before writing a line: the official SDKs are tiered (tiering formalized by SEP-1730) — **Tier 1**: TypeScript, Python, C#, Go; **Tier 2**: Java, Rust; **Tier 3**: Swift, Ruby, PHP, Kotlin; all under `github.com/modelcontextprotocol/{language}-sdk` (modelcontextprotocol.io/docs/sdk, fetched 2026-07-21). This chapter covers the two Tier-1 paths the official quickstart documents.

**The trap worth this page's existence: both flagship SDKs are mid-major-version as of July 2026** (both READMEs, fetched 2026-07-21), so any example you copy — including this book's — must state which line it targets.

- **Python** (github.com/modelcontextprotocol/python-sdk README, fetched 2026-07-21): v2 is pre-release (`pip install "mcp[cli]==2.0.0b1"`), renaming the server class to `MCPServer` from `mcp.server` and adding a unified `Client`. The README directs production use to **v1.x, constraint `mcp>=1.27,<2`**, where the class is `FastMCP`. If your import of `FastMCP` fails, you are probably on v2; if `MCPServer` fails, you are on v1.
- **TypeScript** (github.com/modelcontextprotocol/typescript-sdk README): v1 (`@modelcontextprotocol/sdk`) is the supported production release; v2 beta splits into `@modelcontextprotocol/server` / `@modelcontextprotocol/client` (plus `/node`, `/express`, `/hono` middleware) and moves to Zod v4.

Everything below targets the **v1** lines, matching the official quickstart at modelcontextprotocol.io/docs/develop/build-server — which is also where to fetch the full runnable example; this page keeps only the skeleton and the decisions around it.

**Python minimal path** (quickstart, Python tab, + python-sdk README): `uv add "mcp[cli]" httpx`, then

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("weather")

@mcp.tool()
async def get_forecast(latitude: float, longitude: float) -> str:
    """Get the forecast for a location."""   # (constructed, illustrative body — the shape is the quickstart's)
    ...

mcp.run(transport="stdio")
```

FastMCP auto-generates tool schemas from type hints and docstrings — so the docstring and annotations *are* your API contract, not decoration. `@mcp.resource("greeting://{name}")` and `@mcp.prompt()` register the other two server primitives (see [what-mcp-is](what-mcp-is.md)). Test with `uv run mcp dev server.py`, which launches the Inspector (see [test-and-connect](test-and-connect.md)).

**TypeScript minimal path** (quickstart, TypeScript tab): `npm install @modelcontextprotocol/sdk zod@3` — note the explicit Zod 3 pin, given v2's move to Zod 4 — then `import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js"` and `import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js"`; construct `new McpServer({ name, version })`, register tools with `server.registerTool(name, { description, inputSchema }, handler)` using Zod schemas, and connect via a `StdioServerTransport`.

In both SDKs you never declare the handshake's capabilities object yourself — the server classes compute it from what you register (see [lifecycle-and-transports](lifecycle-and-transports.md) for the claim's derivation and the wire format). One stdio rule to respect from day one: log to stderr only — stdout belongs to the protocol (same chapter). And before shipping anything beyond a toy, read [security-pitfalls](security-pitfalls.md) — your tool descriptions and docstrings are fed verbatim to every host's model, making them attack surface; the demonstrated tool-poisoning attack (Invariant Labs, April 2025) and the spec's named attack classes live there.
