---
type: rule
description: Every book keeps an index.md (catalog) and a log.md (history), both updated on every edit.
load_when: Editing any chapter of a book — what must update in the same change — or auditing an index/changelog for staleness.
keywords: [index, changelog, log, catalog, reserved chapters, stale]
rules:
  - id: structure/index-current
    severity: error
    scope: book
    statement: The book's index.md lists every chapter with its frontmatter description, updated in the same change as any chapter change.
    gate_criteria: >
      A change passes when index.md lists every chapter in the book and reflects any
      chapter added, renamed, or re-described in that same change. It fails when a
      chapter exists but is absent from the index, or when a chapter's index entry
      contradicts its frontmatter description. Mechanical regeneration via
      'bk index --write' satisfies this rule; hand-maintained extras (part
      groupings, review notes) are allowed on top as long as the listing is
      complete.
  - id: structure/reserved-pages-plain
    severity: warn
    scope: chapter
    statement: The reserved chapters index.md and log.md carry no frontmatter — they open directly with their H1.
    gate_criteria: >
      index.md and log.md open with '# ...' and carry no YAML frontmatter block;
      book-level metadata lives in the book's chapters and folder name, not in the
      reserved chapters. A frontmatter block on a reserved chapter warns (convention,
      not breakage — bk exempts reserved chapters from frontmatter checks); the fix
      is to delete the block. Codified 2026-07-07 after the same break recurred
      in two consecutive drafts.
  - id: structure/log-current
    severity: error
    scope: book
    statement: The book's log.md gains a dated entry in every change that touches the book, most recent first.
    gate_criteria: >
      A change passes when log.md contains a dated entry ('## [YYYY-MM-DD] ...')
      describing that change, placed most-recent-first. It fails when chapters
      changed but the changelog did not, or when the entry is undated. Exception:
      a change that touches only log.md itself needs no second entry, and
      mechanical index regeneration alone may share the entry of the change that
      caused it.
---

# Index and changelog chapters

**What it is** — two reserved files every book must keep: `index.md`, a catalog of every chapter with a one-line summary, and `log.md`, a dated history of changes, most recent first. Both are updated on *every* edit — no exceptions.

**Mechanics**

| File | Holds | Updated when |
|---|---|---|
| `index.md` | One line per chapter: title + the chapter's frontmatter `description`. Grouped into parts if the book has them. | Any chapter is added, renamed, or its description changes. |
| `log.md` | `## [YYYY-MM-DD] What changed` entries, newest first, 1–3 sentences each. | Every edit to the book, including index-only edits. |

The names are OKF's reserved filenames — any OKF-aware agent knows to read `index.md` before descending into a bundle. Both are **frontmatter-less**: they open directly with their H1; book-level metadata lives in the chapters and the folder name, not in the reserved chapters (codified 2026-07-07 after the break recurred in two consecutive drafts).

**Takeaway** — **the index is what agents read instead of the whole book; a stale index doesn't just mislead — it silently hides every chapter it forgot.**

**Example** — an agent asks "what does the standard say about links?" The scout assigned to this book runs its TOC (`bk toc`), sees "interlinks — links are chapter pointers an agent can follow," and points there — one chapter read instead of ten. *(superseded 2026-07-14: previously "The librarian reads this book's index.md … and routes there" — pipeline restructured to the pointer flow: a scout runs the book's TOC and points; see log.md)* If the index had missed that entry, the chapter effectively doesn't exist.

**In this system** — the gate rejects any edit that touched a chapter but not the index and log (structure checklist). This mirrors CandleKeep's recipe ("update both on every edit") — but ours is enforced, not requested.
