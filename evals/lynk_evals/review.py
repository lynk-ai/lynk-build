"""Human review gate: promote candidates into datasets/. Humans are the only path in."""

import os
import subprocess
import tempfile

import yaml

from .config import CANDIDATES_DIR, DATASETS_DIR
from .datasets import _validate_paths, load_cases
from .schema import CaseMetadata


def review(approve: str | None = None) -> None:
    approve_names = {n.strip() for n in approve.split(",")} if approve else None
    existing_names = {c.name for c in load_cases()}
    promoted = rejected = 0

    for f in sorted(CANDIDATES_DIR.glob("*.yaml")):
        data = yaml.safe_load(f.read_text()) or {}
        remaining = []
        for case in data.get("cases", []):
            action = _decide(case, approve_names)
            if action == "approve":
                _promote(case, existing_names)
                promoted += 1
            elif action == "reject":
                rejected += 1
            else:
                remaining.append(case)

        if remaining:
            data["cases"] = remaining
            f.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=100))
        else:
            f.unlink()

    print(f"\npromoted {promoted}, rejected {rejected}")


def _decide(case: dict, approve_names: set[str] | None) -> str:
    if approve_names is not None:
        return "approve" if case["name"] in approve_names else "skip"
    if case.get("status") != "ready_for_review":
        return "skip"

    _print_case(case)
    while True:
        choice = input("[a]pprove / [r]eject / [s]kip / [e]dit rubric > ").strip().lower()
        if choice == "a":
            return "approve"
        if choice == "r":
            return "reject"
        if choice == "s":
            return "skip"
        if choice == "e":
            case["metadata"]["rubric"] = _edit_text(case["metadata"]["rubric"])
            print("--- updated rubric ---\n" + case["metadata"]["rubric"])


def _print_case(case: dict) -> None:
    md = case["metadata"]
    critic = case.get("critic", {})
    print("\n" + "=" * 72)
    print(f"case: {case['name']}   [{md.get('perspective')}]  tags={md.get('tags')}")
    print(f"\nQ: {case['inputs']['question']}")
    print(f"\nrequired: {md['expected_docs'].get('required')}")
    print(f"optional: {md['expected_docs'].get('optional', [])}")
    print(f"optimal_hops: {md['optimal_hops']}")
    print(f"\nrubric:\n{md['rubric']}")
    if critic:
        print(f"\ncritic: {critic.get('scores')}  verdict={critic.get('verdict')}")
        print(f"notes: {critic.get('notes')}")


def _edit_text(text: str) -> str:
    editor = os.environ.get("EDITOR")
    if editor:
        with tempfile.NamedTemporaryFile("w+", suffix=".md", delete=False) as tf:
            tf.write(text)
            path = tf.name
        subprocess.run([editor, path])
        with open(path) as fh:
            return fh.read()
    print("enter new rubric, end with a single '.' line:")
    lines = []
    while (line := input()) != ".":
        lines.append(line)
    return "\n".join(lines)


def _promote(case: dict, existing_names: set[str]) -> None:
    name = case["name"]
    if name in existing_names:
        raise SystemExit(f"cannot promote {name!r}: name already exists in datasets/")

    metadata = CaseMetadata(**case["metadata"])  # re-validate before it enters the dataset
    _validate_paths(DATASETS_DIR, name, metadata)
    existing_names.add(name)

    target = DATASETS_DIR / f"{metadata.perspective}.yaml"
    entry = {
        "name": name,
        "inputs": case["inputs"],
        "metadata": metadata.model_dump(exclude_defaults=True, mode="json"),
    }
    block = yaml.safe_dump([entry], sort_keys=False, allow_unicode=True, width=100)
    with target.open("a") as fh:
        fh.write("\n" + block)
    print(f"promoted {name} -> {target.name}")
