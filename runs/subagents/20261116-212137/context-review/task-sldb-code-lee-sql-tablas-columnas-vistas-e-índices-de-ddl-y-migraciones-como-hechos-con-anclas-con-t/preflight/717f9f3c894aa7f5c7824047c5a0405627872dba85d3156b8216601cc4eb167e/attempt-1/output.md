## REFORMULACION

Encargo: en `sldb.code` (repo SLDB_1), añadir lectura de SQL al pipeline de hechos con anclas. Propósito: que specIR pueda anclar nodos a DDL de Postgres. Resultado: extra `code` con `tree-sitter-sql`, módulo `lang_sql.py` que emite hechos `table`, `column`, `view`, `index`, `module` con `qualified_name` (con esquema si se escribe), docstring desde `--` contiguos, sufijos `~2` para duplicados, anclas `code:<ruta>.sql::<símbolo>` verificables por `check_anchors`; `.sql` añadido al dispatch, `find_files` y `code_ref` generalizados por B2; fixtures Postgres, tests intact/changed/lost/reconnected, CHANGELOG y aviso a IR. Límites: sin ALTER TABLE, sin estado acumulado entre migraciones, sin dialectos fuera de la gramática, sin TS/TSX; depende de la tarea B2 cerrada.

## AMBIGUEDADES

1. "una migración de dos tablas y una vista" vs. "El fixture cubre CREATE VIEW y CREATE MATERIALIZED VIEW, las dos con kind view": ¿una o dos vistas en el fixture? Obliga a inventar el número de fixtures.
2. "kind: table, column, view, index, module": no se define qué representa `module` en SQL ni su `qualified_name`; obliga a inventar si es el archivo.
3. "como ya hace Ids con nombres repetidos": no se da la regla exacta de numeración ni el formato del símbolo con sufijo; obliga a inferirla de código no citado.
4. "se omite la sentencia completa" frente a "se salta con un hecho menos": no queda claro si se emite algún hecho parcial de la sentencia no reconocida.
5. "con la misma forma que los de Python y TS": la forma exacta depende de B2 y no se especifica aquí; obliga a inventar el esquema del hecho.

## DRY-RUN

Lecturas: `pyproject.toml`, `uv.lock`, `src/sldb/code/runtime.py`, `models/code_ref.py`, tests citados, salida de B2. Cambios previstos: dependencia `tree-sitter-sql>=0.3`, `lang_sql.py` nuevo, `.sql` en dispatch/`find_files`/`code_ref`, fixtures y tests, CHANGELOG. Dependencias: B2 cerrada; gramática instalable. Validaciones futuras: los cuatro pytest y `tools/check.sh --fast` con `--extra code --extra dev`.

## FUTURO

Cierre de B2 y su API de dispatch (otro nodo). Decisión humana sobre el alcance de `module` y número de fixtures. Revisión de IR tras el aviso.
