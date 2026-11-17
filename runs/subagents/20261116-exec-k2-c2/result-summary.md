# Ejecutor deskops-e-764590554721: corrección 2 de C4 (la última)

Parto del diff de los intentos 1 y c1 (sin commitear en el árbol, incluidos `sql_columns.py`, `sql_fact.py`, `sql_keys.py` y el fixture `blog_0001_initial.sql`). Corrijo los defectos A y B del tester c1 y las precisiones C y D de la corrección 2. Pills: ninguno.

## Cambios (archivo y función)
- `src/sldb/code/sql_names.py` (nuevo, lo autoriza el Scope: «partir en módulos si pasa de 80 líneas»):
  - `unquote`: quita las comillas y lee `""` como `"`; las partes se unen por puntos.
  - `name_end`: un nodo de nombre (tabla, columna, tabla referenciada) sigue sobre los trozos entre comillas que tree-sitter-sql 0.3.13 separa de él (`"a""b"` llega como `"a"` + `ERROR "b"`).
  - `span_name`: el nombre escrito entre el primer y el último nodo de un tramo.
  - `groups`: los nombres de una lista entre paréntesis del árbol, partida en los tokens `,`.
- `src/sldb/code/sql_key_text.py` (nuevo): la lectura textual, que ahora se aplica **solo a nodos `ERROR`**. Contiene:
  - `text_key`: la clave entera dentro de un `ERROR`, por ejemplo `CONSTRAINT "x" UNIQUE (...)` de Django.
  - `text_refs`: el `REFERENCES tabla [(cols)]` que la gramática deja en un `ERROR`.
  - `tail_name`: un `CONSTRAINT nombre` al final de un `ERROR`, que nombra la clave siguiente.
  - Los identificadores admiten `""`, `)` y `,` entre comillas.
- `src/sldb/code/sql_keys.py` (reescrito): lee las claves del árbol.
  - `read_key` / `_tree_key`: el tipo sale de `keyword_primary|foreign|unique`, las columnas de `ordered_columns` (con `groups`) y el nombre de los nodos entre `CONSTRAINT` y la clave (`_tree_name`), o del `ERROR` previo si la gramática partió la clave.
  - `references(owner, src)`: el `REFERENCES` de una constraint o de una columna. Lo lee del árbol (`object_reference` + `(...)`) o, si la gramática no lo dio, del `ERROR` que sigue (`_after`).
  - `_after` sube por `constraints`, `constraint`, `add_constraint`, `alter_table` y `statement` mientras el nodo es el último. Así arregla **A**: el `ERROR 'REFERENCES t'` queda como hermano de `constraints` cuando la FK es la última clave de `CREATE TABLE`.
- `src/sldb/code/sql_columns.py`, `column_attrs`:
  - el nombre termina en `name_end`;
  - un `ERROR` justo después del nombre no corta el tipo (`"i""d" int` tiene tipo `int`);
  - **C**: `attrs.references` desde `references(col)`;
  - `_NOISE` admite `""`.
- `src/sldb/code/sql_readers.py`, `sql_name`: usa `unquote` + `name_end`. Así arregla **B** en los nombres de tabla (`"p""q"` es `p"q`). Se actualizó el docstring.
- `src/sldb/code/sql_fact.py`, `link_references`: la relación `references` también sale desde una columna con `REFERENCES` propio, si la tabla referenciada está en el archivo. Se actualizó el docstring.
- `src/sldb/code/lang_sql.py`: el docstring se reescribe con lo que entra y los límites.
- **D**: el sufijo ya se contaba por tipo dentro de la tabla, porque `Ids.take("<tabla>.fk")` cuenta por qualified name. Ahora queda fijado con un test.
- `tests/selfdoc/test_treesitter_symbols.py`:
  - cuatro tests nuevos, uno por punto:
    - A: `test_a_table_foreign_key_without_referenced_columns_has_references`;
    - B: `test_escaped_double_quotes_in_table_constraint_and_column_names`;
    - C: `test_a_references_written_in_a_column_marks_the_column_and_gives_no_key`;
    - D: `test_unnamed_keys_count_their_suffix_per_type_within_their_table`;
  - en `test_sql_unnamed_table_keys_and_the_keys_written_in_a_column`, la aserción «a REFERENCES in a column is no key and no mark» pasa a pedir `orders.user_id.attrs.references == {public.users, [id]}` sin hecho constraint, como pide C. El resto de esa aserción se mantiene.
