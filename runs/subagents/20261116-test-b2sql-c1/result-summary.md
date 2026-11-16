# Tester deskops-t-ad9f049e2cf8: B2, parte SQL, corrección 1

Task: `task-sldb-code-lee-sql-tablas-columnas-vistas-e-índices-de-ddl-y-migraciones-como-hechos-con-anclas-con-t`. Pills: ninguno. Ejecutor: deskops-e-90f36a61abe4 (corrección 1, tras la FALLA del intento 1 en `runs/subagents/20261116-test-b2sql/`).
Salida completa en `validation.log`. Sondas en `/dev/shm/b2sqlc1t/`: `proj/gen.py` (Django), `probe.py`, `anchor.py`, `dump.py`, `e/*.sql`, `head/` (`git archive HEAD`).

## Veredicto: PASA

## Validation (cada comando con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)
| comando | rc | resultado |
|---|---|---|
| pytest -q tests/api/test_anchors.py | 0 | 14 passed |
| pytest -q tests/selfdoc/test_treesitter_symbols.py | 0 | 14 passed |
| pytest -q tests/selfdoc/test_fingerprints.py | 0 | 4 passed |
| pytest -q tests/test_clean_code_rules.py | 0 | 1180 passed (también lo exige el brief) |
| bash tools/check.sh --fast | 0 | OK (también lo exige el brief) |

La suite completa y `sldb stores build --check` no figuran en Validation. No los corrí: quedan delegados al integrador.

## Done When, punto por punto
| punto | veredicto | evidencia |
|---|---|---|
| Validation pasa con tests nuevos sobre una migración Postgres de dos tablas (una con esquema) y una vista materializada | PASA | fixture `sql/migrations/0001_initial.sql` (`public.users`, `orders`, vista, vista materializada, índice CONCURRENTLY) y `sql/django/0001_initial.sql`; los 5 comandos dan rc 0 |
| Anclas de tabla y columna: intact, changed, lost, reconnected | PASA | test parametrizado del ejecutor, y mi sonda sobre DDL real de Django (abajo) |
| CHANGELOG | PASA | entrada en 0.1.13 con la corrección 1 y el límite; `check.sh --fast` rc 0 |
| Commit / aviso a IR | no aplica al tester | sigue sin commitear |

## Aclaraciones del coordinador
1. **Archivos del cambio**: el diff solo toca pyproject.toml, uv.lock, `src/sldb/code/{files,runtime,scan}.py`, `src/sldb/models/code_ref.py`, los nuevos `lang_sql.py`, `sql_readers.py` y `sql_fingerprints.py`, `tests/fixtures/treesitter/sql/`, los dos tests y CHANGELOG. **PASA.** `.sldb/*`, los RunDoc sin trackear, `desk/runtimes/` y `.herdr-coordination.md` son ajenos (conteos del store tras crear los RunDoc); no los revisé.
2. **DDL de sqlmigrate regenerado por mí**: venv propio en `/dev/shm/b2sqlc1t/dj` (Django 6.1.3), proyecto `proj/` con modelos distintos de los del ejecutor: Publisher (CharField unique, JSONField), Tag, Book (FK, `db_index`, CharField unique, PositiveIntegerField, ManyToMany, `unique_together`, `Meta.constraints` con Check y Unique, `Meta.indexes`), Review (OneToOne). `makemigrations` y luego `call_command("sqlmigrate", ...)` con la conexión parcheada (sin servidor: recorder vacío, autocommit y commit no-op, `compose_sql` con `psycopg2.adapt`). Resultado: `BEGIN;…COMMIT;`, IDENTITY en todos los `id`, constraints, FK y `unique_together` como `ALTER TABLE`, índices entre comillas. **PASA**: salen las 5 tablas (`app_publisher`, `app_tag`, `app_book`, `app_book_tags` de la M2M, `app_review`), sus 12 columnas sin `id` (límite documentado) y los 8 índices; `doc` = `Create model X`. ALTER ignorado, como dice el Scope.
3. **Desvío 1 (`has_error` frente a `parse_errors`)**: **PASA.** En la migración de Django el módulo da `has_error=False, parse_errors=True`. Anclas sobre ese archivo: `app_book` (table), `app_book.title` (column) y `app_book_publisher_id_74fff6a5` (index) dan intact → changed → lost; tabla y columna también reconnected al renombrar (`app_volume`, `app_book.headline`). Ninguna `unparseable`. Un `.py` y un `.ts` con errores reales dan `intact` → `unparseable`, igual en HEAD (PYTHONPATH a `git archive HEAD`) y en el árbol. Un `.sql` sin ningún CREATE legible da `unparseable` también.
4. **Hechos de .py y TS frente a HEAD**: **PASA.** `scan_tree` sobre `src/` (5597 hechos) y `tests/fixtures/treesitter/` (64 sin `.sql`) con el código de HEAD y con el del árbol: JSON idénticos (`cmp`).
5. **uv.lock**: **PASA.** Un solo `[[package]]` nuevo, `tree-sitter-sql 0.3.13`, más sus líneas en el extra `code` y `requires-dist`.

## Casos que el ejecutor no cubrió (sondas propias, `e/*.sql`)
| caso | resultado | |
|---|---|---|
| `"public"."users"` con IDENTITY y `CONSTRAINT k UNIQUE`, luego `public.users` | `public.users` (doc `uno\ndos`, solo `email`), `public.users~2` con `public.users~2.x` | correcto |
| `CREATE UNIQUE INDEX IF NOT EXISTS ux ON public.users` | índice `ux` | correcto |
| `CREATE TABLE (z int)` sin nombre | sin hechos | correcto |
| Dos transacciones con `CREATE VIEW "v"` y `CREATE MATERIALIZED VIEW mv` | `v` y `mv`, kind view | correcto |
| `CONSTRAINT pk PRIMARY KEY`, `FOREIGN KEY` al final | no son columnas | correcto |
| Archivo vacío y archivo solo con comentario | solo el módulo, sin error | correcto |
| Bytes no UTF-8 en el nombre de columna | la tabla sí; la columna con error se omite | aceptable |
| `CREATE INDEX ON t (b)` sin nombre | sin hecho | aceptable |
| Sin la gramática (`available('.sql')` en False) | `find_files` no lista ningún `.sql` | correcto |

Nota menor, no bloqueante: una columna con espacio (`"weird col"`) da el qualified_name `ok3.weird col`; al quitar las comillas, el `.` dentro de un identificador entre comillas también se vuelve ambiguo. Es la letra de la precisión (b).

## Alcance y clean code
Ningún cambio del ejecutor fuera de lo autorizado (aclaración 1). `test_clean_code_rules.py` 1180 passed y `check.sh --fast` rc 0: sin violaciones en los archivos tocados.

## Regresiones vecinas (un archivo por corrida; todos rc 0)
Importan los módulos cambiados: `tests/api/test_anchors.py`, `tests/notations/test_component_spec_python.py`, `tests/selfdoc/test_fingerprints.py`, `tests/selfdoc/test_treesitter_agreement.py`, `tests/selfdoc/test_treesitter_symbols.py`. Además, por anclas y `code_ref`: `tests/api/test_api_edges.py`, `test_doc_anchors.py`, `test_graph_source_parity.py`, `test_referrers.py`, `test_rules_end_to_end.py`, `test_rules_evaluation.py`, `test_tags.py`, `test_tags_scope.py`, `tests/test_literal_paragraph_anchor.py`. No hay fallas, así que tampoco hay fallas nuevas frente a HEAD.
