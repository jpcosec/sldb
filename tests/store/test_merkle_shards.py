"""PLAN 15 capa 5: semantic and sections indexes are per-document shards under
`.sldb/runtime/{semantic,sections}/<Model>/<doc>.yaml`. The invariant: the aggregate
`load_semantic_index`/`load_sections_index` compose from shards equals what extracting every
document directly (bypassing the whole index machinery) would produce — after add, change,
and untrack. Also: untracking removes the shard, and a store still in the old single-file
shape is migrated into shards (and the old files removed) the next time it is touched."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as cli_main
from sldb.cli.commands.store_update import update_store
from sldb.cli.model_utils import resolve_model_ref
from sldb.store.io import load_documents_index, load_models_index, load_sections_index, load_semantic_index, load_store_index
from sldb.store.io.utils import yaml_dump
from sldb.store.layout import (
    project_root,
    sections_index_relpath,
    sections_shards_dir,
    semantic_index_path,
    semantic_shards_dir,
    store_index_path,
)
from sldb.store.migration import migrate_store_layout
from sldb.store.section_rebuild import _extract_sections
from sldb.store.semantic_tags import collect_document_semantic_tags


def _write_model(project: Path) -> str:
    package = project / "shardnotes"
    package.mkdir()
    (package / "__init__.py").write_text("", encoding="utf-8")
    (package / "models.py").write_text(
        "from pydantic import Field\n"
        "from sldb import StructuredNLDoc\n\n"
        "class Note(StructuredNLDoc):\n"
        "    __semantics__ = {'domain': ['notes']}\n"
        "    __template__ = '# ⸢rev•title⸥\\n\\n## Body\\n\\n⸢rev•body⸥'\n"
        "    title: str = Field(description='Title')\n"
        "    body: str = Field(description='Body')\n"
        "    semantic_tags: list[str] = Field(default_factory=list, description='Tags')\n",
        encoding="utf-8",
    )
    return "shardnotes.models:Note"


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
    doc = root / f"note-{i}.md"
    tag = "type.even" if i % 2 == 0 else "type.odd"
    payload = {"title": f"Note {i}", "body": f"Body of note {i}", "semantic_tags": [tag]}
    import json

    assert cli_main(["docs", "create", "--model", "Note", "-o", str(doc), "--name", f"note-{i}", json.dumps(payload), "--store", str(store), "--pythonpath", str(root)]) == 0


def _reference(root: Path, store: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    """Every tracked Note's tags and section titles, extracted directly — no index, no cache."""
    note_type = resolve_model_ref("shardnotes.models:Note", str(root))
    idx = load_store_index(store)
    m_entry = next(m for m in idx.models if m.name == "Note")
    m_idx = load_models_index(root / m_entry.models_index)
    d_idx = load_documents_index(root / m_idx.documents_index)
    tags: dict[str, list[str]] = {}
    sections: dict[str, list[str]] = {}
    for doc in d_idx.documents:
        text = (root / doc.path).read_text(encoding="utf-8")
        tags[doc.name] = collect_document_semantic_tags(note_type, _payload_of(note_type, text))
        sections[doc.name] = [s["title"] for s in _extract_sections(text)]
    return tags, sections


def _payload_of(model_type, text: str) -> dict:
    from sldb.store.codec import default_codec

    return default_codec.extract(model_type, text)


def _composed(root: Path, store: Path) -> tuple[dict[str, list[str]], dict[str, list[str]]]:
    semantic = load_semantic_index(store)
    m_idx = load_models_index(root / next(m for m in load_store_index(store).models if m.name == "Note").models_index)
    sections_idx = load_sections_index(root / m_idx.sections_index) if m_idx.sections_index else None
    tags = {name: rec.tags for name, rec in semantic.documents.items()}
    secs = {ds.doc_name: [s.title for s in ds.sections] for ds in (sections_idx.documents if sections_idx else [])}
    return tags, secs


