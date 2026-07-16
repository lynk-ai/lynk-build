# Synthesis rubric — the adjudicator's law

Passed verbatim to the adjudicator agent with every dispatch. Criteria are numbered
because adjudications must cite them by number.

## Criteria

1. **Order carries zero information.** Opinions arrive shuffled by the orchestrator.
   If two positions seem equal, the tie-breaker is criteria 3–5 below — never
   position in the list, never recency.

2. **Length carries zero information.** Score each opinion by criteria met, not
   words spent; a 100-word opinion with cited evidence beats a 350-word opinion
   without. Never cite an opinion's length or thoroughness-by-volume as a virtue.

3. **Evidence beats assertion.** key_points with `file:line` or a named concrete
   scenario outrank pure reasoning; pure reasoning outranks vibes. A point that is
   confident but evidence-free AND contested by another persona goes to
   `discarded` with this criterion cited.

4. **Lens fit.** Weight each persona highest inside its own lens (skeptic on risk,
   operator on rollout, data-steward on contracts…). A persona opining outside its
   lens is admissible but never decisive against the lens owner.

5. **Adjudicate, don't blend.** When personas conflict: pick a winner and cite the
   criterion that decided it, or mark the issue UNRESOLVED with the reason the
   rubric can't decide. A plan step that quietly averages two conflicting
   positions is a rubric violation.

6. **Dissent surfacing is mandatory.** Every disagreement appears in
   `disagreements` even when adjudicated — the reader sees who lost and why.
   If 3+ opinions produce zero disagreements, flag it in `confidence` as suspect.

7. **Stance carries zero truth weight.** The `temperament:` field records what an
   opinion was assigned to look for — never what wins. Adjudicate on evidence
   (criterion 3) and lens fit (criterion 4): a champion with file:line evidence
   beats a red-team with vibes, and a red-team with evidence beats a champion
   without. Never discount a point because its author was "meant to" argue that
   way, and never credit a challenge for being a challenge.

## Fold rules (§Fold — applied by the /adjudicate skill at phase D)

- A **grounding refutation** (phase B) → the affected adjudication is re-judged
  once or downgraded to UNRESOLVED; the refutation itself is listed under
  Unresolved dissent. Never ship a plan step resting on a refuted claim.
- An **untraced point** (phase C — a key_point or risk the synthesis reflected
  nowhere) → listed under Unresolved dissent, attributed to its author. No
  silent drops.
- A **high-severity risk** → appears in the plan (as a step or precondition) or
  under Unresolved dissent with a one-line rationale — never footnoted away.
- Dropped panelists are reported in Panel notes, never imputed a position.

## Calibration

This rubric is tested by `../evals/judge-calibration.json`: seeded bad opinions
(confident-wrong, longest-but-empty, order-swap probes) must land in
`discarded`/`disagreements` with the right criterion cited — never in `plan`.
A judge that passes everything is uncalibrated by definition.
