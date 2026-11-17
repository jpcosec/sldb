# Ejecutor deskops-e-67dedd6aa01e-a2: corrección 1 de C4 con pglast (extra postgres)

Tarea: `task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl`. No tiene pills atados.

Parto del diff del intento anterior, que está en el árbol (`runs/subagents/20261116-exec-k2-pg/`). Corrijo el único defecto que encontró el tester (`runs/subagents/20261116-test-k2-pg/result-summary.md`, sección «Defecto»), siguiendo el mensaje del coordinador.

**Resultado: LISTO, rc=0.**

## El defecto y el arreglo elegido
**Defecto.** `sql_pg.pg_statements` decodificaba con `utf-8`/`replace`, y `to_byte`/`_statement` volvían a bytes con `.encode()`. Cada byte inválido (por ejemplo, de un comentario en Latin-1) pasaba a U+FFFD, que ocupa 3 bytes. Así, cada byte inválido corría los offsets 2 bytes, y una tabla recibía las columnas y las claves de la anterior.

**Arreglo elegido: la primera opción del coordinador, con ida y vuelta exacta.** Todo el cambio está en `src/sldb/code/sql_pg.py`:
- `pg_statements` decodifica el archivo con `utf-8`/`surrogateescape`, el texto `raw`, en el que cada byte inválido es un solo carácter.
- pglast no acepta surrogates (lo comprobé: `UnicodeEncodeError: surrogates not allowed`). Por eso Postgres parsea una copia en la que cada surrogate es un U+FFFD (`_ESCAPED`). Las dos versiones tienen los mismos caracteres en las mismas posiciones, así que los offsets de pglast valen en las dos.
- `_statement` guarda `raw` además de `text`. `to_byte` y el rango de la sentencia cuentan los bytes sobre `raw` con `surrogateescape` (`_nbytes`), que es la cuenta exacta de bytes del archivo.
- Los nombres siguen saliendo de `text`: un byte inválido se lee como U+FFFD, igual que en la lectura de tree-sitter (`decode("utf-8", "replace")`).
- Documentado en el docstring de `sql_pg.py` y en el CHANGELOG.

**Comprobación sobre las sondas del tester** (`/dev/shm/k2pgt/l1/{shift,latin1,shift_utf8}.sql`):
- `shift.sql`, en Latin-1:
  - la tabla `b` da `b.k` y `b.b_fk` con `references {a,[id]}` y su relación;
  - `a` da `a.id` (con `primary_key`), `a.x` y `a.a_u`;
  - ninguna tabla lleva `keys_partial`.
- En los tres archivos, con el extra, ninguna signature de columna o de clave difiere de la lectura de tree-sitter (`sql_pg._pg = None`), y no se pierde ningún id.
- La única columna con `parse_partial` es la `id` IDENTITY, como corresponde. Desaparecen las columnas que antes pasaban a `parse_partial` por error.

## Cambios por archivo y función (en esta corrección)
- `src/sldb/code/sql_pg.py`:
  - en `pg_statements`, la decodificación con `surrogateescape` y la sustitución por U+FFFD;
  - en `to_byte`, el conteo sobre `raw`;
  - `_nbytes`, nuevo;
  - en `_statement`, la firma pasa a `(raw, text, start, stop)` y se agrega el campo `raw`;
  - el docstring, con un párrafo sobre los archivos que no son UTF-8.
- `src/sldb/code/lang_sql.py`: solo el docstring. Agrega el límite `ADD CONSTRAINT u UNIQUE USING INDEX idx`, que da `columns: []` (lo había sugerido anotar el tester), y una línea sobre los archivos que no son UTF-8.
- `tests/selfdoc/test_treesitter_symbols.py`: test nuevo parametrizado `test_a_non_ascii_comment_in_latin_1_or_utf_8_does_not_shift_the_keys_of_the_next_table[latin-1|utf-8]`, con la constante `ENCODED`. Usa el mismo DDL del tester (un comentario con «año» ×20 delante de dos tablas con claves) codificado en Latin-1 y en UTF-8, y comprueba:
  - las claves;
  - los ids de `b`;
  - las signatures;
  - la relación;
  - que no aparezca `keys_partial`.

  El test de no ASCII en UTF-8 que ya existía (`test_names_keep_their_spelling_and_byte_spans_survive_non_ascii`) sigue pasando.
