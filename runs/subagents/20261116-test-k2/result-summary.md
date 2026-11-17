# Tester deskops-t-9676f952c667: resultado

Tarea: `task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl` (C4 de IR). Pills: ninguno.
Ejecutor: deskops-e-aaf14ca96f71 (`runs/subagents/20261116-exec-k2/`).

**Veredicto: FALLA.** Validation y Done When pasan (el camino de Django es correcto, también sobre DDL real recién generado). Fallan dos bordes de Postgres válido, uno de ellos contra el Scope (2), porque dan datos erróneos sin avisar (ver «Defectos»).

Salida completa en `validation.log`. Scripts y datos en `/dev/shm/k2t/` (`sqlm.py`, `scan.py`, `dbg.py`, `dump.py`, `shop_0001.sql`, `root/mig/edge.sql`).

## Validation (corrido por mí)
| Comando | rc | Resultado |
|---|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | 0 | 18 passed — PASA |
| pytest -q tests/api/test_anchors.py | 0 | 23 passed — PASA |
| pytest -q tests/selfdoc/test_fingerprints.py | 0 | 4 passed — PASA |
| pytest -q tests/test_clean_code_rules.py | 0 | 1196 passed — PASA |
| bash tools/check.sh --fast | 0 | todas las puertas PASS (`--fast` omite afirmaciones y selfdoc) — PASA |

Clean code: archivos tocados entre 35 y 77 líneas; 1 clase por archivo o ninguna; la regla de líneas por función pasa (test_clean_code_rules). No hay suite completa ni `stores build --check` (Validation no los nombra).

## Done When, punto por punto
- Validation pasa: **PASA** (tabla de arriba).
- Columna `id` con `primary_key` true y `parse_partial` true en el fixture de Django: **PASA**. `app_author.id` y `app_book.id` dan `{"type":"bigint","primary_key":true,"identity":true,"parse_partial":true}`.
- Un hecho constraint por cada FK de ALTER TABLE con references correcto: **PASA**. `app_book.app_book_author_id_980d3e25_fk_app_author_id`: `columns:[author_id]`, `references:{table:app_author, columns:[id]}`, relación `references` → `…0001_initial.app_author`. El fixture de blog (FK a `auth_user`, que no está en el archivo) tiene `attrs.references` y no tiene relación, como pide el contrato.
- Hechos de .py y TS sin cambios: **PASA**. Corrí `scan_tree` con el código de HEAD (`git archive`) y con el árbol de trabajo sobre el mismo corpus (`src/` + `tests/fixtures/treesitter`): 5736 hechos que no son .sql (.py/.js/.jsx/.ts/.tsx), JSON byte a byte idéntico (md5 `53e7661d…`).
- CHANGELOG: **PASA** (entrada nueva en 0.1.13). Commit y aviso a IR: **no hechos**, por la decisión 6 del coordinador; quedan para el integrador.

## Aclaraciones del coordinador
1. Los módulos nuevos `sql_columns.py`, `sql_fact.py`, `sql_keys.py` y el fixture `blog_0001_initial.sql` se cuentan como parte del cambio y fueron revisados.
2. **DDL real de sqlmigrate**: Django 6.1.3 + psycopg en un venv de /dev/shm. App `shop` con FK, FK nullable a `AUTH_USER_MODEL`, `unique_together`, `UniqueConstraint`, `CheckConstraint`, `ManyToManyField` y `unique=True`. sqlmigrate necesita una conexión solo para el historial de migraciones y la versión del servidor; las parcheé (`sqlm.py`), y el SQL lo genera Django sin cambios. Resultado: **PASA**.
   - `id` de las 4 tablas (incluida la tabla M2M `shop_product_tags`): primary_key, identity, parse_partial y type bigint.
   - `name ... UNIQUE` sale como marca `unique` en la columna, sin hecho propio.
   - `uniq_cat_sku` (Meta.constraints) da `constraint_type: unique`. `CHECK price_pos` no da hecho (fuera de scope, documentado).
   - Los 2 `unique_together` de ALTER (incluido el de M2M) dan `unique`.
   - Las 4 FK de ALTER dan `foreign_key` con `references` correcto y `DEFERRABLE INITIALLY DEFERRED` no estorba. La relación `references` aparece hacia `shop_category`, `shop_product` y `shop_tag`, y no hacia `auth_user`.
   - Cada constraint queda `contained-in` en su tabla.
