# Tester deskops-t-1ad7afff3591: C4 corrección 2

**Veredicto: FALLA.** Validation pasa, pero en `CREATE TABLE` se pierden sin aviso claves con nombre: la que genera Django y la que se escribe a mano de forma común. Una de ellas es una regresión respecto de c1.

Toda la salida está en `validation.log`. Las sondas están en `/dev/shm/k2c2t/v/*.sql` y su salida en `/dev/shm/k2c2t/probes.log`.

## Validation (comandos corridos por mí; todos con `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev`)

| Comando | rc | Resultado |
|---|---|---|
| pytest -q tests/selfdoc/test_treesitter_symbols.py | 0 | 24 passed: PASA |
| pytest -q tests/api/test_anchors.py | 0 | 23 passed: PASA |
| pytest -q tests/selfdoc/test_fingerprints.py | 0 | 4 passed: PASA |
| pytest -q tests/test_clean_code_rules.py | 0 | 1198 passed: PASA |
| bash tools/check.sh --fast | 0 | PASA |

No corrí la suite completa ni `stores build --check`: Validation no los nombra.

## Done When
- **Validation pasa: PASA.**
- **`id` con `primary_key` y `parse_partial` en el fixture de Django: PASA.**
  - `app_book.id`, `app_author.id` y `posts.id` dan `{type: bigint, primary_key, identity, parse_partial}`.
  - Las FK de `ALTER` dan `references` correctas:
    - `app_book_author_id_…_fk_app_author_id` da `{app_author, [id]}`, con su relación;
    - `posts_…_fk_auth_user_id` da `{auth_user, [id]}`, sin relación.
- **Hechos de .py y TS iguales a HEAD: PASA.**
  - Corpus: `src/` + `tests/fixtures/treesitter`, sin `.sql`.
  - Corrí `scan_tree` con el `src` de HEAD (`git archive`) y con el de trabajo: 5749 hechos en los dos y md5 `f69a5fbe…` idéntico.
- **CHANGELOG: está. Commit y aviso a IR: no hechos**, por instrucción; quedan al integrador.

## (1) Sondas anteriores, repetidas
- `edge.sql`, `edge2.sql`, `edge3.sql` (`/dev/shm/k2c1t/root/mig`): **PASA**.
  - Los defectos 1, 2, A y B de los testers anteriores salen corregidos: `parent_self_fk {public.parent, []}`, `odd.unique ["a)b"]`, `d.fk`/`f2.fk`/`e_fk` con `{t, []}`, `p"q`, `p"k`, `"a""b"` → `a"b`, `g"h`.
  - Los `CHECK`, `ADD COLUMN` y `ADD PRIMARY KEY` sin nombre no dan hecho.
  - `weird."unique"` y `weird."primary key"` no se marcan.
- **sqlmigrate real** (`/dev/shm/k2t/shop_0001.sql`, Django 6.1.3, modelos con `unique=True`, `unique_together`, `Meta.constraints` con `UniqueConstraint` + `CheckConstraint`, FK a `auth_user`, M2M): **FALLA, por regresión**.
  - `CONSTRAINT "uniq_cat_sku" UNIQUE ("category_id", "sku"), CONSTRAINT "price_pos" CHECK ("price" >= 0)` ya no da `shop_product.uniq_cat_sku`.
  - El tester de c1 lo vio salir. El ejecutor afirma «la migración real da las mismas claves que en c1», y eso es falso.
  - El resto de shop está bien: 4 `id`, la marca `unique` de `name`, `unique_together`, las 4 FK y sus relaciones.
- **.py/TS:** PASA (arriba).

## (2) Puntos A–D de la corrección 2
- **A, toda FK lleva `references`: FALLA.**
  - Una FK de tabla **sin nombre** está bien: `a1`, `a2` y `a7` dan `{t, []}`.
  - Una FK de tabla **con nombre** y sin columnas referenciadas que es la última clave no da ningún hecho:
    - `CREATE TABLE a5 (id int, x int, CONSTRAINT a5_fk FOREIGN KEY (x) REFERENCES t);` → solo la tabla y sus columnas (`a5.sql`).
    - Pasa lo mismo con `REFERENCES public.t` (`a6`).
    - Pasa lo mismo con `... REFERENCES t ON DELETE CASCADE, UNIQUE (id)` (`a3`), que además pierde el `UNIQUE`.
  - Las FK de columna (`REFERENCES u`, `REFERENCES u (id) ON DELETE CASCADE`, `REFERENCES "public"."u"("id")` y en una tabla con `id` IDENTITY) dan `attrs.references` correcto, sin hecho constraint: PASA.
