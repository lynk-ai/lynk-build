---
type: principle
description: A verification is only as trustworthy as the surface it runs on; static and proxy checks are necessary but not sufficient, and a green proxy over a red authoritative surface is false green — choose the authoritative surface first, then trust the tool.
---

# Verify at the authoritative surface

**What it is** — the precondition beneath every eval: before you trust a check, ask *what surface did it run on?* A verification observes an artifact through some surface — a static parse, a proxy engine, or the real place the artifact is consumed. Only one of these is the **authoritative surface**: the surface where the artifact actually does its job (compiles, is consumed, ships). A check is only as trustworthy as the surface it runs on, and a tool pointed at the wrong surface is *worse than none* — a failing artifact tells you nothing, but a false green manufactures confidence (our call).

**Mechanics** — surfaces form a ladder of authority for any given claim:

| Surface | Checks | Blind to |
|---|---|---|
| **Static / structural** | references resolve, names and types match | anything that only appears under execution — cycles, compile errors |
| **Proxy engine** | the logic/numbers against a stand-in (e.g. the raw warehouse instead of the compiled layer) | the real engine's compile and consumption semantics |
| **Authoritative (consumption / compile)** | the artifact exactly as it is consumed | — this is the truth surface |

Static and proxy checks are **necessary but not sufficient**: they can pass GREEN while the authoritative surface is RED. That combination — green below, red at the authority — is **false green**. The failure it hides is invisible *by construction*: the lower surface cannot see it, so more careful lower-surface checking never finds it. The fix is not a better proxy; it is choosing the right surface. The routing rule: **identify where the artifact is actually consumed, point the tool there first, and only then trust its verdict** (our call, generalizing execution grounding — see below).

Execution grounding is this principle's most-measured special case: for code, the authoritative surface is compile/run, and grounding a judge there more than doubled its accuracy (→ the LLM4VV numbers live in [judge-calibration](judge-calibration.md)). This page owns the general principle; `judge-calibration` owns execution grounding as one *judge* bias-fix; `run-a-baseline-delta` requires it as a *recipe* prerequisite.

**Takeaway** — **a check is only as trustworthy as the surface it runs on — a green proxy over a red authority is false green, so choose the authoritative surface first and trust the tool second.**

**Example** *(real — Lynk semantic-layer audit incident, 2026-07-12)* — an audit verified a semantic layer on two lower surfaces and declared it clean: static structure passed (every reference resolved, names matched) *and* the numbers ran green against the raw warehouse. But the authoritative surface — the Lynk build that compiles the layer and probes every field at the consumption layer — FAILED. Two entities referenced each other in a cycle (`player_game.team_minutes_in_game` → `team_game.team_minutes_played` → `metric(player_game.total_minutes_played)`), so neither entity compiled ("CTE does not exist") and dozens of field probes failed as downstream metrics cascaded to "metric not found." Neither static resolution nor raw-warehouse queries could see any of it: the audit's grounder used a *proxy* surface (raw tables) instead of the *consumption* surface (the compiled layer), producing false green on a layer that was in fact broken (source: `docs/semantic-layer-build-cycle-2026-07-12.md`).

**In this system** — our gate is a judge that runs on the authoritative surface by design: it invokes `bk lint` and (in the Book 4 consumption eval) verified claims against the *live* `bk` CLI, not a mock — which is exactly how its round-2 judge caught a gap the static round-1 judge could not (source: `docs/book-4-consumption-eval-2026-07-08.md`). A gate that checked drafts against a stand-in instead of the real substrate would be false green about its own library. → See the Subagents book · `gates-and-ablation`: a gate at a handoff earns trust only when it checks the authoritative surface, not a static or proxy one. → See [judge-calibration](judge-calibration.md) for execution grounding as the judge-specific lever, [run-a-baseline-delta](run-a-baseline-delta.md) for it as a recipe prerequisite, and [the-eval-matrix](the-eval-matrix.md) for where every mechanism sits — this principle is the precondition on all of them.
