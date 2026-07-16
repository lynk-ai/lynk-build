---
type: reference
description: The Agent Skill format precisely — a directory with SKILL.md (YAML frontmatter + markdown body), optional scripts/references/assets, the frontmatter field table, and the three disclosure budgets.
---

# What a skill is

**What it is** — an Agent Skill is a **directory** containing at minimum a `SKILL.md` file: YAML frontmatter plus a markdown instruction body. Optional subdirectories carry the rest: `scripts/` (executable code), `references/` (on-demand docs), `assets/` (templates, data) (source: `docs/skills-spec-notes.md`, "The format, precisely"). It is an open standard — developed by Anthropic, released and community-governed at github.com/agentskills/agentskills (source: same).

**Mechanics** — the complete frontmatter field set (source: `docs/skills-spec-notes.md`, frontmatter table):

| Field | Required | Constraints |
|---|---|---|
| `name` | yes | 1–64 chars; lowercase alphanumerics + hyphens; no leading/trailing or consecutive hyphens; **must match the parent directory name** |
| `description` | yes | 1–1024 chars; says **what it does AND when to use it**, with keywords a task can match against |
| `license` | no | a license name or pointer to a bundled file |
| `compatibility` | no | 1–500 chars; only when the skill has real environment requirements ("Requires git, docker, jq") |
| `metadata` | no | arbitrary string→string map for client-specific extras; use distinctive keys |
| `allowed-tools` | no | space-separated pre-approved tools, e.g. `Bash(git:*) Read` — **experimental**, support varies |

The body loads under three disclosure budgets (source: `docs/skills-spec-notes.md`, "Progressive disclosure budgets"): **metadata** (name + description, ~100 tokens, loaded at startup for *every* skill); **instructions** (the full SKILL.md body on activation — recommended < 5000 tokens and under 500 lines); **resources** (scripts/references/assets, loaded only when required).

Those budgets are three loading stages. **This page owns the skill *format*; the Progressive Disclosure book · `three-stages` page owns the disclosure *mechanism*** — why layering by load-frequency keeps cost flat is its concept, not restated here (one concept, one home). three-stages already uses Agent Skills as its worked example; read it for the *why*, read this for the *what*.

**Takeaway** — **a skill is a named directory whose `SKILL.md` frontmatter (name matching the directory, description saying what + when) is always in context, whose body loads on match, and whose bundled resources load only when touched.**

**Example** — our own live skill `.claude/skills/library/SKILL.md` (real, 96 lines): `name: library` matches its directory; the description states both what ("Runs the library pipeline — librarian routes by metadata, book-readers read cited pages") and when ("Use when the user asks what the books/library/standard say…"). It ships no `scripts/`, `references/`, or `assets/` — a valid minimal skill. *(superseded 2026-07-14: previously "83 lines" — SKILL.md grew to 96 in the pipeline restructure; see log.md)*

**In this system** — adoption is why this format is worth a book: per `docs/research-brief-2026-07.md`, Agent Skills reached ~40 clients within ~90 days of the spec opening (Dec 18, 2025) and ~500K skills across marketplaces — cross-vendor (Anthropic-originated, adopted by OpenAI, Google, Microsoft, JetBrains, Databricks, Snowflake tooling per `docs/skills-spec-notes.md` ecosystem list). Our library skill *is* an Agent Skill; the librarian/gate/writer it names are subagents. → See [what-makes-a-skill-good](what-makes-a-skill-good.md) for the quality bar, and the Progressive Disclosure book · `three-stages` for the disclosure economics this format rides on.
