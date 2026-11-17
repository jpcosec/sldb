# Tester deskops-t-9676f952c667-a2: resultado (corrección 1 de C4)

Tarea: `task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl`. Pills: ninguno.
Ejecutor: deskops-e-aaf14ca96f71-a2 (`runs/subagents/20261116-exec-k2-c1/`).

**Veredicto: FALLA.** Validation pasa, Done When pasa y los dos defectos del intento 1 quedan corregidos en `ALTER TABLE`. Quedan dos bordes que dan datos erróneos sin avisar, de la misma clase que los defectos 1 y 2 (ver «Defectos nuevos»):
- (A) una FK de tabla en `CREATE TABLE` sin columnas referenciadas pierde `attrs.references`, y eso va contra el Scope (2);
- (B) las comillas dobles escapadas `""` parten los identificadores.

La salida completa está en `validation.log`, que incluye las sondas y su salida. Los scripts y datos están en `/dev/shm/k2c1t/`: `root/mig/{edge,edge2,edge3,shop_0001}.sql`, `tree.py`, `head/`, `head.json` y `work.json`. También uso `scan.py` y `dump.py` de `/dev/shm/k2t/`.

## Validation (corrido por mí)
| Comando | rc | Resultado |
|---|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | 0 | 20 passed: PASA |
| pytest -q tests/api/test_anchors.py | 0 | 23 passed: PASA |
| pytest -q tests/selfdoc/test_fingerprints.py | 0 | 4 passed: PASA |
| pytest -q tests/test_clean_code_rules.py | 0 | 1196 passed: PASA |
| bash tools/check.sh --fast | 0 | todas las puertas PASS: PASA |

Clean code: los archivos tocados tienen entre 35 y 79 líneas brutas (`lang_sql.py` 79, `sql_keys.py` 73), con 0 o 1 clase cada uno, y `test_clean_code_rules` pasa. No corrí la suite completa ni `stores build --check`, que Validation no nombra.

## Done When
- Validation pasa: **PASA**.
- La columna `id` sale con `primary_key` y `parse_partial`: **PASA**. `posts.id` del fixture de blog da `{type: bigint, primary_key, identity, parse_partial}`. En `shop_0001.sql` (sqlmigrate real) las 4 `id` dan lo mismo.
- Un hecho constraint por cada FK de ALTER con `references` correcto: **PASA**. `posts_author_id_099b8aca_fk_auth_user_id` da `references {auth_user, [id]}` y no tiene relación, porque `auth_user` no está en el archivo. En shop, las 4 FK son correctas y la relación sale hacia las tablas del archivo.
- Hechos de .py/TS idénticos a HEAD: **PASA**. Corrí `scan_tree` sobre el mismo corpus (`src/` + `tests/fixtures/treesitter` del árbol) con el código de HEAD (`git archive` nuevo) y con el de trabajo: 5737 hechos no-.sql, JSON idéntico (md5 `2c788f21…` en los dos).
- CHANGELOG: **PASA** (la entrada C4 en 0.1.13 menciona los dos bordes nuevos). Commit y aviso a IR: no hechos, por instrucción; quedan al integrador.

## (1) Sondas del tester anterior, repetidas
- `edge.sql`: **PASA**. Todo lo que pasaba sigue igual, y los dos defectos están corregidos:
  - defecto 1: `parent_self_fk` da `references {table: public.parent, columns: []}`, más la relación `references`;
  - defecto 2: `CREATE TABLE odd ("a)b" int, UNIQUE ("a)b"))` da `columns: ["a)b"]`.
- sqlmigrate de Django (`shop_0001.sql`): **PASA**, con la misma salida que en el intento 1 (`uniq_cat_sku`, los 2 `unique_together`, las 4 FK, la marca `unique` en `name`, ningún hecho por el CHECK).
- .py/TS idénticos a HEAD: **PASA** (arriba).

## (2) Bordes nuevos de la regex
- **ALTER TABLE con varias acciones: PASA.**
  - `ADD COLUMN z int, ADD CONSTRAINT c_k_uniq UNIQUE (k)` da `c_k_uniq`.
  - `ADD CONSTRAINT c_id_uniq UNIQUE (id), DROP COLUMN z` da `c_id_uniq`.
  - `ADD CONSTRAINT c_pid_fk3 FOREIGN KEY ... REFERENCES c (id) ON DELETE CASCADE, ADD CONSTRAINT c_pk PRIMARY KEY (id)` da las dos, cada una correcta.
  - Las otras acciones no dan hecho.
