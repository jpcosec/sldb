"""`Model:name` finds a document tracked under a submodel of Model.

An instance of a submodel is an instance of its bases (`extends`). A consumer asking for
`NoteDoc:x` must find the document tracked as `MemoNoteDoc:x` without its own family logic.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest

from sldb.api import AmbiguousDocument, add_model, init_store, resolve_indexed_document, track_document_file
from sldb.store.io import invalidate_index_cache
from sldb.store.runtime_cache import invalidate_runtime_cache

MODULE = "sldb_family_resolve_models"
_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class NoteDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥"""
    title: str = Field(description="Note title.")


class MemoNoteDoc(NoteDoc):
    pass


class DraftMemoNoteDoc(MemoNoteDoc):
    pass


class LetterNoteDoc(NoteDoc):
    pass


class OtherDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥"""
    title: str = Field(description="Title.")
'''


@pytest.fixture
def store(tmp_path):
    (tmp_path / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    sp = init_store(tmp_path).store_path
    for model in ("NoteDoc", "MemoNoteDoc", "DraftMemoNoteDoc", "LetterNoteDoc", "OtherDoc"):
        add_model(sp, f"{MODULE}:{model}", str(tmp_path))
    yield tmp_path, sp
    sys.modules.pop(MODULE, None)
    while str(tmp_path) in sys.path:
        sys.path.remove(str(tmp_path))
    invalidate_index_cache()
    invalidate_runtime_cache()


def _track(root: Path, sp: Path, model: str, name: str) -> None:
    path = root / f"{model}-{name}.md"
    path.write_text("# A title\n", encoding="utf-8")
    track_document_file(sp, model, path, name, str(root))


def test_a_base_model_finds_the_document_of_a_submodel(store):
    root, sp = store
    _track(root, sp, "MemoNoteDoc", "x")
    found = resolve_indexed_document(sp, "NoteDoc", "x")
    assert found == {"name": "x", "model": "MemoNoteDoc", "path": "MemoNoteDoc-x.md"}


def test_the_family_reaches_more_than_one_level(store):
    root, sp = store
    _track(root, sp, "DraftMemoNoteDoc", "deep")
    assert resolve_indexed_document(sp, "NoteDoc", "deep")["model"] == "DraftMemoNoteDoc"
    assert resolve_indexed_document(sp, "MemoNoteDoc", "deep")["model"] == "DraftMemoNoteDoc"


def test_the_own_model_is_an_exact_match(store):
    root, sp = store
    _track(root, sp, "MemoNoteDoc", "x")
    assert resolve_indexed_document(sp, "MemoNoteDoc", "x")["model"] == "MemoNoteDoc"


def test_an_exact_match_wins_over_a_submodel(store):
    root, sp = store
    _track(root, sp, "NoteDoc", "same")
    _track(root, sp, "MemoNoteDoc", "same")
    assert resolve_indexed_document(sp, "NoteDoc", "same")["model"] == "NoteDoc"


def test_a_submodel_does_not_find_its_base_or_an_unrelated_model(store):
    root, sp = store
    _track(root, sp, "NoteDoc", "base-only")
    _track(root, sp, "OtherDoc", "other")
    assert resolve_indexed_document(sp, "MemoNoteDoc", "base-only") is None
    assert resolve_indexed_document(sp, "NoteDoc", "other") is None
    assert resolve_indexed_document(sp, "NoteDoc", "missing") is None


def test_two_submodels_with_the_same_name_are_ambiguous(store):
    root, sp = store
    _track(root, sp, "MemoNoteDoc", "twin")
    _track(root, sp, "LetterNoteDoc", "twin")
    with pytest.raises(AmbiguousDocument) as exc:
        resolve_indexed_document(sp, "NoteDoc", "twin")
    assert exc.value.models == ["LetterNoteDoc", "MemoNoteDoc"]
    assert "MemoNoteDoc:twin" in str(exc.value)


def test_an_inherited_submodel_is_found_through_its_owners_bases(tmp_path):
    """The repo inherits the models from the store that owns them (as desks inherit deskops'):
    the local index keeps no `base_models`; the owner's does."""
    from sldb.api import inherit_model, link_store

    owner, local = tmp_path / "owner", tmp_path / "repo"
    owner.mkdir(), local.mkdir()
    (owner / f"{MODULE}.py").write_text(_MODELS, encoding="utf-8")
    owner_sp, local_sp = init_store(owner).store_path, init_store(local).store_path
    try:
        for model in ("NoteDoc", "MemoNoteDoc"):
            add_model(owner_sp, f"{MODULE}:{model}", str(owner))
        link_store(local_sp, owner_sp, "owner")
        for model in ("NoteDoc", "MemoNoteDoc"):
            inherit_model(local_sp, f"owner:{model}")
        _track(local, local_sp, "MemoNoteDoc", "x")
        assert resolve_indexed_document(local_sp, "NoteDoc", "x")["model"] == "MemoNoteDoc"
    finally:
        sys.modules.pop(MODULE, None)
        while str(owner) in sys.path:
            sys.path.remove(str(owner))
        invalidate_index_cache()
        invalidate_runtime_cache()
