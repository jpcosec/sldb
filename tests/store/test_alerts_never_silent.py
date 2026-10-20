"""No alert is silent (docs/architecture/anchoring.md §4): every alert a command reports shows in
its text (`--quiet` too), in its JSON, in the envelope's `warnings` and as a GitHub annotation,
and an alert alone exits 0."""
from __future__ import annotations

import json

import pytest

from sldb.api.stores.store_findings import diagnosis_findings
from sldb.cli import main as cli_main
from sldb.store.diagnostics import diagnose_store
from sldb.api import resolve_model_ref

from .test_diagnostics import _PYTHONPATH, _make_store


@pytest.fixture
def moved(tmp_path, capsys):
    """A store whose document changed under it: a `store/data-mutation` alert, no error."""
    _make_store(tmp_path)
    (tmp_path / "doc.md").write_text("# Different Title\n", encoding="utf-8")
    capsys.readouterr()
    alerts = [f for f in diagnosis_findings(diagnose_store(tmp_path / ".sldb", resolve_model_ref, tmp_path, _PYTHONPATH)) if f.level == "alert"]
    assert alerts
    return tmp_path, alerts


def _check(tmp_path, *extra) -> list[str]:
    return ["stores", "check", "--store", str(tmp_path / ".sldb"), "--pythonpath", _PYTHONPATH, *extra]


@pytest.mark.parametrize("extra", [(), ("--quiet",)])
def test_every_alert_is_a_line_of_the_text(moved, capsys, extra):
    tmp_path, alerts = moved
    assert cli_main(_check(tmp_path, *extra)) == 0
    out = capsys.readouterr().out
    assert all(a.line() in out for a in alerts)


def test_every_alert_is_in_the_json(moved, capsys):
    tmp_path, alerts = moved
    assert cli_main(_check(tmp_path, "--format", "json")) == 0
    assert json.loads(capsys.readouterr().out)["alerts"] == [a.as_dict() for a in alerts]


def test_every_alert_is_in_the_envelopes_warnings(moved, capsys):
    tmp_path, alerts = moved
    assert cli_main(["--envelope", *_check(tmp_path, "--format", "json")]) == 0
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["ok"] is True and envelope["warnings"] == [a.as_dict() for a in alerts]


def test_every_alert_is_a_github_annotation(moved, capsys, monkeypatch):
    tmp_path, alerts = moved
    monkeypatch.setenv("GITHUB_ACTIONS", "true")
    assert cli_main(_check(tmp_path, "--format", "json")) == 0
    err = capsys.readouterr().err
    assert all(f"::warning title={a.code}::" in err for a in alerts)


def test_an_error_still_fails_and_its_alerts_still_show(moved, capsys):
    tmp_path, alerts = moved
    (tmp_path / "doc.md").unlink()
    assert cli_main(["--envelope", *_check(tmp_path, "--format", "json")]) == 1
    envelope = json.loads(capsys.readouterr().out)
    assert envelope["ok"] is False and "store/missing" in [e["code"] for e in envelope["data"]["errors"]]
    assert "warnings" in envelope
