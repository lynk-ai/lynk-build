---
type: principle
description: Agent-written and human-written knowledge are the same artifact before and after review — the agent proposes, the merge makes it truth.
---

# Self-compiled vs. externally curated

**What it is** — the two ways knowledge gets made. **Self-compiled:** an agent writes it from what it observed or derived. **Externally curated:** a human authored and reviewed it. The insight is that these aren't rival systems — they're *the same artifact at two stages*: a self-compiled draft becomes curated truth by passing review. Same shape as a pull request: proposed by the agent, merged by a human.

**Mechanics**

| Stage | Who wrote it | Trust level | What moves it forward |
|---|---|---|---|
| Draft | The agent | A working opinion — private, per [one-concept-one-home](one-concept-one-home.md) | Submission to review |
| Reviewed | Same content, now checked | Shared truth — readers may rely on it blindly | The merge |

Why the merge must be human *for foundational knowledge*: readers downstream trust the shared layer without re-checking it. An agent can verify structure and consistency (a gate does exactly that), but the *authority* to declare something true carries liability no agent holds. The more blindly a layer is trusted, the more human its door must be.

The gradient that follows: routine content → agent-gated (the gate verifies against the standard); the standard itself → human-gated (amendments to the constitution are always a human merge). Gate the door in proportion to the blast radius of a wrong merge.

**Takeaway** — **self-compiled and externally-curated aren't rivals — the same artifact before and after review; the agent proposes, the merge is what makes it truth.**

**Example** *(constructed, illustrative)* — an agent notices a naming convention in a codebase and drafts a note about it. As a draft, it's a useful guess. Merged after a maintainer confirms it, it's a rule other agents may follow blindly. Same words, same file — the review is the only thing that changed, and it changed everything.

**In this system** — the bootstrap ran on this exact principle: the two meta-books were written by us and human-merged (curated) because the system that could gate them didn't exist yet. Every Book N after is self-compiled + gate-checked; amendments to Books 1–2 are proposed by maintenance and merged only by the human. → See [hook-vs-router](hook-vs-router.md) — the gate is the router this principle demands.
