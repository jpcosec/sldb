FILE:desk/tasks/task-sldb-code-lee-sql-tablas-columnas-vistas-e-índices-de-ddl-y-migraciones-como-hechos-con-anclas-con-t.md
---
sldb:
  by: agent
  at: '2026-11-16T20:29:10Z'
  authority: generated
  via: save_document_payload
id: task-sldb-code-lee-sql-tablas-columnas-vistas-e-índices-de-ddl-y-migraciones-como-hechos-con-anclas-con-t
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
- host:robocop2
current_node: ritual-execution
history: []
references:
- desk/inbox/20261115-022446-suggestion-specir-anclas-de-c-digo-para-tsx-y-sql.md
depends_on:
- task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2
pills: []
files:
- pyproject.toml
- uv.lock
- src/sldb/code/runtime.py
- src/sldb/models/code_ref.py
- tests/api/test_anchors.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-el-inventario-de-código-de-sldb-se-publica-como-hechos-de-fuente-y-cada-consumidor-los-proyecta
---

# sldb.code lee SQL: tablas, columnas, vistas e índices de DDL y migraciones como hechos con anclas, con tree-sitter-sql como extra (B2, parte SQL)

## Rationale

_Explain why this task exists or the business driver behind it._

specIR ancla cada nodo extraído a su fuente con las anclas de código de SLDB (decisión IR05 D3) y sus extractores leen también SQL (DDL y migraciones de Django). La parte TS/TSX y la infraestructura por lenguaje (runtime por extensión, dispatch en scan_file, code_ref con varias extensiones) las hace la tarea task-código-readers-y-facts-de-tsx-ts-y-sql-con-anclas-sobre-tree-sitter-inbox-20261115-022446-b2, de la que esta depende. Bloquea IR09. Origen: desk/inbox/20261115-022446-suggestion-specir-anclas-de-c-digo-para-tsx-y-sql.md.

## Goal

_Describe the concrete result this task must produce._

Con el extra code instalado, sldb.code escanea archivos .sql y publica hechos de tablas, columnas, vistas e índices con la misma forma que los de Python y TS; un ancla code:<ruta>.sql::<tabla> o ::<tabla>.<columna> se registra y check_anchors la informa intact, changed, lost o reconnected.

## Scope

_State what is in scope and what is out of scope._

Entra: agregar tree-sitter-sql>=0.3 (la versión 0.3.13 está en PyPI) al extra code de pyproject.toml y regenerar uv.lock; un módulo nuevo lang_sql.py en el paquete sldb.code con la query y los readers de CREATE TABLE, CREATE VIEW y CREATE INDEX, con las columnas como hijos de su tabla. qualified_name: <tabla> y <tabla>.<columna>. Si un archivo de migraciones define dos veces la misma tabla, la segunda lleva el sufijo ~2, como ya hace Ids con nombres repetidos. docstring: un comentario -- inmediatamente anterior a la sentencia. kind: table, column, view, index, module. El dispatch por extensión agrega .sql; find_files incluye .sql solo si la gramática está. code_ref acepta .sql. Fixtures en tests/fixtures/treesitter/ con una migración de dos tablas y una vista; tests de intact/changed/lost/reconnected que se saltan sin la gramática. CHANGELOG.md. No entra: ALTER TABLE ni el estado acumulado de varias migraciones (cada archivo se lee por sí solo); dialectos más allá de lo que la gramática tree-sitter-sql reconoce; TS/TSX (tarea de la que depende).

Precisiones (JP, 2026-11-16): el dialecto objetivo es PostgreSQL, que es el que se usa. Los fixtures son DDL de Postgres: CREATE TABLE IF NOT EXISTS, tipos serial/bigserial/jsonb/timestamptz, nombres calificados por esquema (public.users), CREATE INDEX CONCURRENTLY, CREATE VIEW y CREATE MATERIALIZED VIEW (kind view). El qualified_name conserva el esquema si viene escrito (public.users, public.users.email) y si no va sin él. Lo que tree-sitter-sql no reconozca de Postgres se salta con un hecho menos, nunca con error. Las constraints de tabla (PRIMARY KEY, FOREIGN KEY, UNIQUE al final de CREATE TABLE) no son columnas. Comentario --: solo las líneas -- contiguas inmediatamente encima de la sentencia, sin línea en blanco en medio.

Precisiones (intento 3): el símbolo del ancla es el qualified_name tal cual queda en el hecho: code:<ruta>.sql::public.users si la sentencia escribe public.users, y code:<ruta>.sql::users si no lo escribe. Las columnas no tienen docstring propio. Varias líneas -- contiguas se unen con salto de línea, sin el prefijo -- ni los espacios de los extremos. El fixture cubre CREATE VIEW y CREATE MATERIALIZED VIEW, las dos con kind view. Las vistas y los índices también se anclan (code:<ruta>.sql::<vista> y ::<índice>); los tests de intact/changed/lost/reconnected se exigen sobre tabla y columna. El sufijo ~2, ~3, etc. aplica a tablas, vistas e índices repetidos en el mismo archivo, y sus columnas cuelgan del nombre con sufijo. Si tree-sitter-sql no reconoce una sentencia, se omite la sentencia completa. parse_code_ref y el dispatch por extensión ya quedan generalizados por B2: aquí solo se agrega .sql a la lista que dejó B2.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Esperar a que la tarea de TS/TSX esté cerrada y leer cómo quedó el dispatch por lenguaje (runtime y scan_file). 2) pyproject.toml y uv lock. 3) Escribir lang_sql.py siguiendo el módulo de TS. 4) Registrar .sql en el dispatch, en find_files y en code_ref. 5) Fixtures y tests. 6) Validation.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_anchors.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_fingerprints.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py
- TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast

## Done When

_Name the observable condition that makes the task complete._

Los comandos de Validation pasan con los tests nuevos sobre una migración Postgres de dos tablas (una calificada por esquema) y una vista materializada; las anclas de tabla y de columna pasan por intact, changed, lost y reconnected; CHANGELOG y commit; aviso a IR por deskops message send --desk-root a su desk.

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-sldb-code-lee-sql-tablas-columnas-vistas-e-índices-de-ddl-y-migraciones-como-hechos-con-anclas-con-t: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

