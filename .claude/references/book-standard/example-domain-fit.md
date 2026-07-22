---
type: rule
description: An example's domain matches the book's declared scope — a domain book draws examples from its domain, a general/method book uses domain-neutral examples; the writer picks the mode from the book's scope.
load_when: Choosing the worked example for a chapter — deciding whether it should be domain-specific or domain-neutral.
keywords: [examples, domain, general, domain-neutral, domain-specific, reusable, declared scope, both modes, generality]
rules:
  - id: quality/example-domain-fit
    severity: warn
    scope: chapter
    statement: An illustrative example's subject domain must fall within the book's declared scope — a domain-scoped book uses that domain's examples; a general or method book uses domain-neutral (or deliberately rotating) examples, never a single incidental outside domain.
    gate_criteria: >
      Judged against the book's declared scope (its index description). A book
      whose subject IS a domain passes by drawing examples from that domain —
      concrete and on-subject. A general or method book passes when its examples
      are domain-neutral, or deliberately rotate domains, so no single incidental
      domain makes the method read as domain-specific. It warns when a
      general/method book leans on one outside domain throughout (e.g. sports
      statistics across a data-modeling method), or when a domain book
      illustrates with off-domain examples that never exercise its subject.
      "Neutral" means domain-agnostic, not vague: the example stays concrete and
      falsifiable (quality/examples-labeled) — swap the domain, keep the numbers
      and the mechanism. Real, cited examples that ARE the book's subject
      (benchmarks in an evals book, frameworks in a multi-agent book) count as
      in-domain and pass. The writer sets the mode when the book is created, from
      its declared scope; severity is warn because domain-fit is a judgment the
      gate flags rather than mechanically rejects.
---

# Example domain fit

**What it is** — the rule that an example's *domain* is a deliberate choice, set by the book's scope, not an accident of whatever was handy. A book is either scoped to a domain or it is a general method — and its examples must match. A general method illustrated entirely in one incidental domain reads as a book *about* that domain; a domain book illustrated with off-domain examples never shows its own subject working. Neither serves the reader who arrives from a different place.

**Mechanics** — the mode follows the book's declared scope (its index description):

| The book is… | Examples should be… | The smell |
|---|---|---|
| Scoped to a domain (its subject IS that domain) | drawn from that domain — concrete, on-subject | off-domain examples that never exercise the subject |
| A general method / cross-cutting principle | domain-neutral, or deliberately rotating domains | one incidental domain used throughout, so the method reads as domain-specific |

Two clarifications keep this from being misapplied. **Neutral is not vague** — a domain-neutral example is still concrete and falsifiable ([sourced-statements](sourced-statements.md)): you swap the domain, but you keep the numbers and the mechanism. And **real, cited examples that ARE the subject count as in-domain** — benchmark citations in a book about evaluation, framework citations in a book about multi-agent systems, are on-subject evidence, not an incidental domain to strip.

The test, in one question: does the example's subject fall inside the book's declared scope? If a general book's example could be lifted into a reader's unrelated field unchanged, it is neutral enough; if understanding it first requires knowing an outside domain the book is not about, re-cast it.

**Takeaway** — **pick the example's domain to match the book's scope — in-domain for a domain book, domain-neutral but still concrete for a general one — a choice made when the book is created, not left to whatever example was nearest.**

**Example** *(constructed, illustrative)* — a general method chapter on averaged-ratio bugs illustrated only with basketball shooting percentages reads as a sports-analytics chapter. Re-cast to a neutral metric — a conversion rate that is 36.5% as `SUM(conversions)/SUM(visits)` but 30.5% as the mean of per-day rates — the same mechanism and the same numbers now land for a reader in any field. A book whose declared subject *were* basketball analytics would keep the shooting-percentage version, and would be right to.

**In this system** — a gate check (quality dimension): the verifier reads each example against the book's declared scope and warns on an incidental-domain mismatch. It is the example-side companion of [write-for-the-shelf](write-for-the-shelf.md) — that rule asks whether a *referent* resolves for the reader; this one asks whether the *example's domain* fits the book the reader is holding. → See [sourced-statements](sourced-statements.md) for the concreteness bar a neutral example must still clear.
