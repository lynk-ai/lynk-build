#!/usr/bin/env python3
"""Deterministic structure checks for generated books (grader layer 1).

Usage: python3 check.py <library-root> [book-slug]
Checks every book under the root (or just the named one). Exit 0 = all pass.
"""
import json
import re
import sys
from pathlib import Path

SLUG = re.compile(r"^[a-z0-9-]+$")
FM = re.compile(r"^---\n(.*?)\n---\n?(.*)$", re.S)


def parse_fm(text):
    m = FM.match(text)
    if not m:
        return None, None
    try:
        import yaml
        return yaml.safe_load(m.group(1)), m.group(2)
    except Exception:
        return None, m.group(2)


def check_book(book: Path, failures: list):
    def fail(msg):
        failures.append(f"{book.name}: {msg}")

    if not SLUG.match(book.name):
        fail(f"book slug '{book.name}' violates ^[a-z0-9-]+$")

    index = book / "index.md"
    if not index.exists():
        fail("missing index.md")
    else:
        fm, body = parse_fm(index.read_text())
        if fm is None:
            fail("index.md frontmatter missing or unparseable")
        else:
            for key in ("name", "description"):
                if key not in fm:
                    fail(f"index.md missing '{key}'")
        if body and body.strip():
            fail("index.md has a body — index must be frontmatter only")

    chapters = book / "chapters"
    if not chapters.is_dir():
        fail("missing chapters/ dir")
        return
    ch_files = sorted(chapters.glob("*.md"))
    if not ch_files:
        fail("chapters/ is empty")
    for ch in ch_files:
        rel = f"{book.name}/chapters/{ch.name}"
        if not SLUG.match(ch.stem):
            failures.append(f"{rel}: slug violates ^[a-z0-9-]+$")
        fm, body = parse_fm(ch.read_text())
        if fm is None:
            failures.append(f"{rel}: frontmatter missing or unparseable")
            continue
        for key in ("name", "description"):
            if key not in fm:
                failures.append(f"{rel}: missing '{key}'")
        desc = str(fm.get("description", ""))
        if desc and "read when" not in desc.lower():
            failures.append(f"{rel}: description has no 'Read when …' trigger condition")
        if body:
            for line in body.splitlines():
                if line.startswith("# "):
                    failures.append(f"{rel}: H1 in body ('{line[:50]}') — title lives in frontmatter")
                    break
            # cross-book reference heuristic: markdown links that climb out of the book
            if re.search(r"\]\((\.\./|/)?(library/)?[a-z0-9-]+/(index\.md|chapters/)", body):
                failures.append(f"{rel}: possible cross-book reference — books must be self-contained")


def main():
    root = Path(sys.argv[1])
    only = sys.argv[2] if len(sys.argv) > 2 else None
    failures = []
    books = [root / only] if only else [p for p in sorted(root.iterdir()) if p.is_dir()]
    for book in books:
        check_book(book, failures)
    if failures:
        print(f"FAIL ({len(failures)}):")
        for f in failures:
            print(f"  - {f}")
        sys.exit(1)
    print(f"PASS: {len(books)} book(s) clean")


if __name__ == "__main__":
    main()
