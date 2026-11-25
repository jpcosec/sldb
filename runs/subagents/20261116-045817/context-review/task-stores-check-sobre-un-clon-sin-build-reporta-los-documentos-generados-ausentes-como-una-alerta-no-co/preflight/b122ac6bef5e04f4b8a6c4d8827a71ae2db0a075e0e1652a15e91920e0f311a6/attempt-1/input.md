FILE:desk/tasks/task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co.md
---
sldb:
  by: agent
  at: '2026-11-16T04:17:07Z'
  authority: generated
  via: create_document
id: task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co
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
files:
- src/sldb/store/diagnostics.py
- src/sldb/api/stores/store_check.py
- tests/store/test_diagnostics.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-lo-que-el-código-dice-de-sí-mismo-se-publica-con-lo-que-no-se-pudo-probar-a-la-vista
from_drawer: desk/drawer/tasks/task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales.md
---

# stores check sobre un clon sin build reporta los documentos generados ausentes como una alerta, no como miles de errores

## Rationale

_Explain why this task exists or the business driver behind it._

En un checkout limpio de sldb sin correr stores build, `sldb stores check --store .sldb` da FAIL con 2453 errores, todos PythonSymbolDoc "missing: tracked at knowledge/symbols/<id>.md, not on disk" (mensaje de src/sldb/store/diagnostics_models/document_diagnosis.py:85). knowledge/symbols/ está en .gitignore y esos documentos los genera selfdoc python-sync durante stores build, pero sus shards sí están versionados. Los errores reales quedan tapados. La declaración del store ya dice qué rutas son derivadas (StoreDeclaration.derived en src/sldb/api/stores/store_declaration.py; en este repo `derived: [knowledge/symbols/]` en .sldb/store.yaml), pero stores check no la lee. Se elige reportarlos como alerta resumida (opción reversible y local a stores check); dejar de trackear documentos generados es la decisión de la tarea de python-sync. Origen: drawer desk/drawer/tasks/task-stores-check-sobre-un-clon-sin-build-da-rc-1-con-2453-errores-missing-de-pythonsymboldoc-generados-y-tapa-los-errores-reales.md.

## Goal

_Describe the concrete result this task must produce._

En un store cuyo store.yaml declara rutas derived, un documento trackeado ausente cuya ruta cae bajo una de ellas no es error: stores check emite una sola alerta store/generated-missing con el número y el modelo ("2453 PythonSymbolDoc documents are generated and not on disk: run `sldb stores build`"), sigue reportando como error cualquier otro ausente, y su exit code depende solo de los errores.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/store/diagnostics.py (_diagnose_doc línea 36, diagnose_store línea 112) recibir la lista de prefijos derived (leída de la declaración del store) y, para un missing cuya ruta empieza por uno de ellos, contar en lugar de emitir error; al final emitir la alerta resumida por modelo. src/sldb/api/stores/store_check.py (línea 18) pasa la declaración. Tests en tests/store/test_diagnostics.py: store de prueba con derived: [gen/], 3 documentos trackeados ausentes bajo gen/ y 1 ausente fuera de gen/ -> 1 alerta que dice 3 y 1 error. Al cerrar, correr en un clon limpio en /dev/shm `sldb stores check --store .sldb` y `sldb stores build && sldb selfdoc check`, y anotar en el informe el rc y las alertas changed de selfdoc check que queden (resto de la nota de "main de sldb en verde", punto 2). CHANGELOG.md. No entra: destrackear PythonSymbolDoc (decisión de python-sync) ni cambiar selfdoc check.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer diagnostics.py, store_check.py, store_declaration.py y tests/store/test_diagnostics.py (test_missing_document, línea 78). 2) Pasar los prefijos derived. 3) Contar y resumir. 4) Tests. 5) Prueba en clon limpio e informe.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_diagnostics.py
- TMPDIR=/dev/shm pytest -q tests/test_serve_stores_check.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos pasan con el test nuevo; en un clon limpio sin build stores check sale con 0 errores de PythonSymbolDoc y una alerta store/generated-missing; el informe lista las alertas de selfdoc check; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-stores-check-sobre-un-clon-sin-build-reporta-los-documentos-generados-ausentes-como-una-alerta-no-co: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

