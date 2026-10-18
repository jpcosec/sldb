"""The delivery audit of task-unify-store-context-and-federation: what its done-when names and
no test pinned yet.

- FAQ and explore read their files from the project root, wherever they are run from.
- Federation reaches every linked store once, even when two stores link each other.
"""

from __future__ import annotations

import json

from sldb.api import add_model, create_document, init_store, link_store, load_runtime_documents
from sldb.cli import main
from sldb.store.edge_index.federation import federated_stores

FAQ = "# FAQ\n\n## How do I start?\n\nRun `sldb stores init`.\n"


def test_faq_and_explore_are_anchored_to_the_project_root(tmp_path, monkeypatch, capsys):
    init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "faq.md").write_text(FAQ, encoding="utf-8")
    deep = tmp_path / "src" / "pkg"
    deep.mkdir(parents=True)
    monkeypatch.chdir(deep)
    assert main(["faq", "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["questions"][0]["title"] == "How do I start?"
    assert main(["explore", "stores init", "--source", "docs", "--format", "json"]) == 0
    assert any(hit["path"].endswith("faq.md") for hit in json.loads(capsys.readouterr().out)["results"])


def test_two_stores_linking_each_other_are_each_reached_once(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    a.mkdir(), b.mkdir()
    sa, sb = init_store(a).store_path, init_store(b).store_path
    link_store(sa, sb, "b"), link_store(sb, sa, "a")
    assert [path for path, _ in federated_stores(sa, include_linked=True)] == [sa.resolve(), sb.resolve()]
    ref = "sldb.models.relation_type_doc:RelationTypeDoc"
    add_model(sb, ref)
    create_document(sb, "RelationTypeDoc", b / "t.md", {"name": "t", "title": "t", "description": "d."}, "t")
    names = [d.name for d in load_runtime_documents(sa, None, include_linked=True)]
    assert names.count("t") == 1
