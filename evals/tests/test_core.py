import json
from types import SimpleNamespace

import pytest

from lynk_evals.datasets import load_cases
from lynk_evals.evaluators import ExpectedFilesRead, HopEfficiency
from lynk_evals.schema import AgentTrace, CaseMetadata, DocRead, ExpectedFiles
from lynk_evals.trace import build_trace, normalize_plugin_path


def read(path: str, order: int, first: bool = True) -> DocRead:
    return DocRead(path=path, order=order, first_touch=first)


def ctx_for(trace: AgentTrace, required: list[str], optimal_hops: int = 3) -> SimpleNamespace:
    md = CaseMetadata(
        perspective="drawers",
        expected_docs=ExpectedFiles(required=required),
        optimal_hops=optimal_hops,
        rubric="-",
    )
    return SimpleNamespace(output=trace, metadata=md)


class TestNormalizePluginPath:
    def test_local_absolute_path(self):
        raw = "/Users/x/repo/lynk-wiki/semantics_docs/concepts/policy.md"
        assert normalize_plugin_path(raw) == "semantics_docs/concepts/policy.md"

    def test_plugin_root_env_var(self):
        raw = "${CLAUDE_PLUGIN_ROOT}/semantics_docs/README.md"
        assert normalize_plugin_path(raw) == "semantics_docs/README.md"

    def test_installed_cache_prefix(self):
        raw = "/Users/x/.claude/plugins/cache/lynk-build/lynk-wiki/books/modeling.md"
        assert normalize_plugin_path(raw) == "books/modeling.md"

    def test_plugin_root_non_content_file(self):
        raw = "/repo/lynk-wiki/skills/lynk-wiki/SKILL.md"
        assert normalize_plugin_path(raw) == "skills/lynk-wiki/SKILL.md"

    def test_plugin_root_itself(self):
        assert normalize_plugin_path("/repo/lynk-wiki/") == "."

    def test_outside_plugin(self):
        assert normalize_plugin_path("/etc/hosts") is None


class TestBuildTrace:
    def test_first_touch_and_rereads(self):
        calls = [
            {"tool": "Read", "input": {"file_path": "/r/lynk-wiki/semantics_docs/SUMMARY.md"}},
            {"tool": "Read", "input": {"file_path": "/r/lynk-wiki/semantics_docs/concepts/policy.md"}},
            {"tool": "Read", "input": {"file_path": "/r/lynk-wiki/semantics_docs/SUMMARY.md"}},
        ]
        trace = build_trace(calls)
        assert [r.first_touch for r in trace.doc_reads] == [True, True, False]
        assert trace.unique_docs_read == [
            "semantics_docs/SUMMARY.md",
            "semantics_docs/concepts/policy.md",
        ]

    def test_subagent_reads_included(self):
        calls = [
            {
                "tool": "Read",
                "input": {"file_path": "/r/lynk-wiki/semantics_docs/README.md"},
                "parent_tool_use_id": "tu_123",
            }
        ]
        trace = build_trace(calls)
        assert trace.doc_reads[0].from_subagent is True

    def test_plugin_scoped_grep_counted(self):
        calls = [{"tool": "Grep", "input": {"pattern": "policy", "path": "/r/lynk-wiki", "glob": "*.md"}}]
        trace = build_trace(calls)
        assert len(trace.searches) == 1
        assert trace.searches[0].path == "."

    def test_non_doc_read_is_other(self):
        calls = [{"tool": "Read", "input": {"file_path": "/etc/hosts"}}]
        trace = build_trace(calls)
        assert trace.doc_reads == []
        assert trace.other_tool_calls == ["Read(/etc/hosts)"]


class TestHopEfficiency:
    def test_exact_optimal(self):
        trace = AgentTrace(doc_reads=[read("semantics_docs/SUMMARY.md", 1), read("a.md", 2)])
        trace.doc_reads[1].path = "semantics_docs/concepts/policy.md"
        out = HopEfficiency().evaluate(
            ctx_for(trace, ["semantics_docs/concepts/policy.md"], optimal_hops=2)
        )
        assert out["hop_efficiency"].value == 1.0
        assert out["hops"] == 2

    def test_capped_at_one_when_beating_optimal(self):
        trace = AgentTrace(doc_reads=[read("semantics_docs/concepts/policy.md", 1)])
        out = HopEfficiency().evaluate(
            ctx_for(trace, ["semantics_docs/concepts/policy.md"], optimal_hops=100)
        )
        assert out["hop_efficiency"].value == 1.0

    def test_rereads_not_counted(self):
        trace = AgentTrace(
            doc_reads=[
                read("semantics_docs/SUMMARY.md", 1),
                read("semantics_docs/SUMMARY.md", 2, first=False),
                read("semantics_docs/concepts/policy.md", 3),
            ]
        )
        out = HopEfficiency().evaluate(
            ctx_for(trace, ["semantics_docs/concepts/policy.md"], optimal_hops=2)
        )
        assert out["hops"] == 2

    def test_never_completed(self):
        trace = AgentTrace(doc_reads=[read("semantics_docs/README.md", 1)])
        out = HopEfficiency().evaluate(ctx_for(trace, ["semantics_docs/concepts/policy.md"]))
        assert out["hop_efficiency"].value == 0.0
        assert "never completed" in out["hop_efficiency"].reason

    def test_errored_session(self):
        trace = AgentTrace(error="session errored: timeout after 240s")
        out = HopEfficiency().evaluate(ctx_for(trace, ["semantics_docs/README.md"]))
        assert out["hop_efficiency"].value == 0.0