def test_shard_aggregate_equals_direct_extraction(tmp_path: Path):
    store, root = _store(tmp_path, 8)
    update_store(_Args(store, root))
    ref_tags, ref_secs = _reference(root, store)
    got_tags, got_secs = _composed(root, store)
    assert got_tags == ref_tags
    assert got_secs == ref_secs


def test_shard_aggregate_equals_direct_extraction_after_writes(tmp_path: Path):
    store, root = _store(tmp_path, 5)
    update_store(_Args(store, root))
    _create_doc(root, store, 5)  # add
    assert cli_main(["docs", "update", "note-1", '{"title": "Note 1", "body": "changed", "semantic_tags": ["type.odd"]}', "--store", str(store), "--pythonpath", str(root)]) == 0  # change
    assert cli_main(["docs", "untrack", "note-2", "--store", str(store), "--pythonpath", str(root)]) == 0  # untrack
    update_store(_Args(store, root))
    ref_tags, ref_secs = _reference(root, store)
    got_tags, got_secs = _composed(root, store)
    assert got_tags == ref_tags
    assert got_secs == ref_secs
    assert "note-2" not in got_tags and "note-2" not in got_secs


def test_untrack_deletes_the_shards_not_just_the_aggregate_entry(tmp_path: Path):
    store, root = _store(tmp_path, 3)
    update_store(_Args(store, root))
    sem_dir, sec_dir = semantic_shards_dir(store, "Note"), sections_shards_dir(store, "Note")
    assert (sem_dir / "note-1.yaml").exists()
    assert (sec_dir / "note-1.yaml").exists()
    assert cli_main(["docs", "untrack", "note-1", "--store", str(store), "--pythonpath", str(root)]) == 0
    update_store(_Args(store, root))
    assert not (sem_dir / "note-1.yaml").exists()
    assert not (sec_dir / "note-1.yaml").exists()


def test_migrates_a_legacy_single_file_store_into_shards(tmp_path: Path):
    store, root = _store(tmp_path, 3)
    update_store(_Args(store, root))
    ref_tags, ref_secs = _reference(root, store)

    # Simulate a store still on the old single-file shape: write the legacy files by hand,
    # and remove the shards a real capa-5 store would already have.
    m_idx_path = None
    for m in load_store_index(store).models:
        if m.name == "Note":
            m_idx_path = root / m.models_index
    m_idx = load_models_index(m_idx_path)
    legacy_semantic = {"tags": {}, "documents": {n: {"model": "Note", "path": f"note-{n.split('-')[1]}.md", "tags": t} for n, t in ref_tags.items()}}
    semantic_index_path(store).parent.mkdir(parents=True, exist_ok=True)
    semantic_index_path(store).write_text(yaml_dump(legacy_semantic), encoding="utf-8")
    legacy_sections_path = root / sections_index_relpath(store, "Note")
    legacy_sections = {"documents": [{"doc_name": n, "sections": [{"path": t.lower(), "title": t, "breadcrumbs": [t], "semantic_tags": [], "slug": t.lower(), "level": 2} for t in titles]} for n, titles in ref_secs.items()]}
    legacy_sections_path.parent.mkdir(parents=True, exist_ok=True)
    legacy_sections_path.write_text(yaml_dump(legacy_sections), encoding="utf-8")
    import shutil

    shutil.rmtree(semantic_shards_dir(store, "Note").parent, ignore_errors=True)
    shutil.rmtree(sections_shards_dir(store, "Note"), ignore_errors=True)

    assert semantic_index_path(store).exists()
    assert legacy_sections_path.exists()
    migrate_store_layout(store, root)
    assert not semantic_index_path(store).exists()
    assert not legacy_sections_path.exists()
    assert (semantic_shards_dir(store, "Note") / "note-0.yaml").exists()
    got_tags, got_secs = _composed(root, store)
    assert got_tags == ref_tags
    assert got_secs == ref_secs
