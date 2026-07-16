---
name: bk-search
description: Shared bk CLI reference for library agents - how to list, inspect, read, and grep the library, with role tagging and the slug contract. Preloaded by the librarian and book-reader agents; not for direct invocation by the main agent.
---

# bk — search & read reference (shared by library agents)

**Resolve the CLI first** (works in the dev repo AND inside a host plugin):
```bash
BK_ROOT="${CLAUDE_PLUGIN_ROOT:-$PWD}"; BK="$BK_ROOT/scripts/bk"
BK_DATA="${BK_DATA:-$PWD/.bk}"
```
Books are read from `$BK_ROOT` (the plugin bundle when installed); all state — reads log, gaps, fetch files — lands in `$BK_DATA` (the project you're working in). Always tag your role so the reads telemetry stays honest:
`BK_ROLE=<librarian|reader|hook> BK_ROOT="$BK_ROOT" BK_DATA="$BK_DATA" "$BK" <verb> ...`

## Verbs you use

| Verb | What it returns | Who uses it |
|---|---|---|
| `bk list --json` | The shelf: every book's slug, page count, description | librarian |
| `bk toc <book> --json` | One book's pages: slug, type, one-line description | librarian (to judge books), reader (to judge chapters) |
| `bk read <book>:<slug>,<slug>` | Page bodies, exactly the listed slugs | reader (judgment reads only), hook (the fetch) |
| `bk grep "<term>" --book <book>` | Full-text hits as `book/page:line` | reader (fallback when descriptions mislead) |

## Contracts that never bend
- **Slugs**: `^[a-z0-9-]+$` — anything else is invalid, never guess or construct paths.
- **Never `read <book>:all`** for research — that's for auditing.
- **Metadata before content**: judge from `toc` descriptions first; read only to resolve genuine doubt.
- **Reads are logged** per session with content hashes (`.bk/reads/<session>.jsonl`) — every read leaves a receipt; cite only what you actually read.
- **Descriptions are lossy one-liners**: when a description under- or over-promises its page, flag it (`Metadata flags:`) — that feeds maintenance.

## Miss logging (both routing stages)
A miss is recorded demand — append one line to the writing backlog before returning:
```bash
mkdir -p "$BK_DATA" && printf '%s\n' '{"ts":"'"$(date -Iseconds)"'","stage":"<librarian|reader>","book":"<slug-if-reader>","intent":"<abstracted topic>","context":"<one sentence: what task produced this miss>","suggested":"<page that should exist>"}' >> "$BK_DATA/gaps.jsonl"
```
The `context` field is the sustain loop's research seed — write it for the future author, not the logger.
