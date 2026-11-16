# Executor deskops-e-90f36a61abe4: B2 parte SQL, corrección 1

Task: `task-sldb-code-lee-sql-tablas-columnas-vistas-e-índices-de-ddl-y-migraciones-como-hechos-con-anclas-con-t`. Pills atados: ninguno. Se aplicaron las Precisiones (corrección 1) del Scope y el contexto del coordinador, (1) a (5).

## Punto de partida
`git apply --exclude=CHANGELOG.md runs/subagents/20261116-exec-b2sql/executor-diff-intento1.patch` aplicó limpio. Lo hice así porque el parche choca en CHANGELOG.md, como dice la corrección del coordinador al paso (1). La entrada de CHANGELOG del parche la puse a mano al principio de 0.1.13 y la actualicé (ver abajo). El resto del intento 1 sigue igual que en `runs/subagents/20261116-exec-b2sql/result-summary.md`: pyproject, uv.lock, runtime, files, scan, code_ref y sql_fingerprints, este último sin cambios.

## Cambios de esta corrección
- `src/sldb/code/sql_readers.py`
  - `creations` (a): entra en los nodos `transaction` (`BEGIN; … COMMIT;`) de forma recursiva.
  - `creations` (c): ya no descarta la sentencia que tiene `has_error`. Toma el nombre si es hijo directo del nodo CREATE, sin error y no vacío (`object_reference`; en índices, `identifier` o `literal`). Si el nombre no se lee, la sentencia no da ningún hecho.
  - `columns` (c): omite cada `column_definition` que tenga error. Las constraints y los nodos `ERROR` nunca fueron columnas.
  - `sql_name` (función nueva, b): el nombre sin comillas dobles (`"public"."users"` da `public.users`).
  - Docstring: describe el límite (IDENTITY y `CONSTRAINT nombre UNIQUE` en tree-sitter-sql 0.3.13).
- `src/sldb/code/lang_sql.py`
  - `scan_sql_file`, `_object_facts` y `_fact`: usan `sql_name` para el `local.take`, el qualified_name de las columnas y `name`.
  - `_module_fact` gana `unreadable` (ver Desvío 1). Quité el import `text`, que ya no se usaba.
  - Docstring con el límite.
- Fixture nuevo `tests/fixtures/treesitter/sql/django/0001_initial.sql` (d): es la salida real de `manage.py sqlmigrate app 0001` de Django 6.1.3 para PostgreSQL. La primera línea es un comentario que dice su origen. Los modelos son Author (CharField, JSONField, DateTimeField) y Book (FK, PositiveIntegerField con CHECK, SlugField unique, `unique_together`, `Meta.constraints` con Check y Unique, `Meta.indexes`). El migration está en un venv de `/dev/shm/b2sqlc1`. No había servidor Postgres, así que generé el SQL con `sqlmigrate` llamado por `call_command`, con la conexión parcheada (`/dev/shm/b2sqlc1/proj/sqlmigrate_offline.py`: `pg_version` 16, sin tabla de migraciones aplicadas, autocommit y commit no-op). El SQL sale del schema editor de Django igual que con un servidor.
- `tests/selfdoc/test_treesitter_symbols.py`
  - El fixture `sql_facts` filtra `path` que empiece por `migrations/`, para que el archivo de Django no altere el test anterior.
  - `test_sql_repeated_objects_take_a_suffix_and_a_statement_with_errors_keeps_what_reads` reemplaza al test de "sentencia no reconocida sin hechos". Cubre: `"t"` repetido da `t~2`; `"i"` da `i~2`; una tabla con IDENTITY y `CONSTRAINT k UNIQUE` da la tabla y solo su columna limpia; `CREATE TABLE (z int)` sin nombre no da nada; la semántica de `has_error` y `parse_errors`.
  - Test nuevo `test_a_django_sqlmigrate_migration_gives_its_tables_columns_and_indexes`: exige el conjunto exacto de tablas, columnas e índices de la migración de Django (12 hechos), además del doc `Create model Book`, la contención y la signature de un índice entre comillas.
- `tests/api/test_anchors.py`: test nuevo `test_anchors_on_a_django_sqlmigrate_migration_use_the_unquoted_names`. Las anclas `app_book` (table), `app_book.title` (column) y `app_book_author_id_980d3e25` (index) se registran, y la de columna se informa `intact`. Agregué `import shutil`.
- `CHANGELOG.md`: la entrada SQL en 0.1.13, con la corrección 1, el límite, `parse_errors` y el fixture de Django.

