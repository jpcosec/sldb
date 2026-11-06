from __future__ import annotations

import sys
from pathlib import Path
from pydantic import Field

from sldb import StructuredNLDoc, api
from sldb.api.segments import (
    CompositionPiece,
    FieldRefResolver,
    FieldSegment,
    SourceRef,
    build_document_segments,
)
from sldb.core.segments.instrumented_render import render_with_spans
from sldb.runtime.validation import extract_model_data, render_model_markdown


class SampleDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

Status: ⸢rev•status⸥

Description: ⸢rev•description⸥
""".strip()
    title: str = Field(description="Document title.")
    status: str = Field(description="Document status.")
    description: str = Field(description="Document description.")


class ComposedFieldDoc(StructuredNLDoc):
    __compositions__ = {
        "transcluded": {
            "source_field": "field_refs",
            "ref": "field",
            "template": "- {value} (from {title})",
        }
    }
    __template__ = """# ⸢rev•title⸥

## Refs

- ⸢rev,list•field_refs⸥

## Transcluded

⸢render•transcluded⸥
""".strip()
    title: str = Field(description="Title.")
    field_refs: list[str] = Field(default_factory=list, description="Field refs.")


class RichDiagramAndTableDoc(StructuredNLDoc):
    __template__ = """# ⸢rev•title⸥

## Diagram

⸢rev,diagram•diagram_ref⸥

## Table

