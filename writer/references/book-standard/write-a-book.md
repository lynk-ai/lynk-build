---
type: recipe
description: The end-to-end procedure for creating a whole book — from "does this deserve a book?" through index skeleton, parts, first pages, and the gate.
load_when: Starting a brand-new book, or deciding whether a topic deserves one at all — the book-level procedure above write-a-page.
keywords: [new book, book creation, index skeleton, parts, scaffolding, when to create]
---

# Write a book

**What it is** — the book-level procedure above [write-a-page](write-a-page.md): when a topic earns a whole book, how its container is built, and in what order the pages land. Most of the work is *not* writing — it is proving the book should exist and building an index that routes before there is much to route to.

**Prerequisites**

- The topic is a **cluster of independently-citable concepts**, not one concept stretched thin — the deepening bar; one concept wants sibling pages in an existing book, not a book of its own.
- No existing home — checked across the library TOC; if a page already owns the concept, this is an edit or enrichment of that page — or, when the concept genuinely needs its own book, deleting the old chapter and writing the new book — not a special procedure.
- The audience is declared: which shelf will this book ship to, and what is on it ([write-for-the-shelf](write-for-the-shelf.md)).
- Sources gathered for the load-bearing claims — a book whose first pages are unsourced starts life failing [sourced-statements](sourced-statements.md).

**Steps** — one observable outcome each:

1. **Name it** — kebab-case slug naming the topic ([library-layout](library-layout.md)) → the folder exists and its name is the book's promise.
2. **Skeleton the index** — title + one-paragraph scope, a "When to load this book" section with at least one negative trigger ([loading-triggers](loading-triggers.md)), and the part structure with planned page rows (dead rows are recorded gaps, not errors) → an agent reading only `index.md` can already say what the book will and won't answer.
3. **Write the load-bearing page first** — the concept every other page will cite, via [write-a-page](write-a-page.md) → the book's center of gravity exists before its periphery.
4. **Write outward** — remaining pages in citation order (a page lands after the pages it links to, so within-book links resolve as you go) → each new page links backward, never dangles.
5. **Add the red-flag table** once the book passes ~5 pages — symptom → page routing in the index → a reader with a problem, not a topic, still lands right.
6. **Gate it** — the book enters the library only through the gated write path ([library-layout](library-layout.md)) → a verdict exists before any reader trusts it.

**Verification**

- `bk lint <book>` — 0 errors: layout, reserved pages, frontmatter, links.
- The index-only test: hand a reader `index.md` alone — can they route three sample questions to the right page rows? If not, the labels fail before the content matters.
- Every page reachable from the index; every within-book link resolves or is an intentional recorded gap.

**Failure modes**

- **The book is one concept stretched thin** — symptom: page one-liners restate each other; the parts feel invented. Fix: it's a page, not a book — fold it into its parent (real case: a sibling book, 7 pages folded back to its origin book as 4, 2026-07-19).
- **The index accumulates content** — symptom: explanatory paragraphs growing under the part tables. Fix: the discovery layer carries pointers, never bodies; move the prose into a page.
- **The book wants subfolders** — symptom: pages clustering into sub-directories. Fix: it is two books ([library-layout](library-layout.md)) — split at the cluster line.
- **Pages land before their dependencies** — symptom: forward links that stay dead for weeks. Fix: reorder to citation order (step 4); a dead link is a recorded gap only when it's deliberate.

**Takeaway** — **a book is born index-first: prove the cluster, skeleton the routing, write the center of gravity, grow outward in citation order — and enter only through the gate.**

**Example** *(real — a sibling book, 2026-07-12 to 07-19)* — a sibling book on the shelf demonstrates the full arc: born as an index skeleton with an authorship plan, grown page by page with its load-bearing pages first, gate-corrected on 07-13, retrofitted with triggers and a red-flag table on 07-19 — and its folded-back pages are the counter-case: a cluster that failed prerequisite 1 and returned to page form.

**In this system** — this recipe is the writer's brief for any `bk create`; the gate enforces its outcomes (layout, reserved pages, index honesty). → See [write-a-page](write-a-page.md) for the per-page procedure inside steps 3–4.
