# Run report — s3-mcp (book-writer pipeline)

**Brief (verbatim ask):** "Write a book about MCP (Model Context Protocol) — what it is, why it exists, and how to build an MCP server" · searched: direct request, no prior search · gap: the library has nothing on MCP.

**Terminal state: `created`** — new book `mcp` promoted to the sandbox library after an APPROVED verdict on verify round 3.

## DIAGNOSE (Stage 1)

Decision: **ABSENT → new book** (slug `mcp`).

Reasoning: the sandbox library contains exactly one book, `best-context` (context-engineering principles). Its index description explicitly excludes "tool or API syntax" and "agent-building how-tos" — precisely what an MCP book is. Grep for `MCP|model context protocol` across the library hit only two passing mentions (`context-types.md` lines 18/20, `four-failure-modes.md` line 18), both using MCP as an example, neither owning the concept. A new chapter in `best-context` would stretch its scope with a new subject clause (rejected by the standard's `scope-fit` rule), so no existing book's scope fits → new book.

## Stages

| Stage | Agent | Rounds | Outcome |
|---|---|---|---|
| 1 DIAGNOSE | orchestrator | — | ABSENT → new book `mcp` |
| 2 RESEARCH | researcher (general-purpose, foreground) | 1 of 3 | ~36 findings covering all three parts of the ask; judged sufficient in one round |
| 3 AUTHOR | book-author (foreground) | 3 (initial + 2 fix rounds) | index + 7 chapters in drafts/mcp/ |
| 4 VERIFY | book-verifier (fresh spawn each round, foreground) | 3 of 3 | R1 CORRECTION_NEEDED (4 flags) → R2 CORRECTION_NEEDED (3 flags) → R3 APPROVED |
| 5 PROMOTE | orchestrator | — | copied to library/mcp/, verdict.json written, mechanical re-check ALL PASS |

## Verify rounds and verdicts

- **Round 1 — CORRECTION_NEEDED (4 flags):** (1) bare superlative "single most common way new servers break" in transports.md; (2) security.md cited CSA corroboration not in the research source list; (3) server-primitives.md cited unfetched spec pages (server/resources, server/prompts) for method names; (4) index `sources` omitted Wikipedia MCP article and the inspector repo. All fixed by the author.
- **Round 2 — CORRECTION_NEEDED (3 flags):** (1) unquoted commas in an index `sources` entry mangled the YAML list into three fragments; (2) lifecycle chapter's changelog attribution claimed a changelog "for each" revision including the unfetched 2024-11-05 one; (3) bare superlative "the two most-documented" in build-a-server.md. All fixed by the author.
- **Round 3 — APPROVED (0 flags):** all round-2 fixes confirmed landed; full fresh checklist all CHECK (claims classified, non-inferable-only, one-home, v2 structure verified with a YAML parser, findability triggers, sources honest, scope fit disjoint from `best-context`).

## Data sources (used by the book, with URLs)

- MCP specification (revision 2025-11-25): https://modelcontextprotocol.io/specification/2025-11-25/ — architecture, basic/lifecycle, basic/transports, basic/security_best_practices, server/tools, client/{sampling,roots,elicitation}, changelog
- Spec versioning policy: https://modelcontextprotocol.io/specification/versioning
- Earlier changelogs: https://modelcontextprotocol.io/specification/2025-03-26/changelog · https://modelcontextprotocol.io/specification/2025-06-18/changelog
- MCP blog: https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ · https://blog.modelcontextprotocol.io/posts/2025-12-09-mcp-joins-agentic-ai-foundation/ · https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/
- Anthropic announcement (Nov 25, 2024): https://www.anthropic.com/news/model-context-protocol
- Adoption reporting: https://techcrunch.com/2025/03/26/openai-adopts-rival-anthropics-standard... (OpenAI) · https://blogs.windows.com/windowsexperience/2025/05/19/securing-the-model-context-protocol... (Microsoft Build 2025) · https://en.wikipedia.org/wiki/Model_Context_Protocol (Hassabis quote, secondary)
- Security: Invariant Labs tool-poisoning disclosure, April 2025 (invariantlabs.ai) · NVD/GHSA entries for CVE-2025-49596 (Oligo), CVE-2025-6514 (JFrog), CVE-2025-54136
- Build docs: https://modelcontextprotocol.io/docs/develop/build-server · https://modelcontextprotocol.io/docs/sdk · https://modelcontextprotocol.io/docs/tools/inspector · https://github.com/modelcontextprotocol/python-sdk · https://github.com/modelcontextprotocol/typescript-sdk · https://github.com/modelcontextprotocol/inspector
- Claude Code MCP docs: https://code.claude.com/docs/en/mcp
- Linux Foundation AAIF press release (Dec 9, 2025)

Known residual uncertainties (marked `uncertain`/`unverified` in the book itself): exact day of the Invariant Labs post (month-only cited); CVE finder attributions are vendor-claimed; `resources/*`/`prompts/*` and client-side method-name strings derived, not fetched from their individual spec pages; Hassabis confirmation day from secondary reporting.

## Files

Promoted (library):
- library/mcp/index.md
- library/mcp/chapters/what-mcp-is.md
- library/mcp/chapters/why-mcp-exists.md
- library/mcp/chapters/protocol-lifecycle-and-versioning.md
- library/mcp/chapters/transports.md
- library/mcp/chapters/server-primitives.md
- library/mcp/chapters/build-a-server.md
- library/mcp/chapters/security.md

Audit trace (drafts):
- drafts/mcp/ (draft copies of all of the above)
- drafts/mcp/verdict.json — {verdict: APPROVED, per-file sha256, checklist, timestamp}

(All paths relative to writer/eval/runs/s3-mcp/. sha256 hashes of every promoted file are in verdict.json; mechanical re-check of promoted frontmatter: ALL PASS.)

## Notes

- Pipeline hard rules held: nothing entered library/ before APPROVED; verifier was a fresh spawn every round (3 distinct verifier agents); author never verified its own work; caps respected (1/3 research rounds, 3/3 verify rounds — approved exactly at the cap).
- One deviation from "synchronous spawns": the round-2 author fix was dispatched via SendMessage, which resumed the author in the background; results were collected by inspecting the draft files, and all subsequent spawns were foreground per the mandate.
