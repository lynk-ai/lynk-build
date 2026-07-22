# Run report — s3-mcp (book-writer pipeline)

**Date:** 2026-07-21 · **Terminal state:** `created`

## Brief

- Ask (verbatim): "Write a book about MCP (Model Context Protocol) — what it is, why it exists, and how to build an MCP server"
- Searched/missed: direct request — no prior search.
- Gap: the library has nothing on MCP.

## DIAGNOSE decision (Stage 1, orchestrator's own step)

**Case 3 — ABSENT → new book, slug `mcp`.**

Reasoning: the sandbox library contains exactly one book, `best-context` (context-engineering principles: context rot, progressive disclosure, memory shapes, etc.). Its index description explicitly scopes it out of this task: "not for tool or API syntax, and not for agent-building how-tos." MCP — a concrete protocol with wire formats, SDKs, and a build recipe — does not fit that scope, and no other book exists. The playbook default (new chapter in the best-fitting existing book) was overridden per its own rule: a new book is warranted when no existing book's scope fits. The round-2 verifier independently confirmed zero overlap (best-context mentions MCP only twice, in passing, in a different concept space).

## Stages run

| Stage | Agent | Rounds | Outcome |
|---|---|---|---|
| 0 Brief check | orchestrator | — | Brief complete (ask, searched/missed, gap) — proceed |
| 1 DIAGNOSE | orchestrator | — | ABSENT → new book `mcp` |
| 2 RESEARCH | researcher (general-purpose subagent, id ab6b35aea3bdd6ae4) | 1 of max 3 | 22 findings, all three sections covered; 3 honest residual gaps declared (N×M phrasing is community wording; 2025-06-18 changelog not fetched; `--scope` names secondary) |
| 3 AUTHOR | book-author (general-purpose subagent, id a8ca3e3fb9a2f8548; resumed once for retry) | 2 (initial + FLAG-fix retry) | 8 draft files + honest gap map; retry applied all 4 FLAGs, nothing else changed |
| 4 VERIFY | book-verifier (fresh spawn per round: ids adea0ec09928bcdad, a4fb36d0f4c2f041e) | 2 of max 3 | Round 1: CORRECTION_NEEDED (4 FLAGs) · Round 2: APPROVED (all 7 checklist items CHECK) |
| 5 PROMOTE | orchestrator | — | Draft copied into sandbox library, verdict.json written, frontmatter re-check ALL PASS |
| 6 RETURN | orchestrator | — | `created` |

## Verify rounds and verdicts

**Round 1 — CORRECTION_NEEDED** (verifier adea0ec09928bcdad). FLAGs:
1. One-concept-one-home: "SDKs auto-compute capabilities" derivation duplicated in `lifecycle-and-transports.md` and `build-a-server.md`.
2. v2 structure: index `sources` flow list split at commas inside parentheses (20 fragments instead of ~13 sources).
3. Sources honest: index omitted three inline-cited sources (Anthropic donation announcement, OWASP Agentic Top 10 Dec 2025, Windows Experience Blog).
4. Sources honest: `test-and-connect.md` cited a corroborator ("github-mcp-server install guide") absent from the research source list.

The round-1 verifier also spot-checked the riskiest citations against live changelogs and found them accurate.

**Round 2 — APPROVED** (fresh verifier a4fb36d0f4c2f041e). All four round-1 FLAGs confirmed resolved; full checklist re-run fresh: 7/7 CHECK. Two attributions re-spot-checked against the live 2025-11-25 changelog (stderr logging = Minor #1/PR #670; Origin-403 = Minor #3/PR #1439) — accurate.

## Data sources used (research stage, primary-first)

- modelcontextprotocol.io/specification/latest (spec 2025-11-25: main page, lifecycle, security_best_practices, Security & Trust & Safety)
- modelcontextprotocol.io/specification/2025-03-26/changelog · /2025-11-25/changelog
- blog.modelcontextprotocol.io — "The 2026-07-28 MCP Specification Release Candidate"; "Building to Last" (2025-07-31); "MCP joins the Agentic AI Foundation" (2025-12-09)
- anthropic.com/news/model-context-protocol (2024-11-25) · anthropic.com/news/donating-the-model-context-protocol (2025-12-09)
- modelcontextprotocol.io/docs/sdk · /docs/develop/build-server · /docs/develop/connect-local-servers · /docs/tools/inspector
- github.com/modelcontextprotocol/python-sdk README · typescript-sdk README (fetched 2026-07-21)
- code.claude.com/docs/en/mcp-quickstart (secondary-confirmed)
- TechCrunch 2025-03-26 (OpenAI adoption) · x.com/demishassabis/status/1910107859041271977 (Google, 2025-04-09) · Windows Developer Blog + Windows Experience Blog (2025-05-19)
- Invariant Labs tool-poisoning demo (via Docker "MCP Horror Stories" + github.com/invariantlabs-ai/mcp-injection-experiments) · arXiv:2508.14925 (MCPTox) · OWASP Agentic Top 10 (Dec 2025, secondary) · The Hacker News (June 2026 Microsoft warning)

## Files created or modified (full paths)

**Promoted into the sandbox library (Stage 5, on APPROVED only):**
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/index.md
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/chapters/what-mcp-is.md
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/chapters/why-mcp-exists.md
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/chapters/lifecycle-and-transports.md
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/chapters/versions-and-governance.md
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/chapters/build-a-server.md
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/chapters/test-and-connect.md
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/library/mcp/chapters/security-pitfalls.md

**Staging / audit trace (drafts kept as evidence):**
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/drafts/mcp/index.md (+ chapters/*.md, 8 files — written by author round 1, 4 of them re-written in the FLAG-fix retry)
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/drafts/mcp/verdict.json (verdict, per-file sha256, checklist, timestamp)

**This report:**
- /Users/shakedyacoby/git/lynk/builder/optimizing-book-1/lynk-build/writer/eval/runs/s3-mcp/report.md

No file outside the s3-mcp sandbox was touched; the real library/ was never written to.

## Findability closure (Stage 5.3)

New book — its `index.md` was authored fresh and already covers all seven chapters (description is a trigger-condition list, 16 labels, 15 quoted sources); verified as checklist item 5 CHECK in round 2, so no post-promotion index edit was required. Mechanical re-check of all 8 promoted files: frontmatter parses, `name`/`description`/`labels` present everywhere, index also `sources` (15 items) and zero body — ALL PASS.

## Honest residual limits (carried visibly inside the book, not hidden)

- 2026-07-28 RC details marked "to-be-confirmed against the final publication."
- `claude mcp add --scope` value names marked secondarily sourced, with a "check `claude mcp add --help`" caveat.
- 2025-06-18 revision: lineage stated, no features attributed (changelog not fetched).
- N×M phrasing presented as community wording, not Anthropic's.
- OWASP Agentic Top 10 and the Invariant Labs blog cited via secondary coverage, marked as such.
