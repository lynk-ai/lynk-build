---
type: rule
description: Never delete content — add a dated supersede note; history is diagnostic evidence.
load_when: Correcting, reversing, or removing existing book content — what must remain and how to mark it.
keywords: [supersede, delete, corrections, history, evidence, dated notes]
rules:
  - id: quality/supersede-not-delete
    severity: error
    scope: book
    statement: Corrections keep the old text and add a dated supersede note — deletion destroys diagnostic evidence.
    gate_criteria: >
      An edit passes when content it invalidates remains readable next to a dated
      note in the form '(superseded YYYY-MM-DD: correction)', with large
      corrections also logged in log.md. It fails when the diff removes or
      reverses substantive lines without a supersede note. Exceptions: typo and
      formatting fixes that do not change meaning, mechanical regeneration of
      derived files (a generated index), and edits within a draft that has never
      passed the gate — history protection begins at first promotion.
---

# Supersede, don't delete

**What it is** — the rule for correcting a book: wrong or outdated content is never removed, it's *superseded* — the old text stays, a dated note marks what replaced it and why.

**Mechanics**

Format, inline where the old claim lives:

```markdown
Orders join to Customers via `customer_key`.
*(superseded 2026-07-06: the join moved to `customer_id` in the v4 schema — see log.md)*
```

| Rule | Why |
|---|---|
| The correction is dated | "When did we learn this?" is often the question that matters. |
| The old text stays readable | Diagnosing *poisoning* requires the trail — if a wrong fact spread, you need to see what it said and when it changed. |
| Big corrections also get a `log.md` entry | The changelog is where a reader checks "what changed since I last read this?" |
| Superseded ≠ current | A chapter drowning in supersede notes has outgrown itself — that triggers [chapter-budget](chapter-budget.md), not deletion. |

**Takeaway** — **deletion destroys evidence; supersession preserves both the truth and the history of how we got it wrong.**

**Example** *(constructed, illustrative)* — a consumer agent quotes a stale join rule. With deletion, you can't tell whether it hallucinated or read an old version. With supersession, one look at the chapter shows the claim existed until 2026-07-06 and exactly what replaced it — the diagnosis takes seconds.

**In this system** — the gate's quality checklist rejects edits that removed lines without a supersede note (git diff makes this checkable). Inherited from CandleKeep's recipe, kept because it's right. Poisoning is the failure this rule makes diagnosable.
