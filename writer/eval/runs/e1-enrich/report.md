# Run report — E3 enrich: SEP submission process → mcp book

**Ask (verbatim):** "Add how to actually submit a Specification Enhancement Proposal — the concrete SEP submission process — to the mcp book"

**Terminal state:** enriched

## DIAGNOSE (PARTIAL vs ABSENT reasoning)

Read both books' `index.md` frontmatter (`mcp`, `best-context`), then all seven mcp chapter frontmatters, then grepped the library for "SEP".

- Not **EXISTS**: `versions-and-governance.md` says *what* SEPs are (change mechanism, SEP-932 formalization, Working/Interest Groups, foundation history) but contains nothing on *how* to submit one — no repo location, template, sponsor role, statuses, or timelines. The knowledge is genuinely absent; this was not a retrieval miss, so no findability-only fix applies.
- Not **ABSENT**: the mcp book's index description explicitly covers "its version and governance history" — a book covers the area.
- → **PARTIAL**: the mcp book covers governance; the specific piece (the concrete submission procedure) is missing.

**Placement decision:** the researched material is a full recipe (filing mechanism, template fields/sections, sponsor acquisition, eight lifecycle statuses, review cadence, prototype and conformance requirements). Enriching `versions-and-governance` with all of it would break the chapter's one-concept boundary (its concept: revision lineage + who governs) and blow its page budget — so the addition outgrew the chapter. Chosen: **one new chapter** `submit-a-sep.md` in the mcp book, plus a minimal one-sentence interlink added to `versions-and-governance.md`. Scope-fit: "how to submit a SEP" is the actionable face of the book's existing governance clause — no new subject clause needed (verifier confirmed under checklist item 8).

## Stages

| Stage | Agent | Rounds | Outcome |
|---|---|---|---|
| DIAGNOSE | orchestrator (own step) | — | PARTIAL; target = mcp book, new chapter + interlink |
| RESEARCH | researcher (general-purpose, sync) | 1 of 3 | All eight brief questions covered from primary sources; STILL MISSING immaterial |
| AUTHOR | book-author (general-purpose, sync) | 1 | Two draft files + honest gap map (index routing deferred to promote; non-inferable borderline noted; currency claim kept derived) |
| VERIFY | book-verifier (general-purpose, fresh spawn, sync) | 1 of 3 | All 8 checklist items CHECK → **VERDICT: APPROVED** (first round) |
| PROMOTE | orchestrator (own step) | — | Files moved, verdict.json written, index updated, mechanical re-check passed |

## Sources

- modelcontextprotocol.io/community/sep-guidelines (fetched 2026-07-21) — authoritative process doc; confirmed current post-Linux-Foundation (references Extensions Track and SEP-2484, both post-Dec-2025 — derived)
- github.com/modelcontextprotocol/modelcontextprotocol `seps/` directory listing (live examples 414, 932, 2663)
- github.com/modelcontextprotocol/modelcontextprotocol `seps/TEMPLATE.md`
- github.com/modelcontextprotocol/modelcontextprotocol issues #932/#1395/#1502 (early issue-based SEPs — numbering trap)
- MAINTAINERS.md in the spec repo (sponsor eligibility)
- github.com/modelcontextprotocol/conformance (via SEP-2484)

## Verify rounds

One. APPROVED on the first author⇄verify round; no FLAGs, no CORRECTION_NEEDED, no INSUFFICIENT_INFO.

## Files changed (exact)

All under `/Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/e1-enrich/`:

1. `library/mcp/chapters/submit-a-sep.md` — **new chapter** (promoted from drafts; sha256 `b87ff3ed9cbf5249dcb3a03ceb788ef2ec04098154b783a50ae94d21f7323e28`). Recipe shape in flowing prose: scope gate (what needs a SEP vs plain PR) → pre-submission (WG/IG Discord discussion, roadmap alignment) → four SEP types → 5 steps (template with required header fields and sections; PR into `seps/`; rename to PR number; sponsor hunt with 2-week escalation rule; sponsor-owned status transitions and biweekly Core Maintainer review) → verification (eight named statuses; prototype/consensus/benefit acceptance criteria; SEP-2484 conformance + `sep-NNNN.yaml` traceability for `final`) → failure-mode table (6-month `dormant`, motivation rejection, status-field canonicality, prototype pushback, issue-vs-file numbering trap).
2. `library/mcp/chapters/versions-and-governance.md` — **one sentence added** in the Governance paragraph linking to [submit-a-sep](submit-a-sep.md); zero removals or rewordings (diff-verified; supersede rule satisfied — pure addition, no correction). sha256 `a74566d1bc36487db445de60a84958940c2da0988ebe9e4670ec7e1ce8d0d7e1`.
3. `library/mcp/index.md` — findability closed: description extends the existing governance clause ("…including how to submit a Specification Enhancement Proposal (SEP)") and the read-when list ("proposing or shepherding a change to the MCP spec"); labels +`sep`, +`specification-enhancement-proposal`, +`sponsor`; sources +6 SEP-process entries.
4. `drafts/mcp/verdict.json` — audit trace: verdict, promoted-file sha256s, checklist, round counts, timestamp.
5. `drafts/mcp/chapters/` — emptied (drafts moved to library on APPROVED).

Mechanical re-check: all three promoted/updated files' frontmatter parses (YAML) and carries `name`/`description`/`labels` (index also `sources`).
