---
type: principle
description: Poisoning, distraction, confusion, clash — four distinct ways context breaks an agent; mixing them up means applying the wrong fix.
---

# The four failure modes

**What it is** — four distinct ways context breaks an agent. They present as the same symptom ("this feels off"), but each has a different cause and a different fix — mixing them up means applying the wrong one.

**Mechanics**

| Failure mode | Trigger | Fix |
|---|---|---|
| **Poisoning** | A wrong fact gets repeated back into context; the model treats it as truth. | Verify before writing to persistent memory. |
| **Distraction** | History piles up unpruned; the model rehashes instead of reasoning fresh. | Summarize — don't just accumulate. |
| **Confusion** | Irrelevant (not wrong) context is present; output degrades anyway. | Curate harder — don't include "everything that might matter." |
| **Clash** | Two pieces of context disagree; the model can't tell which is true. | Flag it and escalate to a human — never let the agent silently pick a side. |

Note the asymmetry: three modes have mechanical fixes; **clash** alone requires an authority decision — an agent may *notice* a contradiction, but it has no standing to *resolve* one.

**Takeaway** — **same symptom, four different causes — diagnose before you fix.**

**Example** *(constructed, illustrative)* — one code-review agent, mid-project, all four: it keeps recommending a caching pattern from a PR that was reverted weeks ago (*poisoning*); its suggestions get vaguer as conversation history balloons (*distraction*); pasting the full lint output beside the diff makes it miss the actual bug (*confusion*); the style guide and the linter config disagree and it flags both (*clash*). Four bugs, four fixes — none of them is "just give it more/less context."

**In this system** — each mode has a named guard: the Book Standard · `supersede-dont-delete` makes poisoning *diagnosable*; changelogs + page reads (never whole books) starve distraction; the Book Standard · `toc-discipline` + honest indexes prevent confusion; [one-concept-one-home](one-concept-one-home.md) prevents clash structurally, and the gate escalates the rest to the human merge. → See [context-governance](context-governance.md) for *whose job* catching these is.
