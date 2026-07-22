# Index

**The Book Standard.** The *how* of the library: what a book must look like to enter it. Three parts mirror the quality model — structure (agents can navigate it), context quality (the information is precise), generality (a how-to is a complete recipe). The gate's checklists are derived from this book — improve a rule here and enforcement updates with it. This book applies the library's context-engineering principles without restating them; no rule lives in two places.

## When to load this book

- Writing, editing, or gating any book or page — the rules live here, keyed by stable `rule_id`s.
- Deciding where content belongs: admission, placement, splitting.
- A gate rejection cited a rule and you need its statement, criteria, and exceptions.
- **Not** for the *why* behind these rules (grounded elsewhere in the library) and not for domain knowledge (the domain books own that).

## Red flags — situation → page

| Situation | Open |
|---|---|
| Starting a whole new book — or unsure the topic deserves one | `write-a-book.md` |
| Sitting down to write a new page | `write-a-page.md` |
| Stuck on one section — definition, takeaway, example | `write-a-section.md` |
| Adding or amending a rule's frontmatter block | `write-a-rule.md` |
| Does this content belong in a book at all? | `non-inferable-only.md` |
| Does this chapter belong in THIS book? | `scope-fit.md` |
| Naming or describing a page; routing picks wrong pages | `toc-discipline.md` |
| Readers can't find a page that answers their question | `loading-triggers.md` · `keywords.md` |
| Making a factual claim — how to mark it | `sourced-statements.md` |
| A page is too long or piling caveats | `page-budget.md` |
| Linking pages within a book (a book never references another) | `interlinks.md` |
| A page names tools, people, or books the reader may not have | `write-for-the-shelf.md` |
| Writing a how-to — what makes it complete | `the-recipe-shape.md` |

**Page shape:** every page runs *What it is → Mechanics → Takeaway → Example → In this system* (`page-template.md`); each carries a `load_when:` trigger and `keywords:`.

## Part I — Structure *(agents can navigate it)*

| # | Page | One-liner |
|---|---|---|
| 0 | `page-template.md` | The concept template every page follows: *What it is → Mechanics → Takeaway → Example → In this system.* |
| 1 | `page-anatomy.md` | One concept per page · single H1 as title · frontmatter (type, description) — the file-level rules. |
| 3 | `interlinks.md` | Within-book links are followable markdown pointers, used liberally; a book is self-contained and never references another book. |
| 4 | `toc-discipline.md` | The TOC is derived from headings and descriptions; keep them clean or routing breaks. |
| 5 | `library-layout.md` | Folder = book, files = pages; shelves as curated sub-sets; where new books land. |
| 5b | `loading-triggers.md` | Every book states when to load it and every page carries a `load_when` trigger — agents route on triggers, not titles. |
| 5c | `keywords.md` | Every page carries a keywords list — the synonym surface a search hits when the asker uses different words than the page. |
| 5d | `scope-fit.md` | A chapter must fit the book's existing index description — a placement that stretches the scope with a new subject clause is rejected as wrong-home (added 2026-07-21, from eval findings). |

## Part II — Context Quality *(the information is precise)*

| # | Page | One-liner |
|---|---|---|
| 6 | `sourced-statements.md` | Every factual claim is classified — sourced, derived, or opinion — and the gate rejects unmarked claims. |
| 7 | `page-budget.md` | When a page outgrows itself, split it — restructure triggered by size, not schedule. |
| 7b | `non-inferable-only.md` | A book holds only what the reader can't infer or fetch elsewhere — restating the obvious is rot. |
| 7d | `write-for-the-shelf.md` | A page's referents must resolve on the shelf the reader holds — internal machinery doesn't ship. |

## Part III — Generality *(a book is a recipe)*

| # | Page | One-liner |
|---|---|---|
| 9 | `the-recipe-shape.md` | Every how-to page runs prerequisites → steps → verification → failure modes. E2E or it doesn't ship. |
| 9b | `write-a-book.md` | Creating a whole book — prove the cluster, skeleton the index, write the center of gravity, grow outward, enter through the gate. |
| 9c | `write-a-page.md` | The end-to-end procedure for writing one page — the standard's rules applied in writing order. |
| 9d | `write-a-section.md` | The craft of each of the five sections — definition, mechanics, takeaway, example, tie-in — each against its own bar. |
| 9e | `write-a-rule.md` | Authoring the machine layer — stable rule_id, one-sentence statement, gate_criteria with named exceptions, defensible severity. |
