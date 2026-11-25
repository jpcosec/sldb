## REFORMULACION

Encargo ejecutable (`task.code`): añadir `--reindex` a `docs track` para re-indexar desde el archivo un documento ya trackeado en la misma ruta, aplicando las validaciones de un track normal; si el archivo no valida, debe fallar y dejar el índice intacto. Incluye el flag en parser y comando, el parámetro `reindex` en `track_document_file` propagado hasta `StoreOperations.track`, rechazo claro de `--reindex`+`--force`, tests en `tests/api/test_api_documents.py`, CHANGELOG y ayuda. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límite: `--force` no cambia; fuera de alcance cualquier otra modificación.

## AMBIGUEDADES

1. «el camino de force de la tarea CI2»: no se identifica CI2 ni su código; obligaría a inventar qué implementación concreta reutilizar.
2. «deja el índice como estaba» / «byte a byte igual»: no define atomicidad, rollback ni qué se compara; obligaría a inventar el mecanismo.
3. «corre las mismas validaciones que un track normal»: no enumera el conjunto exacto; obligaría a inventar qué validaciones incluir.
4. «sobre un documento no trackeado se comporta como track»: no aclara si equivale exactamente al track normal, con o sin validación adicional; obligaría a inventar la semántica.
5. «aviso a sldb-ui»: sin canal, formato ni responsable; obligaría a inventar la notificación.
6. «commit ... con rutas nombradas y Task-Id»: no fija formato exacto; obligaría a inventar la convención de mensaje.

## DRY-RUN

Lecturas: los cinco `files` listados, parser/comando de `docs track`, tests existentes y camino `--force`. Cambios previstos: flag `--reindex` en `src/sldb/cli/parsers/docs1.py`, comando, parámetro en `track_document_file.py`, paso a `ops.py`, validación mutua, tests, CHANGELOG y `selfdoc sync`. Dependencias: camino force de CI2, generación selfdoc y quick_gates. Validaciones futuras: los cinco comandos de Validation, más `selfdoc check` en 0. Nada ejecutado.

## FUTURO

Un humano decide redacción de CHANGELOG, mensaje de commit y ejecuta el aviso a sldb-ui; otro nodo/CI2 provee el camino `--force`; `selfdoc sync` genera la referencia CLI que deberá commitearse.
