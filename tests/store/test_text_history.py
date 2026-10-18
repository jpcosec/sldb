"""`stores check` tells an index that fell behind from one that matches no version of the file,
through the file's git history (inbox 20260924-010929)."""

from __future__ import annotations

import subprocess

from sldb.store.diagnostics_models.text_history import text_history
from sldb.store.hashing import hash_text


def _git(root, *argv):
    subprocess.run(["git", *argv], cwd=root, check=True, capture_output=True)


def _repo(tmp_path):
    _git(tmp_path, "init", "-q")
    _git(tmp_path, "config", "user.email", "t@t")
    _git(tmp_path, "config", "user.name", "t")
    (tmp_path / "d.md").write_text("# one\n", encoding="utf-8")
    _git(tmp_path, "add", "d.md")
    _git(tmp_path, "commit", "-qm", "one")
    (tmp_path / "d.md").write_text("# two\n", encoding="utf-8")
    _git(tmp_path, "commit", "-qam", "two")
    return tmp_path


def test_an_earlier_committed_version_is_stale(tmp_path):
    root = _repo(tmp_path)
    found = text_history(root, "d.md", hash_text("# one\n"), exists=True)
    assert found["verdict"] == "stale" and len(found["commit"]) == 10


def test_a_text_no_commit_has_is_unmatched(tmp_path):
    root = _repo(tmp_path)
    assert text_history(root, "d.md", hash_text("# never written\n"), exists=True)["verdict"] == "unmatched"


def test_a_file_gone_is_orphan_and_outside_git_undetermined(tmp_path):
    root = _repo(tmp_path / "repo") if (tmp_path / "repo").mkdir() is None else None
    assert text_history(root, "d.md", None, exists=False)["verdict"] == "orphan"
    outside = tmp_path / "plain"
    outside.mkdir()
    assert text_history(outside, "d.md", None, exists=True)["verdict"] in ("undetermined", "unmatched")