- **FK con ON DELETE CASCADE: PASA en ALTER, con y sin columnas referenciadas** (`... REFERENCES c ON DELETE CASCADE ON UPDATE SET NULL` da `references {c, []}`). **Falla en CREATE TABLE sin columnas referenciadas**: es el defecto A.
- **Comillas escapadas `""`: FALLA**, ver el defecto B.

## Defectos nuevos (motivo de FALLA)
**A. Una FK de tabla en `CREATE TABLE` sin columnas referenciadas no lleva `references`.** Es el defecto 1 fuera de `ALTER`.
- `CREATE TABLE d (id int, FOREIGN KEY (id) REFERENCES t);` da `d.fk {constraint_type: foreign_key, columns: [id]}`, sin `references` y sin relación.
- Pasa lo mismo con `... REFERENCES t ON DELETE CASCADE` (`f2.fk`) y con `FOREIGN KEY (id) REFERENCES c ON DELETE SET NULL` (`d.fk~2` en edge2).
- Causa: tree-sitter-sql 0.3.13 cierra el nodo `constraint` en `'FOREIGN KEY (id)'` y deja `REFERENCES t ...` en un `ERROR` hermano dentro de `column_definitions` (`tree.py`). `_key_end` (`sql_keys.py`) solo extiende el texto para el último `add_constraint` de un `ALTER`.
- El Scope (2) pide `attrs.references` en las FOREIGN KEY de tabla. El docstring afirma en general que una FK sin columnas da `references.columns: []`, y eso no se cumple aquí.
- Django no lo genera, pero es Postgres válido y el dato sale mal sin avisar.

**B. `""` (comilla doble escapada) parte el identificador.** `_NAME = r'"[^"]+"|[\w$]+'` no admite `""`.
- `CREATE TABLE t (x int, y int, UNIQUE ("a""b", x));` da `columns: ["a", "b", "x"]`; lo correcto es `['a"b', 'x']`.
- `ALTER TABLE t ADD CONSTRAINT f FOREIGN KEY (x) REFERENCES t ("a""b");` da `references.columns: ["a", "b"]`.
- `ALTER TABLE t ADD CONSTRAINT "g""h" UNIQUE (y);` no da ningún hecho, y se pierde sin aviso.
- Con `"p""q"` como nombre de tabla, la gramática ya da `p`. Eso es de `sql_readers`, anterior a la tarea, y no lo cuento. Pero las listas de columnas y los nombres de constraint los lee el regex de esta tarea.
- Es raro y fuera de Django, pero es el mismo criterio por el que el defecto 2 (`"a)b"`) dio FALLA. Arreglo local: `"(?:[^"]|"")+"` en `_NAME` y `_LIST`, y `""` → `"` en `_bare`.

**Nota, no es FALLA:** en `CREATE TABLE e (id int, CONSTRAINT e_fk FOREIGN KEY (id) REFERENCES t, CONSTRAINT e_u UNIQUE (id))`, la gramática mete las dos constraints en un solo `ERROR` y `e_u` se pierde. `e_fk` sale bien. Es un límite de la gramática del mismo tipo que el que el ejecutor ya documentó para un ALTER seguido de otro.

## Alcance de archivos: PASA
- `git diff --name-only` da CHANGELOG, `lang_sql.py`, `sql_readers.py` y los 2 tests del contrato.
- Sin trackear: `sql_columns.py`, `sql_fact.py`, `sql_keys.py` y el fixture `blog_0001_initial.sql`, todos de esta tarea según el coordinador.
- `.sldb/` (RunDoc/ReviewDoc, índices) es el registro de los runs; no lo revisé.
- No hay cambios del ejecutor en `desk/`.

## Regresiones vecinas: PASA
- Módulos de `src/` cambiados: `lang_sql` y `sql_readers`, más los 3 nuevos. Por nombre, los importa solo `test_treesitter_symbols.py`. Sumé los tests que usan el scanner: `test_anchors.py`, `test_component_spec_python.py`, `test_treesitter_agreement.py` y `test_fingerprints.py`.
- Trabajo: 20, 23, 5, 2 y 4 passed. HEAD (`git archive` en /dev/shm, venv aparte): 14, 22, 5, 2 y 4 passed. No hay fallas nuevas.
- El diff de tests borra 2 aserciones y las reemplaza por expectativas nuevas (ahora salen `id` y las claves); suma 31 aserciones. No veo nada debilitado.

## Entorno
`uv run --frozen --extra code --extra dev` funcionó. No hice git stash, add ni commit, y no edité `desk/` ni `.sldb/`.
