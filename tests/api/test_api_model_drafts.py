"""`sldb.api` model draft operations: field and template edits, validation, promotion."""

from __future__ import annotations

import json
import sys

import pytest

import sldb.api as api
from sldb.core.exceptions import SLDBModelDraftError, SLDBModelEditError
from sldb.runtime.validation import extract_model_data

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


INHERITED_MODULE = "sldb_api_inherited_models"

INHERITED_MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class Party(StructuredNLDoc):
    __template__ = "# ⸢rev•title⸥\\n\\nSize: ⸢rev•party_size⸥"
    title: str = Field(description="Title.")
    party_size: int = Field(description="People.")


class Reservation(Party):
    pass
'''


def test_add_model_field_materializes_an_inherited_template(tmp_path):
    sys.modules.pop(INHERITED_MODULE, None)
    (tmp_path / f"{INHERITED_MODULE}.py").write_text(INHERITED_MODELS, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    api.init_store(root)
    store = root / ".sldb"
    pythonpath = str(tmp_path)
    for model in ("Party", "Reservation"):
        api.add_model(store, f"{INHERITED_MODULE}:{model}", pythonpath)
    api.create_document(store, "Reservation", root / "res-1.md", {"title": "Ana", "party_size": 6}, "res-1", pythonpath)

    draft = api.add_model_field(store, "Reservation", "zone", "str", "Where they sit.", json.dumps("indoor"), pythonpath)
    text = draft.draft_path.read_text(encoding="utf-8")
    # The draft declares its own template now, not the base's, and it keeps the base order.
    assert "__template__ = " in text
    assert "⸢optrev•zone⸥" in text and "## Zone" in text
    assert text.index("⸢rev•title⸥") < text.index("⸢optrev•zone⸥")
    # The base file is never edited: its other subclasses must not inherit the new marker.
    assert "zone" not in (tmp_path / f"{INHERITED_MODULE}.py").read_text(encoding="utf-8")

    report = api.promote_model_draft(store, "Reservation", pythonpath)
    assert (report.promoted, report.version) == (True, 2)
    sys.modules.pop(INHERITED_MODULE, None)
    model_type = api.resolve_model_ref(f"{INHERITED_MODULE}:Reservation", pythonpath)
    assert model_type.__template__ and "⸢optrev•zone⸥" in model_type.__template__

    api.save_document_payload(store, "Reservation", "res-1", {"title": "Ana", "party_size": 6, "zone": "patio"}, pythonpath)
    text = (root / "res-1.md").read_text(encoding="utf-8")
    assert "## Zone\n\npatio" in text
    assert extract_model_data(model_type, text)["zone"] == "patio"


def test_remove_model_field_does_not_touch_an_inherited_template(tmp_path):
    source = INHERITED_MODELS.replace(
        "    pass\n",
        "    extra: str = Field(description='Extra.')\n    pass\n",
    )
    sys.modules.pop(INHERITED_MODULE, None)
    (tmp_path / f"{INHERITED_MODULE}.py").write_text(source, encoding="utf-8")
    root = tmp_path / "repo"
    root.mkdir()
    api.init_store(root)
    store = root / ".sldb"
    pythonpath = str(tmp_path)
    for model in ("Party", "Reservation"):
        api.add_model(store, f"{INHERITED_MODULE}:{model}", pythonpath)

    draft = api.remove_model_field(store, "Reservation", "extra", pythonpath)
    text = draft.draft_path.read_text(encoding="utf-8")
    assert "extra" not in text
    # Only Party's template assignment remains: Reservation's inherited one is left untouched.
    assert text.count("__template__ = ") == 1


def test_describe_field_reports_kind_enum_annotation_and_description(api_store):
    model_type = api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath)
    status = api.describe_field("status", model_type.model_fields["status"])
    assert (status.kind, status.enum, status.required, status.description) == ("enum", ["open", "closed"], True, "Ticket state.")
    kinds = {f.name: f.kind for f in api.describe_model_fields(model_type)}
    assert kinds["title"] == "string" and kinds["tags"] == "stringlist"
