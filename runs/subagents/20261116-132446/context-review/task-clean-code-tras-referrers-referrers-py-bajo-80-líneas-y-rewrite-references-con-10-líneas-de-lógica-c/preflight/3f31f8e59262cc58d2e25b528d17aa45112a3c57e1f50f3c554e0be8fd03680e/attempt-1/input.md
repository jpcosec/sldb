FILE:desk/tasks/task-clean-code-tras-referrers-referrers-py-bajo-80-líneas-y-rewrite-references-con-10-líneas-de-lógica-c.md
---
sldb:
  by: agent
  at: '2026-11-16T13:08:49Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-referrers-referrers-py-bajo-80-líneas-y-rewrite-references-con-10-líneas-de-lógica-c
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/api/edges/referrers.py
- src/sldb/api/edges/rewrite_references.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-referrers-y-rewrite-references-trabajan-sobre-un-grafo-armado-en-proceso-excluyen-fuentes-y-no-cuent
---

# Clean code tras referrers: referrers.py bajo 80 líneas y rewrite_references con 10 líneas de lógica como máximo

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: src/sldb/api/edges/referrers.py tiene 97 líneas efectivas (máximo 80) y la función rewrite_references de src/sldb/api/edges/rewrite_references.py tiene 15 líneas de lógica (máximo 10). Lo introdujo task-referrers-y-rewrite-references (3772a1fa); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-referrers-y-rewrite-references, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Mover document_paths, frontmatter_lines y _in_frontmatter de referrers.py a un módulo nuevo referrer_frontmatter.py del paquete sldb.api.edges (reexportar document_paths y frontmatter_lines desde referrers.py); partir rewrite_references en pasos con nombre (resolver grafo y exclusiones, planificar, escribir) dentro de rewrite_references.py o en un módulo vecino. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_referrers.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_rewrite_references.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Todos los comandos de Validation pasan (incluidos test_clean_code_rules y check.sh --fast); git diff no toca archivos de tests de comportamiento; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-clean-code-tras-referrers-referrers-py-bajo-80-líneas-y-rewrite-references-con-10-líneas-de-lógica-c: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

