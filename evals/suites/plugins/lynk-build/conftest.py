"""Target for every suite under this plugin: the lynk-build plugin, loaded via
plugins=[local]. Add a sibling <skill>/ dir to eval another of its skills."""

import pytest

from harness.subject import Target


@pytest.fixture(scope="session")
def target(repo_dir):
    return Target(mode="plugin", path=repo_dir / "lynk-build")
