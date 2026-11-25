FILE:desk/tasks/task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2.md
---
sldb:
  by: agent
  at: '2026-11-16T17:34:37Z'
  authority: generated
  via: save_document_payload
id: task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2
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
- pyproject.toml
- uv.lock
- src/sldb/code/runtime.py
- src/sldb/code/scan.py
- src/sldb/models/code_ref.py
- src/sldb/api/anchors/record_anchor.py
- tests/api/test_anchors.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
---

# sldb.code lee TS y TSX: readers, facts y anclas con tree-sitter-typescript como extra (B2, parte TS; SQL va aparte)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR ancla cada nodo extraído a su fuente con las anclas de código de sldb y debe leer Django (Python, cubierto), SQL y React TSX/TS. Decisión de JP 2026-11-15: lo genérico va a sldb y specIR solo mapea al dominio (IR08 e IR09 quedan como mapeo sobre estos extractores).

## Goal

_Describe the concrete result this task must produce._

El paquete sldb.code lee TS y TSX, publica sus hechos de fuente con la misma forma que los de Python y soporta anclas code:<ruta>.ts|.tsx::<símbolo>, con tree-sitter-typescript como parte del extra code; SQL lo hace la tarea hermana.

## Scope

_State what is in scope and what is out of scope._

Amplía el pedido parcial del inbox sldb 20261115-022446, que solo pedía anclas: aquí entran readers y facts, no solo anclas. Hoy el escáner recorre solo .py con tree-sitter-python (extra code); sldb.code tiene readers, facts, fingerprints, ids, imports y scan. Alcance: TS/TSX (componentes, funciones, hooks, tipos, imports) y SQL (tablas, columnas, vistas, DDL y migraciones); hechos en la misma forma que los de Python (ver el atom del inventario de código como hechos de fuente); record_anchor y check_anchors con la misma referencia code:<ruta>::<qualified_name>, fingerprints por nodo, estados y reconexión; gramáticas como extras opcionales. Reutilizar la maquinaria existente de Python, no duplicarla. Fuera de alcance: mapear a conceptos de dominio (eso es specIR).

Precisiones (coordinador, 2026-11-16): esta tarea cubre TS y TSX; SQL va en la tarea hermana que depende de esta. kind de los hechos TS: component (función o const que devuelve JSX, nombre en mayúscula), hook (función cuyo nombre empieza por use), type (type o interface), function (el resto), module (el archivo). qualified_name del módulo: la ruta sin extensión con '.' como separador, igual que py_module_name. docstring: el comentario JSDoc /** */ inmediatamente anterior. NORMALIZATION no cambia si la salida de .py es la misma.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) pyproject.toml: agregar tree-sitter-typescript>=0.23 al extra code (la versión 0.23.2 está en PyPI) y correr `uv lock` (único cambio de uv.lock: el paquete nuevo; si uv.lock tiene cambios ajenos sin commitear, el ejecutor lo anota y deja al coordinador decidir cómo commitear el lock). 2) src/sldb/code/runtime.py: un runtime por lenguaje elegido por extensión (.py, .ts, .tsx) en lugar del Language de Python fijo; si falta la gramática, TreeSitterUnavailable nombra el extra. 3) Un módulo nuevo lang_ts.py en el paquete sldb.code con la query, los readers (JSDoc /** */ como docstring) y los imports de TS/TSX; scan_file (src/sldb/code/scan.py, 78 líneas efectivas: la dispatch por extensión saca código a módulos nuevos) despacha por extensión y find_files incluye .ts/.tsx solo si la gramática está. 4) src/sldb/models/code_ref.py (parse_code_ref) acepta .ts y .tsx; src/sldb/api/anchors/record_anchor.py (recorded_with) informa la gramática del archivo. 5) Fixtures en tests/fixtures/treesitter/ con un componente .tsx, un hook y un tipo; tests de intact/changed/lost/reconnected que se saltan sin la gramática.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_agreement.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/notations/test_component_spec_python.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan; un ancla code:<ruta>.tsx::<Componente> se registra y check_anchors la informa intact, changed al cambiar el cuerpo, lost al borrarla y reconnected al moverla; sldb sin tree-sitter-typescript sigue escaneando .py; la salida de los .py no cambia (NORMALIZATION igual); CHANGELOG y commit; aviso a IR anotado en result-summary.md (IR no está en el registro). La tarea hermana de SQL depende de esta.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

