---
name: Convergent evolution on the file shape
description: Independent systems converged on the same shape — small markdown files plus YAML frontmatter plus progressive disclosure — evidence the pattern is load-bearing, not fashion. Read when questioning the substrate — why plain markdown files and frontmatter instead of a database, or whether the file shape is arbitrary.
---

Several teams, solving different problems, independently landed on the same container for agent-read knowledge: small markdown files plus YAML frontmatter plus progressive disclosure. Convergence under independent selection is evidence a pattern is load-bearing rather than fashionable (derived: unrelated designs reaching one answer points at a real constraint). The convergence, from public sources:

| System | Owner | The shape |
|---|---|---|
| OKF (Open Knowledge Format) | Google Cloud, BigQuery team | Directory of markdown + YAML frontmatter, one concept per file |
| SKILL.md / Agent Skills | Anthropic | Markdown skill + frontmatter, three-stage disclosure |
| `.mdc` rules | Cursor | Markdown rule files with frontmatter |
| CLAUDE.md / AGENTS.md | Anthropic / community | Markdown behavioral-instruction files |
| MemFS / Context Repositories | Letta | Markdown files in a git-backed filesystem (source: letta.com/blog/context-repositories, Feb 2026) |

OKF specifics (source: github.com/GoogleCloudPlatform/knowledge-catalog — SPEC.md v0.1, June 2026): a directory bundle of markdown plus YAML frontmatter, one concept per file, `index.md` as the listing layer, `log.md` as history, only `type` required in frontmatter. OKF standardizes the *container*, not the vocabulary — it bets that an LLM reader makes a standardized vocabulary unnecessary, so adopting the container costs almost nothing. A related caution: *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* (ETH Zurich, 2026) found such context files often hinder agents unless limited to non-inferable detail — the container is cheap, but what you pour into it still has to earn its place.

**When five independent systems reach the same markdown-plus-frontmatter-plus-progressive-disclosure shape, that shape is a constraint the problem imposes, not a trend to follow.** A library built on this shape ships the OKF pattern nearly field-for-field: folder = book, `.md` = chapter, `index.md` and `log.md` reserved, metadata in frontmatter — a convergent container adopted rather than invented.

The convergence is why the right substrate for agent-read knowledge is plain files, not a database — the shape is proven repeatedly under independent selection. This chapter is the full home for the evidence; a layout rule can point here rather than restating it (one concept, one home). See [living-sources](living-sources.md) for how these files stay accurate as they grow, and [progressive-disclosure](progressive-disclosure.md) for the disclosure mechanism they all share.
