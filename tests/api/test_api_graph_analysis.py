"""The whole-graph analyses over a real store, and the `sldb graph` commands that print them."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.graph import graph_central, graph_components, graph_cycles, graph_isolated, graph_order, graph_path, graph_similar
from sldb.cli import main as cli_main

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
