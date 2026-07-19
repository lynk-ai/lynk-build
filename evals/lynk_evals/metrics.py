"""Tier-2 evaluators: deterministic trace metrics, one function each.

Write a function (AgentTrace, CaseMetadata) -> value, decorate it, done — the
function name becomes a report column. No other wiring.

    @trace_metric                    # score/label column, never gates a case
    def my_signal(trace, md) -> bool | int | float | str: ...

    @trace_metric(assertion=True)    # a gate: False makes the case red
    def my_gate(trace, md) -> bool: ...

Value handling: bools on non-assertion metrics become 0/1 scores (so the report
average reads as a rate); assertion metrics stay bools; strings become labels.
On an errored session, assertions fail with the session error and plain metrics
are omitted (measuring a dead session is meaningless). A metric that raises
shows up as an "error: ..." label instead of killing the run.

Checks that belong elsewhere: answer-content checks go in the case rubric
(the judge grades them — no code needed); async or LLM-backed checks get a
full Evaluator class (see judge.py).
"""

from dataclasses import dataclass
from typing import Callable

from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

from .schema import AgentTrace, CaseInputs, CaseMetadata

_REGISTRY: dict[str, tuple[Callable, bool]] = {}


def trace_metric(fn: Callable | None = None, *, assertion: bool = False):
    def register(f: Callable) -> Callable:
        if f.__name__ in _REGISTRY:
            raise ValueError(f"trace_metric {f.__name__!r} registered twice")
        _REGISTRY[f.__name__] = (f, assertion)
        return f

    return register(fn) if fn is not None else register


@dataclass
class TraceMetrics(Evaluator[CaseInputs, AgentTrace, CaseMetadata]):
    """Runs every registered @trace_metric and emits its value under its name."""

    def evaluate(self, ctx: EvaluatorContext[CaseInputs, AgentTrace, CaseMetadata]) -> dict:
        out: dict = {}
        for name, (fn, is_assertion) in _REGISTRY.items():
            if ctx.output.errored:
                if is_assertion:
                    out[name] = EvaluationReason(False, reason=ctx.output.error)
                continue
            try:
                value = fn(ctx.output, ctx.metadata)
            except Exception as e:
                out[name] = f"error: {type(e).__name__}: {e}"
                continue
            if isinstance(value, EvaluationReason):
                out[name] = value
            elif is_assertion:
                out[name] = bool(value)
            elif isinstance(value, bool):
                out[name] = int(value)
            else:
                out[name] = value
        return out


# --- built-in metrics ---------------------------------------------------------

ENTRY_POINTS = {"semantics_docs/README.md", "semantics_docs/SUMMARY.md"}


@trace_metric
def skill_triggered(trace: AgentTrace, md: CaseMetadata) -> bool:
    """Did the lynk-wiki skill fire during the session?"""
    return "Skill" in trace.other_tool_calls


@trace_metric
def entry_point_reads(trace: AgentTrace, md: CaseMetadata) -> int:
    """First-touch reads of README.md/SUMMARY.md; 2 = paying the double-entry hop tax."""
    return sum(1 for r in trace.doc_reads if r.first_touch and r.path in ENTRY_POINTS)


# --- library retrieval (populated from .bk/ telemetry; 0 on docs-only cases) ---


@trace_metric
def book_pages_read(trace: AgentTrace, md: CaseMetadata) -> int:
    """Distinct library pages the bk pipeline read — the library analog of doc reads.

    0 on a library case whose answer was judged correct is the prior-knowledge tell:
    the agent answered without opening the books.
    """
    return len(trace.unique_books_read)


@trace_metric
def library_gaps(trace: AgentTrace, md: CaseMetadata) -> int:
    """Misses the pipeline logged to .bk/gaps.jsonl (no book/page served the objective)."""
    return len(trace.gaps)
