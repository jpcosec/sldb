"""`refs: [Model:name]` por elemento del spec -> referencias a documentos sldb, y aristas de átomos.

Portado de spec2viz (`tests/test_refs.py`, y `test_build_atoms_by_view_uses_store_scoped_payload`
de `tests/test_deskops.py`) contra `sldb.api.matching`. Donde spec2viz falseaba el store con
monkeypatch, aquí hay un store sldb real en el tmp de la prueba (conftest); por eso las aristas
de `TaskDoc:task-x` ya no son vacías: su campo `about` apunta a `AtomDoc:atom-y`.
No se portan los de modelos y schema (tarea de modelos de spec), los de la CLI del catálogo
(HTML, se quedan en spec2viz) ni el descubrimiento del store (la vista trae su `store`).
"""
from pathlib import Path

import pytest

import sldb.api
from sldb.api.matching import (
    STRUCTURAL_RELATIONS, SpecView, StoreReader, UnknownAtomError, attach_atom_edges, build_atoms_by_view, build_explicit_atoms,
    build_explicit_refs, collect_explicit_refs, store_documents,
)


def _view(store, refs=None, atoms=None):
    nodes = {"cli": {"label": "CLI", **({"refs": refs} if refs else {}), **({"atoms": atoms} if atoms else {})}, "core": {"label": "Core"}}
    spec = {"id": "arq", "title": "Arq", "type": "component", "version": "1.0", "data": {"nodes": nodes, "edges": []}}
    return SpecView(key="v1", id="v1", specs=[spec], store=store)


IN_FROM_TASK = {"relation": "references", "direction": "in", "node": "sldb://document/TaskDoc:task-x", "ref": "TaskDoc:task-x", "title": "Tarea X"}
OUT_TO_ATOM = {"relation": "references", "direction": "out", "node": "sldb://document/AtomDoc:atom-y", "ref": "AtomDoc:atom-y", "title": "Atomo Y"}


def test_collect_explicit_refs_indexes_by_label_and_id():
    assert collect_explicit_refs(_view(None, ["TaskDoc:task-x"])) == {"cli": ["TaskDoc:task-x"]}


def test_build_resolves_refs_with_title_path_and_summary(matching_store):
    payload, findings = build_explicit_refs([_view(matching_store, ["TaskDoc:task-x", "AtomDoc:atom-y"])])
    assert findings == []
    refs = payload["v1"]["cli"]
    assert [r["ref"] for r in refs] == ["TaskDoc:task-x", "AtomDoc:atom-y"]
    assert refs[0] == {
        "ref": "TaskDoc:task-x", "model": "TaskDoc", "name": "task-x", "title": "Tarea X",
        "path": str(matching_store.parent / "desk/tasks/task-x.md"), "store": str(matching_store), "summary": "Resumen de X",
        "edges": [OUT_TO_ATOM],
    }
    assert refs[1]["summary"] == "Respuesta Y"
    assert refs[1]["edges"] == [IN_FROM_TASK]


def test_unknown_ref_is_warning_unless_strict(matching_store):
    payload, findings = build_explicit_refs([_view(matching_store, ["TaskDoc:no-existe"])])
    assert payload == {}
    assert [(f.level, f.code) for f in findings] == [("warning", "matching/unknown-ref")]
    assert "no-existe" in findings[0].what
    with pytest.raises(UnknownAtomError) as raised:
        build_explicit_refs([_view(matching_store, ["TaskDoc:no-existe"])], strict=True)
    assert "no-existe" in str(raised.value)


def test_view_without_store_warns_per_ref():
    result, findings = build_explicit_refs([_view(None, ["TaskDoc:task-x"])])
    assert result == {}
    assert len(findings) == 1 and findings[0].code == "matching/no-store" and "sin store" in findings[0].what


