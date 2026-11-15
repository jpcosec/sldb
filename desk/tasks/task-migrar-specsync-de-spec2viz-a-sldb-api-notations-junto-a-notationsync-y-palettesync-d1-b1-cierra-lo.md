---
sldb:
  by: agent
  at: '2026-11-15T17:41:28Z'
  authority: generated
  via: save_document_payload
id: task-migrar-specsync-de-spec2viz-a-sldb-api-notations-junto-a-notationsync-y-palettesync-d1-b1-cierra-lo
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files: []
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Migrar SpecSync de spec2viz a sldb.api.notations junto a NotationSync y PaletteSync (D1, B1, cierra lo pendiente de SV02)

## Rationale

_Explain why this task exists or the business driver behind it._

Decisión de JP 2026-11-15: nunca reimplementar en un consumidor lo que es de sldb. NotationSync y PaletteSync ya están en sldb; SpecSync, que reconcilia un conjunto de specs (materializa y borra lo que salió), quedó en spec2viz.

## Goal

_Describe the concrete result this task must produce._

Reconciliar un conjunto de documentos de spec en un store: crear, actualizar y borrar SpecDoc, SpecNodeDoc y RelationDoc, con informe.

## Scope

_State what is in scope and what is out of scope._

SI EL CÓDIGO YA EXISTE, SE MIGRA, NO SE REESCRIBE. Entra: SpecSync y sus ayudantes de spec y catálogo del módulo spec2viz.sldb_sync, expuestos como API pública de sldb.api.notations y en "sldb notations sync" (--spec, --catalog, --check, --prune). Reutiliza el StoreWriter y el SyncReport de sldb (se converge en ellos; la copia de spec2viz no se toca). Sale: PaletteSync y NotationSync (ya en sldb), modelos de spec por tipo y su carga (D3; aquí la validación previa es un parámetro opcional), compiladores y renderers, y cualquier cambio en el repo spec2viz. spec2viz NO se retira y conserva su código; el gate IR13 es la tarea IR13 del desk de IR, que decide el retiro; aquí solo se nombra. Paridad: los tests de spec2viz de la pieza se portan a sldb con el mínimo cambio, contra un store real y sin mocks. "La misma salida" significa: mismos documentos creados, actualizados y borrados (nombres y payload) y el mismo texto de format_report sobre los mismos specs, comparando campo a campo; no byte a byte del store. Cierra B1 del brief.

## Implementation Path

_Outline the expected implementation route or affected surface._

