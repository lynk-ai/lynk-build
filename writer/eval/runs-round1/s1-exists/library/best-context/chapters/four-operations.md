---
name: The four operations
description: WRITE / SELECT / COMPRESS / ISOLATE — the four levers on what's inside the context window right now. Read when deciding what to do about an overfull or polluted context window — offload, fetch back, shrink, or isolate.
labels: [write, select, compress, isolate, offload, retrieval, context window, levers]
---

There is a taxonomy (Lance Martin, LangChain — *Context Engineering for Agents*, 2025 — building on Karpathy) for one problem: *what's inside the context window right now, and what to do about it*. Four levers: push out, pull back in, shrink in place, split off.

| Operation | What it means | Everyday example |
|---|---|---|
| **WRITE** | Save something outside the window so it isn't lost — without cramming it into the prompt now. | A todo list saved to a file; a subagent's notes on disk instead of in chat. |
| **SELECT** | Pull back in only what's relevant, exactly when it's relevant. | Reading one specific file instead of the whole repo; loading one skill's instructions. |
| **COMPRESS** | Shrink something already in the window without losing the point. | Summarizing a long tool result; conversation compaction. |
| **ISOLATE** | Give a sub-task its own window so it doesn't pollute the main one. | A research subagent that hands back only a summary. |

WRITE and SELECT fire around *needed now vs. later*; COMPRESS and ISOLATE fire when *volume itself* is the problem. **This is not "everything an agent does" — it is the toolkit for one job: keeping the context window lean.** The simplest illustration is a todo list written to a file instead of kept in chat (WRITE), from which only the one relevant item is later pulled back in, not the whole list (SELECT).

Two of the levers have moved partly into the platform (sourced): WRITE and COMPRESS are now API-native — Anthropic ships server-side compaction (`compact_20260112`, default trigger 150K tokens), tool-result clearing (`clear_tool_uses_20250919`, keeps the last 3), and a memory tool (`memory_20250818`, client-executed). ISOLATE stays application-level — no primitive provides subagent isolation. (A parallel academic view: a 2025 memory survey, Du et al., arXiv 2505.00675, splits memory work into six operations and elevates *indexing* and *forgetting* to first-class — a richer taxonomy than these four window-levers, for the memory scope specifically.)

A routed knowledge system composes all four: stored documents are WRITEs, a targeted reading list is SELECT, isolated readers returning only cited findings are ISOLATE plus COMPRESS, and a small pointer note is a SELECT-enabler — pointers up front so details are pulled only on demand. See [progressive-disclosure](progressive-disclosure.md) — SELECT turned into an economy — and [compression](compression.md) for the COMPRESS lever in depth.
