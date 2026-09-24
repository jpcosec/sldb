"""Parity: the GraphSnapshot generated from the source indexes vs the one composed from the
`runtime/edges/` shards (the retired layer — the reference while it lives).

The retirement plan (`docs/architecture/edges-retirement-plan.md`, §2 rows 2-3) marks the
store/model/document/section/semantic_tag nodes and the has_model/has_document/has_section/
tagged_as/semantic_parent/semantic_equivalent edges as "equivalente exacto". These tests
prove that subset node-for-node and edge-for-edge against the shard route, and declare every
remaining difference by its gap number: G1 (field nodes), G2 (typed contribution: relation
types, anchors, authored relations), G3 (cross-document resolve rules). G4-G6 have no window
in a snapshot's own nodes and edges.

Never asserted against inline literals: both graphs are built, and the old one is the oracle.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api.edges.edge_reading import load_edge_index
from sldb.api.graph import snapshot_load, snapshot_save
from sldb.store.export import export_kgdb_semantic_payload
from sldb.store.graph.convert import snapshot_from_index
from sldb.store.graph.ingest_sldb import sldb_semantic_export_to_snapshot

MODULE = "sldb_graph_source_parity_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Table(StructuredNLDoc):
    __semantics__ = {"type": ["restaurant", "table"]}
    __template__ = "# ⸢rev•title⸥\\n\\nCapacity: ⸢rev•capacity⸥\\n\\n## Notes\\n\\n⸢rev,markdown•notes⸥"
    title: str = Field(description="Title.")
    capacity: int = Field(description="Seats.")
    notes: str = Field(default="", description="Notes.")


class Booking(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nSize: ⸢rev•party_size⸥"
    title: str = Field(description="Title.")
    party_size: int = Field(description="People.")


class Move(StructuredNLDoc):
    __semantics__ = {"type": ["pron", "move"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''

STRUCTURAL_KINDS = ("sldb://store", "sldb://model/", "sldb://document/", "sldb://section/", "sldb://semantic_tag/")
STRUCTURAL_RELATIONS = {"has_model", "has_document", "has_section", "tagged_as", "semantic_parent", "semantic_equivalent"}


class GraphWorld:
    """A real store prepared through the public API; the relations variant adds the typed
    vocabulary (RelationTypeDoc/RelationDoc documents, anchors) of `init_relations`."""

    def __init__(self, base: Path, name: str = "world", relations: bool = False) -> None:
        self.root, self.py = base / name, str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Table", "Booking", "Move"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        if relations:
            api.init_relations(self.store, self.py)
        self.create("Table", "t12", {"title": "Table 12", "capacity": 6, "notes": "By the window."})
        self.create("Table", "t14", {"title": "Table 14", "capacity": 8, "notes": ""})
        self.create("Booking", "b1", {"title": "Ana", "party_size": 6})
        if relations:
            self.relation_type("assigned_to", ["Booking"], ["Table"], cardinality="many_to_one", condition="capacity >= {party_size}")
            self.relation("b1-t12", "Booking:b1", "Table:t12", "assigned_to")
        from sldb.api.semantic import add_semantic_equivalence

        add_semantic_equivalence(self.store, "type.restaurant.table", "exo.table")

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str, source: list[str], target: list[str], **extra) -> None:
        payload = {"title": name, "name": name, "direction": "directed", "cardinality": "many_to_many", "axis": "WHERE", "source_types": source, "target_types": target, "condition": "", "description": f"{name}."}
        self.create("RelationTypeDoc", f"rt-{name}", {**payload, **extra})

    def relation(self, name: str, src: str, tgt: str, rtype: str, condition: str = "") -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": rtype, "condition": condition, "notes": ""})

    def old_snapshot(self, include_linked: bool = False, exclude_tags: tuple = ()):
        """The reference: composed from the `runtime/edges/` shards, as the layer always did."""
        return snapshot_from_index(load_edge_index(self.store, include_linked, exclude_tags))

    def new_snapshot(self):
        """The ported route: source indexes -> semantic export -> GraphSnapshot."""
        return sldb_semantic_export_to_snapshot(export_kgdb_semantic_payload(self.store, self.root, command=["graph", "snapshot", "save"]))


@pytest.fixture
def clean_world(tmp_path: Path) -> GraphWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    return GraphWorld(tmp_path)


@pytest.fixture
def relations_world(tmp_path: Path) -> GraphWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    return GraphWorld(tmp_path, relations=True)


def _by_id(snapshot) -> dict:
    return {n.identity.node_id: n for n in snapshot.nodes}


def _triples(snapshot, relations: set | None = None) -> set:
    out = {(n.identity.node_id, e.target_id, str(e.relation_type)) for n in snapshot.nodes for e in n.edges}
    return out if relations is None else {t for t in out if t[2] in relations}


def _semantics(node) -> dict:
    return {} if node.semantics is None else node.semantics.model_dump()


# --- parity of ids ---------------------------------------------------------------


def test_the_five_structural_kinds_have_the_same_node_ids(clean_world):
    old, new = clean_world.old_snapshot(), clean_world.new_snapshot()
    old_ids, new_ids = set(_by_id(old)), set(_by_id(new))
    old_fields = {i for i in old_ids if i.startswith("sldb://field/")}
    # The only old-layer ids the source route cannot produce are the field nodes: GAP G1.
    assert old_ids - new_ids == old_fields and old_fields
    assert not new_ids - old_ids


def test_every_document_section_and_tag_node_is_in_both_routes(clean_world):
    old, new = clean_world.old_snapshot(), clean_world.new_snapshot()
    assert all(i in _by_id(new) for i in _by_id(old) if i.startswith(STRUCTURAL_KINDS))


def test_a_model_without_documents_is_present_in_both(clean_world):
    old, new = _by_id(clean_world.old_snapshot()), _by_id(clean_world.new_snapshot())
    assert "sldb://model/Move" in old and "sldb://model/Move" in new
    assert not any(e.relation_type == "has_document" for e in new["sldb://model/Move"].edges)


# --- parity of semantics ----------------------------------------------------------


def test_document_section_and_tag_semantics_are_identical(clean_world):
    old, new = clean_world.old_snapshot(), clean_world.new_snapshot()
    old_ids, new_ids = _by_id(old), _by_id(new)
    for node_id in sorted(i for i in old_ids if i.startswith(("sldb://document/", "sldb://section/", "sldb://semantic_tag/"))):
        assert _semantics(old_ids[node_id]) == _semantics(new_ids[node_id]), node_id


def test_store_and_model_nodes_carry_the_old_semantics_plus_documented_extras(clean_world):
    """The source route enriches two nodes the shards deliberately left thin: the store node
    (shards stated "the store node carries no path and no hash_a") and the model node ("hash_b
    is left out on purpose"). Every old key keeps its old value; the extras are additive."""
    old, new = clean_world.old_snapshot(), clean_world.new_snapshot()
    old_ids, new_ids = _by_id(old), _by_id(new)
    store_old, store_new = _semantics(old_ids["sldb://store"]), _semantics(new_ids["sldb://store"])
    assert store_old == {} and set(store_new) == {"root", "store_path", "hash_a"}
    for node_id in sorted(i for i in old_ids if i.startswith("sldb://model/")):
        o, n = _semantics(old_ids[node_id]), _semantics(new_ids[node_id])
        assert {k: o[k] for k in o} == {k: n[k] for k in o}, node_id
        assert set(n) - set(o) == {"hash_b"}, node_id


# --- parity of edges --------------------------------------------------------------


def test_the_six_structural_edges_are_identical(clean_world):
    old, new = clean_world.old_snapshot(), clean_world.new_snapshot()
    assert _triples(old, STRUCTURAL_RELATIONS) == _triples(new, STRUCTURAL_RELATIONS)


def test_structure_edge_metadata_difference_is_declared(clean_world):
    """Known difference, not a gap: the shard route stamps `{"origin": "structural"}` on its
    edges; the source route writes bare `{}`. The (source, relation, target) triples match."""
    old, new = clean_world.old_snapshot(), clean_world.new_snapshot()
    old_meta = {(n.identity.node_id, e.target_id, str(e.relation_type)): e.metadata for n in old.nodes for e in n.edges}
    new_meta = {(n.identity.node_id, e.target_id, str(e.relation_type)): e.metadata for n in new.nodes for e in n.edges}
    shared = set(old_meta) & set(new_meta)
    assert shared
    assert all(old_meta[k] == {"origin": "structural"} for k in shared)
    assert all(new_meta[k] == {} for k in shared)


# --- declared gaps ----------------------------------------------------------------


def test_gap_G1_field_nodes_and_edges_have_no_source_producer(relations_world):
    old, new = _by_id(relations_world.old_snapshot()), _by_id(relations_world.new_snapshot())
    old_edges = set(_triples(relations_world.old_snapshot()))
    new_edges = set(_triples(relations_world.new_snapshot()))
    assert {i for i in old if i.startswith("sldb://field/")}
    assert not {i for i in new if i.startswith("sldb://field/")}
    assert {t for t in old_edges if t[2] in ("has_field", "extends")}
    assert not {t for t in new_edges if t[2] in ("has_field", "extends")}


def test_gap_G2_typed_contribution_is_old_only_and_the_docs_appear_raw_in_new(relations_world):
    """The old layer re-types RelationTypeDoc/RelationDoc documents into relation_type/anchor
    nodes and authored edges. The source route has no typed producer yet: those documents
    surface as their raw `sldb://document/...` nodes instead (their sections and tags too)."""
    old, new = _by_id(relations_world.old_snapshot()), _by_id(relations_world.new_snapshot())
    old_edges, new_edges = set(_triples(relations_world.old_snapshot())), set(_triples(relations_world.new_snapshot()))
    old_typed = {i for i in old if i.startswith(("sldb://relation_type/", "sldb://anchor/"))}
    assert old_typed and not {i for i in new if i.startswith(("sldb://relation_type/", "sldb://anchor/"))}
    authored = {"relation_doc", "applies_to_source", "applies_to_target", "alias"}
    assert {t for t in old_edges if t[2] in authored}
    assert not {t for t in new_edges if t[2] in authored}
    # The raw materialization in the new route, declared as the G2 difference:
    materialized = {i for i in new if i.startswith(("sldb://document/RelationTypeDoc:", "sldb://document/RelationDoc:", "sldb://section/RelationTypeDoc:", "sldb://section/RelationDoc:"))}
    assert materialized and not {i for i in old if i.startswith(("sldb://document/RelationTypeDoc:", "sldb://document/RelationDoc:", "sldb://section/RelationTypeDoc:", "sldb://section/RelationDoc:"))}
    # The structural subset still matches around the G2 materializations:
    raw = {i for i in new if i.startswith(("sldb://document/RelationTypeDoc:", "sldb://document/RelationDoc:", "sldb://section/RelationTypeDoc:", "sldb://section/RelationDoc:", "sldb://model/RelationTypeDoc", "sldb://model/RelationDoc"))}
    assert _triples(relations_world.old_snapshot(), STRUCTURAL_RELATIONS) <= _triples(relations_world.new_snapshot(), STRUCTURAL_RELATIONS)
    extra = _triples(relations_world.new_snapshot(), STRUCTURAL_RELATIONS) - _triples(relations_world.old_snapshot(), STRUCTURAL_RELATIONS)
    assert {t for t in extra if t[0] in raw or t[1] in raw} == extra


def test_gap_G3_authored_edge_resolution_only_exists_in_the_old_route(relations_world):
    """The old compose resolves authored edges at read time (inherited condition/axis). The
    source route materializes no authored edge at all, so nothing to resolve: GAP G3."""
    old = relations_world.old_snapshot()
    authored = [(n.identity.node_id, e.target_id, str(e.relation_type), e.metadata) for n in old.nodes for e in n.edges if e.metadata.get("origin") == "relation_doc"]
    assert authored
    for _, _, _, meta in authored:
        assert "condition" in meta and "axis" in meta
    new = relations_world.new_snapshot()
    assert not any(e.metadata.get("origin") == "relation_doc" for n in new.nodes for e in n.edges)


# --- snapshot_save behaviour -----------------------------------------------------------


def test_snapshot_save_generates_from_the_source_indexes(clean_world, tmp_path):
    out = tmp_path / "graph.json"
    snapshot_save(clean_world.store, out, include_linked=False)
    loaded = _by_id(snapshot_load(out))
    reference = _by_id(clean_world.new_snapshot())
    assert set(loaded) == set(reference)
    assert all(_semantics(loaded[i]) == _semantics(reference[i]) for i in loaded)
    assert _triples(snapshot_load(out)) == _triples(clean_world.new_snapshot())
    # and the shard route's field nodes are gone from the saved graph (G1), not silently kept
    assert not any(i.startswith("sldb://field/") for i in loaded)


def test_snapshot_save_keeps_the_legacy_route_for_exclude_tags_gap_G6(clean_world, tmp_path):
    """GAP G6: no snapshot-side tag filter yet — when tags are excluded the old shard route
    still runs, and its result is byte-for-byte what `load_edge_index` composed."""
    out = tmp_path / "graph.json"
    snapshot_save(clean_world.store, out, include_linked=False, exclude_tags=["type.restaurant.table"])
    loaded = snapshot_load(out)
    legacy = clean_world.old_snapshot(exclude_tags=("type.restaurant.table",))
    assert set(_by_id(loaded)) == set(_by_id(legacy))
    assert _triples(loaded) == _triples(legacy)
    # the filter is real: excluded documents are not in the saved graph
    assert not any(i.startswith("sldb://document/Table:") for i in _by_id(loaded))
    # (the legacy route keeps its field nodes: that is GAP G1, not a parity regression)


def test_snapshot_save_keeps_the_legacy_route_for_linked_stores_gap_G5(clean_world, tmp_path):
    """GAP G5: no snapshot federation yet — a store with linked stores still composes them
    (ids qualified by the link's name) through the old route; `include_linked=False` stays
    on the source route and matches the unlinked shard composition."""
    linked = GraphWorld(tmp_path, name="linked")
    api.link_store(clean_world.store, linked.store, "bee")

    out = tmp_path / "with-links.json"
    snapshot_save(clean_world.store, out)  # include_linked defaults to True
    loaded = snapshot_load(out)
    legacy = snapshot_from_index(load_edge_index(clean_world.store, include_linked=True))
    assert set(_by_id(loaded)) == set(_by_id(legacy))
    assert _triples(loaded) == _triples(legacy)
    assert any(i.startswith("sldb://document/bee:") for i in _by_id(loaded))

    out_local = tmp_path / "local.json"
    snapshot_save(clean_world.store, out_local, include_linked=False)
    local = snapshot_load(out_local)
    assert not any(i.startswith("sldb://document/bee:") for i in _by_id(local))
    assert set(_by_id(local)) == set(_by_id(clean_world.new_snapshot()))
    assert _triples(local) == _triples(clean_world.new_snapshot())
