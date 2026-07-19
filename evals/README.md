# lynk-wiki agent evaluations

Measures whether the lynk-wiki build agent, given a question, (1) reaches the relevant
`semantics_docs/` documents, (2) does so efficiently, and (3) answers correctly. Each
case runs a **fresh headless Claude session with the plugin loaded** (Claude Agent SDK,
`claude_code` system-prompt preset, isolated from your global Claude settings) and
records every tool call the agent makes.

## Run

```bash
make setup                       # once: uv sync
make eval                        # all cases in datasets/
make eval CASE=policy-vs-skill   # one case (doubles as a smoke check)
make eval PERSPECTIVE=drawers    # drawers | business
make eval TAG=policy             # by tag
make eval REPEAT=3               # hop-noise measurement
```

Auth: uses the `claude` CLI's login (subscription) — no `ANTHROPIC_API_KEY` needed
(don't set one: the CLI would switch to API-key billing).

Env vars go in `evals/.env` (gitignored, loaded automatically). Only one matters today:

```bash
# evals/.env — Logfire write token: logfire.pydantic.dev -> your project -> Settings -> Write tokens
LOGFIRE_TOKEN=pylf_v1_us_...
```

Without it, runs are still fully recorded in `runs/` — Logfire just adds the hosted
compare-over-time view. (Alternative to a token: `uv run logfire auth` once, then
`uv run logfire projects use <project>` inside `evals/`.)
Each run writes `runs/<utc>-<label>/` with `meta.json` (git SHA, plugin version,
dataset hashes, config, **resolved models** from each session's init message),
`traces/<case>.json` (ordered doc reads, searches, answer, cost), `report.txt`/`.json`.
With a Logfire token configured, every run is also a pydantic-evals experiment there —
that's the compare-over-time surface.

**Discipline:** between runs you compare, change the plugin *or* the model — never both.

## Metrics per case

| Metric | Kind | Meaning |
|---|---|---|
| `required_docs_read` | assertion (gate) | every `expected_docs.required` file was Read |
| `docs_recall` / `optional_docs_read` | score | fraction of required / optional docs read |
| `hop_efficiency` | score (trend, never a gate) | `min(1, optimal_hops / hops_to_complete)`; a **hop** = first-touch Read of a doc file (re-reads and offset/limit paging don't count; Grep/Glob don't count but are reported as `searches`) |
| `answer_pass` | assertion (gate) | LLM judge: answer satisfies the case rubric |
| `answer_quality` | score | judge's fraction of rubric items satisfied |
| `suspect_answer` | label | `suspect` = judge passed but required docs weren't read (grep leak / model prior) — inspect the trace |

Errored sessions (timeout, max-turns, CLI failure) fail all assertions with a
`session errored: ...` reason and keep their partial trace — they are visible as
*errored*, not misread as *wrong answers*.

## Add a new check

Three tiers, in order of preference:

1. **Answer-content check** ("must mention X") → add a `Pass requires` / `Must NOT`
   line to the case's rubric. No code; the judge grades it.
2. **Deterministic trace signal** → one function in `lynk_evals/metrics.py`:

   ```python
   @trace_metric                      # score/label column, never gates
   def used_subagent(trace, md) -> bool:
       return any(r.from_subagent for r in trace.doc_reads)

   @trace_metric(assertion=True)      # a gate — use sparingly, every gate is a way to go red
   def under_cost_budget(trace, md) -> bool:
       return (trace.total_cost_usd or 0) <= 1.0
   ```

   The function name becomes the report column; no other wiring. Bools become 0/1
   scores (report average = rate) unless `assertion=True`. Built-ins: `skill_triggered`,
   `entry_point_reads`.
3. **Async / LLM-backed / cross-field logic** → a full `Evaluator` class registered in
   `run_eval.py` (see `judge.py` for the pattern). Rare.

## Author new cases

```bash
make generate PERSPECTIVE=business N=10 [BUSINESS="ferry operator"]
make critic     # independent LLM grades each candidate against the real doc text
make review     # you approve/reject/edit; approved cases land in datasets/
```

Generated cases go to `candidates/` with `status: candidate`; the critic scores
clarity, leakage, groundedness, and routing value (1-5) and marks all->=4 cases
`ready_for_review`. Only `make review` (a human) writes into `datasets/`.

Case authoring rules (enforced by the critic):
- The question never names a doc file or path.
- `expected_docs.required` is the minimal set needed to answer; rubric claims must be
  verifiable from those docs' text.
- `optimal_hops` counts doc reads on the shortest sensible path, entry point included
  (SUMMARY.md or README.md = hop 1); the path is written out in `rationale`.
- Rubrics are binary: "Pass requires ALL of:" / "Must NOT:" (+ optional "Bonus").

`expected_books` is wired the same way and activates once `lynk-wiki/books/` has content.

## Notes & known limits

- **Model pins**: `config.yaml` uses aliases where no dated snapshot exists; the
  *resolved* model per session is recorded in `meta.json` and is the trustworthy record.
- **Judge**: runs via the CLI (no temperature control) on a different model family than
  the agent (`claude-opus-4-8` vs `claude-sonnet-5`) to avoid self-grading bias.
- **Hop nondeterminism**: navigation varies between runs; treat `hop_efficiency` as a
  trend, use `REPEAT=3` when it matters.
- **Grep leak**: an agent can answer from Grep content output without Reading the doc —
  that surfaces as `suspect_answer: suspect`, not as a retrieval pass.

## Layout

```
lynk_evals/       runner.py (headless session) · trace.py (tool calls -> AgentTrace)
                  evaluators.py · judge.py · generate.py · critic.py · review.py
datasets/         approved cases (committed; humans only)
candidates/       generated cases awaiting critic + review (committed)
runs/             per-run traces + reports (gitignored)
tests/            unit tests for normalization, hop metric, dataset loading
```
