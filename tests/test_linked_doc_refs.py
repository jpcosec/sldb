"""Referencing a document of a linked store: `alias:ref` resolves through DIRECT links only,
a bare ref never leaves the local store, and checking a reference neither imports the document
nor writes the store that asks (the referenced document stays trackable, not tracked)."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from sldb.api import doc_status, init_store, link_store, split_doc_ref, store_links
from sldb.api.records.resolve import resolve_runtime_doc
from sldb.cli import main as sldb_main
from sldb.core.exceptions import SLDBDocumentTargetError, SLDBStoreError

MODEL_SRC = (
    "from sldb.models import StructuredNLDoc\nfrom pydantic import Field\n\n"
    "class NoteDoc(StructuredNLDoc):\n    __template__ = '# ⸢rev•title⸥\\n\\n⸢rev•body⸥\\n'\n"
    "    title: str = Field(description='the title')\n    body: str = Field(description='the body')\n"
)


def _store(root: Path, names: list[str]) -> Path:
    root.mkdir(parents=True, exist_ok=True)
    (root / "linkref_models.py").write_text(MODEL_SRC)
    assert sldb_main(["stores", "init", "--path", str(root)]) == 0
    assert sldb_main(["models", "add", "linkref_models:NoteDoc", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    for name in names:
        (root / f"{name}.md").write_text(f"# {name}\n\nbody of {name}\n")
        assert sldb_main(["docs", "track", str(root / f"{name}.md"), "--model", "NoteDoc", "--store", str(root / ".sldb"), "--pythonpath", str(root)]) == 0
    return root / ".sldb"


@pytest.fixture
def linked(tmp_path: Path) -> tuple[Path, Path]:
    a, b = _store(tmp_path / "a", ["alpha"]), _store(tmp_path / "b", ["beta"])
    link_store(a, b, "b")
    return a, b


def _index_bytes(store: Path) -> bytes:
    return (store / "core" / "store_index.yaml").read_bytes()


def test_a_new_store_and_a_store_that_only_links_pass_check(tmp_path: Path):
    a, b = init_store(tmp_path / "a").store_path, init_store(tmp_path / "b").store_path
    assert sldb_main(["stores", "check", "--store", str(a), "--quiet"]) == 0
    link_store(a, b, "b")
    assert sldb_main(["stores", "check", "--store", str(a), "--quiet"]) == 0


def test_a_link_is_recorded_relative_even_outside_the_project(linked):
    a, _ = linked
    assert store_links(a) == [{"name": "b", "path": "../b/.sldb", "resolved": str((a.parent.parent / "b" / ".sldb").resolve()), "status": "ok"}]


@pytest.mark.parametrize("name", ["local", "has space", "-dash", "a:b", "a/b"])
def test_a_link_name_references_cannot_write_is_refused(tmp_path: Path, name: str):
    a, b = init_store(tmp_path / "a").store_path, init_store(tmp_path / "b").store_path
    with pytest.raises(SLDBStoreError, match="Invalid link name"):
        link_store(a, b, name)


def test_a_store_cannot_link_to_itself(tmp_path: Path):
    a = init_store(tmp_path / "a").store_path
    with pytest.raises(SLDBStoreError, match="itself"):
        link_store(a, a, "me")


def test_a_broken_link_is_reported_not_raised(linked, capsys):
    a, b = linked
    shutil.rmtree(b)
    assert store_links(a)[0]["status"] == "missing"
    assert sldb_main(["stores", "list", "--store", str(a)]) == 0
    assert "[missing:" in capsys.readouterr().out


def test_a_qualified_ref_resolves_in_the_linked_store_only(linked):
    a, _ = linked
    found = doc_status(a, "b:beta")
    assert (found.status, found.store, found.model, found.path) == ("ok", "b", "NoteDoc", "beta.md")
    assert doc_status(a, "b:NoteDoc/beta").exists
    assert doc_status(a, "b:alpha").status == "missing"
    assert doc_status(a, "local:alpha").exists


def test_a_bare_ref_never_leaves_the_local_store(linked):
    a, _ = linked
    assert doc_status(a, "beta").status == "missing"
    with pytest.raises(SLDBDocumentTargetError):
        resolve_runtime_doc(str(a), "beta", None)


def test_an_unknown_alias_is_told_apart_from_a_missing_doc(linked):
    a, b = linked
    assert doc_status(a, "nope:beta").status == "link-missing"
    shutil.rmtree(b)
    assert doc_status(a, "b:beta").status == "link-broken"


def test_an_unlinked_prefix_keeps_the_whole_ref_local(linked):
    a, _ = linked
    assert split_doc_ref(a, "nope:x") == (None, "nope:x")
    assert split_doc_ref(a, "b:x") == ("b", "x")
    assert split_doc_ref(a, "local:x") == (None, "x")


def test_checking_a_ref_does_not_import_its_model(linked):
    a, b = linked
    (b.parent / "linkref_models.py").unlink()
    assert doc_status(a, "b:beta").exists


def test_referencing_writes_nothing_to_the_store_that_asks(linked):
    a, _ = linked
    before = _index_bytes(a)
    doc_status(a, "b:beta")
    resolve_runtime_doc(str(a), "b:beta", None)
    assert _index_bytes(a) == before
    assert sldb_main(["docs", "list", "--store", str(a), "--format", "json"]) == 0


def test_links_in_both_directions_do_not_loop(linked):
    a, b = linked
    link_store(b, a, "a")
    assert doc_status(a, "b:beta").exists and doc_status(b, "a:alpha").exists
    assert doc_status(a, "b:a:alpha").status == "missing"


def test_docs_show_reads_a_linked_doc_from_its_own_project(linked):
    a, b = linked
    doc = resolve_runtime_doc(str(a), "b:beta", None)
    assert (doc["store"], doc["name"], doc["payload"]["body"]) == ("b", "beta", "body of beta")
    assert doc["absolute_path"] == str((b.parent / "beta.md").resolve())


@pytest.mark.parametrize(("ref", "code"), [("b:beta", 0), ("b:nope", 1), ("nope:beta", 5)])
def test_docs_exists_answers_with_its_exit_code(linked, capsys, ref: str, code: int):
    a, _ = linked
    assert sldb_main(["docs", "exists", ref, "--store", str(a), "--format", "json"]) == code
    assert json.loads(capsys.readouterr().out)["ref"] == ref
