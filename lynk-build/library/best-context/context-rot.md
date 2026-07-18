---
type: principle
description: Answer quality drops as context grows — even relevant context — and it starts dropping before the window is full.
---

# Context rot

**What it is** — the core problem every other page in this book exists to fight: answer quality drops as more context is added — *even context that looks relevant* — and the drop starts well before the window is full.

**Mechanics**

| | |
|---|---|
| **Builds** | Every extra token added to context, relevant or not. |
| **Triggers** | No single event — it's continuous, as noise-to-signal rises. |
| **Result** | Attention dilutes across more tokens; the answer measurably gets worse. |

The trap hiding inside it: "more context means more accuracy" is *also* true — for **curated, scoped** context that a task actually needs. Rot is about **raw volume**. The resolution: context should *compound* (more of the right things, loaded when applicable), never *pile* (everything, always). The difference between compounding and piling is everything else in this book.

**Takeaway** — **more context is never free: ask "does this token help," not "is there room."**

**Example** — same model, same question. 500 tokens containing just the relevant doc → correct answer. 50,000 tokens with that same doc buried in meeting notes → measurably worse, sometimes wrong. Nothing was removed; the answer degraded anyway. *(constructed, illustrative)*

Sourced evidence that even *well-intentioned* context rots: an ETH Zurich study (2026, via InfoQ) found AGENTS.md-style context files frequently **hinder** agents — the recommendation was to omit LLM-generated context files entirely and limit human-written ones to non-inferable details. Adding context is an intervention with side effects, not a free vitamin.

**In this system** — rot is why the library exists at all: knowledge lives in small routed pages instead of one big prompt. The librarian reads the shelf (not books); each scout runs its own book's TOC and points at only the chapters that serve the objective — the hook fetches exactly those, and the session note is ≤2KB of pointers. *(superseded 2026-07-14: previously "The librarian reads indexes (not books), readers open only listed pages" — pipeline restructured to the pointer flow; see log.md)* Every design choice traces back to this page. → See [four-operations](four-operations.md) for the levers, [progressive-disclosure](progressive-disclosure.md) for the economy that keeps growth from becoming rot.
