# Segments and Transclusion

## Overview

SLDB's document segments representation (`GET /document/segments` and `sldb.api.build_document_segments`) breaks rendered document text into editable spans and literal gaps without re-parsing markdown. Every offset is exact by construction because it is captured during the template render phase via sentinel instrumentation (`SpanRecorder`).

This architecture supports rich transclusions and embedded visual blocks:
1. Document transclusion (`ref: "document"`): Assembles sections or summaries of whole external documents into composed fields.
2. Field transclusion (`ref: "field"`): Transcludes individual field values from other store documents into rendered sentences or lists.
3. Diagram & view transclusion (`trait: "diagram"` / `"view"`, or composition `ref: "view"` / `"spec"`): Resolves graph specifications (`SpecDoc:<id>` or `ViewDoc:<name>`) inline with notation glyphs, links, layout, and legend.
4. Structured table data (`trait: "table"` or `"table[col1,col2]"`): Emits structured rows and columns alongside the Markdown table.

## Field Transclusion (`FieldRefResolver`)

A composition declaring `ref: "field"` resolves references pointing to individual fields in other store documents:
- `Model:name#campo`
- `docs/<Model>/<name>/<campo>`
- `docs/<name>/<campo>` (when unambiguous across models)

Resolution is performed by `FieldRefResolver`, which queries the store and returns:
- `model`: Model name of the target document.
- `doc`: Document name in the store.
- `path`: Document file path.
- `field`: Normalized field path (`dotted.path`).
- `value`: Typed value extracted from the target payload.
- `payload`: Full payload of the target document.

In `build_document_segments(store_path, pythonpath, doc)`, `FieldRefResolver` is instantiated and injected into `render_with_spans` and `StructuredNLDoc.compose_field`.
When rendered without a store resolver (e.g. pure renderer calls), a composition with `ref: "field"` renders as an empty string without raising exceptions, preserving renderer purity without store dependencies.

Each resolved reference renders a piece wrapped with `CompositionPiece` carrying:
- `source`: `SourceRef(doc=..., path=..., model=..., field=...)`
- `ref_index`: Index of the reference in the composed field's list.
- `ref`: Reference string as authored.

## Diagram and View Projections

When a `FieldSegment` or `CompositionPiece` carries the trait `diagram` or `view` (or when a composition declares `ref: "view"` or `"spec"`):
- If the segment's value or ref refers to a `SpecDoc:<id>`, it is evaluated via `resolve_view(store, spec_ref)`.
- If it refers to a `ViewDoc:<name>`, it is evaluated via `evaluate_projection_view(store, view_ref)`.
- The resolved projection dictionary (containing `nodes`, `links`, `layout`, `legend`, etc.) is attached to the segment under `projection: dict | None = None`.
- If view resolution encounters an error or missing target, `projection` contains `{"error": str(exc)}` without interrupting segment generation or throwing an HTTP error.

## Structured Table Data

When a `FieldSegment` or `CompositionPiece` carries the trait `table` or `table[...]`:
- The columns and rows are parsed and structured into `table_data: dict | None = None`.
- The structure contains `{"columns": [...], "rows": [...]}` where `rows` provides the typed dictionaries corresponding to each table entry.
