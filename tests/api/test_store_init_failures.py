"""`stores init` fails cleanly: nothing left behind, an actionable message, and an exit code that
tells deskops what happened (inbox 20260614-000000).

0: created, or already there. 2: the place refused it (permissions). 1: failed half-way.
"""

from __future__ import annotations

import os

import pytest

from sldb.api.stores import init_store as init_module
from sldb.cli import main


def test_twice_in_the_same_place_is_zero_both_times(tmp_path, capsys):
    assert main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert "already exists" in capsys.readouterr().out


@pytest.mark.skipif(os.geteuid() == 0, reason="root writes through read-only permissions")
def test_a_read_only_parent_is_a_precondition_error_and_leaves_nothing(tmp_path, capsys):
    tmp_path.chmod(0o555)
    try:
        assert main(["stores", "init", "--path", str(tmp_path)]) == 2
    finally:
        tmp_path.chmod(0o755)
    assert "is writable" in capsys.readouterr().err
    assert not (tmp_path / ".sldb").exists()


def test_a_failure_half_way_removes_the_partial_store(tmp_path, monkeypatch, capsys):
    def half_way(store_path):
        (store_path / "core").mkdir(parents=True)
        raise OSError(5, "Input/output error")

    monkeypatch.setattr(init_module, "write_empty_store", half_way)
    assert main(["stores", "init", "--path", str(tmp_path)]) == 1
    assert not (tmp_path / ".sldb").exists()
