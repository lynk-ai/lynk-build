"""Shared eval harness. `load_evaluator` lets a suite load its own
`evaluators/<name>.py` by file path under a unique module name — needed because
pytest runs in importlib mode (no suite dir on sys.path) and suite dirs may have
hyphens (can't be packages), so `from evaluators import x` isn't available."""

import importlib.util
from pathlib import Path


def load_evaluator(caller_file, name):
    """Load <dir of caller_file>/evaluators/<name>.py as a uniquely-named module."""
    suite = Path(caller_file).resolve().parent
    path = suite / "evaluators" / f"{name}.py"
    mod_name = f"evaluator_{suite.name}_{name}".replace("-", "_")
    spec = importlib.util.spec_from_file_location(mod_name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod
