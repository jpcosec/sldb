"""The model lifecycle: draft edits, schema diffs, backfill and create_model."""

from __future__ import annotations

import pytest

import sldb.api as api
from sldb.api.documents.payload_diff import changed_paths
from sldb.api.model_drafts.template_sections import section_for_field
from sldb.core.exceptions import SLDBValidationError
from sldb.runtime.validation import extract_model_data

from .conftest import MODULE, PAYLOAD


def test_draft_edits_rewrite_the_draft_and_leave_the_installed_model_alone(api_store):
    draft = api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath).draft_path
    assert "priority" in draft.read_text(encoding="utf-8")
    api.remove_model_field(api_store.store, "TicketDoc", "priority", api_store.pythonpath)
    assert "priority" not in draft.read_text(encoding="utf-8")
    api.edit_model_template(api_store.store, "TicketDoc", "# Ticket ⸢rev•title⸥\n", api_store.pythonpath)
    assert "# Ticket ⸢rev•title⸥" in draft.read_text(encoding="utf-8")
    assert "# Ticket ⸢rev•title⸥" not in (api_store.root.parent / f"{MODULE}.py").read_text(encoding="utf-8")


def test_promote_bumps_the_version_and_installs_the_field(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    report = api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert (report.promoted, report.version) == (True, 2)
    assert "priority" in api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath).model_fields


def test_reindex_keeps_the_version(api_store):
    assert api.reindex_model(api_store.store, "TicketDoc", api_store.pythonpath).version == 1


def test_changed_paths_include_dotted_nested_keys():
    assert changed_paths({"a": {"b": 1}}, {"a": {"b": 2}}) == ["a.b"]
    assert changed_paths({"a": 1}, {"a": 1, "b": 2}) == ["b"]


def test_add_model_field_adds_the_template_marker(api_store):
    draft = api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    text = draft.draft_path.read_text(encoding="utf-8")
    assert "## Priority" in text and "⸢optrev•priority⸥" in text


def test_add_model_field_required_uses_rev_marker(api_store):
    draft = api.add_model_field(api_store.store, "TicketDoc", "note", "str", "x", None, api_store.pythonpath)
    assert "⸢rev•note⸥" in draft.draft_path.read_text(encoding="utf-8")


def test_section_markers_match_the_field_annotation():
    assert "⸢rev•title⸥" in section_for_field("title", "str")
    assert "- ⸢rev,list•labels⸥" in section_for_field("labels", "list[str]")
    assert "⸢rev,dict•meta⸥" in section_for_field("meta", "dict")
    assert "⸢rev,table•tasks⸥" in section_for_field("tasks", "list[dict[str, str]]")


def test_add_model_field_empty_string_default_is_a_real_default(api_store):
    draft = api.add_model_field(api_store.store, "TicketDoc", "note", "str", "note desc", "", api_store.pythonpath)
    assert "note: str = Field(default='', description='note desc')" in draft.draft_path.read_text(encoding="utf-8")
    report = api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert report.promoted and report.version == 2


def test_promote_required_field_without_default_is_rejected_with_clear_error(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "note", "str", "note desc", None, api_store.pythonpath)
    with pytest.raises(SLDBValidationError, match="lacks required field"):
        api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)


def _add_note_field(api_store, default='"pending"'):
    api.add_model_field(api_store.store, "TicketDoc", "note", "str", "note desc", default, api_store.pythonpath)


def test_dry_run_reports_backfill_documents(api_store):
    _add_note_field(api_store)
    report = api.validate_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert report.backfill == ["login"]


def test_promote_without_backfill_leaves_document_unchanged(api_store):
    _add_note_field(api_store)
    api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert "## Note" not in (api_store.root / "login.md").read_text(encoding="utf-8")


def test_promote_with_backfill_rewrites_documents(api_store):
    _add_note_field(api_store)
    report = api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath, backfill=True)
    assert report.version == 2
    text = (api_store.root / "login.md").read_text(encoding="utf-8")
    assert "## Note\n\npending" in text


def test_full_roundtrip_add_backfill_write_and_reread(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath, backfill=True)
    model_type = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    api.save_document_payload(api_store.store, "TicketDoc", "login", {**PAYLOAD, "priority": 9}, api_store.pythonpath)
    text = (api_store.root / "login.md").read_text(encoding="utf-8")
    assert "## Priority\n\n9" in text
    assert extract_model_data(model_type, text)["priority"] == 9


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
    assert [m.name for m in api.registered_models(store)] == ["Dish"]
