"""GO04: a document node carries its projected payload, field_hashes, source_hash and the model's
contract_signature; EdgeIndex.stale sees an edit from outside sldb, a moved contract and an older
shard; a StructuredQuery filters on the `payload` facet without re-extracting a document."""

from __future__ import annotations

import sys

import pytest
import yaml

from sldb import api
from sldb.api.graph import execute_query as api_execute_query
from sldb.core.exceptions import SLDBGraphArgumentError, SLDBModelError
from sldb.runtime.validation import Validator
from sldb.store import documents_hash
from sldb.store.edge_index.compose import compose_edge_index, invalidate_composed_edge_indexes
from sldb.store.edge_index.doc_contribution import build_doc_edges
from sldb.store.edge_index.edge_index import EdgeIndex
from sldb.store.edge_index.node_ids import EDGE_INDEX_VERSION
from sldb.store.graph.executor import execute_query
from sldb.store.graph.language import FacetFilter, FieldCondition, StructuredQuery
from sldb.store.graph.payload_match import payload_condition
from sldb.store.io.shards import invalidate_shard_cache
from sldb.store.layout import edges_shard_path
from sldb.store.model_contract import contract_signature, indexed_fields, projected_fields
from sldb.store.models import DocumentEntry, EdgeNodeRecord
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_payload_projection_test_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Ticket(StructuredNLDoc):
    __references__ = {references}
    {extra}
    __template__ = """---
status: ⸢rev•status⸥
priority: ⸢rev•priority⸥
labels: ⸢rev•labels⸥
---

# ⸢rev•title⸥

```yaml
⸢rev,dict•meta⸥
```

⸢rev,table[name,state]•steps⸥
"""
    title: str = Field(description="Title.")
    status: str = Field(description="Status.")
    priority: int = Field(description="Priority.")
    labels: list[str] = Field(description="Labels.")
    meta: dict = Field(description="Free metadata, nested.")
    steps: list[dict[str, str]] = Field(description="Steps, a table.")
