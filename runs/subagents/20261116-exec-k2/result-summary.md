# Executor deskops-e-aaf14ca96f71: resultado

Tarea: `task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl` (C4 de IR). Pills: ninguno.
Resultado: **LISTO 0**. Todos los comandos de Validation dan rc=0 (salida completa en `validation.log`).

## Decisiones del coordinador aplicadas (mensaje durante la ejecución)
1. Tipo de una columna: el texto entre el nombre y la primera palabra clave (`NOT`, `NULL`, `DEFAULT`, `PRIMARY`, `GENERATED`, `REFERENCES`, `UNIQUE`, `CHECK`) o el primer nodo `ERROR`, normalizado a un espacio. Se aplica a todas las columnas (`attrs.type`), no solo a las que tienen error.
2. `attrs.constraint_type` ∈ {`primary_key`, `foreign_key`, `unique`}.
3. La relación `references` sale solo si la tabla referenciada tiene hecho en el mismo archivo, antes o después (se resuelve en una segunda pasada, `link_references`); si no, solo `attrs.references`.
4. Fixture de IR copiado a `tests/fixtures/treesitter/sql/django/blog_0001_initial.sql`: aporta una FK a una tabla de otra app (`auth_user`), que el fixture de Django de sldb no cubría, y una columna `NULL`.
5. Prioridad 1: anotado.
6. Sin commit ni avisos: no hice commit ni avisé a IR (el Done When pide "commit; aviso a IR": queda para el coordinador/integrador).

## Cambios (archivo y función)
- `src/sldb/code/lang_sql.py`: `scan_sql_file` lleva `local` (Ids de nombres del archivo) y `tables` en `ctx`, despacha `alter_table` a `_alter_facts` y termina con `link_references`; `_object_facts` emite tabla, columnas (vía `_column_fact`, que añade `column_attrs`) y claves de la tabla (`key_facts`); `_alter_facts` nuevo; `_fact` sale a `sql_fact.py`. Docstring con lo que queda fuera.
- `src/sldb/code/sql_readers.py`: `creations` incluye `ALTER TABLE` con `add_constraint` (predicado `_read`); `columns` admite definiciones con error cuyo nombre es el primer hijo y se lee limpio (`column_name`). Docstring al día.
- Nuevo `src/sldb/code/sql_columns.py`: `column_name`, `column_attrs` (`type`, `primary_key`, `unique`, `identity`, `parse_partial`).
- Nuevo `src/sldb/code/sql_keys.py`: `table_keys`, `alter_keys`, `read_key` (regex sobre el texto del nodo), `key_name_node`.
- Nuevo `src/sldb/code/sql_fact.py`: `sql_fact` (antes `_fact`), `key_facts`, `link_references`.
- `tests/selfdoc/test_treesitter_symbols.py`: tests existentes actualizados (ahora salen `id` y las claves) y 4 nuevos: `test_sql_unnamed_table_keys_and_the_keys_written_in_a_column`, `test_a_django_migration_gives_the_identity_primary_key_and_the_keys_of_alter_table`, `test_a_foreign_key_to_a_table_of_another_migration_has_references_but_no_relation`, `test_keys_of_alter_table_unnamed_repeated_and_out_of_scope`.
- `tests/api/test_anchors.py`: `test_a_sql_key_and_the_identity_id_are_anchored_and_a_changed_key_is_reported` (ancla de constraint FK y de `app_book.id`; intact y changed).
- `CHANGELOG.md`: entrada nueva al principio de 0.1.13.
- Nuevo fixture `tests/fixtures/treesitter/sql/django/blog_0001_initial.sql` (copia literal del de IR).

