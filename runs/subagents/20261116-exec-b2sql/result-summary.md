# Executor deskops-e-1cc9693036d5 — B2 parte SQL

Task: `task-sldb-code-lee-sql-tablas-columnas-vistas-e-índices-de-ddl-y-migraciones-como-hechos-con-anclas-con-t`. Pills atados: ninguno. Aclaraciones del coordinador (1)–(8) aplicadas.

## Cambios
- `pyproject.toml`: extra `code` suma `tree-sitter-sql>=0.3`. `uv.lock`: `uv lock` una vez (agrega tree-sitter-sql 0.3.13; diff +18 líneas, nada más).
- `src/sldb/code/runtime.py`: `GRAMMARS[".sql"] = ("sql", "tree_sitter_sql", "language")` y docstring.
- `src/sldb/code/files.py` (`find_files`): incluye `.sql` solo si `available(".sql")`.
- `src/sldb/code/scan.py` (`scan_file`): despacha `.sql` a `scan_sql_file`.
- `src/sldb/models/code_ref.py`: `SUFFIXES` gana `.sql` y el docstring.
- Nuevos (partición de lang_sql.py por la regla de 80 líneas, como B2 con lang_ts/ts_readers/ts_fingerprints):
  - `src/sldb/code/lang_sql.py`: `scan_sql_file`, `_module_fact`, `_object_facts`, `_fact`.
  - `src/sldb/code/sql_readers.py`: `KINDS`, `creations` (sentencias `statement` sin error con create_table/create_view/create_materialized_view/create_index), `columns` (solo `column_definition`, las constraints no), `sql_doc` (líneas `--` contiguas justo encima, cada una en su propia línea, unidas con `\n`), `sql_norm`.
  - `src/sldb/code/sql_fingerprints.py`: `sql_fingerprints` (signature = sentencia o columna normalizada; shape = sin el nombre; docstring = `--`; body = tokens después del nombre).
- Fixture: `tests/fixtures/treesitter/sql/migrations/0001_initial.sql` (Postgres: `CREATE TABLE IF NOT EXISTS public.users` con bigserial/jsonb/timestamptz, `orders` con constraints de tabla, `CREATE VIEW`, `CREATE MATERIALIZED VIEW`, `CREATE INDEX CONCURRENTLY`).
- Tests: `tests/selfdoc/test_treesitter_symbols.py` (+4: kinds/nombres/constraints, doc/signature/span/imports, sufijo ~N y sentencia no reconocida sin hechos, sin gramática no se escanea .sql); `tests/api/test_anchors.py` (+3 casos: tabla y columna parametrizadas por intact→changed→reconnected→lost; vista, índice, columna y módulo se anclan; parse_code_ref acepta `.sql`). Se saltan sin la gramática (`needs_sql`).
- `CHANGELOG.md`: entrada en 0.1.13.

## Forma de los hechos
id `<módulo>.<qualified_name>`; module qualified_name = ruta sin extensión (`migrations.0001_initial`), `imports` []. table/view/index: qualified_name como se escribe (`public.users`, `orders`); column `<tabla>.<columna>`, contained-in su tabla, sin doc. Repetidos en el archivo: `Ids().take` local por archivo → `t~2`, columnas `t~2.b`, índices `i~2`. El símbolo del ancla es ese qualified_name. `recorded_with`: `treesitter-symbols/1 (tree-sitter-sql 0.3.13, sql)`, sin cambio en record_anchor.py.

## Done When
- Validation pasa con los tests nuevos sobre la migración Postgres (dos tablas, una `public.users`; vista y vista materializada; índice): ver abajo.
- Anclas de tabla (`public.users`) y de columna (`public.users.email`): intact, changed (`signature`, `body`), reconnected (`public.people` / `public.users.mail`) y lost (sin candidatos): `test_a_sql_table_and_column_anchor_are_intact_changed_reconnected_and_lost[...]`.
- CHANGELOG: hecho. **Commit: no lo hice** (el brief lo prohíbe; queda para el integrador o el coordinador). **Aviso a IR: lo manda el coordinador**, según la aclaración (8).

## Comandos (salida completa en validation.log)
| comando (`TMPDIR=/dev/shm uv run --frozen --extra code --extra dev ...`) | rc |
|---|---|
| pytest -q tests/api/test_anchors.py | 0 |
| pytest -q tests/selfdoc/test_treesitter_symbols.py | 0 |
| pytest -q tests/selfdoc/test_fingerprints.py | 0 |
| pytest -q tests/test_clean_code_rules.py | 0 |
| bash tools/check.sh --fast | 0 |
También `TMPDIR=/dev/shm uv lock` (rc 0). Ni la suite completa ni `sldb stores build --check`: Validation no los nombra y los corre el integrador.

## Archivos tocados (exactos)
CHANGELOG.md, pyproject.toml, uv.lock, src/sldb/code/runtime.py, src/sldb/code/files.py, src/sldb/code/scan.py, src/sldb/models/code_ref.py, src/sldb/code/lang_sql.py (nuevo), src/sldb/code/sql_readers.py (nuevo), src/sldb/code/sql_fingerprints.py (nuevo), tests/api/test_anchors.py, tests/selfdoc/test_treesitter_symbols.py, tests/fixtures/treesitter/sql/migrations/0001_initial.sql (nuevo), runs/subagents/20261116-exec-b2sql/{validation.log,result-summary.md}.
Fuera de la lista del contrato pero autorizados por Scope o por el coordinador: files.py y scan.py (dispatch y find_files), sql_readers.py y sql_fingerprints.py (partición de lang_sql, aclaración 1).
`desk/inbox/20261116-184421-unclear-ir04b-...md` aparece sin trackear y no es mío.

## Desvíos y dudas
1. **Bug previo en `src/sldb/api/anchors/reconnect.py::_qualified`; no lo toqué porque está fuera del alcance.** Le agrega al qualified_name el sufijo del id desde el primer `~`. Si el destino de una reconexión es un símbolo con sufijo, la ref sale mal: `t~2` da `t~2~2` y `t~2.b` da `t~2.b~2.b`. En Python ya pasaba: un método de una clase repetida da `K.f~2.f`. Verificado llamando a `_ref`. Solo afecta reconectar *hacia* un símbolo con sufijo; registrar y comprobar anclas con sufijo funciona (`symbol_of` compara por id). Lo propongo como tarea aparte: derivar la ref de `id` sin el prefijo del módulo.
2. Una sentencia con un error de parseo local no deja hechos: tree-sitter-sql 0.3.13 no reconoce `CONSTRAINT nombre UNIQUE (...)` dentro de `CREATE TABLE`, así que esa tabla entera no da ningún hecho (precisión del intento 3 y aclaración 6). Lo cubre un test.
3. La signature normaliza solo los espacios, sin el reentrecomillado de `py_norm`, porque en SQL `"x"` es un identificador.
4. Columnas: un cambio de tipo o de constraints aparece como `signature`+`body` changed. La reconexión de una columna renombrada falla (queda lost con varios candidatos) si otra columna del mismo archivo tiene exactamente la misma definición.
