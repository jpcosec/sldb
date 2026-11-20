# Result — stores check: documentos generados ausentes como alerta

Estado: implementado y probado; NO commiteado ni avanzado, porque `bash tools/check.sh --fast` sale rc 1 por un fallo ajeno.

## Cambios (archivos tocados por esta tarea)
- src/sldb/store/diagnostics.py: `diagnose_store(..., derived=())`; un documento ausente bajo un prefijo derived (comparación por componentes de ruta) se cuenta, no se diagnostica.
- src/sldb/store/diagnostics_models/model_diagnosis.py: campo `generated_missing`.
- src/sldb/api/stores/store_findings.py: alerta `store/generated-missing` (sujeto = modelo, texto del Goal).
- src/sldb/api/stores/store_check.py: `derived_prefixes(store_path)` (lista de str de `StoreDeclaration.derived`), pasada a diagnose_store.
- src/sldb/cli/commands/store_check.py, src/sldb/cli/serve/stores_check.py, src/sldb/cli/serve/lint_routes.py: pasan los prefijos (mismos llamadores de diagnose_store).
- tests/store/test_diagnostics.py: test nuevo (3 ausentes bajo gen/ -> 1 alerta que dice 3; `genx.md` ausente fuera -> 1 error store/missing).
- CHANGELOG.md: una línea bajo 0.1.13. OJO: el árbol ya traía otras líneas sin commitear de otras tareas en CHANGELOG.md y otros archivos sucios ajenos; al commitear, stagear solo mi línea.

## Validación
- pytest tests/store/test_diagnostics.py tests/test_serve_stores_check.py: rc 0, 19 passed.
- `tools/check.sh --fast`: rc 1, por `identidad`: "directorio versionado sin clasificar en la raíz: workbench_demo" (versionado desde 562847e2, ajeno a la tarea). Por eso no commiteé.

## Clon limpio (/dev/shm/cl, clon de HEAD + mis archivos src superpuestos, PYTHONPATH al clon)
- `sldb stores check --store .sldb`: rc=1. 0 errores de PythonSymbolDoc; una alerta: `store/generated-missing PythonSymbolDoc: 2540 PythonSymbolDoc documents are generated and not on disk: run `sldb stores build``. Los 27 errores restantes son ajenos (modelos de deskops no importables en el clon: store/model-unresolved; y 1 InboxNoteDoc missing real).
- `sldb stores build`: rc=1 `Unexpected: [Errno 2] No such file or directory: '/dev/shm/cl/knowledge/symbols/python-sldb-sldb-api-actor-set_actor.md'` (el directorio knowledge/symbols/ no existe en el clon; fallo de python-sync, fuera de alcance).
- `sldb selfdoc check`: rc=0; líneas con estado changed: `"changed": []` (ninguna). (Corrió tras el build fallido.)

Aviso a deskops/python-sync: `stores build` en clon limpio falla por falta de knowledge/symbols/.

## Actualización (autorizada por el coordinador)
`check.sh --fast` falla SOLO en la puerta `identidad`, por `workbench_demo` (preexistente de 562847e2; hay tarea de decisión aparte). Ninguna otra puerta en rojo. Commit hecho con los archivos por nombre y el CHANGELOG stageado solo con mi línea.

## Commit (incidente)
Mi `git commit` falló por identidad git ausente (el `advance` corrió igualmente: la tarea está en ritual-testing). Entre mi `git add` y el reintento, otro agente (índice compartido, shared-plain) commiteó con lo ya stageado: mis 8 archivos (7 de src + tests/store/test_diagnostics.py) y mi línea de CHANGELOG quedaron dentro del commit 0f91540d ("on_write: save_document_payload devuelve las alertas..."), sin trailer Task-Id de esta tarea. No reescribí historia compartida. El coordinador debe tenerlo en cuenta al cerrar (el código de esta tarea está en 0f91540d).

## Commit de CHANGELOG
Mi línea de CHANGELOG no había entrado en 0f91540d; la commiteé en 07450d10 (con Task-Id). Ese commit arrastró además la línea de CHANGELOG de otra tarea (`save_document_payload` devuelve alertas), que estaba sin commitear en el árbol compartido. Código y test de esta tarea: 0f91540d.
