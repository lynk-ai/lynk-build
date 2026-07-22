---
type: rule
description: One concept per page, single H1 as title, OKF-style frontmatter — the file-level rules.
load_when: Creating or renaming a page file — its filename, frontmatter, and how many concepts it may hold.
keywords: [frontmatter, H1, filename, kebab-case, one concept per page, container]
rules:
  - id: structure/one-concept-per-page
    severity: error
    scope: page
    statement: A page holds exactly one concept, decision, rule, or pattern.
    gate_criteria: >
      A page passes when everything in it serves one nameable concept — the H1's
      promise. It fails when it defines or regulates two separable concepts that a
      reader could want to cite independently; the fix is a split. Exceptions: the
      reserved index page; a rule page whose two rules always fire
      together on the same trigger and share one home (they read as one
      contract); and pages where splitting would leave a fragment too
      trivial to stand alone (a sentence or two) — in that case the minor point
      may stay, marked as an aside.
  - id: structure/single-h1
    severity: error
    scope: page
    statement: A page opens with exactly one H1 — its title; sub-points use deeper headings.
    gate_criteria: >
      Exactly one line starting with a single '#' must exist and it is the page
      title. Zero H1s or more than one is a failure. Checked deterministically by
      lint; no exceptions.
  - id: structure/frontmatter-required
    severity: error
    scope: page
    statement: Every page carries frontmatter with a type and a one-sentence description that honestly summarizes the body.
    gate_criteria: >
      The page passes when frontmatter contains a non-empty type and a non-empty
      one-sentence description whose promise matches the body's content. Presence
      is checked by lint; honesty of the description is judged against the body
      (see structure/label-matches-content for the body-vs-label comparison).
      Fails on missing keys, empty values, or a description about a different
      concept than the page delivers.
  - id: structure/frontmatter-subset
    severity: error
    scope: page
    statement: Frontmatter uses the strict subset — scalar values, flow-style lists, and the documented nested rules shape only.
    gate_criteria: >
      Frontmatter must parse under bk's strict subset parser: 'key: value'
      scalars, flow lists like [a, b], and the documented rules block. Tabs,
      other block nesting, or unterminated structures fail. Checked
      deterministically by lint; no exceptions.
  - id: structure/kebab-filename
    severity: error
    scope: page
    statement: A page's filename is the kebab-case promise of its concept.
    gate_criteria: >
      Filenames must match ^[a-z0-9-]+\.md$ and name the page's concept (not
      notes3.md). The slug pattern is checked deterministically by lint; whether
      the name matches the concept is judged with the same standard as
      structure/label-matches-content. index.md is reserved and
      exempt.
---

# Page anatomy

**What it is** — the file-level rules for a page: what one page holds, how it's named, and what metadata it opens with. The template ([page-template](page-template.md)) governs the *inside*; this page governs the *container*.

**Mechanics**

| Rule | Detail |
|---|---|
| One concept per page | A page holds exactly one concept, decision, rule, or pattern. Two concepts sharing a page is a split waiting to happen. |
| Single H1 | The page opens with one `# Heading` — its title. Sub-points use `##`/`###` inside. The H1 is what the TOC and routing see. |
| Frontmatter | YAML at the top, OKF shape: `type` (required — principle · rule · template · recipe) and `description` (one sentence — reused verbatim by the index listing). |
| Filename | Kebab-case of the concept: `context-rot.md`, not `notes3.md`. The filename is a promise about the content. |

**Takeaway** — **a page is one concept in one file with one H1 and honest metadata — anything else breaks routing before a reader ever opens it.**

**Example** *(constructed, illustrative)* — a `hook-vs-router` page carries `type: principle` and the description "Hooks fire themselves and skip silently; routers are explicit and fail closed…". An agent scanning the index knows whether to open it without reading a line of the body.

**In this system** — the gate's structure checklist starts here: reject a draft whose page has two H1-worthy concepts, a missing `type`, or a description that doesn't match the body. → See [toc-discipline](toc-discipline.md) for why the H1 matters downstream.
