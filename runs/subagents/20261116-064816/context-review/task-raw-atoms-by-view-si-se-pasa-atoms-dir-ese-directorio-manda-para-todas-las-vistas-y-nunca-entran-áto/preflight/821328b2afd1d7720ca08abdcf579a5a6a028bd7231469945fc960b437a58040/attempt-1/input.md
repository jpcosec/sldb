FILE:desk/tasks/task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto.md
---
sldb:
  by: agent
  at: '2026-11-16T06:19:51Z'
  authority: generated
  via: create_document
id: task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-004642-suggestion-sldb-notations-atoms-dir-no-manda-el-resolver-trae-tomos-de-un-store-ajeno-heredado-de-spec2viz-que-se-retira.md
depends_on: []
pills: []
files:
- src/sldb/api/matching/atoms_by_view.py
- tests/matching/test_matching_refs.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# raw_atoms_by_view: si se pasa atoms_dir, ese directorio manda para todas las vistas y nunca entran átomos de un store ajeno

## Rationale

_Explain why this task exists or the business driver behind it._

raw_atoms_by_view (src/sldb/api/matching/atoms_by_view.py) toma primero reader.atoms(view.store) de cada vista y solo usa atoms_dir como respaldo para las vistas vacías. Corrido desde labchile_chatbots/docs/spec2viz con --atoms-dir ../../desk/atoms, el store que se descubre era el de deskops y entraron 146 átomos ajenos en vez de los 3 del repo. specir catalog build la llama (repo IR). Heredado de spec2viz, que se retira. Origen: desk/inbox/20261116-004642-suggestion-sldb-notations-atoms-dir-no-manda-el-resolver-trae-tomos-de-un-store-ajeno-heredado-de-spec2viz-que-se-retira.md.

## Goal

_Describe the concrete result this task must produce._

raw_atoms_by_view(views, atoms_dir=d) devuelve para todas las vistas los átomos de d y no consulta ningún store; sin atoms_dir, el comportamiento es el de hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: en raw_atoms_by_view, si atoms_dir es truthy, armar atoms_by_view solo desde parse_atoms(atoms_dir, findings) para todas las vistas, sin llamar reader.atoms; docstring actualizada. Test nuevo en tests/matching/test_matching_refs.py: dos vistas, una con store que tiene átomos y otra sin store, más un atoms_dir con un átomo distinto; con atoms_dir las dos vistas traen solo el átomo del directorio; sin atoms_dir, la vista con store trae los del store. CHANGELOG.md. No entra: cambiar cómo se descubre el store de una vista sin atoms_dir.

Convenciones (valen para todo el contrato): la entrada de CHANGELOG.md es una línea en español bajo el encabezado "## 0.1.13 — not released yet", con el estilo de las entradas vecinas. El commit lo hace el coordinador con deskops closeout commit (mensaje "<título corto de la tarea>"); el ejecutor no hace push. El informe del ejecutor es runs/subagents/<run-dir>/result-summary.md y ahí va todo lo que el contrato manda "anotar en el informe". Los números de línea citados son orientativos a HEAD 7288d93e: se localiza por nombre de función. Un aviso con deskops message send --to <repo> lleva como título el de la tarea y como cuerpo qué cambió y el commit; si el comando responde que el repo no está registrado, el aviso va como línea "Aviso a <repo>: ..." en el informe. "Un store de prueba" se arma con las fixtures o helpers que ya usa el archivo de test nombrado (leerlo primero); si no hay, con sldb.api (stores init, add_model, create_document) en tmp_path.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer atoms_by_view.py y los tests de tests/matching/ que la usan (grep -rn raw_atoms_by_view tests). 2) Cambiar la rama de atoms_dir. 3) Test. 4) CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/matching/

## Done When

_Name the observable condition that makes the task complete._

tests/matching/ pasa con el test nuevo; CHANGELOG y commit; aviso a IR con deskops message send --to IR (si no está registrado, línea "Aviso a IR" en result-summary.md).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-raw-atoms-by-view-si-se-pasa-atoms-dir-ese-directorio-manda-para-todas-las-vistas-y-nunca-entran-áto: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

