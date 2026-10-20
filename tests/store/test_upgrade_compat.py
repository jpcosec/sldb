"""Upgrading sldb must not fail a store whose content did not change.

Two upgrades did (Governance's pulse went red on them): the contract hash began signing class
metadata (cecd97b), and a builtin relation type (`composes`) was added after stores had run
`edges init`. Both are reported, not failed; a real change still fails.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb.api import add_model, check_edges, init_relations, init_store, rebuild_edges, resolve_model_ref, track_document_file, untrack_document, update_store_indexes
from sldb.runtime.validation import render_model_markdown
from sldb.store.diagnostics import diagnose_store
from sldb.store.hashing import hash_model_contract, hash_model_layer, hash_models_layer
from sldb.store.io import invalidate_index_cache, load_models_index, load_store_index, save_models_index, save_store_index
from sldb.store.layout import project_root
from sldb.store.legacy_contract import legacy_contract_hash
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_upgrade_compat_models"
_NOTE = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __family__ = "notes"
    __template__ = """# ⸢rev•title⸥""".strip()
    title: str = Field(description="Note title.")
'''
_NOTE_WITH_STATUS = _NOTE.replace('    title: str', '    status: str = Field(default="open", description="Note state.")\n    title: str')


def _write_module(tmp_path: Path, source: str) -> None:
    (tmp_path / f"{MODULE}.py").write_text(source, encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_index_cache()
    invalidate_runtime_cache()


@pytest.fixture
def store(tmp_path: Path):
    _write_module(tmp_path, _NOTE)
    root = tmp_path / "repo"
    root.mkdir()
    sp = init_store(root).store_path
    add_model(sp, f"{MODULE}:NoteDoc", str(tmp_path))
    model_type = resolve_model_ref(f"{MODULE}:NoteDoc", str(tmp_path))
    (root / "note.md").write_text(render_model_markdown(model_type, {"title": "A note"}) + "\n", encoding="utf-8")
    track_document_file(sp, "NoteDoc", root / "note.md", "note", str(tmp_path))
    yield sp
    sys.modules.pop(MODULE, None)


def _seal_with_legacy_contract(sp: Path, pythonpath: str) -> None:
    """Rewrite the store as sldb wrote it before cecd97b: contract over fields and template only."""
    idx = load_store_index(sp)
    path = project_root(sp) / idx.models[0].models_index
    m_idx = load_models_index(path)
    m_idx.contract_hash = legacy_contract_hash(resolve_model_ref(f"{MODULE}:NoteDoc", pythonpath))
    m_idx.model_hash = hash_model_layer(m_idx.roster_hash, m_idx.contract_hash)
    save_models_index(path, m_idx)
    idx.store_hash = hash_models_layer([m_idx])
    save_store_index(sp, idx)
    invalidate_index_cache()


def _diagnose(sp: Path, pythonpath: str):
    return diagnose_store(sp, resolve_model_ref, project_root(sp), pythonpath=pythonpath)


def test_a_legacy_contract_hash_of_an_unchanged_class_passes_and_is_named(store, tmp_path):
    _seal_with_legacy_contract(store, str(tmp_path))
    diagnosis = _diagnose(store, str(tmp_path))
    assert diagnosis.is_valid
    assert diagnosis.models[0].legacy_contract
    assert "cecd97b" in diagnosis.models[0].explain()


def test_stores_update_reseals_a_legacy_contract(store, tmp_path):
    _seal_with_legacy_contract(store, str(tmp_path))
    update_store_indexes(store, str(tmp_path))
    invalidate_index_cache()
    model = _diagnose(store, str(tmp_path)).models[0]
    assert model.contract_ok and not model.legacy_contract
    m_idx = load_models_index(project_root(store) / load_store_index(store).models[0].models_index)
    assert m_idx.contract_hash == hash_model_contract(resolve_model_ref(f"{MODULE}:NoteDoc", str(tmp_path)))


def test_a_legacy_hash_does_not_excuse_a_class_that_changed(store, tmp_path):
    _seal_with_legacy_contract(store, str(tmp_path))
    _write_module(tmp_path, _NOTE_WITH_STATUS)
    diagnosis = _diagnose(store, str(tmp_path))
    assert diagnosis.is_valid, "a moved contract is an alert"
    assert not diagnosis.models[0].contract_ok and not diagnosis.models[0].legacy_contract


def test_a_builtin_newer_than_edges_init_is_noted_not_failed(store, tmp_path):
    init_relations(store, str(tmp_path))
    untrack_document(store, "reltype-has_section", str(tmp_path))
    rebuild_edges(store, str(tmp_path))
    report = check_edges(store, include_linked=False)
    assert report.ok, report.errors
    assert report.untracked_builtins == ["has_section"]


def test_a_store_that_never_ran_edges_init_still_fails(store, tmp_path):
    rebuild_edges(store, str(tmp_path))
    report = check_edges(store, include_linked=False)
    assert not report.ok and any("unknown relation type" in e for e in report.errors)
    assert report.untracked_builtins == []
