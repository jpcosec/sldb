"""Writing the semantic DAG: a parent beyond what the name says, an equivalence, and the guards.

The point is the round trip. A parent declared here has to show up everywhere the DAG is read:
`se.` navigation and closure, `sldb graph`, the journal, and it must survive the rebuild that
re-derives the name's own parents.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.api import semantic as sem
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBStoreError
from sldb.store.query import get_semantic
from sldb.store.semantic import rebuild_semantic_indexes

MODULE = "sldb_semantic_write_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Spec(StructuredNLDoc):
    __semantics__ = {"type": ["knowledge", "spec"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class Topology(StructuredNLDoc):
    __semantics__ = {"layer": ["topology"]}
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


@pytest.fixture
def world(tmp_path: Path) -> tuple[Path, str]:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root, py = tmp_path / "world", str(tmp_path)
    root.mkdir()
    store = api.init_store(root).store_path
    for model in ("Spec", "Topology"):
        api.add_model(store, f"{MODULE}:{model}", py)
    api.create_document(store, "Spec", root / "s1.md", {"title": "S1"}, "s1", py)
    api.create_document(store, "Topology", root / "t1.md", {"title": "T1"}, "t1", py)
    return store, py


def _resolve(py: str):
    return lambda ref, pythonpath=None: api.resolve_model_ref(ref, py)


def test_a_declared_parent_is_read_by_the_closure_by_the_graph_and_by_the_journal(world):
    store, py = world
    assert get_semantic(store, "se.type.knowledge", _resolve(py)) == ["st.{Spec}.s1"]
    assert sem.add_semantic_parent(store, "layer.topology", "type.knowledge", actor="test") is True
    assert get_semantic(store, "se.type.knowledge", _resolve(py)) == ["st.{Spec}.s1", "st.{Topology}.t1"]
    parents = [e.target for e in api.edges_from(store, "sldb://semantic_tag/layer.topology", "semantic_parent")]
    assert "sldb://semantic_tag/type.knowledge" in parents
    entry = api.journal(store, limit=1)[0]
    assert (entry.operation, entry.address, entry.new_value, entry.actor) == ("add_semantic_parent", "se.layer.topology", "type.knowledge", "test")


def test_declaring_it_twice_changes_nothing_and_journals_nothing(world):
    store, _ = world
    sem.add_semantic_parent(store, "layer.topology", "type.knowledge")
    count = len(api.journal(store))
    assert sem.add_semantic_parent(store, "layer.topology", "type.knowledge") is False
    assert len(api.journal(store)) == count


def test_a_declared_parent_survives_the_rebuild_that_rederives_the_names(world):
    store, py = world
    sem.add_semantic_parent(store, "layer.topology", "type.knowledge")
    api.create_document(store, "Topology", store.parent / "t2.md", {"title": "T2"}, "t2", py)
    rebuild_semantic_indexes(store, store.parent, api.resolve_model_ref, py)
    assert sem.semantic_tag(store, "layer.topology")["parents"] == ["layer", "type.knowledge"]


def test_the_guards_unknown_tags_cycles_and_parents_the_name_implies(world):
    store, _ = world
    with pytest.raises(SLDBStoreError, match="Unknown semantic tag 'nope'"):
        sem.add_semantic_parent(store, "nope", "type")
    with pytest.raises(SLDBStoreError, match="Unknown semantic tag 'nope'"):
        sem.add_semantic_parent(store, "layer.topology", "nope")
    with pytest.raises(SLDBStoreError, match="'type.knowledge' is already a kind of 'type'"):
        sem.add_semantic_parent(store, "type", "type.knowledge")
    with pytest.raises(SLDBStoreError, match="kind of itself"):
        sem.add_semantic_parent(store, "type", "type")
    with pytest.raises(SLDBStoreError, match="gets from its own name"):
        sem.remove_semantic_parent(store, "type.knowledge", "type")


def test_removing_a_declared_parent_takes_it_out_of_the_closure(world):
    store, py = world
    sem.add_semantic_parent(store, "layer.topology", "type.knowledge")
    assert sem.remove_semantic_parent(store, "layer.topology", "type.knowledge") is True
    assert get_semantic(store, "se.type.knowledge", _resolve(py)) == ["st.{Spec}.s1"]
    assert sem.remove_semantic_parent(store, "layer.topology", "type.knowledge") is False


def test_an_equivalence_finally_has_a_way_in(world):
    store, _ = world
    assert sem.add_semantic_equivalence(store, "type.knowledge.spec", "global.spec") is True
    assert sem.add_semantic_equivalence(store, "type.knowledge.spec", "global.spec") is False
    assert sem.semantic_tag(store, "type.knowledge.spec")["equivalents"] == ["global.spec"]


def test_show_reports_both_directions(world):
    store, _ = world
    sem.add_semantic_parent(store, "layer.topology", "type.knowledge")
    shown = sem.semantic_tag(store, "type.knowledge")
    assert shown["parents"] == ["type"]
    assert "layer.topology" in shown["children"] and "type.knowledge.spec" in shown["below"]
    assert sem.semantic_tag(store, "layer.topology")["above"] == ["layer", "type", "type.knowledge"]


def test_the_cli_writes_refuses_and_shows(world, capsys):
    store, _ = world
    assert cli_main(["semantic", "parent", "add", "layer.topology", "type.knowledge", "--store", str(store)]) == 0
    assert "is now a kind of" in capsys.readouterr().out
    assert cli_main(["semantic", "parent", "add", "type", "type.knowledge", "--store", str(store)]) == 1
    assert "already a kind of" in capsys.readouterr().out
    assert cli_main(["semantic", "show", "layer.topology", "--store", str(store)]) == 0
    assert '"type.knowledge"' in capsys.readouterr().out
