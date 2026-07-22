---
type: rule
description: Every factual claim is classified — sourced, derived, opinion, or uncertain — and the gate rejects unmarked claims.
load_when: Making or reviewing a factual claim in a chapter — which of the four epistemic classes it carries and how to mark it.
keywords: [citations, sources, claims, verifiability, epistemic class, opinion, uncertain, examples labeled]
rules:
  - id: quality/claims-classified
    severity: error
    scope: chapter
    statement: Every factual claim is visibly one of sourced, derived, marked opinion, or marked uncertain.
    gate_criteria: >
      A chapter passes when each factual claim can be classified by a reader as
      sourced (origin named inline), derived (reasoning shown on the chapter),
      opinion (owner marked, e.g. 'our call:'), or uncertain (explicitly flagged
      as unverified/likely). It fails on any bare factual assertion carrying
      none of the four marks — a derived claim whose derivation is absent counts
      as bare. Exceptions: common-knowledge definitional statements, the chapter's
      own structural/navigational text, and restatements of another chapter's claim
      that link to it.
  - id: quality/examples-labeled
    severity: error
    scope: chapter
    statement: Constructed examples are labeled as illustrative; real examples are preferred where available.
    gate_criteria: >
      An example passes when it is either verifiably real (named product, cited
      paper, recorded event) or explicitly labeled as constructed/illustrative.
      It fails when invented material is presented in the voice of evidence with
      no label. The label may be inline ('(constructed, illustrative)') or in the
      example's lead sentence; one label covers one example, not a whole chapter.
---

# Sourced statements

**What it is** — the precision bar for everything a book asserts. Readers trust the library blindly (that's the point of the gate), so no claim may ride on confidence alone: every factual claim carries its **epistemic class**, visible to the reader. The bar is *verifiability*: a reader must be able to check — even when nobody does.

**Mechanics** — the four classes; every factual claim is exactly one:

| Class | Meaning | How it's marked |
|---|---|---|
| **Sourced** | Backed by a citable origin. | Name the source inline: a paper, a doc, a product, a chapter in this library (interlink it). |
| **Derived** | Follows from stated reasoning. | Show the reasoning — a derived claim without its derivation is just an unsourced claim in disguise. |
| **Opinion** | A judgment call. | Mark *whose*: "our call:", "CK chose X; we choose Y because…". |
| **Uncertain** | Believed but unverified. | Say so explicitly: "unverified", "likely", "we haven't tested this". Uncertainty is a valid state — hiding it is the violation. |

Examples follow the same discipline: real examples preferred; **constructed examples are allowed when labeled** as illustrative. An unlabeled constructed example presents fiction as evidence — that's an unsourced claim.

**Takeaway** — **a claim's class must be visible to the reader — the gate rejects any factual claim that is none of: sourced, derived, marked opinion, or marked uncertain.**

**Example** — "A-MEM is 2× more token-efficient than MemGPT on multi-hop QA (LoCoMo)" — *sourced*, checkable. "A copy is a fork; a pointer survives the original's edits" — *derived*, reasoning on the chapter. "We prefer fewer, deeper books" — *opinion, ours*. "This threshold probably holds for non-English chapters — untested" — *uncertain, and honest about it*. All four pass the gate; the same sentences with their markings stripped all fail.

**In this system** — this chapter is a gate checklist (quality dimension): the verifier walks a draft's claims and bounces any it can't classify, citing this rule. Bar seeded from Wikipedia's verifiability principle and CK's one-line version ("prefer precise, sourced statements"); tightened to full classification by decision of the human maintainer, 2026-07-06. → See [supersede-dont-delete](supersede-dont-delete.md) — how sourced claims stay honest over time. Unmarked claims are how poisoning starts.
