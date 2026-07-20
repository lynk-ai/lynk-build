# eval suites

Pytest eval harness for the repo's skills. Framework in `harness/`; suites under
`suites/<group>/<skill>/` (`plugins/<plugin>/` or `local/`). Full design in
README.md — read it before changing anything here.

## Rules

- Run from `evals/`: `uv run pytest suites/plugins/lynk-build/lynk-research`
  (`-k <case-id>` for one case). Every case costs real money (subject + judge) —
  don't run casually. `EVAL_CONCURRENCY` (default 4) caps simultaneous sessions.
  Subject on Sonnet (`SUBJECT_MODEL`, harness/subject.py); judge on Opus
  (`JUDGE_MODEL`, harness/judge.py).
- A suite is only its dataset + evaluators + an `evaluate()` coroutine + the two
  `globals().update(suite.wire(__file__) / suite.build(name, evaluate, directive))`
  calls. The shared batch (concurrency, artifacts, `-k`, reports) lives in
  `harness/suite.py` — don't re-implement it per suite.
- The subject loads a `Target` (from the group's conftest `target` fixture):
  `mode="plugin"` → `plugins=[local]` in a throwaway cwd; `mode="project"` → run in
  the repo with `setting_sources=["project"]` (its `.claude/`). The user's global
  `~/.claude` never loads either way.
- Built on `claude-agent-sdk`; pytest runs in `--import-mode=importlib` + `pythonpath=["."]`
  so the duplicate `evals_run.py` basenames (hyphenated, non-package dirs) don't clash.
  Evaluators load by file path via `harness.load_evaluator(__file__, name)`.
- Artifacts are written BEFORE asserts (in the batch) — a failing case keeps its
  trace; the root `report.md` / `meta.json` / `RESULTS.md` write when the batch finishes.
- Verdicts (PASS / SUSPECT / FAIL / ERROR) are load-bearing: ERROR means the
  session/judge died (never read as FAIL); SUSPECT means the answer was right but
  the library was never reached.
- Routing signal (lynk-research): parse chapter paths ONLY from the enrich hook's
  injection (`selected chapters WITH their content`), never the whole transcript —
  the librarian's `generate_book_toc` dumps every chapter path in the book.
- `datasets/*.yml` is the reviewable answer key. A `case` is a plain dict;
  evaluators define its shape (only `id` + `question` are required). Deterministic
  evaluators (no judge) are fine — see `suites/local/slugify`.
