# Ejecutor deskops-e-67dedd6aa01e: C4 con pglast (extra postgres)

Tarea: `task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl`. No tiene pills atados. Sigo el contrato del intento nuevo (decisión del supervisor del 2026-11-17) y el mensaje del coordinador con sus decisiones (3).

**Resultado: LISTO, rc=0.** Todos los comandos de Validation pasan, con el extra y sin él.

## Qué se hizo, paso a paso
1. **Punto de partida.** Apliqué el parche con `git apply --exclude=CHANGELOG.md runs/subagents/20261116-exec-k2-c2/executor-diff-c4-c2.patch` y reescribí a mano la entrada del CHANGELOG. Del parche:
   - se conservan los tests, los fixtures y `sql_fact.py`, este último reescrito;
   - de `sql_names.py` se conservan `unquote` y `name_end`;
   - se borran `sql_keys.py`, `sql_key_text.py` y `sql_columns.py`, que eran la lectura textual o desde el árbol de tree-sitter. Eran archivos nuevos del parche, sin trackear;
   - `sql_readers.py` vuelve a HEAD (`git show HEAD:...`), así que no figura como modificado.
2. **Extra.** Agregué a `pyproject.toml` el extra `postgres = ["pglast>=7"]` y corrí `uv lock` una sola vez. El lock resolvió pglast 8.8 y solo agrega pglast; antes de empezar, `uv.lock` no tenía cambios ajenos en el árbol.
3. **Lectura con pglast.** Detalle por archivo más abajo.
4. **Tests.** Escribí los tests de los bordes de los tres testers y los de la lectura sin el extra.
5. **Validation.** Corrida completa (ver «Comandos»).

## Cambios por archivo y función
- `src/sldb/code/sql_pg.py` (nuevo). Importa pglast dentro de un `try`.
  - `pg_statements(src)`: parte el archivo con el scanner de Postgres (`parser.split`, solo slices) y parsea cada sentencia por separado. Cada sentencia lleva su rango de bytes, su texto, sus tokens sin comentarios y su nodo, o `None` si Postgres la rechaza.
  - Devuelve `None` sin pglast y `[]` si el scanner no puede partir el archivo.
  - `to_byte` convierte los offsets de pglast, que son caracteres, a bytes. Hay un test con no ASCII.
  - `is_table` distingue un `ALTER TABLE` de un `ALTER INDEX`.
- `src/sldb/code/sql_pg_tokens.py` (nuevo). Funciones `index_at`, `tok_text`, `written`, `paren_list` y `element_end` sobre los tokens de Postgres.
  - Un identificador entre comillas es un solo token, así que `"a)b"`, `"c,d"` y `"a""b"` no parten las listas.
  - Los nombres salen tal como están escritos: sin comillas, `""` leído como `"` y sin pasar a minúsculas. Así coinciden con los qualified names de tree-sitter.
- `src/sldb/code/sql_pg_keys.py` (nuevo).
  - `create_parts`: de un `CreateStmt` saca las columnas con `type`, `primary_key`, `unique`, `identity` y `references`, y las claves de tabla.
  - `alter_parts`: de un `AlterTableStmt` de tabla saca cada `AT_AddConstraint` de tipo PK, FK o UNIQUE, con nombre o sin él. Si Postgres rechaza el `ALTER TABLE`, devuelve `(tabla, None)`.
  - `_key`, `_refs`, `_column`, `_span`: el tipo de columna son los tokens entre el nombre y la primera constraint, sin comentarios.
- `src/sldb/code/sql_fact.py`, reescrito sobre el del parche.
  - `sql_fact` usa `ctx["name"]`.
  - `span_fact` (nuevo) arma el hecho desde un span de bytes de pglast, con signature, shape y body sobre el texto.
  - `link_references` resuelve la relación por qualified name exacto.
- `src/sldb/code/sql_names.py`: `exact_name` (nuevo) es `unquote` aplicado a `name_end`. Lo usa la lectura con el extra; sin el extra se usa `sql_readers.sql_name` de HEAD. Saqué `span_name` y `groups`, que ya no se usaban.
- `src/sldb/code/lang_sql.py`:
  - `scan_sql_file` intercala en orden de fuente los `CREATE` de tree-sitter y los `ALTER` de pglast;
  - `_object_facts` busca la sentencia de pglast que contiene el `CREATE TABLE`;
  - `_tree_sitter_table` es la lectura de HEAD más `keys_partial`;
  - `_column_fact` usa el nodo de tree-sitter cuando la columna empieza donde la de Postgres y está limpia, y si no, el span de pglast con `parse_partial`;
  - `_key_fact` y `_alter_facts` arman los hechos de las claves;
  - el docstring lista lo que entra y los límites.
