---
name: Why MCP exists — origin, adoption, governance
description: The integration problem MCP solves, who created it and when, how the major vendors adopted it, and who governs it now. Read when deciding whether to bet on MCP, justifying that bet to others, or checking who actually controls the spec.
labels: [origin, anthropic, adoption, openai, google, microsoft, governance, linux-foundation, aaif, history, n-times-m]
---

Before MCP, every AI application that wanted to reach a data source or tool built a bespoke integration — N applications × M integrations, each pair custom. Anthropic's launch announcement (anthropic.com/news/model-context-protocol, November 25, 2024) framed the problem in exactly those terms: AI systems "trapped behind information silos," to be fixed by replacing "fragmented integrations with a single protocol." MCP was announced and open-sourced that day; the announcement names David Soria Parra and Justin Spahr-Summers as the creators, and it shipped with the spec plus SDKs, Claude Desktop local-server support, pre-built servers (Google Drive, Slack, GitHub, Git, Postgres, Puppeteer), and named early adopters Block, Apollo, Zed, Replit, Codeium, and Sourcegraph (same source).

What makes MCP a safe dependency rather than one vendor's SDK is that every major competitor of its creator adopted it within six months:

| When | Who | What |
|---|---|---|
| March 26, 2025 | OpenAI | MCP support announced — Agents SDK first, then Responses API and ChatGPT desktop; Altman: "people love MCP" (TechCrunch, 2025-03-26) |
| April 2025 | Google DeepMind | Demis Hassabis confirmed MCP support for Gemini, calling it "rapidly becoming an open standard for the AI agentic era" (widely reported April 2025; the exact date is from secondary reporting, e.g. Wikipedia's MCP article — treat the day as uncertain, the month as solid) |
| May 19, 2025 | Microsoft | At Build: native MCP support in Windows 11 as the foundation of an "agentic OS"; joined the MCP steering committee; MCP wired into GitHub, Copilot Studio, Dynamics 365, Azure AI Foundry, and Semantic Kernel (Microsoft's Windows blog, 2025-05-19) |

The governance question — "isn't this still Anthropic's protocol?" — closed on December 9, 2025: Anthropic transferred MCP entirely (spec, reference code, docs, and trademark) to the newly formed **Agentic AI Foundation (AAIF)**, a directed fund under the Linux Foundation (blog.modelcontextprotocol.io, 2025-12-09; Linux Foundation press release). AAIF launched with 150+ member organizations; its founding projects are MCP, Block's goose, and OpenAI's AGENTS.md; and MCP is governed by a community-elected technical steering structure with Anthropic holding a non-veto seat, Kubernetes/PyTorch-style (same sources).

One dating anchor that prevents version confusion: the 2025-11-25 spec revision landed on MCP's exact one-year anniversary and was framed by the project itself as the "stable" release milestone (blog.modelcontextprotocol.io anniversary post, 2025-11-25). That revision is the one this book is anchored on; the versioning scheme itself is covered in [protocol-lifecycle-and-versioning](protocol-lifecycle-and-versioning.md).
