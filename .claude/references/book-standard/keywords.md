---
type: rule
description: Every chapter carries a keywords list — the synonym surface a search hits when the asker uses different words than the chapter.
load_when: Writing a chapter's frontmatter, or diagnosing why a search or grep misses a chapter that answers the question.
keywords: [keywords, synonyms, aliases, grep, search, findability]
rules:
  - id: structure/keywords
    severity: warn
    scope: chapter
    statement: Every non-reserved chapter's frontmatter carries a keywords flow-list of synonyms and adjacent terms a searcher might use that the chapter's title and description do not already contain.
    gate_criteria: >
      A chapter passes when its frontmatter carries a keywords flow-list
      (e.g. [compaction, lost in the middle]) whose entries add search
      surface — synonyms, community terms, tool and system names — beyond
      words already present in the H1 and description. It fails when the
      list is missing, or when every entry merely restates title/description
      words (zero added surface). Reserved chapters (index.md, log.md) are
      exempt. There is no upper bound, but entries must plausibly be terms
      a searcher would use — padding with unrelated terms to game routing
      fails toc-discipline's honesty bar. Severity is warn while the
      existing shelf is retrofitted; hardens to error with structure/load-triggers.
---

# Keywords

**What it is** — the third findability surface. The H1 + description serve the reader who *navigates* ([toc-discipline](toc-discipline.md)); the `load_when` trigger serves the reader who arrives with a *situation* ([loading-triggers](loading-triggers.md)); **keywords** serve the reader who *searches* — and searchers use their own words, not the chapter's. A chapter about compression that never says "compaction" or "summarization" is invisible to every grep for those terms.

**Mechanics** — what earns a slot in the list:

| Earns a slot | Doesn't |
|---|---|
| Synonyms the body doesn't use ("compaction" on a compression chapter) | Words already in the H1 or description (zero added surface) |
| Community terms of art ("lost in the middle", "L1/L2/L3") | Generic filler ("agent", "context" on every chapter) |
| System and tool names the concept implicates (MemGPT, OKF) | Unrelated bait terms (routing-gaming fails the honesty bar) |

**Takeaway** — **keywords are the synonym surface: they catch the searcher whose vocabulary differs from the writer's — the reader every other surface misses.**

**Example** *(real — a sibling book's retrofit, 2026-07-19)* — its `context-rot` chapter never contains the community phrase "lost in the middle", and its `compression` chapter reads naturally without the word "compaction"; both terms are exactly what a practitioner would grep for. The keywords lists added both — sixteen chapters gained a search surface their prose deliberately doesn't carry.

**In this system** — deterministic search (`bk grep`) is the fallback when index routing misses; keywords are what make the fallback land. Presence of the list is checked by lint; whether entries add surface is the gate's judgment call. → See [loading-triggers](loading-triggers.md) — its sibling surface for situation-routing — and [toc-discipline](toc-discipline.md) for the honesty bar keyword lists must not undermine.
