## REFORMULACION

**Propósito:** ampliar `sldb.code` para leer TS/TSX con `tree-sitter-typescript` como extra opcional, publicar hechos de fuente y soportar anclas, reutilizando la maquinaria de Python y sin mapear a dominio.

**Resultado:** runtime por extensión; módulo `lang_ts.py` con query, readers, JSDoc e imports; `scan_file`/`find_files` con `.ts`/`.tsx`; `parse_code_ref` y `record_anchor` adaptados; fixtures y tests de estados de ancla.

**Repo:** `/mnt/ssd/proyectos/SLDB_1`, paquete `sldb` y archivos listados en `files`.

**Límites:** esta tarea cubre TS/TSX; SQL corresponde a la tarea hermana según Precisiones; no duplicar Python; no mapear conceptos de dominio; las gramáticas siguen siendo extras opcionales; no cambiar NORMALIZATION si la salida `.py` no cambia.

## AMBIGUEDADES

1. «El paquete sldb.code lee TS/TSX y SQL» / «esta tarea cubre TS y TSX; SQL va en la tarea hermana» / «Fixtures reales de TSX y de SQL producen hechos...». Obligaría a inventar si SQL, sus fixtures y validaciones entran o no en este nodo.
2. «SQL va en la tarea hermana que depende de esta» frente a `depends_on: []`. Obligaría a inventar si existe dependencia real y el orden de ejecución.
3. «ver el atom del inventario de código como hechos de fuente» frente a `atoms: []`. Obligaría a inventar la forma exacta de los hechos y su correspondencia TS/TSX.

## DRY-RUN

**Lecturas previstas:** TaskDoc, `pyproject.toml`, `uv.lock`, `runtime.py`, `scan.py`, `code_ref.py`, `record_anchor.py`, tests y fixtures existentes, `CHANGELOG.md`; buscaría el atom referido, ausente en el input.

**Cambios previstos:** añadir extra y lock; runtime por extensión; nuevo `lang_ts.py`; dispatch y `find_files`; aceptar `.ts`/`.tsx`; `recorded_with`; fixtures y tests intact/changed/lost/reconnected.

**Dependencias:** `tree-sitter-typescript>=0.23`, `uv`, extras `code`/`dev`; suite existente de Python.

**Validaciones futuras:** los siete comandos de Validation y `stores build --check` citado en Done When; comprobar funcionamiento sin extras.

## FUTURO

La tarea hermana ejecutará SQL. El coordinador decidirá cómo commitear `uv.lock` si hay cambios ajenos. Un humano o la planificación resolverá las ambigüedades 1–3 antes de ejecutar; la aceptación final corresponde al humano.
