"""The executor over the edge index's _out/_in maps, without networkx."""

from __future__ import annotations

from sldb.store.graph import StructuredQuery, execute_query
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.models import EdgeNodeRecord, EdgeRecord


def _index() -> EdgeIndex:
    nodes = {
        "sldb://model/TaskDoc": EdgeNodeRecord(id="sldb://model/TaskDoc", node_type="sldb_model"),
        "sldb://document/TaskDoc:001": EdgeNodeRecord(id="sldb://document/TaskDoc:001", node_type="TaskDoc", semantics={"name": "001", "path": "a.md"}),
        "sldb://section/TaskDoc:001#s": EdgeNodeRecord(id="sldb://section/TaskDoc:001#s", node_type="sldb_section"),
        "sldb://semantic_tag/domain.workflow.task": EdgeNodeRecord(id="sldb://semantic_tag/domain.workflow.task", node_type="semantic_tag", facets={"source": {"producer": "sldb"}}),
    }
    edges = [
        EdgeRecord(source="sldb://model/TaskDoc", target="sldb://document/TaskDoc:001", relation="has_document"),
        EdgeRecord(source="sldb://document/TaskDoc:001", target="sldb://section/TaskDoc:001#s", relation="has_section"),
        EdgeRecord(source="sldb://document/TaskDoc:001", target="sldb://semantic_tag/domain.workflow.task", relation="tagged_as"),
    ]
    return EdgeIndex(nodes=nodes, edges=edges)


def _ids(query) -> list[str]:
    return [n.id for n in execute_query(_index(), query)]


def test_descendant_scope_reaches_all_nodes_except_the_root():
    query = StructuredQuery.model_validate({"scope": {"descendant_of": "sldb://model/TaskDoc"}})
    assert _ids(query) == [
        "sldb://document/TaskDoc:001",
        "sldb://section/TaskDoc:001#s",
        "sldb://semantic_tag/domain.workflow.task",
    ]


def test_identity_filter_narrows_by_node_type():
    query = StructuredQuery.model_validate({"scope": {"descendant_of": "sldb://model/TaskDoc"}, "filters": [{"facet": "identity", "conditions": [{"field": "node_type", "op": "eq", "value": "sldb_section"}]}]})
    assert _ids(query) == ["sldb://section/TaskDoc:001#s"]


def test_ancestor_scope_and_semantics_filter():
    query = StructuredQuery.model_validate({"scope": {"ancestor_of": "sldb://section/TaskDoc:001#s"}, "filters": [{"facet": "semantics", "conditions": [{"field": "name", "op": "eq", "value": "001"}]}]})
    assert _ids(query) == ["sldb://document/TaskDoc:001"]


def test_prefix_scope_finds_tag_nodes():
    query = StructuredQuery.model_validate({"scope": {"node_id_prefix": "sldb://semantic_tag/"}})
    assert _ids(query) == ["sldb://semantic_tag/domain.workflow.task"]


def test_source_facet_is_filterable():
    query = StructuredQuery.model_validate({"filters": [{"facet": "source", "conditions": [{"field": "producer", "op": "eq", "value": "sldb"}]}]})
    assert _ids(query) == ["sldb://semantic_tag/domain.workflow.task"]


def test_relation_filter_honors_direction():
    query = StructuredQuery.model_validate({"scope": {"node_id_prefix": "sldb://document/"}, "relations": [{"direction": "incoming"}]})
    [node] = execute_query(_index(), query)
    assert [e.relation for e in node.edges] == ["has_document"]