⸢rev,table[name,role]•team⸥
""".strip()
    title: str = Field(description="Title.")
    diagram_ref: str = Field(description="Ref to SpecDoc or ViewDoc.")
    team: list[dict[str, str]] = Field(default_factory=list, description="Team table rows.")


def _setup_store(tmp_path: Path):
    proj_root = tmp_path / "project"
    proj_root.mkdir(parents=True, exist_ok=True)
    store_loc = api.init_store(proj_root)
    store_path = store_loc.store_path
    py = str(tmp_path)

    # Register models
    api.add_model(store_path, "tests.segments.test_field_transclusion_and_diagram_segments:SampleDoc", py)
    api.add_model(store_path, "tests.segments.test_field_transclusion_and_diagram_segments:ComposedFieldDoc", py)
    api.add_model(store_path, "tests.segments.test_field_transclusion_and_diagram_segments:RichDiagramAndTableDoc", py)

    # Create target doc
    doc_path = proj_root / "sample-1.md"
    api.create_document(
        store_path,
        "SampleDoc",
        doc_path,
        {"title": "Sample 1", "status": "active", "description": "A valuable sample doc."},
        name="sample-1",
        pythonpath=py,
    )
    return store_path, py, proj_root


def test_field_ref_resolver_resolves_all_formats(tmp_path: Path):
    store_path, py, _ = _setup_store(tmp_path)
    resolver = FieldRefResolver(store_path, py)

    # Format 1: Model:name#field
    res1 = resolver.resolve("SampleDoc:sample-1#status")
    assert res1["model"] == "SampleDoc"
    assert res1["doc"] == "sample-1"
    assert res1["field"] == "status"
    assert res1["value"] == "active"
    assert res1["payload"]["title"] == "Sample 1"

    # Format 2: docs/Model/name/field
    res2 = resolver.resolve("docs/SampleDoc/sample-1/description")
    assert res2["field"] == "description"
    assert res2["value"] == "A valuable sample doc."

    # Format 3: docs/name/field (unambiguous)
    res3 = resolver.resolve("docs/sample-1/title")
    assert res3["field"] == "title"
    assert res3["value"] == "Sample 1"


def test_field_composition_without_resolver_renders_empty_and_preserves_roundtrip(tmp_path: Path):
    payload = {
        "title": "Pure Render",
        "field_refs": ["SampleDoc:sample-1#status", "docs/sample-1/description"],
    }
    # Pure render without resolver returns empty string for the composition field
    rendered = render_model_markdown(ComposedFieldDoc, payload)
    assert "## Transcluded" in rendered
    assert "- active" not in rendered

    # Validation roundtrip is unaffected
    extracted = extract_model_data(ComposedFieldDoc, rendered)
    assert extracted["title"] == "Pure Render"
    assert extracted["field_refs"] == ["SampleDoc:sample-1#status", "docs/sample-1/description"]


def test_field_composition_with_resolver_in_segments(tmp_path: Path):
    store_path, py, proj_root = _setup_store(tmp_path)
    composed_path = proj_root / "composed-1.md"
    payload = {
        "title": "Composed Doc",
        "field_refs": ["SampleDoc:sample-1#status", "docs/SampleDoc/sample-1/description"],
    }
    api.create_document(store_path, "ComposedFieldDoc", composed_path, payload, name="composed-1", pythonpath=py)

    doc_segments = build_document_segments(store_path, py, "ComposedFieldDoc/composed-1")
    assert "- active (from Sample 1)" in doc_segments.text
    assert "- A valuable sample doc. (from Sample 1)" in doc_segments.text

    # Verify pieces in segment tree
    def find_pieces(segs):
        pieces = []
        for s in segs:
            if getattr(s, "type", None) == "composition":
                pieces.append(s)
            pieces.extend(find_pieces(getattr(s, "children", [])))
        return pieces

    pieces = find_pieces(doc_segments.segments)
    assert len(pieces) == 2
    p1 = pieces[0]
    assert isinstance(p1.source, SourceRef)
    assert p1.source.model == "SampleDoc"
    assert p1.source.doc == "sample-1"
    assert p1.source.field == "status"
    assert p1.ref_index == 0
    assert p1.ref == "SampleDoc:sample-1#status"

    p2 = pieces[1]
    assert p2.source.field == "description"
    assert p2.ref_index == 1


def test_diagram_and_table_enrichment(tmp_path: Path):
    store_path, py, proj_root = _setup_store(tmp_path)

    # Sync a builtin notation to store so resolve_view / evaluate_projection_view have notation data
    api.sync_notation(store_path, "statechart")

    # Save a ViewDoc
    view_payload = {
        "id": "arch-view",
        "name": "arch-view",
        "title": "Arch View",
        "nodes": [{"model": "SampleDoc", "where": ""}],
        "relations": ["*"],
        "direction": "both",
        "notation": "statechart",
    }
    api.save_projection_view(store_path, "arch-view", view_payload, pythonpath=py)

    rich_path = proj_root / "rich-1.md"
    rich_payload = {
        "title": "Rich View",
        "diagram_ref": "ViewDoc:arch-view",
        "team": [
            {"name": "Alice", "role": "Architect"},
            {"name": "Bob", "role": "Engineer"},
        ],
    }
    api.create_document(store_path, "RichDiagramAndTableDoc", rich_path, rich_payload, name="rich-1", pythonpath=py)

    doc_segments = build_document_segments(store_path, py, "RichDiagramAndTableDoc/rich-1")

    # Find FieldSegments
    def find_fields(segs):
        fields = []
        for s in segs:
            if getattr(s, "type", None) == "field":
                fields.append(s)
            fields.extend(find_fields(getattr(s, "children", [])))
        return fields

    fields = {f.path: f for f in find_fields(doc_segments.segments)}

    # Diagram field has projection resolved
    diagram_field = fields["diagram_ref"]
    assert diagram_field.projection is not None
    assert "error" not in diagram_field.projection
    assert "nodes" in diagram_field.projection

    # Table field has structured table_data
    table_field = fields["team"]
    assert table_field.table_data is not None
    assert table_field.table_data["columns"] == ["name", "role"]
    assert len(table_field.table_data["rows"]) == 2
    assert table_field.table_data["rows"][0] == {"name": "Alice", "role": "Architect"}
    assert table_field.table_data["rows"][1] == {"name": "Bob", "role": "Engineer"}


def test_missing_diagram_attaches_error_without_failing(tmp_path: Path):
    store_path, py, proj_root = _setup_store(tmp_path)
    rich_path = proj_root / "rich-err.md"
    rich_payload = {
        "title": "Error Diagram",
        "diagram_ref": "SpecDoc:non-existent-spec",
        "team": [],
    }
    api.create_document(store_path, "RichDiagramAndTableDoc", rich_path, rich_payload, name="rich-err", pythonpath=py)

    doc_segments = build_document_segments(store_path, py, "RichDiagramAndTableDoc/rich-err")
    def find_fields(segs):
        fields = []
        for s in segs:
            if getattr(s, "type", None) == "field":
                fields.append(s)
            fields.extend(find_fields(getattr(s, "children", [])))
        return fields

    fields = {f.path: f for f in find_fields(doc_segments.segments)}
    diagram_field = fields["diagram_ref"]
    assert diagram_field.projection is not None
    assert "error" in diagram_field.projection
