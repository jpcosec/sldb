FILE:desk/tasks/task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio.md
---
sldb:
  by: agent
  at: '2026-11-16T06:13:26Z'
  authority: generated
  via: save_document_payload
id: task-una-escritura-en-un-store-con-documentos-generados-ausentes-no-imprime-una-línea-por-cada-uno-sectio
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
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

Precisiones (preflight-1): la acumulación usa el report que ya recorre la reconstrucción (report.docs_skipped_missing y report.verbose en section_sync.py): _missing_doc deja de llamar a logger.warning y agrega la ruta relativa al proyecto a una lista nueva report.missing_paths; la función de nivel superior que arma el report emite al terminar un solo logger.warning si la lista no está vacía. Formato exacto: "Sections rebuild: <n> documents missing on disk (<Modelo>: <n>[, <Modelo>: <n>...]); e.g. <ruta1>, <ruta2>, <ruta3>" con modelos en orden alfabético y las tres primeras rutas en orden alfabético. La comprobación manual en el desk es opcional y se hace con una copia del repo en /dev/shm, no en el checkout.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

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

