---
name: Types of context
description: Context comes in six types — behavior, domain knowledge, procedures, memory, working context, actions — each with its own home, lifetime, and dominant failure mode; never merged. Read when deciding where a piece of context should live — system prompt, book, skill, memory, or tool definition — or why one artifact keeps failing in one specific way.
---

"Context" is not one substance. What an agent sees divides into six types, and each wants a different home, has a different lifetime, and breaks in a different way. The general laws of this book — rot, the failure modes, the levers — apply to all six, but treatment is per-type, and the most common building decision, *where does this sentence live?*, is really a typing decision.

The six types:

| Type | Answers | Home | Lifetime | Dominant failure |
|---|---|---|---|---|
| **Behavior** | How should I act? | System prompt / operating contract | Session-stable | Clash — two instructions disagree |
| **Domain knowledge** | What is true? | Books, docs (declarative pages) | Durable, versioned | Poisoning, staleness |
| **Procedures** | How is it done? | Skills, recipes (how-to pages) | Durable | Incompleteness — the unlisted prerequisite |
| **Memory / state** | What have we learned? | Memory files, session notes | Evolving | Rot at write time |
| **Working context** | What is this task, now? | The window itself | Ephemeral | Distraction — volume drowning signal |
| **Actions** | What can I do? | Tool / MCP definitions | Session | Confusion — too many, too-similar tools |

The separation is a widely-recommended design rule (our framing): keep knowledge in docs, behavior in system prompts, calibration in memory — never merged — and keep declarative ("what/why") content separate from procedural ("how/steps"). The industry's layering stack (see [convergent-evolution](convergent-evolution.md)) is this same taxonomy shipped as file conventions: behavioral instructions (CLAUDE.md/AGENTS.md) → procedures (SKILL.md) → domain knowledge (OKF) → actions (MCP).

The placement test follows: take the sentence you're about to write and ask which question it answers. A "how to act" sentence in a knowledge book is behavior smuggled past review; a "what is true" claim in a system prompt is knowledge that will silently stale there. Mixed types in one home is how each type's failure mode escapes its guard. **Type the context before you place it: each of the six types has its own home, lifetime, and failure mode — and a sentence in the wrong home inherits the wrong guards.**

A well-built system gives each type its own home — behavior in a system prompt or operating contract, domain knowledge in docs and books, procedures in skills or recipes, memory in memory files, working context in the window itself, actions in tool definitions — precisely so a "how to act" line never hides inside a reference doc. This chapter is the router for the "where does this belong?" question: type first, then the type's own rules take over — [one-concept-one-home](one-concept-one-home.md) decides the *uniqueness* of the home this chapter picks the *kind* of; [four-failure-modes](four-failure-modes.md) diagnoses per-type breakage; [memory-shapes](memory-shapes.md) owns the memory row's evolution. The levers in [four-operations](four-operations.md) apply to every type, but which fires first depends on the type in hand.
