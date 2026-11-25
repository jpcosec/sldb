## REFORMULACION
Propósito: que `sldb.code` lea SQL (DDL y migraciones Postgres) y publique tablas, columnas, vistas e índices como hechos con anclas `code:<ruta>.sql::<qualified_name>`, verificables por `check_anchors` (intact/changed/lost/reconnected). Resultado: extra `code` con `tree-sitter-sql>=0.3`, módulo `lang_sql.py`, dispatch `.sql`, `find_files`, `code_ref`, fixtures y tests, CHANGELOG y commit. Repo: SLDB_1. Límites: solo PostgreSQL; sin ALTER TABLE, estado acumulado entre migraciones ni dialectos fuera de la gramática; TS/TSX queda en la tarea dependiente.

## AMBIGUEDADES
1. «Esperar a que la tarea de TS/TSX esté cerrada y leer cómo quedó el dispatch por lenguaje»: no fija la interfaz de runtime/dispatch; obligaría a inventar la API multigramática.
2. «un ancla code:<ruta>.sql::<tabla> o ::<tabla>.<columna> se registra y check_anchors la informa intact, changed, lost o reconnected»: no define anclas de vistas/índices ni candidatos de reconexión SQL; obligaría a inventar su semántica.
3. «docstring: un comentario -- inmediatamente anterior» y «solo las líneas -- contiguas inmediatamente encima»: no dice cómo unir varias líneas ni normalizar espacios; obligaría a inventar el texto.
4. «Si un archivo de migraciones define dos veces la misma tabla, la segunda lleva el sufijo ~2»: no aclara duplicados de columnas ni ámbito exacto; obligaría a inventar reglas de deduplicación.
5. «code_ref acepta .sql», pero `parse_code_ref` solo admite `.py`: no dice si también cambia el parser; obligaría a inventar la validación.

## DRY-RUN
Nodo unitario, no agregado. Lecturas hipotéticas: Board, tarea TS/TSX cerrada, `runtime.py`, `scan.py`, `code_ref.py`, `test_anchors.py`, `test_treesitter_symbols.py`, `pyproject.toml`, `uv.lock`. Cambios previstos: añadir `tree-sitter-sql`, regenerar lock, crear `lang_sql.py` con query y readers, registrar `.sql` en dispatch/`find_files`/`code_ref`, fixtures Postgres, tests de los cuatro estados, CHANGELOG. Dependencias: cierre de la tarea B2 TS/TSX y gramática instalable. Validaciones futuras: los cinco comandos listados en Validation.

## FUTURO
Otro nodo debe cerrar la tarea TS/TSX y fijar el dispatch; un humano decide el commit/closeout y la actualización del Board; IR09 queda bloqueado hasta esta tarea; el aviso a IR se envía tras validar.
