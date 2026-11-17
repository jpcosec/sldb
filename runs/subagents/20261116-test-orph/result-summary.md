# result-summary — tester deskops-t-7b2e60544646

Tarea: task-test-apply-batch-lock-no-deja-procesos-huérfanos-… · Ejecutor: deskops-e-cdb27fa3f0f8.
Evidencia completa en `validation.log`. Pruebas forzadas en copias en `/dev/shm/torph` (HEAD + test del ejecutor), ya borradas; el repo no se editó.

## Veredicto: PASA

| Punto | Veredicto | Evidencia |
|---|---|---|
| Validation 1: `pytest -q tests/api/test_apply_batch_lock.py` | PASA | 4 passed, rc=0 |
| Validation 2: `pytest -q tests/test_clean_code_rules.py` | PASA | 1206 passed, rc=0 |
| Validation 3: `bash tools/check.sh --fast` | PASA | rc=0 |
| Done When: tras forzar un fallo no queda ningún proceso del test vivo | PASA | ver casos A–D |
| Done When: commit; aviso a IR | No aplica al tester | No hechos (el brief prohíbe commit); los hace el coordinador/integrador |
| (1) Solo cambió `tests/api/test_apply_batch_lock.py` | PASA | `git diff --name-only`: ese test y además `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml`, `.sldb/store.yaml` + 2 shards RunDoc nuevos: son los registros de las corridas (run-deskops-e/t), no del ejecutor. `uv.lock` sin cambios |
| Regresiones vecinas | PASA (vacío) | ningún módulo de `src/` cambió → no hay tests vecinos que correr |

## Casos forzados (2), con ps después

- **A, falla de assert** (`assert False` tras `started`, con ambos hijos vivos): pytest rc=1; hijos vivos después: 0.
- **B, SIGINT a pytest** con los dos hijos vivos (vistos en ps antes): pytest rc=2 (KeyboardInterrupt); hijos vivos después: 0.
- **C, timeout de pytest** (no hay pytest-timeout en el lock; se usó `uv run --with pytest-timeout`, sin tocar `uv.lock`):
  - C1 `--timeout=5` (método signal): rc=1, `Failed: Timeout (>5.0s)`; hijos vivos después: 0 (el teardown de la fixture los mata).
  - C2 `--timeout-method=thread` (os._exit, sin teardown): los 2 hijos quedan con ppid 1 y salen solos por el tope 120 s después de `ready`.
  - C3 `kill -TERM` al pytest: igual que C2 (sin teardown), salen solos por el tope.
- **D, kill -9 al pytest padre**: rc=137; justo después, 2 hijos con ppid 1. Salen solos **118 s después de morir el padre (120 s después de `ready`)**, o sea, dentro del tope de 120 s. El retenedor sale por el tope (rc 3, suelta el cerrojo) y el segundo hijo, que esperaba el cerrojo, entra (`entered` a +120 s), aplica su lote en el store temporal y termina. `ps` vacío después.
  - Ojo: el hijo **no detecta** que murió el padre. Sale *al llegar* el tope (≈120 s desde `ready`), no antes. Si "antes del tope" quería decir que el hijo se entera de la muerte del padre (por ppid), eso no está implementado (el ejecutor lo dice). El contrato solo pide un tope, y se cumple.

## (3) El test de concurrencia sigue discriminando — PASA
Con `with store_lock(...)` cambiado por `nullcontext()` en `apply_batch.py` (copia `repo-nolock`): `test_second_process_…` FALLA (`assert not (tmp_path / "entered").exists()`), 1 failed / 3 passed, y no quedan hijos vivos.

## Caso extra (no cubierto por el ejecutor) — PASA
Mutación: en `_processes` se cambió `child.kill()` por `pass`. `test_a_failing_test_leaves_no_child_alive` lo detecta y FALLA (`TimeoutExpired` en `communicate(timeout=30)`). Así, el test de fallo simulado sí protege la limpieza. Los 2 hijos de la mutación salieron solos por el tope (~88 s después).

## Notas (no bloquean)
- En el `finally` de `_processes`, si `communicate(timeout=30)` de un hijo lanza `TimeoutExpired`, el bucle se corta y los hijos siguientes no se esperan (en la práctica no pasa después de SIGKILL).
- Siguen vivos los dos huérfanos ANTIGUOS (PID 2256206, pytest-607, ~20 h; PID 3167657, pytest-652, ~18 h), que corren el código viejo sin tope. No son de esta corrida y no los toqué; hay que matarlos a mano (`kill 2256206 3167657`).

## (4) ps final
Ningún proceso de mis pruebas (`/dev/shm/torph`) vivo; copias borradas.
