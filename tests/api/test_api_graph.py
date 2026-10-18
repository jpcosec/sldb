"""The graph layer as a library: the store's graph, queried and saved."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api import graph as graph_api
from sldb.store.graph import StructuredQuery, execute_query


MODULE = "sldb_graph_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class TaskDoc(StructuredNLDoc):
    __semantics__ = {"domain": ["workflow", "task"], "system": "desk"}
    __template__ = "# ⸢rev•title⸥\\n\\n⸢rev•body⸥"
    title: str = Field(description="Title.")
    body: str = Field(description="Body.")
'''


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
