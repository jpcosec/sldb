---
sldb:
  by: agent
  at: '2026-11-16T08:24:01Z'
  authority: generated
  via: save_document_payload
# unclear | suggestion
kind: suggestion
# e.g., other_repo
sender_project: IR
# e.g., target_repo
target_project: sldb
# ISO 8601 timestamp
created_at: '2026-11-15T21:50:07'
# open | closed
status: closed
# project identity that acknowledged the note
acknowledged_by: sldb
# ISO 8601 timestamp, set when acknowledged
acknowledged_at: '2026-11-16T05:23:45'
---

# IR13b pide exportar desde sldb.api.notations los errores de rutas del catálogo, DEFAULT_NOTATIONS, builtin_notations y resolve_catalog_path

_Describe the incoming message with enough evidence to triage._

El catálogo de specIR (IR13b) usa la regla de rutas de sldb y sus errores tipados. sldb.api.notations no exporta: AmbiguousPathError, UnknownReferenceError, UnknownNotationError (están en sldb.notations), DEFAULT_NOTATIONS y builtin_notations (sldb.notations), ni resolve_catalog_path y split_fragment (solo en el submódulo sldb.api.notations.catalog_paths). specIR los toma por ahora de sldb.notations a través de su único módulo puente (specir/visual/notation_style.py, el mismo de la nota de IR12 sobre resolve_style, load_palette y NotationError) y del submódulo catalog_paths. Pedido: reexportarlos desde sldb.api.notations, junto con lo de la nota de IR12. Cuando esté, specIR solo cambia esos imports y quita la excepción de tests/test_imports.py.
