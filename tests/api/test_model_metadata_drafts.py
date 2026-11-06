"""Tests for SV04: Model metadata declaration (create_model) and draft editing (edit_model_metadata).

Covers containment, references, compositions, semantics, and authority in create_model,
describe_model, edit_model_metadata, validate_model_draft, promote_model_draft(backfill=True),
CLI commands and HTTP serve routes.
"""

from __future__ import annotations

import json
from pathlib import Path
import pytest

import sldb.api as api
from sldb.api.edges.edge_reading import load_edge_index
from sldb.cli.dispatcher import CLI
from sldb.core.exceptions import SLDBModelEditError, SLDBModelError
from .conftest import MODULE


def test_create_model_with_containment_references_compositions_semantics_authority(api_store):
    fields = [
        {"name": "title", "type": "str", "description": "Title of the project"},
        {"name": "subtasks", "type": "list[str]", "description": "Subtask doc references"},
        {"name": "related", "type": "list[str]", "description": "Related ticket references"},
    ]
    containment = {"subtasks": ["TicketDoc"]}
    references = ["related"]
    compositions = {
        "subtask_summary": {
            "source_field": "subtasks",
            "model": f"{MODULE}:TicketDoc",
            "template": "- {title}",
            "separator": "\n",
        }
    }
    semantics = {"domain": ["project_management"]}
    authority = "authored"

    reg = api.create_model(
        api_store.store,
        "ProjectDoc",
        fields=fields,
        containment=containment,
        references=references,
        compositions=compositions,
        semantics=semantics,
        authority=authority,
        pythonpath=api_store.pythonpath,
    )
    assert reg.name == "ProjectDoc"
    assert reg.version == 1

    desc = api.describe_model(api_store.store, "ProjectDoc", api_store.pythonpath)
    assert desc.name == "ProjectDoc"
    assert desc.containment == containment
    assert desc.references == references
    assert desc.compositions == compositions
    assert desc.semantics_map == semantics
    assert desc.authority == "authored"
    assert "⸢render•subtask_summary⸥" in desc.template
    assert desc.has_draft is False
    assert desc.draft_path is None


def test_create_model_validation_rejects_unknown_fields(api_store):
    fields = [{"name": "title", "type": "str", "description": "Title"}]

    # Unknown containment field
    with pytest.raises(SLDBModelError, match="containment"):
        api.create_model(
            api_store.store,
            "BadContDoc",
            fields=fields,
            containment={"nonexistent": ["OtherDoc"]},
            pythonpath=api_store.pythonpath,
        )

    # Unknown references field
    with pytest.raises(SLDBModelError, match="references"):
        api.create_model(
            api_store.store,
            "BadRefDoc",
            fields=fields,
            references=["missing_field"],
            pythonpath=api_store.pythonpath,
        )

    # Unknown source_field in composition
    with pytest.raises(SLDBModelError, match="source field"):
        api.create_model(
            api_store.store,
            "BadCompDoc",
            fields=fields,
            compositions={"summary": {"source_field": "no_such_field"}},
            pythonpath=api_store.pythonpath,
        )

    # Composition missing render marker in custom template
    with pytest.raises(SLDBModelError, match="marker"):
        api.create_model(
            api_store.store,
            "MissingMarkerDoc",
            fields=fields,
            template="# ⸢rev•title⸥\n",
            compositions={"comp": {"source_field": "title"}},
            pythonpath=api_store.pythonpath,
        )