- **B, `""`: PASA en lo pedido**, con un defecto menor fuera de lo pedido.
  - Pasan los nombres de tabla `x"y`, los nombres de constraint `k"1`, `f"k` y `z"fk`, las listas `["c\"1","c2"]`, y las refs de `ALTER` y de `CREATE` hacia `x"y (c"1)`.
  - Defecto menor: una columna `"c""1" int` da `attrs.type: null`, sea la primera columna o no (`b.sql`, `b2.sql`). El informe del ejecutor dice «`"i""d" int` tiene tipo `int`», y eso no se reproduce. Es exótico: lo clasifico como no-falla, pero es un dato erróneo no documentado.
- **C, REFERENCES en columna: PASA.** Lo da `attrs.references` en la columna, más la relación si la tabla está en el archivo, y ningún hecho constraint.
- **D, sufijos por tipo dentro de la tabla: PASA.** `d.unique`/`unique~2`, `d.fk`/`fk~2` y `d.pk` (`d.sql`); `e.unique`/`e.unique~2`.

## (3) Bordes nuevos, clasificados

**FALLA (datos que faltan sin aviso, sobre SQL común):**
1. **`CONSTRAINT x UNIQUE (...)` seguido de `CONSTRAINT y CHECK (...)` en `CREATE TABLE`: se pierde el UNIQUE** (`u1.sql`; `u4.sql` con CHECK antes y después).
   - Es exactamente lo que `sqlmigrate` escribe para `Meta.constraints = [UniqueConstraint(...), CheckConstraint(...)]`, un patrón normal en Django.
   - Causa: tree-sitter-sql 0.3.13 deja `UNIQUE ("a", "b"), CONSTRAINT "a_pos"` en un `ERROR` dentro del nodo `constraint` del CHECK.
   - El límite documentado («una clave enterrada en el ERROR de otra clave: `CONSTRAINT a FOREIGN KEY … , CONSTRAINT b UNIQUE` pierde b») no lo cubre: aquí se pierde la primera, y el CHECK no es una clave. Además es una regresión respecto de c1.
   - Con el UNIQUE detrás del CHECK (`u3`), o sin CHECK (`u2`), sale bien.
2. **`CONSTRAINT x FOREIGN KEY (c) REFERENCES t (id), CONSTRAINT y CHECK (...)`: se pierde la FK** (`a8.sql`). Es la forma más común de declarar una FK con nombre a mano en Postgres.
3. **`CONSTRAINT x FOREIGN KEY (c) REFERENCES t` como última clave, con o sin esquema: no da hecho** (`a5`, `a6`). Es Postgres escrito a mano habitual y es el caso que pide el punto A del Scope. Solo funciona sin nombre.

**Límites (no son falla):**
- Una columna `"c""1" int` da `type: null`. Es exótico y nunca lo genera Django, pero no está documentado: convendría documentarlo o arreglarlo.
- `ALTER TABLE … ADD CONSTRAINT … EXCLUDE USING gist (...)` hace que la gramática se trague el `ALTER … ADD CONSTRAINT n4_u UNIQUE …` siguiente (`n.sql`; el mismo ALTER aislado sale bien en `n5.sql`). EXCLUDE es raro y está documentado como límite, aunque el efecto sobre la sentencia siguiente no lo está.
- `REFERENCES "public"."u"` cuando la tabla se creó como `u`: no hay relación porque los nombres difieren, y `attrs.references` es correcto. Es coherente con el diseño de un archivo sin estado.

## Alcance de archivos: PASA, con una nota
- `git diff --name-only -- src tests CHANGELOG.md`: `lang_sql.py`, `sql_readers.py`, los 2 tests del contrato y CHANGELOG.
- Sin trackear: `sql_columns.py`, `sql_fact.py`, `sql_keys.py`, `sql_key_text.py` y `sql_names.py`, que el Scope permite al partir en módulos, y el fixture `blog_0001_initial.sql`.
- El Scope pedía «ampliar el fixture existente»; se agregó uno nuevo y el existente `0001_initial.sql` no cambió. El coordinador lo da por parte de la tarea.
- Los cambios en `desk/` y `.sldb/` son del registro de runs y no los reviso.
- `sql_keys.py` tiene 97 líneas brutas; `test_clean_code_rules` pasa (cuenta líneas efectivas).

## Regresiones vecinas: PASA
- Módulos cambiados: `lang_sql` y `sql_readers`, más los 5 nuevos. Por nombre los importa solo `test_treesitter_symbols.py`. Sumé `test_anchors.py`, `test_fingerprints.py`, `tests/notations/test_component_spec_python.py` y `tests/selfdoc/test_treesitter_agreement.py`.
- Trabajo: 24, 23, 4, 5 y 2 passed. HEAD (`git archive` en `/dev/shm/k2c2t/head`, `PYTHONPATH` al `src` de HEAD): 14, 22, 4, 5 y 2 passed.
- No hay fallas nuevas.
- Una línea `rc=4` del log es una ruta mía equivocada (`tests/selfdoc/test_component_spec_python.py`); se repitió con la correcta.

## Entorno
`uv run --frozen` funcionó. No hice git add, stash ni commit, y no edité `desk/` ni `.sldb/`.
