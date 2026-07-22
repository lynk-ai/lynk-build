# Judge Report — Round 1 artifacts vs. best-context principles

*Caveat: the external judge agent died on an org spend limit; this judging was done
inline by the session that built the pipeline. Independence is therefore weaker than
designed — Shaked's human read (grader layer 3) carries extra weight this round.*

## Artifact 1 — the `mcp` book (index + 7 chapters)

| Principle | Grade | Evidence |
|---|---|---|
| Findability (descriptions = trigger conditions) | PASS | Every chapter: "Read when a connection fails at startup…", "…when imports from a tutorial don't match the SDK you installed" — situations, not topics |
| One concept, one home | PASS | Capabilities-derivation lives once in lifecycle-and-transports; build-a-server links instead of restating (the round-1 FLAG fix held) |
| Pointers, not content | PASS | build-a-server: "the quickstart… is also where to fetch the full runnable example; this page keeps only the skeleton and the decisions around it" |
| Claims classified | PASS (minor) | sourced/derived/our-call/to-be-confirmed used throughout; the RC section marks its own weak sourcing. Minor: "The bet paid off across vendors" (why-mcp-exists) is unmarked editorial |
| Non-inferable only | **MINOR** | The traps are clearly non-inferable (v1/v2 SDK trap, elicitation dating trap, stdout-corruption rule). But e.g. the six-primitives table is one-hop fetchable from the spec — admitted here as *synthesis*, which the rule as written doesn't actually license → RULE GAP 2 |
| Compression | PASS | 18–36 lines/chapter, condensed cited returns |
| Distinguishability | PASS | No two descriptions overlap; a reader can route on frontmatter alone |

**Verdict: ADMIT as-is.** Residual risk (not a violation): the verifier is
deliberately tool-less, so citation *reality* (do those arXiv IDs exist?) rests
entirely on the researcher's chain of custody. Recommend a spot-fetch of 2–3
citations as a standing eval step / human check.

## Artifact 2 — `multi-agent-failure-rates` chapter (into best-context)

| Principle | Grade | Evidence |
|---|---|---|
| Claims classified | PASS (exemplary) | The absence claim is marked "derived… and uncertain in the way absence claims always are"; version-mixing hazard; laundered-statistics exposure with provenance |
| Non-inferable only | PASS | Multi-source assembly + laundering exposé — expensive to rediscover, exactly what earns admission |
| Findability | PASS | Trigger-condition description ("…to check whether a number someone else cited is benchmark, survey, or production") |
| One concept, one home | PASS | Explicitly walls itself off from four-failure-modes ("don't merge their categories") |
| Page budget | MINOR | 36 lines — the longest chapter in the book (typical: 13–22). Watch, not reject |
| **Book scope fit** | **MAJOR** | The index description had to be STRETCHED to admit it: "The why of context engineering… **plus the measured failure-rate numbers for multi-agent LLM systems**". That "plus" is a scope seam — multi-agent reliability is not context engineering. The chapter is excellent; its home is wrong (it belongs in a subagents/multi-agent book). With a one-book library, "best-fitting book" degenerates to "the only book" → RULE GAP 1 |

**Verdict: content ADMIT, placement REJECT.** In a fuller library this chapter
moves to a multi-agent book; best-context's index reverts to its clean scope.

## Violations classified

| Finding | Class | Disposition |
|---|---|---|
| Chapter admitted by stretching the book's scope ("plus…" seam) | **RULE GAP** | New book-standard rule: *"A chapter must fit the book's existing index description. If admitting it requires appending a new subject clause to the description, the placement is rejected — that's a new-book (or different-book) signal."* Checkable: diff the index description; a scope-extending edit fails |
| Fetchable material admitted as synthesis with no rule licensing it | **RULE GAP** | New book-standard rule: *"Fetchable material is admissible only as condensed multi-source synthesis where the assembly itself is the value (traps, contradictions across sources, curation); a one-hop restatement of a single reachable source is rejected."* Sharpens non-inferable-only instead of contradicting it |
| "The bet paid off" — unmarked editorial voice | Writer bug (borderline) | Covered by existing sourced-statements rule; the verifier let a mild one through. Tighten verifier check #1 wording: "editorial characterizations count as claims" |
| Orchestrator stalls on background stage spawns | Harness bug | Already fixed in SKILL.md (synchronous spawns hard rule) |

## The recommendation this eval exists to produce

**The writer does NOT need to read best-context.** Evidence: both artifacts already
embody nearly every best-context principle having read only book-standard + the
skill's structure spec. Both real misses are *rule-shaped* — expressible as checkable
book-standard rules (above). Add the two rules to book-standard; the writer inherits
them through the reference it already reads. Revisit only if post-rule re-runs still
show principle violations that resist being written as rules.

## Actions

1. Add RULE GAP 1 (scope-fit) and RULE GAP 2 (assembly-value) to book-standard. ← owner: Shaked/next session
2. Tighten book-verifier check #1: editorial characterizations are claims.
3. Add citation spot-fetch to the eval checklist (grader layer 1.5).
4. Round 2 (edit-flow evals, per EVAL.md) runs after 1–2 land.
