# Round 2 Report — full re-run + edit flow (2026-07-21)

Round 2 ran with the round-1 fixes applied first: `scope-fit` rule (book-standard),
assembly-value license (`non-inferable-only`), verifier check #8 + editorial-claims
tightening, synchronous-spawn hard rule. Round-1 artifacts archived in `runs-round1/`.

## What this eval is trying to prove

The book-writer pipeline writes into a library that readers trust **blindly**, so a
bad write is worse than no write. The eval's job is to prove the pipeline does the
**right thing on every kind of input** — not just "can it write a book," but: does it
*refuse* when it should, *degrade honestly* when evidence is thin, *find existing
content* instead of duplicating, put content in the *right home*, and *gate out*
unsourced claims. We test that across three classes (should-create / should-degrade /
should-NOT-create) plus the full edit flow, and we grade three ways: deterministic
structure checks, an independent judge against best-context's principles, and a human
read. Round 1 tested create; round 2 re-runs everything with fixes applied **and** adds
the edit flow (the true production case — editing writer-authored content).

## The inputs and the goal of each run

Every run gets a strict brief (the ask verbatim · what was searched/missed · the gap ·
target). Below: the actual input and the specific behavior it is designed to catch.

| Run | Input (the ask) | What it is designed to test | Pass = |
|---|---|---|---|
| **s1-exists** | "What is context rot and why does long context degrade?" | Content already in the library → does it recognize that and NOT re-write? | found-existing; 0 new content; at most a findability fix |
| **s2-dogs** | "I want to write a book about dogs" | **The trap.** General dog knowledge is inferable by any reader → does the admission filter fire instead of producing a fluffy encyclopedia? | refusal OR an evidence-only book; the encyclopedia is never written |
| **s3-mcp** | "Write a book about MCP — what it is, why it exists, how to build a server" | The real create case: genuine non-inferable material exists → can it produce a sound, cited, multi-chapter book? | new book, all claims cited, APPROVED, promoted |
| **s4-thin** | "Write a chapter with measured *production* failure-rate benchmarks for multi-agent LLM systems" | Degrade + placement: the exact ask (production rates) barely exists, and it doesn't belong in the only existing book | honest scope handling + correct home (its own book, not best-context) |
| **e1-enrich** | "Add the concrete SEP submission process to the mcp book" | Edit / PARTIAL diagnose: enrich an existing writer-authored book without breaking one-concept-per-chapter | fact added with source; chapter stays one concept; index kept in sync |
| **e2-supersede** | "Verify the mcp book's to-be-confirmed 2026-07-28 RC claims against the actual announcement and correct them" | Correction flow: supersede-don't-delete on real content | dated supersede notes; old claims still visible; nothing deleted |
| **e3-wrong-target** | "Add the tool-poisoning attack to the build-a-server chapter" (names the WRONG chapter — it already lives in security-pitfalls) | Does it honor one-concept-one-home over the user's stated target? | redirect / link, not a duplicate |
| **e4-negative-gate** | A planted draft full of bare, unsourced numbers, fed straight to the verifier with an empty source list | The gate itself: can plausible-looking rot ever pass? | never APPROVED — must bounce with the unsourced claims cited |

## Scoreboard — 8/8 PASS (pipeline behavior)

| Run | Terminal state | Gate activity | Judged vs best-context (layer-2) | Key evidence |
|---|---|---|---|---|
| s1-exists | found-existing | none needed | n/a (no new book) | Same 2-file findability fix as round 1; 0 new content; reproducible |
| s2-dogs | **created (degraded scope)** | 2 verify rounds, 1 FLAG | **ADMIT** — clean; exemplary claim-classification; nit: index omits 1 inline source (AKC 2023) | `dog-care-evidence`: 8 evidence-pocket chapters; encyclopedia explicitly declined with reasoning returned to user |
| s3-mcp | created | 3 verify rounds (cap), 7 total FLAGs | **ADMIT** — strong, unusually honest re own gaps; minor: DNS-rebinding MUST-rule duplicated across transports+security (RULE GAP) | 8-file `mcp` book; APPROVED exactly at cap; every verifier fresh |
| s4-thin | **created (new book)** | 4 verifier spawns / 3 corrections | **ADMIT-WITH-FIXES** — exemplary synthesis, but a 1-chapter book whose index ≈ its sole chapter (thin-book); no negative trigger | `multi-agent-reliability`; **best-context byte-identical** (round 1 had stretched it) |
| e1-enrich | enriched | 1 round, APPROVED | n/a (judged as part of mcp) | PARTIAL diagnose; SEP procedure → new recipe-shaped chapter + interlink + index |
| e2-supersede | enriched | 1 round, APPROVED | n/a (judged as part of mcp) | Primary source reached; 2 dated supersede notes, history preserved; corrected a real round-1 error (MCP Apps dialect) |
| e3-wrong-target | found-existing | none needed | n/a (no new content) | User's wrong target overridden (one-concept-one-home); findability fixed on both ends |
| e4-negative-gate | INSUFFICIENT_INFO | all planted defects caught | n/a (never promoted) | 7 bare claims flagged + 3 unplanted catches (derived counterexample, batching-removed error, "typical" population claim); check #8 fired |

