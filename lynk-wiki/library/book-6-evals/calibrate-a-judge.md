---
type: recipe
description: Validate a judge by planting known violations in known-good artifacts and scoring its catch-rate and false-alarm rate — a judge that passes everything is uncalibrated by definition.
---

# Calibrate a judge

**What it is** — the end-to-end recipe for seeded-error calibration (negative probing): before trusting a judge's verdicts, prove it catches faults you planted on purpose. The principle and its sourcing caveat live in [judge-calibration](judge-calibration.md); this page is the procedure.

**Prerequisites**
- A judge: an agent plus its rubric (the rubric's bar imported from the owning book — see [the-eval-matrix](the-eval-matrix.md)).
- A set of artifacts known to be **good** (they should pass clean).
- The ability to plant realistic violations derived from real past defects.
- A **ledger** recording, per artifact, the expected verdict (which rule it violates, or "clean").

**Steps** (one observable outcome each)
1. **Derive one violation per rule under test** from the rule set → a list of planned faults, each traced to a real past defect, exists.
2. **Plant each fault into a copy** of a known-good artifact → a set of seeded artifacts exists, one fault each.
3. **Mix seeded artifacts with clean controls** → a shuffled batch exists where the judge cannot tell seeded from clean.
4. **Run the judge blind** over the batch → a verdict per artifact is recorded.
5. **Score against the ledger** → two numbers exist: **catch rate** (seeded faults flagged) and **false-alarm rate** (clean artifacts wrongly failed).
6. **If the judge is generative, swap presentation order and re-run** → a second verdict set exists; verdicts that flip across order are downgraded to "tie" (position-bias guard, per [judge-calibration](judge-calibration.md)).

**Verification**
- Catch rate and false-alarm rate are both computed against the ledger. A judge that passes every seeded artifact is **uncalibrated by definition** — no signal. A useful judge has high catch rate *and* low false-alarm rate; either alone is a broken instrument.

**Failure modes** (symptom → fix/escape)
- **Seeded errors too obvious** — symptom: 100% catch, no discrimination; fix: derive faults from real past defects, not cartoon violations.
- **Same-model self-preference** — symptom: judge is systematically kinder to text from its own model family; fix: use a different-model judge, or ground the judge in execution (causal basis: arXiv 2404.13076).
- **Ungrounded judging** — symptom: false passes on artifacts that don't actually work; fix: give the judge commands to run — LLM4VV's bare judge hit 56.63% and the grounded judge 80.53–92.57% (source: arXiv 2408.11729 v2).

**Takeaway** — **calibrate a judge by planting known faults and scoring catch-rate against false-alarm rate — a judge that never fails anything has proven nothing.**

**Example** *(real)* — our gate's smoke test: 2 violations planted into draft artifacts, the gate caught 2/2 and flagged 1 real bonus defect it wasn't told about (source: git 7ab2826). That is this recipe run once — before the practice had a name in our library.

**In this system** — this recipe is how any new library judge (a new gate check, a panel member) earns trust before it rules on real drafts. → See [judge-calibration](judge-calibration.md) for the biases this measures, and the Subagents book · `gates-and-ablation` for the gate as the judge under calibration.
