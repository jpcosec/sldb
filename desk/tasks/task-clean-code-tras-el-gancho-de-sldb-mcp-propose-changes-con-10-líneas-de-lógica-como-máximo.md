---
sldb:
  by: agent
  at: '2026-11-16T13:10:32Z'
  authority: generated
  via: create_document
id: task-clean-code-tras-el-gancho-de-sldb-mcp-propose-changes-con-10-líneas-de-lógica-como-máximo
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
- src/sldb/mcp/write/tools.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-una-extensión-de-sldb-mcp-agrega-reglas-de-dominio-a-la-escritura-registrando-validadores-de-lote-si
---

# Clean code tras el gancho de sldb mcp: propose_changes con 10 líneas de lógica como máximo

## Rationale

_Explain why this task exists or the business driver behind it._

La integración del lote 2 de sldb (wA:p1, 2026-11-16) no pasa tools/check.sh: el método propose_changes de src/sldb/mcp/write/tools.py tiene 11 líneas de lógica (máximo 10). Lo introdujo task-sldb-mcp-gancho (11b6c537); ni su ejecutor ni su tester corrieron tests/test_clean_code_rules.py.

## Goal

_Describe the concrete result this task must produce._

tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-sldb-mcp-gancho, con el mismo comportamiento: los tests de la tarea original siguen verdes sin cambios.

## Scope

_State what is in scope and what is out of scope._

Entra: Reglas de tests/test_clean_code_rules.py: como máximo 1 clase por archivo, 80 líneas efectivas por archivo y 10 líneas de lógica por función. Se arregla extrayendo funciones o clases a módulos nuevos junto al original (mismo paquete), sin cambiar el comportamiento ni la API pública: los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport). Extraer la corrida de validadores de dominio y la respuesta de rechazo (o el armado del lote sellado) a un método o función privada con nombre, compartida con apply_changes si aplica. Una línea en CHANGELOG.md bajo '## 0.1.13 — not released yet' que diga que es un arreglo de clean code. No entra: cambiar comportamiento, tests de comportamiento ni otras violaciones que no sean de estos archivos (si check.sh muestra otras, se anotan en result-summary.md y no se tocan).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Correr tests/test_clean_code_rules.py para ver la violación exacta. 2) Aplicar el arreglo de Scope. 3) Correr cada comando de Validation. 4) Comprobar con git diff que los tests de comportamiento no cambiaron.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_extension.py
- TMPDIR=/dev/shm uvx --from 'pytest>=8' --with-editable '.[mcp,code]' pytest -q tests/mcp/test_write_tools.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Todos los comandos de Validation pasan (incluidos test_clean_code_rules y check.sh --fast); git diff no toca archivos de tests de comportamiento; CHANGELOG y commit.
