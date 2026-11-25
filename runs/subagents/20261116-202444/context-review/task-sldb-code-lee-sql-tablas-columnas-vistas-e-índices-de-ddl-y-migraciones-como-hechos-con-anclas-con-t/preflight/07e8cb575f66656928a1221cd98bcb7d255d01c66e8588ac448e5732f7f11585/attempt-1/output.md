## REFORMULACION
No es un agregado: es una tarea ejecutable. Propósito: que `sldb.code` lea DDL y migraciones SQL y publique tablas, columnas, vistas e índices como hechos anclables, igual que Python/TS. Resultado: extra `code` con `tree-sitter-sql>=0.3`, `lang_sql.py`, dispatch `.sql`, `code_ref` con `.sql`, fixtures Postgres, tests de anclas y CHANGELOG. Repo: `SLDB_1`. Límites: sin `ALTER TABLE`, sin estado acumulado entre migraciones, sin dialectos fuera de la gramática y sin TS/TSX, que pertenece a la tarea dependiente.

## AMBIGUEDADES
1. “docstring: un comentario -- inmediatamente anterior a la sentencia” y “columnas como hijos de su tabla”: no dice si las columnas heredan docstring ni cómo unir varias líneas `--`; obliga a inventar asociación y concatenación.
2. “la segunda lleva el sufijo ~2”: no define alcance del sufijo —tabla, columnas, índices— ni qué pasa en la tercera repetición; obliga a inventar unicidad.
3. “se salta con un hecho menos, nunca con error”: no aclara si se omite la sentencia completa o solo el elemento no reconocido; obliga a inventar granularidad del descarte.
4. “code:<ruta>.sql::<tabla>” frente a “conserva el esquema si viene escrito”: no dice si el ancla usa `public.users` o `users`; obliga a inventar la forma canónica.
5. “una migración de dos tablas y una vista” frente a “una vista materializada”: no aclara si cubre `CREATE VIEW`, `CREATE MATERIALIZED VIEW` o ambas; obliga a inventar cobertura.

## DRY-RUN
Lecturas hipotéticas: cierre de la tarea dependiente, módulo TS existente, `runtime.py`/`scan_file`, `code_ref.py`, `pyproject.toml`, `uv.lock`, fixtures y tests. Cambios previstos: dependencia y lock; `lang_sql.py`; registro `.sql` en dispatch, `find_files` y `code_ref`; fixtures Postgres; tests de `intact/changed/lost/reconnected`; CHANGELOG. Dependencias: gramática instalada, base TS/TSX cerrada y fixtures válidos. Validaciones futuras: los cinco comandos de Validation y los tests nuevos de anclas SQL, sin ejecutar ahora.

## FUTURO
La tarea dependiente produce el runtime por lenguaje y TS/TSX. El ejecutor futuro generará commit y aviso a IR; un humano o nodo de cierre validará y cerrará.