'''


def _payload(title: str, status: str) -> dict:
    return {"title": title, "status": status, "priority": 2, "labels": ["x", "y"], "meta": {"k": "v"}, "steps": [{"name": "s1", "state": "done"}]}


def _write_models(tmp_path, references: str = '["title"]', extra: str = "") -> None:
    (tmp_path / f"{MODULE}.py").write_text(_MODELS.format(references=references, extra=extra), encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_runtime_cache()


def _fresh_read() -> None:
    invalidate_composed_edge_indexes()
    invalidate_shard_cache()


@pytest.fixture
def world(tmp_path):
    py = str(tmp_path)
    _write_models(tmp_path)
    sys.path.insert(0, py)
    try:
        root = tmp_path / "world"
        root.mkdir()
        sp = api.init_store(root).store_path
        api.add_model(sp, f"{MODULE}:Ticket", py)
        api.create_document(sp, "Ticket", root / "a.md", _payload("a", "open"), "a", py)
        api.create_document(sp, "Ticket", root / "b.md", _payload("b", "closed"), "b", py)
        yield tmp_path, root, sp, py
    finally:
        sys.path.remove(py)
        sys.modules.pop(MODULE, None)


def _status_is(value: str) -> StructuredQuery:
    return StructuredQuery(filters=[FacetFilter(facet="payload", conditions=[FieldCondition(field="status", op="eq", value=value)])])


def test_the_index_version_is_5():
    assert EDGE_INDEX_VERSION == "5"


def test_a_written_document_node_exposes_its_projection_and_omits_nested_fields(world):
    _, _, sp, _ = world
    node = api.edge_node(sp, "Ticket:a")
    assert node.payload == {"labels": ["x", "y"], "priority": 2, "status": "open", "title": "a"}
    entry = next(e for e in documents_hash.entries_of(sp, "Ticket") if e.name == "a")
    assert node.field_hashes == entry.field_hashes and set(node.field_hashes) >= {"meta", "steps"}
    assert node.source_hash == entry.source_hash != ""
    assert node.contract_signature == contract_signature(sys.modules[MODULE].Ticket) != ""
    sections = [n for n in api.edge_nodes_of_type(sp, "sldb_section") if n.semantics["document_id"] == "Ticket:a"]
    assert sections and all(n.payload == {} and n.source_hash == "" and n.contract_signature == "" for n in sections)


def test_the_shard_persists_the_four_fields_only_on_the_document_node(world):
    _, _, sp, _ = world
    shard = yaml.safe_load(edges_shard_path(sp, "Ticket", "a").read_text(encoding="utf-8"))
    doc = next(n for n in shard["nodes"] if n["id"] == "sldb://document/Ticket:a")
    assert {"payload", "field_hashes", "source_hash", "contract_signature"} <= set(doc)
    others = [n for n in shard["nodes"] if n["id"] != doc["id"]]
    assert others and not any({"payload", "field_hashes", "source_hash", "contract_signature"} & set(n) for n in others)


def test_status_closed_is_answered_with_zero_extractions(world, monkeypatch):
    _, _, sp, _ = world
    calls = []
    original = Validator.extract
    monkeypatch.setattr(Validator, "extract", lambda self, md: calls.append(1) or original(self, md))
    _fresh_read()
    invalidate_runtime_cache()
    nodes = api_execute_query(sp, _status_is("closed"))
    assert [n.id for n in nodes] == ["sldb://document/Ticket:b"]
    assert calls == []


def test_existing_facets_answer_as_before_and_nodes_show_no_new_keys(world):
    _, _, sp, _ = world
    query = StructuredQuery(filters=[FacetFilter(facet="identity", conditions=[FieldCondition(field="node_type", op="eq", value="Ticket")])])
    nodes = api_execute_query(sp, query)
    assert [n.id for n in nodes] == ["sldb://document/Ticket:a", "sldb://document/Ticket:b"]
    assert "payload" not in nodes[0].model_dump()


def test_a_filter_on_a_field_not_projected_is_a_query_error_naming_it(world):
    _, _, sp, _ = world
    for field in ("meta", "steps", "nonexistent"):
        query = StructuredQuery(filters=[FacetFilter(facet="payload", conditions=[FieldCondition(field=field, op="is_not_null")])])
        with pytest.raises(SLDBGraphArgumentError, match=repr(field)):
            api_execute_query(sp, query)


def _doc(id_: str, payload: dict) -> EdgeNodeRecord:
    return EdgeNodeRecord(id=f"sldb://document/M:{id_}", node_type="M", payload=payload)


def test_a_projectable_field_absent_from_every_payload_gives_the_empty_set():
    index = EdgeIndex(nodes={n.id: n for n in [_doc("a", {"s": "x"}), _doc("b", {})]}, payload_fields={"M": ["s", "owner"]})
    query = StructuredQuery(filters=[FacetFilter(facet="payload", conditions=[FieldCondition(field="owner", op="eq", value="z")])])
    assert execute_query(index, query) == []


def test_only_document_nodes_match_a_payload_filter():
    tag = EdgeNodeRecord(id="sldb://semantic_tag/t", node_type="semantic_tag")
    index = EdgeIndex(nodes={n.id: n for n in [_doc("a", {"s": "x"}), _doc("b", {}), tag]}, payload_fields={"M": ["s"]})
    query = StructuredQuery(filters=[FacetFilter(facet="payload", conditions=[FieldCondition(field="s", op="is_null")])])
    assert [n.id for n in execute_query(index, query)] == ["sldb://document/M:b"]


@pytest.mark.parametrize(("value", "op", "operand", "expected"), [
    (None, "is_null", None, True), (None, "is_not_null", None, False), (None, "eq", None, False),
    (None, "ne", "x", False), (None, "contains", "x", False), (None, "gt", 1, False), (None, "starts_with", "x", False),
    (["a", "b"], "contains", "a", True), (["a", "b"], "contains", "c", False), (["a", "b"], "eq", ["a", "b"], True),
    (["a", "b"], "eq", "a", False), (["a", "b"], "ne", "a", True), (["a"], "gt", 0, False), (["a"], "lt", 9, False),
    (["a"], "starts_with", "a", False), (["a"], "is_null", None, False), (["a"], "is_not_null", None, True),
    ([], "eq", [], True), (1, "eq", 1.0, True), (True, "eq", 1, True), ("b", "gt", "a", True), ("b", "gt", 1, False),
    ("abc", "starts_with", "ab", True), (3, "lt", 5, True),
])
def test_payload_operators_follow_the_contract(value, op, operand, expected):
    payload = {} if value is None else {"f": value}
    assert payload_condition(payload, FieldCondition(field="f", op=op, value=operand)) is expected


def test_an_edit_from_outside_sldb_is_stale_and_the_rebuild_updates_the_projection(world):
    _, root, sp, py = world
    path = root / "a.md"
    path.write_text(path.read_text(encoding="utf-8").replace("status: open", "status: closed"), encoding="utf-8")
    assert "Ticket:a" in api.load_edge_index(sp).stale
    api.update_store_indexes(sp, py)
    assert api.edge_node(sp, "Ticket:a").payload["status"] == "closed"
    assert api.load_edge_index(sp).stale == []


def test_a_new_references_entry_is_stale_and_the_rebuild_takes_it(world):
    tmp_path, _, sp, py = world
    assert api.load_edge_index(sp).stale == []
    _write_models(tmp_path, references='["title", "status"]')
    assert sorted(api.load_edge_index(sp).stale) == ["Ticket:a", "Ticket:b"]
    api.rebuild_edges(sp, py)
    assert api.load_edge_index(sp).stale == []
    assert api.edge_node(sp, "Ticket:a").contract_signature == contract_signature(sys.modules[MODULE].Ticket)


def test_a_version_4_shard_is_stale_on_open_and_rebuilt_on_the_next_write(world):
    _, root, sp, py = world
    path = edges_shard_path(sp, "Ticket", "a")
    shard = yaml.safe_load(path.read_text(encoding="utf-8"))
    shard["edges_version"] = shard["edges_version"].replace("5|", "4|", 1)
    for node in shard["nodes"]:
        for key in ("payload", "field_hashes", "source_hash", "contract_signature"):
            node.pop(key, None)
    path.write_text(yaml.safe_dump(shard, sort_keys=False, allow_unicode=True), encoding="utf-8")
    _fresh_read()
    assert api.load_edge_index(sp).stale == ["Ticket:a"]
    api.create_document(sp, "Ticket", root / "c.md", _payload("c", "open"), "c", py)
    _fresh_read()
    assert yaml.safe_load(path.read_text(encoding="utf-8"))["edges_version"].startswith("5|")
    assert api.edge_node(sp, "Ticket:a").payload["status"] == "open"
    assert api.load_edge_index(sp).stale == []


def test_indexed_restricts_the_projection(world):
    tmp_path, root, sp, py = world
    _write_models(tmp_path, extra='__indexed__ = ["status", "labels"]')
    api.create_document(sp, "Ticket", root / "c.md", _payload("c", "closed"), "c", py)
    assert api.edge_node(sp, "Ticket:c").payload == {"labels": ["x", "y"], "status": "closed"}
    query = StructuredQuery(filters=[FacetFilter(facet="payload", conditions=[FieldCondition(field="priority", op="eq", value=2)])])
    with pytest.raises(SLDBGraphArgumentError, match="'priority'"):
        api_execute_query(sp, query)


@pytest.mark.parametrize(("indexed", "field"), [('["meta"]', "meta"), ('["steps"]', "steps"), ('["ghost"]', "ghost")])
def test_an_indexed_name_that_cannot_be_projected_fails_when_the_model_loads(tmp_path, indexed, field):
    _write_models(tmp_path, extra=f"__indexed__ = {indexed}")
    sys.path.insert(0, str(tmp_path))
    try:
        with pytest.raises(SLDBModelError, match=f"Ticket.*'{field}'"):
            api.resolve_model_ref(f"{MODULE}:Ticket", str(tmp_path))
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_projected_fields_and_the_signature_follow_the_class(tmp_path):
    _write_models(tmp_path)
    sys.path.insert(0, str(tmp_path))
    try:
        ticket = api.resolve_model_ref(f"{MODULE}:Ticket", str(tmp_path))
        assert indexed_fields(ticket) is None
        assert projected_fields(ticket) == ["labels", "priority", "status", "title"]
        before = contract_signature(ticket)
        ticket.__containment__ = {"steps": ["Ticket"]}
        assert contract_signature(ticket) != before
    finally:
        sys.path.remove(str(tmp_path))
        sys.modules.pop(MODULE, None)


def test_a_model_that_cannot_be_loaded_projects_nothing_and_signs_empty(world):
    _, _, sp, _ = world
    doc = DocumentEntry(name="a", path="a.md", hash_c="h", field_hashes={"title": "t"})
    shard = build_doc_edges("Ticket", doc, [], lambda: None, None)
    node = next(n for n in shard.nodes if n.id == "sldb://document/Ticket:a")
    assert (node.payload, node.contract_signature, node.source_hash, node.field_hashes) == ({}, "", "h", {"title": "t"})
    _fresh_read()
    assert sorted(compose_edge_index(sp, model_type_of=lambda ref, root: None).stale) == ["Ticket:a", "Ticket:b"]
