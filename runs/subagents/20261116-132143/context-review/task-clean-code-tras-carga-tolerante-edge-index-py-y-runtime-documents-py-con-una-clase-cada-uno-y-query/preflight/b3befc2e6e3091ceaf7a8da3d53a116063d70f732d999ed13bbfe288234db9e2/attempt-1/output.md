# REFORMULACION

**Propósito:** corregir violaciones de clean code introducidas por task-carga-tolerante (163726f2) en el repo SLDB_1, sin alterar comportamiento ni API pública.
**Resultado:** `edge_index.py` y `runtime_documents.py` con máximo 1 clase cada uno; `query.py` con ≤80 líneas efectivas; reexports desde los módulos originales; una línea en CHANGELOG bajo `## 0.1.13 — not released yet`.
**Repo:** `/mnt/ssd/proyectos/SLDB_1`.
**Límites:** no cambiar comportamiento, tests de comportamiento ni otras violaciones; anotar en `result-summary.md` las ajenas. Extracciones a módulos nuevos en el mismo paquete. Validación con pytest y `tools/check.sh --fast`.

# AMBIGUEDADES

1. «bajar query.py a 80 líneas extrayendo un helper de la carga con rechazados a un módulo vecino» — no se nombra el helper ni el módulo. Obliga a inventar nombre de función, nombre de archivo y qué bloque exacto se mueve.
2. «los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport)» — no se enumera el conjunto de símbolos; obliga a inferirlo del código o de los tests.
3. «tests/test_clean_code_rules.py y bash tools/check.sh --fast pasan sin la violación de task-carga-tolerante» — no se define cómo aislar esa violación si check.sh reporta otras. Obliga a decidir criterio de atribución.

# DRY-RUN

**Lecturas:** los tres archivos fuente, `tests/test_clean_code_rules.py`, tests de validación, `CHANGELOG.md`, `tools/check.sh`, y `git diff`/historial de 163726f2.
**Cambios previstos:** crear `sldb/store/edge_index/edge_problem.py` (EdgeProblem, edge_problem, ENDPOINT_NOT_A_NODE) y `sldb/api/documents/invalid_document.py` (InvalidDocument); reexportar desde los originales; extraer helper de query.py a módulo vecino; añadir línea de CHANGELOG.
**Dependencias:** `uv run --frozen --extra code --extra dev`, entorno TMPDIR=/dev/shm, permisos de escritura en src y CHANGELOG.
**Validaciones futuras (no ejecutadas):** los cinco comandos de Validation, más `git diff` para confirmar que no se tocaron tests de comportamiento.

# FUTURO

- Un ejecutor aplicará las extracciones y correrá las validaciones.
- Un nodo tester verificará los cinco comandos y el diff.
- Un humano decidirá el commit y si las violaciones ajenas requieren tarea aparte.
