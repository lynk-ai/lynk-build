"""Generic dataset loader, shared across skill suites.

A case is a plain dict with at least `id` and `question`; every other field is
skill-specific and interpreted by that skill's evaluators. Loading validates the
key itself — unique, present ids and a non-empty question — so a typo in the
answer key fails loudly at collection, not silently mid-run.
"""

from pathlib import Path

import yaml


def load_cases(dataset_path):
    raw = yaml.safe_load(Path(dataset_path).read_text())
    cases = raw.get("cases") if isinstance(raw, dict) else raw
    if not cases:
        raise ValueError(f"{dataset_path}: no `cases` found")
    seen = set()
    for c in cases:
        cid = c.get("id")
        if not cid:
            raise ValueError(f"{dataset_path}: a case is missing `id`")
        if not c.get("question"):
            raise ValueError(f"{cid}: missing `question`")
        if cid in seen:
            raise ValueError(f"duplicate case id {cid!r} in {dataset_path}")
        seen.add(cid)
    return cases
