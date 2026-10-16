"""`models remove`: a model with no documents is unregistered without importing it.

Covers: the entry, its indexes and its shards go and the store still passes `stores check`
and `edges check`; a model that still tracks documents, or is not registered, is refused;
the class need not be importable (it is usually being deleted); `stores check` names an
unimportable model with no documents as removable.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb import api
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBModelError
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
