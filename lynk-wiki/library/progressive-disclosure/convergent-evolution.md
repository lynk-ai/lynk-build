---
type: reference
description: Independent systems converged on the same shape — small markdown files plus YAML frontmatter plus progressive disclosure — which is evidence the pattern is load-bearing, not fashion.
---

# Convergent evolution on the file shape

**What it is** — the observation that several teams, solving different problems, independently landed on the *same* container for agent-read knowledge: **small markdown files + YAML frontmatter + progressive disclosure**. Convergence under independent selection is evidence a pattern is load-bearing rather than fashionable (derived from the reasoning of convergent evolution: unrelated designs reaching one answer points at a real constraint).

**Mechanics** — the convergence, all sourced (research-brief-2026-07, §"Convergent evolution on the file shape"):

| System | Owner | The shape |
|---|---|---|
| OKF (Open Knowledge Format) | Google Cloud, BigQuery team | Directory of markdown + YAML frontmatter, one concept per file |
| SKILL.md / Agent Skills | Anthropic | Markdown skill + frontmatter, three-stage disclosure |
| `.mdc` rules | Cursor | Markdown rule files with frontmatter |
| CLAUDE.md / AGENTS.md | Anthropic / community | Markdown behavioral-instruction files |
| MemFS / Context Repositories | Letta | Markdown files in a git-backed filesystem (source: letta.com/blog/context-repositories, Feb 12 2026) |

The layering stack the brief draws from these (source: research-brief-2026-07): **llms.txt / agents-md-on-websites** (discovery) → **AGENTS.md / CLAUDE.md / .mdc** (behavioral instructions) → **SKILL.md** (procedures) → **OKF** (domain knowledge) → **MCP / agents.json** (actions).

OKF specifics (source: github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md — v0.1, announced June 12 2026): a directory bundle of markdown + YAML frontmatter, one concept per file, `index.md` as the progressive-disclosure/listing layer, `log.md` as history, and only `type` required in frontmatter.

Honest framing (source: talk §B, docs/talk-outline.md): OKF standardizes the *container*, not the vocabulary — it bets that an LLM reader makes a standardized vocabulary unnecessary, so adopting the container costs almost nothing. A related caution fits here: ETH Zurich (via InfoQ, Mar 2026) found AGENTS.md-style context files often *hinder* agents, recommending human-written context be limited to non-inferable detail (source: infoq.com/news/2026/03/agents-context-file-value-review/; this finding's home is the Book Standard · `non-inferable-only`) — the container is cheap, but what you pour into it still has to earn its place.

**Takeaway** — **when five independent systems reach the same markdown-plus-frontmatter-plus-progressive-disclosure shape, that shape is a constraint the problem imposes, not a trend to follow.**

**Example** — this very library ships the OKF shape nearly field-for-field: folder = book, `.md` = page, `index.md` and `log.md` reserved, `type` in frontmatter. We adopted a convergent container rather than inventing one.

**In this system** — the convergence is why our substrate is plain files, not a database — the shape is proven repeatedly under independent selection. This is the full home for the convergence evidence; the Book Standard · `library-layout` keeps a one-line pointer here rather than re-stating it (one concept, one home). → See the Best Context book · `living-sources` for how these files stay accurate as they grow, and [three-stages](three-stages.md) for the disclosure mechanism they all share.
