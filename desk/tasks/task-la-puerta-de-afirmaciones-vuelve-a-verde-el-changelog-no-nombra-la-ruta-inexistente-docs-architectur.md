---
sldb:
  by: agent
  at: '2026-11-16T13:41:18Z'
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

Entra: solo CHANGELOG.md. En la línea de la tarea de portar las pruebas de spec2viz (la que empieza con 'Las pruebas de spec2viz de notaciones, paletas, vista resuelta y ViewDoc pasan a sldb'), donde nombra la copia de vistas.yml, escribir la ruta real tests/notations/fixtures/docs/architecture/vistas.yml en lugar de la ruta sin el prefijo tests/notations/fixtures. No se agrega otra línea al CHANGELOG ni se toca otra línea. No entra: código, tests ni otras afirmaciones; si tools/check.sh --fast muestra otras afirmaciones falsas que no son de esa línea, se anotan en result-summary.md del run y no se tocan.

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
