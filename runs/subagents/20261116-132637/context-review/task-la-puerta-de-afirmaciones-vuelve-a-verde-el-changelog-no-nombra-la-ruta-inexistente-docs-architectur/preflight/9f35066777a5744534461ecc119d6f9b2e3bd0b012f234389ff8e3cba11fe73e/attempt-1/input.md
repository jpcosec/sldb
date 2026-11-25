FILE:desk/tasks/task-la-puerta-de-afirmaciones-vuelve-a-verde-el-changelog-no-nombra-la-ruta-inexistente-docs-architectur.md
---
sldb:
  by: agent
  at: '2026-11-16T13:15:56Z'
  authority: generated
  via: save_document_payload
id: task-la-puerta-de-afirmaciones-vuelve-a-verde-el-changelog-no-nombra-la-ruta-inexistente-docs-architectur
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
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-las-pruebas-de-notaciones-paletas-vista-resuelta-y-viewdoc-que-tenía-spec2viz-viven-en-sldb-y-solo-i
---

# La puerta de afirmaciones vuelve a verde: el CHANGELOG no nombra como ruta un vistas.yml que no existe

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: CHANGELOG.md (la línea de la tarea de portar las pruebas de spec2viz) nombra como ruta del repo un vistas.yml bajo docs-architecture que no existe; la copia vive en tests/notations/fixtures/docs/architecture/vistas.yml. Lo introdujo task-portar-a-sldb-las-pruebas-de-spec2viz (bee4ae7f); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-portar-a-sldb-las-pruebas-de-spec2viz, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Corregir esa línea del CHANGELOG para que nombre la ruta real (tests/notations/fixtures/docs/architecture/vistas.yml) o la describa sin forma de ruta; no tocar otras líneas. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Todos los comandos de Validation pasan (incluidos test_clean_code_rules y check.sh --fast); git diff no toca archivos de tests de comportamiento; CHANGELOG y commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-la-puerta-de-afirmaciones-vuelve-a-verde-el-changelog-no-nombra-la-ruta-inexistente-docs-architectur: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

