---
type: principle
description: Call/return keeps the parent driving; a handoff transfers control one-way — default to call/return, reserve handoffs for work you'll never steer again.
---

# Call/return vs. handoff

**What it is** — the two ways one agent can pass work to another. **Call/return** is a function call: the parent invokes a subagent, the subagent reports back, and the parent keeps driving. A **handoff** is a `goto`: control transfers to another agent one-way, and the caller does not resume.

**Mechanics** — how the two shapes differ, grounded in the frameworks that implement them:

| | Call/return | Handoff |
|---|---|---|
| Control | Returns to the caller | Transfers away, no automatic return |
| Parent stays in charge? | Yes | No — "the new agent takes over the conversation" |
| OpenAI Agents SDK form | `Agent.as_tool(...)` | a tool the LLM calls, e.g. `transfer_to_refund_agent` |
| Default context passed | Structured input you choose | the receiving agent sees the **entire previous conversation history** |

In OpenAI's SDK, a handoff is exposed to the model *as a tool* (an agent named `Refund Agent` becomes tool `transfer_to_refund_agent`), transfer is one-way within a run, and the receiving agent sees the whole prior history by default — `input_filter` is the pruning escape hatch (source: openai.github.io/openai-agents-python/handoffs/, fetched 2026-07-07). The same docs recommend `Agent.as_tool(...)` — call/return — for "structured input for a nested specialist without transferring the conversation" (same source).

A framework nuance: in LangGraph, subagents are "stateless by design" (they start fresh each call), while **handoffs** are what persist shared state, via `Command` objects carrying `goto=agent_name` plus `update={...}` (source: docs.langchain.com/oss/python/langchain/multi-agent, fetched 2026-07-07). So "handoff" is where state travels, "call" is where it resets — the reverse of the naive intuition.

**Takeaway** — **default to call/return so the parent keeps steering; reach for a handoff only when the work is a one-way goto you'll never need to steer again.**

**Example** — real, from OpenAI's docs: a triage agent handing a refund case to a `Refund Agent` via `transfer_to_refund_agent` is a handoff — the refund agent takes over, no return. Contrast the docs' own recommended alternative, `Agent.as_tool(...)`, which invokes the specialist, gets a structured result, and hands control back to the triage agent (source: openai.github.io/openai-agents-python/handoffs/).

**In this system** — every agent here is call/return: the librarian dispatches readers and gets their findings back; the gate is invoked, renders a verdict, and *returns* it. The library skill's REJECT → revise → re-gate loop only works because the gate returns — a handoff would strand the revision with no one to re-check it. → See [isolation-is-a-decision](isolation-is-a-decision.md) for what the returning worker's window looks like, and the Best Context book · `four-operations` (ISOLATE) for where subagents sit among the levers.
