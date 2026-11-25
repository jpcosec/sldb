## REFORMULACION

Encargo ejecutable (`task.code`, nodo `ritual-execution`): corregir la violación de clean code introducida por e55d872f — `process_model_sections` en `src/sldb/store/section_sync.py` tiene 13 líneas de lógica (máx. 10). Propósito: que `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasen sin cambiar comportamiento ni API pública (reexport). Resultado: extraer `_warn_missing(report, start, model_name)` agrupando `missing_paths` nuevos, `missing_summary` y `logger.warning`; si el archivo supera 80 líneas efectivas, mover `missing_summary` a un módulo vecino reexportándola; una línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`. Límites: no tocar tests de comportamiento ni otras violaciones (anotarlas en `result-summary.md`); los nombres importados hoy desde el módulo original siguen importándose desde ahí.

## AMBIGUEDADES

1. "si section_sync.py pasa de 80 líneas" — no define "líneas efectivas" (¿incluye docstrings, imports?): obliga a inventar la métrica o inferirla del test.
2. "mover missing_summary a un módulo vecino reexportándola" — no nombra módulo ni ruta: obliga a inventar nombre y ubicación.
3. "se anotan en result-summary.md" — sin ruta ni formato: obliga a inventar ubicación y esquema.
4. "_warn_missing(report, start, model_name)" — no dice si absorbe el guard `if missing :=` ni qué retorna: obliga a inferir equivalencia exacta.
5. "Una línea en CHANGELOG.md ... que diga que es un arreglo de clean code" — redacción exacta no fijada.

## DRY-RUN

- Lecturas: TaskDoc, rituales execution/testing/closeout/phase, átomo, `section_sync.py`, `tests/test_clean_code_rules.py`, `tests/store/test_semantic_rebuild.py`, `CHANGELOG.md`, `git show e55d872f`.
- Cambios previstos: añadir `_warn_missing` en `section_sync.py` y sustituir el bloque de aviso; opcionalmente módulo vecino con `missing_summary` reexportada; línea de CHANGELOG.
- Dependencias: `uv run --frozen` con extras `code`/`dev`, `TMPDIR=/dev/shm`, `tools/check.sh`.
- Validaciones futuras (sin ejecutar): los tres comandos del TaskDoc; `git diff` sin cambios en tests de comportamiento; commit atómico y closeout.

## FUTURO

`deskops` actualiza el Board y ejecuta closeout; el ritual de testing valida; un humano o el nodo de closeout decide el mensaje de commit y la aceptación; el ritual de phase cierra el lote.
