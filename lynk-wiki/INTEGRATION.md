# Integrating the lynk-book library into `lynk-wiki`

Rendered 2026-07-16 from lynk-book @ 83a03a8. Contents of this folder drop into the
plugin ROOT of `lynk-wiki` (merge, don't replace, if folders already exist).

## What this gives your plugin
A knowledge pipeline the builder agent consults instead of guessing:
`lynk-wiki:librarian` routes BOOKS by metadata → one `lynk-wiki:book-reader`
(chapter scout) per routed book returns POINTER lines → a SubagentStop hook
fetches exactly those chapters to `.bk/fetch/<agent>.txt` in the consumer's
project → the orchestrating agent Reads that file and answers from primary
text with (book · page) citations. The `library` skill is the orchestration
recipe; `bk-search` is the shared CLI reference the agents preload;
`semantic-layer-audit` is the Lynk audit capability.

## Install steps
1. Copy `skills/`, `agents/`, `scripts/`, `bk`, `library/`, `BUNDLE_VERSION`
   into the plugin root (components must sit at the ROOT, not inside
   `.claude-plugin/`).
2. Merge `hooks.fragment.json` into your `hooks/hooks.json` (all four entries: SessionStart note, SubagentStop fetch, UserPromptSubmit router, PostToolUse nudge).
   If you already have a SessionStart hook, append ours to your list.
3. Nothing else: agents resolve the CLI via `CLAUDE_PLUGIN_ROOT`, and all
   state (reads log, gaps, fetch files) lands in the consumer project's
   `.bk/` via `BK_DATA` — the plugin cache is never written to.

## The environment contract
- `CLAUDE_PLUGIN_ROOT` → where books + `bk` live (your plugin's cache dir).
- `BK_DATA` (set by the hook commands) → `<consumer project>/.bk` for all state.
- Roles are telemetry: every read is logged with `BK_ROLE` + content hash.

## Rules
- **This is the PUBLISHED shelf.** Governance/packaging books (the warehouse)
  stay in the lynk-book repo by design — questions about them will miss and
  land as gaps, which is correct demand signal.
- **Never edit `library/` here.** Books are gate-verified in the lynk-book
  repo; they update only by rendering a new bundle (`scripts/bundle.sh`).
  Treat `BUNDLE_VERSION` as the provenance stamp.
- **Gaps are a feature.** When the librarian can't route or a scout finds an
  empty book, a demand record lands in the consumer project's
  `.bk/gaps.jsonl` (with a `context` sentence). Collect these — they are the
  library's writing backlog. (Automated phone-home is deferred by design.)
- The write path (book-writer/gate agents, sustain loop) does NOT ship —
  and `bk` itself refuses write verbs beside a BUNDLE_VERSION marker, so the
  bundle is mechanically read-only, not just by convention.

## Verifying the integration
Run your plugin against a scratch project and ask a library question
("what does the standard say about interlinks?"). Expect: librarian routing
list (books + objectives, no page slugs) → scout POINTER lines → a
`[library pointer fetch]` line naming `.bk/fetch/<agent>.txt` → answer with
(book · page) citations. Check `.bk/reads/*.jsonl` in the scratch project:
`role=hook` entries must match the scouts' pointers exactly.
