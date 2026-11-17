# Tester deskops-t-ea7b55aab3a8-a2: corrección 1 de C4 con pglast (extra postgres)

Tarea: `task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl`. Pills: ninguno.
Ejecutor: deskops-e-67dedd6aa01e-a2 (`runs/subagents/20261116-exec-k2-pg-c1/`).

**Veredicto: PASA.**
- El defecto del tester anterior (los offsets se corrían en los `.sql` que no están en UTF-8) está corregido. Lo comprobé con sus sondas y con encodings mezclados.
- Pasan Validation, con el extra y sin él, y Done When.
- No hay regresiones en los bordes de los tres testers, en el sqlmigrate real de Django, en los hechos de .py y TS ni en la lectura sin el extra.
- Encontré dos límites, que no hacen fallar la tarea: el BOM, que queda avisado con `keys_partial`, y una secuencia UTF-8 truncada dentro de un nombre, que es exótica. Están en «Casos propios».

La salida completa está en `validation.log`. Los scripts, las sondas y los JSON están en `/dev/shm/k2pgt2/`.

## Validation (corrida por mí)
| Comando | rc | Resultado |
|---|---|---|
| `uv run --frozen --extra code --extra postgres --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 32 passed |
| `... --extra postgres ... pytest -q tests/api/test_anchors.py` | 0 | 23 passed |
| `... --extra postgres ... pytest -q tests/selfdoc/test_fingerprints.py` | 0 | 4 passed |
| `uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 32 passed |
| `... --extra postgres ... pytest -q tests/test_clean_code_rules.py` | 0 | 1198 passed |
| `... --extra postgres ... bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |
| Obligatorios del brief sin el extra: `test_clean_code_rules.py` y `check.sh --fast` | 0 | 1198 passed; PASAN |
| `uv run --exact` sin el extra: `find_spec('pglast')`, luego symbols, anchors y fingerprints | 0 | pglast None; 41 passed, 18 skipped |

- `uv` funcionó.
- La suite completa y `stores build --check` no figuran en Validation: no los corrí (delegado al integrador).
- El `.venv` queda con el extra `postgres` y con los paquetes que quitó la corrida `--exact`; la siguiente `uv run` los vuelve a sincronizar.

## Done When
- **Validation pasa, con el extra y sin él: PASA** (tabla de arriba).
- **Los bordes de los tres testers dan las claves correctas: PASA.** Ver el punto (2).
- **Fixture de Django: PASA.** `shop.out` sale idéntico al aprobado:
  - `app_author.id` y `app_book.id` dan `bigint`, `primary_key` e `identity`;
  - salen las FK de ALTER;
  - `slug_pages_uniq` sale antes del CHECK, y el CHECK no da hecho.
- **Sin el extra, igual que HEAD salvo `keys_partial`: PASA.** Ver el punto (3).
- **Los hechos de .py y TS no cambian: PASA.** Ver el punto (3).
- **CHANGELOG: PASA.** La entrada C4 suma un párrafo sobre los archivos que no son UTF-8 y la nota sobre `UNIQUE USING INDEX`. El commit y el aviso a IR le tocan al integrador.

## Puntos del coordinador
**(1) Sondas del tester anterior y encodings mezclados: PASA.**
- `shift.sql`, en Latin-1:
  - `b` da `b.k` y `b.b_fk` con `references {a,[id]}` y su relación;
  - `a` da `a.id` (con `primary_key`), `a.x` y `a.a_u`;
  - no aparece `keys_partial`;
  - las signatures son correctas (`'CONSTRAINT a_u UNIQUE (x)'`).

  `latin1.sql` y `shift_utf8.sql` también salen bien.
- **Sondas nuevas** en `/dev/shm/k2pgt2/enc/`, generadas por `scripts/mk.py`. Cada una lleva PK con IDENTITY, UNIQUE de tabla, FK de tabla, ALTER ADD CONSTRAINT y una tabla posterior que referencia a la anterior:
  - `crlf.sql` y `crlf_latin1.sql`;
  - `lit_latin1.sql` y `lit_utf8.sql`: Latin-1 dentro de un literal `DEFAULT '...'` y de un `COMMENT ON ... IS '...'` antes de las claves;
  - `name_latin1.sql` y `name_utf8.sql`: Latin-1 dentro de nombres entre comillas de tabla, columna, constraint y FK (`"año"`, `"señal"`, `"niño_fk"`, `"niño_x_uñiq"`), también en la tabla con IDENTITY;
  - `bom.sql`, `bom_crlf_latin1.sql` y `name_latin1_crlf_bom.sql`.
- **Cómo lo comprobé** (`scripts/check.py`), por cada archivo:
  - las signatures de las constraints empiezan por `CONSTRAINT`, `PRIMARY`, `FOREIGN` o `UNIQUE` y contienen su nombre;
  - las `columns` de cada clave existen como columnas de su tabla;
  - cada hecho de tree-sitter (tabla, columna o módulo) tiene, con el extra, el mismo id, span, signature, `source_hash` y fingerprints que sin él.
- **Resultado:**
  - CRLF, Latin-1 en literales y Latin-1 en nombres dan todas las claves y relaciones correctas;
  - no hay offsets corridos ni `keys_partial`;
  - los nombres en Latin-1 salen con U+FFFD, igual que los de tree-sitter.
- Con el BOM y con una secuencia truncada aparecen los límites que se describen abajo.

**(2) Bordes de los tres testers y sqlmigrate real: PASA, sin regresiones.**
- Corrí el mismo `dump.py` del tester anterior sobre:
  - `edge*.sql`;
  - los 15 `v_*.sql`;
  - `shop_0001.sql` (sqlmigrate de Django 6.1.3, el mismo archivo);
  - los dos fixtures de Django;
  - sus sondas propias (`mine/`).
- Las cuatro salidas (`edges1`, `edges2`, `shop`, `mine`) son **idénticas** (diff vacío) a las que el tester anterior dio por buenas en `/dev/shm/k2pgt/*.out`.

**(3) .py/TS y la lectura sin el extra comparados con HEAD: PASA.**
- Usé un `git archive HEAD` nuevo en `/dev/shm/k2pgt2/head`. Su `src/` es igual al de la ronda anterior.
- El corpus son 6173 hechos:
  - el `src/` actual;
  - los fixtures de trabajo y de HEAD;
  - todos los bordes y las sondas, también las de encoding.
- **Sin el extra frente a HEAD:**
  - el JSON es idéntico una vez quitado `keys_partial`;
  - `keys_partial` aparece en 67 tablas, siempre true y solo en hechos `table`.
- **Con el extra frente a HEAD:** los 5816 hechos que no son `.sql` son idénticos (py 5784, tsx 18, ts 6, jsx 4, js 4).
- **Con el extra frente a sin el extra, en `.sql`:**
  - ningún hecho común difiere en span, signature ni fingerprints;
  - los ids que cambian son los esperados por el contrato, como los nombres con `""` (`p` pasa a `p"q`, `x` a `x"y`) y las columnas IDENTITY que se agregan;
  - `tp1.Id` desaparece, que es el límite ya conocido de `PARTITION OF` (tree-sitter funde dos sentencias);
  - el caso truncado se describe abajo.

## Casos propios (no cubiertos por el ejecutor)
**Límite A, el BOM UTF-8.**
- Con el extra, la primera sentencia del archivo no parsea con pglast, porque el BOM queda pegado a `CREATE`.
- Su tabla pierde las claves y la columna IDENTITY, igual que sin el extra, y **lleva `keys_partial: true`**. Las sentencias siguientes salen completas.
- Es el fallback que fija el contrato y queda avisado. No es peor que HEAD.
- psql tampoco acepta un archivo con BOM.
- No es falla. Conviene documentarlo o quitar el BOM antes de pasar el texto a pglast.

**Límite B, una secuencia UTF-8 truncada dentro de un nombre entre comillas** (`trunc.sql`: `"t\xe2\x80x"`, `"c\xe2\x80z"`).
- La lectura de tree-sitter (`replace`) da un U+FFFD, y la de pglast (`surrogateescape`) da uno por byte.
- Con el extra, el resultado es:
  - la columna pasa a `t�x.c��z`, un id distinto del de HEAD;
  - la clave da `columns ["c��z"]`;
  - la FK da `references {"t��x"}`, y se pierde la relación;
  - no aparece `keys_partial`.
- El ejecutor lo anotó en «Desvíos», pero no está en el docstring ni en el CHANGELOG.
- Lo clasifico como **límite**, no como falla:
  - hace falta un nombre entre comillas con una secuencia multibyte truncada; en Latin-1, una letra à–ï u ð–ô pegada a un símbolo 0x80–0xBF, cosa que casi no pasa en un identificador;
  - los spans y las signatures siguen exactos;
  - lo común, que son los comentarios, los literales y los nombres en Latin-1, sale bien.
- Recomendación: documentarlo, o decodificar los nombres de pglast desde los bytes con `replace`.

## Alcance de archivos: PASA
- **Modificados:**
  - `CHANGELOG.md`, `pyproject.toml` y `uv.lock`;
  - `lang_sql.py`;
  - `tests/api/test_anchors.py` y `tests/selfdoc/test_treesitter_symbols.py`;
  - el fixture `0001_initial.sql`.
- **Nuevos:** `sql_fact.py`, `sql_names.py`, `sql_pg.py`, `sql_pg_keys.py`, `sql_pg_tokens.py` y `blog_0001_initial.sql`. Los autorizan el Implementation Path (3) y el coordinador («todo el diff del árbol es de esta tarea»).
- `sql_readers.py` queda igual que en HEAD.
- Ya no aparecen los cambios ajenos que lista el brief (`apply_batch.py`, `lock.py` y `test_apply_batch_lock.py`).
- `desk/` y `.sldb/` son del registro de runs y no los reviso.

## Regresiones vecinas: PASA
- **Módulos de `src/` cambiados:** `lang_sql`, `sql_fact`, `sql_names`, `sql_pg`, `sql_pg_keys` y `sql_pg_tokens`.
- **Tests que los usan:**
  - por nombre, `test_treesitter_symbols.py`;
  - por el scanner, `test_anchors.py`, `test_fingerprints.py`, `test_treesitter_agreement.py` y `test_component_spec_python.py`.
- **Resultados, archivo por archivo:**
  - en el árbol de trabajo, con el extra: 32, 23, 4, 2 y 5 passed;
  - en HEAD, con `PYTHONPATH` apuntando a `/dev/shm/k2pgt2/head/src` (verificado con `sldb.__file__`): 14, 22, 4, 2 y 5 passed.
- No hay ninguna falla nueva.

## Entorno
No hice git add, stash ni commit. No edité `desk/`, `.sldb/` ni el repo. Todo lo que escribí fuera de este run-dir está en `/dev/shm/k2pgt2`.
