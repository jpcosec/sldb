REFORMULACION
Propósito: corregir H1 —que `sldb stores check` aborte con "Unexpected: 1 validation error" ante un documento que su modelo rechaza— convirtiéndolo en un hallazgo por documento y continuando el diagnóstico; fijar H2/H3 con tests de regresión. Resultado: guarda en `sldb.store.diagnostics` que captura el `ValidationError` y emite un código nuevo de hallazgo (severidad error), diagnóstico completo en texto y JSON con rc 1; tests, docs y CHANGELOG. Repo: sldb (src/sldb/store/, api/stores/, cli/commands/, tests/, docs/, CHANGELOG.md, contracts/layers.toml). Límites: fuera la guarda preventiva de deskops, source_read y cambiar qué valida cada modelo; no subir límites de clean-code.

AMBIGUEDADES
1. "código nuevo store/doc-invalid (o el nombre que encaje con los existentes)": obliga a inventar el identificador exacto del hallazgo.
2. "el mensaje de pydantic resumido": no define cuánto resumir; obliga a inventar el formato.
3. "las otras rutas de stores check que extraen con el modelo (contrato movido, secciones, aristas)": no enumera las rutas exactas ni el mecanismo de deduplicación para "una sola vez, no una vez por subsistema".
4. "El informe dice qué commit de sldb dejó de reproducir H2 (git bisect ... o el mecanismo leído en el código)": dos vías alternativas sin criterio; obliga a elegir.
5. "una escritura transaccional de un válido": no nombra la operación concreta a cubrir en el test.

DRY-RUN
Lecturas: TaskDoc, nota 3895e9f7, runs/subagents/20261111-repro-h123/repro.sh y repro.log, `store/diagnostics.py` y `diagnostics_models`, catálogo de códigos de hallazgo, `cli/commands/`, tests existentes, `tests/test_clean_code_rules.py`, `contracts/layers.toml`, docs de stores check. Cambios previstos: guarda por documento en el diagnóstico, código nuevo, dedupe entre subsistemas, tests H1/H2/H3, docs y CHANGELOG. Dependencias: pydantic, infraestructura de hallazgos (`core/finding.py`). Validaciones futuras: tests tocados, suite completa archivo por archivo desde /dev/shm con wait-pytest, test_clean_code_rules, tools/check.sh --fast.

FUTURO
El coordinador ejecuta los 7 pasos del workflow en clon limpio; un humano decide el nombre final del código de hallazgo y la vía (bisect vs lectura) si no se resuelve; la guarda preventiva de deskops es otra tarea.
