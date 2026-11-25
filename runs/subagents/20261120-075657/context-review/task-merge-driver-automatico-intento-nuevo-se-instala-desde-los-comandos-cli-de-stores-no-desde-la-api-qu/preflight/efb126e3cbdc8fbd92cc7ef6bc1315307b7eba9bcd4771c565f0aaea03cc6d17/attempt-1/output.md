## REFORMULACION

**Propósito:** que la instalación automática del merge driver de sldb ocurra en los comandos CLI de stores (`init`, `scaffold`, `build`) y no en las funciones de API (`init_store`, `scaffold_store`, `build_store`), evitando que un `build` dentro de una `Transaction` escriba `.gitattributes`/`git config` fuera del rollback.

**Resultado:** (1) los tres comandos CLI instalan el driver vía `ensure_merge_driver`/`install_merge_driver`, idempotente, sin hacer nada fuera de un repo git y avisando por stderr sin romper si git falla; (2) `sldb stores check` emite el alert `stores/merge_driver_missing` con fix `sldb stores merge-driver --install`; (3) los tests de `tests/api/test_gitignore_policy.py` que preparan repo con la API y comparan alerts esperan también ese alert, ajustándose sin debilitar lo verificado; más CHANGELOG y commit con trailer `Task-Id`.

**Repo:** sldb (`src/sldb/cli/commands/`, `src/sldb/api/stores/`), más deskops solo como verificación opcional.

**Límites:** fuera de alcance tocar `init_store`/`scaffold_store`/`build_store` de la API. Punto de partida: el patch del intento 2.

## AMBIGUEDADES

1. «aplicar como punto de partida el patch del intento 2 (git apply runs/.../intento2-sin-commit.patch)» — no se adjunta el patch ni su contenido; obligaría a inventar qué cambia exactamente y si aplica limpio sobre el HEAD actual.
2. «el contenedor tiene /workspace/deskops» — condicional sin criterio de comprobación ni qué hacer si no existe; obligaría a inventar la política (¿falla, se omite?).
3. «salvo 'identidad' por workbench_demo (preexistente, excepción autorizada por el coordinador; decisión aparte)» — no se cita la autorización; obligaría a inventar si el ejecutor puede declarar verde con esa puerta roja.
4. «los tests que haga falta ajustar por el alert nuevo» — conjunto abierto; obligaría a inventar el alcance del ajuste.

## DRY-RUN

**Lecturas:** patch del intento 2, los tres comandos CLI, `ensure_merge_driver.py`, `store_surroundings.py`, `tests/api/test_gitignore_policy.py`, `test_merge_driver_auto_install.py`, CHANGELOG.

**Cambios previstos:** aplicar patch; ajustar los 3 tests de gitignore_policy; añadir/verificar tests de auto-instalación; actualizar CHANGELOG.

**Dependencias:** git disponible, repo en estado limpio, patch aplicable.

**Validaciones futuras (no ejecutadas):** `pytest` de los ficheros de Validation; p3 completo; `tools/check.sh --fast`; commit con `Task-Id`; `deskops advance`.

## FUTURO

Decide un humano: aceptar la puerta `identidad` en rojo y validar el criterio de ajuste de tests. Otro nodo (integración) corre la suite completa de sldb y la de deskops.
