from typing import Literal

from pydantic import BaseModel, Field


class CaseInputs(BaseModel):
    question: str


class ExpectedFiles(BaseModel):
    required: list[str] = Field(default_factory=list)
    optional: list[str] = Field(default_factory=list)


class CaseMetadata(BaseModel):
    perspective: Literal["drawers", "business"]
    tags: list[str] = Field(default_factory=list)
    business: str | None = None
    expected_docs: ExpectedFiles
    expected_books: ExpectedFiles = Field(default_factory=ExpectedFiles)
    optimal_hops: int
    rubric: str
    rationale: str = ""


class DocRead(BaseModel):
    path: str  # normalized, plugin-root-relative (e.g. "semantics_docs/concepts/policy.md")
    order: int  # 1-based position among doc reads
    first_touch: bool
    offset: int | None = None
    limit: int | None = None
    from_subagent: bool = False


class SearchCall(BaseModel):
    tool: str  # Grep | Glob
    pattern: str = ""
    path: str | None = None  # normalized, None if the call had no path inside the plugin
    glob: str | None = None
    output_mode: str | None = None
    from_subagent: bool = False


class BookRead(BaseModel):
    """One `bk read` of one page, from the .bk/reads telemetry. Books are reached
    via the bk CLI, not the Read tool, so this — not DocRead — is the library signal."""

    book: str
    page: str  # page slug ("the-strict-brief", "index", "log")
    sha: str  # content hash bk recorded — the receipt that this exact text was read
    role: str  # librarian | reader | hook | unknown — who ran the read
    order: int  # 1-based, chronological across the session

    @property
    def path(self) -> str:  # plugin-root-relative, matches expected_books entries
        return f"library/{self.book}/{self.page}.md"


class Gap(BaseModel):
    """A library miss logged to .bk/gaps.jsonl — recorded demand for a page."""

    stage: str  # librarian | reader
    book: str | None = None
    intent: str = ""
    suggested: str = ""


class AgentTrace(BaseModel):
    answer: str = ""
    doc_reads: list[DocRead] = Field(default_factory=list)
    unique_docs_read: list[str] = Field(default_factory=list)
    # Library retrieval (parsed from .bk/ telemetry; empty on docs-only cases):
    book_reads: list[BookRead] = Field(default_factory=list)
    unique_books_read: list[str] = Field(default_factory=list)  # sorted "library/<book>/<page>.md"
    gaps: list[Gap] = Field(default_factory=list)
    searches: list[SearchCall] = Field(default_factory=list)
    other_tool_calls: list[str] = Field(default_factory=list)
    num_turns: int = 0
    duration_s: float = 0.0
    total_cost_usd: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    session_id: str = ""
    model: str = ""  # resolved model from the session's init message
    error: str | None = None  # set → session errored; assertions fail with this reason

    @property
    def errored(self) -> bool:
        return self.error is not None
