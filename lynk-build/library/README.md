# library

The research-only book library the build agent reads via the `lynk-research` skill
(librarian picks books, scholars read chapters). No build step — `bin/` renders the
catalog and each book's TOC on demand.

## Add a book

```
library/<book-slug>/
├── index.md              # frontmatter: name, description, labels
└── chapters/NN-title.md  # each: frontmatter (name, description, labels) then content
```

`index.md` and each chapter start with a YAML frontmatter block:

```markdown
---
name: Undoing a commit
description: How to revert, reset, and amend commits safely.
labels: git, version-control, recovery
---

<chapter content…>
```

The catalog (`bin/generate_library_index`) lists every `*/index.md`; a book's TOC
(`bin/generate_book_toc <slug>`) lists its chapters with absolute paths. Slugs must
match `^[a-z0-9._-]+$`.
