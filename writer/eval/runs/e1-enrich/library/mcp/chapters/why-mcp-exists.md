---
name: Why MCP exists — the integration problem and what it replaced
description: The problem MCP was created to solve, its launch and adoption timeline, and how it differs from vendor function calling. Read when deciding whether to adopt MCP at all, justifying it to stakeholders, or answering "isn't this just function calling?".
labels: [motivation, integration-problem, function-calling, adoption, openai, google, microsoft, anthropic-announcement, n-times-m]
---

Anthropic open-sourced MCP on **November 25, 2024**, releasing the specification and SDKs together with local MCP server support in Claude Desktop and a set of pre-built servers (Google Drive, Slack, GitHub, Git, Postgres, Puppeteer); named launch adopters were Block, Apollo, Zed, Replit, Codeium, and Sourcegraph (Anthropic announcement, anthropic.com/news/model-context-protocol, Nov 25, 2024).

The problem framing, in the announcement's own words: "every new data source requires its own custom implementation," to be replaced by "a single protocol." You will often see this phrased as the "N×M → N+M" argument — M applications times N tools each needing a custom integration. That phrasing is a community formulation, not Anthropic's: the announcement text was checked and "N×M" does not appear in it (derived — announcement text vs. common secondary usage). If you need strict sourcing, cite the "fragmented integrations" framing from the announcement itself.

The bet paid off across vendors within six months (all sourced): **OpenAI** announced MCP support on March 26, 2025 — immediately in the Agents SDK, with ChatGPT desktop and the Responses API "coming soon" (Altman on X, via TechCrunch 2025-03-26). **Google DeepMind** followed on April 9, 2025 — support in Gemini models and SDK, with Hassabis calling MCP "rapidly becoming an open standard for the AI agentic era" (x.com/demishassabis/status/1910107859041271977). **Microsoft** announced native MCP support in Windows 11 at Build on May 19, 2025, framing Windows as an "agentic OS" with system functions exposed as MCP servers; Microsoft and GitHub joined the MCP steering committee at the same time (Windows Developer Blog and Windows Experience Blog, 2025-05-19). Where governance went after that — foundation, SEPs — is covered in [versions-and-governance](versions-and-governance.md).

**MCP vs. plain function calling.** The honest comparison (derived — each MCP-side property below is sourced to the 2025-11-25 spec; the contrast itself is analysis, since "function calling" is a per-vendor API feature, not a specified standard): with function calling, the developer statically supplies tool schemas per request to one vendor's API. MCP adds what that lacks by construction —

- **runtime discovery**: `tools/list` plus `listChanged` notifications, so the tool set is queried live, not compiled in;
- **a transport and wire standard** independent of any model vendor;
- **stateful capability negotiation** between client and server (see [lifecycle-and-transports](lifecycle-and-transports.md));
- **non-tool primitives** — resources, prompts, sampling, elicitation (see [what-mcp-is](what-mcp-is.md)) — including channels for the server to call back into the host.

Function calling answers "how does this model emit a structured call"; MCP answers "how does any application connect to any capability service." They compose rather than compete — a host typically translates MCP tools into its model's function-calling format (derived: this last sentence is our reading of how the two layers fit; the spec does not mandate a host's internal mechanics).
