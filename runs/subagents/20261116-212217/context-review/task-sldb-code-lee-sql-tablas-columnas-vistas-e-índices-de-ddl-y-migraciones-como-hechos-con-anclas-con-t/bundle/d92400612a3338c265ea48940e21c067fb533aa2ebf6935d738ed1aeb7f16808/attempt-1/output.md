REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: extender `sldb.code` para leer DDL y migraciones SQL de PostgreSQL y publicar hechos de tablas, columnas, vistas e índices con anclas `code:<ruta>.sql::<qualified_name>`. Resultado: `tree-sitter-sql>=0.3` en el extra `code`, nuevo `lang_sql.py`, `.sql` en dispatch/`find_files`/`code_ref`, fixtures y tests de anclas, CHANGELOG. Repo: `/mnt/ssd/proyectos/SLDB_1`, paquete `sldb`. Límites: sin `ALTER TABLE`, sin estado acumulado entre migraciones, sin dialectos fuera de la gramática, sin TS/TSX.

AMBIGUEDADES
1. «las columnas como hijos de su tabla» y «CREATE VIEW y CREATE MATERIALIZED VIEW (kind view)»: no se especifica si las columnas de vistas o vistas materializadas se publican como hechos `column`; obligaría a inventar si se emiten, su `qualified_name` y su ancla.
2. «Las vistas y los índices también se anclan […] los tests de intact/changed/lost/reconnected se exigen sobre tabla y columna»: no aclara si vistas e índices deben cubrir los cuatro estados o solo registrarse/anclarse; obligaría a inventar la cobertura exigida.

DRY-RUN
Lecturas: TaskDoc, rituales `execution`, `testing` y `closeout`, átomo ligado, `pyproject.toml`, `uv.lock`, `runtime.py`, `code_ref.py`, tests nombrados y la implementación dejada por B2. Cambios previstos: añadir `tree-sitter-sql>=0.3` al extra `code`; regenerar `uv.lock`; crear `lang_sql.py` con query y readers de `CREATE TABLE`, `CREATE VIEW`/`CREATE MATERIALIZED VIEW` y `CREATE INDEX`, columnas hijas, `qualified_name`, sufijos `~n`, docstring `--` y `kind`; registrar `.sql` en dispatch, `find_files` y `code_ref`; añadir fixtures y tests; actualizar CHANGELOG. Dependencias: B2 cerrada, con dispatch y `code_ref` generalizados, y gramática instalable. Validaciones futuras: los cinco comandos de Validation y `check.sh --fast`. Sin ejecutar nada.

FUTURO
B2 entrega la infraestructura por lenguaje; el ejecutor implementa y valida; closeout produce commit, CHANGELOG y aviso a IR; IR09 queda desbloqueado.
