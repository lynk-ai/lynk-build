---
name: Versions and governance — revision lineage, the 2026-07-28 RC, SEPs, and the foundation
description: Which spec revision introduced what, what the 2026-07-28 release candidate changes, and who governs the protocol. Read when pinning a protocol version, checking whether a feature exists in the revision you target, planning for the next revision, or answering who controls MCP.
labels: [versions, revisions, changelog, 2025-11-25, 2026-07-28, release-candidate, sep, governance, linux-foundation, agentic-ai-foundation, extensions, mcp-apps, tasks, oauth]
---

The revision lineage is **2024-11-05 → 2025-03-26 → 2025-06-18 → 2025-11-25**, each spec page naming its predecessor (modelcontextprotocol.io/specification/2025-11-25/changelog; the 2025-06-18 link in the chain is derived from the 2025-11-25 changelog's "since 2025-06-18" header — the 2025-06-18 changelog itself was not fetched, so this book attributes no specific features to that revision). The current stable revision as of this writing (2026-07-21) is **2025-11-25** (modelcontextprotocol.io/specification/latest, fetched 2026-07-21).

What landed where (all from the official changelogs for 2025-03-26 and 2025-11-25):

| Revision | Notable changes |
|---|---|
| 2025-03-26 | Streamable HTTP replaces HTTP+SSE (PR #206); OAuth 2.1 authorization framework; tool annotations (read-only/destructive); JSON-RPC batching; audio content |
| 2025-11-25 | Tasks (experimental); OpenID Connect Discovery for auth-server discovery; icons metadata; sampling gains `tools`/`toolChoice`; JSON Schema 2020-12 as default dialect; `ElicitResult`/enum schema changes + URL-mode elicitation |

One dating trap from the same source: **elicitation predates 2025-11-25** — that changelog only *modifies* elicitation (schemas, URL mode); it did not introduce it. Do not cite 2025-11-25 as elicitation's origin.

**The next revision.** A release candidate for **2026-07-28** is public, with final publication scheduled July 28, 2026 (MCP official blog, blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ — headline list below is sourced via a search-result summary of that post, consistent across the official blog and roadmap post, so treat exact details as to-be-confirmed against the final publication). Headline changes: a **stateless protocol core** (drops the init handshake and the protocol-level session header for remote servers — a direct break with the lifecycle described in [lifecycle-and-transports](lifecycle-and-transports.md)); an **Extensions framework** (reverse-DNS IDs, negotiated via capability maps, versioned independently in `ext-*` repos); **MCP Apps** (servers ship sandboxed-iframe HTML UIs speaking the same JSON-RPC); and **Tasks** moving from experimental core to an extension.

**Governance.** MCP adopted a formal governance model in **July 2025**: SEPs — Specification Enhancement Proposals — as the change mechanism (formalized as SEP-932 in the 2025-11-25 revision), plus Working and Interest Groups (blog.modelcontextprotocol.io, "Building to Last", 2025-07-31; 2025-11-25 changelog). To actually propose a change — the scope gate, template, sponsor requirement, and review flow — follow the recipe in [submit-a-sep](submit-a-sep.md). On **December 9, 2025**, Anthropic donated MCP to the newly created **Agentic AI Foundation**, a directed fund under the **Linux Foundation**, as a founding project alongside Block's goose and OpenAI's AGENTS.md; the steering committee draws from Anthropic, OpenAI, Microsoft, Google, and Amazon, and day-to-day maintainer governance stayed unchanged (blog.modelcontextprotocol.io "MCP joins the Agentic AI Foundation", 2025-12-09; Anthropic's donation announcement). The practical consequence (derived): "will Anthropic change this under us?" is no longer the right risk question — protocol changes go through SEPs under a multi-vendor foundation.
