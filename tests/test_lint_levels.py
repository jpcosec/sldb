"""`sldb lint`: a path that no longer exists is the alert `lint/lost`; a malformed one an error."""
from __future__ import annotations

import json

from sldb.cli import main as cli_main


def _lint(tmp_path, capsys, text: str, *extra) -> tuple[int, str]:
    (tmp_path / "docs").mkdir(exist_ok=True)
    (tmp_path / "docs" / "here.md").write_text("x\n", encoding="utf-8")
    note = tmp_path / "note.md"
    note.write_text(text, encoding="utf-8")
    code = cli_main(["lint", str(note), "--repo-root", str(tmp_path), *extra])
    return code, capsys.readouterr().out


def test_a_cited_path_that_is_gone_is_an_alert_with_exit_0(tmp_path, capsys):
    code, out = _lint(tmp_path, capsys, "see docs/gone.md and docs/here.md\n")
    assert code == 0
    assert "alert: [lint/lost]" in out and "docs/gone.md" in out


def test_a_malformed_path_is_still_an_error(tmp_path, capsys):
    code, out = _lint(tmp_path, capsys, "see ../outside/x.md\n")
    assert code == 1 and "error: [lint/path]" in out


def test_json_carries_the_level_of_every_entry(tmp_path, capsys):
    code, out = _lint(tmp_path, capsys, "docs/gone.md\n", "--format", "json")
    assert code == 0
    assert [(r["level"], r["code"]) for r in json.loads(out)] == [("alert", "lint/lost")]
