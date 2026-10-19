"""`sldb --envelope`: one JSON value per run and typed exit codes, opt-in."""
from __future__ import annotations

import json

import pytest

from sldb.api.stores.store_skeleton import write_empty_store
from sldb.cli import main as cli_main
from sldb.cli.error_types import error_type
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBModelError, SLDBStoreError


@pytest.fixture
def store(tmp_path):
    write_empty_store(tmp_path / ".sldb")
    return tmp_path / ".sldb"


def _run(capsys, *argv) -> tuple[int, dict]:
    code = cli_main(["--envelope", *argv])
    return code, json.loads(capsys.readouterr().out)


def test_a_successful_run_carries_the_commands_json_as_data(store, capsys):
    code, envelope = _run(capsys, "stores", "list", "--store", str(store), "--format", "json")
    assert code == 0 and envelope["ok"] is True
    assert envelope["command"] == "stores list" and envelope["store"] == {"path": str(store)}
    assert envelope["data"]["stores"] == [] and envelope["warnings"] == []
    assert envelope["revision"]


def test_an_unknown_document_is_a_typed_missing_error(store, capsys):
    code, envelope = _run(capsys, "docs", "show", "nope", "--store", str(store))
    assert code == 1 and envelope["ok"] is False and envelope["exit"] == 1
    assert envelope["error"]["type"] == "docs/missing"


def test_bad_usage_is_cli_usage_with_exit_6(capsys):
    code, envelope = _run(capsys, "stores", "bogus")
    assert code == 6 and envelope["error"]["type"] == "cli/usage"
    assert "invalid choice" in envelope["error"]["message"]


def test_without_the_flag_the_output_and_exit_are_what_callers_parse_today(store, capsys):
    assert cli_main(["stores", "list", "--store", str(store), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["stores"] == []


@pytest.mark.parametrize("exc, expected", [
    (SLDBDocumentTargetError("Ambiguous document target: x"), ("docs/ambiguous", 2)),
    (SLDBStoreError("Store at s is busy. Use --wait to block."), ("store/busy", 4)),
    (SLDBStoreError("No store"), ("store/error", 5)),
    (SLDBModelError("Model 'X' exists."), ("models/rejected", 3)),
    (FileNotFoundError("gone"), ("io/missing", 1)),
    (RuntimeError("boom"), ("cli/unexpected", 70)),
])
def test_each_error_maps_to_one_type_and_exit(exc, expected):
    assert error_type(exc) == expected
