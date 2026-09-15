"""PLAN 15 capa 8: after a write, no consumer walks every leaf.

`compose_documents_entries` (the shard glob + per-shard read behind `load_documents_index`)
runs at most once per operation, reused across operations too while the model's hash_b says
nothing moved — never recomposed just because a fresh `new_operation()` started. Semantic and
sections rebuild use the per-document hash map's dirty set to process only a document whose
hash_c actually differs from what its shard reflects, not every document in the model."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.commands.store_update import update_store
from sldb.store import documents_hash
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.io.shard_compose import compose_documents_entries


def _write_model(project: Path) -> str:
    package = project / "opcache"
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
    return "opcache.models:Note"


def _store(tmp_path: Path, n: int) -> tuple[Path, Path]:
    model_ref = _write_model(tmp_path)
    store = tmp_path / ".sldb"
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["models", "add", model_ref, "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    for i in range(n):
        doc = tmp_path / f"note-{i}.md"
        doc.write_text(f"# Opcache note {i}\n\n## Body\n\nBody of opcache note {i}\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(doc), "--model", "Note", "--name", f"note-{i}", "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    return store, tmp_path


class _Args:
    def __init__(self, store: Path, pythonpath: Path):
        self.store, self.pythonpath, self.wait, self.verbose = str(store), str(pythonpath), False, False


def _count_composes(monkeypatch) -> dict[str, int]:
    calls = {"n": 0}
    import sldb.store.documents_hash as dh

    real = dh._compose

    def counted(s_path, model_name):
        calls["n"] += 1
        return real(s_path, model_name)

    monkeypatch.setattr(dh, "_compose", counted)
    return calls


def test_documents_index_composed_at_most_once_per_operation(tmp_path: Path, monkeypatch):
    store, root = _store(tmp_path, 12)
    documents_hash.invalidate(store, "Note")  # drop what tracking the 12 docs already cached
    calls = _count_composes(monkeypatch)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index

    # Several load_documents_index calls in the same operation: one compose, not several.
    for _ in range(5):
        load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 1, calls


def test_documents_index_cache_reused_across_operations_when_nothing_moved(tmp_path: Path, monkeypatch):
    store, root = _store(tmp_path, 12)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index
    load_documents_index(root / load_models_index(m_idx_path).documents_index)  # warm the cache

    calls = _count_composes(monkeypatch)
    documents_hash.new_operation(store)  # a fresh operation, nothing changed in between
    load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 0, calls  # reused verbatim: the model's hash_b agrees with the cache's


def test_invalidate_forces_exactly_one_recompose_with_correct_content(tmp_path: Path, monkeypatch):
    """`invalidate` (a full scan that could have moved anything outside `note`/`forget`, or a
    cache holding something from a completely different, untracked change) always recomposes
    from the shards on disk exactly once, and gets the right content."""
    store, root = _store(tmp_path, 6)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index
    load_documents_index(root / load_models_index(m_idx_path).documents_index)  # warm the cache
    documents_hash.invalidate(store, "Note")

    calls = _count_composes(monkeypatch)
    got = load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 1, calls
    assert {d.name: d.hash_c for d in got.documents} == {d.name: d.hash_c for d in compose_documents_entries(store, "Note")}


def test_a_hand_edit_through_stores_update_needs_no_recompose_next_operation(tmp_path: Path, monkeypatch):
    """`stores update` keeps the cache in step incrementally (`documents_hash.note` per
    document whose hash_c actually moved) rather than invalidating it outright — so a fresh
    operation right after still reuses it verbatim, and its content is correct."""
    store, root = _store(tmp_path, 5)
    m_idx_path = root / next(m for m in load_store_index(store).models if m.name == "Note").models_index
    load_documents_index(root / load_models_index(m_idx_path).documents_index)  # warm the cache

    (root / "note-0.md").write_text("# Opcache note 0\n\n## Body\n\nHand-edited body\n", encoding="utf-8")
    assert update_store(_Args(store, root)) == 0
    documents_hash.new_operation(store)

    calls = _count_composes(monkeypatch)
    got = load_documents_index(root / load_models_index(m_idx_path).documents_index)
    assert calls["n"] == 0, calls  # stores update's own note() calls already kept it current
    assert {d.name: d.hash_c for d in got.documents} == {d.name: d.hash_c for d in compose_documents_entries(store, "Note")}


def test_a_single_write_processes_only_its_own_document_not_every_document(tmp_path: Path, monkeypatch):
    """documents_hash's dirty set (namespaced per consumer) drives semantic/sections rebuild:
    a write to one document among many marks only that one dirty, and a rebuild right after
    reads (`_get`) the cache once but only opens/extracts the dirty document's own shard."""
    from sldb.store import section_rebuild, semantic_doc_contribution

    store, root = _store(tmp_path, 15)
    update_store(_Args(store, root))  # settle semantic/sections for all 15

    calls = {"semantic": 0, "sections": 0}
    real_semantic = semantic_doc_contribution.process_doc
    real_sections = section_rebuild._process_doc_sections

    def counted_semantic(*a, **kw):
        calls["semantic"] += 1
        return real_semantic(*a, **kw)

    def counted_sections(*a, **kw):
        calls["sections"] += 1
        return real_sections(*a, **kw)

    monkeypatch.setattr(semantic_doc_contribution, "process_doc", counted_semantic)
    monkeypatch.setattr(section_rebuild, "_process_doc_sections", counted_sections)

    assert cli_main(["docs", "update", "note-3", '{"title": "Note 3", "body": "changed body"}', "--store", str(store), "--pythonpath", str(root)]) == 0

    assert calls["semantic"] == 1, calls
    assert calls["sections"] == 1, calls


def test_dirty_namespaces_are_independent(tmp_path: Path):
    """One namespace's `clear_dirty` must not erase what another namespace still needs — the
    bug this test guards against: semantic and sections used to share one dirty set, so
    whichever ran first cleared the signal the other relied on to see the very same write."""
    store, root = _store(tmp_path, 3)
    from sldb.store.models import DocumentEntry

    entry = DocumentEntry(name="note-0", path="note-0.md", hash_c="x", hash_d="y")
    documents_hash.clear_dirty(store, "Note", "semantic")
    documents_hash.clear_dirty(store, "Note", "sections")
    documents_hash.note(store, "Note", entry)
    assert documents_hash.dirty_names(store, "Note", "semantic") == {"note-0"}
    assert documents_hash.dirty_names(store, "Note", "sections") == {"note-0"}
    documents_hash.clear_dirty(store, "Note", "semantic")
    assert documents_hash.dirty_names(store, "Note", "semantic") == set()
    assert documents_hash.dirty_names(store, "Note", "sections") == {"note-0"}  # untouched
