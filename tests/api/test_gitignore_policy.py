"""The store's split in git: `.sldb/` versioned whole, `.sldb_cache/` ignored (owner, 2026-10-29).

`stores init` writes the `.sldb_cache/` line in the root `.gitignore` and never touches another
line; `stores check` errors (`stores/core_ignored`, exit 1) when git ignores `.sldb/core/` or
`.sldb/store.yaml`, and alerts (`stores/cache_not_ignored`, exit 0) when the cache is not ignored.
deskops guarded the older split with a test of its own (inbox 20260904).
"""

from __future__ import annotations

import json
import subprocess

from sldb.api import check_store, init_store
from sldb.api.stores.gitignore_lines import ensure_cache_ignored
from sldb.cli import main


def _repo(tmp_path, gitignore: str | None):
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    if gitignore is not None:
        (tmp_path / ".gitignore").write_text(gitignore, encoding="utf-8")
    return init_store(tmp_path).store_path


def _check(sp, capsys) -> tuple[int, dict]:
    code = main(["stores", "check", "--store", str(sp), "--format", "json"])
    return code, json.loads(capsys.readouterr().out)


def test_init_writes_the_cache_line_and_keeps_every_other_line(tmp_path):
    _repo(tmp_path, "# mine\n.venv/\n")
    assert (tmp_path / ".gitignore").read_text(encoding="utf-8") == "# mine\n.venv/\n.sldb_cache/\n"


def test_init_creates_the_gitignore_when_there_is_none(tmp_path):
    _repo(tmp_path, None)
    assert (tmp_path / ".gitignore").read_text(encoding="utf-8") == ".sldb_cache/\n"


def test_the_cache_line_is_added_once(tmp_path):
    _repo(tmp_path, ".sldb_cache\n")
    assert ensure_cache_ignored(tmp_path / ".gitignore") is False
    assert main(["stores", "init", "--path", str(tmp_path), "--force"]) == 0
    assert (tmp_path / ".gitignore").read_text(encoding="utf-8") == ".sldb_cache\n"


def test_a_repo_that_ignores_the_cache_and_versions_the_store_is_fine(tmp_path, capsys):
    sp = _repo(tmp_path, None)
    assert check_store(sp, tmp_path)["gitignore_policy"] == {"core_ignored": False, "declaration_ignored": False, "cache_ignored": True, "ok": True}
    code, payload = _check(sp, capsys)
    assert code == 0 and payload["errors"] == [] and payload["alerts"] == []


def test_core_ignored_is_an_error(tmp_path, capsys):
    sp = _repo(tmp_path, ".sldb/core/\n")
    assert check_store(sp, tmp_path)["gitignore_policy"]["core_ignored"] is True
    code, payload = _check(sp, capsys)
    assert code == 1
    assert [e["code"] for e in payload["errors"]] == ["stores/core_ignored"]
    assert "`.sldb/core/`" in payload["errors"][0]["what"] and "migrate-layout" in payload["errors"][0]["fix"]


def test_the_whole_store_ignored_names_the_declaration_too(tmp_path, capsys):
    sp = _repo(tmp_path, ".sldb/\n")
    (sp / "store.yaml").write_text("version: 1\n", encoding="utf-8")
    code, payload = _check(sp, capsys)
    assert code == 1
    assert "`.sldb/store.yaml`" in payload["errors"][0]["what"]


def test_the_cache_not_ignored_is_an_alert(tmp_path, capsys):
    sp = _repo(tmp_path, None)
    (tmp_path / ".gitignore").write_text("# nothing here\n", encoding="utf-8")
    code, payload = _check(sp, capsys)
    assert code == 0 and payload["errors"] == []
    assert [a["code"] for a in payload["alerts"]] == ["stores/cache_not_ignored"]
    main(["stores", "check", "--store", str(sp)])
    assert "alert: [stores/cache_not_ignored] .gitignore" in capsys.readouterr().out


def test_any_rule_that_covers_the_cache_counts(tmp_path, capsys):
    sp = _repo(tmp_path, ".sldb_cache\n")
    code, payload = _check(sp, capsys)
    assert code == 0 and payload["alerts"] == []


def test_outside_git_there_is_no_policy(tmp_path, capsys):
    sp = init_store(tmp_path).store_path
    assert check_store(sp, tmp_path)["gitignore_policy"] is None
    code, payload = _check(sp, capsys)
    assert code == 0 and payload["errors"] == [] and payload["alerts"] == []
