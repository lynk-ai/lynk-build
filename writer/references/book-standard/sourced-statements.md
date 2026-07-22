---
type: rule
description: Every factual claim is classified — sourced, derived, or opinion — and the gate rejects unmarked claims; unverifiable content is omitted, not hedged.
load_when: Making or reviewing a factual claim in a page — which of the three epistemic classes it carries and how to mark it.
keywords: [citations, sources, claims, verifiability, epistemic class, opinion, examples labeled]
rules:
  - id: quality/claims-classified
    severity: error
    scope: page
    statement: Every factual claim is visibly one of sourced, derived, or marked opinion; content that can't be reliably stated is omitted, not hedged.
    gate_criteria: >
      A page passes when each factual claim can be classified by a reader as
      sourced (origin named inline), derived (reasoning shown on the page), or
      opinion (owner marked, e.g. 'our call:'). It fails on any bare factual
      assertion carrying none of the three marks — a derived claim whose
      derivation is absent counts as bare — and on hedged/uncertain content,
      which must be resolved to a single value or omitted, never shipped as
      'unverified/likely'. Exceptions: common-knowledge definitional statements,
      the page's own structural/navigational text, and restatements of another
      page's claim that link to it.
  - id: quality/examples-labeled
    severity: error
    scope: page
    statement: Constructed examples are labeled as illustrative; real examples are preferred where available.
    gate_criteria: >
      An example passes when it is either verifiably real (named product, cited
      paper, recorded event) or explicitly labeled as constructed/illustrative.
      It fails when invented material is presented in the voice of evidence with
      no label. The label may be inline ('(constructed, illustrative)') or in the
      example's lead sentence; one label covers one example, not a whole page.
---

# Sourced statements

**What it is** — the precision bar for everything a book asserts. Readers trust the library blindly (that's the point of the gate), so no claim may ride on confidence alone: every factual claim carries its **epistemic class**, visible to the reader. The bar is *verifiability*: a reader must be able to check — even when nobody does.

**Mechanics** — the three classes; every factual claim is exactly one:

| Class | Meaning | How it's marked |
|---|---|---|
| **Sourced** | Backed by a citable origin. | Name the source inline: a paper, a doc, a product, a page in this library (interlink it). |
| **Derived** | Follows from stated reasoning. | Show the reasoning — a derived claim without its derivation is just an unsourced claim in disguise. |
| **Opinion** | A judgment call. | Mark *whose*: "our call:", "CK chose X; we choose Y because…". |

Content you can't put in one of these three — unverified, or where sources conflict and you can't resolve which is right — is **omitted, not hedged**. A book carries single, clean truths; "probably", "likely", "sources disagree" confuse the reader and don't belong in it.

Examples follow the same discipline: real examples preferred; **constructed examples are allowed when labeled** as illustrative. An unlabeled constructed example presents fiction as evidence — that's an unsourced claim.

**Takeaway** — **a claim's class must be visible to the reader — the gate rejects any factual claim that is none of: sourced, derived, or marked opinion. Content that can't be reliably stated is omitted, not hedged.**

**Example** — "A-MEM is 2× more token-efficient than MemGPT on multi-hop QA (LoCoMo)" — *sourced*, checkable. "A copy is a fork; a pointer survives the original's edits" — *derived*, reasoning on the page. "We prefer fewer, deeper books" — *opinion, ours*. All three pass the gate; the same sentences with their markings stripped all fail. A claim you could only mark "probably, untested" doesn't get hedged — you omit it until it can be sourced or derived.

**In this system** — this page is a gate checklist (quality dimension): the verifier walks a draft's claims and bounces any it can't classify, citing this rule. Bar seeded from Wikipedia's verifiability principle and CK's one-line version ("prefer precise, sourced statements"); tightened to full classification by decision of the human maintainer, 2026-07-06. Unmarked claims are how poisoning starts.
