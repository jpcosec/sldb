# Ejecutor deskops-e-aaf14ca96f71-a2: corrección 1 de C4

Parte del diff del intento 1 (sin commitear, en el árbol) y corrige los dos defectos del tester (`runs/subagents/20261116-test-k2/result-summary.md`, «Defectos»).

## Cambios
- `src/sldb/code/sql_keys.py`
  - Defecto 1: `read_key` toma el texto desde el nodo hasta `_key_end(node)` (función nueva). Para el último `add_constraint` de un `ALTER TABLE`, el texto sigue por los nodos `ERROR` hermanos del `statement` hasta su `;`. Con eso, el `REFERENCES public.parent` que tree-sitter-sql 0.3.13 deja fuera del nodo da `references: {table: public.parent, columns: []}`, y la relación `references` sale si la tabla está en el archivo.
  - Defecto 2: las listas `(cols)` de `_KEY` usan `_LIST = (?:"[^"]*"|[^)"])*` en vez de `[^)]*`, y `_cols` tokeniza con `re.findall(_NAME, ...)`, que respeta las comillas dobles. `UNIQUE ("a)b")` da `['a)b']`, y `"c,d"` no se parte.
  - En el docstring: las comillas, el texto extendido tras `ERROR` y que `columns: []` es la PK de la tabla referenciada. Se quita el import de `text`, que ya no se usa.
- `src/sldb/code/lang_sql.py`: el docstring documenta `attrs.references.columns: []` = clave primaria de la tabla referenciada.
- `tests/selfdoc/test_treesitter_symbols.py`: dos tests nuevos:
  - `test_a_foreign_key_without_referenced_columns_references_the_primary_key`
  - `test_key_columns_respect_double_quotes` (con `)` y `,` entre comillas, en `UNIQUE` y en las dos listas de una FK)
- `CHANGELOG.md`: la entrada de C4 suma los dos bordes y los tests.

## Done When
- Los comandos de Validation pasan, todos con rc=0 (ver `validation.log`): symbols 20 passed, anchors 23, fingerprints 4, clean_code_rules 1196, check.sh --fast rc=0.
- Fixture de Django: la columna `id` y las FK de `ALTER TABLE` siguen igual (los tests del intento 1 pasan sin cambios).
- Hechos de .py y TS: no se tocó su código. Los tests de py y TS en symbols y anchors pasan.
- Commit y aviso a IR: no se hacen, por instrucción expresa de esta corrección («No hagas commit ni mandes avisos»).

## Comandos (rc)
1. `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py`: 0
2. `... pytest -q tests/api/test_anchors.py`: 0
3. `... pytest -q tests/selfdoc/test_fingerprints.py`: 0
4. `... pytest -q tests/test_clean_code_rules.py`: 0
5. `... bash tools/check.sh --fast`: 0

`uv` funcionó y no hizo falta el fallback. No corrí la suite completa ni `sldb stores build --check`.

## Archivos tocados en esta corrección
- src/sldb/code/sql_keys.py
- src/sldb/code/lang_sql.py
- tests/selfdoc/test_treesitter_symbols.py
- CHANGELOG.md
- runs/subagents/20261116-exec-k2-c1/{validation.log,result-summary.md}

Siguen en el árbol, del intento 1: sql_readers.py, sql_columns.py, sql_fact.py, tests/api/test_anchors.py y el fixture blog_0001_initial.sql. No toqué desk/ ni .sldb/.

## Desvíos y dudas
- Límite de la gramática, anterior a esta corrección y fuera de alcance: si un `ALTER TABLE ... REFERENCES q DEFERRABLE INITIALLY DEFERRED;` sin columnas va seguido de otro `ALTER TABLE`, la recuperación de errores de tree-sitter-sql 0.3.13 mete el segundo statement en un `ERROR` y su clave se pierde. La primera FK sale bien (`references {q, []}`). Django siempre escribe las columnas referenciadas, así que el fixture no se ve afectado. Repro en `/dev/shm/k2c1/r/e.sql`.
