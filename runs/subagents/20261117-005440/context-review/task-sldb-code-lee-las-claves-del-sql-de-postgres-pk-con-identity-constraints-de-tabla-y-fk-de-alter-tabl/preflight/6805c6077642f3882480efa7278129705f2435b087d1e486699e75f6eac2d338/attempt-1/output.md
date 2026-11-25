## REFORMULACION

Encargo ejecutable (nodo único, no agregado): en el repo `SLDB_1`, ampliar el lector SQL de `sldb.code` para que, sobre migraciones `sqlmigrate` de Django/Postgres, emita: (a) la columna `id` con tipo, `primary_key` y `parse_partial` aunque `column_definition` tenga error, más `identity` si hay `GENERATED ... AS IDENTITY`; (b) un kind `constraint` hijo de su tabla para PK/FK/UNIQUE declaradas en `CREATE TABLE` y en `ALTER TABLE ... ADD CONSTRAINT`, con `qualified_name`, `constraint_type`, `columns` y, en FK, `references{table,columns}` y relación `references` intra-archivo. Sin nombre, `pk`/`fk`/`unique` con sufijo `~N` vía `ids.py`. Fuera: otras acciones de `ALTER TABLE`, estado acumulado, otros dialectos. Resultado esperado: tests y `check.sh --fast` en verde, fixture Django actualizado, docstring de `lang_sql.py`, CHANGELOG, commit y aviso a IR.

## AMBIGUEDADES

1. "el tipo leído del texto hasta el primer error": no define recorte, delimitadores ni normalización; obligaría a inventar el algoritmo exacto.
2. "attrs.constraint_type": no fija valores literales; obligaría a inventar el vocabulario (`primary_key` vs `PRIMARY KEY`).
3. "relación references hacia el hecho de la tabla referenciada si está en el mismo archivo": no cubre referencia a tabla ausente o posterior; obligaría a inventar comportamiento parcial.
4. "sin comentarios -- ni literales entre comillas simples": omite identificadores entre comillas dobles y dollar-quoting; obligaría a inventar el lexer de exclusión.
5. "Ampliar el fixture de Django existente": no nombra el archivo concreto; obligaría a elegir fixture nuevo o existente.
6. "partir en módulos si pasa de 80 líneas": no aclara si son líneas nuevas o del archivo; obligaría a fijar umbral.
7. "la misma función de ids.py": no nombra la función; obligaría a localizarla e inventar el contrato.

## DRY-RUN

**Lecturas:** `lang_sql.py`, `sql_readers.py`, `sql_fingerprints.py`, `ids.py`, fixture `tests/fixtures/treesitter/sql/django/`, tests citados, `CHANGELOG.md`. **Cambios previstos:** parser de `column_definition` con error; nuevo kind `constraint`; soporte `ALTER TABLE ADD CONSTRAINT`; naming con `ids.py`; relación `references`; docstring; tests y fixture; CHANGELOG. **Dependencias:** tree-sitter-sql 0.3.13, `ids.py`, fixture Django. **Validaciones futuras:** los cinco comandos de Validation y el criterio de Done When (columna `id` y una constraint por FK).

## FUTURO

Un humano resuelve las ambigüedades 1–7 antes de ejecutar; el ejecutor produce commit y aviso a IR; otro nodo valida el cierre.
