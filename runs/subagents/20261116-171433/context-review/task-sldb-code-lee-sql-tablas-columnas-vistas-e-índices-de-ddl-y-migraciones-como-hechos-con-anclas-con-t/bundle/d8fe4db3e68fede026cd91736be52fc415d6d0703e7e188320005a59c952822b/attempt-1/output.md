## REFORMULACION
Propósito: que `sldb.code` lea DDL y migraciones `.sql` con `tree-sitter-sql` y publique tablas, columnas, vistas e índices como hechos anclables (`code:<ruta>.sql::<tabla>` o `::<tabla>.<columna>`), con estados `intact/changed/lost/reconnected`. Resultado: módulo `lang_sql.py`, extra `code` con `tree-sitter-sql>=0.3`, `uv.lock` regenerado, dispatch/`find_files`/`code_ref` aceptando `.sql`, fixtures, tests y `CHANGELOG.md`. Repo: `structuredLanguageDB` en `/mnt/ssd/proyectos/SLDB_1`. Límites: depende de la tarea TS/TSX; fuera `ALTER TABLE`, estado acumulado entre migraciones, dialectos no reconocidos y TS/TSX.

## AMBIGUEDADES
1. «Esperar a que la tarea de TS/TSX esté cerrada y leer cómo quedó el dispatch por lenguaje»: el bundle no incluye su resultado ni `scan_file`/`find_files`; obligaría a inventar esa interfaz y el runtime multigramática.
2. «un módulo nuevo lang_sql.py ... con la query y los readers»: no hay módulo TS de referencia ni capturas definidas; obligaría a inventar nombres de captura y estructura.
3. «qualified_name: <tabla> y <tabla>.<columna>» y «la segunda lleva el sufijo ~2»: no aclara colisiones de columnas ni el id del módulo `.sql`; obligaría a inventar reglas de unicidad.
4. «docstring: un comentario -- inmediatamente anterior a la sentencia»: no define comentarios multilínea, líneas en blanco ni comentarios internos; obligaría a inventar el criterio.
5. «con las columnas como hijos de su tabla»: no dice si constraints (`PRIMARY KEY`, `FOREIGN KEY`) cuentan como columnas.
6. «check_anchors la informa intact, changed, lost o reconnected»: no define qué comparar en SQL ni cómo reconectar renombres; obligaría a inventar huella e identidad.
7. «find_files incluye .sql solo si la gramática está»: no indica cómo detectarlo; obligaría a inventar la comprobación.

## DRY-RUN
Lecturas: `pyproject.toml`, `runtime.py`, `code_ref.py`, tests y rituales listados, y la tarea TS/TSX cerrada. Cambios previstos: dependencia en el extra `code`, `uv.lock`, nuevo `lang_sql.py`, registro `.sql` en runtime/dispatch/`find_files`, `code_ref`, fixtures en `tests/fixtures/treesitter/`, tests de estados y `CHANGELOG.md`. Dependencias: `tree-sitter-sql` y el dispatch de la tarea B2. Validaciones futuras: los cinco comandos de Validation. Sin ejecutar nada.

## FUTURO
Otro nodo debe cerrar la tarea TS/TSX y entregar el dispatch real; un humano decide el vocabulario de capturas y aprueba fixtures; el cierre, commit y aviso a IR quedan fuera de este nodo.
