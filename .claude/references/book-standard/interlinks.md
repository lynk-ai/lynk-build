---
type: rule
description: Within-book links are relative markdown pointers an agent follows, used liberally; a book is self-contained and never references another book — cross-book relationships are the routing layer's job.
load_when: Linking chapters within a book, or tempted to point at another book — deciding what a chapter may reference.
keywords: [links, within-book, cross-book, references, self-contained, leads, pointers, dead links]
rules:
  - id: structure/interlinks
    severity: error
    scope: chapter
    statement: A chapter links the related within-book chapters it names with relative markdown links; a chapter with no links must justify standing alone.
    gate_criteria: >
      A chapter passes when within-book concepts that have their own chapters are
      linked where named (relative markdown links), and the In this system
      section carries the chapter's most important within-book pointers. It fails
      when it has zero interlinks and no visible justification for being
      standalone. Deliberate dead within-book links are allowed as recorded gaps
      — a link to a not-yet-written chapter in the same book is a feature — but a
      dead link caused by a typo or a rename is a defect; lint flags all
      unresolved links and the judgment call is whether the gap reads as
      intentional. Cross-book references are out of scope here — they are
      governed by structure/no-cross-book-links.
  - id: structure/no-cross-book-links
    severity: error
    scope: chapter
    statement: A book never references another book — no cross-book markdown links and no cross-book name-references; a chapter references only chapters within its own book.
    gate_criteria: >
      A chapter passes when every reference it makes points to a chapter in the same
      book (a relative markdown link). It fails on any cross-book reference: a
      relative markdown link into another book's folder ('](../other-book/...)'),
      or a plain-text name that points a reader at a chapter in another book. The
      mechanical half — no '](../' cross-book link — is enforced
      deterministically by lint/cross-book-link; the gate judges that no prose
      reference sends the reader out to another book. Rationale: a book is a
      self-contained, general unit assigned to a specific task, so it cannot
      assume any other book is on the reader's shelf; cross-book relationships
      are resolved by the routing layer (the librarian, against whatever shelf
      is present), never by an in-chapter reference. If a chapter seems to need
      another book, inline the non-inferable point or the two concepts belong in
      one book. Exception: history — dated supersede notes and the changelog may
      name a former home as a record, since they document the past rather than
      route the reader. Within-book relative links are unaffected
      (structure/interlinks governs those).
---

# Interlinks

**What it is** — how chapters point at each other. There is one kind of reference: the *within-book* link — a relative markdown link a reading agent follows inline to its next chapter (OKF: "plain markdown links between files are the graph"). A book never points *out* to another book: it is a self-contained unit, and the reader's shelf may not even carry the book you would have named.

**Mechanics**

| Case | Form |
|---|---|
| Same book | `→ See [chapter-anatomy](chapter-anatomy.md)` — a relative markdown link, followed inline. Use liberally: every link saves a future reader a search. |
| Another book | **Not referenced.** A book is self-contained; cross-book relationships are the routing layer's job (the librarian resolves them against the shelf), never an in-chapter link or name. If you are reaching for one, inline the non-inferable point or the two concepts belong in one book. |
| Not-yet-written chapter (same book) | Link it anyway — a dead within-book link is a recorded gap, a chapter worth writing, not an error. |

*(superseded 2026-07-20: this table previously carried an "Another book (cross-book)" row permitting a plain-text canonical name as a routable Lead. Cross-book references of every kind are now forbidden: a book references only its own chapters. See the rationale below and log.md. The earlier 2026-07-16 note — which forbade cross-book markdown links but still allowed the name form — is itself superseded by this stricter rule.)*

**Why a book never references another book** — books are independently shippable, general units, each assignable to a specific task: the published shelf ships in the plugin bundle while other books stay home, so a book routinely sits on a shelf without the books it might have named. A cross-book pointer — link *or* name — is therefore a reference the reader may be unable to resolve. Keeping references in-book makes every book portable: drop it onto any shelf and all its links still work. Cross-book discovery is the routing layer's job — the librarian and scouts relate books against whatever shelf is actually present — not something an in-chapter reference should hard-code.

**Where** — within-book links: inline when a concept is named mid-sentence, and every chapter ends its "In this system" section with its most important within-book pointers.

Why within-book paths, not chapter numbers: CandleKeep's recipe used `ck items read <bookId>:<pageNum>` because its substrate was a paginated cloud API. Ours is git + files, so the within-book pointer is a relative path — same idea, native form.

**Takeaway** — **link liberally within a book; never reference another book — cross-book relationships are the routing layer's job, so every book stays a self-contained unit that works on any shelf.**

**Example** — a reader on `supersede-dont-delete.md` follows `→ See [chapter-budget](chapter-budget.md)` inline — same book, one hop. A concept that lives in a *different* book is not linked or named inline at all: the chapter makes its own point self-containedly, and if the reader needs that other book, the librarian routes them there from the shelf. *(superseded 2026-07-20: the prior example named a chapter in another book as a routable Lead — cross-book names are no longer used; see the rationale above.)*

**In this system** — the gate's structure checklist counts within-book links (a chapter with zero is presumed disconnected — reject unless genuinely standalone) and, per `structure/no-cross-book-links`, rejects any cross-book reference — a markdown link into another book *or* a prose name pointing at one. The deterministic `lint/cross-book-link` enforces the mechanical half; the gate judges that no prose sends the reader out of the book. Maintenance walks within-book links to find dead ones — each becomes a proposed chapter. → See [toc-discipline](toc-discipline.md) for the other half of navigability.
