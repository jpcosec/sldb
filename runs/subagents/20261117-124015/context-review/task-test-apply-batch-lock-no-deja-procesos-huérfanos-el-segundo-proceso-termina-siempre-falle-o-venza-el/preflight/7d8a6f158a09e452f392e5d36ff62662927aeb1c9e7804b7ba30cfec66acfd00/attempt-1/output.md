## REFORMULACION

El encargo es corregir `tests/api/test_apply_batch_lock.py` en el repo `SLDB_1` (host robocop2) para que ningún proceso lanzado por el test quede huérfano. El resultado esperado: cada proceso termina siempre al salir del test —pase, falle o venza—, la espera de `marks/go` en el hijo tiene un tope, y existe un test que simula un fallo del padre y verifica que no queda ningún hijo vivo. Límites: no modificar `apply_batch` ni `lock.py`.

## AMBIGUEDADES

1. «lanzar los procesos en un contexto que los mata y los espera en finally (o una fixture con yield)»: no se elige entre contexto y fixture; obligaría a inventar el mecanismo concreto.
2. «poner un tope de tiempo a la espera de marks/go»: no se indica duración; obligaría a inventar el valor del timeout.
3. «un test que simula un fallo del padre»: no se define cómo simularlo; obligaría a inventar el método (excepción, kill, salida temprana).
4. «comprobando con ps que no quedan procesos del test»: no se da comando ni filtro; obligaría a inventar el criterio de detección.
5. «commit; aviso a IR»: no se especifica rama, mensaje ni canal de aviso; obligaría a inventar el procedimiento.

## DRY-RUN

Lecturas previas: el TaskDoc, `tests/api/test_apply_batch_lock.py`, helpers/fixtures de procesos y la sugerencia de `desk/inbox/...` si se necesita contexto; `lock.py` solo lectura para entender `marks/go`, sin modificarlo.

Cambios previstos: envolver el lanzamiento de procesos en un context manager o fixture con `yield` que garantice `terminate`/`kill` y `wait` en `finally`; añadir un timeout máximo a la espera de `marks/go` dentro del hijo; añadir un test que fuerce el fallo del padre y compruebe que no quedan hijos.

Dependencias: `pytest`, `subprocess`, utilidades estándar de procesos; no se prevé dependencia nueva.

Validaciones futuras, sin ejecutar: los tres comandos de Validation con `TMPDIR=/dev/shm`; comprobación con `ps` tras el fallo forzado; commit y aviso a IR según Done When.

## FUTURO

La ejecución real de las validaciones, el commit en la rama correspondiente, el aviso a IR y la aceptación o rechazo del cambio corresponden a otro nodo o a un humano. También queda fuera de este preflight decidir si el enfoque de limpieza y el umbral de timeout son aceptables.
