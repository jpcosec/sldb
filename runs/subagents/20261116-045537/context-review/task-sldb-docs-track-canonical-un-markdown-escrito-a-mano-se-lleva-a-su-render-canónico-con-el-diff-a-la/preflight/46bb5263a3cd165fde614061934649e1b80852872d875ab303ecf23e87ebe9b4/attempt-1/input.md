FILE:desk/tasks/task-sldb-docs-track-canonical-un-markdown-escrito-a-mano-se-lleva-a-su-render-canónico-con-el-diff-a-la.md
---
sldb:
  by: agent
  at: '2026-11-16T04:15:21Z'
  authority: generated
  via: create_document
id: task-sldb-docs-track-canonical-un-markdown-escrito-a-mano-se-lleva-a-su-render-canónico-con-el-diff-a-la
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/tasks/task-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo.md
depends_on: []
pills: []
files:
- src/sldb/api/documents/track_document_file.py
- src/sldb/cli/parsers/docs1.py
- src/sldb/assets/skills/sldb.md
- tests/test_cli_v2.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/tasks/task-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo.md
---

# sldb docs track --canonical: un Markdown escrito a mano se lleva a su render canónico, con el diff a la vista, antes de trackearlo

## Rationale

_Explain why this task exists or the business driver behind it._

Los LLM se saltan la API de escritura y escriben el Markdown directo: el render parece la cosa y no una proyección, escribirlo cuesta una llamada y la API cuesta descubrimiento, y la divergencia aparece después en stores check. `sldb docs track` ya extrae, valida y rechaza ruido estructural (src/sldb/api/documents/track_document_file.py:67-70, 9450adab), pero cuando el archivo no hace round trip solo lo rechaza: no devuelve el render canónico ni el diff, que es lo que le daría al autor algo visible a cambio de usar la API. Parte (b) del ítem del drawer; las partes (a) hook PreToolUse y (c) autocarga de la skill van en una task.decision aparte. Origen: drawer desk/drawer/tasks/task-los-llm-se-saltan-la-api-de-escritura-y-escriben-markdown-directo.md.

## Goal

_Describe the concrete result this task must produce._

`sldb docs track <ruta> --model <M> --canonical` extrae el payload del archivo, lo renderiza con el modelo, imprime el diff unificado entre el archivo y el render canónico, reescribe el archivo con el render canónico y lo trackea; si el payload no se puede extraer o no valida, no escribe nada y sale con 1 mostrando el error. Sin --canonical, track se comporta como hoy.

## Scope

_State what is in scope and what is out of scope._

Entra: flag --canonical en el parser de track (src/sldb/cli/parsers/docs1.py, _track) y su manejo en el comando; en la API, un parámetro canonical: bool = False en track_document_file que, antes de _refuse_unfit, reemplaza el texto por render_model_markdown(extract_model_data(texto)) y devuelve el diff en el DocumentReference (campo canonical_diff opcional, "" si no hubo cambios). El diff se calcula con difflib.unified_diff. Tests en tests/test_cli_v2.py: un archivo con un campo escrito con espacios de más se trackea con --canonical, el archivo queda canónico y la salida tiene el diff; un archivo sin payload extraíble sale con 1 y queda intacto; sin --canonical el mismo archivo se rechaza como hoy. CHANGELOG.md y la línea correspondiente en la skill src/sldb/assets/skills/sldb.md. No entra: el hook PreToolUse, la autocarga de la skill, POST /docs de sldb serve.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/cli/parsers/docs1.py, el comando de docs track (grep -rn "track_document_file" src/sldb/cli), track_document_file.py y src/sldb/runtime/validation.py (extract_model_data, render_model_markdown). 2) Implementar canonical en la API. 3) Flag en la CLI. 4) Tests, skill y CHANGELOG.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/test_cli_v2.py
- TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py

## Done When

_Name the observable condition that makes the task complete._

Los dos comandos pasan con los tres casos nuevos; `sldb docs track --help` muestra --canonical; skill y CHANGELOG actualizados; commit.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-docs-track-canonical-un-markdown-escrito-a-mano-se-lleva-a-su-render-canónico-con-el-diff-a-la: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

