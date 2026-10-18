"""A model is defined once, in the store that owns it; another store inherits it.

The store of a repo that uses deskops' models used to register a copy of each, pinned to the
absolute path of its source and imported only with the right `--pythonpath`. When deskops moved,
every copy in every store broke. An inherited entry keeps no source path: the class imports from
the owner's project root, and what stays local is the store's own roster and signed contract.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
import yaml

from sldb.api import add_model, check_store, inherit_model, init_store, link_store, track_document_file
from sldb.core.exceptions import SLDBModelError
from sldb.store.diagnostics import diagnose_store
from sldb.store.io import invalidate_index_cache, load_store_index
from sldb.store.io.shards import load_edges_shard
from sldb.store.layout import edges_store_shard_path
from sldb.store.model_origin import shadowed_models
from sldb.store.models import EdgeContribution
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_inherit_owner_models"
_OWNER = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥"""
    title: str = Field(description="Note title.")
'''


def _forget_module(owner: Path) -> None:
    """As a fresh process would be: the owner's module neither imported nor on sys.path."""
    sys.modules.pop(MODULE, None)
    while str(owner.resolve()) in sys.path:
        sys.path.remove(str(owner.resolve()))
    invalidate_index_cache()
    invalidate_runtime_cache()


@pytest.fixture
def stores(tmp_path):
    owner, local = tmp_path / "deskops", tmp_path / "repo"
    owner.mkdir(), local.mkdir()
    (owner / f"{MODULE}.py").write_text(_OWNER, encoding="utf-8")
    owner_sp, local_sp = init_store(owner).store_path, init_store(local).store_path
    add_model(owner_sp, f"{MODULE}:NoteDoc", str(owner))
    link_store(local_sp, owner_sp, "deskops")
    (local / "note.md").write_text("# A note\n", encoding="utf-8")
    yield owner, local, local_sp
    _forget_module(owner)


def _entry(sp: Path, name: str = "NoteDoc"):
    return next(m for m in load_store_index(sp).models if m.name == name)


def test_a_copy_becomes_inherited_and_imports_from_its_owner(stores):
    owner, local, sp = stores
    add_model(sp, f"{MODULE}:NoteDoc", str(owner))           # the copy deskops init used to make
    track_document_file(sp, "NoteDoc", local / "note.md", "note", str(owner))
    assert shadowed_models(sp) == [{"model": "NoteDoc", "store": "deskops", "copy": True}]

    inherit_model(sp, "deskops:NoteDoc")

    entry = _entry(sp)
    assert entry.origin == "deskops" and entry.path == ""
    assert shadowed_models(sp) == []
    _forget_module(owner)
    report = check_store(sp, local)                           # no pythonpath: the link says where
    assert report["valid"] and report["checked"] == 1
    assert diagnose_store(sp, __import__("sldb.api", fromlist=["resolve_model_ref"]).resolve_model_ref, local).models[0].resolved


def test_inheriting_needs_no_copy_and_no_pythonpath(stores):
    owner, local, sp = stores
    _forget_module(owner)
    inherit_model(sp, "deskops:NoteDoc")
    track_document_file(sp, "NoteDoc", local / "note.md", "note")
    assert _entry(sp).origin == "deskops"
    assert check_store(sp, local)["valid"]


def test_the_first_use_of_alias_model_registers_it_inherited(stores):
    owner, local, sp = stores
    track_document_file(sp, "deskops:NoteDoc", local / "note.md", "note", str(owner))
    assert _entry(sp).origin == "deskops" and _entry(sp).path == ""


def test_another_class_under_the_owners_name_is_an_override_not_a_copy(stores, tmp_path):
    owner, local, sp = stores
    (local / "mine.py").write_text(_OWNER, encoding="utf-8")
    add_model(sp, "mine:NoteDoc", str(local))
    assert shadowed_models(sp) == [{"model": "NoteDoc", "store": "deskops", "copy": False}]
    with pytest.raises(SLDBModelError, match="override"):
        inherit_model(sp, "deskops:NoteDoc")
    sys.modules.pop("mine", None)


def test_the_store_keeps_working_while_the_owner_is_away(stores, tmp_path):
    owner, local, sp = stores
    inherit_model(sp, "deskops:NoteDoc")
    track_document_file(sp, "NoteDoc", local / "note.md", "note")
    owner.rename(tmp_path / "moved-away")
    _forget_module(owner)
    report = check_store(sp, local)
    assert report["valid"], "the roster and the contract it signed are the store's own"


def test_the_graph_shows_the_link_and_where_a_model_comes_from(stores):
    owner, local, sp = stores
    inherit_model(sp, "deskops:NoteDoc")
    shard = load_edges_shard(edges_store_shard_path(sp), EdgeContribution)
    edges = {(e.relation, e.target): e.metadata for e in shard.edges}
    assert ("links_to", "sldb://store/deskops") in edges
    assert edges[("has_model", "sldb://model/NoteDoc")]["origin_store"] == "deskops"


def test_a_store_that_owns_its_models_writes_no_origin_key(stores):
    owner, local, sp = stores
    raw = yaml.safe_load((owner / ".sldb" / "core" / "store_index.yaml").read_text(encoding="utf-8"))
    assert all("origin" not in m for m in raw["models"])


def test_sldbs_own_models_are_nobodys_to_inherit(stores):
    owner, local, sp = stores
    ref = "sldb.models.relation_doc:RelationDoc"
    add_model(owner / ".sldb", ref), add_model(sp, ref)
    assert shadowed_models(sp) == []


def test_a_shared_model_is_one_fact_in_the_federated_edge_check(stores):
    """Both stores emit the inherited model's node and fields; the same edge from two stores
    is one edge, and two stores registering one model is what `has_model` now allows."""
    from sldb.api import check_edges, init_relations

    owner, local, sp = stores
    init_relations(owner / ".sldb", str(owner)), init_relations(sp)
    inherit_model(sp, "deskops:NoteDoc")
    track_document_file(sp, "NoteDoc", local / "note.md", "note")
    report = check_edges(sp)
    assert report.errors == [], report.errors


def test_edges_init_rewrites_an_outdated_builtin_and_leaves_an_authored_namesake(stores):
    from sldb.api import init_relations

    owner, local, sp = stores
    init_relations(sp)
    has_model = local / "sldb" / "relation_types" / "has_model.md"
    has_model.write_text(has_model.read_text(encoding="utf-8").replace("many_to_many", "one_to_many"), encoding="utf-8")
    report = init_relations(sp)
    assert report.types_updated == ["has_model"] and "many_to_many" in has_model.read_text(encoding="utf-8")
    assert init_relations(sp).types_updated == []
    assert check_store(sp, local)["valid"]


def test_a_copy_registered_by_a_reexporting_module_is_still_a_copy(stores):
    """graph_ui registered `deskops.models.atom:AtomDoc`; deskops owns `deskops.models:AtomDoc`,
    which re-exports the same class. Comparing strings called it an override."""
    owner, local, sp = stores
    (owner / "sldb_inherit_reexport.py").write_text(f"from {MODULE} import NoteDoc  # noqa: F401\n", encoding="utf-8")
    add_model(sp, "sldb_inherit_reexport:NoteDoc", str(owner))
    assert shadowed_models(sp, lambda a, b: a == b)[0]["copy"] is False
    inherit_model(sp, "deskops:NoteDoc")
    assert _entry(sp).origin == "deskops" and _entry(sp).model_ref == f"{MODULE}:NoteDoc"
    sys.modules.pop("sldb_inherit_reexport", None)
