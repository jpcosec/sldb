---
sldb:
  by: agent
  at: '2026-11-17T05:09:24Z'
  authority: generated
  via: create_document
id: task-el-valor-de-un-campo-se-renderiza-literal-render-model-markdown-deja-de-pasar-los-valores-del-usuari
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos-llaves-dobles-rompen-expresiones-se-evaluan.md
depends_on: []
pills: []
files:
- src/sldb/core/renderer_engine/base.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El valor de un campo se renderiza literal: render_model_markdown deja de pasar los valores del usuario por Jinja

## Rationale

_Explain why this task exists or the business driver behind it._

render_model_markdown interpreta como Jinja el valor de un campo de texto: src/sldb/core/renderer_engine/base.py (BaseRenderer.replace_markers) sustituye los valores de los marcadores dentro del texto fuente del bloque y después compila todo con jinja_env.from_string(source).render(**data). Dos o tres llaves de apertura seguidas rompen el render con TemplateSyntaxError; una expresión Jinja válida se evalúa y se guarda alterada (7*7 entre llaves dobles se guarda como 49; un comentario Jinja desaparece) con rc 0. Le pasa a deskops en edit task y message send. Es una inyección de plantilla con datos del usuario. Origen: desk/inbox/20261117-015212-suggestion-render-model-markdown-interpreta-como-jinja-el-valor-de-los-campos-llaves-dobles-rompen-expresiones-se-evaluan.md.

## Goal

_Describe the concrete result this task must produce._

El valor de un campo se guarda literal, byte a byte, y vuelve igual en extract; solo la plantilla del modelo es Jinja. Ningún valor con llaves, porcentajes o almohadillas cambia el render ni lo rompe.

## Scope

_State what is in scope and what is out of scope._

Entra: separar en replace_markers lo que es plantilla de lo que es dato: los valores de los marcadores no llegan a Jinja como código (por ejemplo, sustituirlos por variables de Jinja o por tokens que se reemplazan después del render, o escapar el valor con raw); mantener el comportamiento de optrev y de las líneas ausentes; tests de roundtrip con valores que contengan dos y tres llaves de apertura, una expresión, un comentario Jinja, bloques de control y llaves de cierre, en un archivo de tests del renderer existente. CHANGELOG. No entra: cambiar la sintaxis de las plantillas.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/core/renderer_engine/base.py y sus subclases, y quién llama a replace_markers. 2) Reproducir los casos de la nota con un modelo de prueba. 3) Implementar la separación. 4) Tests. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_documents.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_structural_noise.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos de roundtrip; los casos de la nota se guardan literales; CHANGELOG y commit; aviso a deskops para que quite su xfail.
