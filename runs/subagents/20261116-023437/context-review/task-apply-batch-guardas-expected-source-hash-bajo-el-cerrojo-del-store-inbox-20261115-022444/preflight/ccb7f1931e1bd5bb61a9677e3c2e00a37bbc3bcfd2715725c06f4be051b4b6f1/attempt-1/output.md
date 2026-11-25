## REFORMULACION
Encargo: modificar `apply_batch` para que tome el cerrojo del store (`StoreIOLock`) durante todo el lote —desde la prevalidación hasta la última escritura— y compruebe los guardas `expected_source_hash` dentro de esa transacción, evitando carreras entre dos procesos. Resultado observable: test de concurrencia con dos procesos reales sobre un store copiado donde el guarda rechaza con `ConflictError` sin escritura parcial; además pytest por archivo, `tools/check.sh` y `sldb stores build --check`. Repo: `sldb`. Límites: solo `apply_batch` y sus guardas; fuera el lote inverso (inbox 20261115-123855), que es prerrequisito dependiente, no parte de este nodo.

## AMBIGUEDADES
1. "## Implementation Path" vacío. Obliga a inventar archivos, funciones y punto exacto de adquisición del cerrojo.
2. "el cerrojo StoreIOLock se toma por escritura de índice" — no se especifica si el cerrojo pasa a ser único por lote o por store; inventaría granularidad y reentrancy.
3. "los guardas se comprueban dentro de la transacción" — no define qué es "transacción" ni si ya existe una abstracción; inventaría API.
4. "test con dos procesos reales sobre un store copiado" — no indica ruta, fixture ni cómo se copia el store; inventaría infraestructura de test.
5. "guarda rechaza como ConflictError" — no cita clase/módulo existente; inventaría import y contrato de error.
6. "uno a la vez" en validación — no aclara orden ni si fallo detiene la secuencia; inventaría criterio de parada.
7. "Prerrequisito del lote inverso (inbox 20261115-123855)" — no dice si este nodo debe esperar algo de ese inbox; inventaría dependencia.

## DRY-RUN
Lecturas hipotéticas: módulo de `apply_batch`, implementación de `StoreIOLock`, prevalidación de guardas, tests de concurrencia existentes, `tools/check.sh`. Cambios previstos: mover adquisición del cerrojo al inicio del lote, pasar guardas a la fase transaccional, adaptar llamadas internas, añadir test multiproceso sobre store copiado. Dependencias: semántica de `StoreIOLock`, contrato `ConflictError`, utilidades de copia de store. Validaciones futuras: pytest por archivo con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check`; sin ejecutar aquí.

## FUTURO
Un ejecutor decide archivos concretos y diseño del test; un humano valida el criterio de "sin escritura parcial" y la coordinación con el inbox 20261115-123855.
