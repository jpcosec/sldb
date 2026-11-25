## REFORMULACION
Encargo ejecutable de `task.code` en el repo SLDB_1: leer las claves del DDL de Postgres con `pglast` (extra opcional `postgres`) y mantener tree-sitter-sql como fallback. Propósito: que `sldb.code` emita hechos correctos de PK, FK, UNIQUE, columnas con `IDENTITY`/`UNIQUE`/tipo y `references`, sin pérdidas silenciosas. Resultado: parche aplicado, módulo de lectura con pglast, facts/attrs acordados, tests con bordes de testers, docstring, CHANGELOG y validaciones. Límites: no estado acumulado entre migraciones, no otros dialectos, no CHECK/EXCLUDE, no otras acciones de `ALTER TABLE`.

## AMBIGUEDADES
1. “si el texto contiene PRIMARY KEY, attrs.primary_key true” frente a “la lectura textual de claves sobre nodos ERROR se reemplaza por pglast”. Obliga a inventar si se conserva o elimina el fallback textual en columnas con error.
2. “excluyendo CHANGELOG.md si choca y reescribiendo su entrada”. No define resolución de conflictos del parche; obliga a inventar estrategia de merge.
3. “los bordes de los tres testers (runs/subagents/20261116-test-k2*/result-summary.md)”. El glob no enumera los tres archivos ni sus casos; obliga a inventar el inventario si no coinciden exactamente.
4. “sin el extra, la lectura de .sql no cambia respecto de HEAD salvo attrs.keys_partial” frente a “sin el extra… documenta que las claves pueden faltar”. Obliga a decidir cuándo se marca `keys_partial` sin pglast.
5. “Si pglast no puede parsear una sentencia… el hecho de la tabla lleva attrs.keys_partial true”. En `ALTER TABLE` no siempre hay hecho de tabla; obliga a inventar dónde adjuntarlo.

## DRY-RUN
Lecturas: TaskDoc, parche `runs/subagents/20261116-exec-k2-c2/executor-diff-c4-c2.patch`, resúmenes de testers, `lang_sql.py`, `sql_readers.py`, tests, `pyproject.toml`, `uv.lock`, `CHANGELOG.md`. Cambios previstos: aplicar parche; añadir extra `postgres` con `pglast>=7`; crear módulo que parsee cada `CREATE/ALTER TABLE` con pglast usando offsets de tree-sitter; emitir constraints y attrs; fallback a tree-sitter con `keys_partial`; retirar lectura textual de claves; ampliar fixtures/tests; documentar límites. Dependencias: pglast/libpg_query, tree-sitter, `ids.py`, `uv lock`. Validaciones futuras: los seis comandos de `Validation`, con y sin `--extra postgres`. Sin ejecutar nada.

## FUTURO
El ejecutor producirá parche, commit, CHANGELOG y aviso a IR. Un humano/supervisor decidirá conflictos del parche, cobertura exacta de bordes y aceptación. IR consumirá los facts; el runner reportará validaciones.
