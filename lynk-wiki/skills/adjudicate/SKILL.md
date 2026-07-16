---
name: adjudicate
description: Adjudicates a set of structured expert opinions into one committed plan with attributed disagreement, grounds the decisive claims, and folds the result. Invoked by /round-table as phase two of the roundtable; also usable standalone on any set of contract-shaped <persona_opinion> blocks ("adjudicate these opinions", "merge these expert reviews"). NOT for merging free-text documents, meeting notes, or opinions that don't follow the panel contract — reject those with a pointer to panel-contracts rather than guessing at structure.
---

# Adjudicate — shuffle, judge, ground, fold, stop

**What it is:** phase two of the roundtable. Takes a decision plus ≥2 contract-shaped
`<persona_opinion>` blocks, dispatches the calibrated judge, verifies the claims
that decided the synthesis, and delivers a single folded plan with unresolved
dissent surfaced. Single-round by design: opinions are collected once and judged
once — there is no revision pass, which is why the grounding and conservation
checks below are not optional.

**Takeaway:** the judge adjudicates, never blends — and because no second round
exists to catch its mistakes, every claim that decided an adjudication gets
verified against the actual files before the fold.

## Input contract

- The decision (one paragraph) and ≥2 `<persona_opinion>` blocks (shapes in the
  panel-contracts skill).
- Optional: the roster used, for the Panel notes section.
- If the inputs aren't contract-shaped: stop and say so, pointing to
  panel-contracts. Do not guess structure out of free text.

## Phases

- **A · Shuffle + judge** — randomize the opinions' order (never roster order,
  never arrival order), truncate any opinion over its 350-word budget, then
  dispatch ONE `adjudicator` agent with: the decision, the shuffled opinions, and
  the full text of `references/synthesis-rubric.md`.
  **Gate A→B:** the return parses as `<panel_synthesis>`; every disagreement is
  persona-attributed with a rubric-criterion-cited adjudication or marked
  UNRESOLVED. A synthesis that blends without attribution gets exactly ONE
  re-dispatch with the violation named; a second failure fails closed — report
  the raw disagreements to the user instead of a bad synthesis.
- **B · Ground the decisive claims** — from the `<panel_synthesis>`, list every
  file:line claim that DECIDED an adjudication or a discard (not every citation —
  only the load-bearing ones). Verify each with a direct look (Read/grep the
  cited line). A refuted claim re-opens exactly that adjudication: re-dispatch
  the adjudicator once with the refutation attached, or downgrade the issue to
  UNRESOLVED. The judge sees only the payload by design — this pass is the only
  thing standing between a confident wrong citation and the final plan.
  (Pattern borrowed from semantic-layer-audit's execution-grounding.)
- **C · Conservation of points** — trace every panelist key_point and risk into
  the synthesis: each must appear in `plan`, `agreements`, `disagreements`, or
  `discarded`. Anything untraced is an OMISSION the judge never saw — list it
  under **Unresolved dissent** in the fold, attributed to its author. Never drop
  a panelist's point silently.
- **D · Fold, then STOP** — deliver ONE artifact in the final-fold shape from
  panel-contracts: Recommendation (the plan, post-grounding) · Unresolved dissent
  (UNRESOLVED adjudications + grounding refutations + untraced points, all
  persona-attributed) · Panel notes (roster, drops, confidence, and any
  would_change_my_mind conditions worth the reader's attention). The fold is
  advisory — never apply the plan.

## Guardrails — operating contract (never overridden)

- **One round only** — opinions are never sent back to their authors for
  revision; dissent is surfaced, not re-debated.
- **Shuffle before judging** — opinions never reach the adjudicator in a
  meaningful order.
- **Adjudicate, don't blend** — enforced by Gate A→B, fail closed.
- **Ground before folding** — a plan step resting on an unverified decisive
  claim doesn't ship; verify it or mark the issue UNRESOLVED.
- **Typed returns only** — free prose from any agent is not folded.
- **Advisory output** — this skill never edits files or applies the plan.
- **Zero disagreement across 3+ personas is suspect** — say so in Panel notes.

## Fallback — subagents can't spawn

Do phase A inline: apply the rubric yourself, criterion by criterion, and produce
the `<panel_synthesis>` block. Phases B–D run inline as normal (they are
orchestrator work anyway). Don't retry spawning.

## Common mistakes

- Dispatching the adjudicator with opinions in roster order — always shuffle.
- Skipping the grounding pass because the citations "look plausible" — plausible
  wrong citations deciding a plan is the exact failure this phase exists for.
- Softening a high-severity risk into a footnote — it goes in the plan or in
  Unresolved dissent, nothing in between.
- Sending opinions back to panelists for another round — single-round is a
  design decision (cost); omissions go to Unresolved dissent instead.
