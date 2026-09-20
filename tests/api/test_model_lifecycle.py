"""The model lifecycle: journaled draft edits, schema diffs, backfill and create_model."""

from __future__ import annotations

import pytest

import sldb.api as api
from sldb.api.documents.payload_diff import changed_paths
from sldb.core.exceptions import SLDBValidationError

from .conftest import MODULE, PAYLOAD


def _entries(store, operation):
    return [e for e in api.journal(store) if e.operation == operation]


def test_draft_edits_leave_journal_entries(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    api.remove_model_field(api_store.store, "TicketDoc", "priority", api_store.pythonpath)
    api.edit_model_template(api_store.store, "TicketDoc", "# Ticket ⸢rev•title⸥\n", api_store.pythonpath)
    ops = {e.operation for e in api.journal(api_store.store)}
    assert {"add_model_field", "remove_model_field", "edit_model_template"} <= ops
    add = _entries(api_store.store, "add_model_field")[0]
    assert (add.address, add.field) == ("TicketDoc", "priority") and add.new_value is not None
    remove = _entries(api_store.store, "remove_model_field")[0]
    assert (remove.address, remove.field) == ("TicketDoc", "priority") and remove.previous_value is not None
    template = _entries(api_store.store, "edit_model_template")[0]
    assert template.address == "TicketDoc" and template.field == "__template__"


def test_promote_entry_carries_schema_before_and_after(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    entry = _entries(api_store.store, "promote_model_draft")[0]
    assert entry.previous_value["version"] == 1 and entry.new_value["version"] == 2
    before, after = {f["name"] for f in entry.previous_value["fields"]}, {f["name"] for f in entry.new_value["fields"]}
    assert "priority" not in before and "priority" in after
    assert all("required" in f and "description" in f for f in entry.new_value["fields"])


def test_reindex_entry_carries_schema(api_store):
    api.reindex_model(api_store.store, "TicketDoc", api_store.pythonpath)
    entry = _entries(api_store.store, "reindex_model")[0]
    assert entry.previous_value["version"] == 1 and entry.new_value["version"] == 1
    assert entry.previous_value["fields"] == entry.new_value["fields"]


def test_save_entry_derives_field(api_store):
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "title": "New"}, api_store.pythonpath)
    entry = api.journal(api_store.store, limit=1)[0]
    assert entry.field == "title"


def test_changed_paths_include_dotted_nested_keys():
    assert changed_paths({"a": {"b": 1}}, {"a": {"b": 2}}) == ["a.b"]
    assert changed_paths({"a": 1}, {"a": 1, "b": 2}) == ["b"]


def test_add_model_field_empty_string_default_is_a_real_default(api_store):
    draft = api.add_model_field(api_store.store, "TicketDoc", "note", "str", "note desc", "", api_store.pythonpath)
    assert "note: str = Field(default='', description='note desc')" in draft.draft_path.read_text(encoding="utf-8")
    report = api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert report.promoted and report.version == 2


def test_promote_required_field_without_default_is_rejected_with_clear_error(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "note", "str", "note desc", None, api_store.pythonpath)
    with pytest.raises(SLDBValidationError, match="lacks required field"):
        api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)


def _add_note_field_and_section(api_store, default='"pending"'):
    model_type = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    api.add_model_field(api_store.store, "TicketDoc", "note", "str", "note desc", default, api_store.pythonpath)
    api.edit_model_template(api_store.store, "TicketDoc", model_type.__template__ + "\n\n## Note\n\n⸢rev•note⸥\n", api_store.pythonpath)


def test_dry_run_reports_backfill_documents(api_store):
    _add_note_field_and_section(api_store)
    report = api.validate_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert report.backfill == ["login"]


def test_promote_without_backfill_leaves_document_unchanged(api_store, tmp_path):
    _add_note_field_and_section(api_store)
    api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert "## Note" not in (api_store.root / "login.md").read_text(encoding="utf-8")


def test_promote_with_backfill_rewrites_documents(api_store):
    _add_note_field_and_section(api_store)
    report = api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath, backfill=True)
    assert report.version == 2
    text = (api_store.root / "login.md").read_text(encoding="utf-8")
    assert "## Note\n\npending" in text
    entry = _entries(api_store.store, "backfill_document")[0]
    assert (entry.address, entry.field) == ("TicketDoc:login", "note")
    assert entry.previous_value.get("note") is None and entry.new_value["note"] == "pending"
    assert api.verify_journal(api_store.store).valid


def test_create_model_end_to_end(tmp_path):
    root = tmp_path / "repo"
    root.mkdir()
    api.init_store(root)
    store = root / ".sldb"
    registration = api.create_model(
        store,
        "Dish",
        [{"name": "title", "type": "str", "description": "Title."}, {"name": "price", "type": "int", "description": "Price."}],
        pythonpath=str(tmp_path),
    )
    assert (registration.name, registration.version) == ("Dish", 1)
    document = api.create_document(store, "Dish", "dish.md", {"title": "Soup", "price": 3}, pythonpath=str(tmp_path))
    assert document.model == "Dish"
    ops = {e.operation for e in api.journal(store)}
    assert {"create_model", "add_model", "create_document"} <= ops
    assert api.verify_journal(store).valid