- `CHANGELOG.md`, dentro de la entrada C4:
  - un párrafo sobre los archivos que no son UTF-8;
  - una nota sobre `UNIQUE USING INDEX`;
  - el test nuevo en la lista de tests.

## Done When
- **Validation pasa, con el extra y sin él: sí.** Ver la tabla de comandos.
- **Bordes de los tres testers con el extra: siguen pasando.** Sus tests están en el mismo archivo, que pasa entero (32 passed).
- **Fixture de Django: sin cambios respecto del intento anterior**, que el tester dio por bueno. Sus tests pasan.
- **Sin el extra, igual que HEAD salvo `keys_partial`.** El cambio solo toca `sql_pg.py`, que no corre sin el extra (`pg_statements` devuelve `None` antes de decodificar). La corrida con `--exact` sin pglast da 41 passed y 18 skipped.
- **Los hechos de .py y TS no cambian.** El cambio no toca nada fuera de la lectura de `.sql` con el extra.
- **CHANGELOG: sí. Commit y aviso a IR: no**, por instrucción del coordinador.

## Comandos (rc), salida completa en `validation.log`
| Comando | rc | Resultado |
|---|---|---|
| `uv run --frozen --extra code --extra postgres --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 32 passed |
| `... --extra postgres ... pytest -q tests/api/test_anchors.py` | 0 | 23 passed |
| `... --extra postgres ... pytest -q tests/selfdoc/test_fingerprints.py` | 0 | 4 passed |
| `uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 32 passed |
| `uv run --exact --frozen --extra code --extra dev`: `find_spec('pglast')`, luego symbols, anchors y fingerprints | 0 | pglast None; 41 passed, 18 skipped |
| `... --extra dev pytest -q tests/test_clean_code_rules.py` (sin el extra) | 0 | 1198 passed |
| `... --extra dev bash tools/check.sh --fast` (sin el extra) | 0 | TODAS LAS PUERTAS PASAN |
| `... --extra postgres ... pytest -q tests/test_clean_code_rules.py` | 0 | 1198 passed |
| `... --extra postgres ... bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |
| Vecinos con el extra: `test_treesitter_agreement.py` y `tests/notations/test_component_spec_python.py` | 0 | 7 passed |

- `uv` funcionó; no hizo falta el fallback de uvx.
- No corrí la suite completa ni `stores build --check`: Validation no los nombra.
- El `.venv` queda con el extra `postgres`, porque la última sincronización fue con `--extra postgres`.

## Archivos tocados en esta corrección
- `src/sldb/code/sql_pg.py`: archivo nuevo del intento, sin trackear. Lo autoriza el Implementation Path (3), y el coordinador pide documentar ahí el arreglo.
- `src/sldb/code/lang_sql.py`: solo el docstring.
- `tests/selfdoc/test_treesitter_symbols.py`.
- `CHANGELOG.md`.
- Evidencia: `runs/subagents/20261116-exec-k2-pg-c1/{validation.log,result-summary.md}`.

Los demás archivos del diff (`pyproject.toml`, `uv.lock`, `sql_pg_keys.py`, `sql_pg_tokens.py`, `sql_fact.py`, `sql_names.py`, los fixtures y `tests/api/test_anchors.py`) quedan como los dejó el intento anterior. No toqué `desk/` ni `.sldb/`, ni los cambios ajenos del árbol. No hice git add, stash ni commit.

## Desvíos y dudas
- **Caso límite.** Un nombre que contiene una secuencia UTF-8 truncada de varios bytes (por ejemplo, `\xe2\x82` seguido de ASCII):
  - `replace` de tree-sitter lo lee como un solo U+FFFD;
  - el texto de pglast lleva un U+FFFD por byte.

  El nombre de la clave podría diferir del de tree-sitter en ese caso. Los spans siguen exactos. Es un caso muy raro (un identificador con bytes que no son UTF-8 ni Latin-1 simple) y no lo documenté aparte.
- **Límite anotado.** Saqué de la lista «no dan hecho» del CHANGELOG el `UNIQUE USING INDEX` y lo dejé en una frase propia, porque sí da hecho, con `columns: []`.
