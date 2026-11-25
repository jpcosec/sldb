REFORMULACION
Nodo ejecutable (`task.code`), no agregado. Propósito: que `sldb stores check` en un clon limpio sin `stores build` no confunda documentos generados ausentes con errores reales. Resultado: si `.sldb/store.yaml` declara rutas `derived`, un documento trackeado ausente bajo esos prefijos se cuenta y se resume en una alerta `store/generated-missing` con número y modelo; los demás ausentes siguen siendo error y el exit code solo refleja errores. Incluye tests, prueba en clon limpio, informe, CHANGELOG y commit. Repo: sldb (`/mnt/ssd/proyectos/SLDB_1`). Límites: no destrackear PythonSymbolDoc ni tocar `selfdoc check`; superficie en `diagnostics.py`, `store_check.py`, `tests/store/test_diagnostics.py`, `CHANGELOG.md`.

AMBIGUEDADES
1. "src/sldb/api/stores/store_check.py (línea 18) pasa la declaración" frente a "recibir la lista de prefijos derived": no fija si se pasa `StoreDeclaration` o solo prefijos; obliga a inventar la firma.
2. "anotar en el informe el rc y las alertas changed": no nombra archivo ni formato del informe; obliga a inventar destino.
3. "resto de la nota de 'main de sldb en verde', punto 2": contexto externo no incluido; obliga a inventar qué alertas cuentan.
4. "CHANGELOG.md": no indica sección ni formato de entrada; obliga a elegir convención.
5. "emite una sola alerta store/generated-missing": no define estructura ni severidad de la alerta en el modelo; obliga a inventar representación.
6. "empieza por uno de ellos": no aclara prefijo textual o por componente de ruta; obliga a decidir el matching.

DRY-RUN
Lecturas: `diagnostics.py`, `store_check.py`, `store_declaration.py`, `tests/store/test_diagnostics.py`, `.sldb/store.yaml`, `CHANGELOG.md`. Cambios previstos: propagar prefijos `derived`; contar missing bajo `derived` por modelo; emitir una alerta resumida; añadir test con `derived: [gen/]`, 3 ausentes dentro y 1 fuera; actualizar CHANGELOG. Dependencias: `StoreDeclaration.derived`, modelo de diagnóstico con alertas, fixtures. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/store/test_diagnostics.py`; `TMPDIR=/dev/shm pytest -q tests/test_serve_stores_check.py`; clon limpio en `/dev/shm` con `sldb stores check --store .sldb`, luego `sldb stores build && sldb selfdoc check`; informe y commit. Sin ejecutar.

FUTURO
La tarea de python-sync decide destrackear documentos generados. Un humano revisa el informe y autoriza el commit. El nodo de verificación/CI ejecutará las validaciones y confirmará el estado verde.
