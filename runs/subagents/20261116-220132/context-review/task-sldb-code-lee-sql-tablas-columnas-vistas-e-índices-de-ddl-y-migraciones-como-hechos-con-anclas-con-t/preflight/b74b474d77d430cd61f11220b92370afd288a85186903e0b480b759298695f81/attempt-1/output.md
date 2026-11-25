REFORMULACION
Propósito: que sldb.code extraiga de DDL y migraciones Postgres hechos de tablas, columnas, vistas e índices, anclados como `code:<ruta>.sql::<qualified_name>`, reutilizando el runtime y dispatch que dejó B2. Resultado: extra `code` con `tree-sitter-sql>=0.3` y `uv.lock` regenerado; `lang_sql.py` con queries y readers; `.sql` en dispatch, `find_files` y `code_ref`; fixtures; tests de anclas; CHANGELOG. Repo: `/mnt/ssd/proyectos/SLDB_1`, tocando `pyproject.toml`, `uv.lock`, `src/sldb/code/runtime.py`, `src/sldb/models/code_ref.py`, `tests/api/test_anchors.py`, `tests/selfdoc/test_treesitter_symbols.py` y `CHANGELOG.md`. Límites: solo PostgreSQL; sin `ALTER TABLE` ni estado acumulado entre migraciones; sin dialectos no soportados; TS/TSX queda fuera.

AMBIGUEDADES
1. «kind: table, column, view, index, module»: no se define qué nodo genera `kind module` ni cuándo; obligaría a inventar un hecho de módulo SQL.
2. «aviso a IR por deskops message send --desk-root a su desk»: no se indica el valor de `--desk-root` ni el desk destinatario; obligaría a inventar el destino.
3. «una migración generada con sqlmigrate de Django para Postgres»: no fija tablas, campos ni contenido literal; obligaría a inventar el DDL del fixture.
4. «find_files incluye .sql solo si la gramática está»: no define cómo detectar disponibilidad; obligaría a inventar el mecanismo (import, capability u otro).
5. «la segunda lleva el sufijo ~2, como ya hace Ids con nombres repetidos»: no aclara si la repetición se cuenta tras normalizar comillas; obligaría a inventar el orden de normalización y sufijado.

DRY-RUN
Un ejecutor leería primero el cierre de B2 (runtime, `scan_file`, `parse_code_ref`), `pyproject.toml`, el reader TS y `code_ref`. Luego añadiría `tree-sitter-sql` al extra `code`, regeneraría `uv.lock`, crearía `lang_sql.py` con queries de `CREATE TABLE`/`VIEW`/`MATERIALIZED VIEW`/`INDEX` y readers, registraría `.sql` en dispatch, `find_files` y `code_ref`, añadiría fixtures y tests, y documentaría límites en docstring y CHANGELOG. Dependencias: gramática instalada y API generalizada de B2. Validaría con los cinco comandos listados, sin ejecutarlos aquí.

FUTURO
B2 entrega dispatch y `parse_code_ref` generalizados; un ejecutor posterior implementa y corre validaciones; un humano resuelve las ambigüedades, hace commit y envía el aviso a IR. La tarea desbloquea IR09.
