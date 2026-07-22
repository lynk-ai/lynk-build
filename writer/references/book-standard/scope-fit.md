---
type: rule
description: A chapter must fit its book's existing index description — a placement that requires stretching the book's scope is rejected as a wrong-home signal.
rules:
  - id: structure/scope-fit
    severity: error
    scope: page
    statement: A page joins a book only if the book's existing index description already covers its subject; if admission requires appending a new subject clause to the description, the placement is rejected.
    gate_criteria: >
      A placement passes when the book's index description, as it stood BEFORE
      the edit, already encompasses the new page's subject — rewording
      for clarity is fine. It fails when the
      description must gain a new subject clause ("plus ...", "and also ...",
      "as well as ...") to cover the page: that seam marks a wrong home. The
      fix is placement in the book whose scope already fits, or a new book
      when none does. Detectable mechanically: diff the index description
      before and after the change — a scope-extending edit fails, a clarifying
      edit passes. With a small library, beware the degenerate case: "the
      best-fitting book" must never mean "the only book".
---

# Scope fit

**What it is** — the placement bar: a book is one subject, and its index description *is* that subject's contract with readers. A chapter earns its place in a book only if the description as already written covers it. Content quality does not rescue placement: an excellent chapter in the wrong book still breaks routing (readers looking for it check the right-subject book and miss) and dilutes the host book's scope.

**Mechanics** — the test is a diff of the index description. Rewording for clarity: pass. Appending a new subject clause so the description now says "X — plus Y": fail. The "plus" seam is the tell — if the description needs to grow a second subject to admit the page, the page belongs elsewhere. When no existing book's scope fits, that is the new-book signal.

**Takeaway** — **if admitting a page stretches the book's index description with a new subject clause, the placement is rejected — right content, wrong home is still a rejection.**

**Example** *(real, from this library's own evaluation, 2026-07-21)* — an automated writer produced an excellent, fully-sourced chapter on multi-agent failure rates and placed it in the context-engineering principles book because that was the only book on the shelf. The index description had to become "The why of context engineering — … *plus the measured failure-rate numbers for multi-agent LLM systems*". Under this rule the placement is rejected: the chapter's home is a multi-agent book, and the context book's description reverts to its clean scope.

**In this system** — a gate check (structure dimension): the verifier diffs the target book's index description; a scope-extending edit bounces with this rule cited. It complements [non-inferable-only](non-inferable-only.md) (admission on merit) — this rule is admission on *address*.
