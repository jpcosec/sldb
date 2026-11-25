## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): en un clon limpio de SLDB_1 sin `stores build`, hacer que `sldb stores check` no reporte como errores los documentos trackeados ausentes bajo rutas declaradas `derived`, sino una alerta resumida `store/generated-missing`, manteniendo como error cualquier otro ausente y con exit code dependiente solo de errores. Superficie: `src/sldb/store/diagnostics.py`, `src/sldb/api/stores/store_check.py`, `tests/store/test_diagnostics.py`, `CHANGELOG.md`. Límites: no destrackear PythonSymbolDoc (decisión de python-sync), no tocar `selfdoc check`, sin push; el commit lo hace el coordinador.

## AMBIGUEDADES

1. "una sola alerta store/generated-missing con el número y el modelo" frente a "emitir la alerta resumida por modelo". Obligaría a inventar si hay una alerta total o una por modelo, y qué `subject` usar si conviven varios modelos.
2. "deskops message send --to <repo>". No se identifica el repo destinatario; obligaría a inventar su nombre.
3. "2453 PythonSymbolDoc documents are generated and not on disk: run `sldb stores build`". No se define plantilla para singular ni para varios modelos; obligaría a inventar el texto exacto.

## DRY-RUN

Lecturas: `diagnostics.py` (`_diagnose_doc`, `diagnose_store`), `store_check.py`, `store_declaration.py`, `tests/store/test_diagnostics.py`, `CHANGELOG.md`. Cambios previstos: `store_check.py` pasa `list[str]` de `StoreDeclaration.derived`; en `_diagnose_doc`, un missing cuya ruta empieza por un prefijo (comparación por `Path.parts`) se cuenta en vez de emitir error; al final se emite el Finding alert con `alert()` de `sldb.core.finding`; test con `derived: [gen/]`, 3 ausentes dentro y 1 fuera; línea de CHANGELOG. Dependencias: `StoreDeclaration.derived` y `alert()`. Validaciones futuras: `TMPDIR=/dev/shm pytest -q` de los dos archivos; clon limpio en `/dev/shm` con `stores check` y `stores build && selfdoc check`; anotar rc y líneas `changed` en `runs/subagents/<run-dir>/result-summary.md`.

## FUTURO

El coordinador ejecuta `deskops closeout commit` sin push. Python-sync decide destrackear documentos generados. Se envía el aviso `deskops message send` o, si el repo no está registrado, queda como línea en el informe. Un humano revisa las alertas `changed` de `selfdoc check`.
