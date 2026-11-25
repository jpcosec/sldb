## REFORMULACION
Propósito: ampliar `sldb.code` para leer TS, TSX, JS y JSX con un único reader (`lang_ts.py`) sobre `tree-sitter-typescript` como extra `code`, publicando hechos con la misma forma que Python y anclas `code:<ruta>::<qualified_name>`. Resultado: runtime y scanner despachados por extensión; componentes, hooks, tipos, funciones, módulo, imports, JSDoc, fingerprints y reconexión; `parse_code_ref` y `recorded_with` actualizados; fixtures y tests; CHANGELOG, commit y aviso a IR. Repo: SLDB_1. Límites: no mapear a dominio specIR; no reimplementar fuera de `sldb.code` salvo el registro de extensiones; SQL queda en la tarea hermana; la salida de `.py` no cambia (`NORMALIZATION` igual).

## AMBIGUEDADES
1. Alcance contradictorio sobre SQL: «Alcance: TS/TSX (...) y SQL (tablas, columnas, vistas, DDL y migraciones)» frente a «esta tarea cubre TS y TSX; SQL va en la tarea hermana». Obligaría a inventar si SQL entra aquí o no.
2. Lista de archivos incompleta: «files: ... src/sldb/code/runtime.py, src/sldb/code/scan.py...» no incluye `lang_ts.py`, aunque el Implementation Path lo exige. Obligaría a decidir si `files` es taxativa.
3. Detección de componentes: «component (función o const que devuelve JSX, nombre en mayúscula)». Obligaría a inventar si cubre arrows, `memo`/`forwardRef`, exports por defecto o JSX anidado.
4. JSDoc: «el comentario JSDoc /** */ inmediatamente anterior». Obligaría a inventar qué separa “inmediatamente” (línea en blanco, decoradores, varios comentarios) y a qué nodo se adjunta.
5. Sufijo por colisión: «si a.ts y a.js coexisten (...) el segundo en orden alfabético de ruta completa lleva el sufijo ~2». Obligaría a fijar el orden exacto y el alcance del sufijo.
6. Tests TS: «tests ... se saltan sin la gramática» frente a que Done When exige registrar un ancla TSX. Obligaría a decidir si el skip valida el cierre.

## DRY-RUN
Lecturas hipotéticas: `pyproject.toml`, `uv.lock`, `runtime.py`, `scan.py`, `code_ref.py`, `record_anchor.py`, `tests/api/test_anchors.py`, `tests/selfdoc/test_treesitter_symbols.py`, y módulos de facts, fingerprints, ids, imports y readers. Cambios previstos: dependencia y lock; runtime por extensión; nuevo `lang_ts.py` con query, readers e imports; dispatch en `scan_file`/`find_files`; extensiones en `parse_code_ref`; gramática en `recorded_with`; fixtures y tests. Dependencias: `tree-sitter-typescript>=0.23` (0.23.2 en PyPI), `Ids`, forma de `facts`, `fingerprints`. Validaciones futuras: los siete comandos de Validation, de menor a mayor, más estados intact/changed/lost/reconnected y comprobación de que `.py` no cambia. Sin ejecutar nada.

## FUTURO
La tarea hermana SQL depende de esta. Un humano/coordinador decide el alcance SQL, los cambios ajenos de `uv.lock` y el commit. IR recibe el aviso por `deskops message send`.
