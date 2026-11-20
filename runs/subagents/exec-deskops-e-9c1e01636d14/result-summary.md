# result-summary — deskops-e-9c1e01636d14
run_id: deskops-e-9c1e01636d14 · session: n/a · session_sha256: n/a

Estado: implementado y commiteado. `check.sh --fast` falla solo en la puerta `identidad` por `workbench_demo` (preexistente de 562847e2; autorizado por el coordinador); las demás puertas PASS.

## Cambios (sin commitear)
- src/sldb/api/stores/link_store.py: `link_store(..., *, raw=None)` y `record_store_link(..., *, raw=None)`; si `raw` empieza por `/`, `~` o `$` se guarda tal cual, si no `relpath` a la raíz. Validaciones sobre el texto expandido. Helpers `KEPT_PREFIXES`, `expand_link_path`, `kept_as_written`.
- src/sldb/cli/commands/store_add.py: pasa `raw=str(args.path)`.
- src/sldb/store/query.py: `_linked_stores` expande `~` y variables antes de resolver.
- tests/api/test_api_stores.py: 4 tests nuevos (absoluta, ~ con HOME, $VAR/${VAR} + remove + --replace, relativa).
- tests/store/test_stores_build.py: 4 llamadas a `stores add` pasan `os.path.relpath(...)` para conservar la intención (enlace relativo que sube niveles); sin ello fallaban 3 tests, porque ahora una ruta absoluta se guarda absoluta (efecto directo del contrato).
- CHANGELOG.md, docs/architecture/store-declaration.md (sección "Links: how `sldb stores add` records the path").

## Validación
Ver validation.log. Los tres comandos del contrato pasan; también test_cli_store, test_export_contract_frozen y test_linked_structural.

## Para el supervisor
- Gate `check.sh --fast`: rc 1 solo por `identidad` (workbench_demo), no por esta tarea. Hay que decidir/clasificar workbench_demo o aceptar el gate; luego commitear los archivos listados con `Task-Id`.
- Aviso a AntonIA: AntonIA no está registrado en deskops. Aviso a AntonIA: `sldb stores add` ahora guarda tal cual una ruta que empieza por `/`, `~` o `$` y la lectura expande `~` y variables; re-enlazar con `sldb stores add <ruta> --name <alias> --replace` en shared_llm-gateway y manifest; commit <pendiente>.
