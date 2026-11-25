FILE:desk/tasks/task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla.md
---
sldb:
  by: agent
  at: '2026-11-16T04:08:56Z'
  authority: generated
  via: create_document
id: task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/inbox/inbox-note-h1-de-placeholder-deskops-api-pública-para-leer-los-párrafos-ancla-literales-de-la-plantilla-de-un-m.md
depends_on: []
pills: []
files:
- src/sldb/api/model_registry/template_anchors.py
- src/sldb/api/__init__.py
- src/sldb/core/template_extractor.py
- tests/test_literal_paragraph_anchor.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-template-de-un-modelo-es-estable-sus-recetas-se-calculan-una-vez-no-en-cada-extract
---

# sldb.api.template_anchors devuelve, por campo de un modelo, el párrafo ancla literal de su plantilla

## Rationale

_Explain why this task exists or the business driver behind it._

deskops (task.debug "edit no guarda el párrafo placeholder de la plantilla como contenido") necesita saber qué párrafo literal ancla cada campo (como "_Outline the expected implementation route or affected surface._" antes de implementation_path) para no guardarlo como valor. Hoy lo saca con internos de sldb: AST_Handler().split_nodes sobre model.__template__ y TemplateExtractor().extract_nodes (src/sldb/core/template_extractor.py), recorriendo las recetas (outer_type paragraph, anchor, props). 9dcabd9a arregló un caso vecino (tests/test_literal_paragraph_anchor.py) pero no hay API pública. Se elige la opción (a) de la nota, API de lectura, porque es aditiva; la opción (b), descartar en render/save un valor igual a su ancla, cambia el contrato de escritura y no se hace aquí. Origen: desk/inbox/inbox-note-h1-de-placeholder-deskops-api-pública-para-leer-los-párrafos-ancla-literales-de-la-plantilla-de-un-m.md.

## Goal

_Describe the concrete result this task must produce._

sldb.api.template_anchors(model_type) -> dict[str, str] devuelve, para cada campo cuyo marcador en __template__ va precedido por un párrafo literal que ancla su extracción, el texto exacto de ese párrafo tal como render lo escribe y extract lo consume; los campos sin párrafo ancla no aparecen.

## Scope

_State what is in scope and what is out of scope._

Entra: módulo nuevo src/sldb/api/model_registry/template_anchors.py que usa las mismas recetas que el extractor (TemplateExtractor y el split de nodos), sin reimplementar el parseo; export en sldb.api. Tests en tests/test_literal_paragraph_anchor.py: para un modelo de prueba con dos campos anclados por párrafos en cursiva y uno sin ancla, el dict tiene exactamente las dos claves con el texto literal; para TaskDoc de deskops no se prueba (es otro repo). CHANGELOG.md. No entra: la opción (b), cambiar render o extract, ni tocar deskops (aviso al cerrar).

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/core/template_extractor.py, src/sldb/runtime/validation.py (65-68) y tests/test_literal_paragraph_anchor.py. 2) Ubicar en las recetas el anchor de tipo paragraph previo a cada campo. 3) Implementar y exportar. 4) Tests. 5) bash tools/check.sh --fast por las capas (api puede importar core).

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_literal_paragraph_anchor.py
- bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

`from sldb.api import template_anchors` funciona; el test del modelo de prueba pasa; check.sh --fast pasa; CHANGELOG, commit y aviso a deskops con deskops message send --to deskops.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-api-template-anchors-devuelve-por-campo-de-un-modelo-el-párrafo-ancla-literal-de-su-plantilla: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

