## REFORMULACION

Encargo: en el repo SLDB_1, ampliar el lector de código `sldb.code` para que escanee `.sql` y publique hechos de tablas, columnas, vistas e índices con la misma forma que Python/TS, con anclas `code:<ruta>.sql::<tabla>` y `::<tabla>.<columna>` reconocibles por `check_anchors` (intact/changed/lost/reconnected). Resultado: extra `code` con `tree-sitter-sql`, `lang_sql.py` nuevo (queries y readers de CREATE TABLE/VIEW/INDEX, columnas hijas, `qualified_name` `<tabla>`/`<tabla>.<columna>`, sufijo `~2` en tablas repetidas, docstring desde `--` previo, kinds table/column/view/index/module), dispatch por extensión y `find_files`/`code_ref` aceptando `.sql`, fixtures y tests, CHANGELOG. Límites: sin ALTER TABLE, sin estado acumulado entre migraciones (cada archivo aislado), sin dialectos fuera de la gramática, sin TS/TSX (tarea previa de la que depende). Cierre: Validation en verde, anclas recorriendo los cuatro estados, CHANGELOG+commit, aviso a IR en result-summary.md.

## AMBIGUEDADES

1. «Con el extra code instalado» y «agregar tree-sitter-sql>=0.3 … 0.3.13 está en PyPI»: no fija si el pin es `>=0.3` o `==0.3.13`; obliga a inventar la política de versión.
2. «la segunda lleva el sufijo ~2, como ya hace Ids»: remite a un módulo `Ids` no descrito; obliga a inventar su algoritmo exacto (`~2`, `~3`, alcance por archivo).
3. «un comentario -- inmediatamente anterior a la sentencia»: no define tolerancia (línea en blanco, varios `--`, comentario dentro de CREATE); obliga a inventar la regla.
4. «tests … que se saltan sin la gramática»: no indica mecanismo (`importorskip`, marcador, fixture); obliga a inventarlo.
5. «aviso a IR anotado en result-summary.md (IR no está en el registro)»: no dice formato ni destinatario; obliga a inventar el canal.
6. «Esperar a que la tarea de TS/TSX esté cerrada»: no define cómo verificar ese cierre; obliga a inventar el criterio.

## DRY-RUN

Lecturas: `pyproject.toml`, `uv.lock`, `src/sldb/code/runtime.py`, `models/code_ref.py`, módulo lang TS resultante, tests citados. Cambios previstos: dependencia + lock; `lang_sql.py`; dispatch/`find_files`/`code_ref` con `.sql`; fixtures en `tests/fixtures/treesitter/`; tests de anclas; CHANGELOG. Dependencias: tarea TS/TSX cerrada (infraestructura de dispatch). Validaciones futuras: los cinco comandos de Validation, sin ejecutarlos ahora.

## FUTURO

La tarea TS/TSX debe cerrarse y dejar su dispatch legible; un humano verifica el cierre, aprueba el aviso a IR y el commit; IR (fuera del registro) recibe el result-summary.
