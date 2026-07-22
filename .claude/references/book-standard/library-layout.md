---
type: rule
description: Folder = book, files = chapters, index.md + log.md reserved — where books live and where new ones land.
load_when: Adding a book to the library, structuring one on disk, or wondering whether a book may have subfolders.
keywords: [folders, layout, shelves, books, slugs, flat, structure]
rules:
  - id: structure/library-layout
    severity: error
    scope: book
    statement: A book is a flat kebab-case folder of chapters with reserved index.md and log.md; books enter the library only through the gate.
    gate_criteria: >
      A book passes when its folder slug matches ^[a-z0-9-]+$, contains index.md
      and log.md, holds chapters directly (no subdirectories), and — for new books —
      arrived via the gated write path rather than direct copy. A book wanting
      subfolders fails: it is usually two books and should split. Shelves are
      lists of book slugs, never copies. Flatness, slugs, and reserved files are
      checked deterministically by lint.
---

# Library layout

**What it is** — the shape of the library on disk. One convention, no database: a folder is a book, its markdown files are chapters, and two filenames are reserved in every book.

**Mechanics**

```
library/
├── payments-runbook/         ← a book: kebab-case slug names the folder
│   ├── index.md              ← reserved: the catalog (read first)
│   ├── log.md                ← reserved: the history
│   ├── context-rot.md        ← a chapter (one concept)
│   └── …
└── retry-policies/
```

| Rule | Detail |
|---|---|
| Folder slug = book title | `payments-runbook`, not `misc/`. The slug is the book's ID everywhere. |
| Flat inside a book | Chapters sit directly in the book folder. A book that wants subfolders is usually two books — split it. |
| New books land in `library/` | Only through the gate. Nothing enters by copy-paste. |
| Shelves (later) | A shelf is a curated *list* of book slugs (one file), never a copy — books have one home. |

**Takeaway** — **the directory structure is the feature: an agent that can list a folder can browse the library — no server, no index build, no query protocol.**

**Example** — an OKF-aware agent pointed at `library/` needs zero instructions: it lists folders (the shelf), reads each `index.md` (the TOC), and descends only into chapters it needs — the same walk CandleKeep's librarian does through its cloud API, done with `ls` and `cat`.

This shape isn't our invention — it's *convergent evolution*: independent teams landed on **small markdown files + YAML frontmatter + progressive disclosure**, evidence that files beat databases for agent-read knowledge.

> Superseded 2026-07-07: the convergence evidence graduated to `book-3-progressive-disclosure:convergent-evolution` (its full home). Kept here as a one-line pointer because it is the evidence for this chapter's files-beat-databases claim.

**In this system** — this layout *is* our replacement for CandleKeep's cloud (Phase 2): their DB rows become our folders, their chapter API becomes file reads, their version history becomes git. → See [chapter-anatomy](chapter-anatomy.md) for what's inside a chapter.
