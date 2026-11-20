"""`sldb.api.move_path`: a file or directory moves with git, the store's fields and the repo's
Markdown links that name it follow, and a failure puts everything back."""

from __future__ import annotations

import sys

import pytest

from sldb import api
from sldb.cli import main
from sldb.core.exceptions import SLDBStoreError
from tests.cli.move_repo import MODULE, build_repo, commit_all, field, git, snapshot, track, write


@pytest.fixture
def repo(tmp_path):
    root, py = build_repo(tmp_path)
    yield root, py
    sys.modules.pop(MODULE, None)


def _status(root):
    return git(root, "status", "--porcelain").splitlines()


def test_moving_a_tracked_document_is_a_git_rename_and_keeps_it_tracked(repo):
    root, py = repo
    track(root, py, "login", "login.md", "x")
    commit_all(root)
    report = api.move_path(root / ".sldb", "login.md", "docs/login.md", pythonpath=py)
    assert report.moves == [{"source": "login.md", "destination": "docs/login.md"}]
    assert any(line.startswith("R") and "login.md -> docs/login.md" in line for line in _status(root))
    assert api.doc_status(root / ".sldb", "login").path == "docs/login.md"
    assert main(["stores", "check", "--store", str(root / ".sldb")]) == 0


def test_a_field_naming_the_moved_file_takes_the_new_path(repo):
    root, py = repo
    write(root, "src/app.py", "print(1)\n")
    track(root, py, "mat", "mat.md", "src/app.py", ["src/app.py", "src/other.py"])
    commit_all(root)
    report = api.move_path(root / ".sldb", "src/app.py", "src/core/app.py", pythonpath=py)
    assert field(root, py, "mat")["target"] == "src/core/app.py"
    assert field(root, py, "mat")["files"] == ["src/core/app.py", "src/other.py"]
    assert {(c["field"], c["old"], c["new"]) for c in report.fields} == {("target", "src/app.py", "src/core/app.py"), ("files.0", "src/app.py", "src/core/app.py")}
    assert (root / "src/core/app.py").exists() and not (root / "src/app.py").exists()


def test_moving_a_directory_rewrites_prefixes_but_not_lookalike_siblings(repo):
    root, py = repo
    write(root, "pkg/a.py", "a\n")
    write(root, "pkgzero/a.py", "z\n")
    track(root, py, "mat", "mat.md", "pkg", ["pkg/a.py", "pkgzero/a.py", "pkg2"])
    track(root, py, "inside", "pkg/inside.md", "pkg/a.py")
    commit_all(root)
    api.move_path(root / ".sldb", "pkg", "lib", pythonpath=py)
    assert field(root, py, "mat") == {"title": "mat", "target": "lib", "files": ["lib/a.py", "pkgzero/a.py", "pkg2"]}
    assert field(root, py, "inside")["target"] == "lib/a.py"
    assert api.doc_status(root / ".sldb", "inside").path == "lib/inside.md"
    assert not (root / "pkg").exists() and (root / "pkgzero/a.py").exists()
    assert main(["stores", "check", "--store", str(root / ".sldb")]) == 0


def test_relative_markdown_links_to_the_old_path_point_at_the_new_one(repo):
    root, py = repo
    write(root, "src/app.py", "x\n")
    write(root, "README.md", "See [app](src/app.py) and [also](./src/app.py#L3).\n\n```\n[no](src/app.py)\n```\n[web](https://e.com/src/app.py) [other](src/apps.py)\n")
    write(root, "docs/guide.md", "[app](../src/app.py)\n")
    commit_all(root)
    report = api.move_path(root / ".sldb", "src/app.py", "lib/app.py", pythonpath=py)
    assert (root / "README.md").read_text() == "See [app](lib/app.py) and [also](./lib/app.py#L3).\n\n```\n[no](src/app.py)\n```\n[web](https://e.com/src/app.py) [other](src/apps.py)\n"
    assert (root / "docs/guide.md").read_text() == "[app](../lib/app.py)\n"
    assert [(c["file"], c["line"]) for c in report.links] == [("README.md", 1), ("README.md", 1), ("docs/guide.md", 1)]


def test_dry_run_changes_nothing_and_lists_what_the_real_run_does(repo):
    root, py = repo
    write(root, "src/app.py", "x\n")
    write(root, "README.md", "[app](src/app.py)\n")
    track(root, py, "mat", "mat.md", "src/app.py")
    commit_all(root)
    before, status = snapshot(root), _status(root)
    planned = api.move_path(root / ".sldb", "src/app.py", "lib/app.py", dry_run=True, pythonpath=py)
    assert snapshot(root) == before and _status(root) == status
    done = api.move_path(root / ".sldb", "src/app.py", "lib/app.py", pythonpath=py)
    assert planned.dry_run and not done.dry_run
    assert planned.model_dump(exclude={"dry_run"}) == done.model_dump(exclude={"dry_run"})
    assert planned.fields and planned.links and planned.moves


@pytest.mark.parametrize("destination", ["README.md", "../outside.md", "src/app.py/inner.py"])
def test_a_taken_or_outside_destination_is_refused_and_nothing_changes(repo, destination):
    root, py = repo
    write(root, "src/app.py", "x\n")
    write(root, "README.md", "[app](src/app.py)\n")
    track(root, py, "mat", "mat.md", "src/app.py")
    commit_all(root)
    before, status = snapshot(root), _status(root)
    with pytest.raises(SLDBStoreError):
        api.move_path(root / ".sldb", "src/app.py", destination, pythonpath=py)
    assert snapshot(root) == before and _status(root) == status


def test_a_failure_halfway_restores_the_tree_the_index_and_the_store(repo, monkeypatch):
    root, py = repo
    write(root, "pkg/plain.txt", "p\n")
    write(root, "README.md", "[d](pkg/a.md)\n")
    track(root, py, "a", "pkg/a.md", "pkg/plain.txt")
    track(root, py, "b", "pkg/b.md", "pkg")
    commit_all(root)
    before, status = snapshot(root), _status(root)
    from sldb.api.documents import move_document as module
    real, calls = module.relocate_file, []

    def flaky(source, target):
        calls.append(source)
        if len(calls) == 2:
            raise RuntimeError("disk gone")
        real(source, target)

    monkeypatch.setattr(module, "relocate_file", flaky)
    with pytest.raises(RuntimeError):
        api.move_path(root / ".sldb", "pkg", "lib", pythonpath=py)
    assert len(calls) == 2
    assert {k: v for k, v in snapshot(root).items() if not k.startswith(".sldb")} == {k: v for k, v in before.items() if not k.startswith(".sldb")}
    assert snapshot(root) == before and _status(root) == status
    assert api.doc_status(root / ".sldb", "a").path == "pkg/a.md"
    assert main(["stores", "check", "--store", str(root / ".sldb")]) == 0
