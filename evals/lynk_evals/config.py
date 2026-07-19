from pathlib import Path

import yaml
from pydantic import BaseModel

EVALS_ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = EVALS_ROOT.parent
PLUGIN_ROOT = REPO_ROOT / "lynk-wiki"
DATASETS_DIR = EVALS_ROOT / "datasets"
CANDIDATES_DIR = EVALS_ROOT / "candidates"
RUNS_DIR = EVALS_ROOT / "runs"


class Config(BaseModel):
    agent_model: str = "claude-sonnet-5"
    judge_model: str = "claude-opus-4-8"
    system_prompt: str = "claude_code"
    per_case_timeout_s: float = 240
    max_concurrency: int = 3
    max_turns: int = 30
    # The library pipeline (nested librarian + book-reader scouts + bk) burns far
    # more turns and wall-clock than a docs case; budget it separately.
    library_timeout_s: float = 480
    library_max_turns: int = 60


def load_config(path: Path | None = None, **overrides) -> Config:
    p = path or EVALS_ROOT / "config.yaml"
    data = yaml.safe_load(p.read_text()) if p.exists() else {}
    data.update({k: v for k, v in overrides.items() if v is not None})
    return Config(**data)
