"""`sldb.api.select_documents`: one rule to choose tracked documents by ref, prefix, path glob,
model family and predicate (GD23). The store: two models (`ChildDoc` extends `BaseDoc`) in two
folders, a linked store with a document of the same name, and a link of that link."""

from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest
from pydantic import ValidationError

from sldb.api import AmbiguousSelectionError, Selector, add_model, init_store, link_store, resolve_model_ref, select_documents, track_document_file
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBDocumentTargetError
from sldb.runtime.validation import Validator, render_model_markdown
from sldb.store.query import find_structural, glob_structural
from sldb.store.query_engine.where_parse import WherePredicateError

MODULE = "sldb_select_test_models"
MODELS_SOURCE = '''from pydantic import Field
from sldb import StructuredNLDoc


class BaseDoc(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nStatus: ⸢rev•status⸥"
    title: str = Field(description="Title.")
    status: str = Field(description="State.")


class ChildDoc(BaseDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nStatus: ⸢rev•status⸥\\n\\nOwner: ⸢rev•owner⸥"
    owner: str = Field(description="Owner.")
'''
LOCAL = [("BaseDoc", "task-a", "task-a.md", "open"), ("BaseDoc", "task-ab", "task-ab.md", "closed"),
         ("ChildDoc", "task-b", "sub/task-b.md", "open"), ("ChildDoc", "note", "sub/deep/note.md", "closed")]


def _write(root: Path, pythonpath: str, model: str, name: str, rel: str, status: str) -> None:
    payload = {"title": name.title(), "status": status, **({"owner": "me"} if model == "ChildDoc" else {})}
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_model_markdown(resolve_model_ref(f"{MODULE}:{model}", pythonpath), payload) + "\n", encoding="utf-8")
    track_document_file(root / ".sldb", model, path, name, pythonpath)


def _store(root: Path, pythonpath: str, docs: list[tuple[str, str, str, str]]) -> Path:
    root.mkdir()
    init_store(root)
    for model in ("BaseDoc", "ChildDoc"):
        add_model(root / ".sldb", f"{MODULE}:{model}", pythonpath)
    for model, name, rel, status in docs:
        _write(root, pythonpath, model, name, rel, status)
    return root / ".sldb"


@pytest.fixture
def store(tmp_path: Path) -> Path:
    sys.modules.pop(MODULE, None)
    (tmp_path / f"{MODULE}.py").write_text(MODELS_SOURCE, encoding="utf-8")
    pythonpath = str(tmp_path)
    local = _store(tmp_path / "repo", pythonpath, LOCAL)
    other = _store(tmp_path / "other", pythonpath, [("BaseDoc", "task-a", "task-a.md", "open"), ("BaseDoc", "remote", "remote.md", "closed")])
    third = _store(tmp_path / "third", pythonpath, [("BaseDoc", "far", "far.md", "open")])
    link_store(other, third, "third")
    link_store(local, other, "other")
    yield local
    sys.modules.pop(MODULE, None)


def _ids(rows: list[dict]) -> list[str]:
    return [row["export_id"] for row in rows]


def test_a_unique_prefix_resolves_to_one_document(store):
    assert select_documents(store, {"prefix": "task-b"}, expect="one") == [{"export_id": "ChildDoc:task-b", "model": "ChildDoc", "name": "task-b", "path": "sub/task-b.md"}]
    assert _ids(select_documents(store, {"prefix": "no"}, expect="one")) == ["ChildDoc:note"]


def test_an_ambiguous_prefix_fails_listing_its_candidates(store):
    with pytest.raises(AmbiguousSelectionError, match="Ambiguous selection prefix='task-': ChildDoc:task-b, BaseDoc:task-a, BaseDoc:task-ab") as raised:
        select_documents(store, {"prefix": "task-"}, expect="one")
    assert raised.value.candidates == ["ChildDoc:task-b", "BaseDoc:task-a", "BaseDoc:task-ab"]
    assert isinstance(raised.value, SLDBDocumentTargetError)


def test_an_exact_name_wins_over_the_prefix_matches_only_when_one_is_expected(store):
    assert _ids(select_documents(store, {"prefix": "task-a"}, expect="one")) == ["BaseDoc:task-a"]
    assert _ids(select_documents(store, {"prefix": "task-a"})) == ["BaseDoc:task-a", "BaseDoc:task-ab"]


def test_a_path_glob_keeps_only_the_subfolder_at_any_depth(store):
    assert _ids(select_documents(store, {"path_glob": "sub/**/*.md"})) == ["ChildDoc:note", "ChildDoc:task-b"]
    assert _ids(select_documents(store, {"path_glob": "*.md"})) == ["BaseDoc:task-a", "BaseDoc:task-ab"]


def test_a_model_names_its_whole_family(store):
    assert _ids(select_documents(store, {"model": "BaseDoc"})) == ["ChildDoc:note", "ChildDoc:task-b", "BaseDoc:task-a", "BaseDoc:task-ab"]
    assert _ids(select_documents(store, {"model": "ChildDoc"})) == ["ChildDoc:note", "ChildDoc:task-b"]


def test_where_reads_the_index_projection_and_never_extracts(store, monkeypatch):
    calls: list[str] = []
    original = Validator.extract
    monkeypatch.setattr(Validator, "extract", lambda self, markdown: calls.append(markdown) or original(self, markdown))
    assert _ids(select_documents(store, {"where": 'status = "open"'})) == ["ChildDoc:task-b", "BaseDoc:task-a"]
    assert _ids(select_documents(store, {"where": "model <= ChildDoc and has(owner)"})) == ["ChildDoc:note", "ChildDoc:task-b"]
    assert calls == []


