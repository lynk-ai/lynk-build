# Index

**The Book Standard.** The *how* of the library: what a book must look like to enter it. Three parts mirror the quality model — structure (agents can navigate it), context quality (the information is precise), generality (a how-to is a complete recipe). The gate's checklists are derived from this book — improve a rule here and enforcement updates with it. This book applies the library's context-engineering principles without restating them; no rule lives in two places.

## When to load this book

- Writing, editing, or gating any book or chapter — the rules live here, keyed by stable `rule_id`s.
- Deciding where content belongs: admission, placement, splitting, graduation.
- A gate rejection cited a rule and you need its statement, criteria, and exceptions.
- **Not** for the *why* behind these rules (grounded elsewhere in the library) and not for domain knowledge (the domain books own that).

## Red flags — situation → chapter

| Situation | Open |
|---|---|
| Starting a whole new book — or unsure the topic deserves one | `write-a-book.md` |
| Sitting down to write a new chapter | `write-a-chapter.md` |
| Stuck on one section — definition, takeaway, example | `write-a-section.md` |
| Adding or amending a rule's frontmatter block | `write-a-rule.md` |
| Does this content belong in a book at all? | `non-inferable-only.md` |
| Does this chapter belong in THIS book? | `scope-fit.md` |
| Naming or describing a chapter; routing picks wrong chapters | `toc-discipline.md` |
| Readers can't find a chapter that answers their question | `loading-triggers.md` · `keywords.md` |
| Making a factual claim — how to mark it | `sourced-statements.md` |
| Correcting or removing existing content | `supersede-dont-delete.md` |
| A chapter is too long or piling caveats | `chapter-budget.md` |
| A concept is outgrowing its chapter into a book | `graduation.md` |
| Linking chapters within a book (a book never references another) | `interlinks.md` |
| A chapter names tools, people, or books the reader may not have | `write-for-the-shelf.md` |
| Choosing a worked example — should it be domain-specific or general? | `example-domain-fit.md` |
| Writing a how-to — what makes it complete | `the-recipe-shape.md` |

**Chapter shape:** every chapter runs *What it is → Mechanics → Takeaway → Example → In this system* (`chapter-template.md`); each carries a `load_when:` trigger and `keywords:`.

## Part I — Structure *(agents can navigate it)*

| # | Chapter | One-liner |
|---|---|---|
| 0 | `chapter-template.md` | The concept template every chapter follows: *What it is → Mechanics → Takeaway → Example → In this system.* |
| 1 | `chapter-anatomy.md` | One concept per chapter · single H1 as title · frontmatter (type, description) — the file-level rules. |
| 2 | `index-and-changelog.md` | Every book keeps an Index chapter and a Changelog chapter, updated on every edit. |
| 3 | `interlinks.md` | Within-book links are followable markdown pointers, used liberally; a book is self-contained and never references another book. |
| 4 | `toc-discipline.md` | The TOC is derived from headings and descriptions; keep them clean or routing breaks. |
| 5 | `library-layout.md` | Folder = book, files = chapters; shelves as curated sub-sets; where new books land. |
| 5b | `loading-triggers.md` | Every book states when to load it and every chapter carries a `load_when` trigger — agents route on triggers, not titles. |
| 5c | `keywords.md` | Every chapter carries a keywords list — the synonym surface a search hits when the asker uses different words than the chapter. |
| 5d | `scope-fit.md` | A chapter must fit the book's existing index description — a placement that stretches the scope with a new subject clause is rejected as wrong-home (added 2026-07-21, from eval findings). |

## Part II — Context Quality *(the information is precise)*

| # | Chapter | One-liner |
|---|---|---|
| 6 | `sourced-statements.md` | Every factual claim is classified — sourced, derived, opinion, or uncertain — and the gate rejects unmarked claims. |
| 7 | `supersede-dont-delete.md` | Never delete — add a dated supersede note. History is evidence. |
| 8 | `chapter-budget.md` | A chapter targets ~4,000 characters (± 1,000; recipes larger) — outgrowing the range triggers a split (or a merge), not more growth. |
| 8b | `non-inferable-only.md` | A book holds only what the reader can't infer or fetch elsewhere — restating the obvious is rot. |
| 8c | `graduation.md` | When a concept outgrows its chapter into its own book, the old chapter becomes a self-contained stub — no pointer out; one concept keeps one home. |
| 8d | `write-for-the-shelf.md` | A chapter's referents must resolve on the shelf the reader holds — internal machinery doesn't ship. |
| 8e | `example-domain-fit.md` | An example's domain matches the book's declared scope — in-domain for a domain book, domain-neutral for a general/method book; the writer picks the mode. |

## Part III — Generality *(a book is a recipe)*

| # | Chapter | One-liner |
|---|---|---|
| 9 | `the-recipe-shape.md` | Every how-to chapter runs prerequisites → steps → verification → failure modes. E2E or it doesn't ship. |
| 9b | `write-a-book.md` | Creating a whole book — prove the cluster, skeleton the index, write the center of gravity, grow outward, enter through the gate. |
| 9c | `write-a-chapter.md` | The end-to-end procedure for writing one chapter — the standard's rules applied in writing order. |
| 9d | `write-a-section.md` | The craft of each of the five sections — definition, mechanics, takeaway, example, tie-in — each against its own bar. |
| 9e | `write-a-rule.md` | Authoring the machine layer — stable rule_id, one-sentence statement, gate_criteria with named exceptions, defensible severity. |
