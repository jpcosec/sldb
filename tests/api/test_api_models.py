"""`sldb.api` model registry operations and the `sldb.cli` bridges over them."""

from __future__ import annotations

import pytest

from sldb.api import add_model, describe_model, load_registered_model, reindex_model
from sldb.cli.graph_ops import ast_for_target
from sldb.cli.model_utils import registered_model
from sldb.core.exceptions import SLDBModelError, SLDBStoreError
from sldb.store.io import load_store_index

from .conftest import MODULE


def test_add_model_refuses_an_already_registered_model(api_store):
    with pytest.raises(SLDBModelError, match="exists"):
        add_model(api_store.store, f"{MODULE}:TicketDoc", api_store.pythonpath)


def test_add_model_registers_version_one(api_store):
    registration = load_store_index(api_store.store).models[0]
    assert (registration.name, registration.version) == ("TicketDoc", 1)


def test_load_registered_model_keeps_the_entry_inside_the_store_index(api_store):
    registered = load_registered_model(api_store.store, "TicketDoc", api_store.pythonpath)
    assert registered.model_type.__name__ == "TicketDoc"
    assert any(entry is registered.entry for entry in registered.store_index.models)
    model_type, entry, idx = registered_model(api_store.store, "TicketDoc", api_store.pythonpath)
    assert (model_type, entry.name, len(idx.models)) == (registered.model_type, "TicketDoc", 1)


def test_load_registered_model_raises_for_an_unknown_model(api_store):
    with pytest.raises(SLDBStoreError, match="not registered"):
        load_registered_model(api_store.store, "NopeDoc", api_store.pythonpath)


def test_describe_model_matches_the_models_show_ast(api_store):
    description = describe_model(api_store.store, "TicketDoc", api_store.pythonpath)
    expected = ast_for_target(str(api_store.store), api_store.pythonpath, "models/TicketDoc")["model"]
    assert description.model_dump() == expected
    assert [d.name for d in description.documents] == ["login"]


def test_reindex_model_bumps_the_version_only_when_asked(api_store):
    assert reindex_model(api_store.store, "TicketDoc", api_store.pythonpath).version == 1
    assert reindex_model(api_store.store, "TicketDoc", api_store.pythonpath, bump_version=True).version == 2
    with pytest.raises(SLDBModelError, match="not found"):
        reindex_model(api_store.store, "NopeDoc", api_store.pythonpath)
