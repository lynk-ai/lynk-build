# book-writer — Evaluation Plan

Goal: prove the pipeline does the right thing on every entry, with full traceability
(what we got · what the steps were · where the data came from), then judge the
generated books against **best-context** (the principles) to find rule gaps in
**book-standard** (the manual).

## 1. Entries of the skill (what can invoke it)

| # | Entry | Brief carries | Maps to DIAGNOSE |
|---|---|---|---|
| E1 | Search miss → user agreed to fill the gap | ask verbatim · searches tried+missed · gap · suggested page | any of the three |
| E2 | Direct: "write a book about X" | ask verbatim · "direct request" · gap | ABSENT (usually) |
| E3 | Direct: "add/update X in chapter Y" | ask verbatim · target book/chapter | PARTIAL (enrich/edit) |
| E4 | Thin/empty brief | — | Stage 0 asks the user, spends nothing |

## 2. Scenario matrix — the three classes

Each run must produce a **run report**: DIAGNOSE decision + reasoning · steps per
stage · data sources used · terminal state · artifacts.

### Class A — books the system SHOULD generate
| Run | Prompt | Why this topic | Expected |
|---|---|---|---|
| s3-mcp | "Write a book about MCP (Model Context Protocol) — what it is, why it exists, how to build a server" | Outside best-context's scope → new BOOK; real spec + docs to cite → non-inferable material exists | New book, multi-chapter (expect what/why/how coverage), all claims cited, APPROVED, promoted |

### Class B — books generated THINLY (degrade path)
| Run | Prompt | Why this topic | Expected |
|---|---|---|---|
| s4-thin | "Write a chapter with measured production failure-rate benchmarks for multi-agent LLM systems" | Very little solid public data exists → research must cap out | Degraded scope (stub/short chapter), gaps marked `uncertain`, honest "what's missing" report — NOT padded fluff |

### Class C — books the system should NOT generate
| Run | Prompt | Why this topic | Expected |
|---|---|---|---|
| s1-exists | "What is context rot and why does long context degrade?" | Already fully covered by best-context | found-existing: pointer returned, ZERO new content (at most findability edits) |
| s2-dogs | "I want to write a book about dogs" | THE TRAP: general dog knowledge is inferable by any capable reader — the admission filter must fire | nothing-written or a minimal non-obvious stub + honest explanation. A fluffy encyclopedia = FAIL (plausible-looking rot) |

### Round 2 — the EDIT flow (mandatory, on the best generated book)

Round 1 tested create; the edit flow is untested until these run. Target: the
**generated `mcp` book** (s3 sandbox) — editing writer-authored content is the
real production case.

| Run | Prompt (entry E3) | Tests | Expected |
|---|---|---|---|
| e1-enrich | "Add X to `versions-and-governance`" (a genuinely new dated fact) | PARTIAL diagnose → enrich an existing chapter | Fact added with source; chapter description/labels updated if scope grew; index untouched unless needed |
| e2-supersede | "Correct the RC claim — the 2026-07-28 release candidate has shipped as final" (or any claim correction) | supersede-dont-delete | Dated supersede note; old claim still visible; verifier check #6 exercised for real |
| e3-wrong-target | Ask to add content that belongs in a DIFFERENT chapter than the one named | one-concept-one-home under edit pressure | Writer redirects to the right home (or links), doesn't duplicate |
| e4-negative-gate | Planted draft containing an unsourced claim fed straight to VERIFY | the gate itself | CORRECTION_NEEDED citing check #1 — never APPROVED |

Insights to extract: does DIAGNOSE correctly pick PARTIAL over ABSENT when the
book exists? · does enrichment keep the chapter one-concept? · does the index
stay in sync? · is the supersede note shaped so a reader can trust the history?

Round 3 (later): search-miss entry (E1) end-to-end · concurrent edits to the
same book · re-run round 1 after book-standard gains the judge's proposed rules
(measure improvement).

## 3. Graders (three layers, in order)

1. **Code checks** (`check.py`, deterministic): frontmatter parses; chapters carry
   name/description/labels; index frontmatter-only + sources; no H1 in bodies;
   slugs `^[a-z0-9-]+$`; no cross-book references; verdict.json present for promoted slugs.
2. **Independent judge** (fresh agent — NEVER the pipeline's verifier): reads the
   generated book + **best-context** as the rubric. Grades per principle:
   findability (descriptions as trigger conditions), one-concept-one-home,
   non-inferable-only, pointers-not-content, claims classified, compression.
   For every violation: does a book-standard rule cover it?
   - Rule exists → writer bug (fix the writer/agents).
   - No rule → **rule gap** → the fix is a NEW RULE in book-standard, not giving
     the writer a second rulebook (one concept, one home applies to the writer too).
3. **Human read** (Shaked): the final call on content quality.

## 4. The outsource question this eval answers

"Do we need to expose the writer to best-context too?" — Expected answer: **no**;
every judge finding traceable to a best-context principle becomes a rule in
book-standard. If, after encoding the rules, quality gaps persist that can't be
expressed as rules → THEN revisit exposing the writer to best-context directly.

## 5. Run mechanics

- Each scenario gets its own sandbox: `writer/eval/runs/<run>/library/` (copy of
  the real library) + `writer/eval/runs/<run>/drafts/`. The real `library/` is
  never touched.
- The orchestrator is simulated faithfully to `context: fork` semantics: a fresh
  general-purpose agent whose prompt = the SKILL.md body + the brief + sandbox
  path overrides. Stage agents are spawned nested with their `agents/*.md` bodies
  as instructions.
- Every run writes `writer/eval/runs/<run>/report.md` (the traceability record).
