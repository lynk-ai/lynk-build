"""Shared, suite-agnostic wiring. Anchors `evals/` on sys.path (pytest prepends
each conftest's dir) so suites can `import harness`.

Targets are declared per group (suites/plugins/<plugin>/conftest.py,
suites/local/conftest.py) via a `target` fixture; these fixtures just provide the
repo root they build on, the code SHA, and the generic `-k` selection capture.
"""

from pathlib import Path

import pytest

from harness import report

REPO_DIR = Path(__file__).resolve().parent.parent      # the repo root (holds .claude/ and the plugin)


@pytest.fixture(scope="session")
def repo_dir():
    return REPO_DIR


@pytest.fixture(scope="session")
def sha():
    # git HEAD of the repo — the code-under-test version, whether plugin or repo skill.
    return report.plugin_sha(REPO_DIR)


@pytest.hookimpl(trylast=True)
def pytest_collection_modifyitems(config, items):
    """Record which case ids survived selection (-k / -m / ids) so each suite's
    batch runs ONLY those — a targeted `-k q04` costs one case, not the whole suite.
    trylast so we see `items` AFTER pytest's own -k deselection."""
    selected = set()
    for it in items:
        cs = getattr(it, "callspec", None)
        if cs and "case" in cs.params:
            selected.add(cs.params["case"]["id"])
    config._selected_cases = selected
