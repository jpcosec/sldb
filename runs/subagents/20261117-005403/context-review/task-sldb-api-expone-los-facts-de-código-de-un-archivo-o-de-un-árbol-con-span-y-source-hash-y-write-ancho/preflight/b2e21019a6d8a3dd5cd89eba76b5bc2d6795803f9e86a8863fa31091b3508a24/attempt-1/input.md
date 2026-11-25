FILE:desk/tasks/task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho.md
---
sldb:
  by: agent
  at: '2026-11-17T00:42:28Z'
  authority: generated
  via: save_document_payload
id: task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md
depends_on: []
pills: []
files:
- src/sldb/api/anchors/__init__.py
- CHANGELOG.md
- tests/api/test_anchors.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-sldb-code-lee-ts-tsx-js-y-jsx-con-un-mismo-reader-y-ancla-sus-símbolos
---

# sldb.api expone los facts de código de un archivo o de un árbol, con span y source_hash, y write_anchor es público (C1, C2 y C5 de IR)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR solo puede consumir sldb.api, y los facts de código (Python, TS, TSX, JS, JSX y SQL) solo existen en funciones internas: sldb.code.scan.scan_file y scan_tree. IR08 e IR09 quedan bloqueadas sin una función pública que los liste (C1), sin el span y el source_hash de cada símbolo, que la validación de IR pide como archivo, línea y hash (C2), y write_anchor de sldb.api.anchors.anchor_docs está fuera de __all__ (C5). Origen: desk/inbox/20261116-211648-suggestion-ir08-ir09-bloqueadas-b2-lee-ts-tsx-js-jsx-y-sql-pero-sldb-api-no-expone-los-facts-c1-c5.md.

## Goal

_Describe the concrete result this task must produce._

specIR obtiene con una sola llamada pública de sldb.api los facts de un archivo o de un árbol del proyecto, cada uno con path, span (líneas de inicio y fin), source_hash del archivo, kind, qualified_name, signature, doc, relations y attrs, y puede escribir un ancla con write_anchor importado desde sldb.api.anchors.

## Scope

_State what is in scope and what is out of scope._

Entra: un paquete nuevo code dentro de sldb.api con code_facts(root, paths=None) que devuelve la lista de facts de los archivos dados (rutas relativas a root) o de todo el árbol si paths es None, reutilizando scan_file y scan_tree sin duplicar lógica; los facts salen con la forma que ya tienen (fact() de sldb.code.facts), garantizando que span y source_hash vengan llenos; si un archivo no tiene gramática disponible, se omite y la respuesta lo lista en un campo aparte (skipped). Exportar code_facts en el __all__ del paquete nuevo y documentarlo en el docstring. Agregar write_anchor al __all__ de sldb.api.anchors. Tests de la API con un árbol de prueba que mezcle .py, .tsx y .sql. CHANGELOG. No entra: facts nuevos (otras tareas C3 y C4), cambiar la forma de los facts, la CLI.

Precisiones (intento 2): code_facts(root, paths=None) devuelve un dict {"facts": [...], "skipped": [...]}: facts es la lista de facts y skipped la lista de rutas (relativas a root, ordenadas) que no se escanearon por falta de gramática. path en cada fact es relativo a root, con / como separador, como ya lo da scan_file. span es el que ya producen los readers: {"start_line", "end_line"}, base 1 e inclusivo. source_hash es el que ya producen los readers: "sha256:<hex>" de los bytes del archivo; code_facts no lo recalcula, solo garantiza que no venga vacío. Los tests de code_facts van en tests/api/test_anchors.py porque ese archivo ya cubre la API pública de código y anclas; no se crea un archivo de test nuevo. El aviso a IR lo manda el coordinador por deskops message send.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer sldb.code.scan (scan_file, scan_tree), sldb.code.files (find_files), sldb.code.facts y cómo se calcula source_hash. 2) Escribir el paquete nuevo con code_facts. 3) Agregar write_anchor al __all__ de sldb.api.anchors. 4) Tests de la API nueva en tests/api/test_anchors.py. 5) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; from sldb.api.code import code_facts y from sldb.api.anchors import write_anchor funcionan; cada fact devuelto tiene span y source_hash no vacíos; CHANGELOG y commit; aviso a IR.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-api-expone-los-facts-de-código-de-un-archivo-o-de-un-árbol-con-span-y-source-hash-y-write-ancho: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

