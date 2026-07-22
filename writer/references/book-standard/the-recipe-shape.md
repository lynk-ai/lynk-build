---
type: rule
description: Every how-to book has all four sections — prerequisites, steps, verification, failure modes — fail-closed; E2E or it doesn't ship.
load_when: Writing or gating a how-to page — the four mandatory recipe sections and the bar each must meet.
keywords: [recipe, how-to, prerequisites, steps, verification, failure modes, E2E]
rules:
  - id: generality/recipe-complete
    severity: error
    scope: page
    statement: A how-to page carries all four recipe sections — prerequisites, steps with observable outcomes, checkable verification, failure modes — or it doesn't ship.
    gate_criteria: >
      A how-to (type recipe) page passes when all four sections are present and
      each meets its bar: prerequisites complete enough that failure can't be
      blamed on an unlisted assumption; each step has one observable outcome;
      verification is checkable by the reader (a command, an output, a state),
      not 'it should work now'; failure modes name symptom and fix or escape.
      Missing any section is a rejection — 'we'll document the sharp edges
      later' is how sharp edges become incidents. Not applicable to
      principle/reference pages, which the template and quality rules govern
      instead. Section presence is pre-checked by lint; section quality is the
      judgment call.
---

# The recipe shape

**What it is** — the generality bar: a how-to book is a **recipe**, and a recipe is complete only end-to-end. The test of E2E: *an agent with no prior knowledge, given only the book and its listed prerequisites, can reach the verified outcome.* If the reader needs anything unlisted, the recipe is broken — however good its prose.

**Mechanics** — four mandatory sections; missing any one → the gate rejects:

| Section | Answers | The bar |
|---|---|---|
| **Prerequisites** | What must exist/be true before step 1? | Complete enough that "it didn't work" can't be blamed on an unlisted assumption. |
| **Steps** | What to do, in order. | One observable outcome per step — if you can't tell whether a step happened, it's not a step; if two things must be observed, it's two steps. |
| **Verification** | How do you *know* it worked? | Checkable by the reader: a command to run, an output to compare, a state to inspect. "It should work now" is not verification. |
| **Failure modes** | What goes wrong, how you'd notice, what to do. | The known ways this recipe breaks — each with its symptom and its fix or escape. |

Why fail-closed on all four (our call): a recipe missing failure-modes *works in the demo and strands the reader in production* — precisely when they can't ask the author. Failure-modes discovered later are added by maintenance; their absence at birth is still a rejection, because "we'll document the sharp edges later" is how sharp edges become incidents.

**Takeaway** — **E2E or it doesn't ship: prerequisites → steps with observable outcomes → checkable verification → failure modes, all four, or the gate bounces it.**

**Example** *(constructed, illustrative)* — a "deploy the service" book with beautiful steps but no prerequisites section: it silently assumes credentials exist. The first reader without them fails at step 3 with no way to tell whether they broke it or were never equipped. Under this rule the book never shipped: **reject — prerequisites missing** (this page cited).

**In this system** — this page is the gate's generality checklist. It applies to *how-to* books; principle/reference books (like this one) are governed by the template and quality rules instead. Bar seeded from Diátaxis's how-to-guide type (Daniele Procida, diataxis.fr); hardened to all-four-fail-closed by decision of the human maintainer, 2026-07-06. → See [page-template](page-template.md) for the shape of individual pages. A recipe is, in effect, a strict brief whose worker is the future reader.
