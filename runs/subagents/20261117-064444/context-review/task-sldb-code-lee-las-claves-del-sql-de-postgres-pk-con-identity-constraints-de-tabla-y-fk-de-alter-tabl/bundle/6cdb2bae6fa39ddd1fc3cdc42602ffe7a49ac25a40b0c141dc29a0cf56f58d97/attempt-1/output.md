REFORMULACION
Propósito: que `sldb.code` lea las claves del DDL de Postgres con el parser real (pglast, extra opcional `postgres`), sin pérdidas silenciosas sobre SQL válido. Resultado: hechos `constraint` (`primary_key|foreign_key|unique`) con `columns` y `references {table, columns}`; en columnas `attrs.primary_key/unique/identity/type`; `attrs.keys_partial` cuando pglast no parsea; fallback intacto a tree-sitter-sql sin el extra. Repo: SLDB_1, archivos listados en `files` (lang_sql.py, sql_readers.py, tests, pyproject.toml, uv.lock, CHANGELOG). Límites: sin estado acumulado entre migraciones, sin otros dialectos, CHECK/EXCLUDE y demás acciones de ALTER fuera.

AMBIGUEDADES
1. "El diff del intento anterior (runs/subagents/20261116-exec-k2-c2/executor-diff-c4-c2.patch) es el punto de partida": el parche no está en el bundle; obligaría a inventar su contenido o a asumir que existe y aplica limpio.
2. "si pglast no puede parsear una sentencia, se usa lo de tree-sitter y el hecho de la tabla lleva attrs.keys_partial true": no dice si las columnas de esa tabla también llevan `keys_partial` ni si se conservan claves parciales de tree-sitter. Habría que inventar el contrato exacto del fallback.
3. "nombres sin comillas con esquema si viene escrito" aplicado a `references`: no aclara si la tabla referenciada conserva esquema (`public.users`) y si la relación apunta al id con o sin sufijo `~N`. Obligaría a inventar la resolución de nombres.
4. "sufijo ~N por tipo dentro de la tabla" y "con la misma función de ids.py": no define si `pk`, `fk`, `unique` comparten contador ni si `~N` cuenta por tipo o global. Habría que inventar la numeración.
5. "attrs.primary_key/unique/identity/type en la columna": no especifica el formato de `type` (texto crudo, normalizado, con o sin esquema). Obligaría a inventar la normalización.
6. "CHECK y EXCLUDE no son claves (fuera)" frente a "Lo que siga fuera ... va documentado como límite": no queda claro si CHECK/EXCLUDE producen algún hecho o solo se omiten. Habría que inventar el comportamiento.

DRY-RUN
Lecturas: parche del run previo, `lang_sql.py`, `sql_readers.py`, `pyproject.toml`, `uv.lock`, tests y fixtures Django citados, CHANGELOG, `tools/check.sh`. Cambios previstos: aplicar parche (excluyendo CHANGELOG), añadir extra `postgres` con `pglast>=7`, nuevo módulo lector pglast, integración por sentencia con offsets de tree-sitter, eliminar lectura textual de claves, tests de bordes y de fallback, entrada CHANGELOG. Dependencias: `uv lock`, ruedas pglast Linux x86_64/Py3.12-3.13, tree-sitter-sql intacto. Validaciones futuras: los seis comandos de Validation, con y sin `--extra postgres`.

FUTURO
Decide un humano: aprobar la dependencia nueva y el uso del parche de otro run. Otro nodo: ejecución, testing ritual, closeout/commit y aviso a IR.