## Done When
- Validation pasa: sí, los 5 comandos rc=0.
- Sobre el fixture de Django sale `app_author.id` y `app_book.id` con `primary_key: true`, `identity: true`, `parse_partial: true`, `type: bigint` (test `test_a_django_migration_gives_the_identity_primary_key_and_the_keys_of_alter_table`).
- Un hecho `constraint` por la FK de ALTER TABLE: `app_book.app_book_author_id_980d3e25_fk_app_author_id`, `columns: [author_id]`, `references: {table: app_author, columns: [id]}` y relación `references` → `django.0001_initial.app_author`. También salen el `UNIQUE` de `unique_together` (ALTER) y el `CONSTRAINT "slug_pages_uniq" UNIQUE` de `Meta.constraints` (nodo ERROR de la gramática).
- Hechos de `.py` y TS sin cambios: sus tests en `test_treesitter_symbols.py` y `test_anchors.py` pasan sin tocarlos; solo cambió el camino de `.sql`.
- CHANGELOG: sí. Commit y aviso a IR: **no**, por la decisión 6 del coordinador.

## Comandos corridos (rc)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` → 0 (18 passed)
- `... pytest -q tests/api/test_anchors.py` → 0 (23 passed)
- `... pytest -q tests/selfdoc/test_fingerprints.py` → 0 (4 passed)
- `... pytest -q tests/test_clean_code_rules.py` → 0 (1196 passed)
- `... bash tools/check.sh --fast` → 0 (TODAS LAS PUERTAS PASAN; `--fast` omite afirmaciones y pruebas selfdoc)
No corrí la suite completa ni `sldb stores build --check` (no figuran; serían del integrador).

## Archivos tocados (lista exacta)
- M `CHANGELOG.md`
- M `src/sldb/code/lang_sql.py`
- M `src/sldb/code/sql_readers.py`
- M `tests/api/test_anchors.py`
- M `tests/selfdoc/test_treesitter_symbols.py`
- A `src/sldb/code/sql_columns.py`
- A `src/sldb/code/sql_fact.py`
- A `src/sldb/code/sql_keys.py`
- A `tests/fixtures/treesitter/sql/django/blog_0001_initial.sql`
- A `runs/subagents/20261116-exec-k2/validation.log`, `result-summary.md`
Los cambios en `.sldb/` (RunDoc del run) ya estaban al empezar; no son míos.

## Desvíos y dudas
- Módulos nuevos (`sql_columns.py`, `sql_keys.py`, `sql_fact.py`) fuera de la lista `files`: autorizados por el Implementation Path ("partir en módulos si pasa de 80 líneas"); `lang_sql.py` no cabía. El fixture de IR, por la decisión 4.
- Las claves se leen con una regex sobre el texto del nodo (`constraint`, `add_constraint` o `ERROR` entre las columnas), no recorriendo hijos: la gramática pierde `FOREIGN`/`PRIMARY` o el nombre en varios casos y el texto es uniforme.
- Además de comentarios y comillas simples (contrato), la detección de marcas ignora identificadores entre comillas dobles y el propio nombre de la columna (una columna `"unique"` o un `CHECK ("primary key" ...)` no marca). Más estricto que el contrato, no lo contradice.
- Extra no pedido explícitamente: `CONSTRAINT nombre UNIQUE (...)` dentro de `CREATE TABLE` (nodo ERROR en tree-sitter-sql 0.3.13) sí da hecho; el Goal pide "un hecho por cada clave".
- Límites documentados: `CONSTRAINT f FOREIGN KEY ...` dentro de `CREATE TABLE` la gramática lo parte en dos y no da hecho; `ALTER TABLE t ADD PRIMARY KEY (...)` sin nombre, `ADD COLUMN`, `CHECK`, `EXCLUDE` y el `REFERENCES` de columna no dan hecho.
- Clave de un `ALTER TABLE` sobre una tabla que no está en el archivo: cuelga del módulo (`contained-in` al módulo). El contrato dice "hijo de su tabla" sin cubrir este caso.
- Un unnamed constraint usa como "nombre" para las huellas el primer token del nodo (p. ej. `PRIMARY`), porque `sql_fingerprints` trata `name=None` como módulo.
