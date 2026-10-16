"""`models remove`, and writes that survive a model whose class is gone.

Covers: the entry, its indexes and its shards go and the store still passes `stores check`
and `edges check`; a model that still tracks documents, or is not registered, is refused;
the class need not be importable (it is usually being deleted); `stores check` names an
unimportable model with no documents as removable; `--with-documents` drops a model and
its documents without importing it; untracking works while another model does not import;
an untrack that raises halfway leaves the store's files as they were.
"""

from __future__ import annotations

import shutil
import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBModelError
from sldb.store import built_cache, documents_hash
from sldb.store.user_cache import built_cache_file
from sldb.store.diagnostics import diagnose_store
from sldb.store.io import invalidate_index_cache, load_store_index
from sldb.store.layout import documents_index_relpath, edges_model_shard_path, models_index_relpath, project_root
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_remove_model_test_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class KeptDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")


class GoneDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥"
    title: str = Field(description="Title.")
'''


@pytest.fixture
def store(tmp_path: Path) -> tuple[Path, str]:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    root, py = tmp_path / "repo", str(tmp_path)
    root.mkdir()
    sp = api.init_store(root).store_path
    api.init_relations(sp, py)
    for model in ("KeptDoc", "GoneDoc"):
        api.add_model(sp, f"{MODULE}:{model}", py)
    api.create_document(sp, "KeptDoc", root / "kept.md", {"title": "Kept"}, "kept", py)
    return sp, py


def _forget_the_class(py: str) -> None:
    (Path(py) / f"{MODULE}.py").write_text(MODELS.split("class GoneDoc")[0], encoding="utf-8")
    sys.modules.pop(MODULE, None)
    invalidate_index_cache()
    invalidate_runtime_cache()


def test_a_model_without_documents_is_removed_whole(store):
    sp, py = store
    _forget_the_class(py)
    removed = api.remove_model(sp, "GoneDoc", py)
    assert removed.model_ref == f"{MODULE}:GoneDoc"
    assert [m.name for m in load_store_index(sp).models if m.name.endswith("Doc") and "Relation" not in m.name] == ["KeptDoc"]
    root = project_root(sp)
    assert not (root / models_index_relpath(sp, "GoneDoc")).exists()
    assert not (root / documents_index_relpath(sp, "GoneDoc")).exists()
    assert not edges_model_shard_path(sp, "GoneDoc").exists()
    assert diagnose_store(sp, api.resolve_model_ref, root, py).is_valid
    assert api.check_edges(sp).ok


def _gone_with_a_document(store) -> tuple[Path, str]:
    sp, py = store
    api.create_document(sp, "GoneDoc", project_root(sp) / "gone.md", {"title": "Gone"}, "gone", py)
    _forget_the_class(py)
    shutil.rmtree(sp / "runtime")  # a fresh clone: no derived shard to reuse, so rebuilds re-extract
    (built_cache_file(sp) or Path("/nonexistent")).unlink(missing_ok=True)
    built_cache.clear()
    documents_hash.invalidate(sp, "GoneDoc")  # nor an in-memory baseline: a new process
    return sp, py


def test_untracking_works_while_another_model_does_not_import(store):
    sp, py = _gone_with_a_document(store)
    api.untrack_document(sp, "kept", py)
    assert diagnose_store(sp, api.resolve_model_ref, project_root(sp), py).is_valid


def test_a_model_is_removed_with_its_documents_when_asked(store):
    sp, py = _gone_with_a_document(store)
    with pytest.raises(SLDBModelError, match="--with-documents"):
        api.remove_model(sp, "GoneDoc", py)
    assert cli_main(["models", "remove", "GoneDoc", "--with-documents", "--store", str(sp), "--pythonpath", py]) == 0
    assert (project_root(sp) / "gone.md").exists()
    assert "GoneDoc" not in [m.name for m in load_store_index(sp).models]
    assert diagnose_store(sp, api.resolve_model_ref, project_root(sp), py).is_valid
    assert api.check_edges(sp).ok


def test_a_failed_untrack_leaves_the_store_as_it_was(store, monkeypatch):
    sp, py = store
    core = sorted((p, p.read_bytes()) for p in (sp / "core").rglob("*") if p.is_file())
    import sldb.api.documents.untrack_document as untrack

    def boom(*args, **kwargs):
        raise RuntimeError("rebuild failed")

    monkeypatch.setattr(untrack, "rebuild_edges_indexes", boom)
    with pytest.raises(RuntimeError):
        api.untrack_document(sp, "kept", py)
    assert sorted((p, p.read_bytes()) for p in (sp / "core").rglob("*") if p.is_file()) == core
    assert diagnose_store(sp, api.resolve_model_ref, project_root(sp), py).is_valid
    assert [d.name for d in api.load_runtime_documents(sp, py) if d.model_name == "KeptDoc"] == ["kept"]


def test_a_model_that_tracks_documents_is_refused(store):
    sp, py = store
    with pytest.raises(SLDBModelError, match="untrack them first"):
        api.remove_model(sp, "KeptDoc", py)
    with pytest.raises(SLDBModelError, match="not registered"):
        api.remove_model(sp, "NoSuchDoc", py)


def test_stores_check_names_a_removable_model(store, capsys):
    sp, py = store
    _forget_the_class(py)
    assert cli_main(["stores", "check", "--store", str(sp), "--pythonpath", py]) == 0
    assert "sldb models remove <name>` unregisters one with no documents: GoneDoc" in capsys.readouterr().out
    assert cli_main(["models", "remove", "GoneDoc", "--store", str(sp), "--pythonpath", py]) == 0
    assert capsys.readouterr().out.startswith("Removed model: GoneDoc")
    assert cli_main(["stores", "check", "--store", str(sp), "--pythonpath", py]) == 0
    assert "GoneDoc" not in capsys.readouterr().out
