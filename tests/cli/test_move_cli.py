"""`sldb move SOURCE DESTINATION [--store S] [--dry-run] [--format text|json]`."""

from __future__ import annotations

import json
import sys

import pytest

from sldb.cli import main
from tests.cli.move_repo import MODULE, build_repo, commit_all, field, git, snapshot, track, write


@pytest.fixture
def repo(tmp_path):
    root, py = build_repo(tmp_path)
    write(root, "src/app.py", "x\n")
    write(root, "README.md", "[app](src/app.py)\n")
    track(root, py, "mat", "mat.md", "src/app.py")
    commit_all(root)
    yield root, py
    sys.modules.pop(MODULE, None)


def _args(root, py, *more):
    return ["move", "src/app.py", "lib/app.py", "--store", str(root / ".sldb"), "--pythonpath", py, *more]


def test_move_moves_with_git_and_fixes_fields_and_links(repo, capsys):
    root, py = repo
    assert main(_args(root, py)) == 0
    out = capsys.readouterr().out
    assert "Moved src/app.py -> lib/app.py" in out
    assert "R  src/app.py -> lib/app.py" in git(root, "status", "--porcelain")
    assert field(root, py, "mat")["target"] == "lib/app.py"
    assert (root / "README.md").read_text() == "[app](lib/app.py)\n"


def test_dry_run_json_lists_the_changes_and_touches_nothing(repo, capsys):
    root, py = repo
    before = snapshot(root)
    assert main(_args(root, py, "--dry-run", "--format", "json")) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["dry_run"] is True
    assert report["moves"] == [{"source": "src/app.py", "destination": "lib/app.py"}]
    assert report["fields"] == [{"document": "FileDoc:mat", "field": "target", "old": "src/app.py", "new": "lib/app.py"}]
    assert report["links"] == [{"file": "README.md", "line": 1, "old": "src/app.py", "new": "lib/app.py"}]
    assert snapshot(root) == before


def test_move_to_an_existing_destination_fails_and_changes_nothing(repo):
    root, py = repo
    before = snapshot(root)
    with pytest.raises(SystemExit):
        main(["move", "src/app.py", "README.md", "--store", str(root / ".sldb"), "--pythonpath", py])
    assert snapshot(root) == before
