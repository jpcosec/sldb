"""Regression (desk/inbox/20260916-095507): index relpaths derive from the store's real
directory name, not a hardcoded `.sldb`. A store renamed to `.sldb_custom` must stay fully
readable — `models add` writes `kb/.sldb_custom/core/models/...`, tracking writes document
shards under the real store, `docs list` composes them back, and no phantom `.sldb`
directory is created."""

from __future__ import annotations

from pathlib import Path

from sldb.cli import main as cli_main
from sldb.store.io import load_documents_index, load_models_index, load_store_index
from sldb.store.layout import documents_shard_path, models_index_relpath


def _write_model(project: Path) -> str:
    package = project / "renamedocs"
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
    return "renamedocs.models:Note"


def _renamed_store(tmp_path: Path, name: str) -> tuple[Path, Path]:
    """Init a store under the default name, then rename it to `name` (the repro's `mv`)."""
    root = tmp_path / "kb"
    root.mkdir()
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    store = root / ".sldb"
    renamed = root / name
    store.rename(renamed)
    return renamed, root


def test_renamed_store_stays_fully_readable(tmp_path: Path, capsys) -> None:
    model_ref = _write_model(tmp_path)
    store, root = _renamed_store(tmp_path, ".sldb_custom")
    assert cli_main(["models", "add", model_ref, "--store", str(store), "--pythonpath", str(tmp_path)]) == 0
    assert cli_main(["docs", "create", '{"title": "Hola", "body": "Mundo"}', "--model", "Note", "-o", str(root / "x2.md"), "--store", str(store), "--pythonpath", str(tmp_path)]) == 0

    # The model index and document shard live under the real store directory...
    m_entry = next(m for m in load_store_index(store).models if m.name == "Note")
    assert m_entry.models_index == models_index_relpath(store, "Note")
    assert (root / m_entry.models_index).exists()
    assert documents_shard_path(store, "Note", "x2").exists()
    # ...and `docs list` composes the tracked document from them.
    out = capsys.readouterr().out
    assert cli_main(["docs", "list", "--store", str(store)]) == 0
    listed = capsys.readouterr().out
    assert "Note" in listed and "x2" in listed and "No tracked" not in listed
    assert out  # sanity: the create command printed its confirmation

    d_idx = load_documents_index(root / load_models_index(root / m_entry.models_index).documents_index)
    assert [d.name for d in d_idx.documents] == ["x2"]

    # No phantom `.sldb` directory may exist anywhere under the project root.
    assert not (root / ".sldb").exists()