# Run report — e2-supersede (edit request E3)

**Ask (verbatim):** "The mcp book's versions-and-governance chapter marks the 2026-07-28 release-candidate details as to-be-confirmed, sourced only via a search-result summary. Verify those claims against the actual RC announcement and correct or strengthen them."

**Terminal state: enriched** (correction landed, supersede history preserved, sourcing strengthened to primary).

## Stages

| Stage | Agent | Rounds | Outcome |
|---|---|---|---|
| 0 Brief check | orchestrator | — | Brief complete (ask, searched, gap, target) — proceed |
| 1 Diagnose | orchestrator | — | Case 2 PARTIAL/edit: knowledge exists in `library/mcp/chapters/versions-and-governance.md`; its RC paragraph self-flags weak sourcing. Target = correct that chapter; supersede rules apply |
| 2 Research | researcher (general-purpose, foreground) | 1 of 3 | Primary sources reached; all 5 claims adjudicated; missed changes captured |
| 3 Author | book-author (general-purpose, foreground) | 1 | Draft at `drafts/mcp/chapters/versions-and-governance.md`, honest gap map (no log.md in v2 layout; page grew) |
| 4 Verify | book-verifier (general-purpose, fresh spawn, foreground) | 1 of 3 | All 8 checklist items CHECK → **VERDICT: APPROVED** |
| 5 Promote | orchestrator | — | Chapter moved into library; `verdict.json` written; index labels+sources extended; mechanical frontmatter re-check passed |

## What the researcher could / couldn't confirm

**URLs fetched successfully (2026-07-21):**
- https://blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ (the actual RC announcement — post dated 2026-05-21)
- https://blog.modelcontextprotocol.io/ (blog index)
- https://modelcontextprotocol.io/specification/draft/changelog (authoritative RC changelog)
- https://modelcontextprotocol.io/docs/extensions/overview
- https://modelcontextprotocol.io/extensions/apps/overview

**Failed:** https://modelcontextprotocol.io/specification/2026-07-28/changelog — 404; RC content still lives under `/specification/draft/` until final publication (itself a useful finding, now in the chapter as a URL trap).

**Claim adjudication:**
1. RC public, final ships July 28, 2026 — **CONFIRMED** against the announcement post ("The final specification ships on July 28, 2026"; ten-week validation window; "largest revision of the protocol since launch").
2. Stateless protocol core — **CONFIRMED + sharpened**: SEP-2575 removes `initialize`/`notifications/initialized` entirely (version/capabilities ride in `_meta`; `UnsupportedProtocolVersionError`); SEP-2567 removes protocol sessions and `Mcp-Session-Id`; mandatory new `server/discover` RPC.
3. Extensions framework — **CONFIRMED + precision fix**: reverse-DNS prefixes are the third-party half only; official extensions use `io.modelcontextprotocol/…`; negotiation via new `extensions` capability field; `ext-*` / `experimental-ext-*` repos.
4. MCP Apps — **CORRECTED**: "speaking the same JSON-RPC" overstated it; the sandboxed-iframe UI speaks its own MCP dialect built on JSON-RPC over postMessage (`ui/` prefix, some shared methods like `tools/call`).
5. Tasks → extension — **CONFIRMED + detail**: SEP-2663; `io.modelcontextprotocol/tasks`; blocking `tasks/result` → polling `tasks/get`; `tasks/update` added; `tasks/list` removed.

**Bonus (headline changes the old summary missed, now in the chapter):** MRTR (SEP-2322) replacing all server-initiated requests + required `resultType`; `subscriptions/listen` replacing HTTP GET + resource subscribe/unsubscribe; SSE resumability removed; `ping`/`logging/setLevel`/`notifications/roots/list_changed` removed; feature-lifecycle policy (SEP-2596) with Roots/Sampling/Logging deprecated (SEP-2577); OAuth DCR deprecated for Client ID Metadata Documents; `Mcp-Method`/`Mcp-Name` headers, `CacheableResult` caching fields, full JSON Schema 2020-12, mandatory RFC 9207 `iss` validation, error-code range reservation. Beta-SDK (2026-06-29) and enterprise-auth (2026-06-18) posts included with confidence honestly capped at "blog-index titles and dates only".