def test_edit_model_metadata_writes_draft_and_leaves_active_untouched(api_store, tmp_path):
    active_path = tmp_path / f"{MODULE}.py"
    before = active_path.read_text(encoding="utf-8")

    draft = api.edit_model_metadata(
        api_store.store,
        "TicketDoc",
        containment={"tags": ["TagDoc"]},
        references=["tags"],
        authority="authored",
        semantics={"topic": ["support"]},
        pythonpath=api_store.pythonpath,
    )

    assert draft.draft_path.exists()
    draft_text = draft.draft_path.read_text(encoding="utf-8")
    assert "__containment__ = {'tags': ['TagDoc']}" in draft_text
    assert "__references__ = ['tags']" in draft_text
    assert "__authority__ = 'authored'" in draft_text
    assert "__semantics__ = {'topic': ['support']}" in draft_text

    # Active file was untouched
    assert active_path.read_text(encoding="utf-8") == before

    # describe_model reports draft
    desc = api.describe_model(api_store.store, "TicketDoc", api_store.pythonpath)
    assert desc.has_draft is True
    assert desc.draft_path == str(draft.draft_path)


def test_edit_model_metadata_compositions_syncs_template(api_store):
    comp_spec = {
        "tag_summaries": {
            "source_field": "tags",
            "model": f"{MODULE}:TicketDoc",
            "template": "- {title}",
        }
    }
    draft = api.edit_model_metadata(
        api_store.store,
        "TicketDoc",
        compositions=comp_spec,
        pythonpath=api_store.pythonpath,
    )
    draft_text = draft.draft_path.read_text(encoding="utf-8")
    assert "⸢render•tag_summaries⸥" in draft_text
    assert "## Tag summaries" in draft_text

    # Remove composition
    draft2 = api.edit_model_metadata(
        api_store.store,
        "TicketDoc",
        compositions={},
        pythonpath=api_store.pythonpath,
    )
    draft_text2 = draft2.draft_path.read_text(encoding="utf-8")
    assert "⸢render•tag_summaries⸥" not in draft_text2
    assert "## Tag summaries" not in draft_text2


def test_validate_model_draft_rejects_invalid_metadata(api_store):
    # Draft with unknown field in references
    api.edit_model_metadata(
        api_store.store,
        "TicketDoc",
        references=["ghost_field"],
        pythonpath=api_store.pythonpath,
    )
    with pytest.raises(SLDBModelEditError, match="__references__ references unknown"):
        api.validate_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)

    # Draft with unknown field in containment
    api.edit_model_metadata(
        api_store.store,
        "TicketDoc",
        references=[],
        containment={"ghost_containment": ["OtherDoc"]},
        pythonpath=api_store.pythonpath,
    )
    with pytest.raises(SLDBModelEditError, match="__containment__ references unknown"):
        api.validate_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)

    # Draft with unknown source_field in composition
    api.edit_model_metadata(
        api_store.store,
        "TicketDoc",
        containment={},
        compositions={"comp": {"source_field": "ghost_field"}},
        pythonpath=api_store.pythonpath,
    )
    with pytest.raises(SLDBModelEditError, match="unknown source field"):
        api.validate_model_draft(api_store.store, "TicketDoc", api_store.pythonpath)


def test_promote_model_draft_with_backfill_updates_indexes_and_documents(api_store, tmp_path):
    active_path = tmp_path / f"{MODULE}.py"
    # Create child ticket document
    child_payload = {"title": "Child issue", "status": "open", "tags": []}
    api_store.write_document("child-1", child_payload)
    api.track_document_file(api_store.store, "TicketDoc", api_store.root / "child-1.md", "child-1", api_store.pythonpath)

    # Edit parent login document to hold child in tags
    doc_path = api_store.root / "login.md"
    parent_payload = {"title": "Broken login", "status": "open", "tags": ["child-1"]}
    from sldb.runtime.validation import render_model_markdown
    doc_path.write_text(render_model_markdown(api.resolve_model_ref(f"{MODULE}:TicketDoc", api_store.pythonpath), parent_payload) + "\n", encoding="utf-8")
    api.save_document_payload(api_store.store, "TicketDoc", "login", parent_payload, api_store.pythonpath)

    # Edit metadata to declare tags as containment
    draft = api.edit_model_metadata(
        api_store.store,
        "TicketDoc",
        containment={"tags": ["TicketDoc"]},
        references=["tags"],
        authority="authored",
        semantics={"domain": ["support"]},
        pythonpath=api_store.pythonpath,
    )

    report = api.promote_model_draft(api_store.store, "TicketDoc", api_store.pythonpath, backfill=True)
    assert report.promoted is True
    assert report.version == 2
    assert not draft.draft_path.exists()
    assert "__containment__ = {'tags': ['TicketDoc']}" in active_path.read_text(encoding="utf-8")

    # Check edge index was rebuilt and contains the contains edge
    edges = load_edge_index(api_store.store)
    contains_edges = [e for e in edges.edges if e.relation == "contains" and "login" in e.source and "child-1" in e.target]
    assert len(contains_edges) == 1
    assert contains_edges[0].metadata.get("field") == "tags"

    # Check describe_model reflects the promoted state
    desc = api.describe_model(api_store.store, "TicketDoc", api_store.pythonpath)
    assert desc.version == 2
    assert desc.has_draft is False
    assert desc.containment == {"tags": ["TicketDoc"]}
    assert desc.authority == "authored"


