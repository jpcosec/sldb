"""The whole-graph analyses over a real store, and the `sldb graph` commands that print them."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from sldb import api
from sldb.api.graph import graph_central, graph_components, graph_cycles, graph_isolated, graph_order, graph_path, graph_paths, graph_similar
from sldb.cli import main as cli_main
from sldb.cli.serve.graph_routes import path_payload
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.graph.analysis.path_steps import explain_path
from sldb.store.models import EdgeNodeRecord, EdgeRecord

MODULE = "sldb_analysis_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Spec(StructuredNLDoc):
    __semantics__ = {"type": ["doc", "spec"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


class AnalysisWorld:
    """A store whose specs form a chain: 3 -> 2 -> 1, plus one spec nobody relates to."""

    def __init__(self, base: Path) -> None:
        self.root, self.py = base / "world", str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        api.add_model(self.store, f"{MODULE}:Spec", self.py)
        api.init_relations(self.store, self.py)
        self._populate()

    def _populate(self) -> None:
        for name in ("s1", "s2", "s3", "lonely"):
            self.create("Spec", name, {"title": name.upper()})
        self.relation_type("refines")
        self.relation("s2-s1", "Spec:s2", "Spec:s1")
        self.relation("s3-s2", "Spec:s3", "Spec:s2")

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str) -> None:
        self.create("RelationTypeDoc", f"rt-{name}", {"title": name, "name": name, "direction": "directed", "cardinality": "many_to_many", "axis": "WHY", "source_types": ["Spec"], "target_types": ["Spec"], "condition": "", "description": f"{name}."})

    def relation(self, name: str, src: str, tgt: str) -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": "refines", "condition": "", "notes": ""})


@pytest.fixture
def world(tmp_path: Path) -> AnalysisWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    return AnalysisWorld(tmp_path)


S1, S2, S3 = (f"sldb://document/Spec:{n}" for n in ("s1", "s2", "s3"))


def test_the_authored_relation_is_what_gets_walked_not_the_structural_spine(world: AnalysisWorld):
    """Without this, every pair of specs is two hops apart through their model node."""
    assert graph_path(world.store, S3, S1) == [S3, S2, S1]
    assert graph_path(world.store, S3, S1, relations=["has_document"]) == [S3, "sldb://model/Spec", S1]


def test_order_and_cycles_over_what_the_store_asserts(world: AnalysisWorld):
    assert graph_cycles(world.store) == []
    order = graph_order(world.store)
    assert order.index(S1) < order.index(S2) < order.index(S3)


def test_a_document_nobody_relates_to_shows_up_as_isolated(world: AnalysisWorld):
    """Restricted to one class: unrestricted, every field and section node is isolated too."""
    assert graph_isolated(world.store, node_types=["Spec"]) == ["sldb://document/Spec:lonely"]
    assert graph_components(world.store, node_types=["Spec"])[0] == [S1, S2, S3]
    assert "sldb://field/RelationDoc.condition" in graph_isolated(world.store)


def test_centrality_and_resemblance_over_a_real_store(world: AnalysisWorld):
    assert graph_central(world.store, kind="in_degree", limit=1) == [(S1, 1.0)]
    resembling = dict(graph_similar(world.store, S1, node_types=["Spec"]))
    assert resembling == {S2: 3, S3: 3, "sldb://document/Spec:lonely": 3}


def test_the_cli_prints_each_analysis(world: AnalysisWorld, capsys):
    for argv in (["graph", "cycles"], ["graph", "order"], ["graph", "components"], ["graph", "central", "--kind", "degree"], ["graph", "similar", S1], ["graph", "path", S3, S1]):
        assert cli_main([*argv, "--store", str(world.store)]) == 0
    assert S1 in capsys.readouterr().out


def test_the_cli_says_so_when_there_is_no_path_and_exits_nonzero(world: AnalysisWorld, capsys):
    assert cli_main(["graph", "path", S1, "sldb://document/Spec:lonely", "--store", str(world.store)]) == 1
    assert "No path" in capsys.readouterr().out


def _refines(relation_doc: str, direction: str = "forward") -> dict:
    return {"relation": "refines", "direction": direction, "provenance": {"origin": "relation_doc", "relation_doc": relation_doc}}


def test_explain_says_which_edge_joins_each_hop_and_where_it_came_from(world: AnalysisWorld):
    """The authored chain read both ways: forward from s3, backward from s1; the plain form stays a list."""
    assert graph_path(world.store, S3, S1, explain=True) == {"path": [S3, S2, S1], "steps": [{"source": S3, "target": S2, "edges": [_refines("s3-s2")]}, {"source": S2, "target": S1, "edges": [_refines("s2-s1")]}]}
    backward = graph_path(world.store, S1, S3, explain=True)
    assert [e["direction"] for step in backward["steps"] for e in step["edges"]] == ["backward", "backward"]
    assert graph_paths(world.store, S3, S1, explain=True) == [graph_path(world.store, S3, S1, explain=True)]
    assert graph_paths(world.store, S3, S1) == [[S3, S2, S1]]


def test_a_hop_lists_every_edge_by_precedence_and_a_mirror_is_its_authored_edge_read_backward():
    a, b = "sldb://document/M:a", "sldb://document/M:b"
    meta = {"origin": "relation_doc", "relation_doc": "r1", "evidence": "x"}
    edges = [EdgeRecord(source=b, target=a, relation="peer", metadata=meta), EdgeRecord(source=a, target=b, relation="peer", metadata={**meta, "reverse": True}),
             EdgeRecord(source=a, target=b, relation="mentions", metadata={"origin": "alias"}), EdgeRecord(source=a, target=b, relation="owns", metadata={"origin": "schema", "field": "owner", "from_store": "other"}),
             EdgeRecord(source=a, target=b, relation="odd", metadata={"origin": "custom"})]
    index = EdgeIndex(nodes={n: EdgeNodeRecord(id=n, node_type="M") for n in (a, b)}, edges=edges)
    peer = {"relation": "peer", "direction": "backward", "provenance": {"origin": "relation_doc", "relation_doc": "r1"}}
    owns = {"relation": "owns", "direction": "forward", "provenance": {"origin": "schema", "field": "owner", "from_store": "other"}}
    rest = [{"relation": "mentions", "direction": "forward", "provenance": {"origin": "alias"}}, {"relation": "odd", "direction": "forward", "provenance": {"origin": "custom"}}]
    assert explain_path(index, [a, b], "*")["steps"][0]["edges"] == [peer, owns, *rest]
    assert explain_path(index, [a, b], ["peer"], directed=True)["steps"][0]["edges"] == [peer]


def test_the_cli_and_serve_expose_the_explained_path(world: AnalysisWorld, capsys):
    assert cli_main(["graph", "path", S3, S1, "--explain", "--store", str(world.store)]) == 0
    assert json.loads(capsys.readouterr().out)["steps"][0]["edges"] == [_refines("s3-s2")]
    plain, explained = (path_payload(SimpleNamespace(path=f"/graph/path?source={S3}&target={S1}{q}"), world.store) for q in ("", "&explain=1"))
    assert plain == ({"path": [S3, S2, S1]}, 200)
    assert explained[0]["path"] == [S3, S2, S1] and explained[0]["steps"][1]["edges"] == [_refines("s2-s1")]


def test_explain_over_the_repo_own_index_names_origin_and_relation_doc():
    """The desk's rituals: execution activates testing, testing hands to closeout."""
    store = str(Path(__file__).resolve().parents[2] / ".sldb")
    found = graph_path(store, "sldb://document/RitualDoc:ritual-execution", "sldb://document/RitualDoc:ritual-closeout", explain=True, include_linked=False)
    edges = [e for step in found["steps"] for e in step["edges"]]
    assert edges and all(e["provenance"]["origin"] and ("relation_doc" in e["provenance"] or "field" in e["provenance"]) for e in edges)
