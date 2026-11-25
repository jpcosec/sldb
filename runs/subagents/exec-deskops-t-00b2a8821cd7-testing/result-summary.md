FALLA

# Testing — merge driver automático al preparar un store y hallazgo en `stores check`

Commit verificado: `68d4ee1d9019475b84acd370f7ef1eba4f927e85`
("El merge driver de sldb se instala al preparar un store y stores check avisa si falta",
con `Task-Id: task-el-merge-driver-de-sldb-se-instala-solo-al-preparar-un-store-y-stores-check-avisa-si-falta`).
HEAD actual: `f055723d`; no hay cambios posteriores en los archivos del commit.

## Veredicto

El comportamiento pedido está implementado y los tests pasan. La única causa del veredicto FALLA es la puerta rápida:
`bash tools/check.sh --fast` termina con **rc 1** porque falla `identidad` por un directorio preexistente sin clasificar
(`workbench_demo`, incorporado en `562847e2`, anterior al commit del ejecutor y ajeno a este cambio). La regla del rol
de testing es explícita: rc distinto de 0 en `check.sh --fast` ⇒ FALLA. El propio informe del ejecutor registra que el
coordinador autorizó commitear con esa puerta en rojo y que la clasificación de `workbench_demo` va en otra tarea.

Si el coordinador acepta formalmente esa roja preexistente como excepción, el veredicto funcional de este commit es PASA.

## Tests ejecutados (de a uno, con `TMPDIR=/tmp`)

Comando base: `TMPDIR=/tmp python -m pytest -q -p no:cacheprovider <archivo>` con el Python de `/tmp/ws-venv`
(creado como symlink al `.venv` del repo, porque `/tmp/ws-venv` no existía al inicio).

| Archivo | Resultado |
|---|---|
| `tests/store/test_merge_driver_auto_install.py` (archivo nuevo del commit) | **6 passed** |
| `tests/store/test_stores_build.py` (validación explícita de la tarea) | **35 passed** |
| `tests/api/test_scaffold_store.py` (módulo tocado: `scaffold_store`) | **20 passed** |
| `tests/api/test_api_stores.py` (superficie de stores/check) | **14 passed** |
| `tests/api/test_gitignore_policy.py` (init/entorno de store) | **9 passed** |

No se corrió la suite completa: la corre integrate en el host, según la instrucción del rol.

Los tests del commit cubren: (a) `init` deja las tres líneas de `.gitattributes` y `merge.sldb.driver`;
(b) `build` instala el driver si falta; (c) correr dos veces (build/build/init --force) no duplica líneas;
(d) fuera de git `init`/`build` funcionan y no crean `.gitattributes`; (e) `stores check` reporta
`merge-driver-missing` con fix `sldb stores merge-driver --install` y deja de reportarlo tras instalar;
más el caso de fallo de git, que solo avisa por stderr y no rompe `init`.

## Gate rápido

    PATH=/tmp/ws-venv/bin:$PATH TMPDIR=/tmp bash tools/check.sh --fast   -> rc 1
    PASS: núcleo aislado
    PASS: capas
    FAIL: identidad — "directorio versionado sin clasificar en la raíz: workbench_demo"
    PASS: ejes
    PASS: superficie

Log completo en `/tmp/check-fast-merge-driver.log`. La violación de identidad no proviene de este commit:
`workbench_demo` se versionó en `562847e2`, que ya es ancestro del commit del ejecutor, y
`contracts/identity.toml` no lo clasifica. El commit del ejecutor no toca `contracts/identity.toml`
ni `workbench_demo`.

## Revisión del código

- `src/sldb/api/stores/ensure_merge_driver.py` (nuevo): `ensure_merge_driver` detecta el repo git, delega en
  `install_merge_driver` y captura `RuntimeError`/`OSError`/`ValueError` avisando por stderr sin propagar;
  `missing_merge_driver` compara las tres líneas de `.gitattributes` y las claves `merge.sldb.*`;
  `merge_driver_finding` emite el hallazgo no-error `merge-driver-missing` con el fix pedido.
- `init_store.py`, `scaffold_store.py` (solo con `apply`) y `build_store.py` (solo con `apply`) llaman a
  `ensure_merge_driver`, después de crear el store y dentro del flujo normal.
- `store_surroundings.py` incorpora el hallazgo a los findings que consume `stores check` (`check_store`).
- `CHANGELOG.md`: entrada correspondiente, con alcance y nombre del test.
- Idempotencia y no-op fuera de git se apoyan en `install_merge_driver`, que ya era idempotente.
- No se modifica el driver ni se toca deskops.

## Observaciones

- `/tmp/ws-venv` no existía; se creó un symlink a `/mnt/ssd/proyectos/SLDB_1/sldb/.venv`. No es un cambio del repo.
- El nivel del hallazgo se implementa como `alert` (el nivel no-error del repo, el que no hace fallar el comando);
  el test verifica que aparece en `report["alerts"]` y que `report["ok"]` sigue siendo `True`, consistente con el
  pedido de que sea un aviso y con la taxonomía de `sldb.core.finding`.