def test_cli_metadata_edit_and_validate_promote(api_store, tmp_path):
    cli = CLI()
    ret = cli.run([
        "models", "metadata", "edit", "TicketDoc",
        "--authority", "authored",
        "--references", '["tags"]',
        "--store", str(api_store.store),
        "--pythonpath", api_store.pythonpath,
    ])
    assert ret == 0

    draft_path = tmp_path / f"{MODULE}.py.temp"
    assert draft_path.exists()
    assert "__references__ = ['tags']" in draft_path.read_text(encoding="utf-8")

    ret_val = cli.run([
        "models", "validate", "TicketDoc",
        "--promote", "--backfill",
        "--store", str(api_store.store),
        "--pythonpath", api_store.pythonpath,
    ])
    assert ret_val == 0
    assert not draft_path.exists()

    desc = api.describe_model(api_store.store, "TicketDoc", api_store.pythonpath)
    assert desc.authority == "authored"
    assert desc.references == ["tags"]


def test_http_serve_routes_for_model_metadata(api_store, tmp_path):
    from http.server import ThreadingHTTPServer
    from sldb.cli.serve.http_server import build_handler
    import threading
    import urllib.request

    handler = build_handler(str(api_store.store), api_store.pythonpath, cors=False)
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    port = server.server_port
    base_url = f"http://127.0.0.1:{port}"

    try:
        # 1. POST /models/create
        req_data = {
            "name": "NoteDoc",
            "fields": [
                {"name": "body", "type": "str", "description": "Note content"},
                {"name": "parent", "type": "str", "description": "Parent ticket", "default": ""},
            ],
            "containment": {"parent": ["TicketDoc"]},
            "authority": "authored",
        }
        req = urllib.request.Request(
            f"{base_url}/models/create",
            data=json.dumps(req_data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            assert data["ok"] is True
            assert data["name"] == "NoteDoc"

        # 2. GET /models/detail
        with urllib.request.urlopen(f"{base_url}/models/detail?model=NoteDoc") as resp:
            data = json.loads(resp.read().decode("utf-8"))
            assert data["ok"] is True
            model_info = data["model"]
            assert model_info["containment"] == {"parent": ["TicketDoc"]}
            assert model_info["authority"] == "authored"
            assert model_info["has_draft"] is False

        # 3. POST /models/metadata-edit
        edit_data = {
            "model": "NoteDoc",
            "authority": "source_raw",
        }
        req_edit = urllib.request.Request(
            f"{base_url}/models/metadata-edit",
            data=json.dumps(edit_data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req_edit) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            assert data["ok"] is True
            assert data["draft_path"].endswith("note_doc.py.temp")

        # 4. POST /models/promote with backfill: true
        promote_data = {
            "model": "NoteDoc",
            "backfill": True,
        }
        req_prom = urllib.request.Request(
            f"{base_url}/models/promote",
            data=json.dumps(promote_data).encode("utf-8"),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urllib.request.urlopen(req_prom) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            assert data["ok"] is True
            assert data["promoted"] is True
            assert data["version"] == 2

    finally:
        server.shutdown()
