"""The address surface: read and write fields by address, never by opening Markdown.

Covers what `docs/addressability_model.md` promises:
- `sldb legacy ls|get|glob|find` (and the singular aliases) are wired and answer
  `st.{Model}.doc.field` addresses;
- `st.{Base+}` names a family even when the base model is not registered;
- `find --where 'model <= Base'` filters by family from the public surface;
- `models add` records `__family__` and the StructuredNLDoc bases;
- `fields update` rewrites the Markdown and the next address read sees the new value.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

from sldb.cli import main as cli_main
from sldb.store.io import load_models_index, load_store_index


def _write_models(base: Path) -> str:
    sys.modules.pop("address_models", None)
    (base / "address_models.py").write_text(
        '''from pydantic import Field
from sldb import StructuredNLDoc


class BaseNote(StructuredNLDoc):
    __family__ = "notes"
    __template__ = "# ⸢rev•title⸥\\n\\nStatus: ⸢rev•status⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="Workflow status.")


class MemoDoc(BaseNote):
    __semantics__ = {"type": ["note", "memo"]}
''',
        encoding="utf-8",
    )
    return str(base)


def _setup(tmp_path: Path, capsys=None) -> tuple[Path, list[str]]:
    """Build a store with two MemoDoc documents; drains captured setup output when capsys is given."""
    pythonpath = _write_models(tmp_path)
    root = tmp_path / "repo"
    root.mkdir()
    store = root / ".sldb"
    common = ["--store", str(store), "--pythonpath", pythonpath]
    assert cli_main(["stores", "init", "--path", str(root)]) == 0
    assert cli_main(["models", "add", "address_models:MemoDoc", *common]) == 0
    for name, status in (("memo1", "open"), ("memo2", "done")):
        payload = json.dumps({"title": name.title(), "status": status})
        assert cli_main(["docs", "create", "--model", "MemoDoc", "-o", str(root / f"{name}.md"), payload, *common]) == 0
    if capsys is not None: capsys.readouterr()
    return store, common


def test_models_add_records_family_and_bases(tmp_path):
    store, _ = _setup(tmp_path)
    entry = next(m for m in load_store_index(store).models if m.name == "MemoDoc")
    index = load_models_index(store.parent / entry.models_index)
    assert index.family == "notes"
    assert index.base_models == ["BaseNote"]
    assert entry.family == "notes"
    assert "type.note.memo" in entry.semantics


def test_legacy_get_reads_a_field_by_address(tmp_path, capsys):
    _, common = _setup(tmp_path, capsys)
    assert cli_main(["legacy", "get", "st.{MemoDoc}.memo1.status", "--format", "text", *common]) == 0
    assert capsys.readouterr().out.strip() == "open"


def test_legacy_ls_walks_store_model_doc(tmp_path, capsys):
    _, common = _setup(tmp_path, capsys)
    assert cli_main(["legacy", "ls", "st", *common]) == 0
    assert "st.{MemoDoc}" in capsys.readouterr().out
    assert cli_main(["legacy", "ls", "st.{MemoDoc}", *common]) == 0
    assert capsys.readouterr().out.split() == ["memo1", "memo2"]
    assert cli_main(["legacy", "ls", "st.{MemoDoc}.memo1", *common]) == 0
    assert "status: Workflow status." in capsys.readouterr().out


def test_family_scope_works_for_an_unregistered_base(tmp_path, capsys):
    _, common = _setup(tmp_path, capsys)
    assert cli_main(["legacy", "find", "st.{BaseNote+}", "--where", 'status = "open"', *common]) == 0
    assert capsys.readouterr().out.split() == ["st.{BaseNote+}.memo1"]
    assert cli_main(["legacy", "ls", "st.{BaseNote}", *common]) == 0
    assert capsys.readouterr().out.strip() == ""


def test_find_filters_by_family_from_the_public_surface(tmp_path, capsys):
    _, common = _setup(tmp_path, capsys)
    assert cli_main(["find", "", "--in", "physical", "--type", "doc", "--where", "model <= BaseNote", *common]) == 0
    out = capsys.readouterr().out
    assert "memo1" in out and "memo2" in out


def test_singular_alias_routes_to_the_same_handler(tmp_path, capsys):
    _, common = _setup(tmp_path, capsys)
    assert cli_main(["get", "st.{MemoDoc}.memo2.title", "--format", "text", *common]) == 0
    assert capsys.readouterr().out.strip() == "Memo2"
    assert cli_main(["glob", "st.{MemoDoc}.memo*.status", *common]) == 0
    assert capsys.readouterr().out.split() == ["st.{MemoDoc}.memo1.status", "st.{MemoDoc}.memo2.status"]


def test_field_update_is_visible_at_the_address(tmp_path, capsys):
    store, common = _setup(tmp_path, capsys)
    assert cli_main(["fields", "update", "docs/memo2/status", '"open"', *common]) == 0
    capsys.readouterr()
    assert cli_main(["legacy", "find", "st.{BaseNote+}", "--where", 'status = "open"', *common]) == 0
    assert capsys.readouterr().out.split() == ["st.{BaseNote+}.memo1", "st.{BaseNote+}.memo2"]
    assert "Status: open" in (store.parent / "memo2.md").read_text(encoding="utf-8")


def test_field_update_moves_the_model_hash_and_keeps_integrity(tmp_path, capsys):
    """A field write must recompute the model's hash_b, or `stores check` fails afterwards."""
    store, common = _setup(tmp_path, capsys)
    before = load_models_index(store.parent / next(m for m in load_store_index(store).models if m.name == "MemoDoc").models_index).hash_b
    assert cli_main(["fields", "update", "docs/memo1/status", '"done"', *common]) == 0
    after = load_models_index(store.parent / next(m for m in load_store_index(store).models if m.name == "MemoDoc").models_index).hash_b
    assert after != before
    assert cli_main(["stores", "check", *common]) == 0
