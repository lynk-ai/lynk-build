---
type: recipe
description: How to author the machine layer — a stable rule_id, a one-sentence statement, gate_criteria with named exceptions, a severity and scope — so the gate judges consistently.
load_when: Adding or amending a rules block in a chapter's frontmatter — minting an id, writing gate_criteria, choosing severity and scope.
keywords: [rules, rule_id, gate_criteria, statement, severity, scope, machine layer, amendment]
---

# Write a rule

**What it is** — the procedure for the standard's machine layer: every normative rule is an addressable object — `id` + `statement` + `gate_criteria` + `severity` + `scope` — declared in the frontmatter of the chapter that owns the concept. Citations, failure counts, and amendments key on the id, not the prose; the criteria are what the verifier actually executes. Writing them well is what makes the gate *consistent* instead of moody.

**Prerequisites**

- The rule earned existence: a real failure, a live case, or a sourced external bar — rules invented in the abstract are wishes ([non-inferable-only](non-inferable-only.md) applies to rules too).
- Its home chapter exists — a rule lives on the chapter that owns its concept, never on a chapter of its own ([chapter-anatomy](chapter-anatomy.md)); if no chapter owns the concept yet, write the chapter first ([write-a-chapter](write-a-chapter.md)).
- You checked no existing rule covers it — an overlap is an amendment to the existing rule, not a sibling (one concept, one home).

**Steps** — one observable outcome each:

1. **Mint the id** — `<dimension>/<kebab-name>`: `structure/`, `quality/`, or `generality/`, naming the behavior, not the chapter → an id that will survive chapter renames; ids are never reused or repurposed.
2. **Write the statement** — one imperative sentence, self-contained: a reader who sees *only* the statement in a rejection message must understand what was violated → one sentence, no pointer needed to parse it.
3. **Write the gate_criteria** — 3–6 sentences covering exactly three things: what **passes**, what **fails**, and the **named exceptions**. This length is load-bearing: one-line criteria are where verdict flakiness comes from — a judgment rule without its exceptions spelled out gets its gaps filled differently by the verifier on every run (source: this repo's PLAN.md, the rules-are-addressable decision) → a stranger could produce one passing and one failing example from the criteria alone.
4. **Choose severity** — `error` (the gate rejects) only when the criteria are sharp enough to defend a rejection; `warn` for guidelines and for new rules during a retrofit window — and a warn that should harden gets its hardening condition written down, dated → severity matches criteria sharpness, not how strongly you feel.
5. **Choose scope** — `chapter` when checkable on one file (preferred: the verifier can run per-chapter), `book` only when the rule genuinely spans files (index consistency, graduation) → scope is as narrow as the check allows.
6. **Attach the precedent** — if a live case exists (a gate rejection, a documented incident), cite it on the chapter; a rule with a precedent is calibrated by history → the origin is findable.

**Verification**

- `bk lint` parses the rules block under the strict frontmatter subset.
- The two-examples test on step 3: write the passing and failing example; if you can't, the criteria are adjectives ([keywords](keywords.md) honesty bar applies — thresholds and predicates, not "good" and "clean").
- Every citation of the id elsewhere resolves — a hallucinated rule_id is a mechanical failure.

**Failure modes**

- **Adjective-only criteria** — symptom: "clear", "well-structured", "appropriate" with no testable predicate. Fix: replace each adjective with a threshold, pattern, or named judgment bar (the anti-pattern is rated HIGH by *Writing Books for AI Agents*, Ch. 9/15).
- **Criteria restate the statement** — symptom: sentence one of the criteria is the statement re-worded, adding no discrimination. Fix: spend the sentences on pass/fail boundaries and exceptions — the statement already said the rest.
- **Error severity, no exceptions listed** — symptom: false rejections on legitimate edge cases (reserved chapters, stubs, historical notes). Fix: name the exceptions or drop to warn until they're known.
- **Rule duplicated across chapters** — symptom: two ids policing one behavior, drifting apart. Fix: merge into the owning chapter's rule; the other chapter cites it.

**Takeaway** — **a rule is an id, one imperative sentence, and criteria a stranger could grade with — pass, fail, and the named exceptions — at a severity the criteria can actually defend.**

**Example** *(real — this book, 2026-07-19)* — `structure/load-triggers`, authored by this procedure: id named for the behavior; a one-sentence statement; criteria giving the pass ("When to load" section + situation-phrased `load_when`), the fail (topic-restating triggers), the named exceptions (reserved chapters, stubs hand off), and a dated hardening condition (warn while the shelf retrofits, error after). Its precedent — a sibling book's retrofit — is cited on the chapter.

**In this system** — rule frontmatter is what the gate's checklists are compiled from, so this recipe is upstream of every verdict; amendments to existing rules follow the same steps plus [supersede-dont-delete](supersede-dont-delete.md) on the prose. → See [write-a-chapter](write-a-chapter.md) for the chapter that must exist first, and [the-recipe-shape](the-recipe-shape.md) — a rule's criteria are to the gate what a recipe's verification is to the reader.
