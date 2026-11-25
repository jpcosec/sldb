## REFORMULACION
Corregir en el repo `/mnt/ssd/proyectos/SLDB_1` la violación de clean code introducida por `task-una-escritura-sections-rebuild`: `process_model_sections` en `src/sldb/store/section_sync.py` tiene 13 líneas de lógica y el máximo es 10. El resultado esperado es que `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasen sin esa violación, manteniendo comportamiento y API pública, con los tests originales verdes y sin cambios. Límites: extraer lógica a funciones privadas o módulos vecinos del mismo paquete con reexportación; tocar solo `section_sync.py`, un módulo vecino si hace falta y `CHANGELOG.md`; no cambiar comportamiento, tests de comportamiento ni otras violaciones. Es una tarea ejecutable (`task.code`), no un agregado ni paquete no ejecutable.

## AMBIGUEDADES
1. «si section_sync.py pasa de 80 líneas»: no precisa si son líneas efectivas ni cómo se mide; obligaría a inventar el criterio exacto.
2. «mover missing_summary a un módulo vecino reexportándola»: no indica nombre ni ruta del módulo; obligaría a inventarlos.
3. «los tests de la tarea original siguen verdes sin cambios»: no identifica esos tests; obligaría a decidir cuáles son.
4. «se anotan en result-summary.md»: no da ruta; obligaría a inventar su ubicación.
5. «commit.»: no define mensaje ni formato; obligaría a inventarlos.

## DRY-RUN
Lecturas previstas: TaskDoc, `src/sldb/store/section_sync.py`, `tests/test_clean_code_rules.py`, `tests/store/test_semantic_rebuild.py`, `CHANGELOG.md`, `tools/check.sh`, configuración de `uv`/pytest. Cambios previstos: extraer `_warn_missing(report, start, model_name)` conservando el aviso; si hace falta, mover `missing_summary` a un módulo vecino y reexportarla; añadir una línea de clean code bajo `## 0.1.13 — not released yet`. Dependencias: entorno `uv --frozen` con extras `code` y `dev`, `TMPDIR=/dev/shm`, pytest y `tools/check.sh`. Validaciones futuras, sin ejecutar: los tres comandos de Validation y `git diff` para confirmar que no cambiaron tests de comportamiento.

## FUTURO
El nodo verificador o tester ejecutará las validaciones y revisará el diff; el humano resolverá las ambigüedades señaladas antes de implementar y decidirá la aceptación final y el commit.
