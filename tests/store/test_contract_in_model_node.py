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

# Same fields, same template, same text on disk: only the class metadata moved.
_FAMILY_A = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __family__ = "notes"
    __semantics__ = {"type": ["knowledge", "note"]}
    __template__ = """# ⸢rev•title⸥""".strip()
    title: str = Field(description="Note title.")
'''

_FAMILY_B = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __family__ = "records"
    __template__ = """# ⸢rev•title⸥""".strip()
    title: str = Field(description="Note title.")
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


def test_contract_hash_covers_family_and_semantics(tmp_path):
    """`__family__` and `__semantics__` moved out of the hash and froze in the store.

    They drive the derived indexes, so a change to them must move the model's node —
    otherwise `stores check` cannot see that the class and the store have diverged.
    """
    _write_module(tmp_path, _FAMILY_A)
    hash_a = hash_model_contract(resolve_model_ref(f"{MODULE}:NoteDoc", str(tmp_path)))
    _write_module(tmp_path, _FAMILY_B)
    hash_b = hash_model_contract(resolve_model_ref(f"{MODULE}:NoteDoc", str(tmp_path)))
    assert hash_a != hash_b


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


def test_a_moved_contract_does_not_excuse_an_edited_file(contract_store, tmp_path):
    """The contract absolves the document only while its TEXT is intact. Both moving at once is
    still a data mutation: excusing it would hide a hand edit behind a safe-to-run verdict."""
    from sldb.store.diagnostics import diagnose_store

    _write_module(tmp_path, _TWO_FIELDS)
    (contract_store.root / "note.md").write_text("# Edited By Hand\n", encoding="utf-8")
    diagnosis = diagnose_store(contract_store.store, resolve_model_ref, project_root(contract_store.store), pythonpath=contract_store.pythonpath)
    doc = diagnosis.models[0].documents[0]
    assert doc.note.value == "data_mutation", "an edited file must not be excused by the contract"
    assert doc.needs_decision


def test_health_names_what_to_look_at_and_what_to_run(contract_store, tmp_path):
    """`/health` used to answer `{"status": "ok"}` unconditionally — the HTTP code already said
    that. It must report the verdict, the subjects, and whether a command or a human is next."""
    from sldb.cli.serve.routes import health_payload

    root = project_root(contract_store.store)
    assert health_payload(contract_store.store, root, contract_store.pythonpath)["status"] == "ok"
    _write_module(tmp_path, _TWO_FIELDS)
    degraded = health_payload(contract_store.store, root, contract_store.pythonpath)
    assert degraded["status"] == "degraded"
    assert degraded["findings"] == [{"kind": "contract_moved", "subject": "NoteDoc", "needs_decision": False}]
    assert degraded["action"] == "run: sldb stores update"


def test_health_demands_a_human_when_a_field_was_edited(contract_store, tmp_path):
    """A changed field value is not something a command should paper over: the index holds the
    only record of the previous value. The action must say inspect, not run."""
    from sldb.cli.serve.routes import health_payload

    (contract_store.root / "note.md").write_text("# Edited By Hand\n", encoding="utf-8")
    report = health_payload(contract_store.store, project_root(contract_store.store), contract_store.pythonpath)
    assert report["status"] == "degraded"
    assert report["action"].startswith("inspect:")
    assert any(f["needs_decision"] for f in report["findings"])


def test_check_report_names_the_source_file_of_a_moved_contract(contract_store, tmp_path, capsys):
    """The operator has to open something. For a moved contract that something is the .py the
    class is declared in, not the document whose text nobody touched."""
    from sldb.cli.commands.store_check_report import print_report
    from sldb.store.diagnostics import diagnose_store

    _write_module(tmp_path, _TWO_FIELDS)
    diagnosis = diagnose_store(contract_store.store, resolve_model_ref, project_root(contract_store.store), pythonpath=contract_store.pythonpath)
    print_report(diagnosis)
    out = capsys.readouterr().out
    assert f"{MODULE}.py" in out, "the report must name the file declaring the contract"
    assert "inspect :" in out and "fix     :" in out
    assert "next: sldb stores update" in out


def test_store_is_valid_again_after_update(contract_store, tmp_path):
    _write_module(tmp_path, _TWO_FIELDS)
    update_store_indexes(contract_store.store, contract_store.pythonpath)
    report = check_store(contract_store.store, project_root(contract_store.store), contract_store.pythonpath)
    assert report["valid"], report


def test_update_restamps_the_roster_of_a_model_that_does_not_import(contract_store, tmp_path):
    """A model whose class is gone still has a document list, and `stores update` must sign it.

    It used to skip the whole model as broken, so a stale roster (here, written by hand; in the
    wild, a merge that brought shards in) stayed `roster stale` in `stores check` until someone
    called `stamp_model_node(..., None)` and `cascade_store_hash` by hand.
    """
    from sldb.store.io import save_models_index

    m_entry = load_store_index(contract_store.store).models[0]
    m_idx = _model_index(contract_store)
    contract = m_idx.contract_hash
    m_idx.roster_hash = "0" * len(m_idx.roster_hash)
    m_idx.model_hash = hash_model_layer(m_idx.roster_hash, m_idx.contract_hash)
    save_models_index(contract_store.root / m_entry.models_index, m_idx)
    _write_module(tmp_path, 'raise ImportError("the class is gone")\n')
    assert check_store(contract_store.store, contract_store.root, contract_store.pythonpath)["roster_only"] == ["NoteDoc"]

    report = update_store_indexes(contract_store.store, contract_store.pythonpath)

    assert report.skipped_models == ["NoteDoc"], "its documents still could not be rehashed"
    after = check_store(contract_store.store, contract_store.root, contract_store.pythonpath)
    assert after["roster_only"] == [] and after["valid"]
    m_idx = _model_index(contract_store)
    assert m_idx.contract_hash == contract, "an unimportable class keeps the contract it signed"
    assert m_idx.model_hash == hash_model_layer(m_idx.roster_hash, contract)