def test_the_keys_combine_by_conjunction(store):
    selector = {"model": "BaseDoc", "path_glob": "sub/**/*.md", "where": 'status = "open"', "prefix": "task"}
    assert _ids(select_documents(store, selector, expect="one")) == ["ChildDoc:task-b"]
    assert select_documents(store, {**selector, "ref": "note"}) == []


def test_one_with_no_match_is_the_unknown_document_error(store):
    with pytest.raises(SLDBDocumentTargetError, match="Unknown document: prefix='zzz', model='BaseDoc'"):
        select_documents(store, {"prefix": "zzz", "model": "BaseDoc"}, expect="one")


def test_ref_accepts_what_doc_status_accepts_and_stays_in_the_local_store(store):
    for ref in ("task-a", "BaseDoc/task-a", "BaseDoc:task-a", "task-a.md", "local:task-a"):
        assert _ids(select_documents(store, {"ref": ref}, expect="one")) == ["BaseDoc:task-a"], ref
    assert _ids(select_documents(store, Selector(ref="sub/task-b.md"))) == ["ChildDoc:task-b"]


def test_include_linked_adds_the_direct_links_after_the_local_rows_and_is_not_transitive(store):
    rows = select_documents(store, {"include_linked": True})
    assert _ids(rows) == ["ChildDoc:note", "ChildDoc:task-b", "BaseDoc:task-a", "BaseDoc:task-ab", "other:BaseDoc:remote", "other:BaseDoc:task-a"]
    assert rows[-1] == {"export_id": "other:BaseDoc:task-a", "model": "BaseDoc", "name": "task-a", "path": "task-a.md"}
    assert _ids(select_documents(store, {"include_linked": True, "prefix": "task-a"})) == ["BaseDoc:task-a", "BaseDoc:task-ab", "other:BaseDoc:task-a"]
    assert _ids(select_documents(store, {"include_linked": True, "where": 'status = "closed"', "model": "BaseDoc"})) == ["ChildDoc:note", "BaseDoc:task-ab", "other:BaseDoc:remote"]


def test_a_ref_with_an_explicit_alias_reaches_that_link_without_include_linked(store):
    assert _ids(select_documents(store, {"ref": "other:task-a"}, expect="one")) == ["other:BaseDoc:task-a"]
    assert _ids(select_documents(store, {"ref": "other:BaseDoc:remote", "model": "BaseDoc"})) == ["other:BaseDoc:remote"]
    assert select_documents(store, {"ref": "third:far"}) == []
    with pytest.raises(SLDBDocumentTargetError, match="Unknown document: ref='nope:task-a'"):
        select_documents(store, {"ref": "nope:task-a"}, expect="one")


@pytest.mark.parametrize("selector", [{"prefix": ""}, {"where": "   "}, {"name": "task-a"}, {"ref": None, "model": ""}])
def test_a_blank_key_or_an_unknown_one_is_rejected(store, selector):
    with pytest.raises(ValidationError):
        select_documents(store, selector)


def test_an_unparseable_where_and_a_bad_expect_are_refused(store):
    with pytest.raises(WherePredicateError, match="bogus predicate"):
        select_documents(store, {"where": "bogus predicate"})
    with pytest.raises(ValueError, match="expect must be one of"):
        select_documents(store, {"prefix": "task"}, expect="all")


def test_glob_and_find_choose_through_the_selection_and_keep_their_addresses(store, tmp_path):
    pythonpath = str(tmp_path)
    assert glob_structural(store, "st.{BaseDoc+}.task-*", resolve_model_ref, pythonpath) == ["st.{BaseDoc+}.task-a", "st.{BaseDoc+}.task-ab", "st.{BaseDoc+}.task-b"]
    assert glob_structural(store, "st.{BaseDoc}.task-*", resolve_model_ref, pythonpath) == ["st.{BaseDoc}.task-a", "st.{BaseDoc}.task-ab"]
    assert glob_structural(store, "st.{ChildDoc}.note.*", resolve_model_ref, pythonpath) == ["st.{ChildDoc}.note.owner", "st.{ChildDoc}.note.status", "st.{ChildDoc}.note.title"]
    assert find_structural(store, "st.{BaseDoc+}", 'status = "open"', resolve_model_ref, pythonpath) == ["st.{BaseDoc+}.task-a", "st.{BaseDoc+}.task-b"]
    assert find_structural(store, "other:st.{BaseDoc}", 'status = "open"', resolve_model_ref, pythonpath) == ["other:st.{BaseDoc}.task-a"]


def test_the_cli_selects_with_flags_and_reports_the_errors_in_the_envelope(store, capsys):
    assert cli_main(["docs", "select", "--prefix", "task-b", "--one", "--format", "json", "--store", str(store)]) == 0
    assert json.loads(capsys.readouterr().out) == {"selector": {"prefix": "task-b"}, "expect": "one", "documents": [{"export_id": "ChildDoc:task-b", "model": "ChildDoc", "name": "task-b", "path": "sub/task-b.md"}]}
    assert cli_main(["docs", "select", "--model", "BaseDoc", "--path-glob", "sub/**/*.md", "--store", str(store)]) == 0
    assert capsys.readouterr().out == "ChildDoc:note -> sub/deep/note.md\nChildDoc:task-b -> sub/task-b.md\n"
    with pytest.raises(SystemExit, match="Ambiguous selection prefix='task-': ChildDoc:task-b, BaseDoc:task-a, BaseDoc:task-ab"):
        cli_main(["docs", "select", "--prefix", "task-", "--one", "--store", str(store)])
    assert cli_main(["--envelope", "docs", "select", "--prefix", "zzz", "--one", "--store", str(store)]) == 1
    envelope = json.loads(capsys.readouterr().out)
    assert (envelope["ok"], envelope["error"]["type"], envelope["error"]["message"]) == (False, "docs/missing", "Unknown document: prefix='zzz'")