1. Origen (repo hermano spec2viz, existe, 886 líneas): módulo spec2viz.sldb_sync. Se migran: SpecSync, spec_style_kinds, spec_elements, spec_edges, relation_token, node_ref, to_slash_ref, stage_id, edge_name, relation_doc_has_attributes, find_store, resolve_spec_notation, _store_notation, catalog_entries, check_catalog, sync_catalog, format_report y format_notation_report. NO se migran _StoreWriter, SyncReport, PaletteSync ni NotationSync: sldb ya los tiene.
2. Reutilizar de sldb (comparado leyendo el código): src/sldb/api/notations/store_writer.py (StoreWriter tiene prepare, root, existing_documents, upsert, ensure_relation_type, delete, finish igual que _StoreWriter, más create; el actor por defecto pasa de "spec2viz" a "sldb"), src/sldb/api/notations/sync_report.py (SyncReport de sldb ya trae los mismos campos; difiere en que "problems" es un campo y en spec2viz es una propiedad unresolved+edge_errors: SpecSync lo rellena con esa suma antes de finish, y format_report lee el campo), src/sldb/api/notations/sync_constants.py (MODEL_REFS ya declara SpecDoc y SpecNodeDoc, y _MANAGED_MODELS ya los cubre), notation_sync.py (NotationSync, sync_notation) y src/sldb/models/notation/spec_doc.py y spec_node_doc.py (modelos de lo que se escribe). Criterio: misma entrada y misma salida observable en los tests portados, se reutiliza; si no, se migra.
3. Destino: un módulo nuevo en src/sldb/api/notations/ para SpecSync (spec_sync) y otro para los ayudantes de spec y catálogo, cada uno bajo el límite de líneas del repo. Exportar SpecSync, sync_spec, check_catalog, sync_catalog y spec_elements desde src/sldb/api/notations/__init__.py.
4. Validación previa del spec: spec2viz llama a spec2viz.loader.load antes de tocar el store. D1 no depende de D3, así que SpecSync de sldb recibe esa validación como parámetro opcional "validate" (callable que recibe la ruta y lanza si es inválido), sin importar nada de spec2viz; por defecto solo valida el YAML y el campo id. Cuando D3 aterrice, se le pasa el cargador de sldb. Queda anotado en el cierre.
5. CLI: ampliar "sldb notations sync" (src/sldb/cli/parsers/notations.py) con --spec RUTA (repetible), --catalog RUTA (el vistas.yml), --check (solo valida el catálogo, sin escribir) y --notation, que ya existe. Salida: el mismo informe de format_report y format_notation_report, y con --json la lista de SyncReport.to_dict(). Registrar el handler junto al de notation y palette.
6. Reconciliación: el "conjunto" es el de SpecDoc con el mismo spec_id, de modo que sync por spec borra los SpecNodeDoc y RelationDoc de ese spec que ya no salen de spec_elements y spec_edges. sync_catalog borra además los SpecDoc del catálogo que dejaron de estar en el vistas.yml, pero solo con --prune explícito (sin él los lista en report.unresolved como aviso). Los avisos usan el formato de findings de sldb (src/sldb/core/finding.py: level, code, subject, what, fix); códigos ns/name: spec-sync/orphan-spec, spec-sync/unresolved-ref, spec-sync/edge-error.
7. Tests: portar a sldb los 16 de spec2viz test_sldb_sync y los 6 de test_catalog_notation (todos ejercen catalog sync, diagram sync o resolve_spec_notation vía la CLI click de spec2viz: se reescribe solo la invocación para llamar a sldb.api.notations o a "sldb notations sync"; las excepciones NotationMismatchError y UnknownNotationError ya existen en sldb.notations.exceptions, se importan de ahí). Mínimo cambio (imports, invocación y actor), contra un store real creado en tmp_path con TMPDIR=/dev/shm, sin mocks. Los que cargan un spec con el cargador de spec2viz usan el parámetro validate vacío.
8. spec2viz no se toca: conserva su sldb_sync y su copia de _StoreWriter y SyncReport. El retiro lo decide la tarea IR13 del desk de IR (gate IR13); aquí solo se nombra.

## Validation

_List the checks required before this task can close._

- Tests de origen en spec2viz (a portar con el mínimo cambio): test_sldb_sync (16 tests) y test_catalog_notation (6 tests, escritos contra la CLI click de spec2viz: se cambia solo la invocación).
- Destino previsto: un archivo de tests de SpecSync y otro del catálogo, junto a los de NotationSync y PaletteSync de sldb, y uno del subcomando notations sync con --spec, --catalog y --check.
- Comparar el informe de sldb con el de spec2viz sobre los mismos specs (campo a campo) y anotar el resultado en el cierre.
- TMPDIR=/dev/shm pytest -q de cada archivo tocado, uno a la vez; antes de entregar, todos los tests/*.py de a uno.
- tools/check.sh
- sldb stores build --check
- deskops graph missing sin faltantes nuevos.

## Done When

_Name the observable condition that makes the task complete._

1. SpecSync, sync_spec, check_catalog y sync_catalog exportados desde sldb.api.notations y usables con "sldb notations sync --spec/--catalog/--check".
2. Usa el StoreWriter y el SyncReport de sldb; no hay copia nueva de ninguno de los dos.
3. Los 16 tests de test_sldb_sync y los 6 de test_catalog_notation, portados, pasan contra un store real sin mocks, y el informe coincide campo a campo con el de spec2viz sobre los mismos specs.
4. Reconciliar borra del store lo que salió del spec (SpecNodeDoc y RelationDoc) y, con --prune, los SpecDoc que salieron del catálogo; los avisos salen con el formato de findings de sldb.
5. spec2viz sin cambios (conserva su código; retiro = gate IR13, tarea IR13 del desk de IR).
6. Suite de a un archivo, tools/check.sh y sldb stores build --check en verde; deskops graph missing sin faltantes nuevos.
