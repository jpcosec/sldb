"""The whole-graph questions: paths, cycles, order, components, centrality, resemblance."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from sldb.core.exceptions import SLDBGraphCycleError
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.graph import analysis, sldb_semantic_export_to_snapshot
from sldb.store.edge_index.acyclic import cycle_errors
from sldb.store.graph.convert import index_from_snapshot
from sldb.store.models import EdgeNodeRecord, EdgeRecord

FIXTURE = Path(__file__).resolve().parents[2] / "contracts" / "fixtures" / "sldb_kgdb_semantic_export.v1.json"


def index_of(edges: list[tuple[str, str, str]], types: dict[str, str] | None = None) -> EdgeIndex:
    """An index holding exactly these `(source, relation, target)` edges."""
    kinds = types or {}
    ids = {end for source, _, target in edges for end in (source, target)}
    nodes = {i: EdgeNodeRecord(id=i, node_type=kinds.get(i, "Doc")) for i in sorted(ids)}
    records = [EdgeRecord(source=s, target=t, relation=r) for s, r, t in edges]
    return EdgeIndex(nodes=nodes, edges=records)


CHAIN = [("a", "implements", "b"), ("b", "implements", "c"), ("c", "implements", "d")]


def test_the_derived_spine_is_excluded_by_default_so_answers_are_not_truisms():
    """Two documents of one model are two hops apart through it; that is not a connection."""
    index = index_of([("doc1", "has_document", "Model"), ("doc2", "has_document", "Model")])
    assert analysis.authored(index) == set()
    assert analysis.to_networkx(index, relations=["implements"]).number_of_edges() == 0
    assert analysis.path_between(index, "doc1", "doc2", relations=["implements"]) is None
    assert analysis.path_between(index, "doc1", "doc2", relations=["has_document"]) == ["doc1", "Model", "doc2"]


def test_a_path_crosses_edges_in_either_direction_unless_asked_to_be_directed():
    index = index_of([("a", "implements", "c"), ("b", "implements", "c")])
    assert analysis.path_between(index, "a", "b") == ["a", "c", "b"]
    assert analysis.path_between(index, "a", "b", directed=True) is None


def test_a_path_between_unrelated_or_unknown_nodes_is_none():
    index = index_of(CHAIN)
    assert analysis.path_between(index, "a", "nowhere") is None
    assert analysis.path_between(index, "a", "d") == ["a", "b", "c", "d"]


def test_every_route_between_two_nodes_shortest_first_and_capped():
    index = index_of([("a", "implements", "b"), ("b", "implements", "d"), ("a", "implements", "c"), ("c", "implements", "d")])
    routes = analysis.paths_between(index, "a", "d")
    assert sorted(routes) == [["a", "b", "d"], ["a", "c", "d"]]
    assert len(analysis.paths_between(index, "a", "d", limit=1)) == 1
    assert analysis.paths_between(index, "a", "d", cutoff=1) == []


def test_a_cycle_is_found_and_a_dag_reports_none():
    assert analysis.cycles(index_of(CHAIN)) == []
    assert analysis.is_acyclic(index_of(CHAIN))
    looped = index_of([*CHAIN, ("d", "implements", "a")])
    assert not analysis.is_acyclic(looped)
    assert sorted(analysis.cycles(looped)[0]) == ["a", "b", "c", "d"]


def test_order_puts_a_node_after_everything_it_points_at():
    index = index_of(CHAIN)
    assert analysis.topological_order(index) == ["d", "c", "b", "a"]
    assert analysis.layers(index) == [["d"], ["c"], ["b"], ["a"]]


def test_ordering_a_cyclic_relation_raises_with_the_cycle_in_hand():
    index = index_of([("a", "implements", "b"), ("b", "implements", "a")])
    with pytest.raises(SLDBGraphCycleError) as caught:
        analysis.topological_order(index)
    assert sorted(caught.value.cycle) == ["a", "b"]
    assert "a -> b" in str(caught.value) or "b -> a" in str(caught.value)


def test_components_islands_and_isolated_nodes():
    index = index_of([*CHAIN, ("x", "implements", "y"), ("lonely", "tagged_as", "tag")])
    assert analysis.components(index) == [["a", "b", "c", "d"], ["x", "y"], ["lonely"], ["tag"]]
    assert analysis.islands(index) == [["x", "y"], ["lonely"], ["tag"]]
    assert analysis.isolated(index) == ["lonely", "tag"]


def test_centrality_ranks_what_the_rest_leans_on():
    index = index_of([("a", "implements", "hub"), ("b", "implements", "hub"), ("c", "implements", "hub")])
    assert analysis.central(index, limit=1)[0][0] == "hub"
    assert analysis.central(index, kind="in_degree", limit=1) == [("hub", 3.0)]
    assert [n for n, _ in analysis.central(index, kind="out_degree", limit=3)] == ["a", "b", "c"]


def test_centrality_rejects_a_kind_it_does_not_know():
    with pytest.raises(ValueError, match="Unknown centrality"):
        analysis.central(index_of(CHAIN), kind="eigenvector")


def test_centrality_of_a_graph_with_no_edges_is_zero_not_a_crash():
    index = EdgeIndex(nodes={"a": EdgeNodeRecord(id="a", node_type="Doc")}, edges=[])
    assert analysis.central(index) == [("a", 0.0)]


def test_resemblance_counts_shared_targets_not_edges_between_the_two():
    index = index_of([
        ("doc1", "tagged_as", "t1"), ("doc1", "tagged_as", "t2"),
        ("doc2", "tagged_as", "t1"), ("doc2", "tagged_as", "t2"),
        ("doc3", "tagged_as", "t1"),
    ])
    assert analysis.similar_to(index, "doc1") == [("doc2", 2), ("doc3", 1)]
    assert analysis.similar_to(index, "doc1", limit=1) == [("doc2", 2)]
    assert analysis.similar_to(index, "nobody") == []


def test_node_types_restrict_the_view_for_components_and_the_answer_for_the_rest():
    """Two different meanings on purpose: see the module docstrings."""
    index = index_of(CHAIN, types={"a": "Spec", "b": "Spec", "c": "Note", "d": "Note"})
    assert analysis.components(index, node_types=["Spec"]) == [["a", "b"]]
    assert [n for n, _ in analysis.central(index, kind="degree", node_types=["Spec"])] == ["b", "a"]
    assert analysis.central(index, kind="degree", node_types=["Spec"])[0][1] == 2.0


def test_resemblance_still_goes_through_the_nodes_the_answer_leaves_out():
    """Asking only for documents must not delete the tags they resemble each other through."""
    index = index_of(
        [("doc1", "tagged_as", "t1"), ("doc2", "tagged_as", "t1")],
        types={"doc1": "Doc", "doc2": "Doc", "t1": "semantic_tag"},
    )
    assert analysis.similar_to(index, "doc1", node_types=["Doc"]) == [("doc2", 1)]


def test_the_analyses_run_over_a_real_semantic_export():
    """End to end on the contract fixture: the derived store graph is one connected DAG."""
    index = index_from_snapshot(sldb_semantic_export_to_snapshot(json.loads(FIXTURE.read_text(encoding="utf-8"))))
    derived = sorted(analysis.present(index))
    assert "has_document" in derived and analysis.authored(index) == set()
    assert analysis.is_acyclic(index)
    assert len(analysis.topological_order(index)) == len(analysis.to_networkx(index).nodes)
    assert analysis.central(index, limit=1)[0][1] > 0


def test_a_cycle_in_a_relation_that_must_be_a_dag_is_an_error_no_per_edge_check_can_see():
    """`semantic_parent` and `extends` are invariants sldb relies on; only the whole graph sees them."""
    healthy = index_of([("child", "semantic_parent", "parent")])
    assert cycle_errors(healthy) == []
    looped = index_of([("a", "semantic_parent", "b"), ("b", "semantic_parent", "a"), ("m", "extends", "m")])
    reported = cycle_errors(looped)
    assert len(reported) == 2
    assert "Relation 'semantic_parent' has a cycle:" in reported[0]
    assert "Relation 'extends' has a cycle: m -> m." in reported[1]
