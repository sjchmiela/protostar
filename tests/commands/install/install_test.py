from git.repo import Repo
import pytest
from src.commands.install import install, installation_exceptions


@pytest.fixture(name="repo_url")
def fixture_repo_url():
    return "https://github.com/starkware-libs/cairo-lang"


def test_invalid_local_repository_error(tmpdir: str, repo_url: str):
    with pytest.raises(installation_exceptions.InvalidLocalRepository):
        install(repo_url, tmpdir)


def test_incorrect_url_error(tmpdir: str):
    Repo.init(tmpdir)

    with pytest.raises(installation_exceptions.IncorrectURL):
        install("https://www.google.com/", tmpdir)


def test_basic_case(tmpdir: str, repo_url: str):
    Repo.init(tmpdir)

    assert install(repo_url, tmpdir) is None