3. **Bordes de la regex** (`edge.sql`):
   - **Pasan**:
     - nombres entre comillas con espacios y no ASCII (`"My Schema"."Child Table"`, `"child→parent fk"`, `"parent id"`);
     - esquemas (`public.parent`; la relación `references` resuelve hacia `public.parent`);
     - `ALTER TABLE ONLY` y `ALTER TABLE IF EXISTS`;
     - `ON DELETE CASCADE DEFERRABLE INITIALLY DEFERRED`;
     - minúsculas;
     - dos `ADD CONSTRAINT` en un mismo ALTER;
     - `PRIMARY KEY`/`UNIQUE` de tabla sin nombre (`pk`, `unique`, `unique~2`);
     - `ADD COLUMN`, `ADD PRIMARY KEY` sin nombre y `ADD CONSTRAINT … CHECK`, que no dan hecho;
     - un ALTER sobre una tabla ausente, que cuelga del módulo;
     - `primary key unique` dentro de un comentario `--` o de un literal `'…'`, y columnas llamadas `"unique"` o `"primary key"`, que no se marcan.
   - **Fallan**: ver «Defectos».
4. Hechos de .py/TS idénticos a HEAD: **PASA** (ver arriba).

## Defectos (motivo de FALLA)
1. **FK sin lista de columnas referenciadas pierde `attrs.references`.** Entrada: `ALTER TABLE public.parent ADD CONSTRAINT parent_self_fk FOREIGN KEY (code) REFERENCES public.parent;` (Postgres válido: referencia la PK). Sale `{"constraint_type":"foreign_key","columns":["code"]}`, sin `references` y sin relación. La causa es que en tree-sitter-sql 0.3.13 el nodo `add_constraint` termina antes de `REFERENCES t` cuando no lleva `(cols)`: su texto es `'ADD CONSTRAINT parent_self_fk FOREIGN KEY (code)'` (`dbg.py`). Va contra el Scope (2) («en las foráneas, attrs.references {table, columns}») y no está documentado en el docstring de `lang_sql.py` ni en el de `sql_keys.py`. Lo esperado es `references: {table: public.parent, columns: []}` leyendo el texto del statement, o al menos dejar el límite documentado.
2. **Un identificador entre comillas con `)` corta la lista de columnas.** `CREATE TABLE odd ("a)b" int, UNIQUE ("a)b"));` da `columns: ["a"]`. La causa es `(?P<cols>[^)]*)` en `_KEY` (`sql_keys.py`), que no respeta las comillas dobles. Es raro, pero devuelve un dato incorrecto sin avisar.

Los dos son bordes fuera de lo que genera Django; el arreglo es local a `sql_keys.py`, o documentar el límite (1).

## Alcance de archivos
`git status`: M en `CHANGELOG.md`, `lang_sql.py`, `sql_readers.py` y los 2 tests del contrato; nuevos `sql_columns.py`, `sql_fact.py`, `sql_keys.py` y el fixture (aclaración 1). Los cambios en `.sldb/` (RunDoc de los runs, `store_index.yaml`, `store.yaml`) son el registro de los runs y no del ejecutor; no los revisé. No vi cambios de `desk/`. Los cambios ajenos que lista el brief (`apply_batch.py`, `lock.py`, `uv.lock`) ya no aparecen en el árbol. **PASA.**

## Regresiones vecinas
Módulos cambiados en src: `lang_sql`, `sql_readers` (+ los 3 nuevos). En tests/, solo `test_treesitter_symbols.py` los importa por nombre. Sumé los que usan el scanner (`scan_tree`/`scan_file`): `test_anchors.py`, `test_component_spec_python.py`, `test_treesitter_agreement.py`, y `test_fingerprints.py`. Los corrí archivo por archivo en el árbol de trabajo y en HEAD (`git archive` en /dev/shm, venv aparte):
- HEAD: symbols 14, anchors 22, fingerprints 4, component_spec_python 5 y agreement 2, todos pasan.
- Trabajo: 18, 23, 4, 5 y 2, todos pasan.
- Ninguna falla nueva. En el test diff, las líneas borradas son expectativas reemplazadas por las nuevas (ahora salen `id` y las claves); no hay aserciones debilitadas. **PASA.**

## Entorno
`uv run --frozen --extra code --extra dev` funcionó; no hizo falta el fallback de uvx. No hice git stash/add/commit ni editados en desk/ o .sldb/.
