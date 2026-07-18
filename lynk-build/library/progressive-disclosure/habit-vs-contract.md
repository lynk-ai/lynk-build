---
type: principle
description: The opinion of the book — reading one page at a time is a habit nothing enforces; a fixed-stage protocol backed by an honest index and a gate is a contract, and only a contract makes routing safe.
---

# Habit vs. contract

**What it is** — the distinction that separates a nice property from a product guarantee. A well-behaved agent that reads one page at a time is running a *habit*: nothing stops it from reading the whole folder, and the moment it does, the economics of [the-economics](the-economics.md) collapse. A *contract* is an enforced protocol with fixed stages — the agent routes through an index it is required to trust, and something keeps that index honest. The gap between the two is the whole reason this book exists.

**Mechanics** — what turns the habit into a contract:

| | Habit | Contract |
|---|---|---|
| Who guarantees the stages | Nobody — the agent's good behavior | An enforced protocol |
| The index | Convenient, may be stale | Kept honest by a gate |
| On drift | Silently degrades; nobody notices | Change is rejected until the index matches |
| Safe to build a product on? | No | Yes |

The framing comes from the context-engineering talk (§B, docs/talk-outline.md): the LLM Wiki has progressive disclosure as a *habit* — a convention agents follow; Anthropic's Agent Skills has it as a *contract* — a protocol the runtime enforces. The design goal that follows is a "wiki-format-with-a-contract": the readable markdown shape of the wiki, plus the enforcement of Skills (source: talk §B).

**Takeaway** — **you can't build a product on a habit — enforcement is what turns polite routing into safe routing.**

**Example (constructed)** — an index that silently forgets a page. Under a habit, agents route by that index and the forgotten page effectively vanishes, with no error anywhere. Under a contract, the change that added the page without indexing it is *rejected* — the index cannot lie, so routing by it stays safe (source: index-and-changelog gate rule).

**In this system** — the gate is the enforcer: it rejects any change that touches a page but not its index (the Book Standard · `index-and-changelog`), so the discovery layer is a contract, not a courtesy. This is the fail-closed half of the Best Context book · `hook-vs-router`: hooks raise the floor, but a contract must guard the door. → See [three-stages](three-stages.md) for the stages a contract fixes in place.
