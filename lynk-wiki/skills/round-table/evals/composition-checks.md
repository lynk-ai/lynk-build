# Composition checks — transcript assertions for the position×temperament mechanism

Run against any full-flow transcript (dev harness or post-integration). Each check
is pass/fail by inspection; a failing check is a mechanism regression, not a
quality judgment. The flow is single-round: fan-out → adjudicate → ground → fold.

## Panel checks

1. **Exactly one red-team.** The opinions contain exactly one
   `temperament: red-team` — never zero, never two. (Gate 3→4 should have caught
   drift; this asserts the gate itself works.)
2. **Red-team can cite.** The red-team assignment never lands on
   product-strategist (or any position whose slice bans internal citation).
3. **No temperament repeats** within a panel.
4. **Position + temperament blocks are verbatim.** Each dispatch brief contains a
   position block (from references/positions.md) AND a temperament block (from
   panel-contracts), both matching their catalog source word-for-word — no
   invented or reworded lenses or stances.
5. **Only declared agents spawned.** Every panel Task spawns the `panelist` worker
   or the `adjudicator` — never a per-position agent name (architect, operator…),
   never the retired `skeptic`/`pragmatist`.
6. **persona == dispatched position.** Each returned `<persona_opinion>`'s
   `persona:` field equals the position injected in its brief; mismatches were
   re-dispatched or dropped (Gate 3→4).
7. **Model per position.** Each panelist Task was dispatched with the position's
   model (opus for architect/product-strategist, sonnet otherwise), not the bare
   default.
8. **Single round.** No panelist is spawned twice for the same decision; no
   revision/recap dispatches exist in the transcript.
9. **Consent honored.** On an OFFER-tier request, no panel spawn occurs without
   a visible user "yes" in the transcript; a declined offer is never re-asked on
   the same topic; SILENT-tier requests receive no offer at all.

## Orchestrator checks (the main agent gets audited too)

10. **Decisive claims were grounded** (adjudicate phase B): every file:line claim
    cited in an `adjudication:` or `discarded.reason` was checked against the
    actual file before the fold; refuted claims re-opened their issue or went to
    UNRESOLVED.
11. **Conservation of points** (adjudicate phase C): every opinion key_point and
    risk is traceable to plan/agreements/disagreements/discarded, or appears under
    Unresolved dissent in the fold, attributed to its author. No silent drops.
12. **Fold shape honored**: Recommendation · Unresolved dissent · Panel notes,
    per the panel-contracts final-fold contract; high-severity risks appear in
    the plan or in dissent, never footnoted away.
13. **No tags in field values** — all contract fields are plain text.
