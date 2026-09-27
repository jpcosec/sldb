"""A model's contract is part of its node: changing it moves the tree and is attributable.

The gap this closes: `stores update` only re-extracts documents whose `source_hash` moved. A
field added to the class, or a changed `__template__`, changes what extraction yields from
text that did not move — so nothing used to signal it, and `content_hash` stayed stale.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from pydantic import Field

from sldb import StructuredNLDoc
from sldb.api import add_model, init_store, resolve_model_ref, store_fingerprint, track_document_file, update_store_indexes
from sldb.api.stores.store_check import check_store
from sldb.runtime.validation import render_model_markdown
from sldb.store.hashing import hash_model_contract, hash_model_layer
from sldb.store.io import invalidate_index_cache, load_models_index, load_store_index
from sldb.store.layout import project_root
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_contract_test_models"

_ONE_FIELD = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥""".strip()
    title: str = Field(description="Note title.")
'''

# Same title field, same text on disk, but a second field the template now also reads.
_TWO_FIELDS = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

Status: ⸢rev•status⸥""".strip()
    title: str = Field(description="Note title.")
    status: str = Field(default="open", description="Note state.")
'''


class _Store:
    def __init__(self, root: Path, pythonpath: str) -> None:
        self.root, self.store, self.pythonpath = root, root / ".sldb", pythonpath


def _write_module(tmp_path: Path, source: str) -> None:
    (tmp_path / f"{MODULE}.py").write_text(source, encoding="utf-8")
    for name in (MODULE, f"{MODULE}__draft__"):
        sys.modules.pop(name, None)
    invalidate_index_cache()
    invalidate_runtime_cache()


@pytest.fixture
def contract_store(tmp_path: Path):
    _write_module(tmp_path, _ONE_FIELD)
    root = tmp_path / "repo"
    root.mkdir()
    init_store(root)
    store = _Store(root, str(tmp_path))
    add_model(store.store, f"{MODULE}:NoteDoc", store.pythonpath)
    model_type = resolve_model_ref(f"{MODULE}:NoteDoc", store.pythonpath)
    path = root / "note.md"
    path.write_text(render_model_markdown(model_type, {"title": "A note"}) + "\n", encoding="utf-8")
    track_document_file(store.store, "NoteDoc", path, "note", store.pythonpath)
    yield store
    sys.modules.pop(MODULE, None)


def _model_index(store: _Store):
    idx = load_store_index(store.store)
    return load_models_index(project_root(store.store) / idx.models[0].models_index)


def test_model_node_is_its_two_children(contract_store):
    m_idx = _model_index(contract_store)
    assert m_idx.roster_hash and m_idx.contract_hash
    assert m_idx.model_hash == hash_model_layer(m_idx.roster_hash, m_idx.contract_hash)


def test_contract_hash_records_the_registered_class(contract_store):
    model_type = resolve_model_ref(f"{MODULE}:NoteDoc", contract_store.pythonpath)
    assert _model_index(contract_store).contract_hash == hash_model_contract(model_type)


def test_a_moved_contract_is_reported_as_its_own_category(contract_store, tmp_path):
    """The store is untouched; only the class changed. The check must say so, and must not
    accuse the document, whose text is exactly what it was."""
    _write_module(tmp_path, _TWO_FIELDS)
    report = check_store(contract_store.store, project_root(contract_store.store), contract_store.pythonpath)
    assert not report["valid"]
    assert report["damaged"] == [], "the document's text never moved"
    from sldb.store.diagnostics import diagnose_store
    diagnosis = diagnose_store(contract_store.store, resolve_model_ref, project_root(contract_store.store), pythonpath=contract_store.pythonpath)
    assert not diagnosis.models[0].contract_ok
    assert "contract" in diagnosis.models[0].explain()


def test_a_moved_contract_moves_the_root(contract_store, tmp_path):
    before = store_fingerprint(contract_store.store)
    _write_module(tmp_path, _TWO_FIELDS)
    update_store_indexes(contract_store.store, contract_store.pythonpath)
    after = store_fingerprint(contract_store.store)
    assert after.store_hash != before.store_hash, "a template change must move the Merkle root"
    assert after.models["NoteDoc"] != before.models["NoteDoc"]


def test_update_re_extracts_documents_whose_text_did_not_move(contract_store, tmp_path):
    """The bug this closes: the new field must reach `content_hash` even though `source_hash`
    is identical, because no rewrite of the Markdown ever happened."""
    before = store_fingerprint(contract_store.store)
    _write_module(tmp_path, _TWO_FIELDS)
    update_store_indexes(contract_store.store, contract_store.pythonpath)
    after = store_fingerprint(contract_store.store)
    assert after.documents["NoteDoc:note"].source_hash == before.documents["NoteDoc:note"].source_hash
    assert after.documents["NoteDoc:note"].content_hash != before.documents["NoteDoc:note"].content_hash


def test_a_moved_contract_invalidates_the_document_cache(contract_store, tmp_path):
    """The cache keys promised "a contract that moved invalidates the entry" while keying on the
    roster, which cannot see a contract change. The payload of an unmodified file must still
    gain the new field — read through the cache, with no `stores update` in between."""
    from sldb.api import load_runtime_documents

    first = load_runtime_documents(contract_store.store, contract_store.pythonpath)
    assert "status" not in first[0].payload
    _write_module(tmp_path, _TWO_FIELDS)
    again = load_runtime_documents(contract_store.store, contract_store.pythonpath)
    assert "status" in again[0].payload, "the stale payload won: the contract change was invisible"


def test_store_is_valid_again_after_update(contract_store, tmp_path):
    _write_module(tmp_path, _TWO_FIELDS)
    update_store_indexes(contract_store.store, contract_store.pythonpath)
    report = check_store(contract_store.store, project_root(contract_store.store), contract_store.pythonpath)
    assert report["valid"], report
