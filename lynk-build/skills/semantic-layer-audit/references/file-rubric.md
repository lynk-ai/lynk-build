# Per-file rubric — what a good `.lynk/` `.md` file is

The checklist each file is judged against. Two passes: **A — the file alone**, **B — the
file in its graph**.

> CANONICAL HOME NOTE: this rubric is the checklist form of the v2 spec. Its intended home is
> **next to the v2 docs** (single source of truth). This copy is the working draft; when the
> docs adopt it, replace this file with a pointer to avoid drift (book-1 one-concept-one-home).

## Pass A — the file on its own
- **Frontmatter** — present, well-formed; `name` matches the folder (v2 `markdown-format`).
- **Description** — one honest line that summarizes the body; specific enough to be
  load-bearing (an agent can judge relevance from it alone). Not vague, stale, or generic.
- **Each field/metric description** — accurate vs the SQL it documents; makes its point; not
  bloated. (book-2 `sourced-statements` for any factual claim.)
- **Progressive disclosure** — right amount: no detail inlined that every load pays for and
  most loads don't need; no over-splitting into unnavigable fragments (book-3
  `pointers-not-content`, `when-to-deepen`).
- **Value smells** — scan for the classes in `bug-taxonomy.md`; each becomes a candidate with
  proposed verification SQL + an external anchor.

## Pass B — the file in its graph
- **Coherence** — who `@`-injects / links to it (pointed-by) and what it points at (points-at)
  cohere; loaded when it should be; no cycles; no danglers.
- **One home / duplication** — nothing here is restated elsewhere; if it is, one copy is the
  home and the rest point (book-1 `one-concept-one-home`).
- **No contradiction** — a term/definition here doesn't conflict with core or another domain.
- **Placement** — the fact is in the right layer (core vs domain); shared truth → core,
  domain-specific working truth → the domain.

## Verdict shape
Each finding: `{file, line?, pass: A|B, class, claim, proposed_verification_sql?, anchor?,
rule_cited}`. A value finding with no way to prove it against execution and no structural
basis is **dropped** or marked `judgment-only` with the book principle it rests on.
