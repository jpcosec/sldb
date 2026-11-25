## REFORMULACION

Encargo ejecutable (`task.code`), no agregado. **Propósito:** restaurar clean code tras `task-carga-tolerante` (163726f2), que dejó `tools/check.sh` en rojo. **Resultado:** `src/sldb/store/edge_index/edge_index.py` y `src/sldb/api/documents/runtime_documents.py` con una clase cada uno, `src/sldb/store/query.py` con ≤80 líneas efectivas y una línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`, sin cambiar comportamiento ni API pública. **Repo:** sldb. **Límites:** solo esos archivos y módulos nuevos vecinos; no tocar tests de comportamiento ni otras violaciones; las demás se anotan en `result-summary.md`.

## AMBIGUEDADES

1. “bajar query.py a 80 líneas extrayendo un helper de la carga con rechazados a un módulo vecino”: no nombra helper, módulo ni firma; obliga a inventar qué se extrae y dónde.
2. “se anotan en result-summary.md”: no indica ruta ni formato; obliga a inventar ubicación y estructura.
3. “git diff no toca archivos de tests de comportamiento”: no enumera esos archivos; los comandos solo citan cuatro tests, pero la expresión puede abarcar más; obliga a inventar el conjunto.
4. “mover EdgeProblem (y edge_problem, ENDPOINT_NOT_A_NODE) a un módulo nuevo edge_problem.py”: la reexportación se detalla explícitamente para `InvalidDocument`, no para todos esos nombres; obliga a decidir el alcance exacto de reexports.
5. “los tests de la tarea original siguen verdes sin cambios”: no da rutas; solo identifica la tarea/commit; obliga a inferirlos desde git.

## DRY-RUN

Un ejecutor futuro leería el TaskDoc, rituales, átomo, los tres `.py`, `CHANGELOG.md` y `tests/test_clean_code_rules.py`. Crearía `edge_problem.py` con `EdgeProblem`, `edge_problem` y `ENDPOINT_NOT_A_NODE`, reexportándolos desde `edge_index.py`; crearía `invalid_document.py` con `InvalidDocument`, reexportándolo; extraería el helper de `query.py`; añadiría la línea del CHANGELOG. Dependencias: imports del paquete, `pydantic`, `dataclasses`, `__all__` y firmas existentes. Validaría con los cinco comandos indicados y `git diff` sobre tests. No se ejecuta nada.

## FUTURO

El nodo ejecutor implementa y corre validaciones; el tester las confirma; `deskops closeout` decide commit y retira la tarea del Board. Un humano debe resolver antes las ambigüedades 1–5.
