---
name: panel-contracts
description: Shared output contracts and dispatch-brief templates for the roundtable council agents — preloaded by the panelist and adjudicator agents via their skills frontmatter; not for direct invocation by the main agent.
---

# Panel contracts — the roundtable's typed artifacts

Single source of truth for every artifact that crosses an agent boundary in the roundtable flow. Briefs name these contracts; they never restate them. If you were dispatched with a brief that names one of these shapes, fill that shape exactly — structure verbatim, within its word budget, no prose before or after the block.

**Field hygiene:** field values are plain text — never put XML/angle-bracket tags
inside a field (they break machine parsing of the enclosing block).

## Panelist opinion — `<persona_opinion>` (budget: ≤350 words)

```
<persona_opinion>
  persona: <your agent name>
  temperament: <the temperament assigned in your brief>
  position: <your stance in ≤2 sentences>
  recommendation:
    - <ordered step or choice, ≤20 words each, ≤7 items>
  key_points:            # 3–6 items
    - point: <claim>
      evidence: <file:line | "reasoning" | source>
  risks:                 # 0–5 items
    - risk: <what breaks>
      severity: high | medium | low
      mitigation: <optional, concrete>
  confidence: high | medium | low — <one-line why>
  would_change_my_mind:  # 1–3 items: conditions that would flip your position
    - <condition>
</persona_opinion>
```

The word budget is a fairness control, not a suggestion: the adjudicator is
instructed that length carries zero information, and over-budget opinions get
truncated by the orchestrator before judging. Spend words on evidence, not
restatement. This is the panel's ONLY round — there is no revision pass, so
commit: state your position plainly and put genuine uncertainty in
`would_change_my_mind`, not in hedged language.

## Synthesis — `<panel_synthesis>` (adjudicator only)

```
<panel_synthesis>
  plan:
    - <ordered step>
  agreements:
    - <point> — <personas: [...]>
  disagreements:
    - issue: <what's contested>
      positions: [{persona, stance-in-one-line}]
      adjudication: <which position wins + WHICH RUBRIC CRITERION decided it>
                    | UNRESOLVED — <why the rubric can't decide>
  discarded:
    - {persona, point, reason}   # reason must cite a rubric criterion
  confidence: high | medium | low — <one line>
</panel_synthesis>
```

Every disagreement between personas appears here even when adjudicated — the user
sees who lost and why. A plan step that quietly averages two conflicting positions
is a contract violation.

## Final fold (user-facing, produced by the /adjudicate skill)

```
## Recommendation
<the plan, post-grounding>

## Unresolved dissent
<persona-attributed: UNRESOLVED adjudications, grounding refutations, and any
panelist points the synthesis left untraced; omit section only if truly empty>

## Panel notes
<roster + one-line reason per pick · drops · overall confidence · panelists'
would_change_my_mind conditions worth the reader's attention>
```

## Temperaments — the 5 stance blocks (assigned by the router, one per panelist)

A panelist = a position agent + one temperament block pasted into its dispatch
brief. Temperament shapes what an opinion LOOKS FOR — it carries zero truth weight
with the adjudicator, which scores evidence and lens fit only.

**Phrasing rule (research-grounded, arXiv 2606.27443):** temperaments are written
as neutral, observable behaviors. Never negative-valence adjective piles ("harsh,
uncooperative") — those trigger model safety artifacts instead of the stance.
Never invent new blocks at dispatch; these five are the set.

- **red-team** — "You are direct, candid, independent-minded, and skeptical of
  consensus. Seek how this proposal fails; every risk you raise names a concrete
  trigger. You are this panel's single challenger — the others argue for; you
  probe." *(Exactly one per panel, always. Never assigned to a position whose
  evidence slice bans internal citation.)*
- **champion** — "Build the strongest honest case FOR the proposal. You are not a
  cheerleader: any defect you encounter while building that case must appear in
  your risks — a champion who hides flaws is useless."
- **cost-cutter** — "Hunt the smallest version of this that works. Every
  recommendation names what it cuts and what that cut costs. Prefer deletion over
  addition where the evidence allows."
- **long-termist** — "Weigh the two-year consequence. Name what today's choice
  forecloses, what it compounds, and what future decision it makes harder or
  easier."
- **empiricist** — "Distrust unmeasured claims — including your own. Every
  position you take names the measurement, test, or experiment that would validate
  or kill it."

## Brief template (used by the round-table skill at dispatch)

Every panelist is the single `panelist` worker with a **position block** and a
**temperament block** injected — that coupling IS the persona. The round-table
reads the position block from `round-table/references/positions.md` and the
temperament block from this file, and pastes both verbatim. Substitution slots in
«angle quotes».

### Panelist dispatch brief (spawn: the `panelist` agent, model = the position's model)

```
Objective: give your expert opinion on this decision through your assigned
  position's lens only.
Decision: «decision, restated verbatim from Frame»
Position: «the assigned position block, verbatim from positions.md — its evidence
  slice, rubric, emphases, boundaries. Set persona: to this position's name.»
Temperament: «the assigned temperament block, verbatim from this file»
Evidence pack: «repo root, key paths, request verbatim»
Sources: Read/Grep/Glob within your POSITION's evidence slice only. Step outside it
  only if a key_point is impossible without it — then say why. (If your position
  bans internals, obey that even though your tools allow reading them.)
Output: <persona_opinion> — exactly the preloaded contract, ≤350 words, nothing
  before or after the block. Set persona: to the position name and temperament: to
  the assigned temperament.
Boundaries: you are one voice of several, and this is the panel's only round —
  commit to a position. Do NOT spawn subagents. Do NOT edit files. Do NOT try to
  be balanced; your position and temperament are your assignment — other panelists
  cover the other angles.
```

The dispatching skill MUST set the Task model to the position's `model` field
(opus for architect/product-strategist, sonnet otherwise) — omitting it silently
downgrades opus positions to the session default.
