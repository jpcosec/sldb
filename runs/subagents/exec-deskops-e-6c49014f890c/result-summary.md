# Result summary
Worktree: .worktrees/deskops-e-6c49014f890c (cambios SIN commitear, ver abajo).

| archivo | decisión | evidencia |
|---|---|---|
| src/sldb/cli/parsers/graph.py | conservado | `add_graph_group` usado en cli/parsers/public.py:11,27; define 13 subcomandos reales |
| src/sldb/cli/parsers/stores.py | conservado | todas las `_xxx` se llaman desde `add_stores_group`; sin funciones/constantes sin uso |
| src/sldb/cli/commands/help_texts_graph.py | conservado | `GRAPH_HELP` importado en cli/commands/help_texts.py:6,20 |
| src/sldb/store/graph/ingest_sldb.py | conservado | api/graph/snapshot.py, api/graph/__init__.py, store/graph/__init__.py y 4 tests importan `sldb_semantic_export_to_snapshot` |
| src/sldb/selfdoc/python_source_graph.py | conservado | cli/commands/selfdoc_python.py:18 + 4 tests de selfdoc importan `source_snapshot` |
| src/sldb/api/schema/field_descriptor.py | borrado | cáscara (solo reexport); único usuario cli/serve/schema.py, repuntado a sldb.models.field_schema.descriptor |
| src/sldb/api/schema/field_kinds.py | borrado | cáscara; usuarios (describe_model, segments/payload_values, records/utils, cli/serve/schema.py) repuntados a sldb.models.field_schema.kinds; docstrings actualizados |
| src/sldb/cli/serve/schema.py | reducido | quitados reexports sin uso (add_enum_values, enum_values, field_kind, list_kind, scalar_kind, unwrap_annotation) |
| src/sldb/api/schema/field_description.py | conservado | reexporta `FieldDescription`, parte del `__all__` de sldb.api |
| api/**/__init__.py y api/notations/notation_view.py (cáscaras por AST) | conservados | reexportan API pública de `__all__` (notations/__init__.py importa notation_view; test lo importa) |

Archivos cambiados: CHANGELOG.md, src/sldb/api/model_registry/describe_model.py, src/sldb/api/records/utils.py, src/sldb/api/segments/{extracted_field,field_segment,payload_values}.py, src/sldb/cli/serve/schema.py, src/sldb/models/field_schema/descriptor.py; borrados api/schema/field_descriptor.py y field_kinds.py (git rm, staged).

Validación (validation.log): los 4 pytest de la tarea pasan; tests/relation_models y segments pasan. tests/api: 16 fallos en documents_dirty/RollbackError — preexistentes (también fallan en el checkout principal sin mis cambios, vienen de la tarea anterior documents_dirty.json).
**BLOQUEO**: `tools/check.sh --fast` sale rc=1 por `identidad: directorio versionado sin clasificar en la raíz: workbench_demo`, preexistente y ajeno. Por eso NO commiteé ni avancé la tarea. El supervisor decide.

## Actualización (autorización del coordinador)
Commit hecho en el worktree con check.sh --fast en rojo solo por `identidad`/workbench_demo (decisión aparte f055723d). Los 16 fallos de tests/api (documents_dirty/RollbackError) son preexistentes y no se tocaron; el coordinador los revisa.