- `pyproject.toml`: extra `postgres`. `uv.lock`: pglast 8.8.
- `tests/fixtures/treesitter/sql/django/0001_initial.sql`: el `UNIQUE` (`slug_pages_uniq`) va ahora antes del `CHECK` (`pages_ok`), como escribe sqlmigrate `Meta.constraints = [UniqueConstraint, CheckConstraint]`. Lo autoriza el Scope (4): «ampliar el fixture de Django existente».
- `tests/fixtures/treesitter/sql/django/blog_0001_initial.sql`: viene del parche, sin cambios.
- `tests/selfdoc/test_treesitter_symbols.py`: sección SQL reescrita.
  - Marcador `needs_pg`.
  - Fixture `no_pg`, que pone `sql_pg._pg = None`: la lectura sin el extra se prueba siempre, esté o no instalado pglast.
  - Los tests de HEAD vuelven a sus expectativas de HEAD bajo `no_pg`, más `keys_partial`. Los de claves llevan `needs_pg`.
- `tests/api/test_anchors.py`: el test del parche (ancla de constraint y de `id`, intact y changed) pasa a `needs_pg`.
- `CHANGELOG.md`: entrada C4 nueva en 0.1.13, escrita a mano.

## Decisiones (3) del coordinador, cómo quedan
- **Sin el extra se usa la lectura de HEAD.** Lo comprobé contra HEAD, con su `src` sacado por `git archive` en `/dev/shm/k2pg/head`:
  - corpus `tests/fixtures/treesitter`, más `src/`, más los 20 `.sql` de bordes de los testers, más el fixture de Django de HEAD: 5965 hechos;
  - la salida es idéntica salvo `attrs.keys_partial`, que aparece en 34 tablas.
- **`keys_partial` solo en el hecho de la tabla.** Sin el extra se pone cuando la sentencia tiene nodos ERROR. Con el extra se pone cuando pglast no parseó el `CREATE TABLE`, o un `ALTER TABLE` sobre esa tabla. Interpreté el «o» por camino:
  - con el extra y la sentencia parseada, las claves están completas aunque tree-sitter tenga `ERROR`. Por eso las tablas de Django con IDENTITY no llevan la marca;
  - si se quiere también en ese caso, se cambia una condición en `_tree_sitter_table`/`_object_facts`.
- **`references` conserva el esquema tal como viene escrito**, y la relación apunta al qualified name exacto. `REFERENCES public.t` no enlaza con la tabla `t`, y hay un test que lo fija.
- **El sufijo `~N` cuenta por tipo dentro de la tabla**, con el mismo `Ids` local. Hay un test.

## Done When
- **Validation pasa con el extra y sin él: sí.** Ver la tabla de comandos.
- **Bordes de los tres testers con el extra: todos dan las claves correctas.** Las sondas originales (`/dev/shm/k2c1t/root/mig/edge*.sql`, `shop_0001.sql`, `/dev/shm/k2c2t/v/*.sql`) están copiadas en `/dev/shm/k2pg/edges/` y su volcado está en `/dev/shm/k2pg/edges.out`. Quedaron fijadas como tests:
  - tester 1: FK sin columnas referenciadas en `ALTER`, y `"a)b"`;
  - tester c1: FK de tabla sin columnas referenciadas (`d`, `f2`), y `""` en listas, refs, nombres de constraint y tablas;
  - tester c2:
    - **`UNIQUE` y luego `CHECK` (`uniq_cat_sku` de sqlmigrate real, u1, u4)**;
    - FK con nombre como última clave, con esquema o sin él (a5, a6);
    - FK con nombre seguida de `CHECK` (a8);
    - `e_u` tras `e_fk`, que antes era un límite;
    - `"c""1" int` con tipo `int`, que antes salía `null`;
    - `EXCLUDE` que ya no se traga el `ALTER` siguiente (n.sql);
  - extra: `ALTER TABLE "p""q" ADD CONSTRAINT`, que antes era un límite, ahora da su hecho.
- **Fixture de Django:**
  - `app_author.id`, `app_book.id` y `posts.id` dan `primary_key`, `identity`, `parse_partial` y `type: bigint`;
  - cada FK de `ALTER TABLE` da `references` correctas, con relación a `app_author` y sin relación a `auth_user`;
  - `slug_pages_uniq` sale, seguido de un `CheckConstraint` sin hecho;
  - sale el `unique_together` del `ALTER`.
- **Sin el extra, la lectura de .sql no cambia respecto de HEAD salvo `keys_partial`: sí.** Lo muestra la comparación de arriba. Además, `--exact` desinstala pglast: 41 passed y 16 skipped.
- **Los hechos de .py y TS no cambian: sí.** Con el extra, los 5751 hechos no-.sql del mismo corpus son idénticos a los de HEAD.
- **CHANGELOG: sí. Commit y aviso a IR: no**, por instrucción (6) del coordinador. Quedan para el integrador.

