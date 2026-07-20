"""Target for every suite here: the repo's own root `.claude/` skills, loaded by
running the subject in the repo (setting_sources=['project']). Add a sibling
<skill>/ dir to eval another repo-local skill."""

import pytest

from harness.subject import Target


@pytest.fixture(scope="session")
def target(repo_dir):
    return Target(mode="project", path=repo_dir)
