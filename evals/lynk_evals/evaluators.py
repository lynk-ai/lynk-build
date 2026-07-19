from dataclasses import dataclass
from typing import Literal

from pydantic_evals.evaluators import EvaluationReason, Evaluator, EvaluatorContext

from .schema import AgentTrace, CaseInputs, CaseMetadata

Ctx = EvaluatorContext[CaseInputs, AgentTrace, CaseMetadata]


@dataclass
class ExpectedFilesRead(Evaluator[CaseInputs, AgentTrace, CaseMetadata]):
    """Did the session Read the expected files? Assertion on required, recall on both."""

    source: Literal["docs", "books"] = "docs"

    def evaluate(self, ctx: Ctx) -> dict:
        expected = ctx.metadata.expected_docs if self.source == "docs" else ctx.metadata.expected_books
        if not (expected.required or expected.optional):
            return {}  # wired but silent — e.g. books before books/ has content

        trace = ctx.output
        if trace.errored:
            return {f"required_{self.source}_read": EvaluationReason(False, reason=trace.error)}

        # Docs are reached via the Read tool; books via the bk CLI (.bk telemetry).
        read = set(trace.unique_docs_read if self.source == "docs" else trace.unique_books_read)
        out: dict = {}
        if expected.required:
            required = set(expected.required)
            missing = sorted(required - read)
            out[f"required_{self.source}_read"] = EvaluationReason(
                not missing,
                reason="all required read" if not missing else "missing: " + ", ".join(missing),
            )
            out[f"{self.source}_recall"] = round(len(required & read) / len(required), 3)
        if expected.optional:
            optional = set(expected.optional)
            out[f"optional_{self.source}_read"] = round(len(optional & read) / len(optional), 3)
        return out


@dataclass
class HopEfficiency(Evaluator[CaseInputs, AgentTrace, CaseMetadata]):
    """min(1, optimal/actual) where actual = first-touch reads until the required set completes.

    Trend metric, never a hard gate. Raw counts emitted alongside for debugging.
    """

    def evaluate(self, ctx: Ctx) -> dict:
        trace = ctx.output
        first_touch = [r.path for r in trace.doc_reads if r.first_touch]
        raw = {
            "doc_reads": len(trace.doc_reads),
            "searches": len(trace.searches),
        }
        if trace.errored:
            return {"hop_efficiency": EvaluationReason(0.0, reason=trace.error), "hops": len(first_touch), **raw}

        remaining = set(ctx.metadata.expected_docs.required)
        hops_to_complete = None
        for i, path in enumerate(first_touch, start=1):
            remaining.discard(path)
            if not remaining:
                hops_to_complete = i
                break

        if hops_to_complete is None:
            return {
                "hop_efficiency": EvaluationReason(
                    0.0, reason=f"required set never completed; missing {sorted(remaining)}"
                ),
                "hops": len(first_touch),
                **raw,
            }

        optimal = ctx.metadata.optimal_hops
        efficiency = min(1.0, optimal / hops_to_complete)
        return {
            "hop_efficiency": EvaluationReason(
                round(efficiency, 3),
                reason=f"{hops_to_complete} hops to complete required set vs optimal {optimal}",
            ),
            "hops": hops_to_complete,
            **raw,
        }
