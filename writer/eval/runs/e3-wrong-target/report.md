# Run report — E3 (wrong-target edit request)

**Date:** 2026-07-21
**Brief:** "Add the Invariant Labs tool-poisoning attack details to the build-a-server chapter, so people writing servers see it" — user read `build-a-server`, found no attack details, and specified `mcp/build-a-server` as the target.

## Stage 0 — Brief check

Complete: ask verbatim, what was searched (user read build-a-server), gap (tool-poisoning coverage for server authors), target (mcp/build-a-server). Proceeded.

## Stage 1 — DIAGNOSE

Read `library/mcp/index.md` frontmatter, then chapter frontmatter; grepped the whole library for `poison|invariant`.

**Target-validity call: the user's stated target is wrong.** The requested content — the Invariant Labs tool-poisoning attack, in full detail — already exists in `library/mcp/chapters/security-pitfalls.md`:

- the April 2025 demonstration (malicious tool description → agent exfiltrates WhatsApp history through a *legitimate* whatsapp-mcp server, whitespace-padded to hide in the UI);
- sources (Docker "MCP Horror Stories" writeup; `github.com/invariantlabs-ai/mcp-injection-experiments`, with an honest caveat that the original blog post was not fetched);
- the derived key property (the poisoned server never touches data — descriptions are attack surface);
- the institutional trail (MCPTox arXiv:2508.14925, OWASP Agentic Top 10 Dec 2025, Microsoft warning June 2026).

Writing it into `build-a-server` would create a **second home** for the concept, violating the library's one-concept-one-home rule (book-standard `graduation.md` #8c: "one concept keeps one home"; also `page-anatomy.md` one-concept-per-page and the standard's own "no rule lives in two places"). Per the invariant, the library's rules override the user's stated target.

**Case: 1 — EXISTS, retrieval missed it.** Why the user missed it: `build-a-server` ended with a bare pointer ("before shipping anything beyond a toy, read [security-pitfalls]") that never named tool poisoning or Invariant Labs, and `security-pitfalls`' description's "Read when" triggers did not include the server-author angle ("writing/publishing your own server") — exactly the angle the user approached from.

## Stages 2–5

Skipped by design. Case 1 mandates: fix findability only, write no new content, no researcher/author/verifier spawns, no drafts, no promote.

## Exact edits (findability only)

1. `library/mcp/chapters/build-a-server.md` — final sentence sharpened from
   `And before shipping anything beyond a toy, read [security-pitfalls](security-pitfalls.md).`
   to
   `And before shipping anything beyond a toy, read [security-pitfalls](security-pitfalls.md) — your tool descriptions and docstrings are fed verbatim to every host's model, making them attack surface; the demonstrated tool-poisoning attack (Invariant Labs, April 2025) and the spec's named attack classes live there.`
   (Pointer, not content — `interlinks.md` sanctions liberal followable pointers; the attack details stay in their one home.)

2. `library/mcp/chapters/security-pitfalls.md` — frontmatter description extended: named the attack ("demonstrated tool-poisoning attack (Invariant Labs, April 2025)") and added the missing trigger "writing or publishing your own server (your tool descriptions are attack surface)".

Not changed: `build-a-server` labels (adding `tool-poisoning` there would be a dishonest label — the chapter does not deliver that content); `mcp/index.md` (its description already covers "its documented attack classes", labels already include `tool-poisoning`, sources already cite Invariant Labs).

## Terminal state

**found-existing** — pointer returned to `mcp` book, `security-pitfalls` chapter; findability fixed at both ends of the missed hop (the referring chapter's pointer now names the attack; the owning chapter's triggers now include the server-author query). No new content written, no drafts created, library rules honored over the stated target.