## Comandos (rc), salida completa en `validation.log`
| Comando | rc | Resultado |
|---|---|---|
| `uv run --frozen --extra code --extra postgres --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 30 passed |
| `... --extra postgres ... pytest -q tests/api/test_anchors.py` | 0 | 23 passed |
| `... --extra postgres ... pytest -q tests/selfdoc/test_fingerprints.py` | 0 | 4 passed |
| `uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 30 passed (*) |
| `uv run --exact --frozen --extra code --extra dev ...`: comprueba pglast, luego symbols, anchors y fingerprints | 0 | pglast no instalado; 41 passed, 16 skipped |
| `... --extra dev pytest -q tests/test_clean_code_rules.py` (sin el extra) | 0 | 1198 passed |
| `... --extra dev bash tools/check.sh --fast` (sin el extra) | 0 | TODAS LAS PUERTAS PASAN |
| `... --extra postgres ... pytest -q tests/test_clean_code_rules.py` | 0 | 1198 passed |
| `... --extra postgres ... bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |
| Vecinos: `test_treesitter_agreement.py` y `tests/notations/test_component_spec_python.py` con el extra | 0 | 7 passed |

(*) `uv run` sin `--exact` no desinstala lo que sobra, así que el comando de Validation «sin el extra», tal como está escrito, corre con pglast presente. Por eso agregué la corrida con `--exact`, que sí lo quita, y el fixture `no_pg`, que prueba la lectura sin el extra en cualquier entorno. Al final, el `.venv` quedó de nuevo con el extra, porque la última corrida fue con `--extra postgres`.

`uv` funcionó y no hizo falta el fallback de uvx. No corrí la suite completa ni `stores build --check`: Validation no los nombra.

## Archivos tocados
- Modificados: `CHANGELOG.md`, `pyproject.toml`, `uv.lock`, `src/sldb/code/lang_sql.py`, `tests/api/test_anchors.py`, `tests/selfdoc/test_treesitter_symbols.py`, `tests/fixtures/treesitter/sql/django/0001_initial.sql`.
- Nuevos:
  - `src/sldb/code/sql_pg.py`, `sql_pg_tokens.py` y `sql_pg_keys.py`, que autoriza el Implementation Path (3);
  - `src/sldb/code/sql_fact.py` y `sql_names.py`, del parche;
  - `tests/fixtures/treesitter/sql/django/blog_0001_initial.sql`, del parche.
- `src/sldb/code/sql_readers.py` queda igual que en HEAD. `sql_keys.py`, `sql_key_text.py` y `sql_columns.py` del parche no quedan.
- Evidencia: `runs/subagents/20261116-exec-k2-pg/{validation.log,result-summary.md}`. Sondas en `/dev/shm/k2pg/`.
- No toqué `desk/` ni `.sldb/`. No hice git add, stash ni commit.

## Desvíos y dudas
- **Un `ALTER TABLE t ADD PRIMARY KEY (a)` sin nombre ahora da `t.pk`.** Antes no daba hecho, y el tester 1 lo listaba como «pasa». El Scope (2) habla de `ADD CONSTRAINT nombre`, pero la meta pide las claves de `ALTER TABLE ADD CONSTRAINT` sin pérdidas silenciosas, y la precisión dice que las constraints sin nombre se nombran por tipo. Si no se quiere, basta con filtrar `key["name"] is None` en `_alter_facts`. Está fijado en `test_keys_of_alter_table_unnamed_repeated_and_out_of_scope`.
- **`native_kind` de los hechos que salen de pglast.** Es `Constraint` para las claves y `ColumnDef` para una columna que tree-sitter no parsea, como la `id` IDENTITY. Antes eran `add_constraint`, `constraint`, `ERROR` o `column_definition`. Los tests se ajustaron.
- **Los nombres no pasan a minúsculas.** Postgres trata `Users` y `users` como el mismo identificador; aquí los nombres se leen como están escritos, igual que los hechos de tree-sitter. `REFERENCES Users (Id)` enlaza con `CREATE TABLE Users`, pero no con `users`. Es coherente con la decisión (3), que conserva el nombre tal como viene escrito.
- **Límites que siguen**, documentados en el docstring de `lang_sql.py` y en el CHANGELOG:
  - `CHECK` y `EXCLUDE`;
  - las otras acciones de `ALTER` (`ADD COLUMN ... PRIMARY KEY` incluido);
  - un `CREATE TABLE` que tree-sitter no ve como tal pierde sus claves con él, sin marca, porque no hay hecho de tabla que la lleve;
  - el estado entre migraciones;
  - otros dialectos.
- **La tarea está en `status: draft` en el desk.** No la toqué (no edito `desk/`).
