"""Orchestrate an eval run: filter cases, execute, score, write the run directory."""

import hashlib
import importlib.metadata
import json
import subprocess
from datetime import UTC, datetime
from pathlib import Path

import logfire
from pydantic_evals import Dataset

from .config import DATASETS_DIR, PLUGIN_ROOT, REPO_ROOT, RUNS_DIR, Config
from .datasets import filter_cases, load_cases
from .evaluators import ExpectedFilesRead, HopEfficiency
from .judge import AnswerRubricJudge
from .metrics import TraceMetrics
from .runner import run_case
from .schema import AgentTrace, CaseInputs


async def run_eval(
    cfg: Config,
    tag: str | None = None,
    perspective: str | None = None,
    case: str | None = None,
    repeat: int = 1,
    label: str | None = None,
) -> Path:
    logfire.configure(send_to_logfire="if-token-present", service_name="lynk-evals", console=False)

    cases = filter_cases(load_cases(), tag=tag, perspective=perspective, case=case)
    if not cases:
        raise SystemExit("no cases match the given filters")

    stamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_dir = RUNS_DIR / (f"{stamp}-{label}" if label else stamp)
    traces_dir = run_dir / "traces"
    traces_dir.mkdir(parents=True)

    name_by_question = {c.inputs.question: c.name for c in cases}
    # A case with expected_books drives the library pipeline (bk CLI + subagents);
    # everything else navigates semantics_docs. The profile picks the tool policy.
    profile_by_question = {
        c.inputs.question: (
            "library"
            if (c.metadata.expected_books.required or c.metadata.expected_books.optional)
            else "docs"
        )
        for c in cases
    }
    trace_counts: dict[str, int] = {}

    async def task(inputs: CaseInputs) -> AgentTrace:
        trace = await run_case(
            inputs.question, cfg, profile=profile_by_question.get(inputs.question, "docs")
        )
        name = name_by_question.get(inputs.question, "unknown")
        trace_counts[name] = trace_counts.get(name, 0) + 1
        n = trace_counts[name]
        fname = f"{name}.json" if n == 1 else f"{name}#{n}.json"
        (traces_dir / fname).write_text(trace.model_dump_json(indent=2))
        return trace

    meta = _run_metadata(cfg, cases, tag=tag, perspective=perspective, case=case, repeat=repeat)

    dataset = Dataset(
        name="lynk-wiki-evals",
        cases=cases,
        evaluators=[
            ExpectedFilesRead(source="docs"),
            ExpectedFilesRead(source="books"),
            HopEfficiency(),
            TraceMetrics(),
            AnswerRubricJudge(model=cfg.judge_model),
        ],
    )
    report = await dataset.evaluate(
        task,
        name=run_dir.name,
        max_concurrency=cfg.max_concurrency,
        repeat=repeat,
        metadata=meta,
    )

    meta["resolved_models"] = sorted(
        {t["model"] for t in map(_load_trace, traces_dir.glob("*.json")) if t.get("model")}
    )
    (run_dir / "meta.json").write_text(json.dumps(meta, indent=2))

    render_kwargs = dict(include_reasons=False, include_averages=True)
    report.print(**render_kwargs)
    (run_dir / "report.txt").write_text(report.render(width=200, **render_kwargs))
    (run_dir / "report.json").write_text(json.dumps(_report_dict(report), indent=2))

    print(f"\nrun dir: {run_dir}")
    return run_dir


def _load_trace(path: Path) -> dict:
    return json.loads(path.read_text())


def _report_dict(report) -> dict:
    def result_dict(results: dict) -> dict:
        return {
            k: {"value": r.value, "reason": r.reason}
            for k, r in results.items()
        }

    return {
        "cases": [
            {
                "name": c.name,
                "assertions": result_dict(c.assertions),
                "scores": result_dict(c.scores),
                "labels": result_dict(c.labels),
                "metrics": dict(c.metrics),
                "task_duration_s": round(c.task_duration, 2),
            }
            for c in report.cases
        ],
    }


def _run_metadata(cfg: Config, cases: list, **filters) -> dict:
    def git(*args: str) -> str:
        return subprocess.run(
            ["git", *args], cwd=REPO_ROOT, capture_output=True, text=True
        ).stdout.strip()

    plugin = json.loads((PLUGIN_ROOT / ".claude-plugin" / "plugin.json").read_text())
    dataset_hashes = {
        f.name: hashlib.sha256(f.read_bytes()).hexdigest()[:16]
        for f in sorted(DATASETS_DIR.glob("*.yaml"))
    }
    try:
        cli_version = subprocess.run(
            ["claude", "--version"], capture_output=True, text=True
        ).stdout.strip()
    except FileNotFoundError:
        cli_version = "unknown"

    return {
        "timestamp": datetime.now(UTC).isoformat(),
        "git_sha": git("rev-parse", "HEAD"),
        "git_dirty": bool(git("status", "--porcelain")),
        "plugin_version": plugin.get("version"),
        "dataset_hashes": dataset_hashes,
        "config": cfg.model_dump(),
        "filters": {k: v for k, v in filters.items() if v},
        "n_cases": len(cases),
        "claude_agent_sdk_version": importlib.metadata.version("claude-agent-sdk"),
        "claude_cli_version": cli_version,
    }
