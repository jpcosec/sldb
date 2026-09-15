"""PLAN 15 M2: a write touches its own document, not the whole model.

Adding one document to a model that already tracks several: the semantic and sections
rebuilds must extract only the new document, not re-parse the ones whose `hash_c` did not
move — the on-disk per-document cache (`built_cache` "semantic"/"sections", keyed by the
model's hash_b, falling back to the stale entry for a document whose own hash_c matches) is
what makes that possible even though the model's aggregate key changed."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.commands.store_update import update_store
from sldb.cli.model_utils import resolve_model_ref
from sldb.store import section_rebuild, semantic_doc_contribution
from sldb.store.io import load_store_index


def _write_model(project: Path) -> str:
    package = project / "notes"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class NoteDoc(StructuredNLDoc):\n"
        "    __template__ = '# ⸢rev•title⸥\\n\\n## Body\\n\\n⸢rev•body⸥'\n"
        "    title: str = Field(description='Title')\n"
        "    body: str = Field(description='Body')\n",
        encoding="utf-8",
    )
    return "notes.models:NoteDoc"


def _store(tmp_path: Path, n: int) -> tuple[Path, Path]:
    model_ref = _write_model(tmp_path)
    store = tmp_path / ".sldb"
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["models", "add", model_ref, "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    for i in range(n):
        doc = tmp_path / f"note-{i}.md"
        doc.write_text(f"# Note {i}\n\n## Body\n\nBody of note {i}\n", encoding="utf-8")
        assert cli_main(["docs", "track", str(doc), "--model", "NoteDoc", "--name", f"note-{i}", "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    return store, tmp_path


class _Args:
    def __init__(self, store: Path, pythonpath: Path):
        self.store, self.pythonpath, self.wait, self.verbose = str(store), str(pythonpath), False, False


def test_adding_one_document_extracts_only_that_document(tmp_path: Path, monkeypatch):
    store, root = _store(tmp_path, 20)
    update_store(_Args(store, root))  # settle hash_c/hash_d/semantic/sections for all 20

    calls = {"semantic": 0, "sections": 0}
    real_process_doc = semantic_doc_contribution.process_doc
    real_process_doc_sections = section_rebuild._process_doc_sections

    def counted_process_doc(*a, **kw):
        calls["semantic"] += 1
        return real_process_doc(*a, **kw)

    def counted_process_doc_sections(*a, **kw):
        calls["sections"] += 1
        return real_process_doc_sections(*a, **kw)

    monkeypatch.setattr(semantic_doc_contribution, "process_doc", counted_process_doc)
    monkeypatch.setattr(section_rebuild, "_process_doc_sections", counted_process_doc_sections)

    new_doc = root / "note-20.md"
    new_doc.write_text("# Note 20\n\n## Body\n\nBody of note 20\n", encoding="utf-8")
    assert cli_main(["docs", "track", str(new_doc), "--model", "NoteDoc", "--name", "note-20", "--store", str(store), "--pythonpath", str(root)]) == 0
    update_store(_Args(store, root))  # the sections half of a real turn's refresh (pron.world.World.refresh)

    assert calls["semantic"] == 1, calls
    assert calls["sections"] == 1, calls


def test_load_store_index_is_cached_by_file_signature(tmp_path: Path):
    """PLAN 15 M2: `load_store_index` reads the file once per (mtime, size); repeated calls in
    a row, nothing saved in between, come back from the in-process cache."""
    store, root = _store(tmp_path, 3)
    from sldb.store.io import _INDEXES  # the cache this test is about

    _INDEXES.clear()
    first = load_store_index(store)
    key = str(store / "core" / "store_index.yaml") if (store / "core" / "store_index.yaml").exists() else next(iter(_INDEXES))
    cached_object_id = id(_INDEXES[key][1])
    for _ in range(20):
        load_store_index(store)
    assert id(_INDEXES[key][1]) == cached_object_id  # never reloaded from disk
    assert load_store_index(store).hash_a == first.hash_a
