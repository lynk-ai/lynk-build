# Changelog

A chronological record of how this book evolves. Most recent first.

## [2026-07-16] Cross-book links converted to name-references (books-are-independent rule; batch A) — 13 links converted, meaning preserved.

## [2026-07-15] Research-driven update: new page read-vs-execute + three-stages additions
New page `read-vs-execute` (Part I): inside the execution stage, two cost shapes — detail READ into context (pay the full token price of the text) vs code EXECUTED outside it (the code never loads; only its output is paid); prefer reading for material the model reasons over, executing for deterministic work. Sourced to `docs/skills-spec-notes.md` (the `scripts/`/`references/` split); worked live example is our fetch stage (`scripts/fetch-pointers.sh` runs `bk read` deterministically, `BK_ROLE=hook` telemetry in `.bk/reads/`, chapters dropped to `.bk/fetch/`, only Read chapters paid). Two additive edits to `three-stages` (no meaning replaced, no supersede notes): the L1/L2/L3 vocabulary bridge (community shorthand for Discovery/Activation/Execution, web-verified 2026-07) and a derived 'is there an L4?' answer (no — a level is defined by WHEN content enters context, and there are only three moments; apparent L4 is execution recursing, the same third ring reapplied). Index restored to its curated Part I–IV + Sources shape with the new page inserted in Part I (the mechanical `bk index --write` had flattened it and dropped the Sources section).

## [2026-07-14] Pipeline restructure (pointer pipeline: librarian routes books, scouts point at chapters, hook fetches). the-economics.md and three-stages.md 'In this system' passages updated to match — librarian scans one line per book, per-page scan is each scout's; discovery→activation now runs twice with deterministic hook-fetched activation.

## [2026-07-12] Maintenance: ETH-Zurich citation cross-link
convergent-evolution's ETH-Zurich (context-files-hinder) citation now points to its home in Book 2's non-inferable-only, resolving the duplicate-citation warning from the 2026-07-09 self-audit (new→old maintenance pass).

## [2026-07-07] Added when-to-deepen (Part IV)
New page: when-to-deepen — the judgment of whether to split sideways (page-budget) or deepen a level (graduation) when a home outgrows itself. The principle lives here (Book 3, the concept's home); Book 2's page-budget and graduation rules now cite it for the *whether/which*, keeping the *how* in the gate-enforced standard. Cross-pointers added both ways.

## [2026-07-07] Book created — graduated from Book 1's progressive-disclosure page
Five pages written, following the concept template. Part I (the wager): the-economics (cost scales with what a task uses, not with what exists), three-stages (discovery → activation → execution, codified by Anthropic's Agent Skills and generalized). Part II (the opinion): habit-vs-contract (you can't build a product on a habit — enforcement makes routing safe), pointers-not-content (discovery carries pointers under budget; CandleKeep's ≤2KB sticky note). Part III (the evidence): convergent-evolution (OKF, SKILL.md, Cursor .mdc, CLAUDE.md, Letta MemFS landed on one file shape). In the same change, Book 1's `progressive-disclosure` page was shrunk to a stub (definition + takeaway + pointer + dated supersede note) per structure/one-home-graduation; Book 1's index and changelog updated to match.

## [2026-07-07] Book created
Empty scaffold — index and changelog only.
