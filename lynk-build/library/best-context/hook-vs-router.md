---
type: principle
description: Hooks fire themselves and skip silently; routers are explicit and fail closed — hooks raise the floor, the router guards the door.
---

# Hook vs. router

**What it is** — the two ways to make something run automatically, distinguished by one question: *who is responsible for it running?* A **hook** is an event listener — nobody invokes it; it watches, fires on a match, and if nothing matches, nothing happens and nothing tells you. A **router** is a dispatcher standing *in* the control flow — everything passes through it, it decides what happens next, and it can refuse.

**Mechanics**

| | Hook | Router |
|---|---|---|
| Mental model | Git hook, DB trigger | API gateway, switch with no default case |
| Trigger | Implicit, pattern-matched | Explicit, deliberately called |
| On failure | **Skips silently** | **Halts / blocks** |
| Build cost | Cheap | Costlier |
| Best for | The floor — defaults that help when they fire, cost nothing when they don't | Any transition where a silent skip would be a bug |

They're layers, not rivals — and the multiplier is **hooks feed the router**: hooks observe and annotate cheaply on every step; by the time work reaches the gate, the router rules on evidence the hooks already collected.

**Takeaway** — **hooks raise the floor, the router guards the door: cheap observation on every step, one fail-closed decision at the chokepoint.**

**Example** — CandleKeep, both shapes in one product: a SessionStart hook injects "you MUST check the library" (and if the agent ignores it, nothing notices — hook), while its librarian explicitly dispatches to books and can refuse "no book covers this" (router). Its one real gap: the *writing* path has no router at all — the writer uploads unverified.

**In this system** — the sticky-note hook is the floor; **the gate is the router**, and it exists precisely because everything downstream trusts gate-passed books blindly — that door cannot be a listener that might not fire. → See [context-governance](context-governance.md) for who owns the door, and Book 2's rules for what the gate actually checks.
