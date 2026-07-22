---
name: Isolation and strict briefs
description: Heavy work runs in isolated windows; strict briefs keep blind workers from colliding; only condensed, cited results return. Read when farming heavy work out to subagents or deciding what an isolated worker should be handed.
labels: [isolation, subagents, briefs, fan-out, workers, delegation]
---

The ISOLATE lever done properly: a subagent gets a fresh context window, does heavy work there, and returns only a condensed answer — its mess never touches the parent. But isolation creates a new problem: isolated workers are blind, so what you hand them decides everything. **Isolation does the containment, compression decides what escapes it, and the brief keeps blind workers from colliding.**

In practice every isolated worker carries a complete brief up front and returns only a condensed, cited result. The fuller mechanics — call/return vs handoff, isolation's cost, the four-part strict brief, orchestrator-workers fan-out, gates and ablation — are a subagents topic in their own right. See [four-operations](four-operations.md) for where ISOLATE sits among the levers.
