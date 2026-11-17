# Tester deskops-t-ea7b55aab3a8: C4 con pglast (extra postgres)

Tarea: `task-sldb-code-lee-las-claves-del-sql-de-postgres-pk-con-identity-constraints-de-tabla-y-fk-de-alter-tabl`. Pills: ninguno.
Ejecutor: deskops-e-67dedd6aa01e (`runs/subagents/20261116-exec-k2-pg/`).

**Veredicto: FALLA.** Pasan Validation (con el extra y sin él), Done When, los puntos (1) a (4) del coordinador y las regresiones vecinas. Todos los bordes de los tres testers anteriores dan las claves correctas.

El motivo de la falla es un defecto nuevo que encontré: **con el extra, un `.sql` que no está en UTF-8 corre los offsets de bytes.** Por ejemplo, un comentario en Latin-1 basta para que una tabla reciba las columnas y las claves de otra y pierda las suyas, sin `keys_partial`. Sin el extra (lectura de HEAD) el mismo archivo se lee bien. El detalle está en «Defecto».

La salida completa está en `validation.log`. Los scripts y las sondas están en `/dev/shm/k2pgt/`.

## Validation (corrida por mí)
| Comando | rc | Resultado |
|---|---|---|
| `uv run --frozen --extra code --extra postgres --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 30 passed |
| `... --extra postgres ... pytest -q tests/api/test_anchors.py` | 0 | 23 passed |
| `... --extra postgres ... pytest -q tests/selfdoc/test_fingerprints.py` | 0 | 4 passed |
| `uv run --frozen --extra code --extra dev pytest -q tests/selfdoc/test_treesitter_symbols.py` | 0 | 30 passed |
| `... --extra postgres ... pytest -q tests/test_clean_code_rules.py` | 0 | 1198 passed |
| `... --extra postgres ... bash tools/check.sh --fast` | 0 | TODAS LAS PUERTAS PASAN |
| Obligatorios del brief sin el extra: `test_clean_code_rules.py` y `check.sh --fast` | 0 | 1198 passed; PASAN |
| `uv run --exact` sin el extra: se comprueba que pglast no está y se corren symbols, anchors y fingerprints | 0 | `find_spec('pglast')` da None; 41 passed, 16 skipped |

`uv` funcionó. La suite completa y `stores build --check` no figuran en Validation y no los corrí.

## Done When
- **Validation pasa, con el extra y sin él: PASA** (tabla de arriba).
- **Los bordes de los tres testers dan las claves correctas con el extra: PASA.** Ver el punto (2).
- **Fixture de Django: PASA.**
  - `app_author.id` y `app_book.id` dan `type bigint`, `primary_key`, `identity` y `parse_partial`. `posts.id` del fixture de blog da lo mismo.
  - La FK de ALTER da `references {app_author,[id]}` con su relación. La de blog da `{auth_user,[id]}` sin relación.
  - `slug_pages_uniq` sale y el CHECK no da hecho. Sale también el `unique_together` del ALTER.
- **Sin el extra, la lectura de .sql es la de HEAD salvo `keys_partial`: PASA.** Ver el punto (3).
- **Los hechos de .py y TS no cambian: PASA.** Ver el punto (4).
- **CHANGELOG: PASA**, con una entrada C4 en 0.1.13 y los límites. Commit y aviso a IR no están hechos: le tocan al integrador.

## Puntos del coordinador
**(1) Fixture `0001_initial.sql` modificado: PASA, no oculta ningún caso.**
- El cambio es una sola línea: `CONSTRAINT "slug_pages_uniq" UNIQUE` pasa a ir antes de `CONSTRAINT "pages_ok" CHECK`, que es el orden en que sqlmigrate escribe `Meta.constraints = [UniqueConstraint, CheckConstraint]`.
- Con el código de HEAD, la lectura de tree-sitter del fixture viejo y la del nuevo dan los mismos 12 objetos y columnas. El cambio no altera lo que probaban los tests de HEAD.
- El orden anterior (el CHECK antes del UNIQUE) sigue cubierto:
  - el test `u4` del archivo de tests lo prueba;
  - pasé el fixture de HEAD por el código nuevo con el extra y da `slug_pages_uniq` igual que el nuevo (lo muestra el log).

**(2) Bordes de los tres testers con el extra: PASA, todos.** Usé los `.sql` originales: `edge.sql` del tester 1, idéntico (cmp) al de `/dev/shm/k2c1t`; `edge2`, `edge3` y `shop_0001` de c1; los 15 `v/*.sql` de c2.
- Tester 1:
  - `parent_self_fk` da `{public.parent, []}` con su relación.
  - `odd.unique` da `["a)b"]`.
  - Pasan los esquemas, `ONLY`, `IF EXISTS`, las minúsculas y dos `ADD` en un mismo ALTER.
  - `pk`, `unique` y `unique~2` salen bien. `ghost_fk` cuelga del módulo.
  - Los comentarios y literales no marcan columnas, y tampoco las columnas `"unique"` o `"primary key"`.
- Tester c1:
  - `d.fk` y `f2.fk` dan `{t, []}`.
  - Con `""`: `p"q`, `p"k`, `i"d`, `["a\"b","x"]`, `t.f → ["a\"b"]` y `g"h`.
  - Las acciones mixtas del ALTER funcionan.
  - El caso `e_fk` seguido de `e_u` ahora da las dos claves.
- Tester c2:
  - `u1`, `u2`, `u3` y `u4` dan `uniq_ab` o `uniq_a` en cualquier orden respecto del CHECK.
  - `a5`, `a6` y `a3` dan la FK con nombre, también cuando es la última. `a3` además da su `unique`.
  - `a8` da `a8_fk` antes del CHECK.
  - `"c""1" int` tiene tipo `int`.
  - `n.sql`: `n4_u` sale después del EXCLUDE.
  - Las FK de columna van en `attrs.references`, sin hecho propio.
  - Los sufijos salen por tipo: `d.fk`/`fk~2` y `unique`/`unique~2`.
- **sqlmigrate real de Django** (`shop_0001.sql`, Django 6.1.3; el tester 1 lo generó con FK, FK a `auth_user`, M2M, `unique_together`, `Meta.constraints` con UniqueConstraint y luego CheckConstraint, y `unique=True`):
  - las 4 `id` dan `primary_key`, `identity` y `bigint`;
  - `uniq_cat_sku` da `unique`, y `price_pos` no da hecho;
  - los 2 `unique_together` salen;
  - las 4 FK tienen las references correctas, con relación a `shop_category`, `shop_product` y `shop_tag`, y sin relación a `auth_user`;
  - `name` lleva la marca `unique`.

  No regeneré la migración: el venv de Django del tester 1 ya no está en `/dev/shm/k2t`. Uso su salida guardada, que es sqlmigrate sin editar.

**(3) Sin el extra comparado con HEAD (`git archive HEAD` en `/dev/shm/k2pgt/head`): PASA.**
- Corpus: `src/`, los fixtures de trabajo y de HEAD, y todas las sondas.
- Comparé `scan_tree` con el código de HEAD y con el de trabajo poniendo `sql_pg._pg = None`: 6055 hechos en los dos y JSON idéntico una vez quitado `keys_partial`.
- `keys_partial` aparece en 36 tablas, siempre con valor true y solo en hechos `table`.

**(4) .py y TS comparados con HEAD: PASA.** Con el extra, los 5815 hechos que no son `.sql` (py 5783, tsx 18, ts 6, jsx 4, js 4) son idénticos a los de HEAD.

## Casos propios (no cubiertos por el ejecutor)
- **pg_dump `-s` de PG 17 con `\restrict`/`\unrestrict`, `SET`, `OWNER TO` y `ALTER COLUMN ... ADD GENERATED`: PASA.** Salen `author_pkey`, `book_pkey` y `book_author_id_fk` con su relación, y los tipos `character varying(100)`.
- **Multibyte UTF-8** (emoji y ñ en un comentario previo y dentro de nombres, más un comentario `/* 😀 */` dentro de la columna): **PASA.** Los spans, los nombres (`ü😀k`, `café_ü_fk`) y la relación son correctos.
- **Tipos y opciones**: **PASA.**
  - Una columna con `CONSTRAINT ty_pk PRIMARY KEY` lleva la marca `primary_key` y tipo `int`.
  - `COLLATE "C" UNIQUE`, `double precision[]`, `numeric(10, 2) DEFAULT round(1.5, 0)` y `timestamp(3) with time zone` dan bien el tipo.
  - `UNIQUE (e) INCLUDE (f)` da `[e]`.
  - Pasan una FK multicolumna con `MATCH FULL`, `PRIMARY KEY ... WITH (...) USING INDEX TABLESPACE`, `IF NOT EXISTS`, `UNLOGGED`, `PARTITION BY` y `NOT VALID`.
- **Límites (no son falla):**
  - Un `COPY ... FROM stdin` con datos (pg_dump con datos): el scanner no puede partir el archivo, se pierde la PK del ALTER y la tabla lleva `keys_partial`. La pérdida queda avisada, y `pg_statements` documenta que en ese caso devuelve `[]`.
  - `CREATE TABLE Mixed` seguido de `ALTER TABLE mixed ...`: la clave cuelga del módulo como `mixed.m_u`. Es el límite documentado de no pasar los nombres a minúsculas.
  - `CREATE TABLE tp1 PARTITION OF ...` seguido de otro `CREATE TABLE`: tree-sitter funde las dos sentencias y la segunda se pierde, igual que en HEAD. Es el límite documentado «un CREATE que tree-sitter no ve como tal».
  - `ADD CONSTRAINT u UNIQUE USING INDEX idx` da `columns: []`. Es exótico y no está documentado; conviene anotarlo.
  - `CREATE TABLE ... AS SELECT` lleva `keys_partial` aunque no tenga claves. Es inocuo.

## Defecto (motivo de FALLA)
**Con el extra, un archivo que no es UTF-8 da hechos de claves y columnas erróneos sin aviso.**
- **Causa:**
  - `sql_pg.pg_statements` decodifica con `src.decode("utf-8", "replace")`, y cada byte inválido pasa a ser U+FFFD, que ocupa 3 bytes.
  - `_statement` y `to_byte` calculan los offsets con `len(text[:pos].encode())`, así que en el archivo original quedan corridos 2 bytes por cada byte inválido.
  - `lang_sql._object_facts` busca la sentencia de pglast con `p["start"] <= node.start_byte < p["end"]`, de modo que el `CREATE TABLE` siguiente cae dentro del rango inflado de la sentencia anterior.
- **Reproducción** (`/dev/shm/k2pgt/l1/shift.sql`, codificado en Latin-1):
  ```sql
  CREATE TABLE a (id int PRIMARY KEY, x int, -- comentario: año año … (20 veces)
    CONSTRAINT a_u UNIQUE (x));
  CREATE TABLE b (k int, CONSTRAINT b_fk FOREIGN KEY (k) REFERENCES a (id));
  ```
- **Con el extra:**
  - la tabla `b` recibe `b.id` (con `primary_key`), `b.x` y la clave `b.a_u` de la tabla `a`;
  - pierde su columna `k` y su FK `b_fk`;
  - no lleva `keys_partial`;
  - la signature de `a.a_u` es `'b (k int, CONSTRAINT b_f'`.
- **El mismo texto en UTF-8** (`shift_utf8.sql`) da todo bien. **HEAD y la lectura sin el extra** dan `b` con `b.k`.
- **Con un solo comentario Latin-1** (`latin1.sql`), las claves son correctas, pero:
  - las signatures, spans y fingerprints de las columnas y constraints salen corridos (`'igint NOT NULL PRIMARY KEY…'`, `'AINT "author_uq" … ALT'`);
  - columnas que tree-sitter parsea limpias pasan a `parse_partial`.
- **Clasificación:** el SQL es común y lo único distinto es la codificación del archivo, cosa plausible en migraciones viejas o escritas en Windows-1252. Son datos erróneos sin aviso, no documentados, y el resultado es peor que sin el extra. Lo cuento como **FALLA**.
- **Arreglo sugerido**, local a `sql_pg.py`, a elección del ejecutor:
  - si `src` no decodifica como UTF-8 estricto, devolver `[]` (la tabla queda con `keys_partial`);
  - o decodificar con `surrogateescape` y codificar igual en `to_byte`/`_statement`.

  Falta además un test con un byte no UTF-8 antes de dos `CREATE TABLE`.

## Alcance de archivos: PASA
- Modificados: `CHANGELOG.md`, `pyproject.toml`, `uv.lock`, `lang_sql.py`, `tests/api/test_anchors.py`, `tests/selfdoc/test_treesitter_symbols.py` y el fixture `0001_initial.sql`.
- Nuevos: `sql_fact.py`, `sql_names.py`, `sql_pg.py`, `sql_pg_keys.py`, `sql_pg_tokens.py` y `blog_0001_initial.sql`. Todos son de la tarea, según el coordinador.
- `sql_readers.py` queda igual que en HEAD.
- El diff de `uv.lock` solo agrega el paquete `pglast` 8.8, el extra `postgres` y su línea en `provides-extras`.
- Los cambios en `desk/` y `.sldb/` son del registro de runs y no los reviso.

## Regresiones vecinas: PASA
- Módulos de `src/` cambiados: `lang_sql`, `sql_fact`, `sql_names`, `sql_pg`, `sql_pg_keys` y `sql_pg_tokens`.
- Por nombre los importa `test_treesitter_symbols.py`. Por el scanner los usan `test_anchors.py`, `test_component_spec_python.py` y `test_treesitter_agreement.py`. Sumé `test_fingerprints.py`.
- Trabajo, con el extra: 30, 23, 4, 5 y 2 passed.
- HEAD, con `git archive` y `PYTHONPATH` a `head/src` (verificado con `sldb.__file__`): 14, 22, 4, 5 y 2 passed.
- No hay fallas nuevas.

## Entorno
- No hice git add, stash ni commit, y no edité `desk/`, `.sldb/` ni el repo.
- El `.venv` queda con el extra `postgres`: la última sincronización fue con `--extra postgres`, después de una corrida `--exact` sin él.
