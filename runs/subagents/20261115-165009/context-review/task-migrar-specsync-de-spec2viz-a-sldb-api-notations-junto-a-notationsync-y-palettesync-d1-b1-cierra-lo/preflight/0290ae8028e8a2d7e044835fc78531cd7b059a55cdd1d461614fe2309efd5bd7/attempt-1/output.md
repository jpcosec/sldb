## REFORMULACION
Nodo ejecutable `task.code`. Propósito: migrar a SLDB la capacidad existente de `SpecSync` para reconciliar un conjunto de specs. Resultado: `SpecSync` disponible como API pública y en la CLI de notaciones de SLDB, reutilizando `StoreWriter` y `SyncReport`, con tests portados y paridad funcional. Repo destino: SLDB, en el paquete de notaciones de `sldb.api`; origen: repo hermano spec2viz. Límites: migrar, no reescribir; no retirar spec2viz; tests contra store real y sin mocks; no duplicar `StoreWriter` ni `SyncReport`.

## AMBIGUEDADES
1. “el paquete de notaciones de sldb.api donde ya viven NotationSync y PaletteSync”: no fija ruta exacta ni nombres de exportación; obligaría a inventar ubicación y superficie pública.
2. “reutilizando su StoreWriter y SyncReport”: no define constructores, visibilidad ni compatibilidad; obligaría a inventar la adaptación.
3. “Exponerlo como API pública y en la CLI de notations”: no fija comando, flags ni formato de salida; obligaría a inventar el contrato CLI.
4. “la misma salida que spec2viz sobre los mismos specs”: no aclara si es byte a byte, orden o campos del informe; obligaría a inventar el criterio de paridad.
5. “los tests de spec2viz de esta pieza se portan”: menciona `test_sldb_sync` y “lo que use de test_catalog_notation”, pero no delimita el conjunto; obligaría a inventar la frontera.
6. “reconciliar borrando lo que salió del conjunto”: no define qué constituye el conjunto, tratamiento de huérfanos ni alcance del borrado; obligaría a inventar semántica destructiva.

## DRY-RUN
Lecturas previstas: TaskDoc, módulo `sldb_sync` y tests de spec2viz, paquete de notaciones de SLDB, `StoreWriter`, `SyncReport`, CLI de notations, `tools/check.sh` y configuración de stores. Cambios previstos: trasladar/adaptar `SpecSync` y símbolos asociados; eliminar la copia local de `_StoreWriter`/`SyncReport` en favor de la de SLDB; exponer API y CLI; portar tests; ajustar informes. Dependencias: código fuente de spec2viz disponible, store real para pruebas, API de notaciones existente. Validaciones futuras: `TMPDIR=/dev/shm pytest -q` por archivo, `tools/check.sh`, `sldb stores build --check` y comparación de salida con spec2viz.

## FUTURO
Un humano u otro nodo debe precisar ruta pública, contrato CLI, criterio de paridad y frontera exacta de tests. El gate IR13 decide la retirada de spec2viz; posteriormente spec2viz podrá importar de SLDB.
