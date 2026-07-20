"""The generic suite runner, shared by every skill suite.

A suite's evals_run.py supplies only what's unique — its dataset (globbed),
evaluators, an `evaluate()` coroutine, and an optional per-case `directive` — and
gets the whole pytest machinery from here: concurrency, per-case artifacts, `-k`
filtering, verdict plumbing, and the run-level reports.

Two calls, both meant for `globals().update(...)` at module top level:

    wire(__file__)              → pytest_generate_tests + all_cases + run_dir fixtures
    build(name, evaluate, ...)  → the `batch` fixture + the `eval_<name>` test

`evaluate` is:  async (case, events, case_dir) -> (verdict:str, [evaluator dict])
`directive` is: (case) -> str|None   (system-prompt directive for that case; default none)
An evaluator dict is {"name", "passed": bool|None, "detail", ...}.
"""

import asyncio
import os
from datetime import datetime
from pathlib import Path

import pytest

from harness import report
from harness.cases import load_cases
from harness.subject import final_answer, model_of, run_subject, total_cost

CONCURRENCY = int(os.environ.get("EVAL_CONCURRENCY", "4"))


def wire(conftest_or_module_file):
    """Fixtures/hooks a suite needs, keyed off its own location. The dataset is the
    single *.yml under datasets/; results land under the suite's results/."""
    suite_dir = Path(conftest_or_module_file).resolve().parent
    dataset = next(suite_dir.glob("datasets/*.yml"))
    results = suite_dir / "results"

    def pytest_generate_tests(metafunc):
        if "case" in metafunc.fixturenames:
            cases = load_cases(dataset)
            metafunc.parametrize("case", cases, ids=[c["id"] for c in cases])

    @pytest.fixture(scope="session")
    def all_cases():
        return load_cases(dataset)

    @pytest.fixture(scope="session")
    def run_dir():
        d = results / datetime.now().strftime("%Y%m%d-%H%M%S")
        d.mkdir(parents=True)
        return d

    return {"pytest_generate_tests": pytest_generate_tests,
            "all_cases": all_cases, "run_dir": run_dir}


async def _run_case(case, sem, target, directive, evaluate, run_dir, sha):
    case_dir = run_dir / case["id"]
    case_dir.mkdir(parents=True, exist_ok=True)
    error = None
    try:
        async with sem:
            events, error = await run_subject(
                case["question"], case_dir / "transcript.jsonl",
                target=target, append_system_prompt=directive(case))
        (case_dir / "answer.md").write_text(final_answer(events) or "(no answer)")
        if error:
            verdict, evaluators = "ERROR", []
        else:
            verdict, evaluators = await evaluate(case, events, case_dir)
    except Exception as e:                     # a case must never take down the batch
        error = f"case errored: {type(e).__name__}: {str(e)[:200]}"
        events, verdict, evaluators = [], "ERROR", []

    cost, model = total_cost(events), model_of(events)
    detail = " | ".join(f"{e['name']}: {e['detail']}" for e in evaluators) or (error or "")
    (case_dir / "report.md").write_text(
        report.render_case_report(case, verdict, evaluators, run_dir.name, sha, cost, error, model))
    return {
        "id": case["id"], "verdict": verdict, "cost": cost, "detail": detail,
        "error": error or (detail if verdict == "ERROR" else None),
        "summary": report.summary_line(case, verdict, evaluators),
        "row": report.results_row(case, verdict, evaluators, run_dir.name, sha, cost, model),
    }


async def _run_batch(cases, target, directive, evaluate, run_dir, sha):
    sem = asyncio.Semaphore(CONCURRENCY)
    outcomes = await asyncio.gather(
        *[_run_case(c, sem, target, directive, evaluate, run_dir, sha) for c in cases])
    report.write_run_reports(run_dir, run_dir.parent, sha,
                             [{k: o[k] for k in ("id", "verdict", "cost", "summary", "row")}
                              for o in outcomes])
    return {o["id"]: o for o in outcomes}


def build(name, evaluate, directive=None):
    """Return {`batch` fixture, `eval_<name>` test} to globals().update() into the
    suite module. The batch runs the selected cases once, concurrently, and writes
    the run reports; each parametrized test asserts on its precomputed outcome."""
    directive = directive or (lambda case: None)

    @pytest.fixture(scope="session")
    def batch(all_cases, target, run_dir, sha, request):
        selected = getattr(request.config, "_selected_cases", None)
        cases = [c for c in all_cases if not selected or c["id"] in selected]
        return asyncio.run(_run_batch(cases, target, directive, evaluate, run_dir, sha))

    @pytest.mark.evaluation
    def _eval(case, batch):
        o = batch[case["id"]]
        if o["verdict"] == "ERROR":
            pytest.fail(f"{o['error'] or o['detail']} — see results/{o['id']}/")
        if o["verdict"] == "SUSPECT":
            pytest.fail(f"SUSPECT: answer right but library not reached — {o['detail']}")
        assert o["verdict"] == "PASS", o["detail"]

    _eval.__name__ = f"eval_{name}"
    return {"batch": batch, f"eval_{name}": _eval}
