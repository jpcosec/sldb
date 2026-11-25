FILE:desk/tasks/task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com.md
---
sldb:
  by: agent
  at: '2026-11-17T15:39:05Z'
  authority: generated
  via: save_document_payload
id: task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261117-021700-suggestion-el-scan-de-enlaces-cuenta-enlaces-dentro-de-bloques-de-c-digo.md
depends_on: []
pills: []
files:
- src/sldb/links/parser.py
- tests/test_links.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# El scan de enlaces ignora el contenido de los bloques de código (fenced e inline) y no los informa como enlaces rotos

## Rationale

_Explain why this task exists or the business driver behind it._

En sldb-ui, el scan de enlaces de un documento real lista dos veces 'target' como enlace roto, y los dos vienen de ejemplos dentro de bloques de código del Markdown. Origen: desk/inbox/20261117-021700-suggestion-el-scan-de-enlaces-cuenta-enlaces-dentro-de-bloques-de-c-digo.md.

## Goal

_Describe the concrete result this task must produce._

El scan de enlaces de sldb (comando sldb links y la API que usa) no cuenta como enlace nada que esté dentro de un bloque de código cercado ni de un código en línea; los enlaces reales se siguen detectando igual.

## Scope

_State what is in scope and what is out of scope._

Decisión del supervisor (2026-11-17): el scan deja de reconocer Markdown con reglas propias. Usa el parser que sldb ya tiene, markdown-it-py (dependencia directa en pyproject.toml), con la misma configuración que src/sldb/core/ast/markdown_ast_handler.py: MarkdownIt("gfm-like") con front_matter_plugin. El árbol de tokens decide qué es código, y los enlaces se extraen de lo que no lo es.

Entra: (1) parse_links (src/sldb/links/parser.py) parsea el documento con ese parser; los tokens fence y code_block no aportan enlaces; en cada token inline, los hijos code_inline no aportan enlaces y el resto de los hijos se recorre en orden, con softbreak y hardbreak como salto de línea, para que [[...]] y [pred:: [[...]]] se sigan reconociendo con los dos regex que hay hoy (LINK_PATTERN e INLINE_PREDICATE_LINK_PATTERN) sin cambiarlos. Lo que no es código (front matter, html_block, html_inline, tablas, encabezados) se escanea como hoy. El orden de salida y la forma de ParsedLink no cambian. (2) Una sola instancia de MarkdownIt por proceso (como _PARSER en src/sldb/store/section_rebuild.py). (3) La lógica de recorrer tokens va a un módulo nuevo del paquete sldb.links para que parser.py siga bajo las reglas de clean code. (4) Tests en tests/test_links.py: todos los bordes de los tres informes de tester anteriores (runs/subagents/20261116-test-lk/result-summary.md, runs/subagents/20261116-test-lk-c1/result-summary.md y runs/subagents/20261116-test-lk-c2/result-summary.md): código indentado en ítem de lista, backtick escapado, CRLF, fence en la línea del marcador de lista, code span que cruza un límite de bloque; más un documento con enlaces reales y ejemplos dentro de código cercado, indentado y en línea. Los tests del intento anterior en runs/subagents/20261116-exec-lk-c2/executor-diff-lk-c2.patch se pueden reutilizar; su código de enmascarado propio (code_mask, code_blocks) no se usa. CHANGELOG.md.

No entra: wikilinks dentro de HTML <code>; sldb docs compose (expande [[...]] por su cuenta); otros tipos de referencia; agregar dependencias.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer src/sldb/links/parser.py, src/sldb/core/ast/markdown_ast_handler.py y src/sldb/store/section_rebuild.py (cómo se arma y se cachea el parser). 2) Escribir el recorrido de tokens en un módulo nuevo de sldb.links y hacer que parse_links lo use. 3) Tests. 4) Validation. 5) Corpus: sobre git ls-files '*.md' comparar parse_links contra HEAD (git archive HEAD src en /dev/shm); toda diferencia tiene que ser un [[...]] que está dentro de código según el mismo parser. 6) Medir el tiempo de parse_links sobre el corpus antes y después y anotarlo en result-summary.md.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_links_batch_cli.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos; los bordes de los tres informes de tester previos dan lo mismo que markdown-it; en el corpus del repo ningún enlace real que HEAD detecta se pierde; result-summary.md tiene el tiempo del corpus antes y después; CHANGELOG. Commit y aviso a sldb-ui los hace el coordinador.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-el-scan-de-enlaces-ignora-el-contenido-de-los-bloques-de-código-fenced-e-inline-y-no-los-informa-com: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

