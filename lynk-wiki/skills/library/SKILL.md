---
name: library
description: Runs the library pipeline - librarian routes by metadata, book-readers read cited pages. Use when the user asks what the books/library/standard say, or when a task needs the constitution's principles or rules. Also use BEFORE creating, updating, or editing semantic-layer artifacts (entities, metrics, relations, features, policies) and before agent/skill/eval design decisions - reference docs give the format, this library gives the methodology and verification.
---

# Library — nested pointer pipeline (one librarian call)

You were invoked to consult the library. You spawn ONE agent; the library handles itself. Only pointers flow up; content lands in fetch files. Do not read whole books inline.

## Step 1 — Spawn the librarian (that's the whole fan-out)
```
Agent tool:
subagent_type: "lynk-wiki:librarian"
prompt: "[Full task context: what the user asked, what you already know,
what decision the answer will feed.]
Route the relevant books, dispatch your scouts, and return the
consolidated pointer list with the fetch files."
```
The librarian routes books from metadata, spawns one chapter-scout per relevant book (nested, parallel), and consolidates their POINTER and fetch lines. The brief must carry the full story — the librarian writes each scout's objective FROM it, so a thin brief compounds into blind scouts two hops down.

## Step 2 — Act on its (exactly three-shape) response

**`## Pointers` + `## Fetch files`** → `Read` each named `.bk/fetch/<agent>.txt` file — each holds one scout's pointers, notes, and the primary text of exactly its pointed chapters. Answer from that primary text; cite `(book · page)` for every claim. Do not answer before reading every listed fetch file.
- Pointers present but NO fetch line for some book (hook silent there) → fetch inline: one `"${CLAUDE_PLUGIN_ROOT}"/bk read <book>:<slugs>` with exactly the pointed slugs.
- `Empty:` books in Routing notes → gap already logged (`"stage":"reader"`); answer from the rest and tell the user which book came up empty despite routing.

**`## Routing List`** (books + objectives, no pointers) → the librarian's scouts couldn't spawn. Dispatch them yourself — one `book-reader` per listed book, all in parallel, passing each book's Objective verbatim plus the RESEARCH_INTENT — then treat their returns as above.

**`### No relevant books found`** → do NOT proceed. The gap is already logged to `.bk/gaps.jsonl` (the writing backlog). Tell the user plainly the library doesn't cover it, and surface the `<suggested_page>` as "a page worth writing."

## Step 3 — the citation block
When library content shaped your answer, end the response with:
```
┌─ Library ─────────────────────────────────────────────┐
│ Read: <book · pages>                                   │
│ Learned: <2-4 key phrases separated by ·>              │
│ Worth remembering: "<a quotable line from the fetched  │
│ text>" — book · page                                   │
└────────────────────────────────────────────────────────┘
```
SKIP the block when nothing relevant was found or nothing was used.


## Gap backlog — the library asking for pages
`.bk/gaps.jsonl` accumulates misses from both stages (`"stage":"librarian"` — no book covered it; `"stage":"reader"` — a book's metadata over-promised). When the user asks "what should we write next?", read it, dedupe, and propose the top gaps as book/page candidates — each gap is recorded demand.

## Fallback — no subagents at all
If even the librarian can't spawn (host thread cap), read inline as the documented exception:
`"${CLAUDE_PLUGIN_ROOT}"/bk toc <book>` → `"${CLAUDE_PLUGIN_ROOT}"/bk read <book>:<specific pages>` — targeted pages only, cite as usual, and don't retry spawning this session.

## Common mistakes
- Spawning scouts yourself while the librarian is available — the librarian owns the fan-out
- Passing page slugs to the librarian — chapter choice is the scouts' procedure
- Answering before Reading the fetch files — the pointers are not the answer
- Running `"${CLAUDE_PLUGIN_ROOT}"/bk read` inline outside the documented fallbacks
- Reading `<book>:all` for research (that's for auditing, not answering)
- Omitting the citation block when fetched pages were used
