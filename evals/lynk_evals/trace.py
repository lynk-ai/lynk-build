"""Turn raw tool-call events from a session into an AgentTrace."""

import json
from pathlib import Path

from .schema import AgentTrace, BookRead, DocRead, Gap, SearchCall

CONTENT_MARKERS = ("semantics_docs/", "books/")
PLUGIN_ROOT_NAMES = ("lynk-wiki", "${CLAUDE_PLUGIN_ROOT}")


def normalize_plugin_path(raw: str) -> str | None:
    """Plugin-root-relative path, or None if the path is outside the plugin.

    Handles every prefix shape a session can produce: the local repo path, an
    installed-cache path, or a literal ${CLAUDE_PLUGIN_ROOT}.
    """
    s = str(raw).replace("\\", "/").rstrip("/")
    for marker in CONTENT_MARKERS:
        idx = s.rfind(marker)
        if idx != -1:
            return s[idx:]
    for name in PLUGIN_ROOT_NAMES:
        if s == name or s.endswith("/" + name):
            return "."
        # First occurrence, not last: the plugin contains a subdir also named
        # lynk-wiki (skills/lynk-wiki/), and the root is always the earlier segment.
        idx = s.find(name + "/")
        if idx != -1:
            return s[idx + len(name) + 1 :].lstrip("/") or "."
    return None


def is_doc_path(normalized: str) -> bool:
    return normalized.startswith(CONTENT_MARKERS)


def parse_bk(bk_dir: Path) -> dict:
    """Parse the library's own telemetry (.bk/) into book_reads + gaps.

    Book content is reached through the `bk` CLI, so the Read-tool trace is blind
    to it; `.bk/reads/*.jsonl` (one line per `bk read`) is the authoritative record
    of which pages were read, by which role, with the content hash. `.bk/gaps.jsonl`
    is the miss log. Absent .bk/ (docs-only case, or nothing retrieved) → empty.
    """
    reads_raw: list[dict] = []
    reads_root = bk_dir / "reads"
    if reads_root.is_dir():
        for f in sorted(reads_root.glob("*.jsonl")):
            for line in f.read_text().splitlines():
                if not line.strip():
                    continue
                try:
                    rec = json.loads(line)
                except json.JSONDecodeError:
                    continue
                for pg in rec.get("pages", []):
                    reads_raw.append(
                        {
                            "ts": rec.get("ts", ""),
                            "role": rec.get("role", "unknown"),
                            "book": rec.get("book", ""),
                            "page": pg.get("page", ""),
                            "sha": pg.get("sha", ""),
                        }
                    )
    reads_raw.sort(key=lambda r: r["ts"])
    book_reads = [
        BookRead(book=r["book"], page=r["page"], sha=r["sha"], role=r["role"], order=i)
        for i, r in enumerate(reads_raw, start=1)
    ]

    gaps: list[Gap] = []
    gaps_file = bk_dir / "gaps.jsonl"
    if gaps_file.exists():
        for line in gaps_file.read_text().splitlines():
            if not line.strip():
                continue
            try:
                g = json.loads(line)
            except json.JSONDecodeError:
                continue
            gaps.append(
                Gap(
                    stage=g.get("stage", ""),
                    book=g.get("book"),
                    intent=g.get("intent", ""),
                    suggested=g.get("suggested", ""),
                )
            )
    return {"book_reads": book_reads, "gaps": gaps}


def build_trace(tool_calls: list[dict], bk_dir: Path | None = None, **session_fields) -> AgentTrace:
    """tool_calls: ordered [{"tool", "input", "parent_tool_use_id"}, ...].

    bk_dir: the session's .bk/ directory, if any — parsed for library retrieval.
    """
    doc_reads: list[DocRead] = []
    searches: list[SearchCall] = []
    others: list[str] = []
    seen: set[str] = set()

    for call in tool_calls:
        tool = call["tool"]
        inp = call.get("input") or {}
        from_subagent = call.get("parent_tool_use_id") is not None

        if tool == "Read":
            norm = normalize_plugin_path(inp.get("file_path", ""))
            if norm and is_doc_path(norm):
                doc_reads.append(
                    DocRead(
                        path=norm,
                        order=len(doc_reads) + 1,
                        first_touch=norm not in seen,
                        offset=inp.get("offset"),
                        limit=inp.get("limit"),
                        from_subagent=from_subagent,
                    )
                )
                seen.add(norm)
            else:
                others.append(f"Read({inp.get('file_path', '?')})")
        elif tool in ("Grep", "Glob"):
            norm = normalize_plugin_path(inp.get("path", "") or "")
            searches.append(
                SearchCall(
                    tool=tool,
                    pattern=inp.get("pattern", ""),
                    path=norm,
                    glob=inp.get("glob"),
                    output_mode=inp.get("output_mode"),
                    from_subagent=from_subagent,
                )
            )
        else:
            others.append(tool)

    bk = parse_bk(bk_dir) if bk_dir is not None else {"book_reads": [], "gaps": []}
    unique_books = sorted({r.path for r in bk["book_reads"]})

    return AgentTrace(
        doc_reads=doc_reads,
        unique_docs_read=sorted(seen),
        book_reads=bk["book_reads"],
        unique_books_read=unique_books,
        gaps=bk["gaps"],
        searches=searches,
        other_tool_calls=others,
        **session_fields,
    )
