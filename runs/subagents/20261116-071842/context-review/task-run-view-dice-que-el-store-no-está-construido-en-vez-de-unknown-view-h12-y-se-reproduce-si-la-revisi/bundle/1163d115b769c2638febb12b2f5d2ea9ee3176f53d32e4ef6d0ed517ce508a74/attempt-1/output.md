REFORMULACION
Nodo ejecutable `task.debug` en `/mnt/ssd/proyectos/SLDB_1`; no es agregado. Propósito: cerrar dos huecos de `sldb.api.run_view`: H12, que un store con índice compuesto vacío/sin construir dé `SLDBStoreError` con “store index not built: run `sldb stores build`” y no “Unknown view”; H13, determinar con test si la `revision` cambia entre el proceso que escribió y uno nuevo y, si cambia, quitar la dependencia de cachés en memoria. Resultado: cambios en `view_source.py`/`view_revision.py` si procede, dos tests en `tests/api/test_run_view_reads.py`, línea en `CHANGELOG.md` bajo “## 0.1.13 — not released yet” e informe `result-summary.md`. Límites: no H1-H8, no rendimiento, no push; commit y aviso los gestiona el coordinador/deskops.

AMBIGUEDADES
1. “usar la misma señal que stores check usa para store/unbuilt, src/sldb/api/stores/store_surroundings.py” / “reutilizar esa función o su condición, sin copiarla”. El input no incluye el contenido de ese archivo; habría que inventar el nombre exacto de la función o la condición reutilizable.
2. “run_view sobre un store cuyo índice compuesto está vacío o sin construir” y “distinguir índice vacío o sin shards”. No se aclara si un store válido con cero documentos debe considerarse “no construido”; obligaría a inventar esa política.
3. “en un subprocess nuevo (python -c con sldb.api.run_view)” no fija comando, entorno ni cómo evitar heredar cachés; obligaría a inventar el arranque del subprocess.

DRY-RUN
Hipotético, sin ejecutar: leer `view_source.py`, `view_revision.py`, `store_surroundings.py`, `tests/api/test_run_view_reads.py` y `CHANGELOG.md`; localizar helpers/fixtures. Cambios previstos: guarda antes de “Unknown view” reutilizando la señal `store/unbuilt` y `SLDBStoreError`; test H12 que borra `.sldb_cache`; test H13 que escribe, ejecuta en proceso actual y subprocess, compara `revision` y, si difiere, diagnostica `documents/view/rules/shards` leyendo del disco; entrada de CHANGELOG. Dependencias: fixtures existentes, API de stores, entorno de test/subprocess y ausencia de cachés de módulo. Validaciones futuras: los tres `pytest` indicados; revisar informe; commit/aviso fuera del ejecutor.

FUTURO
El ejecutor produce `result-summary.md` con si H13 se reprodujo y qué entrada cambió. El coordinador hace `deskops closeout commit` y el aviso a deskops; si el repo no está registrado, el aviso queda en el informe. H1-H8 y rendimiento pertenecen a otros nodos/tasks.
