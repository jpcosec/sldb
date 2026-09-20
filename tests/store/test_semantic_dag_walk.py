"""`se.` navigation reads the semantic DAG's edges instead of matching the tag strings.

Until now the DAG had no reader: `semantic_children` matched `startswith` over the tag list, so
deleting every `semantic_parent` edge changed no answer. These pin what walking it buys — and
what it fixes, because matching strings had a quirk nobody meant.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from sldb.store.io import load_semantic_dag, save_semantic_dag
from sldb.store.models.semantic_d_a_g import SemanticDAG
from sldb.store.models.semantic_node import SemanticNode
from sldb.store.query import list_semantic
from sldb.store.semantic_dag_graph import above, children, dag_graph, reach, relative, roots, scope, under

TAGS = ["type", "type.knowledge", "type.knowledge.anchor", "type.knowledge.spec", "layer", "layer.topology"]


def dag_of(parents: dict[str, list[str]]) -> SemanticDAG:
    return SemanticDAG(nodes=[SemanticNode(id=tag, parents=up) for tag, up in parents.items()])


DERIVED = dag_of({
    "type": [], "type.knowledge": ["type"],
    "type.knowledge.anchor": ["type.knowledge"], "type.knowledge.spec": ["type.knowledge"],
    "layer": [], "layer.topology": ["layer"],
})


def test_naming_a_tag_reaches_its_subtree_and_a_document_is_reached_by_its_ancestors():
    """The two directions of the same edge: `scope` looks down, `reach` looks up."""
    assert scope(DERIVED, "type.knowledge") == {"type.knowledge", "type.knowledge.anchor", "type.knowledge.spec"}
    assert scope(DERIVED, "type.knowledge.spec") == {"type.knowledge.spec"}
    assert scope(DERIVED, "nobody") == {"nobody"}
    assert above(DERIVED, "type.knowledge.spec") == ["type", "type.knowledge"]
    assert reach(DERIVED, ["type.knowledge.spec"]) == {"type.knowledge.spec", "type.knowledge", "type"}


def test_the_dag_is_a_graph_of_child_to_parent_edges():
    graph = dag_graph(DERIVED)
    assert graph.number_of_nodes() == 6
    assert ("type.knowledge", "type") in graph.edges
    assert roots(DERIVED) == ["layer", "type"]
    assert children(DERIVED, "type.knowledge") == ["type.knowledge.anchor", "type.knowledge.spec"]
    assert under(DERIVED, "type") == ["type.knowledge", "type.knowledge.anchor", "type.knowledge.spec"]
    assert children(DERIVED, "nobody") == [] and under(DERIVED, "nobody") == []


def test_a_parent_that_is_not_a_prefix_is_an_edge_like_any_other():
    """The thing the string matching could never see, and the DAG file could always hold."""
    authored = dag_of({**{n.id: list(n.parents) for n in DERIVED.nodes}, "layer.topology": ["layer", "type.knowledge"]})
    assert "layer.topology" in children(authored, "type.knowledge")
    assert "layer.topology" in under(authored, "type")


def test_a_child_reads_relative_to_its_parent_unless_the_name_says_otherwise():
    assert relative("type.knowledge", "type") == "knowledge"
    assert relative("layer.topology", "type.knowledge") == "layer.topology"
    assert relative("type", "") == "type"


@pytest.fixture
def store(tmp_path: Path) -> Path:
    store_path = tmp_path / ".sldb"
    (store_path / "core").mkdir(parents=True)
    (store_path / "core" / "store_index.yaml").write_text("models: []\nstores: []\n", encoding="utf-8")
    save_semantic_dag(store_path, DERIVED)
    return store_path


def test_listing_walks_the_dag_and_leaves_stop_being_invisible(store: Path):
    """Matching strings only listed a child that had children of its own: `layer.topology` was
    reachable by name and unreachable by navigation."""
    assert list_semantic(store, "se", lambda ref, pythonpath=None: None) == ["layer", "type"]
    assert list_semantic(store, "se.type.knowledge", lambda ref, pythonpath=None: None) == ["anchor", "spec"]
    assert list_semantic(store, "se.layer", lambda ref, pythonpath=None: None) == ["topology"]


def test_listing_sees_a_parent_declared_by_hand_in_the_dag_file(store: Path):
    dag = load_semantic_dag(store)
    dag.nodes = [n if n.id != "layer.topology" else SemanticNode(id=n.id, parents=["layer", "type.knowledge"]) for n in dag.nodes]
    save_semantic_dag(store, dag)
    assert "layer.topology" in list_semantic(store, "se.type.knowledge", lambda ref, pythonpath=None: None)


def test_naming_a_parent_now_reaches_the_documents_under_it(store: Path, monkeypatch):
    """`se.type.knowledge` answered [] while its subtree held documents. That was the bug."""
    from sldb.store.query import get_semantic
    from sldb.store.query_engine import semantic_utils

    tagged = [
        _doc("spec-01", ["type.knowledge.spec"]),
        _doc("anchor-a", ["type.knowledge.anchor"]),
        _doc("elsewhere", ["layer.topology"]),
    ]
    monkeypatch.setattr(semantic_utils.SemanticUtils, "local_semantic_docs", classmethod(lambda cls, *a, **k: (tagged, None)))
    assert get_semantic(store, "se.type.knowledge", _no_model) == ["st.{Doc}.anchor-a", "st.{Doc}.spec-01"]
    assert get_semantic(store, "se.type.knowledge.spec", _no_model) == ["st.{Doc}.spec-01"]
    assert get_semantic(store, "se.layer", _no_model) == ["st.{Doc}.elsewhere"]


def test_a_glob_still_matches_tag_by_tag_while_a_plain_tag_names_its_subtree(store: Path):
    """`find` keeps both readings: `se.type` is the subtree, `se.type.*` is the pattern."""
    from sldb.store.query_engine.semantic import SemanticEngine

    spec = _doc("spec-01", ["type.knowledge.spec"])
    assert SemanticEngine._in_scope(store, "type", spec)
    assert SemanticEngine._in_scope(store, "type.knowledge.spec", spec)
    assert not SemanticEngine._in_scope(store, "layer", spec)
    assert SemanticEngine._in_scope(store, "type.knowledge.*", spec)
    assert not SemanticEngine._in_scope(store, "type.*", spec)


def _no_model(model_ref, pythonpath=None):
    return None


class _Doc:
    """The three fields the semantic engine reads off a runtime document."""

    def __init__(self, name: str, tags: list[str]) -> None:
        self.name, self.semantic_tags, self.model_name = name, tags, "Doc"


def _doc(name: str, tags: list[str]) -> _Doc:
    return _Doc(name, tags)
