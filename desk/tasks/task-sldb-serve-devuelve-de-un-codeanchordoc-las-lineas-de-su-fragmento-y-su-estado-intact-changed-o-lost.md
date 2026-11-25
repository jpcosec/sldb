---
sldb:
  by: agent
  at: '2026-11-25T06:28:15Z'
  authority: generated
  via: create_document
id: task-sldb-serve-devuelve-de-un-codeanchordoc-las-lineas-de-su-fragmento-y-su-estado-intact-changed-o-lost
status: draft
summary: ''
tags: []
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

# sldb serve devuelve de un CodeAnchorDoc las lineas de su fragmento y su estado intact, changed o lost

## Rationale

_Explain why this task exists or the business driver behind it._

Nota de IR 20261125-032546-suggestion-sldb-serve-una-ruta-get-que-devuelva-de-un-codeanchordoc-las-lineas-de-su-fragmento-y-su-estado-vigente-o-cambiado (U9, pestana Anclajes de la UI de specIR): serve no lee codigo ni anclas; el estado lo calcula sldb.api.anchors.check_anchors.

## Goal

_Describe the concrete result this task must produce._

Una ruta GET de solo lectura que, dado un anchor, devuelva ruta, rango, lineas del fragmento con contexto y su estado.

## Scope

_State what is in scope and what is out of scope._

src/sldb/cli/serve (ruta nueva y su registro en routes.dispatch_get) y un test. Fuera: escritura, la UI.

## Implementation Path

_Outline the expected implementation route or affected surface._

Repo /mnt/ssd/proyectos/SLDB_1/sldb. GET /anchors/<nombre del CodeAnchorDoc>?context=N (default 3): {path, start_line, end_line, lines: [{n, text, in_fragment}], state} donde state sale de sldb.api.anchors.check_anchors (intact/changed/lost) y lines se leen del archivo bajo project_root (si el archivo no existe, lines vacio y state lost). 404 si el anchor no existe; rutas fuera de project_root se rechazan. Test nuevo tests/serve/test_anchor_route.py con un store temporal y un anchor sobre un .py: intact con las lineas correctas; tras editar el fragmento, changed; anchor inexistente 404.

## Validation

_List the checks required before this task can close._

- TMPDIR=/mnt/ssd/tmp/sldb1 /mnt/ssd/proyectos/SLDB_1/.venv/bin/python -m pytest -q -p no:cacheprovider tests/serve/test_anchor_route.py

## Done When

_Name the observable condition that makes the task complete._

GET /anchors/<nombre> devuelve lineas y estado y el test nuevo pasa.
