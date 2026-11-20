PASA

# Testing — merge driver automático desde los comandos CLI de stores

Commit verificado: `9007f78a22569244709af77779847e14a4d57b2e`
("El merge driver de sldb se instala desde los comandos CLI de stores, no desde la API",
con `Task-Id: task-merge-driver-automatico-intento-nuevo-se-instala-desde-los-comandos-cli-de-stores-no-desde-la-api-qu`).
HEAD actual: `9007f78a`; no hay cambios pendientes en `src/`, `tests/` ni `CHANGELOG.md`.

## Veredicto

El cambio cumple el objetivo y las puertas aplicables quedan en verde. `bash tools/check.sh --fast`
termina con rc 1 solamente por la puerta `identidad` (`workbench_demo` sin clasificar), preexistente y
ajena a este commit; el preflight-1 de esta tarea autoriza expresamente esa roja y solo esa. Ninguna
otra puerta falla.

## Tests ejecutados (de a uno, con `TMPDIR=/tmp`)

Base: `/workspace/sldb/.venv/bin/python -m pytest -q -p no:cacheprovider <archivo>`.
`/tmp/ws-venv` no existía en este contenedor; se usó el `.venv` real del repo (Python 3.13).

| Archivo | Resultado |
|---|---|
| `tests/api/test_gitignore_policy.py` (archivo del commit) | **9 passed** |
| `tests/store/test_merge_driver_auto_install.py` (archivo nuevo del commit) | **7 passed** |
| `tests/store/test_migrate_layout.py` (archivo del commit) | **8 passed** |
| `tests/store/test_stores_build.py` (módulo tocado: build) | **35 passed** |
| `tests/api/test_scaffold_store.py` (módulo tocado: scaffold) | **20 passed** |
| `tests/api/test_api_stores.py` (superficie stores/check) | **14 passed** |
| `tests/api/test_store_init_failures.py` (módulo tocado: init) | **3 passed** |
| `tests/store/test_cli_store.py` (superficie CLI de stores) | **38 passed** |
| `tests/test_clean_code_rules.py` | **1227 passed** |

Validación exacta de la tarea:

    TMPDIR=/tmp python -m pytest -q -p no:cacheprovider \
      tests/store/test_merge_driver_auto_install.py tests/api/test_gitignore_policy.py
    -> 16 passed

También se corrieron completas, para detectar cualquier otro test afectado por el alert nuevo:

- `tests/api`: **657 passed, 8 skipped**.
- `tests/store`: **457 passed**.
- deskops `tests/test_transaction.py -k second_atom_create_fails` con
  `PYTHONPATH=/workspace/sldb/src`: **1 passed** (la regresión que motivó el intento nuevo sigue resuelta).

No se corrió la suite completa de sldb: la corre integrate en el host, según la instrucción del rol.

## Revisión contra el Goal

- `sldb stores init`, `sldb stores scaffold --apply` y `sldb stores build` (comandos CLI en
  `src/sldb/cli/commands/`) llaman a `ensure_merge_driver`, que delega en `install_merge_driver`:
  idempotente, no hace nada fuera de git y, si git falla, avisa por stderr sin cambiar el código de
  salida. Los tests cubren init, scaffold, build, doble ejecución sin duplicar líneas, fuera de git
  y fallo simulado de git.
- Las funciones de API `init_store`, `scaffold_store` y `build_store` ya no instalan nada;
  `test_api_init_and_build_leave_git_untouched` verifica que no escriben `.gitattributes` ni
  `merge.sldb.*`.
- `sldb stores check` emite el hallazgo `merge-driver-missing` (nivel alert, `ok` sigue en true) con
  fix `sldb stores merge-driver --install`, y deja de emitirlo tras instalar el driver.
- Los 3 tests de `tests/api/test_gitignore_policy.py` que preparan un repo git con la API ahora
  esperan el alert nuevo comparando la lista exacta de códigos; no se debilitó lo que verifican.
  `test_migrate_layout.py` instala el driver antes de exigir un check limpio, como pedía el alcance.
- `CHANGELOG.md` tiene la viñeta correspondiente.

## Gate rápido

    PATH=/workspace/sldb/.venv/bin:$PATH bash tools/check.sh --fast  -> rc 1

    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

La única falla es la excepción autorizada por preflight-1: `workbench_demo` es preexistente
(`562847e2`) y el commit no toca `contracts/identity.toml` ni `workbench_demo`.

## Observación

El código del alert implementado es `merge-driver-missing` (el que nombran la Rationale, el patch de
partida aceptado en preflight-1 y los testers de los intentos anteriores), no
`stores/merge_driver_missing` tal como lo escribe el punto (2) del Goal. Funcionalmente es el mismo
requisito y todos los tests/consumidores usan el código aceptado en el preflight.
