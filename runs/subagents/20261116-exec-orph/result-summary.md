# result-summary — deskops-e-cdb27fa3f0f8

Tarea: task-test-apply-batch-lock-no-deja-procesos-huérfanos-… (executor sldb-executor).
Se siguieron las decisiones del coordinador recibidas a mitad de la corrida: (1) fixture con yield, (2) tope de 120 s con salida != 0, (3) fallo simulado con excepción + /proc, (4) ps al final, (5) sin commit ni aviso.

## Cambios (solo tests/api/test_apply_batch_lock.py)
- `CHILD`: la espera de `marks/go` tiene tope `HOLD_LIMIT` (argv[7], 120 s por defecto); al vencer, `sys.exit(3)` (el cerrojo se libera al salir).
- `_processes(api_store, tmp_path)` (nuevo context manager): devuelve `spawn(hold, title, source_hash, hold_limit="120")`, registra cada `Popen` en `spawn.children` y en `finally` mata los vivos (`kill`) y los espera con tope (`communicate(timeout=30)`). Reemplaza `_spawn`.
- Fixture `spawn` (nueva): `with _processes(...) as launcher: yield launcher` → el teardown limpia pase, falle o se interrumpa el test.
- `_alive(pid)` (nueva): lee `/proc/<pid>/stat`; un proceso inexistente o zombi cuenta como muerto.
- `test_second_process_…`: usa la fixture; los `communicate()` de los asserts ahora tienen `timeout=60`.
- Nuevos tests: `test_a_failing_test_leaves_no_child_alive` (usa `_flow_that_fails_while_the_lock_is_held`, que reproduce el flujo con el cerrojo retenido y lanza `RuntimeError` antes de `marks/go`; luego comprueba vía /proc que ningún hijo registrado sigue vivo) y `test_the_held_child_gives_up_on_marks_go_after_its_limit_and_exits_nonzero` (límite 0.5 s → rc 3, login.md sin escribir).

## Done When
- Validation pasa: los 3 comandos con rc=0 (4 passed; 1206 passed; check.sh --fast rc=0). Ver validation.log.
- Fallo forzado sin procesos vivos: SIGINT a un pytest real mientras el primer hijo retenía el cerrojo (pytest-1674) → pytest rc=2 (KeyboardInterrupt), y luego `ps` muestra 0 hijos de ese test vivos. Ver validation.log.
- commit / aviso a IR: NO hechos, por orden del coordinador (decisión 5) y del brief (prohibido commit). Pendiente para el integrador/coordinador.

## Comandos (rc)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_apply_batch_lock.py` → 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` → 0
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` → 0
- Fallo forzado (SIGINT a `pytest -k second_process`) → pytest 2 (lo esperado); hijos vivos después: 0.

## Archivos tocados
- tests/api/test_apply_batch_lock.py
- runs/subagents/20261116-exec-orph/validation.log, result-summary.md (entrega)

## Desvíos / dudas
- El brief marcaba tests/api/test_apply_batch_lock.py como cambio ajeno sin commitear y también como el archivo del contrato; al empezar, `git status` no mostraba cambios en él (ni en apply_batch.py ni en lock.py), así que lo edité como archivo del contrato.
- Siguen vivos los dos huérfanos ANTERIORES que originaron la tarea (PID 2256206, pytest-607, ~20 h y PID 3167657, pytest-652, ~18 h). Corren el código viejo sin tope, así que nunca van a salir solos. No los maté porque pkill está prohibido y no son de esta corrida; los puede matar el coordinador con `kill 2256206 3167657`.
- No agregué la detección de muerte del padre por ppid; el tope de 120 s (decisión 2) cubre el caso del huérfano.
- No hay pills atados; no hubo choque contrato/pill.
