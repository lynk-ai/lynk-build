# Product Evaluation — grading the book / chapter / edit itself

The pipeline evals (EVAL.md, round2-report.md) proved the writer *behaves* right.
This plan grades the *output*: is a generated book/chapter/edit true, findable, and
useful? Five layers, cheapest→truest. Layers 1–2 exist; 3–5 and the edit-regression
check are the new work.

Grounding note: the CandleKeep read-limit (429) blocked a fresh library pass; methods
below draw on this session's earlier reads (*Demystifying Evals*, *Replicating
Anthropic's Self-Service Analytics*) plus standard RAG/faithfulness practice. Re-cite
against the library when reads reset.

## Proxies vs. ground truth

Layers 1–2 are **proxies** (a book can pass both and still be false or useless).
Layer 3 guards the worst case (a *false* book in a blindly-trusted library).
Layer 5 is the only **ground truth** — it measures what a book is actually *for*.

---

## Layer 3 — FAITHFULNESS (are the claims true / citations real?)  ← build first

The poisoning guard. The pipeline's verifier is tool-less by design, so nobody has
ever checked that the cited sources exist and say what the chapter claims.

- **Metric — claim groundedness rate**: sample N claims marked `sourced`; for each,
  fetch the named source and label `supported / unsupported / source-unreachable`.
  Book passes at a threshold (start strict for a trusted library: 100% of *sourced*
  claims must be supported or the claim gets downgraded to `uncertain`).
- **Build**: a grader agent WITH WebFetch (unlike the pipeline verifier) walks each
  inline citation → fetches → checks the specific number/quote → verdict + evidence
  quote. Code-checkable pre-pass: every arXiv id / URL resolves (HTTP 200).
- **Grader**: model-based per claim (semantic match), binary supported/not, with an
  explicit `source-unreachable` escape (don't force a verdict when the fetch fails).
- **Start**: 15–20 claims per book, sampled across chapters, biased toward the
  load-bearing numbers (the ones a reader would cite onward).
- **Pitfalls**: paywalled/moved sources → `unreachable`, not `unsupported`; a source
  that exists but says something subtly different is the real catch — grade the
  *specific* claim, not "is this source about the topic."

## Layer 4 — FINDABILITY (does retrieval surface it for the right query?)

Retrieval-in-the-loop — the gap called out on the s1/e3 runs (findability fixes were
eyeballed, never tested against the real retriever).

- **Metrics — recall@k and MRR**: for a set of realistic queries the book should
  answer, does the actual retrieval path (librarian/scout routing, or whatever ships)
  return the right chapter in the top-k? MRR captures *how high* it ranks.
- **Build**: write 5–10 queries per chapter phrased as a real asker would (not the
  chapter's own title words — that's the easy case). Run them through the real
  retriever against the book. Score hit-position. **The exists-but-unfound test**:
  run the query, confirm miss, apply the writer's findability fix, re-run, confirm hit
  — this is the loop that proves a findability edit actually works.
- **Pitfall**: don't test with the chapter's own vocabulary; test with the *asker's*
  vocabulary (synonyms, the problem not the term) — that's where labels earn their keep.

## Layer 5 — UTILITY (does reading it make an agent answer better?)  ← the real one

The ablation. The only eval that measures the book's reason to exist.

- **Metric — answer lift**: build a question set the book is *supposed* to enable.
  Answer each twice: agent WITHOUT the book vs. agent WITH it. Grade both answers
  against a reference. Lift = with − without. A book with ~zero lift doesn't earn shelf
  space, however clean it is.
- **Build**: 10–20 questions/book, drawn from the non-inferable claims (if the book's
  value is real, these are exactly what an agent can't answer without it). Same model,
  same prompt, book injected vs not. Model-judge the answers (rubric: correct,
  grounded, specific) — ideally blind to which condition produced which.
- **Guardrails from the evals reading**: start small (20–50 items total is enough to
  learn from); calibrate the model-judge against a few human-graded items; give the
  judge an "Unknown" escape; grade the *answer*, not the path. A frontier judge scoring
  everything 0 usually means a broken rubric, not a bad book.
- **Pitfall**: if "without book" already answers well, the topic was inferable — that's
  a Layer-5 signal the book failed non-inferable-only, caught functionally.

## Editing a chapter — REGRESSION eval (edits aren't creates)

An edit must improve the target without harming the rest. Four checks:

1. **Target resolved**: the query/gap that triggered the edit is now answerable
   (a Layer-5 mini-ablation on just that question: fails before, passes after).
2. **No information loss**: every claim present before is still present or explicitly
   superseded — diff old vs new claim set; a silently dropped claim is a regression.
3. **History preserved**: corrections carry a dated supersede note (already gate-checked;
   verify it survived promotion).
4. **No new contradiction**: the edited chapter doesn't now contradict itself or another
   chapter — model-judge scan of the edited book for internal consistency.

## Build order

1. **Layer 3 faithfulness** — cheapest, guards the worst failure. Run on the 3 generated
   books (mcp, dog-care-evidence, multi-agent-reliability); their strongest numeric
   claims are ready-made test items.
2. **Layer 4 findability** — needs the real retriever wired to a sandbox; validates the
   s1/e3 findability claims for real.
3. **Layer 5 utility** — most setup (question sets + ablation harness); the payoff eval.
4. **Edit regression** — reuses Layer 3 + a claim-diff; run on the e1/e2 edited books.

## Open question for the human

Layer 5 needs a reference answer per question. Who writes the gold answers — us by
hand (accurate, slow) or a strong model then human-spot-checked (fast, needs calibration)?
That choice gates how big the utility eval can get.
