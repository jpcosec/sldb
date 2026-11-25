FILE:desk/tasks/task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio.md
---
sldb:
  by: agent
  at: '2026-11-16T04:05:58Z'
  authority: generated
  via: create_document
id: task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-cada-escritura-en-el-desk-de-sldb-imprime-miles-de-líneas-sections-rebuild-missing-de-knowledge-symb.md
depends_on: []
pills: []
files:
- src/sldb/store/section_sync.py
- tests/store/test_semantic_rebuild.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# Una escritura en un store con documentos generados ausentes no imprime una línea por cada uno (Sections rebuild missing)

## Rationale

_Explain why this task exists or the business driver behind it._

Cada comando que escribe en el desk de sldb (add atom, edit task, docs update) imprime unas 2500 líneas "Sections rebuild: doc '<id>' missing at <root>/knowledge/symbols/<id>.md". Son PythonSymbolDoc indexados en el store pero generados (knowledge/symbols/ está en .gitignore), así que no existen en un checkout limpio. El comando termina bien, pero el ruido tapa el resultado. La fuente es src/sldb/store/section_sync.py: _missing_doc (línea 72) emite un logger.warning por documento, llamado desde _sync_one_section (línea 56). Origen: desk/inbox/inbox-note-cada-escritura-en-el-desk-de-sldb-imprime-miles-de-líneas-sections-rebuild-missing-de-knowledge-symb.md.

## Goal

_Describe the concrete result this task must produce._

Una reconstrucción de secciones con N documentos ausentes emite a lo sumo una línea de aviso con el número de ausentes, el modelo y hasta 3 ejemplos, en lugar de N líneas.

## Scope

_State what is in scope and what is out of scope._

Entra: en src/sldb/store/section_sync.py acumular los ausentes durante la reconstrucción y emitir un solo logger.warning al final con el formato "Sections rebuild: <n> documents missing on disk (<modelo>: <n>, ...); e.g. <ruta1>, <ruta2>, <ruta3>". Las rutas que llaman (src/sldb/api/documents/payload_save_steps.py:112, src/sldb/api/documents/untrack_document.py:68, src/sldb/api/edges/rebuild_edges.py:37) no cambian. Test en tests/store/test_semantic_rebuild.py con caplog: un store de prueba con 5 documentos trackeados cuyo archivo se borró produce exactamente un registro de warning que dice 5. CHANGELOG.md. No entra: limitar la reconstrucción a los documentos que tocó la transacción (otro cambio, más invasivo), ni cambiar cómo stores check reporta los PythonSymbolDoc ausentes (tarea de stores check sobre un clon sin build).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/store/section_sync.py entero. 2) Cambiar _missing_doc para que agregue a una lista que vive durante la llamada de nivel superior de la reconstrucción y emitir el resumen al final. 3) Test con caplog. 4) Comprobación manual en el desk: `deskops edit task <una tarea> summary "x" --root sldb` en un worktree limpio imprime una línea de Sections en lugar de miles (anotarlo en el informe; no commitear ese cambio de desk).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_semantic_rebuild.py

## Done When

_Name the observable condition that makes the task complete._

El test nuevo pasa (5 ausentes -> 1 warning que dice 5); test_semantic_rebuild.py completo pasa; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

