"""PLAN 15 capa 7: the documents index is per-document shards under
`.sldb/core/documents/<Model>/<doc>.yaml` — the Merkle tree's own leaf level. The invariant:
the aggregate `load_documents_index` composed from shards equals what reading every tracked
file directly (bypassing the whole index machinery) would produce — after add, change, and
untrack — and the model's `hash_b`/store's `hash_a` match what a full scan of that same
content gives via `hashing.hash_document_entries` (order-independent by design: see
`hashing.hash_documents_index`'s docstring for why that is a deliberate change from the old,
insertion-order-dependent definition). Also: untracking removes the shard, not just the
aggregate entry, and a store still in the old single-file shape is migrated into shards (old
file removed) the next time it is touched, with hash_b unchanged by the migration itself."""

from __future__ import annotations

import json
from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.commands.store_update import update_store
from sldb.store.hashing import hash_document_entries, hash_fields, hash_text
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import documents_index_relpath, documents_shards_dir
from sldb.store.migration import migrate_store_layout


def _write_model(project: Path) -> str:
    package = project / "shardocs"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class Note(StructuredNLDoc):\n"
        "    __template__ = '# ⸢rev•title⸥\\n\\n## Body\\n\\n⸢rev•body⸥'\n"
        "    title: str = Field(description='Title')\n"
        "    body: str = Field(description='Body')\n",
        encoding="utf-8",
    )
    return "shardocs.models:Note"


class _Args:
    def __init__(self, store: Path, pythonpath: Path):
        self.store, self.pythonpath, self.wait, self.verbose = str(store), str(pythonpath), False, False