def test_edges_of_keeps_declared_edges_both_ways_and_drops_structural(matching_store):
    raw = {e.relation for e in [*sldb.api.edges_from(matching_store, "AtomDoc:atom-y"), *sldb.api.edges_to(matching_store, "AtomDoc:atom-y")]}
    assert raw & STRUCTURAL_RELATIONS  # el indice si las tiene
    reader = StoreReader()
    edges = reader.edges_of(matching_store, "AtomDoc:atom-y")
    assert edges == [IN_FROM_TASK]
    assert reader.edges_of(matching_store, "AtomDoc:atom-y") is edges  # cache
    assert reader.findings == []


def test_edges_of_without_edge_index_warns_once_and_is_empty(tmp_path):
    reader = StoreReader()
    assert reader.edges_of(tmp_path / ".sldb", "AtomDoc:a") == []
    assert reader.edges_of(tmp_path / ".sldb", "AtomDoc:b") == []
    assert [f.code for f in reader.findings].count("matching/edges-unavailable") == 1


def test_edges_of_against_a_real_store(tmp_path):
    project = tmp_path / "proj"
    project.mkdir()
    sldb.api.init_store(project)
    sldb.api.init_relations(project / ".sldb")
    sldb.api.rebuild_edges(project / ".sldb")
    reader = StoreReader()
    # la relacion builtin `references` existe como documento, sin aristas declaradas: lista vacia, sin findings
    assert reader.edges_of(project / ".sldb", "RelationTypeDoc:references") == []
    assert reader.findings == []


def test_build_attaches_edges_to_explicit_atoms(matching_store):
    views = [_view(matching_store, atoms=["atom-y"])]
    reader = StoreReader()
    raw, _ = build_atoms_by_view(views, reader=reader)
    explicit, _complete, _findings, linked = build_explicit_atoms(views, raw)
    attach_atom_edges(views, explicit, linked, reader, raw)
    atom = explicit["v1"]["cli"]["list"][0]
    assert atom["id"] == "atom-y" and atom["edges"] == [IN_FROM_TASK]


def test_store_documents_come_from_sldb_api(tmp_path, store_factory):
    atom = {"name": "atom-a", "id": "atom-a", "title": "Alpha", "five_wh_one_plus": "what", "tags": ["x:y"], "answer": "Cuerpo"}
    store = store_factory(tmp_path / "proj", [atom], [])
    other = store_factory(tmp_path / "other", [], [{"name": "task-b", "title": "Beta"}])
    sldb.api.link_store(store, other, "desk")

    docs = {d["ref"]: d for d in store_documents(store)}
    assert {"AtomDoc:atom-a", "desk:TaskDoc:task-b"} <= set(docs)
    assert docs["AtomDoc:atom-a"]["path"] == str(tmp_path / "proj/desk/atoms/atom-a.md")
    assert docs["desk:TaskDoc:task-b"]["path"] == str(tmp_path / "other/desk/tasks/task-b.md")

    reader = StoreReader()
    payload = reader.atoms(store)
    assert list(payload) == ["alpha"]
    assert payload["alpha"]["atoms"]["what"]["id"] == "atom-a"
    assert payload["alpha"]["atoms"]["what"]["tags"] == ["x:y"]
    assert reader.resolve_ref(store, "desk:TaskDoc:task-b")["title"] == "Beta"
    assert reader.resolve_ref(store, "TaskDoc:nope") is None


def test_build_atoms_by_view_uses_store_scoped_payload(matching_store):
    atoms_by_view, findings = build_atoms_by_view([SpecView(key="view-1", id="view-1", store=matching_store)])
    assert findings == []
    assert list(atoms_by_view) == ["view-1"]
    entry = atoms_by_view["view-1"]["atomo y"]
    assert entry["title"] == "Atomo Y" and "atomo" in entry["aliases"] and "oc" in entry["aliases"]
    assert entry["atoms"]["what"]["id"] == "atom-y" and entry["atoms"]["what"]["body"] == "Respuesta Y"
