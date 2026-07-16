---
type: principle
description: WRITE / SELECT / COMPRESS / ISOLATE — the four levers on what's inside the context window right now.
---

# The four operations

**What it is** — a taxonomy (Lance Martin, building on Karpathy) for one problem: *what's inside the context window right now, and what to do about it*. Four levers: push out, pull back in, shrink in place, split off.

**Mechanics**

| Operation | What it means | Everyday example |
|---|---|---|
| **WRITE** | Save something outside the window so it isn't lost — without cramming it into the prompt now. | A todo list saved to a file; a subagent's notes on disk instead of in chat. |
| **SELECT** | Pull back in only what's relevant, exactly when it's relevant. | Reading one specific file instead of the whole repo; loading one skill's instructions. |
| **COMPRESS** | Shrink something already in the window without losing the point. | Summarizing a long tool result; conversation compaction. |
| **ISOLATE** | Give a sub-task its own window so it doesn't pollute the main one. | A research subagent that hands back only a summary. |

WRITE/SELECT fire around *needed now vs. later*. COMPRESS/ISOLATE fire when *volume itself* is the problem.

**Takeaway** — **not "everything an agent does" — the toolkit for one job: keeping the context window lean.**

**Example** *(constructed, illustrative)* — a todo list gets written to a file instead of kept in chat (WRITE); later, only the one relevant item is pulled back in — not the whole list (SELECT).

**In this system** — the whole pipeline is these four levers composed: books are WRITEs, the librarian's reading list is SELECT, readers run ISOLATEd and their cited findings are the COMPRESSed return. The session sticky note is a SELECT-enabler: 2KB of pointers so agents can pull details on demand. → See [progressive-disclosure](progressive-disclosure.md) — SELECT turned into an economy — and the Subagents book · `isolation-is-a-decision` for ISOLATE done right.
