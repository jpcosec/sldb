FALLA

# Testing — merge driver automático al preparar un store (intento 2)

## Alcance verificado

El ejecutor del intento 2 **no dejó commit**: los cambios están en el índice (`git add`) pero no
commiteados. `git log -1 --grep "Task-Id: task-el-merge-driver..."` sigue devolviendo el commit del
intento 1, `68d4ee1d9019475b84acd370f7ef1eba4f927e85`, que es justamente el que provocó la regresión que
motivó volver a ejecución. El árbol de trabajo staged es el intento 2 (instalación movida de las funciones
de API a los comandos CLI). Todos los tests de abajo se corrieron contra ese árbol de trabajo.

Archivos staged del intento 2:

- `src/sldb/api/stores/{init_store,scaffold_store,build_store,ensure_merge_driver}.py`
- `src/sldb/cli/commands/{store_init,stores_scaffold,stores_build}.py`
- `tests/store/test_merge_driver_auto_install.py`
- `tests/store/test_migrate_layout.py`
- `CHANGELOG.md`

No hay commit, así que no hay SHA de ejecutor que el closeout pueda citar para el intento 2.

## Veredicto

**FALLA**, por dos motivos independientes:

1. **Regresión de tests existentes**: `tests/api/test_gitignore_policy.py` falla 3 de 9. Al mover la
   instalación automática a los comandos CLI, los repos git preparados con la API `init_store()` ya no
   reciben el driver; `stores check` agrega entonces el alert `merge-driver-missing`, pero esos tests
   exigen `payload["alerts"] == []` o exactamente `["stores/cache_not_ignored"]`.
   El ejecutor actualizó `test_migrate_layout.py` por esta misma razón, pero no `test_gitignore_policy.py`.
2. **Gate rápido en rojo**: `bash tools/check.sh --fast` termina con rc 1 por `identidad`
   (`workbench_demo` sin clasificar, preexistente y ajeno a este cambio). La regla del rol es explícita:
   rc distinto de 0 ⇒ FALLA.

El objetivo funcional del intento 2 sí se cumple: el test de regresión de deskops pasa y el test nuevo que
verifica que la API no toca git pasa. Pero la suite de tests que el propio cambio rompe no puede quedar así.

## Tests ejecutados (de a uno, `TMPDIR=/tmp`, Python de `/tmp/ws-venv`)

Se creó `/tmp/ws-venv` como symlink a `/workspace/sldb/.venv` (no existía al comenzar; no es un cambio del repo).

| Archivo | Resultado |
|---|---|
| `tests/store/test_merge_driver_auto_install.py` (archivo del cambio) | **7 passed** |
| `tests/store/test_migrate_layout.py` (archivo del cambio) | **8 passed** |
| `tests/store/test_stores_build.py` (validación explícita de la tarea) | **35 passed** |
| `tests/store/test_cli_store.py` (superficie CLI de stores) | **38 passed** |
| `tests/api/test_api_stores.py` + `test_scaffold_store.py` + `test_gitignore_policy.py` + `test_store_init_failures.py` | **43 passed, 3 failed** |
| `tests/api/test_gitignore_policy.py` (aislado, para confirmar) | **3 failed, 6 passed** |
| deskops `tests/test_transaction.py -k second_atom_create_fails` con `PYTHONPATH=/workspace/sldb/src` | **1 passed** |

Fallos concretos de `tests/api/test_gitignore_policy.py`:

- `test_a_repo_that_ignores_the_cache_and_versions_the_store_is_fine`
- `test_the_cache_not_ignored_is_an_alert`
- `test_any_rule_that_covers_the_cache_counts`

Los tres fallan porque `payload["alerts"]` contiene además
`{"level": "alert", "code": "merge-driver-missing", "subject": ".gitattributes", ...}`.
El helper `_repo()` de ese archivo usa `init_store()` de la API; con el intento 2 el driver solo se instala
por CLI, así que el alert nuevo es esperable. Falta actualizar el test (usar `sldb stores init`, instalar el
driver a mano como ya hace `test_migrate_layout.py`, o incluir/filtrar el alert nuevo).

No se corrió la suite completa: la corre integrate en el host, según la instrucción del rol.

## Gate rápido

    PATH=/tmp/ws-venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast   -> rc 1

    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

Log completo en `/tmp/check-fast-merge-driver-a2.log`. La violación de `identidad` es preexistente
(`workbench_demo`, ya versionado antes de esta tarea; `contracts/identity.toml` no lo clasifica). Aun si el
coordinador la aceptara como excepción, el veredicto seguiría siendo FALLA por los 3 tests rotos.

## Revisión del cambio (intento 2)

- La instalación sale correctamente de `init_store`, `scaffold_store` y `build_store` de la API y queda en
  `store_init.py`, `stores_build.py` y `stores_scaffold.py` (solo con `--apply`).
- `ensure_merge_driver.py` conserva el no-op fuera de git, la idempotencia y el aviso por stderr ante fallo
  de git.
- El hallazgo `merge-driver-missing` de `stores check` se mantiene y solo lee.
- El test nuevo `test_api_init_and_build_leave_git_untouched` cubre el caso que motivó el retorno a ejecución.
- La regresión de deskops que originó el intento 2 queda resuelta: el test indicado pasa.

## Acciones pedidas al ejecutor

1. Actualizar `tests/api/test_gitignore_policy.py` para el alert nuevo (o instalar el driver en `_repo()`
   como en `test_migrate_layout.py`).
2. Commitear el intento 2 con rutas nombradas y el trailer `Task-Id: ...` (hoy no existe ese commit).
3. Volver a correr los tests afectados y `bash tools/check.sh --fast`.
