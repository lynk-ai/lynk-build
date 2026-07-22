---
type: rule
description: A page's referents must resolve on the shelf the reader holds — no authoring-repo machinery, internal paths, people, or unshipped book names in reader-facing text.
load_when: Writing any reader-facing passage that names a system, tool, person, or book — checking the referent travels with the page.
keywords: [audience, shipped, referents, internal, portability, consumer shelf]
rules:
  - id: quality/shipped-referents
    severity: error
    scope: page
    statement: Every referent in reader-facing text is either on the reader's shelf, a published external source, or stated generally — never internal machinery that doesn't travel with the book.
    gate_criteria: >
      A page passes when everything it names resolves for the shelf it ships
      to: a book/page that travels with it, a published external source, or
      a general formulation ("a fail-closed check" rather than a named
      internal gate). It fails when reader-facing text names authoring-repo
      machinery — build plans and phase numbers, maintainer names, repo
      paths, tools or books the reader's shelf does not carry. Exception:
      books explicitly scoped to an internal audience, where internal
      referents ARE on-shelf. Judged against the book's declared audience;
      cross-book name-references to unshipped books are governed here, while
      their form is structure/no-cross-book-links.
---

# Write for the shelf

**What it is** — the audience rule: a book is read where it *ships*, not where it was written. Every referent — a tool, a person, a phase, another book — either travels with the page, exists publicly, or must be stated generally. Internal machinery named in reader-facing text is a pointer into a room the reader can't enter: it reads as authority and resolves to nothing.

**Mechanics** — the referent test, per named thing:

| The page names… | Passes when | Fix when not |
|---|---|---|
| Another book/page | It ships on the same shelf. | Generalize, or make it a Lead the routing layer may miss gracefully. |
| A tool or pipeline stage | The reader's environment has it. | Describe the *shape* ("a fail-closed admission check"), not the internal name. |
| A person or team | Recorded in git history, not in reader-facing prose. | Attribute to role or drop. |
| A path or plan | It resolves on the reader's disk. | Cite the published source or generalize. |

**Takeaway** — **write for the shelf the reader holds: every referent must resolve there, exist publicly, or be said generally — internal machinery doesn't ship.**

**Example** *(real — a sibling book, 2026-07-19)* — the shipped copy's pages told readers about "the gate," "maintenance (Phase 5)," and "PLAN.md" — authoring-repo machinery absent from the consumer plugin; the index carried maintainer names and internal doc paths. The retarget replaced each with its shipped or general equivalent (the librarian-as-router, "a fail-closed admission check," named upkeep) — every guard kept, every dead referent gone. That incident is this rule's origin.

**In this system** — the gate judges referents against the book's declared audience (the shelf listing decides who ships where); internal-audience books legitimately name internal machinery — for them, it IS the shelf. → See [interlinks](interlinks.md) for the form cross-book references must take, and [non-inferable-only](non-inferable-only.md) — the admission twin: that rule asks *does this content earn its place*; this one asks *can the reader even resolve it*.
