"""`sldb.api` creation operations: a new store, a new document; and the `sldb.cli` commands over them."""

from __future__ import annotations

import json

import pytest
from pydantic import ValidationError

import sldb.api as api
from sldb.cli import main as cli_main
from sldb.core.exceptions import SLDBError, SLDBStoreError, SLDBValidationError
from sldb.store.io import load_store_index

from .conftest import PAYLOAD


@pytest.fixture
def home(tmp_path, monkeypatch):
    """A throwaway HOME, so the global store catalog written by init is the test's own."""
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    return tmp_path / "home"


def test_init_store_creates_an_empty_store_registered_in_the_global_catalog(tmp_path, home):
    project = home / "project"
    created = api.init_store(project)
    assert (created.store_path, created.project_root) == ((project / ".sldb").resolve(), project.resolve())
    index = load_store_index(created.store_path)
    assert index.models == [] and index.stores == [] and index.predicates
    assert [(s.name, s.path) for s in load_store_index(home / ".sldb").stores] == [("project", str(created.store_path))]


def test_init_store_refuses_an_existing_store_unless_forced(tmp_path, home):
    api.init_store(tmp_path, force=False)
    api.link_store(tmp_path / ".sldb", api.init_store(tmp_path / "other").store_path, "other")
    with pytest.raises(SLDBStoreError, match="already exists"):
        api.init_store(tmp_path)
    assert load_store_index(tmp_path / ".sldb").stores != []
    api.init_store(tmp_path, force=True)
    assert load_store_index(tmp_path / ".sldb").stores == []


def test_cli_stores_init_still_exits_zero_on_an_existing_store(tmp_path, home, capsys):
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert cli_main(["stores", "init", "--path", str(tmp_path)]) == 0
    assert "Use --force to reinitialize." in capsys.readouterr().out


def test_create_document_writes_markdown_and_tracks_it(api_store):
    created = api.create_document(api_store.store, "TicketDoc", "tickets/signup.md", {**PAYLOAD, "title": "Signup"}, pythonpath=api_store.pythonpath)
    assert (created.model, created.name, created.path) == ("TicketDoc", "signup", (api_store.root / "tickets" / "signup.md").resolve())
    assert "# Signup" in created.path.read_text(encoding="utf-8")
    assert api.untrack_document(api_store.store, "signup", api_store.pythonpath).name == "signup"


def test_create_document_writes_nothing_for_a_payload_the_model_rejects(api_store):
    out = api_store.root / "bad.md"
    with pytest.raises((SLDBValidationError, ValidationError)):
        api.create_document(api_store.store, "TicketDoc", out, {**PAYLOAD, "status": "pending"}, "bad", api_store.pythonpath)
    assert not out.exists()
    with pytest.raises(SLDBError, match="NopeDoc"):
        api.create_document(api_store.store, "NopeDoc", out, PAYLOAD, "bad", api_store.pythonpath)
    assert not out.exists()


def test_cli_docs_create_names_the_document(api_store, capsys):
    argv = ["docs", "create", "--model", "TicketDoc", "-o", "cli.md", "--name", "from-cli", json.dumps(PAYLOAD), "--store", str(api_store.store), "--pythonpath", api_store.pythonpath]
    assert cli_main(argv) == 0
    assert "Created and tracked 'from-cli'" in capsys.readouterr().out
    assert api.untrack_document(api_store.store, "from-cli", api_store.pythonpath).path == (api_store.root / "cli.md").resolve()
