"""The graph layer as a library, and its parity with kgdb over the same graph."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api import graph as graph_api
from sldb.store.graph import StructuredQuery, execute_query, sldb_semantic_export_to_snapshot
from sldb.store.graph.convert import index_from_snapshot

FIXTURE = Path(__file__).resolve().parents[2] / "contracts" / "fixtures" / "sldb_kgdb_semantic_export.v1.json"
QUERY_DIR = Path(__file__).resolve().parents[2] / "contracts" / "queries" / "sldb"

MODULE = "sldb_graph_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class TaskDoc(StructuredNLDoc):
    __semantics__ = {"domain": ["workflow", "task"], "system": "desk"}
    __template__ = "# ⸢rev•title⸥\\n\\n⸢rev•body⸥"
    title: str = Field(description="Title.")
    body: str = Field(description="Body.")
'''


def test_executor_matches_kgdb_on_the_five_example_queries():
    """The gate: same ids as kgdb over the same semantic export graph, for all five queries."""
    networkx = pytest.importorskip("networkx")
    kgdb_execute = pytest.importorskip("kgdb.query").execute_query
    kgdb_ingest = pytest.importorskip("kgdb.ingest").sldb_semantic_export_to_snapshot
    add_knowledge_node = pytest.importorskip("kgdb.graph.utils").add_knowledge_node
    kgdb_query = pytest.importorskip("kgdb.query.language").StructuredQuery

    payload = json.loads(FIXTURE.read_text(encoding="utf-8"))
    index = index_from_snapshot(sldb_semantic_export_to_snapshot(payload))
    graph = networkx.DiGraph()
    for node in kgdb_ingest(payload).nodes:
        add_knowledge_node(graph, node)

    for path in sorted(QUERY_DIR.glob("*.json")):
        data = json.loads(path.read_text(encoding="utf-8"))
        mine = [n.id for n in execute_query(index, StructuredQuery.model_validate(data))]
        theirs = [n.identity.node_id for n in kgdb_execute(graph, kgdb_query.model_validate(data))]
        assert sorted(mine) == sorted(theirs), path.name


@pytest.fixture
def world(tmp_path: Path):
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root = tmp_path / "world"
    root.mkdir()
    store = api.init_store(root).store_path
    api.add_model(store, f"{MODULE}:TaskDoc", str(tmp_path))
    api.init_relations(store, str(tmp_path))
    return root, store, str(tmp_path)


def test_graph_reads_the_store_edge_index(world):
    root, store, py = world
    api.create_document(store, "TaskDoc", root / "task.md", {"title": "Alpha", "body": "Body"}, "task", py)
    assert "sldb://document/TaskDoc:task" in graph_api.graph_list(store)
    node = graph_api.graph_get(store, "sldb://document/TaskDoc:task")
    assert node.node_type == "TaskDoc"
    query = StructuredQuery.model_validate({"scope": {"descendant_of": "sldb://model/TaskDoc"}, "filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "TaskDoc"}]}]})
    assert [n.id for n in graph_api.execute_query(store, query)] == ["sldb://document/TaskDoc:task"]


def test_store_typed_graph_matches_kgdb(world):
    """Parity over a real store: the edge index vs kgdb's typed snapshot, same ids."""
    networkx = pytest.importorskip("networkx")
    build_typed_snapshot = pytest.importorskip("kgdb.ingest.typed").build_typed_snapshot
    kgdb_execute = pytest.importorskip("kgdb.query").execute_query
    add_knowledge_node = pytest.importorskip("kgdb.graph.utils").add_knowledge_node
    kgdb_query = pytest.importorskip("kgdb.query.language").StructuredQuery

    root, store, py = world
    api.create_document(store, "TaskDoc", root / "task.md", {"title": "Alpha", "body": "Body"}, "task", py)
    data = {"scope": {"descendant_of": "sldb://model/TaskDoc"}, "filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "TaskDoc"}]}]}

    mine = [n.id for n in graph_api.execute_query(store, StructuredQuery.model_validate(data), include_linked=False)]
    snapshot, _ = build_typed_snapshot(store, py)
    graph = networkx.DiGraph()
    for node in snapshot.nodes:
        add_knowledge_node(graph, node)
    theirs = [n.identity.node_id for n in kgdb_execute(graph, kgdb_query.model_validate(data))]
    assert sorted(mine) == sorted(theirs)


def test_snapshot_round_trip_and_cli(world, tmp_path, capsys):
    from sldb.cli import main as cli_main

    root, store, py = world
    api.create_document(store, "TaskDoc", root / "task.md", {"title": "Alpha", "body": "Body"}, "task", py)
    output = tmp_path / "graph.json"
    graph_api.snapshot_save(store, output, include_linked=False)
    reloaded = graph_api.snapshot_load(output)
    assert any(n.identity.node_id == "sldb://model/TaskDoc" for n in reloaded.nodes)
    assert cli_main(["graph", "get", "sldb://model/TaskDoc", "--store", str(store)]) == 0
    assert '"sldb_model"' in capsys.readouterr().out
    assert cli_main(["graph", "list", "--store", str(store)]) == 0
    assert cli_main(["graph", "neighborhood", "sldb://model/TaskDoc", "--store", str(store)]) == 0
