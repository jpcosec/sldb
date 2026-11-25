## REFORMULACION
Nodo ejecutable `task.code`. Propósito: ampliar `sldb.code` para leer `.ts`, `.tsx`, `.js` y `.jsx` con un único reader (`lang_ts.py`) sobre `tree-sitter-typescript`, publicando hechos de fuente con la misma forma que Python y habilitando anclas `code:<ruta>.<ext>::<símbolo>`. Resultado: readers, facts, fingerprints, ids, imports, `scan` por extensión, `parse_code_ref` y `recorded_with`; la salida `.py` no cambia. Repo: `/mnt/ssd/proyectos/SLDB_1`. Límites: sin mapeo a dominio (specIR); no reimplementar fuera de `sldb.code` salvo el registro de extensiones en `code_ref` y `record_anchor`; SQL queda en la tarea hermana; gramáticas en el extra `code`.

## AMBIGUEDADES
1. Alcance contradictorio: «Alcance: TS/TSX (…) y SQL (tablas, columnas, vistas, DDL y migraciones)» frente a «SQL va aparte» y «SQL lo hace la tarea hermana». Obligaría a inventar si el ejecutor implementa SQL.
2. «si a.ts y a.js coexisten en la misma carpeta, el segundo en orden alfabético de ruta completa lleva el sufijo ~2, como hace Ids»: no define «Ids» ni el algoritmo exacto; obligaría a inventar la desambiguación.
3. «component (función o const que devuelve JSX, nombre en mayúscula)»: no cubre arrow functions, retornos condicionales ni reexports; obligaría a inventar la heurística.
4. «el comentario JSDoc /** */ inmediatamente anterior»: no aclara líneas en blanco, decoradores ni `export`; obligaría a inventar la distancia válida.
5. «--frozen» en Validation con un `uv.lock` que debe cambiar por `tree-sitter-typescript`: obligaría a inventar si se regenera el lock antes o se ejecuta sin `--frozen`.
6. «la ruta sin extensión» del módulo: no fija la raíz (repo, `src`, cwd); obligaría a inventar la base del `qualified_name`.
7. «reconnected al moverla»: no distingue mover el símbolo dentro del archivo de renombrar/mover el archivo; obligaría a inventar la semántica.
8. «los readers» (plural) frente a «un mismo reader (lang_ts.py)» (singular).

## DRY-RUN
Lecturas: task doc, `pyproject.toml`, `uv.lock`, `runtime.py`, `scan.py`, `code_ref.py`, `record_anchor.py`, tests y fixtures. Cambios previstos: dependencia y lock; runtime por gramática/extensión; nuevo `lang_ts.py` con query, readers e imports; dispatch y `find_files`; `parse_code_ref` y `recorded_with`; fixtures TSX/JS/JSX y tests condicionados. Dependencias: `tree-sitter-python` existente, `tree-sitter-typescript`, `uv`, helpers de Ids/fingerprints. Validaciones futuras: los siete comandos de Validation, más CHANGELOG, commit y aviso deskops.

## FUTURO
El coordinador decide cómo commitear `uv.lock` si hay cambios ajenos; la tarea SQL depende de esta; IR recibe aviso; specIR mapea a dominio en otro nodo; humano/CI valida los comandos.
