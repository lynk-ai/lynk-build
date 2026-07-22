---
name: The four failure modes
description: Poisoning, distraction, confusion, clash — four distinct ways context breaks an agent; mixing them up means applying the wrong fix. Read when an agent's output feels off and you need to identify which context failure is causing it before picking a fix.
---

There are four distinct ways context breaks an agent, a taxonomy named by Drew Breunig (*How Long Contexts Fail*, 2025). They present as the same symptom ("this feels off"), but each has a different cause and a different fix — mixing them up means applying the wrong one.

| Failure mode | Trigger | Fix |
|---|---|---|
| **Poisoning** | A wrong fact gets repeated back into context; the model treats it as truth. | Verify before writing to persistent memory. |
| **Distraction** | History piles up unpruned; the model rehashes instead of reasoning fresh. | Summarize — don't just accumulate. |
| **Confusion** | Irrelevant (not wrong) context is present; output degrades anyway. | Curate harder — don't include "everything that might matter." |
| **Clash** | Two pieces of context disagree; the model can't tell which is true. | Flag it and escalate to a human — never let the agent silently pick a side. |

Note the asymmetry: three modes have mechanical fixes, but clash alone requires an authority decision — an agent may *notice* a contradiction, but it has no standing to *resolve* one. **Same symptom, four different causes — diagnose before you fix.**

The four are real, not hypothetical. Breunig documents them (citing Google's Gemini 2.5 report): a Pokémon-playing agent whose poisoned goals section drove it to "nonsensical strategies" repeated in pursuit of an unreachable goal (poisoning); the same agent, past ~100k tokens, favoring repeats of actions from its vast history over synthesizing new plans (distraction); third-party MCP tool descriptions conflicting with the rest of the prompt (clash). One constructed composite (illustrative) covers the last: a code-review agent pasting full lint output beside the diff misses the actual bug (confusion). Four bugs, four fixes — none of them is "just give it more/less context."

Each mode has a natural guard: never let an unverified fact reach persistent memory (poisoning); summarize and prune rather than accumulate (distraction); keep labels honest, so a name and description promise exactly what the body delivers (confusion); give every fact one home so two copies can't disagree ([one-concept-one-home](one-concept-one-home.md), clash) — and a clash that still surfaces is escalated to a human, never silently resolved. See [context-governance](context-governance.md) for whose job catching these is, and [why-context-rots](why-context-rots.md) for the measured evidence behind distraction and confusion.
