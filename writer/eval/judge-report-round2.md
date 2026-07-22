# Independent Judge Report — Round 2

Judge: grader layer 2 (independent; did not write these books).
Date: 2026-07-21.
Rubric: `library/best-context/` principles. Enforcement reference: `writer/references/book-standard/`.

**Schema note.** All three artifacts use the same v2 schema as `best-context` itself: `index.md` is frontmatter-only (`name` / `description` / `labels` / `sources`) with the *when-to-load* trigger folded into the `description` ("Read when …") and the search surface carried in `labels`. So the old-schema book-standard requirements (index H1 body, a literal "When to load this book" section, `load_when:`/`keywords:` frontmatter keys, `log.md`) are graded by their *principle equivalents* in v2, not by key name. Absence of a `log.md` changelog is a v2-schema artifact and is not charged against any single book.

---

## Book 1 — dog-care-evidence

| Principle | Grade | Evidence |
|---|---|---|
| Findability | PASS | Index: "Read when a specific dog-care decision … turns on a claim you suspect is folklore" + explicit negative trigger "NOT a general dog-care manual: it holds no breed guides, no puppy-101 …". Every chapter carries a "Read when" trigger + rich `labels`. |
| One-concept-one-home | PASS | Eight distinct concepts; no fact restated across chapters. |
| Pointers-not-content | PASS | Frontmatter-only index; within-book pointers ("see [neuter-timing]", "see [raw-feeding-pathogens]"). |
| Non-inferable | PASS | Index openly excludes fetchable common knowledge ("common knowledge or one-hop fetchable from AKC/AVMA and is deliberately excluded"); bodies are study/position-statement synthesis. |
| Progressive disclosure | PASS | Small index over 8 chapters a reader cites independently. |
| Claims classified | PASS (exemplary) | Every claim marked; e.g. grain-free "Figures to treat with caution … (uncertain — do not present these as sourced FDA figures …)". |
| Compression | PASS | Each chapter condensed to conclusion + citation + "Bottom line". |
| Distinguishability | PASS | Three diet chapters (grain-free / raw-feeding / lean-feeding) separated in both name and description. |

**Overall: ADMIT.** Cleanest of the three.
**Only nit (trivial):** grain-free chapter cites "AKC 2023 update" inline but that source is absent from the index `sources` list — a completeness slip, not a rule violation.

---

## Book 2 — mcp

| Principle | Grade | Evidence |
|---|---|---|
| Findability | PASS | Index trigger + negative ("Not for general context-engineering principles or prompt design"); chapter triggers are symptom-shaped ("when a working server won't appear in a client", "when sessions won't stick"). |
| One-concept-one-home | MINOR | The Origin-validation / DNS-rebinding MUST-rule is stated **in full** in both `transports.md` ("servers MUST validate the `Origin` header and respond 403 … local servers SHOULD bind to 127.0.0.1") **and** `security.md` (same normative sentence, adding "details in [transports]"). Security points but still restates the whole rule — two homes for one normative fact. |
| Pointers-not-content | PASS | Cross-chapter detail is pointed, not copied ("The full exploitation story is in [security]"). |
| Non-inferable | PASS | Genuine multi-source synthesis (spec revisions + SDK READMEs + CVE/NVD + adoption reporting + blog RC post); version traps and footguns are the value (batching "added and removed within one cycle", `--` separator, `MCP-Protocol-Version` silent downgrade). A couple chapters (`transports`) lean toward single-page condensation but add derived diagnostic tables ("400 means you forgot to echo the ID, 404 means your session died"). |
| Progressive disclosure | PASS | 7 distinct chapters under one small index. |
| Claims classified | PASS (exemplary) | Uncertainty flagged honestly, incl. self-limits: `server-primitives` — "this book's research pass fetched the tools page but not the spec's resources or prompts pages, so check those pages … (unverified)". |
| Compression | PASS | Dense, cited-per-item; recipe chapter carries all four recipe sections. |
| Distinguishability | PASS | `what-mcp-is` / `why-mcp-exists` / `server-primitives` / `protocol-lifecycle-and-versioning` clearly separated by name + description. |

**Overall: ADMIT.** Strong and unusually honest about its own gaps.
**Classification of the MINOR:** the within-book duplication is a **RULE GAP** — `structure/one-concept-per-page` governs *a page holding one concept*, and `graduation` governs *forking a home across books*; neither forbids the same normative fact appearing in full on two pages of one book.

---

## Book 3 — multi-agent-reliability

