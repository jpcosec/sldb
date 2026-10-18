"""The docstring metadata profile is parsed strictly and every problem is reported where it is.

Spec: docs/architecture/code-docstring-indexing.spec.md section 2. The earlier reader returned
nothing for malformed metadata, so a declaration silently lost its identity.
"""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from sldb.api import add_model, init_store, track_document_file
from sldb.cli import main
from sldb.selfdoc.docstring_metadata import parse_docstring
from sldb.selfdoc.python_source_scan import metadata_diagnostics


def test_a_valid_block_with_or_without_the_blank_line_before_the_closer():
    for closer in ("\n---", "\n\n---"):
        meta = parse_docstring(f"---\nid: a.b\nkind: core\ntags: [topic:x, topic:x, system:sldb]{closer}\nFirst paragraph.\n\nMore.")
        assert meta.errors == [] and meta.values == {"id": "a.b", "kind": "core", "tags": ["topic:x", "system:sldb"]}
        assert meta.body == "First paragraph.\n\nMore."


def test_no_metadata_and_a_later_rule_in_prose_are_ordinary_text():
    assert not parse_docstring("Plain docstring.").declared
    later = parse_docstring("Intro.\n---\nid: not.metadata\n---")
    assert not later.declared and later.body.startswith("Intro.")


@pytest.mark.parametrize("block, problem", [
    ("---\nid: a\n", "never closes"),
    ("---\nid: [a\n---", "not valid YAML"),
    ("---\n- a\n---", "must be a mapping"),
    ("---\nid: a\nowner: me\n---", "unknown metadata key 'owner'"),
    ("---\nid: a\nid: b\n---", "duplicate key"),
    ("---\nkind: core\n---", "'id' is required"),
    ("---\nid: a\nkind: ''\n---", "'kind' must be a nonempty string"),
    ("---\nid: a\ntags: topic:x\n---", "'tags' must be a list"),
    ("---\nid: a\ntags: [Topic X]\n---", "is not namespace:value"),
])
def test_each_malformed_block_says_why(block, problem):
    assert any(problem in error for error in parse_docstring(block).errors)


REPO = Path(__file__).resolve().parents[2]


def _project(tmp_path, source: str):
    (tmp_path / "src" / "demo").mkdir(parents=True)
    (tmp_path / "src" / "demo" / "m.py").write_text(source, encoding="utf-8")
    sp = init_store(tmp_path).store_path
    add_model(sp, "sldb.models.relation_type_doc:RelationTypeDoc")
    (tmp_path / "types").mkdir()
    for name in ("contains", "imports", "references"):   # the vocabulary python-sync validates against
        shutil.copy(REPO / "kgdb" / "relation_types" / f"{name}.md", tmp_path / "types" / f"{name}.md")
        track_document_file(sp, "RelationTypeDoc", tmp_path / "types" / f"{name}.md", name)
    return sp


def test_diagnostics_name_the_file_and_line_and_catch_a_repeated_id(tmp_path):
    _project(tmp_path, '"""---\nid: demo.m\n---\nModule."""\n\n\nclass A:\n    """---\nid: demo.m\n---\nAlso demo.m."""\n\n\ndef f():\n    """---\nid: demo.f\nextra: 1\n---\nF."""\n')
    found = metadata_diagnostics(tmp_path / "src", [])
    assert any(d.startswith("demo/m.py:7: declared id 'demo.m' is also declared at demo/m.py:1") for d in found)
    assert any(d.startswith("demo/m.py:14: unknown metadata key 'extra'") for d in found)


def test_python_sync_writes_nothing_while_metadata_is_malformed(tmp_path, monkeypatch, capsys):
    sp = _project(tmp_path, '"""---\nid: demo.m\nbogus: 1\n---\nModule."""\n')
    monkeypatch.chdir(tmp_path)
    assert main(["selfdoc", "python-sync", "--store", str(sp), "--source-root", "src", "--system", "demo"]) == 1
    report = json.loads(capsys.readouterr().out)
    assert report["metadata_errors"] and report["written"] == 0
    assert not (tmp_path / "knowledge").exists() and not (sp / "runtime" / "graphs").exists()


def test_a_failed_sync_leaves_the_previous_graph_and_documents_as_they_were(tmp_path, monkeypatch, capsys):
    """Producer-scoped reconciliation (spec section 4): only a successful scan replaces what
    this extractor published; a scan stopped by malformed metadata removes nothing."""
    sp = _project(tmp_path, '"""---\nid: demo.m\n---\nModule."""\n\n\ndef kept():\n    """Kept."""\n')
    monkeypatch.chdir(tmp_path)
    argv = ["selfdoc", "python-sync", "--store", str(sp), "--source-root", "src", "--system", "demo"]
    assert main(argv) == 0
    graph = sp / "runtime" / "graphs" / "python-source.graph.json"
    before = (graph.read_text(encoding="utf-8"), sorted(p.name for p in (tmp_path / "knowledge" / "symbols").iterdir()))
    (tmp_path / "src" / "demo" / "m.py").write_text('"""---\nid: demo.m\nbogus: 1\n---\nModule."""\n\n\ndef added():\n    pass\n', encoding="utf-8")
    capsys.readouterr()
    assert main(argv) == 1
    assert (graph.read_text(encoding="utf-8"), sorted(p.name for p in (tmp_path / "knowledge" / "symbols").iterdir())) == before
