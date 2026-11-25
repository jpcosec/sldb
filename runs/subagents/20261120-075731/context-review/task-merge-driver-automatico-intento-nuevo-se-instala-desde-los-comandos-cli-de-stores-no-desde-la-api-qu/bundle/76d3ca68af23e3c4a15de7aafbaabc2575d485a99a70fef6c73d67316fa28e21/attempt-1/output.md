## REFORMULACION

**Propósito:** tercer intento de que el merge driver de sldb se instale automáticamente desde los comandos CLI de stores (`init`, `scaffold`, `build`), no desde la API que usan las transacciones, tras dos intentos fallidos (uno revertido, otro con patch sin commit).

**Resultado:** los tres comandos instaladores idempotentes con aviso por stderr sin romper si git falla; las funciones de API no instalan nada; `sldb stores check` emite `stores/merge_driver_missing` con fix `sldb stores merge-driver --install`; los tests de `test_gitignore_policy.py` que preparan repo git esperan el alert nuevo; CHANGELOG; commit con trailer Task-Id.

**Repo:** sldb (`src/sldb/cli/commands/`, `src/sldb/api/stores/`, `tests/`, CHANGELOG), con comprobación opcional en deskops.

**Límites:** fuera tocar `init_store/scaffold_store/build_store` de la API. Nodo ejecutable (`task.code`).

## AMBIGUEDADES

1. «los tests que haga falta ajustar por el alert nuevo» — no enumera; obligaría a inventar el conjunto exacto de tests afectados.
2. «ajustar los 3 que fallan» — no los nombra; obligaría a inventar cuáles son.
3. «si el contenedor tiene /workspace/deskops» — condición no verificable desde el input; obligaría a inventar su existencia.
4. «excepción autorizada por el coordinador; decisión aparte» — autorización externa no incluida; obligaría a asumirla.
5. «runs/subagents/exec-deskops-e-7b45b951426a-a2/intento2-sin-commit.patch» — el bundle no trae el patch ni los archivos nombrados; obligaría a inventar su contenido.
6. «las pills ligadas, los átomos ligados» — el input trae `atoms: []` y no incluye pills; obligaría a inventarlas.

## DRY-RUN

**Lecturas:** patch del intento 2, `src/sldb/cli/commands/*`, `ensure_merge_driver.py`, `store_surroundings.py`, `tests/api/test_gitignore_policy.py`, `tests/store/test_merge_driver_auto_install.py`, CHANGELOG.

**Cambios previstos:** `git apply` del patch como base; ajuste de los tests de gitignore_policy; CHANGELOG; `git add` de rutas nombradas y commit con Task-Id; `deskops advance`.

**Dependencias:** git disponible, pytest, `tools/check.sh`, `/workspace/deskops` opcional.

**Validaciones futuras:** el pytest de la sección Validation; luego los tests de p3; `check.sh --fast` (salvo `identidad`); test deskops `-k second_atom_create_fails`; commit existente; advance.

## FUTURO

El integrador corre las suites completas de sldb y de deskops. Un humano decide sobre la excepción de `identidad`/`workbench_demo` y sobre la autorización del coordinador.