## Exact edits (before → after)

File: `library/mcp/chapters/versions-and-governance.md` (replaced wholesale by the approved draft; untouched sections preserved verbatim: lineage paragraph, what-landed-where table, elicitation trap, Governance section).

**Edit 1 — supersede the to-be-confirmed caveat (in "The next revision." paragraph).**
- Before: `…(MCP official blog, blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/ — headline list below is sourced via a search-result summary of that post, consistent across the official blog and roadmap post, so treat exact details as to-be-confirmed against the final publication).`
- After: old text kept verbatim, immediately followed by: `*(superseded 2026-07-21: the RC claims were verified directly against the RC announcement post and the primary spec pages; the search-result-summary caveat no longer applies. The announcement post is dated May 21, 2026, calls this "the largest revision of the protocol since launch," states "The final specification ships on July 28, 2026," and describes a ten-week validation window between RC lock and final publication — blog.modelcontextprotocol.io/posts/2026-07-28-release-candidate/, fetched 2026-07-21.)*`

**Edit 2 — supersede the MCP Apps wire-protocol wording (same paragraph).**
- Before: `**MCP Apps** (servers ship sandboxed-iframe HTML UIs speaking the same JSON-RPC)`
- After: old text kept verbatim, immediately followed by: `*(superseded 2026-07-21: "the same JSON-RPC" overstated it — the iframe UI speaks "its own dialect of MCP, built on JSON-RPC" over postMessage, sharing some methods with core MCP such as tools/call but with most methods new under a ui/ prefix like ui/initialize — modelcontextprotocol.io/extensions/apps/overview)*`

**Edit 3 — new verified-detail block (added after the headline paragraph):** four bullets (stateless core / extensions / MCP Apps mechanism / tasks) with SEP numbers and inline primary-source citations; the extensions bullet names and corrects "the earlier 'reverse-DNS IDs' phrasing" in place and adds the reading trap about the docs page's stale `initialize` examples.

**Edit 4 — "Headline changes the earlier summary missed" block:** five bullets (MRTR, subscriptions rework, SSE-resumability removal, method removals, deprecations + lifecycle policy) plus one compact line for the smaller items — all cited to the draft changelog.

**Edit 5 — practical notes:** the `/draft/`-vs-`/2026-07-28/` URL trap (404 documented, fetch-dated) and the two blog-index items with confidence explicitly capped.

**Edit 6 — chapter labels extended:** added `stateless`, `server-discover`, `mrtr`, `deprecation` (none removed).

File: `library/mcp/index.md` (findability close at promote):
- labels: added `release-candidate, 2026-07-28, extensions, mcp-apps, stateless, sep`
- sources: blog entry updated to note the RC post was fetched directly 2026-07-21; added `modelcontextprotocol.io/specification/draft/changelog` and the two extension-docs pages.

## Verify rounds

1 round. Verifier (fresh spawn, adversarial checklist): items 1–8 all CHECK — claims classified, non-inferable, one-home, v2 structure, findability, supersede-not-delete (both dated notes present, old text preserved, nothing silently removed), sources honest (every inline citation inside index sources ∪ research list; blog-index items honestly scoped), scope fit (index description byte-identical; RC material inside the existing "version and governance history / pinning a spec revision" clause). **VERDICT: APPROVED.** No CORRECTION_NEEDED or INSUFFICIENT_INFO rounds.

## Audit trace

- `drafts/mcp/verdict.json` — verdict, sha256 `d0723d70ed7afcc56505fd5f35006d4db31b4549dcec7ad5cef0e75cdd835a21` for the promoted chapter, checklist, timestamp.
- Draft retained at `drafts/mcp/chapters/versions-and-governance.md`.
- Mechanical re-check: both promoted files' frontmatter parses with all required fields (`name`/`description`/`labels`, index also `sources`).

## Terminal state

**enriched** — the correction shipped; no degradation needed (research round 1 of 3, verify round 1 of 3).
