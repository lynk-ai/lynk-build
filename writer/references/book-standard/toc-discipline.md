---
type: rule
description: The table of contents is derived from headings and descriptions — keep them clean or routing breaks.
load_when: Writing a page's H1 or description, or diagnosing why routing keeps picking the wrong page.
keywords: [headings, descriptions, labels, routing, TOC, mislabeled]
rules:
  - id: structure/label-matches-content
    severity: error
    scope: page
    statement: A page's H1 and description promise exactly what its body delivers — labels are the routing interface.
    gate_criteria: >
      A page passes when a reader who chose it from its H1 plus description alone
      would find the body answers that promise — nothing materially different,
      nothing materially missing. It fails when the heading is vague ('Notes on
      stuff'), when the body drifts into a second topic the label doesn't
      announce, or when the description oversells or undersells the content.
      This is a judgment rule: minor stylistic mismatch passes; a routing agent
      being misled is the failure bar.
---

# TOC discipline

**What it is** — the rule that headings and descriptions are *load-bearing*. The book's table of contents (its `index.md` listing) is derived from each page's H1 + frontmatter description. Routing agents decide which page to open from the TOC alone — they never scan bodies. A vague heading doesn't just read badly; it makes the page unreachable.

**Mechanics**

| Rule | Bad | Good |
|---|---|---|
| The H1 names the concept | `# Notes on stuff we discussed` | `# Context rot` |
| The description answers "is this the page I need?" | "Some thoughts about links." | "Within-book links are relative markdown pointers an agent follows, used liberally; cross-book references are plain-text canonical names — never links — routable as Leads." |
| Heading promises = body delivers | H1 says "TOC discipline," body drifts into link syntax | One concept, matching its label — split anything that drifted in |

**Takeaway** — **an agent picks pages by their labels, so the label is the interface: mislabel a page and you've deleted it for every reader who routes by the TOC.**

**Example** — CandleKeep's enricher exists almost entirely because of this rule's violation: a book arriving as `scan_001.pdf` with no TOC is dead weight the librarian can't route to, until the metadata is repaired. Our books never need that repair if headings are honest from the first write.

**In this system** — the gate's structure checklist compares each page's H1 + description against its body (label ≠ content → reject). Routing quality at both stages — the librarian's book pick and each scout's chapter pick — is downstream of this one rule. → See [page-anatomy](page-anatomy.md) for the H1 rules; the TOC itself lives in the book's index.md.
