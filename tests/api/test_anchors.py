"""The anchoring rules, executable (docs/architecture/code-anchoring.md §9): one test per rule of
anchoring.md §3, the error-versus-alert split, and no alert ever silent."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

import sldb.api as api
from sldb.api.anchors import check_anchors, record_anchor
from sldb.api.anchors.anchor_docs import write_anchor
from sldb.cli import main as cli_main
from sldb.models.anchor_state import AnchorState
from sldb.code.runtime import available

pytestmark = pytest.mark.skipif(not available(), reason="tree-sitter runtime not installed (extra [code])")

CODE = 'class K:\n    """K doc."""\n\n    def m(self, x: int = 1) -> int:\n        """M doc."""\n        y = x + 1\n        return y\n\n\ndef free(a):\n    """Free doc."""\n    return a\n'
REF = "code:src/x.py::K.m"


@pytest.fixture
def world(tmp_path):
    root = tmp_path / "repo"
    (root / "src").mkdir(parents=True)
    (root / "src" / "x.py").write_text(CODE, encoding="utf-8")
    store = api.init_store(root).store_path
    api.add_model(store, "sldb.models.code_anchor_doc:CodeAnchorDoc")
    write_anchor(store, None, root / "anchors" / "m.md", record_anchor(root, REF), "m adds one")
    yield root, store
    for name in [m for m in sys.modules if m.startswith("tmpdocs")]:
        del sys.modules[name]


def _edit(root: Path, old: str, new: str) -> None:
    path = root / "src" / "x.py"
    path.write_text(path.read_text(encoding="utf-8").replace(old, new), encoding="utf-8")


def _state(store) -> tuple[AnchorState, list[str]]:
    [report] = check_anchors(store)
    return report.state, report.changed


def test_rule_1_docstring_and_body_are_distinct_nodes_and_formatting_is_not_a_mutation(world):
    root, store = world
    assert _state(store) == (AnchorState.INTACT, [])
    _edit(root, "M doc.", "Other doc.")
    assert _state(store) == (AnchorState.CHANGED, ["docstring"])
    _edit(root, "return y", "return y + 1")
    assert _state(store) == (AnchorState.CHANGED, ["docstring", "body"])
    _edit(root, "Other doc.", "M doc.")
    assert _state(store) == (AnchorState.CHANGED, ["body"])
    _edit(root, "return y + 1", "return y")
    _edit(root, "y = x + 1\n", "y   =   x+1\n\n")
    assert _state(store) == (AnchorState.INTACT, [])


def test_rule_2_changed_is_an_alert_with_exit_0_visible_in_text_json_and_envelope(world, capsys):
    root, store = world
    _edit(root, "return y", "return y + 1")
    assert cli_main(["anchors", "check", "--store", str(store)]) == 0
    out = capsys.readouterr().out
    assert "1 changed" in out and "alert: [anchors/changed] CodeAnchorDoc:m: changed(body)" in out
    assert cli_main(["anchors", "check", "--store", str(store), "--format", "json"]) == 0
    report = json.loads(capsys.readouterr().out)
    assert report["anchors"][0]["state"] == "changed" and [a["code"] for a in report["alerts"]] == ["anchors/changed"] and report["errors"] == []
    assert cli_main(["--envelope", "anchors", "check", "--store", str(store), "--format", "json"]) == 0
    assert [w["code"] for w in json.loads(capsys.readouterr().out)["warnings"]] == ["anchors/changed"]


def test_rule_3_a_rename_reconnects_and_only_record_writes_it(world):
    root, store = world
    _edit(root, "def m(", "def renamed(")
    [report] = check_anchors(store)
    assert (report.state, report.to) == (AnchorState.RECONNECTED, "code:src/x.py::K.renamed")
    assert (root / "anchors" / "m.md").read_text(encoding="utf-8").count("K.renamed") == 0, "check reads only"
    [report] = check_anchors(store, record=True)
    assert report.state is AnchorState.RECONNECTED
    text = (root / "anchors" / "m.md").read_text(encoding="utf-8")
    assert "ref: code:src/x.py::K.renamed" in text and "event: reconnected" in text and "from: code:src/x.py::K.m" in text
    assert _state(store) == (AnchorState.INTACT, [])


def test_rule_3_deleted_or_ambiguous_is_lost_and_lists_the_candidates(world):
    root, store = world
    _edit(root, "def m(", "def m1(")
    _edit(root, "def free(a):\n    \"\"\"Free doc.\"\"\"\n    return a\n", "def free(a):\n    \"\"\"Free doc.\"\"\"\n    return a\n\n\nclass J:\n    def m2(self, x: int = 1) -> int:\n        \"\"\"M doc.\"\"\"\n        y = x + 1\n        return y\n")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and sorted(report.candidates) == ["code:src/x.py::J.m2", "code:src/x.py::K.m1"]
    (root / "src" / "x.py").write_text("def other():\n    return 0\n", encoding="utf-8")
    [report] = check_anchors(store)
    assert report.state is AnchorState.LOST and report.candidates == []


def test_errors_fail_the_command_and_alerts_do_not(world, capsys):
    root, store = world
    (root / "src" / "x.py").write_text("def broken(:\n", encoding="utf-8")
    assert cli_main(["anchors", "check", "--store", str(store)]) == 1
    assert "error: [anchors/unparseable]" in capsys.readouterr().out
    (root / "src" / "x.py").write_text(CODE, encoding="utf-8")
    api.save_document_payload(store, "CodeAnchorDoc", "m", {**record_anchor(root, REF), "ref": "nonsense", "claim": "x"})
    [report] = check_anchors(store)
    assert report.state is AnchorState.INVALID


def test_record_refuses_what_it_cannot_see(world):
    root, _store = world
    with pytest.raises(ValueError, match="invalid code reference"):
        record_anchor(root, "src/x.py::K")
    with pytest.raises(ValueError, match="no symbol"):
        record_anchor(root, "code:src/x.py::K.nope")
    assert record_anchor(root, "code:src/x.py::")["kind"] == "module"


def test_the_cli_records_and_writes_a_signed_theorem(world, capsys):
    root, store = world
    assert cli_main(["anchors", "record", "code:src/x.py::free", "--write", "anchors/free.md", "--claim", "free returns its argument", "--store", str(store)]) == 0
    text = (root / "anchors" / "free.md").read_text(encoding="utf-8")
    assert "authority: theorem" in text and "ref: code:src/x.py::free" in text and "free returns its argument" in text
    assert cli_main(["anchors", "check", "--store", str(store)]) == 0
    assert "2 checked" in capsys.readouterr().out
