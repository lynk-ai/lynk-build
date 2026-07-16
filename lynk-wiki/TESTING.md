# lynk-wiki + library integration — test plan

**Build under test:** plugin `lynk-wiki` v0.1.1 · books rendered from lynk-book @ `253276e`
**Branch:** `integrating-lynk-book`

## Setup (2 minutes)

```bash
mkdir /tmp/lynk-wiki-test && cd /tmp/lynk-wiki-test     # any empty scratch dir
claude --plugin-dir <path-to-this-repo>/lynk-wiki
```

On session start you should see a `<library>` block listing **6 books** (best-context 12p, progressive-disclosure 7p, skills 6p, subagents 6p, evals 9p, semantic-layer 8p) and a BUILD DIRECTIVE. If you don't, the plugin didn't load — stop and report.

## Test 1 — research question (the full pipeline)

Ask: **"What does the library say about the strict brief?"**

Expect, in order:
- ONE `librarian` agent spawns (not several) → it spawns `book-reader` scout(s) itself
- The final answer cites `(book · page)` pairs and ends with a `┌─ Library ─┐` citation block
- Files appear in **your scratch project**: `.bk/fetch/<agent>.txt` (the fetched chapters) and `.bk/reads/*.jsonl`

FAIL if: the agent answers from memory with no citations, or no `.bk/` appears in the scratch dir.

## Test 2 — build question (both lanes)

Ask: **"Add an average win percentage metric to the team entity"**

Expect:
- The agent consults the **semantics docs** (format) AND the **library** (methodology) BEFORE writing anything
- The proposed metric is a **ratio of sums** (`SUM(wins)/SUM(games)`), NOT an average of per-game percentages — and the answer names that trap (it comes from book-7 · ground-a-metric)

FAIL if: the agent writes a metric without consulting, or proposes `AVG(win_percentage)`.

## Test 3 — reference question (docs lane only)

Ask: **"How does Lynk resolve relationships between entities?"**

Expect: answer from `semantics_docs` (schema.yml mechanics). The library should stay **silent** — no new `.bk/fetch/` files for this question.

FAIL if: the library pipeline runs for a pure reference question.

## Test 4 — control (everything silent)

Ask: **"Rename the README file and fix the typo"** (in the scratch dir; create a README first if you like)

Expect: no library, no router injection, no `.bk/` activity. Just a normal answer.

FAIL if: any library machinery fires on a non-layer request.

## Test 5 — read-only enforcement

From the scratch dir run:

```bash
<path-to-this-repo>/lynk-wiki/bk read book-3-progressive-disclosure:three-stages   # should print the page
<path-to-this-repo>/lynk-wiki/bk log book-3-progressive-disclosure --entry "x"     # should REFUSE
```

Expect the second command to fail with: *"read-only rendered bundle (BUNDLE_VERSION present)"*.
Also verify NO `.bk/` directory ever appears **inside the plugin folder** — all state must be in your scratch project.

FAIL if: any write verb succeeds, or the plugin dir gains a `.bk/`.

## Test 6 — the write nudge (optional, behavioral)

In a FRESH session (fresh scratch dir), create `.lynk/entities/test.yml` with any content **by asking the agent to write it directly** without mentioning books. After the write, the agent should receive a nudge and consult the library to reconcile.

## What to report

For any failure: the question asked, the session transcript tail, the contents of `<scratch>/.bk/` (reads + fetch + gaps), and the plugin version from `BUNDLE_VERSION`.
Gaps note: if the librarian ever answers "No relevant books found", that's recorded demand in `.bk/gaps.jsonl` — include it in the report, it's useful signal, not a bug.

## Known limitations (don't file these)

- Book-writing / sustain features intentionally absent — this bundle is read-only.
- Governance books (book standard, plugins) intentionally not shipped.
- `semantics_docs` and book-7 overlap on semantic-layer content (docs = WHAT, book = HOW) — a known open item.
- Bash-based file writes (`echo >> file`) bypass the write-nudge hook.
