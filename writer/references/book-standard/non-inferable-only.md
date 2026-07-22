---
type: rule
description: A book holds only what the reader can't infer or fetch elsewhere — restating the obvious is rot, not thoroughness.
load_when: Deciding whether content earns a place in a book at all — the admission test before any writing starts.
keywords: [admission, inferable, fetchable, durable, restatement, tribal knowledge]
rules:
  - id: quality/non-inferable-only
    severity: error
    scope: page
    statement: Content earns admission only if the reader couldn't infer it, fetch it elsewhere, or outlive it — point instead of copying.
    gate_criteria: >
      A page passes when its substance is knowledge a capable reading agent could
      not derive from what it already sees, could not fetch from a source it can
      already reach (the codebase, official docs, another page — those get
      pointers, not copies), and will remain true long enough to be read twice.
      It fails when it is mostly restatement of the inferable or fetchable.
      Exceptions: brief orientation sentences that frame the non-inferable
      content, and index/summary listings whose whole job is restatement for
      navigation. Fetchable material is additionally admissible as condensed
      MULTI-SOURCE SYNTHESIS where the assembly itself is the value — traps,
      contradictions across sources, version hazards, curation a reader would
      spend hours reassembling; a one-hop restatement of a single reachable
      source is still rejected.
---

# Non-inferable content only

**What it is** — the admission rule: content earns a place in a book only if the reading agent **couldn't get it otherwise** — not from its training, not from the environment it can inspect, not from another book already on the shelf. Everything else is weight without lift.

**Mechanics** — three tests before content lands:

| Test | Fails when… |
|---|---|
| **Inferable?** | The reader could derive it from what it already sees (a capable agent doesn't need "functions should be small" restated). |
| **Fetchable?** | It lives somewhere the reader can already reach — the codebase, a tool's own docs, another page (→ point, don't copy). |
| **Durable?** | It'll be stale before it's read twice (session-specific detail belongs in the session, not the shelf). |

Sourced grounding: *Evaluating AGENTS.md: Are Repository-Level Context Files Helpful for Coding Agents?* (ETH Zurich, 2026; 138 repositories, 5,694 pull requests) found LLM-generated context files cut task success ~3% while adding over 20% inference cost — human-written ones gained ~4% only when limited to **non-inferable details**: custom commands, unusual conventions, tribal knowledge. CandleKeep's guide encodes the same instinct as its "do NOT upload" list: no code files, nothing already in the codebase.

**Takeaway** — **before writing, ask "could the reader get this without the book?" — if yes, the page subtracts value: it costs attention and adds nothing.**

One licensed exception (added 2026-07-21, from evaluation findings): fetchable material may be admitted as **condensed multi-source synthesis** when the assembly is the value — the page collects traps, cross-source contradictions, and version hazards a reader would burn hours reassembling from the individual sources. The test: if the page's substance could be replaced by a single link, reject it; if replacing it requires a reader to fetch and reconcile several sources, the synthesis has earned admission.

**Example** *(constructed, illustrative)* — two candidate pages about a build system. *"Run the build with `make build`"* — inferable from the Makefile in seconds; rejected. *"CI builds fail silently if the cache volume predates the v3 runner — wipe it first"* — non-inferable tribal knowledge that costs an afternoon to rediscover; admitted. The second sentence is why libraries exist.

**In this system** — a gate check (quality dimension): drafts get walked for inferable/fetchable/stale content, and pages that are mostly restatement bounce with this rule cited. It's context rot applied at admission time: the cheapest token to manage is the one never written. → See [page-budget](page-budget.md) — the same discipline applied to size instead of existence.
