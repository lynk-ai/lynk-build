---
type: principle
description: The mechanism of lazy loading in three stages — discovery, activation, execution (the community's L1/L2/L3) — codified by Anthropic's Agent Skills and general to any index-plus-pages library.
---

# The three stages

**What it is** — the mechanism that charges the two prices of [the-economics](the-economics.md). Anthropic's Agent Skills codify progressive disclosure as three stages, and the shape generalizes to any library built from an index, pages, and linked detail (source: Anthropic Agent Skills, three-stage progressive disclosure — research-brief-2026-07).

**Mechanics** — each stage loads more and is paid less often:

| Stage | What loads | Cost |
|---|---|---|
| **Discovery** | Name + one-line description, for *everything* that exists (~100 tokens each). | Always paid. |
| **Activation** | The full body of a page, once a task matches its description. | Paid only on match. |
| **Execution** | Bundled references and details the body links to. | Paid only when actually touched. |

Community write-ups label these same three stages Level/Layer 1–3 — commonly abbreviated **L1 / L2 / L3** — mapping onto discovery/activation/execution (sources, both accessed 2026-07-15: hatchworks.com/blog/claude/skills-architecture/ labels them "Level 1: Metadata / Level 2: Instructions / Level 3: Resources"; newsletter.swirlai.com/p/agent-skills-progressive-disclosure labels them "Layer 1: Discovery / Layer 2: Activation / Layer 3: Execution"). Same three stages, different names.

The generalization (derived): any library with an *index* (names + one-liners), *pages* (bodies), and *linked detail* (references a body points at) implements these same three stages, whatever the substrate — a cloud API, a skills folder, or a directory of markdown files. The stages are a shape, not a specific product.

Is there an L4? No (derived): a level is defined by *when* content enters context, and there are only three such moments — always, on match, on touch. What looks like an L4 is execution recursing — a reference that points at another reference is the third ring applied again, not a new ring. The pipeline note in "In this system" below, where discovery→activation runs twice, is that same recursion happening live.

**Takeaway** — **discovery loads a pointer to everything, activation loads a body on match, execution loads detail on touch — three widening rings, each paid less often than the last.**

**Example** — Anthropic's Agent Skills (real): a skill exposes a name and description always; its `SKILL.md` body loads only when the task matches; its bundled files load only when the procedure reaches them. The pattern spread fast on this shape — per research-brief-2026-07, Agent Skills reached ~40 clients within ~90 days of the spec opening (Dec 18, 2025) and ~500K skills across marketplaces.

**In this system** — every book's `index.md` is the discovery layer; each page body is activation; the interlinked detail a page points at is execution. The pipeline now runs discovery→activation twice — the shelf is the librarian's discovery layer, each book's TOC is its scout's — and activation is deterministic (a hook fetches the pointed chapters). → See [pointers-not-content](pointers-not-content.md) for what may live in the discovery layer, [read-vs-execute](read-vs-execute.md) for the two cost shapes inside execution, and [the-economics](the-economics.md) for why the three-stage split is what keeps cost flat.
