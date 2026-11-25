REFORMULACION

Propósito: que `sldb.code` lea las claves del DDL de Postgres que genera `sqlmigrate` de Django (PK con `IDENTITY`, constraints de tabla y FK de `ALTER TABLE ADD CONSTRAINT`). Resultado: hechos de columna `id` con tipo, `primary_key` y `parse_partial`, y un `kind` nuevo `constraint` con `constraint_type`, `columns` y `references`. Repo: `/mnt/ssd/proyectos/SLDB_1`; superficie: `src/sldb/code/lang_sql.py`, `sql_readers.py`, tests citados y `CHANGELOG.md`. Límites: sin estado entre migraciones, sin otros dialectos, sin otras acciones de `ALTER TABLE`.

AMBIGUEDADES

1. «el tipo leído del texto hasta el primer error»: no define cómo localizar ese primer error (nodo `ERROR`/`MISSING`, byte, hijo); obliga a inventar el recorte.
2. «(o `<tabla>.pk`, `<tabla>.fk~N` si no tiene nombre)»: no cubre UNIQUE sin nombre ni aclara si `~N` comparte semántica con los sufijos de `Ids`; obliga a inventar nombres.
3. «un hecho por cada clave (primaria, foránea y única)» frente a «PRIMARY KEY, FOREIGN KEY y UNIQUE de tabla»: no dice si las constraints de columna (`id bigserial PRIMARY KEY`, `email text NOT NULL UNIQUE`) generan hecho `constraint`; obliga a decidir alcance.
4. «relación references hacia el hecho de la tabla referenciada si está en el mismo archivo»: no aclara referencias a tablas definidas después ni el formato del target; obliga a inventar orden y resolución.
5. «Ampliar el fixture de Django existente»: el test actual afirma «the IDENTITY id columns are left out» y el `DJANGO` esperado no incluye `id`; el encargo exige emitirlo, sin decir cómo actualizar ese contrato; obliga a inventar el nuevo esperado.
6. «attrs.parse_partial true»: no existe tal attr en los hechos actuales (`parse_errors` sí); no dice si aplica a toda columna o solo a la parcial.
7. «partir en módulos si pasa de 80 líneas»: no especifica si son líneas por archivo, por función o por diff.

DRY-RUN

Lecturas: `lang_sql.py`, `sql_readers.py`, `sql_fingerprints.py`, fixture `tests/fixtures/treesitter/sql/django/`, tests de símbolos, anclas y fingerprints. Cambios previstos: readers tolerantes para `column_definition` con error y `IDENTITY`; nuevo lector de constraints de tabla y de `ALTER TABLE ... ADD CONSTRAINT`; hechos `constraint` y relaciones; ajuste de tests y `CHANGELOG`. Dependencias: tree-sitter-sql 0.3.13 y su árbol real. Validaciones futuras: los cinco comandos de Validation, más revisión de que `.py`/TS no cambian.

FUTURO

Otro nodo/humano debe: inspeccionar el árbol real de tree-sitter-sql para confirmar el parseo de `ALTER TABLE` e `IDENTITY`; regenerar el fixture con `sqlmigrate`; validar la semántica de `references`; decidir commit y aviso a IR08.
