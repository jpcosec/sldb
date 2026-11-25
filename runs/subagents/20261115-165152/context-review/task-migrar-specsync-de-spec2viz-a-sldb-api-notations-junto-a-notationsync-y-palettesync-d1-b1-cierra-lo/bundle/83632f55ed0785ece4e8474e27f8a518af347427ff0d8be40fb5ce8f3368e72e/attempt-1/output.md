## REFORMULACION

Propósito: migrar el `SpecSync` ya existente desde el módulo `sldb_sync` de spec2viz al paquete de notaciones de `sldb.api`, junto a `NotationSync` y `PaletteSync`, reutilizando `StoreWriter` y `SyncReport` de sldb. Resultado: API pública y comando CLI de notations que reconcilian un conjunto de specs creando, actualizando y borrando `SpecDoc`, `SpecNodeDoc` y `RelationDoc`, con informe; tests portados a sldb contra store real y paridad de salida con spec2viz. Repo destino: sldb; origen: repo hermano spec2viz. Límites: migrar, no reescribir; spec2viz no se retira en este encargo; validaciones indicadas en el TaskDoc.

## AMBIGUEDADES

1. “el paquete de notaciones de sldb.api donde ya viven NotationSync y PaletteSync” y “Exponerlo como API pública y en la CLI de notations”: no fija ruta exacta, nombres públicos, firmas ni sintaxis CLI; obligaría a inventar la superficie.
2. “en spec2viz hay una copia propia de _StoreWriter y SyncReport: converger en la de sldb”: no aclara si este encargo modifica o elimina esa copia en spec2viz; obligaría a inventar el alcance sobre el repo hermano.
3. “lo que use de test_catalog_notation” y “contra un store real y sin mocks”: no enumera tests ni define fixture/ubicación del store; obligaría a inventar selección e infraestructura.
4. “la misma salida que spec2viz sobre los mismos specs”: no fija formato exacto ni casos de paridad; obligaría a inventar el criterio.
5. “D1, B1”: solo B1 se explica; D1 no se define; obligaría a inventar su significado y aceptación.

## DRY-RUN

Lecturas: Board, TaskDoc, rituales, paquete de notaciones de `sldb.api`, módulo `sldb_sync` de spec2viz y tests citados; estado git. Cambios previstos: portar `SpecSync` y auxiliares, adaptar imports, reutilizar `StoreWriter`/`SyncReport`, exponer API y CLI, portar tests. Dependencias: APIs existentes de sldb y acceso al repo spec2viz. Validaciones futuras: pytest por archivo con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check`. No es agregado; no se ejecuta nada.

## FUTURO

Un nodo ejecutor producirá la migración, tests portados y evidencia de paridad. Un humano decidirá ruta/API/CLI, alcance sobre spec2viz y fixture de store; closeout verificará commit y árbol limpio.
