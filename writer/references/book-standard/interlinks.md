---
type: rule
description: Within-book links are relative markdown pointers an agent follows, used liberally; a book is self-contained and never references another book — cross-book relationships are the routing layer's job.
load_when: Linking pages within a book, or tempted to point at another book — deciding what a page may reference.
keywords: [links, within-book, cross-book, references, self-contained, leads, pointers, dead links]
rules:
  - id: structure/interlinks
    severity: error
    scope: page
    statement: A page links the related within-book pages it names with relative markdown links; a page with no links must justify standing alone.
    gate_criteria: >
      A page passes when within-book concepts that have their own pages are
      linked where named (relative markdown links), and the In this system
      section carries the page's most important within-book pointers. It fails
      when it has zero interlinks and no visible justification for being
      standalone. Deliberate dead within-book links are allowed as recorded gaps
      — a link to a not-yet-written page in the same book is a feature — but a
      dead link caused by a typo or a rename is a defect; lint flags all
      unresolved links and the judgment call is whether the gap reads as
      intentional. Cross-book references are out of scope here — they are
      governed by structure/no-cross-book-links.
  - id: structure/no-cross-book-links
    severity: error
    scope: page
    statement: A book never references another book — no cross-book markdown links and no cross-book name-references; a page references only chapters within its own book.
    gate_criteria: >
      A page passes when every reference it makes points to a page in the same
      book (a relative markdown link). It fails on any cross-book reference: a
      relative markdown link into another book's folder ('](../other-book/...)'),
      or a plain-text name that points a reader at a page in another book. The
      mechanical half — no '](../' cross-book link — is enforced
      deterministically by lint/cross-book-link; the gate judges that no prose
      reference sends the reader out to another book. Rationale: a book is a
      self-contained, general unit assigned to a specific task, so it cannot
      assume any other book is on the reader's shelf; cross-book relationships
      are resolved by the routing layer (the librarian, against whatever shelf
      is present), never by an in-page reference. If a page seems to need
      another book, inline the non-inferable point or the two concepts belong in
      one book. Within-book relative links are unaffected
      (structure/interlinks governs those).
---

# Interlinks

**What it is** — how pages point at each other. There is one kind of reference: the *within-book* link — a relative markdown link a reading agent follows inline to its next page (OKF: "plain markdown links between files are the graph"). A book never points *out* to another book: it is a self-contained unit, and the reader's shelf may not even carry the book you would have named.

**Mechanics**

| Case | Form |
|---|---|
| Same book | `→ See [page-anatomy](page-anatomy.md)` — a relative markdown link, followed inline. Use liberally: every link saves a future reader a search. |
| Another book | **Not referenced.** A book is self-contained; cross-book relationships are the routing layer's job (the librarian resolves them against the shelf), never an in-page link or name. If you are reaching for one, inline the non-inferable point or the two concepts belong in one book. |
| Not-yet-written page (same book) | Link it anyway — a dead within-book link is a recorded gap, a page worth writing, not an error. |

**Why a book never references another book** — books are independently shippable, general units, each assignable to a specific task: the published shelf ships in the plugin bundle while other books stay home, so a book routinely sits on a shelf without the books it might have named. A cross-book pointer — link *or* name — is therefore a reference the reader may be unable to resolve. Keeping references in-book makes every book portable: drop it onto any shelf and all its links still work. Cross-book discovery is the routing layer's job — the librarian and scouts relate books against whatever shelf is actually present — not something an in-page reference should hard-code.

**Where** — within-book links: inline when a concept is named mid-sentence, and every page ends its "In this system" section with its most important within-book pointers.

Why within-book paths, not page numbers: CandleKeep's recipe used `ck items read <bookId>:<pageNum>` because its substrate was a paginated cloud API. Ours is git + files, so the within-book pointer is a relative path — same idea, native form.

**Takeaway** — **link liberally within a book; never reference another book — cross-book relationships are the routing layer's job, so every book stays a self-contained unit that works on any shelf.**

**Example** — a reader on `page-anatomy.md` follows `→ See [page-budget](page-budget.md)` inline — same book, one hop. A concept that lives in a *different* book is not linked or named inline at all: the page makes its own point self-containedly, and if the reader needs that other book, the librarian routes them there from the shelf.

**In this system** — the gate's structure checklist counts within-book links (a page with zero is presumed disconnected — reject unless genuinely standalone) and, per `structure/no-cross-book-links`, rejects any cross-book reference — a markdown link into another book *or* a prose name pointing at one. The deterministic `lint/cross-book-link` enforces the mechanical half; the gate judges that no prose sends the reader out of the book. Maintenance walks within-book links to find dead ones — each becomes a proposed page. → See [toc-discipline](toc-discipline.md) for the other half of navigability.
