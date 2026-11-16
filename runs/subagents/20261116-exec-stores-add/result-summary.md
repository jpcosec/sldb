# result-summary — deskops-e-9c1e01636d14

Tarea: `task-sldb-stores-add-guarda-tal-cual-un-enlace-absoluto-con-o-con-variable-de-entorno`.
Estado: **BLOQUEADO** — implementación, tests nuevos, CHANGELOG y doc listos; `tests/store/test_stores_build.py` (Validation 3) falla con 3 tests que fijan el comportamiento viejo y ese archivo no está en el contrato.

## Cambios

- `src/sldb/api/stores/link_store.py`
  - `link_store(..., *, raw: str | None = None)`: con `raw`, valida (`_check_other_exists`, `_check_not_self`, nombre por defecto) sobre `Path(expand_link_path(raw)).resolve()`; pasa `raw` a `record_store_link`.
  - `record_store_link(sp, root, other, name, *, raw=None)`: guarda `raw` sin cambios si `kept_as_written(raw)` (empieza por `/`, `~` o `$`); si no, `os.path.relpath(other, root)` como antes. La firma sigue compatible con pron (`_link_store`).
  - Nuevos: `KEPT_PREFIXES`, `expand_link_path(text)` (= `os.path.expandvars(os.path.expanduser(text))`), `kept_as_written(raw)`.
- `src/sldb/cli/commands/store_add.py` — `add_store` pasa `raw=str(args.path)` (autorizado por Scope y pill).
- `src/sldb/store/query.py` — `_linked_stores` expande `~` y variables de `entry.path` antes de `_resolve_path`; `import os`. `_resolve_path` general no se toca (pill).
- `tests/api/test_api_stores.py` — helpers `_other_store`, `_add_link`, y 4 tests vía CLI `stores add`:
  `test_stores_add_keeps_an_absolute_path_absolute`, `test_stores_add_keeps_a_home_path_as_written_and_reads_it_with_home` (HOME parcheado), `test_stores_add_keeps_a_variable_path_as_written_and_reads_it_with_the_variable` (`$SLDB_TEST_ROOT`, también `${...}`, `stores remove` y `stores add --replace`), `test_stores_add_keeps_a_relative_path_relative_to_the_root`. Cada uno comprueba lo guardado en el índice y la resolución con `_linked_stores`.
- `CHANGELOG.md` — una línea bajo `## 0.1.13 — not released yet`.
- `docs/architecture/store-declaration.md` — sección nueva "Links: how `sldb stores add` records the path" (no había sección de enlaces; se agregó antes de `folders` y `seeds`).

## Pill vs contrato
- Contrato dice expandir en "_resolve_path / _linked_stores"; el pill (precisión posterior) dice solo en `_linked_stores`. Seguí el pill.
- Pill: `raw` se agrega a `link_store` y pasa a `record_store_link`; validación con texto expandido, se guarda `raw` sin expandir. Hecho así.

## Validation (salida completa en validation.log)
| comando | rc |
|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_api_stores.py` | 0 (16 passed) |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_unlink_store.py` | 0 (5 passed) |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/store/test_stores_build.py` | **1 (3 failed, 24 passed)** |

## Bloqueo
Fallan `test_the_check_reaches_a_link_that_climbs_more_than_one_level`, `test_an_absent_linked_store_is_an_alert_naming_the_link_and_its_path_in_the_check` y `test_an_absent_linked_store_does_not_fail_the_build_and_is_reported`. Los tres llaman `sldb stores add <ruta absoluta>` y esperan el enlace relativo (`../../../owner/.sldb`, `../sibling/.sldb`). Es justo lo que el Goal cambia: una ruta absoluta escrita se guarda absoluta. No es por cambios ajenos. Arreglarlo exige editar `tests/store/test_stores_build.py`, que no está en el contrato ni lo autorizan Scope o pill, así que no lo toqué.

Parche propuesto (no aplicado): `runs/subagents/20261116-exec-stores-add/proposed-test_stores_build.patch` — `import os` y pasar `os.path.relpath(<store>)` en vez de `str(<store>)` a `stores add` (en 4 llamadas; 2 de ellas ya pasaban y siguen pasando), lo que conserva la intención de los tests (enlace relativo que sube varios niveles). Verificado en una copia en el scratchpad (import relativo `.test_semantic_export` cambiado a absoluto solo para correrla fuera de `tests/store/`): 27 passed.

Riesgo no verificado (fuera de Validation, no lo corrí): otros tests que llaman `stores add` con ruta absoluta y quizá esperan el relativo: `tests/store/test_export_contract_frozen.py:42`, `tests/store/test_cli_store.py:104,124,129,266`, `tests/test_linked_structural.py:33`.

Fuera de alcance, sin tocar: otros lectores de `entry.path` (p. ej. `src/sldb/api/model_registry/federated_lookup.py:31`, `stores build`/declaración) no expanden `~`/`$`; el pill limita la expansión a `_linked_stores`.

## Done When
- Los tres comandos pasan con los cuatro casos nuevos: **no** (Validation 3, ver Bloqueo); los 4 casos nuevos pasan.
- CHANGELOG y doc: sí.
- Commit: lo hace el coordinador (`deskops closeout commit`); no hice commit.
- Aviso a AntonIA: lo manda el coordinador tras el commit (lleva el hash). Texto sugerido — Aviso a AntonIA: `sldb stores add` ahora guarda tal cual una ruta que empieza por `/`, `~` o `$` y la lectura expande `~` y variables; volver a enlazar `deskops-runtime` con `sldb stores add /mnt/ssd/proyectos/SLDB_1/deskops-runtime/.sldb --name <alias> --replace` (o `$VAR/...`) en shared_llm-gateway y manifest; commit <pendiente>.

## Archivos tocados
- src/sldb/api/stores/link_store.py
- src/sldb/cli/commands/store_add.py
- src/sldb/store/query.py
- tests/api/test_api_stores.py
- CHANGELOG.md
- docs/architecture/store-declaration.md
- runs/subagents/20261116-exec-stores-add/{validation.log,result-summary.md,proposed-test_stores_build.patch}

Ningún archivo ajeno (apply_batch.py, lock.py, uv.lock, desk/, .sldb/) tocado ni staged.