| Principle | Grade | Evidence |
|---|---|---|
| Findability | MINOR | Index has a good positive trigger but **no negative trigger** ("what NOT to load it for"); `loading-triggers` (`structure/load-triggers`) requires at least one. Dogs and MCP both carry one; this book does not. |
| One-concept-one-home | PASS | The single chapter is one clean concept. |
| Pointers-not-content | PASS | Frontmatter-only index. |
| Non-inferable | PASS (exemplary) | Textbook multi-source-synthesis exception: collects benchmark rates, cross-source contradictions, version traps (MAST v2 vs v3 category numbers), and debunks the circulating "70–95% fail in production" statistic by tracing it to its inputs. |
| Progressive disclosure | **MAJOR** | The book is an index wrapping **one** chapter. `best-context/when-to-deepen`: "An index over one page is pure overhead … Don't deepen a single concept." `write-a-book` prereq 1: "one concept … not a book of its own"; its failure mode names it exactly: "it's a page, not a book — fold it into its parent." |
| Claims classified | PASS (exemplary) | Sourced / derived / uncertain / unverifiable all marked; even 403-fetch failures flagged ("SSRN 7041478 … could not be verified … must not be cited as fact"). |
| Compression | PASS | Single dense chapter, every survivor keeps a citation pointer. |
| Distinguishability | MINOR | Index description and its sole chapter's description are near-identical — both "Read when you need [real/actual] measured failure rates … when [sizing/estimating] reliability … when [verifying/checking] a circulated 'agents fail X% in production' statistic." Degenerate distinguishability: the index adds nothing over the one page it points to. |

**Overall: ADMIT-WITH-FIXES.** The *content* is trustworthy and admissible; the *container* is wrong. Fix = fold the chapter into a broader multi-agent book, or hold it as a single page until sibling concepts earn the deepening.

**Classification of the MAJOR:** dual. **WRITER BUG at the prose level** — `write-a-book` prereq 1 and its "one concept stretched thin" failure mode already forbid a single-concept book, so the pipeline violated a written standard. **RULE GAP at the enforcement level** — no gate *rule* (`rule_id` + `gate_criteria`) encodes the cluster / thin-book bar, so the verifier had nothing to fire. This is the exact tension the `scope-fit` rule (added 2026-07-21) created: `scope-fit` correctly evicts multi-agent content from the context-engineering book, but when only one chapter's worth exists, the "make it its own book" fix produces a thin book that nothing catches.

---

## Proposed rules to close the gaps

- **R1 — thin-book / cluster bar (new gate rule, error).** "A book contains at least two non-reserved chapters a reader could cite independently; a book with a single chapter — or whose index description is not materially distinguishable from its sole chapter's description — is rejected: one concept is a page in an existing book, not a book." Checkable: chapter count (mechanical) + index-vs-sole-chapter description diff (judgment). Closes Book 3's MAJOR.
- **R2 — within-book fact home (new gate rule, warn→error).** "A normative fact (a MUST/SHOULD rule, a definition) has one home page within a book; other pages invoke it by pointer, never by restating the full rule." Closes Book 2's MINOR.
- **R3 — harden `loading-triggers` for v2 (existing rule).** Enforce the mandatory negative trigger where "When to load" is folded into the index `description`: reject an index whose description carries no "not for X" clause. Closes Book 3's findability MINOR.

---

## DECISIVE FINAL ANSWER

**The writer does NOT need to read `best-context` directly. Existing book-standard rules plus the three proposed additions close every gap I found.**

Every defect traces to a principle **already transcribed into book-standard**, not to missing context:

- The one structural failure (Book 3's thin book) maps to `when-to-deepen`, and that principle is *already* written into `write-a-book` as prereq 1 and as a named failure mode. The pipeline produced the thin book **anyway** — which is proof that more context would not have helped. What was missing was an *enforceable gate rule*, not knowledge.
- The within-book duplication (Book 2) maps to `one-concept-one-home`, already partially encoded; a small new rule (R2) finishes the job.
- The missing negative trigger (Book 3) is an *existing* rule (`loading-triggers`) that simply was not enforced in v2 (R3).

None of the three books needed the *why* from `best-context` to be written correctly; two of them (dogs, mcp) are strong precisely because the standard's rules were followed, and the third failed on a bar the standard already states in prose but does not enforce. The correct investment is enforcement (R1) and two small rule additions (R2, R3) — **not** wiring `best-context` into the writer's context window.
