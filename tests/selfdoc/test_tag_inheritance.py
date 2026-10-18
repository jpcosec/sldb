"""Effective tags follow the lexical chain package -> module -> declaration (spec section 3)."""

from __future__ import annotations

from pathlib import Path

from sldb.selfdoc.docstring_metadata import parse_docstring
from sldb.selfdoc.python_source_graph import source_snapshot
from sldb.selfdoc.python_source_scan import scan_source_facts

REPO_SRC = Path(__file__).resolve().parents[2] / "src"


def _effective(root: Path) -> dict[str, list[tuple[str, str]]]:
    nodes = source_snapshot(scan_source_facts(root, None), "demo")["nodes"]
    return {n["identity"]["node_id"]: [(t["tag"], t["origin"]) for t in n["semantics"].get("effective_tags", [])] for n in nodes if n["identity"]["node_type"] != "python_external"}


def _meta(id_: str, tags: str) -> str:
    return f'"""---\nid: {id_}\ntags: [{tags}]\n---\nText."""\n'


def test_the_pilot_fixture_of_the_spec():
    found = _effective(REPO_SRC)
    module, cls = "sldb.selfdoc.python_symbol", "sldb.selfdoc.python_symbol.PythonSymbol"
    assert found[module] == [("system:sldb", module), ("workspace:knowledge", module), ("topic:selfdoc", module)]
    assert found[cls] == [("system:sldb", module), ("workspace:knowledge", module), ("topic:selfdoc", module), ("type:code.symbol", cls)]


def test_nearest_wins_topics_unite_and_other_tags_stay_local(tmp_path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "__init__.py").write_text(_meta("pkg", "system:a, workspace:w, topic:t1, type:package"), encoding="utf-8")
    (pkg / "m.py").write_text(_meta("pkg.m", "system:b, topic:t2") + "\n\nclass C:\n    " + _meta("pkg.m.C", "topic:t3").replace("\n", "\n    ") + "\n", encoding="utf-8")
    found = _effective(tmp_path)
    assert found["pkg.m"] == [("workspace:w", "pkg"), ("topic:t1", "pkg"), ("system:b", "pkg.m"), ("topic:t2", "pkg.m")]
    assert found["pkg.m.C"] == [("workspace:w", "pkg"), ("topic:t1", "pkg"), ("system:b", "pkg.m"), ("topic:t2", "pkg.m"), ("topic:t3", "pkg.m.C")]
    assert ("type:package", "pkg") not in found["pkg.m"]


def test_nothing_is_inherited_through_an_import(tmp_path):
    (tmp_path / "a.py").write_text(_meta("a", "topic:from_a"), encoding="utf-8")
    (tmp_path / "b.py").write_text('"""Plain."""\nfrom a import thing\n', encoding="utf-8")
    assert _effective(tmp_path)["python:b"] == []


def test_two_values_of_a_nearest_namespace_are_an_error():
    assert any("more than one 'system:' tag" in e for e in parse_docstring("---\nid: x\ntags: [system:a, system:b]\n---").errors)
