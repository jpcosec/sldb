"""`sldb.api` document operations and the `sldb.cli` bridges over them."""

from __future__ import annotations

from types import SimpleNamespace

import pytest
from pydantic import ValidationError

import sldb.api as api
from sldb.cli import dict_utils
from sldb.cli.commands.fields_save import save_payload
from sldb.core.exceptions import SLDBError, SLDBPayloadSaveError, SLDBValidationError
from sldb.store.query import load_runtime_documents

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


def test_payload_paths_are_the_cli_helpers():
    assert dict_utils.deep_get is api.deep_get and dict_utils.deep_set is api.deep_set
    payload = {"items": [{"name": "a"}]}
    api.deep_set(payload, "items.0.name", "b")
    api.deep_set(payload, "meta.owner", "jp", create=True)
    assert api.deep_get(payload, "items.0.name") == "b"
    assert api.deep_delete(payload, "meta.owner") == {"items": [{"name": "b"}], "meta": {}}
    with pytest.raises(TypeError):
        api.ensure_list(payload, "meta")
