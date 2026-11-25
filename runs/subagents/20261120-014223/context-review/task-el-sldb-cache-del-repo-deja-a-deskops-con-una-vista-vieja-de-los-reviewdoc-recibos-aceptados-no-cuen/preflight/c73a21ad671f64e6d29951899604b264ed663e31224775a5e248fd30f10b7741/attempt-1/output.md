## REFORMULACION

**Propósito:** corregir la regresión por la que `.sldb_cache` deja a deskops con una vista vieja de los ReviewDoc: recibos aceptados en disco no activan la tarea (`rule-activation-task-code`, `seen: {}`).

**Resultado:** tras escribir, actualizar o disponer un documento por API/CLI —en particular `deskops review dispose`— toda lectura posterior (`select_documents`, reglas, `edges_holding`, `deskops next`) ve el estado nuevo sin borrar `.sldb_cache` a mano; una caché vieja se invalida sola y `sldb stores build` deja la caché coherente.

**Repo:** `/mnt/ssd/proyectos/SLDB_1/sldb`.

**Límites:** dentro, la caché causante (`document_rows_disk.py` y/o composición del índice de aristas en `src/sldb/store/edge_index/`), su clave de invalidación, tests en `tests/api/` y CHANGELOG. Fuera: deskops; si el fallo está ahí, el ejecutor lo informa.

Nodo ejecutable (`task.debug`), no agregado.

## AMBIGUEDADES

1. «la caché que dé la vista vieja (document_rows_disk.py y/o la composición del índice de aristas en src/sldb/store/edge_index/)»: «y/o» no fija el componente; obliga a inventar el diagnóstico y el alcance real.
2. «Sospecha: la caché de filas de documentos de d3568eea (...) o la caché compuesta del índice de aristas de H11»: dos sospechas sin confirmar; obliga a elegir sin evidencia.
3. «si el fallo resulta estar en deskops, el ejecutor lo informa»: no define canal ni formato; obliga a inventar el reporte.
4. «deskops next de la tarea de sldb move en el repo real»: no da ruta/checkout ni id de esa tarea; obliga a inventar cuál es.
5. «que cuente lo que cambia en una reescritura in place»: no especifica señal (mtime, tamaño, hash); obliga a inventar la clave.

## DRY-RUN

**Lecturas:** TaskDoc, `runs/subagents/20261120-repro-cache-recibos/repro.log`, `document_rows_disk.py`, `src/sldb/store/edge_index/`, `tests/api/test_select_documents_disk.py`, CHANGELOG y camino de escritura/`review dispose`.

**Cambios previstos:** reproducir en repo temporal; test de regresión que falle antes; ajustar clave de invalidación o invalidar en escritura; hacer que `stores build` regenere/invalide; CHANGELOG.

**Dependencias:** escritura in-place y stores enlazados; cachés d3568eea/H11; deskops solo como lectura.

**Validaciones futuras:** el pytest indicado, `bash tools/check.sh --fast`, suite completa y `deskops next` en repo real. Sin ejecutar nada.

## FUTURO

El integrador corre la suite completa y la de deskops; un humano confirma repo/tarea reales y decide si el fallo es de deskops; revisión de CHANGELOG y commit con Task-Id.
