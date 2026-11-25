REFORMULACION
Propósito: evitar que `stores check` trate como errores los documentos generados ausentes en un clon sin build. Resultado: si `store.yaml` declara rutas `derived`, un documento trackeado ausente bajo esos prefijos se cuenta y se resume en una alerta `store/generated-missing` por modelo; cualquier otro ausente sigue siendo error y el exit code depende solo de errores. Repo: `sldb`; superficie: `src/sldb/store/diagnostics.py`, `src/sldb/api/stores/store_check.py`, `tests/store/test_diagnostics.py`, `CHANGELOG.md`. Límites: no destrackear `PythonSymbolDoc`, no cambiar `selfdoc check`, no hacer push; el commit lo hace el coordinador. No es un agregado: es una tarea de código ejecutable.

AMBIGUEDADES
1. “creado con la función alert() de sldb.core.finding como las demás alertas de stores check”: el input no incluye `sldb.core.finding`; obligaría a inventar la firma exacta y cómo se transporta el `Finding` desde `diagnostics.py`.
2. “store_check.py pasa a diagnose_store solo la lista de prefijos (list[str]) de StoreDeclaration.derived”: no se dice cómo obtiene `store_check` la `StoreDeclaration` desde `store_path`; obligaría a inventar la API de carga.
3. “en un clon limpio en /dev/shm”: no se define URL, revisión ni preparación del entorno; obligaría a inventar el origen del clon y el setup.

DRY-RUN
Lecturas: `diagnostics.py`, `store_check.py`, `store_declaration.py`, `tests/store/test_diagnostics.py`, `sldb.core.finding` y `CHANGELOG.md`. Cambios previstos: recibir prefijos `derived`, comparar por componentes de ruta, contar ausentes generados, emitir una alerta resumida por modelo, conservar errores para el resto, ajustar tests y añadir la línea de CHANGELOG. Dependencias: lector de `StoreDeclaration`, constructor `alert()`, helpers de test y comandos del clon. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_diagnostics.py`; `TMPDIR=/dev/shm pytest -q tests/test_serve_stores_check.py`; en clon limpio, `sldb stores check --store .sldb`, luego `sldb stores build && sldb selfdoc check`; anotar rc y líneas `changed` en `result-summary.md`.

FUTURO
Otro nodo ejecuta implementación y tests. Un humano o nodo de entorno prepara el clon limpio y revisa el informe. El coordinador cierra con `deskops closeout commit`. La decisión de destrackear `PythonSymbolDoc` queda para python-sync; las alertas residuales de `selfdoc check` se reportan, no se corrigen aquí.
