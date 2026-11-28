"""The git port, against a real repository made in `tmp_path`."""

import subprocess
from pathlib import Path

import pytest

from sldb.ports import git


def _git(root: Path, *args: str) -> None:
    subprocess.run(["git", *args], cwd=root, check=True, capture_output=True)


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    _git(tmp_path, "init", "-q", "-b", "main")
    _git(tmp_path, "config", "user.email", "t@example.com")
    _git(tmp_path, "config", "user.name", "t")
    (tmp_path / "a.txt").write_text("uno\n", encoding="utf-8")
    (tmp_path / ".gitignore").write_text("ignored.txt\n", encoding="utf-8")
    _git(tmp_path, "add", "a.txt", ".gitignore")
    _git(tmp_path, "commit", "-q", "-m", "first")
    return tmp_path


def test_run_git_captures_output_and_can_raise(repo):
    assert git.run_git("rev-parse", "--is-inside-work-tree", cwd=repo).stdout.strip() == "true"
    with pytest.raises(subprocess.CalledProcessError):
        git.run_git("show", "no-such-ref", cwd=repo, check=True)


def test_git_output_is_stdout_or_none(repo):
    assert git.git_output(repo, "branch", "--show-current").strip() == "main"
    assert git.git_output(repo, "show", "no-such-ref") is None


def test_git_ok_and_toplevel_outside_a_repo(tmp_path, monkeypatch):
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))
    assert git.git_ok(tmp_path, "rev-parse", "--is-inside-work-tree") is False
    assert git.toplevel(tmp_path) is None


def test_git_ok_and_toplevel_inside_a_repo(repo):
    (repo / "sub").mkdir()
    assert git.git_ok(repo, "rev-parse", "--is-inside-work-tree") is True
    assert git.toplevel(repo / "sub") == repo.resolve()


def test_git_stdout_raises_with_git_stderr_unless_unchecked(repo):
    with pytest.raises(RuntimeError, match="failed in"):
        git.git_stdout(repo, "show", "no-such-ref")
    assert git.git_stdout(repo, "config", "--get", "no.such.key", check=False) == ""
    assert git.git_stdout(repo, "config", "--get", "user.name").strip() == "t"


def test_describe_head_sha_and_dirty_paths(repo):
    assert git.head_sha(repo) == git.git_output(repo, "rev-parse", "HEAD").strip()
    assert git.describe_checkout(repo)
    assert git.dirty_paths(repo) == []
    (repo / "a.txt").write_text("dos\n", encoding="utf-8")
    assert git.dirty_paths(repo) == [" M a.txt"]
    assert git.describe_checkout(repo).endswith("-dirty")


def test_committed_file_reads_head_not_the_disk(repo):
    (repo / "a.txt").write_text("cambiado\n", encoding="utf-8")
    assert git.committed_file(repo / "a.txt") == "uno\n"
    assert git.committed_file(repo / "never.txt") is None


def test_unignored_files_lists_tracked_and_untracked_but_not_ignored(repo):
    (repo / "new.txt").write_text("x", encoding="utf-8")
    (repo / "ignored.txt").write_text("x", encoding="utf-8")
    names = set(filter(None, git.unignored_files(repo).decode().split("\0")))
    assert names == {"a.txt", ".gitignore", "new.txt"}
