---
id: task-sv03-transclusion-de-campos-y-segmentos-ricos-de-diagramas-y-vistas-en-document-segments
status: ready_for_testing
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-closeout
history:
- task_activates
- task_hands_to_closeout
references:
- ea85af56
- tests/segments/test_field_transclusion_and_diagram_segments.py
- atom-la-transclusion-por-campo-y-los-bloques-ricos-de-diagramas-y-tablas-se-resuelven-en-document-segment
depends_on:
- task-sv02-resolvedor-de-vistas-y-notaciones-en-sldb-api-cli-y-sldb-serve
pills: []
files:
- src/sldb/models/structured_doc.py
- src/sldb/api/segments/source_ref.py
- src/sldb/api/segments/composition_spec.py
- src/sldb/api/segments/composition_piece.py
- src/sldb/api/segments/field_segment.py
- src/sldb/api/segments/field_ref_resolver.py
- src/sldb/api/segments/segment_nodes.py
- src/sldb/api/segments/build_document_segments.py
- src/sldb/core/segments/instrumented_render.py
- src/sldb/core/renderer_engine/payload_call.py
- docs/architecture/segments-and-transclusion.md
- CHANGELOG.md
- tests/segments/test_field_transclusion_and_diagram_segments.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-atom-como-field-tipado-composicion-por-field.md
---

# SV03: Transclusion de campos y segmentos ricos de diagramas y vistas en /document/segments

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo SV03 del plan desk/drawer/plans/absorber-spec2viz-y-modelos-ui (dag.yaml rev 1), que absorbe tambien la tarea diferida task-atom-como-field-tipado-composicion-por-field. Hoy StructuredNLDoc.compose_field solo resuelve archivos completos (ref: document) y /document/segments no adjunta vistas de diagrama/proyeccion ni tablas estructuradas para que la UI unificada renderice transclusiones de campo/nodo, tablas y diagramas SpecDoc/ViewDoc inline.

## Goal

_Describe the concrete result this task must produce._

CompositionSpec.ref == "field" resuelve campos de otros documentos del store mediante un FieldRefResolver inyectado (con SourceRef.field en cada CompositionPiece); FieldSegment y CompositionPiece con trait diagram o view adjuntan la vista ya resuelta (projection desde resolve_view / evaluate_projection_view) y con trait table adjuntan {columns, rows} estructurados en /document/segments.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/models/structured_doc.py, src/sldb/api/segments/source_ref.py, src/sldb/api/segments/composition_spec.py, src/sldb/api/segments/composition_piece.py, src/sldb/api/segments/field_segment.py, src/sldb/api/segments/field_ref_resolver.py, src/sldb/api/segments/segment_nodes.py, src/sldb/api/segments/build_document_segments.py, src/sldb/core/segments/instrumented_render.py, src/sldb/core/renderer_engine/payload_call.py, docs/architecture/segments-and-transclusion.md, CHANGELOG.md, tests/segments/test_field_transclusion_and_diagram_segments.py. Fuera: edicion de contratos de modelo (SV04).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 1, SV03): (1) Crear FieldRefResolver en src/sldb/api/segments/field_ref_resolver.py: resuelve referencias de campo en las formas Model:name#campo y docs/<Model>/<name>/<campo> (y docs/<name>/<campo> cuando no es ambiguo) contra el store y devuelve {model, doc, path, field, value, payload}; se inyecta explicitamente en render_with_spans / StructuredNLDoc.compose_field desde build_document_segments(store_path, pythonpath, doc). Sin resolver inyectado, una composicion con ref: "field" rinde vacio sin lanzar excepcion (preservando la pureza del renderer sin store), y la validacion roundtrip no cambia porque es un marcador render. SourceRef gana el campo opcional field: str | None = None. (2) Enriquecer los segmentos en build_document_segments / segment_nodes.py: cuando un FieldSegment o CompositionPiece lleva el trait diagram o view (o la composicion declara ref: "view" o "spec") y su valor nombra un SpecDoc:<id> o ViewDoc:<name>, resolverlo con resolve_view o evaluate_projection_view de SV02 y adjuntar el resultado en el campo opcional projection: dict | None = None del segmento (si la vista no existe o falla, adjuntar {"error": str(exc)} sin tumbar /document/segments). Cuando el FieldSegment lleva el trait table, adjuntar en table_data: dict | None = None las columnas y filas estructuradas ({columns, rows}) junto al texto Markdown renderizado.

## Validation

_List the checks required before this task can close._

- pytest tests/segments/test_field_transclusion_and_diagram_segments.py tests/test_composition.py -q sin fallos ni saltados
- con FieldRefResolver inyectado, ref="field" rinde el valor del campo remoto y emite CompositionPiece con SourceRef.field; sin resolver, rinde vacio y validate_model_data_roundtrip no cambia
- GET /document/segments sobre un documento con trait diagram y trait table incluye projection (nodos, links, layout, legend) y table_data ({columns, rows})

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de SV03 cumplida, tests en verde, G_SV_SEGMENTS satisfecho en dag.yaml.
