REFORMULACION
Propósito: ampliar sldb.code para leer SQL (DDL y migraciones Postgres que emite sqlmigrate de Django) y publicar hechos de tablas, columnas, vistas e índices anclables como `code:<ruta>.sql::<nombre>`. Resultado: extra `code` con tree-sitter-sql, módulo `lang_sql.py` (query y readers de CREATE TABLE/VIEW/MATERIALIZED VIEW/INDEX, nodo transaction, identificadores entrecomillados, sufijo `~n`, docstring `--`), `.sql` en el dispatch de runtime/find_files/code_ref, fixtures y tests de intact/changed/lost/reconnected, CHANGELOG. Repo: `/mnt/ssd/proyectos/SLDB_1`, paquete `src/sldb`. Límites: ni ALTER TABLE ni estado acumulado entre migraciones; solo lo que la gramática reconoce de Postgres; TS/TSX fuera (tarea B2 previa, de la que depende).

AMBIGUEDADES
1. `files:` enumera `pyproject.toml`, `uv.lock`, `src/sldb/code/runtime.py`, `src/sldb/models/code_ref.py`, `tests/api/test_anchors.py`, `tests/selfdoc/test_treesitter_symbols.py`, `CHANGELOG.md`, pero no `src/sldb/code/lang_sql.py` ni los fixtures nuevos. Obliga a inventar rutas y nombres de los artefactos nuevos.
2. "kind: table, column, view, index, module": no fija el qualified_name ni el id del hecho de módulo del archivo `.sql`. Obliga a inventar esa convención.
3. "con la misma forma que los de Python y TS" no fija `recorded_with`; los tests actuales comparan `"treesitter-symbols/1 (tree-sitter-typescript …, tsx)"`. Obliga a inventar la cadena exacta para SQL.
4. "agregar tree-sitter-sql>=0.3" no indica módulo ni atributo que `runtime.py` debe importar. Obliga a inventar o verificar fuera del bundle los entry points de la gramática.
5. "aviso a IR por deskops message send --desk-root a su desk" no identifica el desk destino. Obliga a inventar la ruta.

DRY-RUN
Lecturas: runtime.py, code_ref.py, scan/anchors, tests citados, pyproject.toml, uv.lock. Cambios previstos: pyproject (extra `code`), uv.lock regenerado, lang_sql.py, GRAMMARS/SUFFIXES/find_files, fixtures, tests, CHANGELOG. Dependencias: gramática instalada (si falta, los tests se saltan) y B2 cerrada. Validaciones futuras: los cinco comandos de la sección Validation.

FUTURO
Cerrar B2 antes de empezar; verificar entry points de tree-sitter-sql en el entorno; decidir el desk destino del aviso; commit y closeout vía deskops.
