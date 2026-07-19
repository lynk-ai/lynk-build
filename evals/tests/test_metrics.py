from types import SimpleNamespace

import pytest
from pydantic_evals.evaluators import EvaluationReason

from lynk_evals.metrics import _REGISTRY, TraceMetrics, trace_metric
from lynk_evals.schema import AgentTrace, CaseMetadata, DocRead, ExpectedFiles


def ctx_for(trace: AgentTrace) -> SimpleNamespace:
    md = CaseMetadata(
        perspective="drawers",
        expected_docs=ExpectedFiles(required=["semantics_docs/README.md"]),
        optimal_hops=1,
        rubric="-",
    )
    return SimpleNamespace(output=trace, metadata=md)


@pytest.fixture
def scratch_registry():
    saved = dict(_REGISTRY)
    yield
    _REGISTRY.clear()
    _REGISTRY.update(saved)


class TestRegistry:
    def test_bool_becomes_01_score_when_not_assertion(self, scratch_registry):
        @trace_metric
        def always_true(trace, md):
            return True

        out = TraceMetrics().evaluate(ctx_for(AgentTrace()))
        assert out["always_true"] == 1  # int, not bool -> score column

    def test_assertion_stays_bool(self, scratch_registry):
        @trace_metric(assertion=True)
        def my_gate(trace, md):
            return 1  # truthy non-bool

        out = TraceMetrics().evaluate(ctx_for(AgentTrace()))
        assert out["my_gate"] is True

    def test_errored_session_fails_assertions_and_omits_metrics(self, scratch_registry):
        @trace_metric
        def a_metric(trace, md):
            return 42

        @trace_metric(assertion=True)
        def a_gate(trace, md):
            return True

        out = TraceMetrics().evaluate(ctx_for(AgentTrace(error="session errored: boom")))
        assert "a_metric" not in out
        assert out["a_gate"].value is False
        assert "boom" in out["a_gate"].reason

    def test_raising_metric_becomes_error_label(self, scratch_registry):
        @trace_metric
        def broken(trace, md):
            raise RuntimeError("oops")

        out = TraceMetrics().evaluate(ctx_for(AgentTrace()))
        assert out["broken"].startswith("error: RuntimeError")
        assert "skill_triggered" in out  # other metrics unaffected

    def test_duplicate_name_rejected(self, scratch_registry):
        @trace_metric
        def dup(trace, md):
            return 1

        with pytest.raises(ValueError, match="registered twice"):

            @trace_metric
            def dup(trace, md):  # noqa: F811
                return 2

    def test_evaluation_reason_passthrough(self, scratch_registry):
        @trace_metric
        def with_reason(trace, md):
            return EvaluationReason(0.5, reason="because")

        out = TraceMetrics().evaluate(ctx_for(AgentTrace()))
        assert out["with_reason"].value == 0.5


class TestBuiltins:
    def test_skill_triggered(self):
        out = TraceMetrics().evaluate(ctx_for(AgentTrace(other_tool_calls=["Skill"])))
        assert out["skill_triggered"] == 1
        out = TraceMetrics().evaluate(ctx_for(AgentTrace()))
        assert out["skill_triggered"] == 0

    def test_entry_point_reads_counts_first_touch_only(self):
        trace = AgentTrace(
            doc_reads=[
                DocRead(path="semantics_docs/README.md", order=1, first_touch=True),
                DocRead(path="semantics_docs/SUMMARY.md", order=2, first_touch=True),
                DocRead(path="semantics_docs/SUMMARY.md", order=3, first_touch=False),
                DocRead(path="semantics_docs/concepts/policy.md", order=4, first_touch=True),
            ]
        )
        out = TraceMetrics().evaluate(ctx_for(trace))
        assert out["entry_point_reads"] == 2
