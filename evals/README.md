# lynk-build evals

Eval suites for the repo's skills — both plugin skills and the repo's own
`.claude/` skills. The shared framework lives in `harness/`; the suites live under
`suites/`, grouped by what they load. Simple by design: pytest + a YAML answer key
+ plain-text artifacts.

```
evals/
  conftest.py            shared fixtures: repo_dir, sha, the -k selection hook
  pyproject.toml         deps + pytest config (import-mode=importlib, pythonpath)
  harness/               the framework (importable) — the ONLY non-suite thing
    subject.py           the subject session (async SDK); run_subject(target=Target(mode,path))
    judge.py             reusable LLM judge (a second, tool-less SDK session)
    suite.py             the shared batch runner: wire() + build()
    report.py            artifact + run-report rendering
    cases.py             generic dataset loader (validated at load)
  suites/
    plugins/<plugin>/          conftest.py → target (plugins=[local])
      <skill>/                 evals_run.py · datasets/<set>.yml · evaluators/*.py · results/
    local/                     conftest.py → target (repo .claude, project mode)
      <skill>/                 same shape
```

A suite is tiny: its `evals_run.py` supplies a dataset (`datasets/*.yml`),
`evaluators/*.py`, and an `evaluate()` coroutine, then calls
`suite.wire(__file__)` + `suite.build(name, evaluate, directive)`. Everything else
— concurrency, artifacts, `-k` filtering, run reports — comes from `harness.suite`.
Its **target** (plugin vs the repo's `.claude/`) is declared once per group in the
`plugins/<plugin>/` or `local/` conftest, so sibling skills need no wiring.

Built on the **Claude Agent SDK** (`claude-agent-sdk`): each subject/judge is an
async in-process SDK session, so a suite runs its cases **concurrently**. The
subject runs on the latest **Sonnet** (what the plugin ships to); the judge grades
on **Opus** (a stronger model than the gradee).

## Running

```bash
cd evals
uv run pytest suites/plugins/lynk-build/lynk-research          # whole suite (concurrent)
uv run pytest suites/plugins/lynk-build/lynk-research -k q06   # just this case (batch honors -k)
uv run pytest suites/plugins/lynk-build                        # every suite for the plugin
uv run pytest suites/local/slugify                             # a repo .claude skill
uv run pytest                                                  # everything
EVAL_CONCURRENCY=8 uv run pytest suites/plugins/lynk-build/lynk-research
```

`EVAL_CONCURRENCY` (default 4) caps simultaneous sessions — raise it to go
faster, lower it if you hit rate limits. Each case costs real, live LLM calls (a
subject session + a judge). Retrieval runs are noisy — run a case a few times
before trusting a number.

## The lynk-research suite

The `lynk-research` skill routes a question through the library pipeline
(librarian picks books → scholars read chapters → the enrich hook injects the
chosen chapters' content). The suite is the **golden-questions confusion
matrix** (`datasets/golden-questions.yml`) — does routing fire when it should,
fire *precisely* when it should, stay quiet when it should, and not over-reach?

Two evaluators run per case:

1. **routing** (`evaluators/routing.py`) — deterministic. Parses which library
   chapters the pipeline *surfaced to the answer* — the chapter paths in the
   enrich hook's injection (the `selected chapters WITH their content` marker),
   NOT the whole transcript (which also carries the librarian's full
   `generate_book_toc` dump). Checks them against the case's `expect_routing`:
   `reach-book` · `reach-chapter` · `reach-nowhere` · `reach-book-no-chapter` ·
   `no-activation` (the skill should not fire at all — checked by whether
   lynk-research/librarian/scholar was invoked; these cases run WITHOUT the
   forcing directive, testing the skill's description-based triggering).
2. **citation** (`evaluators/citation.py`) — a judge grades one `answer_claim`:
   for hits, the answer answers from the book and cites `book · chapter`; for
   misses, it states the library doesn't cover it and doesn't fabricate.

### Verdicts

| Verdict | Meaning |
|---|---|
| **PASS** | routing reached the expected target **and** the answer used it / refused correctly |
| **SUSPECT** | the answer was right but the pipeline never surfaced the expected chapter — the answer likely came from the model's prior, not the library |
| **FAIL** | wrong routing (missed target, or over-reached on a trap), or a bad answer |
| **ERROR** | the subject session or the judge died — never misread as a wrong answer |

### Artifacts

```
<skill>/results/<timestamp>/
  meta.json        plugin SHA, verdict per case, total cost
  report.md        one line per case + totals, links to case reports
  <case-id>/       report.md · answer.md · transcript.jsonl · judge.json
```
plus one row per case in `<skill>/results/RESULTS.md` — the trend table (stamped
with the plugin SHA and model, so rows compare over time; between runs change
the plugin *or* the model, never both). Analysis is agentic: point a Claude
session at a run dir and ask why a case failed.

## Content under test

The golden questions test the **best-context** book, which lives in the plugin's
`library/best-context/` (`index.md` + `chapters/*.md`). The reach-chapter cases
pin specific chapter slugs (the chapter filename without extension); if you
rename or remove a chapter, update the matching case.

## Adding a skill suite

1. Pick the group — `suites/plugins/<plugin>/` (plugin skill) or `suites/local/`
   (a repo `.claude/` skill). If it's a new plugin, add `suites/plugins/<plugin>/
   conftest.py` with a `target` fixture (`Target(mode="plugin", path=...)`).
2. Make `suites/<group>/<skill>/` with `datasets/<set>.yml` and `evaluators/*.py`.
3. Write `evals_run.py`:

   ```python
   from harness import load_evaluator, suite
   my_eval = load_evaluator(__file__, "my_eval")

   async def evaluate(case, events, case_dir):
       r = my_eval.evaluate(case, events)          # your evaluators
       return ("PASS" if r["passed"] else "FAIL"), [r]

   globals().update(suite.wire(__file__))          # parametrize + dataset + run_dir
   globals().update(suite.build("myskill", evaluate))   # batch + eval_myskill test
   ```

`evaluate` is `async (case, events, case_dir) -> (verdict, [evaluator dict])`;
verdicts are `PASS` / `FAIL` / `SUSPECT` / `ERROR`. Pass `directive=lambda case: "..."`
to `build` to force/steer the skill per case (omit for none). The `case` dict is
skill-specific — evaluators define its shape; only `id` and `question` are required
by the loader. Deterministic evaluators (no LLM judge) are fine — see
`suites/local/slugify`.
