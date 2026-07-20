---
name: Hook vs. router
description: Hooks fire themselves and skip silently; routers are explicit and fail closed — hooks raise the floor, the router guards the door. Read when choosing how to make something run automatically — a self-firing hook or an explicit fail-closed checkpoint — or a silent skip just bit you.
labels: [hooks, gates, enforcement, fail-closed, automation, router, silent failure]
---

There are two ways to make something run automatically, distinguished by one question: *who is responsible for it running?* A hook is an event listener — nobody invokes it; it watches, fires on a match, and if nothing matches, nothing happens and nothing tells you. A router is a dispatcher standing *in* the control flow — everything passes through it, it decides what happens next, and it can refuse.

| | Hook | Router |
|---|---|---|
| Mental model | Git hook, DB trigger | API gateway, switch with no default case |
| Trigger | Implicit, pattern-matched | Explicit, deliberately called |
| On failure | **Skips silently** | **Halts / blocks** |
| Build cost | Cheap | Costlier |
| Best for | The floor — defaults that help when they fire, cost nothing when they don't | Any transition where a silent skip would be a bug |

They're layers, not rivals, and the multiplier is that hooks feed the router: hooks observe and annotate cheaply on every step, so by the time work reaches the chokepoint the router rules on evidence the hooks already collected. **Hooks raise the floor, the router guards the door: cheap observation on every step, one fail-closed decision at the chokepoint.**

Many systems run both shapes at once: a session-start hook injects a reminder ("check the knowledge base first") and if the agent ignores it nothing notices — a hook — while a dispatcher explicitly routes each request to a handler and can refuse "nothing covers this" — a router. A common gap is a write path with no router at all: content gets published unverified because nothing stands in the doorway.

The pattern generalizes: cheap self-firing hooks raise the floor on every step — a session-start injection, lightweight annotations, help that costs nothing when it doesn't fire — while a router guards any transition where a silent skip would be a bug. The strongest case for a router is a gate that trusted output passes through: when downstream readers rely on that output blindly, the door cannot be a listener that might not fire. See [context-governance](context-governance.md) for who owns the door.
