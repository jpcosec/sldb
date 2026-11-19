"""`sldb.api` document operations and the `sldb.cli` bridges over them."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

import sldb.api as api
from sldb.api.stores.declare_store import declare_store
from sldb.api.stores.store_declaration import save_declaration
from sldb.cli import dict_utils
from sldb.cli.commands.fields_save import save_payload
from sldb.core.exceptions import SLDBError, SLDBPayloadSaveError, SLDBStoreError, SLDBValidationError
from sldb.store.query import load_runtime_documents

from tests.store.invalid_memo_store import store_with_invalid  # noqa: F401 - the fixture

from .conftest import PAYLOAD


def _title(api_store, name: str) -> str:
    docs = load_runtime_documents(api_store.store, api.resolve_model_ref, api_store.pythonpath)
    return next(d.payload["title"] for d in docs if d.name == name)


def test_save_document_payload_rewrites_markdown_and_indexes(api_store):
    saved = api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "Fixed login"}, api_store.pythonpath)
    assert saved.path.resolve() == (api_store.root / "login.md").resolve()
    assert "# Fixed login" in saved.path.read_text(encoding="utf-8")
    api.open_store(api_store.store)
    assert _title(api_store, "login") == "Fixed login"


def test_save_document_payload_refuses_unknown_documents_and_models(api_store):
    with pytest.raises(SLDBPayloadSaveError, match="Doc 'ghost' not registered."):
        api.save_document_payload(api_store.store, "TicketDoc", "ghost", PAYLOAD, api_store.pythonpath)
    with pytest.raises(SLDBPayloadSaveError, match="Model 'NopeDoc' not registered."):
        api.save_document_payload(api_store.store, "NopeDoc", "login", PAYLOAD, api_store.pythonpath)


def test_cli_save_payload_still_exits_with_the_message(api_store):
    doc = SimpleNamespace(model_name="TicketDoc", name="ghost")
    with pytest.raises(SystemExit, match="Doc 'ghost' not registered."):
        save_payload(doc, PAYLOAD, str(api_store.store), api_store.pythonpath)


def test_track_document_file_refuses_a_file_the_model_cannot_read(api_store):
    (api_store.root / "broken.md").write_text("not a ticket\n", encoding="utf-8")
    with pytest.raises((SLDBValidationError, ValidationError)):
        api.track_document_file(api_store.store, "TicketDoc", "broken.md", pythonpath=api_store.pythonpath)


def test_track_document_file_resolves_relative_paths_against_the_project_root(api_store):
    api_store.write_document("signup", PAYLOAD)
    tracked = api.track_document_file(api_store.store, "TicketDoc", "signup.md", pythonpath=api_store.pythonpath, force=True)
    assert (tracked.model, tracked.name, tracked.path) == ("TicketDoc", "signup", (api_store.root / "signup.md").resolve())


def test_untrack_document_drops_it_from_the_store(api_store):
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    untracked = api.untrack_document(api_store.store, "signup", api_store.pythonpath)
    assert (untracked.model, untracked.name) == ("TicketDoc", "signup")
    assert (api_store.root / "signup.md").exists()
    with pytest.raises(SLDBError, match="not found"):
        api.untrack_document(api_store.store, "signup", api_store.pythonpath)


def test_a_document_can_be_named_by_its_absolute_path(api_store):
    """The store records paths relative to the project root; an absolute one used to miss."""
    path = (api_store.root / "signup.md").resolve()
    api.track_document_file(api_store.store, "TicketDoc", api_store.write_document("signup", PAYLOAD), pythonpath=api_store.pythonpath)
    deleted = api.delete_document(api_store.store, str(path), api_store.pythonpath)
    assert (deleted.model, deleted.name) == ("TicketDoc", "signup")
    assert not path.exists()


def test_payload_paths_are_the_cli_helpers():
    assert dict_utils.deep_get is api.deep_get and dict_utils.deep_set is api.deep_set
    payload = {"items": [{"name": "a"}]}
    api.deep_set(payload, "items.0.name", "b")
    api.deep_set(payload, "meta.owner", "jp", create=True)
    assert api.deep_get(payload, "items.0.name") == "b"
    assert api.deep_delete(payload, "meta.owner") == {"items": [{"name": "b"}], "meta": {}}
    with pytest.raises(TypeError):
        api.ensure_list(payload, "meta")


def test_move_document_moves_the_file_and_keeps_the_name(api_store):
    moved = api.move_document(api_store.store, "login", "tickets/login.md", api_store.pythonpath)
    assert (moved.model, moved.name, moved.path) == ("TicketDoc", "login", (api_store.root / "tickets" / "login.md").resolve())
    assert not (api_store.root / "login.md").exists()
    assert api.doc_status(api_store.store, "login").exists
    assert _title(api_store, "login") == "Broken login"


def test_move_document_refuses_a_taken_destination_without_moving(api_store):
    (api_store.root / "taken.md").write_text("# Taken\n", encoding="utf-8")
    with pytest.raises(SLDBStoreError, match="already exists"):
        api.move_document(api_store.store, "login", "taken.md", api_store.pythonpath)
    assert (api_store.root / "login.md").exists()


def test_load_runtime_documents_skip_returns_the_sound_ones_and_names_the_invalid(store_with_invalid):
    root, sp, py = store_with_invalid
    loaded = api.load_runtime_documents(sp, py, on_invalid="skip")
    assert isinstance(loaded, api.RuntimeDocuments)
    assert [d.name for d in loaded.documents] == ["c"]
    assert [(i.path, i.model) for i in loaded.invalid] == [("a.md", "Memo"), ("b.md", "Memo")]
    assert all(isinstance(i, api.InvalidDocument) and "status bad is not a status" in i.error for i in loaded.invalid)


def test_load_runtime_documents_raise_names_the_path_of_the_invalid_document(store_with_invalid):
    root, sp, py = store_with_invalid
    with pytest.raises(SLDBValidationError, match=r"(?s)^a\.md:.*status bad is not a status") as raised:
        api.load_runtime_documents(sp, py)
    assert isinstance(raised.value.__cause__, ValidationError)


def test_load_runtime_documents_default_still_returns_a_list(api_store):
    docs = api.load_runtime_documents(api_store.store, api_store.pythonpath)
    assert isinstance(docs, list) and docs
    skipped = api.load_runtime_documents(api_store.store, api_store.pythonpath, on_invalid="skip")
    assert [d.name for d in skipped.documents] == [d.name for d in docs] and skipped.invalid == []


def _retrack(api_store, path="login.md", force=True):
    return api.track_document_file(api_store.store, "TicketDoc", path, "login", api_store.pythonpath, force=force)


def test_track_force_reindexes_a_document_already_tracked_at_the_same_path(api_store):
    """sldb-ui saves the file and re-tracks it with --force (inbox 20261116-162239)."""
    api_store.write_document("login", {**PAYLOAD, "title": "Edited outside"})
    assert _retrack(api_store).name == "login"
    assert _title(api_store, "login") == "Edited outside"
    report = api.check_store(api_store.store, api_store.root, api_store.pythonpath)
    assert report["ok"], report


def test_track_without_force_still_refuses_a_document_already_tracked(api_store):
    with pytest.raises(SLDBStoreError, match="Doc 'login' already tracked."):
        _retrack(api_store, force=False)


def test_track_force_refuses_a_document_tracked_at_another_path_and_names_both(api_store):
    api_store.write_document("other", PAYLOAD)
    with pytest.raises(SLDBStoreError, match=r"already tracked at 'login\.md', not 'other\.md'"):
        _retrack(api_store, "other.md")
    assert _title(api_store, "login") == "Broken login"


def _index_state(api_store):
    return sorted((str(p), p.read_bytes()) for p in api_store.store.rglob("*.yaml") if p.name != "store.yaml")


def test_track_force_twice_without_changes_is_idempotent(api_store):
    """declare_tracked neither duplicates the path nor rewrites store.yaml."""
    declaration = save_declaration(api_store.store, declare_store(api_store.store, api_store.root))
    before = declaration.read_bytes()
    _retrack(api_store)
    state = _index_state(api_store)
    _retrack(api_store)
    assert _index_state(api_store) == state and declaration.read_bytes() == before
    assert before.count(b"login.md") <= 1
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]


def _reindex(api_store, **kw):
    return api.track_document_file(api_store.store, "TicketDoc", "login.md", "login", api_store.pythonpath, reindex=True, **kw)


def test_track_reindex_reindexes_a_valid_edited_file(api_store):
    api_store.write_document("login", {**PAYLOAD, "title": "Edited for reindex"})
    assert _reindex(api_store).name == "login"
    assert _title(api_store, "login") == "Edited for reindex"
    assert api.check_store(api_store.store, api_store.root, api_store.pythonpath)["ok"]


def test_track_reindex_of_an_invalid_file_fails_and_leaves_the_index_as_it_was(api_store):
    (api_store.root / "login.md").write_text("---\n: [broken\n---\n\n# nope\n", encoding="utf-8")
    before = _index_state(api_store)
    with pytest.raises((SLDBValidationError, ValidationError)):  # the same error a normal track gives
        _reindex(api_store)
    assert _index_state(api_store) == before
    _retrack(api_store)  # --force still skips the validation


def test_track_reindex_on_an_untracked_document_behaves_as_track(api_store):
    api_store.write_document("fresh", PAYLOAD)
    tracked = api.track_document_file(api_store.store, "TicketDoc", "fresh.md", pythonpath=api_store.pythonpath, reindex=True)
    assert tracked.name == "fresh"


def test_track_reindex_with_force_is_refused_clearly(api_store):
    with pytest.raises(SLDBError, match="--reindex and --force cannot be combined"):
        _reindex(api_store, force=True)
