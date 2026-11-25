## REFORMULACION

TaskDoc ejecutable (no agregado) para ampliar `sldb.code`: leer TS/TSX con tree-sitter-typescript como extra `code`, produciendo readers, facts, fingerprints e ids con la misma forma que Python, y soportar anclas `code:<ruta>.ts|.tsx::<símbolo>` en `record_anchor`/`check_anchors`. Repo: `SLDB_1`; superficies: `pyproject.toml`, `uv.lock`, `src/sldb/code/{runtime,scan}.py`, nuevo `lang_ts.py`, `src/sldb/models/code_ref.py`, `src/sldb/api/anchors/record_anchor.py`, tests y `CHANGELOG.md`. Límites: SQL fuera (tarea hermana); mapeo a dominio fuera (specIR); no duplicar maquinaria Python; salida `.py` sin cambios.

## AMBIGUEDADES

1. «Alcance: TS/TSX [...] y SQL (tablas, columnas, vistas, DDL y migraciones)» contradice «esta tarea cubre TS y TSX; SQL va en la tarea hermana». Obliga a inventar si SQL se implementa aquí o se ignora.
2. «ver el atom del inventario de código como hechos de fuente» cita un atom inexistente (`atoms: []`). Obliga a inventar la forma exacta de los facts.
3. «component (función o const que devuelve JSX, nombre en mayúscula), hook (función cuyo nombre empieza por use)» no fija prioridad si un componente empieza por `use`. Obliga a elegir orden de clasificación.
4. «gramáticas como extras opcionales» frente a «agregar tree-sitter-typescript>=0.23 al extra code». Obliga a decidir si es un extra o varios.
5. «el ejecutor lo anota y deja al coordinador decidir cómo commitear el lock» frente a «CHANGELOG y commit» en Done When. Obliga a decidir quién commitea.
6. «docstring: el comentario JSDoc /** */ inmediatamente anterior» no define líneas en blanco entre comentario y nodo. Obliga a inventar tolerancia.

## DRY-RUN

Lecturas: los archivos listados, más `lang_py`/readers existentes y fixtures actuales. Cambios previstos: dependencia y lock; runtime por extensión con error que nombre el extra; `lang_ts.py` con query, readers, imports; dispatch e inclusión `.ts/.tsx` en `scan`; extensiones en `parse_code_ref`; gramática en `recorded_with`; fixtures y tests con skip sin gramática. Dependencias: instalación de tree-sitter-typescript, runtime tree-sitter existente, red/uv para lock. Validaciones futuras: los siete comandos listados y `tools/check.sh --fast`.

## FUTURO

La tarea SQL depende de esta y decide su alcance. El coordinador decide el commit del lock si está sucio. specIR realiza el mapeo de dominio. Un humano revisa CHANGELOG, commit y aviso a IR.
