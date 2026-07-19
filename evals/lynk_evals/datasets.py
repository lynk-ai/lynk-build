from pathlib import Path

import yaml
from pydantic_evals import Case

from .config import DATASETS_DIR, PLUGIN_ROOT
from .schema import CaseInputs, CaseMetadata


def load_cases(files: list[Path] | None = None) -> list[Case]:
    files = files or sorted(DATASETS_DIR.glob("*.yaml"))
    cases: list[Case] = []
    seen: set[str] = set()
    for f in files:
        data = yaml.safe_load(f.read_text()) or {}
        for raw in data.get("cases", []):
            name = raw["name"]
            if name in seen:
                raise ValueError(f"{f}: duplicate case name {name!r}")
            seen.add(name)
            metadata = CaseMetadata(**raw["metadata"])
            _validate_paths(f, name, metadata)
            cases.append(Case(name=name, inputs=CaseInputs(**raw["inputs"]), metadata=metadata))
    return cases


def _validate_paths(source: Path, name: str, md: CaseMetadata) -> None:
    all_paths = (
        md.expected_docs.required
        + md.expected_docs.optional
        + md.expected_books.required
        + md.expected_books.optional
    )
    for p in all_paths:
        if not (PLUGIN_ROOT / p).is_file():
            raise ValueError(
                f"{source}: case {name!r}: expected path not found under lynk-wiki/: {p}"
            )


def filter_cases(
    cases: list[Case],
    tag: str | None = None,
    perspective: str | None = None,
    case: str | None = None,
) -> list[Case]:
    out = cases
    if tag:
        out = [c for c in out if tag in c.metadata.tags]
    if perspective:
        out = [c for c in out if c.metadata.perspective == perspective]
    if case:
        out = [c for c in out if c.name == case]
    return out