class TestExpectedFilesRead:
    def test_missing_required_fails_with_paths_in_reason(self):
        trace = AgentTrace(unique_docs_read=["semantics_docs/concepts/policy.md"])
        out = ExpectedFilesRead(source="docs").evaluate(
            ctx_for(trace, ["semantics_docs/concepts/policy.md", "semantics_docs/concepts/skill.md"])
        )
        assert out["required_docs_read"].value is False
        assert "skill.md" in out["required_docs_read"].reason
        assert out["docs_recall"] == 0.5

    def test_books_silent_when_unset(self):
        trace = AgentTrace()
        out = ExpectedFilesRead(source="books").evaluate(ctx_for(trace, ["semantics_docs/README.md"]))
        assert out == {}

    def test_errored_session_fails_assertion(self):
        trace = AgentTrace(error="session errored: boom")
        out = ExpectedFilesRead(source="docs").evaluate(ctx_for(trace, ["semantics_docs/README.md"]))
        assert out["required_docs_read"].value is False


class TestDatasetLoading:
    def test_seed_datasets_load(self):
        cases = load_cases()
        assert len(cases) == 10
        assert len({c.name for c in cases}) == 10

    def test_nonexistent_expected_doc_fails(self, tmp_path):
        bad = tmp_path / "bad.yaml"
        bad.write_text(
            """
cases:
- name: broken
  inputs: {question: "q?"}
  metadata:
    perspective: drawers
    expected_docs: {required: [semantics_docs/nope.md]}
    optimal_hops: 1
    rubric: "-"
"""
        )
        with pytest.raises(ValueError, match="nope.md"):
            load_cases([bad])


class TestBkTelemetry:
    def _write_bk(self, root, read_files, gaps=None):
        bk = root / ".bk"
        (bk / "reads").mkdir(parents=True)
        for i, records in enumerate(read_files):
            (bk / "reads" / f"s{i}.jsonl").write_text(
                "\n".join(json.dumps(r) for r in records)
            )
        if gaps is not None:
            (bk / "gaps.jsonl").write_text("\n".join(json.dumps(g) for g in gaps))
        return bk

    def test_reads_are_ts_ordered_and_deduped(self, tmp_path):
        bk = self._write_bk(
            tmp_path,
            [
                [{"ts": "2026-07-16T20:00:03", "role": "hook", "book": "subagents",
                  "pages": [{"page": "the-strict-brief", "sha": "a"},
                            {"page": "orchestrator-workers", "sha": "b"}]}],
                [{"ts": "2026-07-16T20:00:01", "role": "reader", "book": "subagents",
                  "pages": [{"page": "the-strict-brief", "sha": "a"}]}],
            ],
        )
        trace = build_trace([], bk_dir=bk)
        assert [r.role for r in trace.book_reads] == ["reader", "hook", "hook"]
        assert trace.book_reads[0].page == "the-strict-brief"
        assert trace.unique_books_read == [
            "library/subagents/orchestrator-workers.md",
            "library/subagents/the-strict-brief.md",
        ]

    def test_gaps_parse(self, tmp_path):
        bk = self._write_bk(
            tmp_path, [], gaps=[{"stage": "librarian", "intent": "x", "suggested": "y"}]
        )
        trace = build_trace([], bk_dir=bk)
        assert len(trace.gaps) == 1 and trace.gaps[0].stage == "librarian"

    def test_no_bk_dir_is_empty(self):
        trace = build_trace([], bk_dir=None)
        assert trace.book_reads == [] and trace.unique_books_read == [] and trace.gaps == []

    def test_books_evaluator_reads_from_bk(self, tmp_path):
        bk = self._write_bk(
            tmp_path,
            [[{"ts": "t", "role": "hook", "book": "subagents",
               "pages": [{"page": "the-strict-brief", "sha": "a"}]}]],
        )
        trace = build_trace([], bk_dir=bk)
        md = CaseMetadata(
            perspective="drawers",
            expected_docs=ExpectedFiles(),
            expected_books=ExpectedFiles(required=["library/subagents/the-strict-brief.md"]),
            optimal_hops=1,
            rubric="-",
        )
        out = ExpectedFilesRead(source="books").evaluate(
            SimpleNamespace(output=trace, metadata=md)
        )
        assert out["required_books_read"].value is True
        assert out["books_recall"] == 1.0