## What the best-context judge gave us (grader layer 2)

An independent judge read the three *created* books against best-context's principles
(full report: `judge-report-round2.md`). Result: **2 ADMIT, 1 ADMIT-WITH-FIXES** — no
rejects. But it surfaced the round's most important finding — and it is a *direct
side-effect of the round-1 fix*:

- **The scope-fit rule created a new failure mode.** scope-fit correctly evicted the
  multi-agent chapter from best-context (round 1's bug) → but with only one chapter's
  worth of material, "give it its own book" produced a **thin, one-chapter book** whose
  index description ≈ its sole chapter. We fixed a wrong-home bug and introduced a
  thin-book bug. Both are placement failures; neither is a knowledge failure.
- **Every defect maps to a principle ALREADY in book-standard** — so these are
  *enforcement* gaps, not *knowledge* gaps. This is the decisive evidence for the
  standing question:

  > **The writer does NOT need to read best-context.** More context would not have
  > prevented the thin book — book-standard already contains `when-to-deepen` /
  > `write-a-book` prereq 1 ("it's a page, not a book"); the pipeline produced the thin
  > book anyway. What's missing is an enforceable *gate rule*, not more principle
  > exposure. Invest in enforcement, not wiring.

- **Three proposed rules** (round-3 fixes, before any re-run):
  - **R1** — reject a single-chapter book, or a book whose index description is
    indistinguishable from its one chapter (the thin-book gate).
  - **R2** — a normative fact has one home page within a book; other pages point to it
    (hardens one-concept-one-home *within* a book — caught the DNS-rebinding duplication).
  - **R3** — harden `loading-triggers` so the v2 folded-in index description must carry
    a negative trigger ("not for …"), which s4's book lacked.

## The headline: the feedback loop works

Round 1 judge finding ("plus" seam in best-context's index) → scope-fit rule written
into book-standard → round 2's writer **cited the rule by name in DIAGNOSE** and
created `multi-agent-reliability` as its own book, leaving best-context untouched.
One eval cycle: principle violation → rule → changed behavior. This is the
best-context-as-judge / book-standard-as-manual division confirmed in practice.

## Behavioral findings (good)

1. **The trap has two honest resolutions.** Round 1 s2 refused pre-research (the ask
   as scoped fails admission on its face). Round 2 researched deeper and found the
   non-inferable core (FDA/DCM contested mechanism, Hart 2020, Purina 14-yr study…)
   → shipped only that. Both times the fluffy book was never written. The admission
   rule is robust to path variance.
2. **Author integrity beats reviewer authority.** s3's author *declined* a verifier-
   suggested citation because no research finding backed it ("writing that citation
   would be fabricated sourcing") and marked the claims `unverified` instead. The
   sourcing bar held against the gate itself.
3. **The gate catches real defects, not ceremony.** Across rounds: YAML source-list
   bugs, internally inconsistent counts, bare superlatives, overbroad changelog
   attributions, unfetched-page citations, a factually wrong batching recommendation.
4. **Honest-scope behavior is stable**: absence claims marked derived+uncertain,
   "production" reframed to what is measured, secondary sourcing labeled.

## Process findings (to fix before production)

1. **Background-spawn stalls (4 occurrences)** despite the sync hard rule — orchestrators
   kept spawning stage agents in the background and idling. Instruction alone is not
   enough; the real harness must make foreground spawning structural (explicit
   `run_in_background: false` in stage-spawn instructions). Note: in the real
   `context: fork` runtime this may not reproduce, but do not rely on that.
2. **Cap semantics were ambiguous** ("3 rounds" — corrections or verifier spawns?).
   Fixed in SKILL.md: ≤3 correction cycles, ≤4 verifier spawns.
3. **Book shape is non-deterministic across runs** (round-1 mcp: 7 chapters incl.
   test-and-connect; round-2: 7 different chapters incl. transports/server-primitives).
   Standards compliance is reproducible; structure is not. Acceptable for v1; know it.
4. **Peer-to-peer agent messaging doesn't exist** — children could never reach their
   orchestrator by name; the main session had to relay. Disappears with foreground
   spawns (the parent just waits), which is one more reason for finding #1.
5. One server-error mid-run (s3) — resume-from-message worked; no state lost thanks
   to drafts-on-disk + report files.

## Verdict

The pipeline is behaviorally sound across create, edit, refuse, degrade, and gate
paths, and the improvement loop (judge → rule → behavior) is demonstrated. Remaining
work before real use: make foreground spawns structural, run the citation-reality
spot-fetch (layer 1.5), and have a human read one full generated book (layer 3 —
never yet done by a human).
