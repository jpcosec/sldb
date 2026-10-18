"""`stores check` notes ignore rules that break the store's split: `.sldb/core` versionable,
`.sldb/runtime` ignored. deskops guarded it with a test of its own (inbox 20260904)."""

from __future__ import annotations

import subprocess

from sldb.api import check_store, init_store
from sldb.cli import main


def _repo(tmp_path, gitignore: str | None):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    if gitignore is not None:
        (tmp_path / ".gitignore").write_text(gitignore, encoding="utf-8")
    return init_store(tmp_path).store_path


def test_a_repo_that_ignores_runtime_and_keeps_core_is_fine(tmp_path, capsys):
    sp = _repo(tmp_path, ".sldb/runtime/\n")
    assert check_store(sp, tmp_path)["gitignore_policy"] == {"core_ignored": False, "runtime_ignored": True, "ok": True}
    main(["stores", "check", "--store", str(sp)])
    assert "ignore rules" not in capsys.readouterr().out


def test_runtime_not_ignored_and_core_ignored_are_noted(tmp_path, capsys):
    sp = _repo(tmp_path, ".sldb/\n")
    assert check_store(sp, tmp_path)["gitignore_policy"]["ok"] is False
    main(["stores", "check", "--store", str(sp)])
    assert "`.sldb/core` is ignored" in capsys.readouterr().out


def test_outside_git_there_is_no_policy(tmp_path):
    sp = init_store(tmp_path).store_path
    assert check_store(sp, tmp_path)["gitignore_policy"] is None
