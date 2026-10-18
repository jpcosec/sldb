"""Import bindings keep their condition, and a later same-scope binding shadows them (spec 4.1)."""

from __future__ import annotations

from pathlib import Path

from sldb.selfdoc.python_source_graph import source_snapshot
from sldb.selfdoc.python_source_scan import scan_source_facts

SOURCE = '''from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from other import Typed
try:
    import fast as engine
except ImportError:
    engine = None
from other import Shadowed


def Shadowed():
    pass


class Holder:
    value: Typed
    later: Shadowed
'''


def _graph(tmp_path: Path) -> dict:
    (tmp_path / "other.py").write_text("class Typed:\n    pass\n\n\nclass Shadowed:\n    pass\n", encoding="utf-8")
    (tmp_path / "m.py").write_text(SOURCE, encoding="utf-8")
    return {n["identity"]["node_id"]: n for n in source_snapshot(scan_source_facts(tmp_path, None), "demo")["nodes"]}


def test_each_import_keeps_the_condition_it_lives_under(tmp_path):
    imports = {e["metadata"]["local"]: e["metadata"] for e in _graph(tmp_path)["python:m"]["edges"] if e["relation_type"] == "imports"}
    assert imports["Typed"]["context"] == ["type_checking"]
    assert imports["engine"]["context"] == ["try"]
    assert "context" not in imports["TYPE_CHECKING"]


def test_a_later_definition_shadows_the_import_for_what_comes_after(tmp_path):
    nodes = _graph(tmp_path)
    imports = {e["metadata"]["local"]: e["metadata"] for e in nodes["python:m"]["edges"] if e["relation_type"] == "imports"}
    assert imports["Shadowed"]["shadowed_at"] == 12
    refs = {e["metadata"]["site"]: e["target_id"] for e in nodes["python:m:Holder"]["edges"] if e["relation_type"] == "references"}
    assert refs["value"] == "python:other:Typed"
    assert "later" not in refs  # `Shadowed` there is the local function, not the import


def test_check_reports_undeclared_unexplained_and_unresolved_apart(tmp_path):
    from sldb.selfdoc.python_source_scan import docstring_survey

    (tmp_path / "m.py").write_text('"""---\nid: m\n---\n"""\n\n\nclass A:\n    """Plain."""\n    x: Missing\n', encoding="utf-8")
    survey = docstring_survey(tmp_path)
    assert survey == {"undeclared": ["m.py:7"], "unexplained": ["m.py:1"]}
    metadata = source_snapshot(scan_source_facts(tmp_path, None), "demo")["metadata"]
    assert metadata["unresolved_references"] == ["m.py:9: Missing"]
