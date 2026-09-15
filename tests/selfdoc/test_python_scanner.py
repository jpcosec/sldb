from __future__ import annotations

from sldb.selfdoc.python_scanner import PythonScanner
from sldb.cli.selfdoc_inspect import rename_candidates
from sldb.cli.commands.selfdoc import SelfdocCLI
from sldb.selfdoc.python_source_graph import source_snapshot
from sldb.selfdoc.python_source_scan import scan_source_facts
from sldb.selfdoc.kgdb_sync import graph_is_current
from sldb.selfdoc.python_relation_registry import validate_source_snapshot
from sldb.models.python_symbol_doc import PythonSymbolDoc
from sldb.runtime.validation import render_model_markdown


def test_scanner_uses_qualified_names_hashes_and_static_imports(tmp_path):
    source = tmp_path / "src" / "demo"
    source.mkdir(parents=True)
    (source / "mod.py").write_text("import os\nfrom . import sibling\nclass Box:\n    \"\"\"A box.\"\"\"\n    def open(self, key: str) -> None:\n        \"\"\"Open it.\"\"\"\n", encoding="utf-8")
    symbols = PythonScanner().scan(tmp_path / "src", "demo")
    assert [(item.id, item.signature, item.imports) for item in symbols] == [
        ("python:demo.demo.mod:Box", None, [".", "os"]),
        ("python:demo.demo.mod:Box.open", "open(self, key: str)", [".", "os"]),
    ]


def test_rename_candidates_reject_ambiguous_matches(tmp_path):
    path = tmp_path / "old.md"
    payload = PythonSymbolDoc(id="old", system="demo", module="demo", qualname="Old", kind="ClassDef",
        source_path="old.py", source_span="1:1", source_sha256="hash", architecture_spec="Not declared.",
        signature="Not applicable.", docstring="Old.", imports="[]", purpose="Not documented.",
        architecture="Not documented.", provenance="test")
    path.write_text(render_model_markdown(PythonSymbolDoc, payload.model_dump()) + "\n", encoding="utf-8")
    plans = [type("Plan", (), {"payload": payload.model_copy(update={"id": name})}) for name in ("new-a", "new-b")]
    assert rename_candidates(plans, [str(path.relative_to(tmp_path))], tmp_path) == []


def test_python_check_returns_failure_when_report_is_not_ok(tmp_path, monkeypatch):
    args = type("Args", (), {"store": None, "source_root": "src", "package": None,
        "selfdoc_command": "python-check"})
    (tmp_path / "src").mkdir()
    monkeypatch.setattr("sldb.cli.commands.selfdoc.documentation_store", lambda _: (tmp_path / ".sldb", tmp_path))
    monkeypatch.setattr("sldb.cli.commands.selfdoc.PythonScanner.scan", lambda *_: [])
    monkeypatch.setattr(SelfdocCLI, "_sync_python_documents", lambda *_: type("Report", (), {"ok": False})())
    assert SelfdocCLI()._python_operate(args) == 1


def test_source_graph_keeps_imports_references_and_containment_separate(tmp_path):
    source = tmp_path / "src" / "demo"
    source.mkdir(parents=True)
    (source / "types.py").write_text("class Thing:\n    pass\n", encoding="utf-8")
    (source / "consumer.py").write_text("from .types import Thing as LocalThing\nclass Use:\n    value: LocalThing\n", encoding="utf-8")
    snapshot = source_snapshot(scan_source_facts(tmp_path / "src", "demo"), "demo")
    use = next(node for node in snapshot["nodes"] if node["ast"].get("name") == "Use")
    edges = {(edge["relation_type"], edge["target_id"]) for edge in use["edges"]}
    assert ("references", "python:demo.demo.types:Thing") in edges
    module = next(node for node in snapshot["nodes"] if node["identity"]["node_id"] == "python:demo.demo.consumer")
    assert ("imports", "python:demo.demo.types:Thing") in {(edge["relation_type"], edge["target_id"]) for edge in module["edges"]}
    assert ("contains", "python:demo.demo.consumer:Use") in {(edge["relation_type"], edge["target_id"]) for edge in module["edges"]}


def test_source_graph_rejects_an_endpoint_outside_registered_relation_types():
    snapshot = {
        "nodes": [
            {"identity": {"node_id": "module", "node_type": "python_module"},
             "edges": [{"target_id": "external", "relation_type": "contains"}]},
            {"identity": {"node_id": "external", "node_type": "python_external"}, "edges": []},
        ]
    }
    registry = {
        "contains": {"source_types": ["python_module"], "target_types": ["python_symbol"], "cardinality": "many_to_many"},
        "imports": {"source_types": [], "target_types": [], "cardinality": "many_to_many"},
        "references": {"source_types": [], "target_types": [], "cardinality": "many_to_many"},
    }
    import pytest
    with pytest.raises(ValueError, match="target type 'python_external' is not allowed"):
        validate_source_snapshot(snapshot, registry)


def test_kgdb_graph_check_rejects_missing_or_stale_source_nodes(tmp_path):
    snapshot = {"nodes": [{"identity": {"node_id": "node", "node_type": "python_symbol"}, "source": {"sha256": "a"}, "ast": {"line": 1}}]}
    output = tmp_path / "graph.json"
    assert not graph_is_current(snapshot, output)
    output.write_text('{"nodes": [{"id": "node", "schema": {"source": {"sha256": "b"}, "ast": {"line": 1}}}]}', encoding="utf-8")
    assert not graph_is_current(snapshot, output)
    output.write_text('{"nodes": [{"id": "node", "schema": {"source": {"sha256": "a"}, "ast": {"line": 1}}}]}', encoding="utf-8")
    assert graph_is_current(snapshot, output)
    output.write_text('{"nodes": [{"id": "node", "schema": {"source": {"sha256": "a"}, "ast": {"line": 1}}}, {"id": "stale", "schema": {}}]}', encoding="utf-8")
    assert not graph_is_current(snapshot, output)
