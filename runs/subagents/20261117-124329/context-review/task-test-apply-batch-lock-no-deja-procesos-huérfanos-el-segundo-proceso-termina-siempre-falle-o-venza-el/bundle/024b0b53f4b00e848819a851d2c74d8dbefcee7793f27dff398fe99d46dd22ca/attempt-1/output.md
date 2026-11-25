## REFORMULACION
Propósito: evitar que `tests/api/test_apply_batch_lock.py` deje procesos huérfanos cuando el test falla o vence. Resultado: cada proceso lanzado termina siempre al salir del test; la espera de `marks/go` en el hijo tiene un tope; y un test simula el fallo del padre y verifica que no queda ningún hijo vivo. Repo: `SLDB_1` (`sldb`). Límites: solo `tests/api/test_apply_batch_lock.py`; no cambiar `apply_batch` ni `lock.py`. Validaciones exigidas: pytest del test, `test_clean_code_rules.py` y `tools/check.sh --fast`. Es un nodo ejecutable, no un agregado.

## AMBIGUEDADES
1. “poner un tope de tiempo a la espera de marks/go dentro del proceso hijo”: no fija duración ni comportamiento exacto al vencer; obligaría a inventar el timeout y si el hijo debe salir con error o silencio.
2. “un test que simula un fallo del padre y comprueba que no queda ningún hijo vivo”: no define cómo simular el fallo ni cómo comprobar “ningún hijo vivo”; obligaría a inventar el mecanismo (matar el padre, fixture, inspección con `ps`).
3. “aviso a IR”: no indica canal ni formato; obligaría a inventar el destinatario operativo y el medio.

## DRY-RUN
Lecturas previstas: task file, `tests/api/test_apply_batch_lock.py`, átomo enlazado y rituales de ejecución/testing/closeout; revisión de historial git antes de afirmar estado. Cambios previstos: gestionar los `Popen` con fixture/contexto que haga `terminate/kill` y `wait` en `finally`; añadir tope a la espera de `marks/go` en el hijo; añadir un test de fallo del padre con comprobación de procesos vivos. Dependencias: `pytest`, `subprocess`, `sys.executable`, fixture `api_store`, cerrojo del store. Validaciones futuras: los tres comandos indicados y comprobación con `ps` tras forzar un fallo. No se ejecuta nada.

## FUTURO
Otro nodo implementará el cambio; el ritual de testing ejecutará las validaciones; closeout hará commit atómico y `deskops closeout`; se enviará el aviso a IR; el auditor de contexto revisará pills/átomos.
