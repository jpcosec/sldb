"""`sldb.api` edge index: per-document shards on the hash chain, read through one door.

Covers: every write keeps its own shard current and touches no other document's; an untracked
document loses its shard; relation types, relations and anchors become nodes and edges, not
document nodes; cross-document rules (inherited condition and axis, reverse edges, orphans)
apply on read and are reported, not stored; `exclude_tags` is the reader's; a linked store's
documents come back qualified by the link's name; `init_relations` is idempotent.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.store.layout import edges_model_shard_path, edges_shard_path, edges_store_shard_path

MODULE = "sldb_edges_test_models"
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


class Alias(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "anchor"]}
    __template__ = "# ⸢rev•symbol⸥\\n\\nRef: ⸢rev•ref⸥"
    symbol: str = Field(description="Word.")
    ref: str = Field(description="What it names.")
'''


class EdgeWorld:
    """A store prepared for relations, with the models above registered."""

    def __init__(self, base: Path, name: str = "world") -> None:
        self.root, self.py = base / name, str(base)
        self.root.mkdir()
        self.store = api.init_store(self.root).store_path
        for model in ("Table", "Booking", "Move", "Alias"):
            api.add_model(self.store, f"{MODULE}:{model}", self.py)
        api.init_relations(self.store, self.py)

    def create(self, model: str, name: str, payload: dict) -> None:
        api.create_document(self.store, model, self.root / f"{name}.md", payload, name, self.py)

    def relation_type(self, name: str, source: list[str], target: list[str], **extra) -> None:
        payload = {"title": name, "name": name, "direction": "directed", "cardinality": "many_to_many", "axis": "WHERE", "source_types": source, "target_types": target, "condition": "", "description": f"{name}."}
        self.create("RelationTypeDoc", f"rt-{name}", {**payload, **extra})

    def relation(self, name: str, src: str, tgt: str, rtype: str, condition: str = "") -> None:
        self.create("RelationDoc", name, {"title": name, "source_id": src, "target_id": tgt, "relation_type": rtype, "condition": condition, "notes": ""})


@pytest.fixture
def world(tmp_path: Path) -> EdgeWorld:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    w = EdgeWorld(tmp_path)
    w.create("Table", "t12", {"title": "Table 12", "capacity": 6, "notes": "By the window."})
    w.create("Table", "t14", {"title": "Table 14", "capacity": 8, "notes": ""})
    w.create("Booking", "b1", {"title": "Ana", "party_size": 6})
    w.relation_type("assigned_to", ["Booking"], ["Table"], cardinality="many_to_one", condition="capacity >= {party_size}")
    w.relation("b1-t12", "Booking:b1", "Table:t12", "assigned_to")
    return w


def _pairs(edges) -> list[tuple[str, str]]:
    return [(e.target, e.relation) for e in edges]


def test_a_write_leaves_a_shard_per_document_model_and_store(world: EdgeWorld):
    assert edges_shard_path(world.store, "Table", "t12").exists()
    assert edges_model_shard_path(world.store, "Table").exists()
    assert edges_store_shard_path(world.store).exists()
    assert api.load_edge_index(world.store).stale == []


def test_structural_edges_and_typed_nodes(world: EdgeWorld):
    assert ("sldb://document/Table:t12", "has_document") in _pairs(api.edges_from(world.store, "sldb://model/Table"))
    assert ("sldb://section/Table:t12#table-12/notes", "has_section") in _pairs(api.edges_from(world.store, "Table:t12"))
    assert ("sldb://semantic_tag/type.restaurant.table", "tagged_as") in _pairs(api.edges_from(world.store, "Table:t12", "tagged_as"))
    assert api.edge_node(world.store, "Table:t12").node_type == "Table"
    assert [n.id for n in api.edge_nodes_of_type(world.store, "Booking")] == ["sldb://document/Booking:b1"]
    field = api.edge_node(world.store, "sldb://field/Table.capacity")
    assert field.node_type == "sldb_field" and field.semantics["kind"] == "integer"
    assert [e.source for e in api.edges_to(world.store, "sldb://model/Table", "has_model")] == ["sldb://store"]


def test_a_relation_doc_is_an_edge_that_inherits_from_its_type(world: EdgeWorld):
    [edge] = api.edges_from(world.store, "Booking:b1", "assigned_to")
    assert (edge.source, edge.target) == ("sldb://document/Booking:b1", "sldb://document/Table:t12")
    assert edge.metadata == {"origin": "relation_doc", "relation_doc": "b1-t12", "condition": "capacity >= {party_size}", "axis": "WHERE"}
    assert api.edges_to(world.store, "Table:t12", "assigned_to") == [edge]
    assert api.edge_node(world.store, "RelationDoc:b1-t12") is None
    applies = api.edges_from(world.store, "sldb://relation_type/assigned_to")
    assert _pairs(applies) == [("sldb://model/Booking", "applies_to_source"), ("sldb://model/Table", "applies_to_target")]
    assert api.check_edges(world.store).ok


def test_editing_one_document_rewrites_only_its_shard(world: EdgeWorld):
    shards = {name: edges_shard_path(world.store, model, name) for model, name in (("Table", "t12"), ("Table", "t14"), ("Booking", "b1"), ("RelationDoc", "b1-t12"))}
    before = {name: path.stat().st_mtime_ns for name, path in shards.items()}
    old_hash = api.edge_node(world.store, "Table:t14").semantics["hash_c"]
    api.save_document_payload(world.store, "Table", "t14", {"title": "Table 14", "capacity": 10, "notes": ""}, world.py)
    after = {name: path.stat().st_mtime_ns for name, path in shards.items()}
    assert [name for name in shards if before[name] != after[name]] == ["t14"]
    assert api.edge_node(world.store, "Table:t14").semantics["hash_c"] not in ("", old_hash)
    assert api.load_edge_index(world.store).stale == []
    assert api.rebuild_edges(world.store, world.py).docs_written == 0


def test_untracking_a_document_drops_its_shard_and_reports_the_orphan(world: EdgeWorld):
    api.untrack_document(world.store, "t12", world.py)
    assert not edges_shard_path(world.store, "Table", "t12").exists()
    assert api.edge_node(world.store, "Table:t12") is None
    assert api.edges_from(world.store, "Booking:b1", "assigned_to") == []
    assert api.check_edges(world.store).errors == ["relation 'b1-t12': target 'Table:t12' is not a tracked document"]


def test_undirected_types_read_both_ways_and_bad_classes_are_reported(world: EdgeWorld):
    world.relation_type("near", ["Table"], ["Table"], direction="undirected")
    world.relation("t12-t14", "Table:t12", "Table:t14", "near")
    [back] = api.edges_from(world.store, "Table:t14", "near")
    assert back.target == "sldb://document/Table:t12" and back.metadata["reverse"] is True
    world.relation("b1-near", "Booking:b1", "Table:t14", "near")
    errors = api.check_edges(world.store).errors
    assert any("source class 'Booking' not in source_types ['Table']" in e for e in errors)


def test_exclude_tags_is_the_readers_choice(world: EdgeWorld):
    world.create("Move", "m1", {"title": "a move"})
    assert api.edge_node(world.store, "Move:m1") is not None
    hidden = api.load_edge_index(world.store, exclude_tags=["type.pron.move"])
    assert hidden.node("Move:m1") is None
    assert hidden.edges_from("sldb://model/Move", "has_document") == []
    assert hidden.node("sldb://semantic_tag/type.pron.move") is not None


def test_anchors_name_what_their_ref_points_at(world: EdgeWorld):
    world.create("Alias", "mesa", {"symbol": "mesa", "ref": "model:Table"})
    world.create("Alias", "cupo", {"symbol": "cupo", "ref": "(field Table capacity)"})
    assert _pairs(api.edges_from(world.store, "sldb://anchor/mesa")) == [("sldb://model/Table", "names")]
    assert _pairs(api.edges_from(world.store, "sldb://anchor/cupo")) == [("sldb://field/Table.capacity", "names")]
    assert api.edge_node(world.store, "Alias:mesa") is None


def test_linked_store_documents_come_back_qualified(world: EdgeWorld, tmp_path: Path):
    other = EdgeWorld(tmp_path, "other")
    other.create("Table", "t99", {"title": "Table 99", "capacity": 2, "notes": ""})
    api.link_store(world.store, other.store, "annex")
    world.relation("b1-t99", "Booking:b1", "annex:Table:t99", "assigned_to")
    index = api.load_edge_index(world.store)
    assert index.node("annex:Table:t99").semantics["store"] == "annex"
    assert "sldb://document/annex:Table:t99" in [e.target for e in index.edges_from("sldb://model/Table", "has_document")]
    assert [e.target for e in index.edges_from("Booking:b1", "assigned_to")] == ["sldb://document/Table:t12", "sldb://document/annex:Table:t99"]
    assert api.load_edge_index(world.store, include_linked=False).node("annex:Table:t99") is None


def test_init_relations_is_idempotent(world: EdgeWorld):
    report = api.init_relations(world.store, world.py)
    assert (report.models_added, report.types_written, report.predicates_added) == ([], [], [])
    assert (world.root / "sldb" / "relation_types" / "tagged_as.md").exists()
    assert "sldb://relation_type/has_document" in [n.id for n in api.edge_nodes_of_type(world.store, "relation_type")]


def test_cli_edges_uses_the_api(world: EdgeWorld, capsys):
    from sldb.cli import main as cli_main

    assert cli_main(["edges", "show", "Booking:b1", "--relation", "assigned_to", "--store", str(world.store)]) == 0
    assert '"target": "sldb://document/Table:t12"' in capsys.readouterr().out
    assert cli_main(["edges", "check", "--store", str(world.store)]) == 0
    assert cli_main(["edges", "rebuild", "--store", str(world.store), "--pythonpath", world.py]) == 0
    assert "0 shard(s) written" in capsys.readouterr().out
    world.relation("orphan", "Booking:b1", "Table:nowhere", "assigned_to")
    assert cli_main(["edges", "check", "--store", str(world.store)]) == 1
    assert cli_main(["help", "edges"]) == 0


def test_a_hand_edit_reaches_the_index_through_stores_update(world: EdgeWorld):
    others = {name: edges_shard_path(world.store, "Table", name).stat().st_mtime_ns for name in ("t14",)}
    old_hash = api.edge_node(world.store, "Table:t12").semantics["hash_c"]
    path = world.root / "t12.md"
    path.write_text(path.read_text(encoding="utf-8").replace("By the window.", "By the door."), encoding="utf-8")
    assert api.update_store_indexes(world.store, world.py).complete
    assert api.edge_node(world.store, "Table:t12").semantics["hash_c"] != old_hash
    assert edges_shard_path(world.store, "Table", "t14").stat().st_mtime_ns == others["t14"]
    assert api.load_edge_index(world.store).stale == []


def test_a_wiped_index_reads_as_stale_and_rebuild_brings_it_back(world: EdgeWorld):
    import shutil

    before = api.load_edge_index(world.store)
    shutil.rmtree(world.store / "runtime" / "edges")
    wiped = api.load_edge_index(world.store)
    assert "Table:t12" in wiped.stale and wiped.node("Table:t12") is None
    assert api.rebuild_edges(world.store, world.py).docs_written == len(wiped.stale)
    rebuilt = api.load_edge_index(world.store)
    assert rebuilt.stale == [] and rebuilt.nodes == before.nodes and rebuilt.edges == before.edges
    edges_shard_path(world.store, "Table", "t14").unlink()  # one shard lost, its model's cache key intact
    assert api.load_edge_index(world.store).stale == ["Table:t14"]
    assert api.rebuild_edges(world.store, world.py).docs_written == 1
    assert api.load_edge_index(world.store).nodes == before.nodes
