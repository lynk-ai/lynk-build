---
type: rule
description: Every book states when to load it and every page carries a load_when trigger — agents route on triggers, not titles.
load_when: Writing or auditing a book's findability — deciding how a reader with a task (not a topic) finds the right page.
keywords: [triggers, findability, load when, routing, red flags, symptom]
rules:
  - id: structure/load-triggers
    severity: warn
    scope: book
    statement: A book's index carries a "When to load this book" section, and every non-reserved page's frontmatter carries a load_when line phrased as a trigger condition, not a subject label.
    gate_criteria: >
      A book passes when its index.md contains a "When to load this book"
      section with concrete trigger bullets — including at least one negative
      trigger (what NOT to load it for) — and every non-reserved page's
      frontmatter carries a load_when value naming the situation that should
      cause a reader to open the page ("answers degrade as the session
      grows", "deciding whether to split or merge"), distinct from the
      description's subject summary. It fails when the section is missing,
      when pages lack load_when, or when a load_when merely restates the
      topic ("about context rot") instead of naming the triggering
      situation. Reserved pages (index.md) are exempt. Severity is warn
      while the existing shelf is retrofitted; hardens to error once every
      shipped book carries triggers.
---

# Loading triggers

**What it is** — the findability rule: a description says what a page is *about*; a **trigger** says *when to open it*. Routing agents arrive with a task or a symptom, not a topic name — so every book must state when it should be loaded, and every page must carry the situation that makes it the right read. Labels answer "is this the page I was looking for?"; triggers answer "should I be looking for it at all?"

**Mechanics**

| Level | Requirement | Form |
|---|---|---|
| Book | A "When to load this book" section in `index.md` | Trigger bullets, including at least one *negative* trigger — what this book is **not** for (mis-routing wastes more than missed routing). |
| Page | A `load_when:` line in frontmatter | The triggering situation, not the subject: "answers degrade as the session grows", never "about context rot". |
| Symptom routing | Optional but recommended: a "Red flags" table in `index.md` | Symptom → page, so a reader arriving with a problem (not a concept) still lands right. |

The test for a good trigger: could a router holding only the trigger — never the body — decide correctly whether to open the page for a given task? If the trigger restates the title, it adds nothing the label didn't already give.

**Takeaway** — **agents route on triggers, not titles: a page without a load_when is findable only by readers who already know it exists.**

**Example** *(real — the first retrofit, 2026-07-19)* — a sibling book on the shelf: its pages carried honest subject descriptions ("Poisoning, distraction, confusion, clash — four distinct ways context breaks an agent"), yet an agent holding the symptom *"my agent keeps repeating a reverted decision"* had no surface naming that situation. After the retrofit, `four-failure-modes`' trigger — "an agent's output feels off and you need to identify which context failure is causing it" — plus the index's red-flag row route that symptom in one hop, no body read.

**In this system** — bar seeded from *Writing Books for AI Agents* (Ch. 10), which ranks missing loading triggers as its single CRITICAL anti-pattern ("agents route on triggers, not titles"); adopted by decision of the human maintainer, 2026-07-19. This rule is [toc-discipline](toc-discipline.md)'s complement: toc-discipline governs the *honesty* of the label (promise = delivery); loading-triggers adds the *routing* surface (situation → page) that honesty alone doesn't provide. The librarian's book pick reads the "When to load" section; a scout's chapter pick reads `load_when` lines beside descriptions. → See [page-anatomy](page-anatomy.md) for where the trigger lives in frontmatter; the "When to load this book" section lives in the book's index.