- `CHANGELOG.md`: en la entrada C4 se reescriben la lectura desde el árbol, A–D, los límites, los módulos nuevos y los tests.

Los bordes de `/dev/shm/k2c1t/root/mig/edge*.sql` dan:
- `d.fk` y `f2.fk` con `references {t, []}`;
- `"a""b"` como `a"b` en las listas, en el `UNIQUE` y en las refs;
- `"g""h"` con su hecho;
- el nombre de tabla `p"q`;
- `CONSTRAINT "p""k" PRIMARY KEY` con el nombre `p"k`.

Además, `CREATE TABLE x (..., CONSTRAINT "k1" UNIQUE (id), CONSTRAINT k2 FOREIGN KEY ...)` ahora da `k2` con nombre; antes salía como `fk`. La migración real de sqlmigrate (`/dev/shm/k2t/shop_0001.sql`) da las mismas claves y referencias que en c1. Sondas en `/dev/shm/k2c2/` (`scan.py`, `dump.py`, `a–e.sql`).

## Done When
- Los comandos de Validation pasan, todos con rc=0:
  - symbols: 24 passed
  - anchors: 23
  - fingerprints: 4
  - clean_code_rules: 1198
  - check.sh --fast: rc=0
- Fixture de Django: `app_book.id` y `posts.id` dan `primary_key`, `identity` y `parse_partial`. Cada FK de `ALTER TABLE` da `references` a la tabla y columnas correctas. Lo cubren los tests existentes, que siguen pasando sin cambios.
- Hechos de .py/TS: no se tocó su código; solo cambian módulos `sql_*` que usa `lang_sql`. Los tests de py y TS en symbols y anchors pasan. Vecinos: `test_treesitter_agreement.py` y `test_component_spec_python.py` pasan (salida en `validation.log`).
- CHANGELOG: actualizado. **Commit y aviso a IR: no se hacen**, por instrucción expresa de esta corrección. Quedan para el integrador.

## Comandos (rc)
Todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev …`:
1. `pytest -q tests/selfdoc/test_treesitter_symbols.py`: 0
2. `pytest -q tests/api/test_anchors.py`: 0
3. `pytest -q tests/selfdoc/test_fingerprints.py`: 0
4. `pytest -q tests/test_clean_code_rules.py`: 0
5. `bash tools/check.sh --fast`: 0
6. Vecinos: `test_treesitter_agreement.py` y `test_component_spec_python.py`: 0

`uv` funcionó y no hizo falta el fallback. No corrí la suite completa ni `stores build --check`; Validation no los nombra.

## Archivos tocados en esta corrección
- src/sldb/code/sql_names.py (nuevo)
- src/sldb/code/sql_key_text.py (nuevo)
- src/sldb/code/sql_keys.py
- src/sldb/code/sql_columns.py
- src/sldb/code/sql_readers.py
- src/sldb/code/sql_fact.py
- src/sldb/code/lang_sql.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
- runs/subagents/20261116-exec-k2-c2/{validation.log,result-summary.md}

No toqué `desk/`, `.sldb/`, `tests/api/test_anchors.py` ni el fixture. No hice git add, stash ni commit.

## Desvíos y dudas
- **Relación `references` desde columnas**: C pide `attrs.references` en la columna. Además agregué la relación `references` cuando la tabla referenciada está en el archivo, por coherencia con las constraints. Si no se quiere, basta con quitar `"column"` en `link_references`.
- **Límite nuevo de la gramática, documentado y sin arreglo**: `ALTER TABLE "p""q" ADD CONSTRAINT ...` no da hecho. Con `""` en el nombre de la tabla, tree-sitter-sql 0.3.13 lee el statement como `ADD COLUMN` y deja la constraint en un `ERROR` de nivel superior. El test B usa un `ALTER` sobre una tabla sin `""` que referencia `"p""q"`.
- **Siguen como límites documentados**:
  - `CHECK` y `EXCLUDE`;
  - las otras acciones de `ALTER`;
  - una clave enterrada en el `ERROR` de otra: en `e`, `e_u` se pierde y `e_fk` sale bien;
  - una FK sin columnas referenciadas que no es la última acción de un `ALTER` y queda en un `ERROR` de la gramática.
- **Lectura en `name_end`**: después de un trozo entre comillas que la gramática cortó, continúa con un regex sobre los bytes contiguos (`"..."` o `.nombre`). Solo actúa cuando el nodo termina en `"` y el byte siguiente sigue el identificador, es decir, en el token que la gramática separó (casi siempre un `ERROR`).
