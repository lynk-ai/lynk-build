---
type: principle
description: A rule without an eval is a wish; Book 2's rules frontmatter is already a machine-readable eval spec, and the coverage matrix tracks which prescriptions actually have a live instrument.
---

# Every rule is an eval

**What it is** — the thesis of this book: **a rule without an eval is a wish.** A prescription nobody measures is indistinguishable from one nobody follows. This page also draws the third distinction (orthogonal to the [eval matrix](the-eval-matrix.md)'s dimension×mechanism): what an eval is *about*.

**Mechanics** — three kinds, and the ledger that tracks them:

| Kind | Question | Example here |
|---|---|---|
| **Artifact** | Is the thing good? | Does this page pass Book 2's checklists? |
| **Adherence** | Was the process followed? | Did the writer read the constitution first? ([instrument-adherence](instrument-adherence.md)) |
| **Coverage** | What fraction of prescriptions have a live eval? | The matrix below. |

Rules here are already machine-readable eval specs. Book 2's `rules:` frontmatter carries, per rule: `statement` (the brief for the writer), `gate_criteria` (the spec for the verifier), `severity`, and `scope` — a specification an evaluator can execute (source: any Book 2 page, e.g. `sourced-statements`). `bk` has a dormant `REGISTRY_ENFORCED` flag (currently `False`, "flips to True once the Phase 1 rule-registry merges" — source: `bk`, `REGISTRY_ENFORCED` (line 51)) that will require every `rule`/`template` page to carry this block.

The **coverage matrix** (claim → owning book → instrument → status) is taught here as a pattern; the live matrix will be generated tooling, not a hand-maintained page here. An honest snapshot (2026-07-08):

| Prescription | Owning book | Instrument | Status |
|---|---|---|---|
| draft passes the standard | Book 2 | the gate, `bk lint` | **running** |
| gate catches seeded violations | Book 2 | seeded-error calibration | ran once (git 7ab2826) |
| constitution shapes drafts | Book 1 | blind-arm spike | ran once (git a8fc53c) |
| Book 4 improves skill-building | Book 4 | baseline delta | ran once (`docs/book-4-consumption-eval-2026-07-08.md`) |
| our own skills trigger correctly | Book 4 | trigger evals | defined, not run |
| writers read the constitution first | Book 1 | adherence over `.bk/reads/` | **telemetry collected, not computed** |
| understanding / faithfulness, economics curve | various | — | missing |

Note: `.bk/reads/<session>.jsonl` is already-collected adherence telemetry — the instrument's raw feed exists before the eval does (source: `bk` startup banner; files present in-repo).

**Takeaway** — **a rule you don't measure is a wish; the coverage matrix names, per claim, which book owns the bar and whether any instrument actually checks it.**

**Example** *(real)* — the "gate catches seeded violations" row: the smoke test planted 2 violations, the gate caught 2/2 plus 1 real bonus defect, recorded at git 7ab2826 — a coverage cell that moved from *missing* to *ran once* the day that commit landed (source: git log, commit 7ab2826).

**In this system** — this page is why the book exists: it turns the library's own rules into things that can be checked, and the matrix is the to-do list of evals still to build. → See [the-eval-matrix](the-eval-matrix.md) for the dimension×mechanism axis, and [instrument-adherence](instrument-adherence.md) for the adherence kind as a recipe.
