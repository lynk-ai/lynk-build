---
type: template
description: The concept template every chapter follows — What it is, Mechanics, Takeaway, Example, In this system.
load_when: Writing or reviewing any chapter — the five sections every chapter must run, and each section's job.
keywords: [template, sections, takeaway, example, mechanics, chapter shape]
rules:
  - id: structure/page-template
    severity: error
    scope: chapter
    statement: Every chapter follows the five-section concept template with a one-sentence bold Takeaway and a concrete Example.
    gate_criteria: >
      A chapter passes when it contains the five sections in order — What it is,
      Mechanics, Takeaway, Example, In this system — with the Takeaway as exactly
      one bold sentence and the Example concrete (real names or labeled-constructed).
      Mechanics may be omitted when the definition already covers how it works.
      How-to (recipe) chapters replace Mechanics with the four recipe sections but
      keep What it is, Takeaway, Example, and In this system. A chapter fails when a
      section is missing without qualifying for these exceptions, or when the
      Takeaway is absent, unbolded, or runs past one sentence.
---

# The chapter template

**What it is** — the fixed shape every chapter in every book follows. One proven format, lifted from the context-engineering talk, where it survived contact with a real audience: each concept runs *What it is → Mechanics → Takeaway → Example → In this system*.

**Mechanics** — the five sections, in order:

| Section | Job | Rule |
|---|---|---|
| **What it is** | Define the concept in 1–3 sentences. | Plain words first; jargon only after it's earned. |
| **Mechanics** | How it works: what builds it, what triggers it, what results. | A table or short list beats prose. Skip if the definition already covers it. |
| **Takeaway** | The one sentence a reader must leave with. | Exactly one sentence, bold. If you can't write it, the chapter has no concept. |
| **Example** | The concept happening, concretely. | Real names, real numbers. "A 500-token doc answers correctly; the same doc buried in 50k tokens fails" — not "less context is better." |
| **In this system** | Where this concept lives in lynk-book itself. | Every chapter ends by pointing at the machinery it explains or governs. |

**Takeaway** — **a chapter is complete when a reader who opens only this chapter gets the full concept: definition, proof, and where it applies.**

**Example** — this chapter. It defines the template (What it is), tables the sections (Mechanics), states the completeness rule (Takeaway), points at itself (Example), and ties in below.

**In this system** — the gate checks drafts against this shape (structure checklist); the writer reads this chapter before writing any other. → See [chapter-anatomy](chapter-anatomy.md) for the file-level rules around the template.
