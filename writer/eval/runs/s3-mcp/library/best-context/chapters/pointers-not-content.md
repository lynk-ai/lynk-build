---
name: Pointers, not content
description: The discovery layer carries pointers — IDs, counts, one-liners an agent can follow later — never bodies, and must stay under budget or its tail gets truncated and is never read. Read when an index, session note, or discovery layer is growing — deciding what may live in it and how big it may get.
labels: [index budget, truncation, sticky note, discovery layer, pointers, session note]
---

This is the rule for what belongs in the discovery layer. Discovery exists to let an agent decide what to open next, so it carries pointers — names, one-line descriptions, IDs, counts — not the bodies those pointers lead to. Put a body in the discovery layer and you have paid full price at the always-paid stage, defeating the economics of [progressive-disclosure](progressive-disclosure.md). So page and book names, one-line descriptions, and IDs and counts an agent can follow later belong at discovery (always paid, keep tiny); page bodies, tables, examples, reasoning, and anything a pointer already stands in for wait for activation (paid on match).

There's a hard constraint on top: the discovery layer must stay under budget. If it overflows, the tail gets truncated and is *never read* — the pages past the cutoff silently cease to exist for the agent. Small is not a nicety here; it is what keeps the whole index reachable. **The discovery layer carries pointers an agent can follow, never the content itself — and it must stay under budget, because a truncated index is an index whose tail is never read.**

A session-start pointer note is the everyday case: a small note (say ≤2KB) carrying counts and IDs, never the contents they point to, that fails silently if it can't be built (no auth, no network) so the session never breaks. The size cap is deliberate — a host often inlines only a small preview of such a note, so anything past the cutoff is never seen: the truncation risk in miniature.

An index that lists a library — one line per chapter, no bodies — is this discovery layer, and a session's pointer note lives under the same budget. The admission discipline is the same rule applied to existence rather than size: don't restate what a reader can fetch — point instead. See [progressive-disclosure](progressive-disclosure.md) for why keeping discovery cheap is the whole wager, and [compression](compression.md) — the same discipline applied to what returns from work already done.
