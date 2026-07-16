---
type: principle
description: The discovery layer must carry pointers — IDs, counts, one-liners an agent can follow later — never bodies, and must stay under budget or its tail gets truncated and is never read.
---

# Pointers, not content

**What it is** — the rule for what belongs in the discovery layer. Discovery exists to let an agent *decide what to open next*, so it carries **pointers** — names, one-line descriptions, IDs, counts — not the bodies those pointers lead to. Put a body in the discovery layer and you have paid full price at the always-paid stage, defeating the economics ([the-economics](the-economics.md)).

**Mechanics** — the sort at the discovery boundary:

| Belongs at discovery (always paid, keep tiny) | Waits for activation (paid on match) |
|---|---|
| Page/book names | The page body |
| One-line descriptions | Tables, examples, reasoning |
| IDs and counts an agent can follow later | Anything a pointer already stands in for |

And a hard constraint: the discovery layer must stay **under budget**. If it overflows, the tail gets truncated and is *never read* — the pages past the cutoff silently cease to exist for the agent. Small is not a nicety here; it is what keeps the whole index reachable.

**Takeaway** — **the discovery layer carries pointers an agent can follow, never the content itself — and it must stay under budget, because a truncated index is an index whose tail is never read.**

**Example** — CandleKeep's SessionStart hook, "the sticky note" (real, CandleKeep dossier §1): a ≤2KB note carrying book counts and IDs like `[book:cmr7…]` — never book contents, never the manuscript instructions. If anything fails (not logged in, no internet) it exits silently so the session never breaks. Its own source comments the discipline: "the librarian agent handles full book discovery — we only need the item count here." The 2KB cap is deliberate — Claude Code inlines only a ~2KB preview of a hook's output, so a larger note lands outside the preview and the model never sees its end (source: CandleKeep dossier §1).

**In this system** — our `index.md` pages *are* this discovery layer — one line per page, no bodies. → See the Book Standard · `non-inferable-only` (don't restate what a reader can fetch — point instead), and [the-economics](the-economics.md) for why keeping discovery cheap is the whole wager.