def _store(tmp_path: Path, n: int) -> tuple[Path, Path]:
    model_ref = _write_model(tmp_path)
    store = tmp_path / ".sldb"
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["models", "add", model_ref, "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    for i in range(n):
        _create_doc(tmp_path, store, i)
    return store, tmp_path


def _create_doc(root: Path, store: Path, i: int) -> None:
    # PLAN 15 capa 7: distinct content from test_merkle_shards.py's own "note-N" docs on
    # purpose — sldb.store.semantic_doc_tags._DOC_TAGS caches by (doc.path, hash_c, model
    # name) without the store's own path, so two stores with the same relative doc path,
    # model name, and (since semantic_tags is not part of the rendered markdown) coincidentally
    # identical hash_c would share a stale cache entry across this file and that one when both
    # run in the same process. Pre-existing, out of scope for capa 7 — worked around here.
    doc = root / f"note-{i}.md"
    payload = {"title": f"Shard Note {i}", "body": f"Body of shard note {i}"}
    assert cli_main(["docs", "create", "--model", "Note", "-o", str(doc), "--name", f"note-{i}", json.dumps(payload), "--store", str(store), "--pythonpath", str(root)]) == 0


def _model_entry(store: Path):
    return next(m for m in load_store_index(store).models if m.name == "Note")


def _reference(root: Path, store: Path) -> dict[str, tuple[str, str]]:
    """Every tracked Note's (hash_c, hash_d), computed directly from its file — no index,
    no cache, no shard."""
    from sldb.cli.model_utils import resolve_model_ref

    note_type = resolve_model_ref("shardocs.models:Note", str(root))
    m_idx = load_models_index(root / _model_entry(store).models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    out = {}
    for doc in d_idx.documents:
        text = (root / doc.path).read_text(encoding="utf-8")
        out[doc.name] = (hash_text(text), hash_fields(note_type, text))
    return out


def _composed(root: Path, store: Path) -> dict[str, tuple[str, str]]:
    m_idx = load_models_index(root / _model_entry(store).models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    return {d.name: (d.hash_c, d.hash_d) for d in d_idx.documents}


def test_shard_aggregate_equals_direct_extraction(tmp_path: Path):
    store, root = _store(tmp_path, 8)
    update_store(_Args(store, root))
    assert _composed(root, store) == _reference(root, store)


def test_shard_aggregate_equals_direct_extraction_after_writes(tmp_path: Path):
    store, root = _store(tmp_path, 5)
    update_store(_Args(store, root))
    _create_doc(root, store, 5)  # add
    assert cli_main(["docs", "update", "note-1", '{"title": "Shard Note 1", "body": "changed shard content"}', "--store", str(store), "--pythonpath", str(root)]) == 0  # change
    assert cli_main(["docs", "untrack", "note-2", "--store", str(store), "--pythonpath", str(root)]) == 0  # untrack
    update_store(_Args(store, root))
    got = _composed(root, store)
    assert got == _reference(root, store)
    assert "note-2" not in got


def test_untrack_deletes_the_shard_not_just_the_aggregate_entry(tmp_path: Path):
    store, root = _store(tmp_path, 3)
    shard = documents_shards_dir(store, "Note") / "note-1.yaml"
    assert shard.exists()
    assert cli_main(["docs", "untrack", "note-1", "--store", str(store), "--pythonpath", str(root)]) == 0
    assert not shard.exists()


def test_hash_b_matches_a_full_scan_of_the_same_content(tmp_path: Path):
    """hash_b, kept incrementally via documents_hash.note()/hash_b_of() on the hot write path,
    equals what hashing every child directly (sorted, order-independent) gives for the same
    content — the proof obligation for capa 7's new, order-independent hash_b definition."""
    store, root = _store(tmp_path, 6)
    m_idx = load_models_index(root / _model_entry(store).models_index)
    ref = _reference(root, store)
    expected = hash_document_entries((n, hc, hd) for n, (hc, hd) in ref.items())
    assert m_idx.hash_b == expected
    assert m_idx.documents_count == len(ref)


def test_hash_b_is_order_independent(tmp_path: Path):
    """Untracking and re-tracking documents in a different order than they were first created
    still gives the same hash_b for the same final content set (PLAN 15 capa 7: hash_b is
    keyed by name and sorted, not insertion order)."""
    store, root = _store(tmp_path, 4)
    m_idx_before = load_models_index(root / _model_entry(store).models_index)
    for i in (0, 1, 2, 3):
        assert cli_main(["docs", "untrack", f"note-{i}", "--store", str(store), "--pythonpath", str(root)]) == 0
    for i in (3, 1, 0, 2):  # re-track in a different order
        assert cli_main(["docs", "track", str(root / f"note-{i}.md"), "--name", f"note-{i}", "--model", "Note", "--store", str(store), "--pythonpath", str(root)]) == 0
    m_idx_after = load_models_index(root / _model_entry(store).models_index)
    assert m_idx_after.hash_b == m_idx_before.hash_b


def test_migrates_a_legacy_single_file_documents_index_into_shards(tmp_path: Path):
    store, root = _store(tmp_path, 3)
    update_store(_Args(store, root))
    ref = _reference(root, store)
    m_entry = _model_entry(store)
    m_idx_path = root / m_entry.models_index
    m_idx = load_models_index(m_idx_path)
    hash_b_before = m_idx.hash_b

    # Simulate a store still on the old single-file shape: write the legacy file by hand, and
    # remove the shards a real capa-7 store would already have.
    legacy_path = root / documents_index_relpath("Note")
    legacy = {"documents": [{"name": n, "path": f"note-{n.split('-')[1]}.md", "hash_c": hc, "hash_d": hd} for n, (hc, hd) in ref.items()]}
    legacy_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_path.write_text(yaml_dump(legacy), encoding="utf-8")
    import shutil

    shutil.rmtree(documents_shards_dir(store, "Note"), ignore_errors=True)

    assert legacy_path.exists()
    migrate_store_layout(store, root)
    assert not legacy_path.exists()
    assert (documents_shards_dir(store, "Note") / "note-0.yaml").exists()
    assert _composed(root, store) == ref
    assert load_models_index(m_idx_path).hash_b == hash_b_before