## Hechos de la migración de Django (sonda)
`app_author` con `name`, `profile` y `created_at`; `app_book` con `title`, `pages`, `slug` y `author_id`; los índices `app_book_slug_780ddf03_like`, `app_book_author_id_980d3e25` y `app_book_title_idx`. Las columnas `id` (IDENTITY) se omiten; ese es el límite documentado. `ALTER TABLE` se ignora por Scope.

## Desvíos y dudas
1. **`has_error` del módulo SQL.** `check_anchors` (fuera de alcance) da `UNPARSEABLE` a cualquier ancla de un archivo cuyo hecho de módulo tenga `attrs.has_error`. Toda migración de Django tiene errores (IDENTITY, `DEFERRABLE INITIALLY DEFERRED`), así que con la lectura tolerante sus anclas habrían quedado siempre `unparseable`. Lo detectó el test nuevo de anclas. Lo resolví sin salir de `lang_sql.py`: `has_error` vale True solo si el árbol tiene errores y ningún CREATE se lee, y `attrs.parse_errors` guarda el `has_error` crudo. Está cubierto por test y documentado en la docstring y el CHANGELOG. Si el coordinador prefiere otra regla (por ejemplo, que nunca sea unparseable), es un cambio de una línea.
2. Al quitar las comillas, `"Users"` y `users` dan el mismo nombre, aunque en Postgres son identificadores distintos (sin comillas se pasa a minúsculas). Es lo que pide la precisión (b). Un identificador con `""` escapado pierde también esas comillas.
3. `CREATE FOO TABLE x (...)` y otras sentencias con un error antes del nombre ahora dan `x`, porque el nombre se lee. Es consecuencia directa de (c).
4. El bug de `reconnect.py::_qualified` sigue fuera de alcance (coordinador, punto 4).
5. **Done When: el commit y el aviso a IR no los hice**, por el brief y el punto (5) del coordinador.

## Done When
- Validation pasa con los tests nuevos sobre una migración Postgres de dos tablas (`public.users` calificada por esquema, y `orders`), una vista y una vista materializada, y también sobre la migración real de `sqlmigrate`.
- Las anclas de tabla y de columna pasan por intact, changed, reconnected y lost: `test_a_sql_table_and_column_anchor_are_intact_changed_reconnected_and_lost[...]` (del intento 1, sigue verde).
- CHANGELOG: hecho. Commit y aviso: no (ver Desvío 5).

## Comandos (salida completa en validation.log)
Todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`:

| comando | rc | resultado |
|---|---|---|
| pytest -q tests/api/test_anchors.py | 0 | 14 passed |
| pytest -q tests/selfdoc/test_treesitter_symbols.py | 0 | 14 passed |
| pytest -q tests/selfdoc/test_fingerprints.py | 0 | 4 passed |
| pytest -q tests/test_clean_code_rules.py | 0 | 1180 passed |
| bash tools/check.sh --fast | 0 | |
| (vecino, extra) pytest -q tests/selfdoc/test_treesitter_agreement.py | 0 | 2 passed |

No corrí la suite completa ni `sldb stores build --check`: Validation no los nombra y los corre el integrador. No usé `uv lock` en esta corrección: uv.lock viene del parche.

## Archivos tocados (exactos)
- Del parche del intento 1, reaplicado: `pyproject.toml`, `uv.lock`, `src/sldb/code/runtime.py`, `src/sldb/code/files.py`, `src/sldb/code/scan.py`, `src/sldb/models/code_ref.py` y `src/sldb/code/sql_fingerprints.py` (nuevo).
- Del parche y modificados en esta corrección: `src/sldb/code/lang_sql.py` (nuevo), `src/sldb/code/sql_readers.py` (nuevo), `tests/api/test_anchors.py`, `tests/selfdoc/test_treesitter_symbols.py` y `tests/fixtures/treesitter/sql/migrations/0001_initial.sql` (nuevo, sin cambios en esta corrección).
- Nuevo en esta corrección: `tests/fixtures/treesitter/sql/django/0001_initial.sql`.
- A mano: `CHANGELOG.md`.
- Evidencia: `runs/subagents/20261116-exec-b2sql-c1/{validation.log,result-summary.md}`.

Los cambios en `.sldb/`, `desk/runtimes/` y `.herdr-coordination.md` no son míos.
