## REFORMULACION

Nodo ejecutable (`task.debug`), no agregado ni paquete. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Propósito: corregir la regresión por la que `.sldb_cache` deja a deskops con una vista vieja de los ReviewDoc y los recibos aceptados no activan la tarea. Resultado: tras escribir, actualizar o disponer un documento por API/CLI, toda lectura posterior (`select_documents`, reglas, `edges_holding`, `deskops next`) ve el estado nuevo sin borrar la caché a mano; una caché vieja se invalida sola y `sldb stores build` deja la caché coherente. Límites: dentro, `document_rows_disk.py` y/o composición del índice de aristas (`src/sldb/store/edge_index/`), clave de invalidación, tests en `tests/api/` y CHANGELOG; fuera, deskops: no se toca y, si el fallo está allí, se informa.

## AMBIGUEDADES

1. «probar con el patrón exacto del repro.log»: el bundle no incluye `runs/subagents/20261120-repro-cache-recibos/repro.log`; si la reproducción simple no falla, el ejecutor tendría que inventar stores enlazados, ReviewDoc e inverso `^subject`.
2. «document_rows_disk.py y/o la composición del índice de aristas»: no hay criterio previo para elegir; el ejecutor debe inventar cuál es la caché culpable si la reproducción no lo aísla.
3. «arreglar la clave de invalidación […] o invalidar explícitamente en el camino de escritura»: faltan criterios de elección (rendimiento, arquitectura, riesgo); el ejecutor tendría que decidir por su cuenta.
4. «sin quitar la caché»: no define si se permite desactivarla temporalmente en tests o bajo una bandera; obligaría a inventar el alcance del arreglo.

## DRY-RUN

Lecturas previstas: Board, este TaskDoc, rituales de ejecución/testing/closeout, pills/átomos ligados (vacíos), `repro.log`, `document_rows_disk.py`, composición del índice de aristas, caminos de escritura/API, test nombrado y CHANGELOG. Cambios previstos: reproducir en repo temporal; añadir test que falle antes; corregir clave de invalidación o invalidar en escritura; hacer que `stores build` regenere/invalide; actualizar CHANGELOG; commit atómico con rutas nombradas y `Task-Id`. Dependencias: contenido del repro, API de escritura real, tests existentes. Validaciones futuras: el pytest indicado, `bash tools/check.sh --fast`, suite completa, `stores check`/`check_claims` si aplica.

## FUTURO

El integrador ejecuta la suite completa de sldb y la de deskops; un humano o nodo externo verifica `deskops next` en el repo real y decide si el fallo pertenece a deskops. Closeout y auditoría de git corresponden al flujo de cierre.
