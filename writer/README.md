# writer/ — the book-writing toolkit (internal only)

Creates and enriches books in `library/` through a verified pipeline:
**DIAGNOSE → RESEARCH → AUTHOR ⇄ VERIFY → PROMOTE**. Nothing lands in the
library without an independent `APPROVED` verdict — readers trust the shelf
blindly, so a bad write is worse than no write.

This directory is **not a plugin and is never shipped**. It lives only in the
authoring repo; the user-facing plugin receives the rendered, read-only
library. Write ability is enforced by location, not permission checks.

## Layout

```
writer/
├── skills/book-writer/SKILL.md   the orchestrator (context: fork — runs isolated)
├── agents/
│   ├── writer-research.md             gathers cited findings (web or repo; read-only)
│   ├── book-author.md            writes v2 drafts under drafts/ only
│   └── book-verifier.md          adversarial gate (read-only; tri-state verdict)
├── references/book-standard/     the authoring standard, read live by author + verifier
└── drafts/                       staging; promoted slugs leave a verdict.json audit trace
```

## Activation (project-level, this repo only)

Symlink (or copy) into the repo's `.claude`:

```sh
mkdir -p .claude/skills .claude/agents
ln -s ../../writer/skills/book-writer .claude/skills/book-writer
ln -s ../../writer/agents/writer-research.md .claude/agents/writer-research.md
ln -s ../../writer/agents/book-author.md .claude/agents/book-author.md
ln -s ../../writer/agents/book-verifier.md .claude/agents/book-verifier.md
```

Invoke as `/book-writer` with a brief: the ask verbatim · what was searched
and missed · the specific gap · target book/chapter if known.

## Design plan

See `writer_plan.md` at the repo root — section "FINAL PLAN (2026-07-20)".
