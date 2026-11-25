## REFORMULACION

Propósito: eliminar la carrera entre la comprobación de guardas `expected_source_hash` y la escritura en `apply_batch`. Resultado: `apply_batch` toma el cerrojo del store desde la prevalidación hasta la última escritura, evalúa los guardas dentro del lote y aporta un test con dos procesos que demuestra ausencia de escritura parcial y de guarda saltado. Repo: sldb, workspace `desk`, nodo `ritual-execution`. Límites: solo `apply_batch`, guardas y cerrojo; el lote inverso queda fuera; validación con pytest por archivo (`TMPDIR=/dev/shm`), `tools/check.sh` y `sldb stores build --check`. El TaskDoc está en `draft`, con `files`, `pills`, `atoms` y `depends_on` vacíos.

## AMBIGUEDADES

1. «los guardas se comprueban dentro de la transacción»: no se define “transacción” ni su API; obligaría a inventar semántica transaccional.
2. «el cerrojo StoreIOLock se toma por escritura de índice»: falta módulo, firma y alcance; obligaría a inventar la API del cerrojo.
3. «test con dos procesos que prueba que no hay escritura parcial ni guarda saltado»: sin mecanismo de sincronización ni criterio de éxito; obligaría a inventar el diseño del test.
4. «Pedido del inbox sldb 20261115-022444»: el mensaje no está en el bundle; obligaría a inventar el alcance original.
5. «Prerrequisito del lote inverso (inbox 20261115-123855)»: el mensaje no se aporta y `depends_on: []`; obligaría a inventar la dependencia.
6. «TMPDIR=/dev/shm pytest -q de los archivos tocados»: con `files: []` no hay archivos nombrados; obligaría a inventar la superficie tocada.
7. «ConflictError»: sin ruta ni contrato definido; obligaría a inventar la clase y su mapeo.

## DRY-RUN

Lecturas hipotéticas: TaskDoc, Board, rituales, inbox 022444 y 123855, código de `apply_batch`, `StoreIOLock`, guardas y tests existentes, más `git log`. Cambios previstos: adquirir `StoreIOLock` al inicio del lote y liberarlo al final; mover la prevalidación dentro del cerrojo; comprobar `expected_source_hash` en la fase de aplicación y mapear el fallo a `ConflictError`; añadir un test multiproceso sobre un store copiado. Dependencias: API real de `StoreIOLock`, firma de `apply_batch`, guardas, `ConflictError` y pytest. Validaciones futuras: pytest archivo a archivo con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check` y `tools/check_claims.py` por tocar el store. Nada se ejecuta aquí.

## FUTURO

Otro nodo debe resolver el lote inverso (inbox 123855) y su dependencia; un humano decide si aporta los inbox ausentes, fija la semántica de transacción y aprueba el bind de pills/átomos. El cierre corresponde a `deskops closeout` tras pasar testing.
