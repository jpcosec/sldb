"""`sldb.api` model draft operations: field and template edits, validation, promotion."""

from __future__ import annotations

import pytest

import sldb.api as api
from sldb.core.exceptions import SLDBModelDraftError, SLDBModelEditError

from .conftest import MODULE


def test_add_model_field_writes_a_draft_and_leaves_the_active_model(api_store, tmp_path):
    active = tmp_path / f"{MODULE}.py"
    before = active.read_text(encoding="utf-8")
    draft = api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "Urgency.", "5", api_store.pythonpath)
    assert draft.draft_path == active.with_name(active.name + ".temp")
    assert "priority: int = Field(default=5, description='Urgency.')" in draft.draft_path.read_text(encoding="utf-8")
    assert active.read_text(encoding="utf-8") == before
    with pytest.raises(SLDBModelEditError, match="already exists"):
        api.add_model_field(api_store.store, "TicketDoc", "priority", pythonpath=api_store.pythonpath)


def test_remove_model_field_edits_the_draft(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    draft = api.remove_model_field(api_store.store, "TicketDoc", "priority", api_store.pythonpath)
    assert "priority" not in draft.draft_path.read_text(encoding="utf-8")


def test_edit_model_template_writes_the_draft_template(api_store):
    draft = api.edit_model_template(api_store.store, "TicketDoc", "# Ticket ⸢rev•title⸥\n\n", api_store.pythonpath)
    assert '"""# Ticket ⸢rev•title⸥""".strip()' in draft.draft_path.read_text(encoding="utf-8")


def test_validate_model_draft_reports_documents_without_promoting(api_store):
    api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    report = api.validate_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert (report.valid, report.draft, report.promoted, report.version) == (True, True, False, 1)
    assert [(d.name, d.valid) for d in report.documents] == [("login", True)]


def test_validate_model_draft_rejects_template_referencing_unknown_fields(api_store):
    api.edit_model_template(api_store.store, "TicketDoc", "# ⸢rev•headline⸥", api_store.pythonpath)
    with pytest.raises(SLDBModelEditError):
        api.validate_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)


def test_promote_model_draft_installs_bumps_and_refreshes_the_class(api_store):
    api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    draft = api.add_model_field(api_store.store, "TicketDoc", "priority", "int", "x", "5", api_store.pythonpath)
    report = api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)
    assert (report.promoted, report.version) == (True, 2)
    assert not draft.draft_path.exists()
    assert "priority" in api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath).model_fields
    with pytest.raises(SLDBModelDraftError, match="draft"):
        api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)


def test_locate_model_source_points_at_the_defining_file(api_store, tmp_path):
    source = api.locate_model_source(api_store.store, "TicketDoc", api_store.pythonpath)
    assert (source.path, source.class_name) == ((tmp_path / f"{MODULE}.py").resolve(), "TicketDoc")


def test_describe_field_reports_kind_enum_annotation_and_description(api_store):
    model_type = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    status = api.describe_field("status", model_type.model_fields["status"])
    assert (status.kind, status.enum, status.required, status.description) == ("enum", ["open", "closed"], True, "Ticket state.")
    kinds = {f.name: f.kind for f in api.describe_model_fields(model_type)}
    assert kinds["title"] == "string" and kinds["tags"] == "stringlist"
