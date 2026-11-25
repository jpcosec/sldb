REFORMULACION

Corregir una violación de clean code introducida por task-sldb-mcp-gancho en `src/sldb/mcp/write/tools.py`: `propose_changes` tiene 11 líneas de lógica y el máximo es 10. Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan, sin cambiar comportamiento ni API pública, y los tests de la tarea original siguen verdes sin modificarse. Repo: SLDB_1. Límites: extraer funciones o clases a módulos nuevos del mismo paquete con reexport desde el original; extraer la corrida de validadores de dominio y la respuesta de rechazo (o el armado del lote sellado) a una función/método privado, compartido con `apply_changes` si aplica; una línea en `CHANGELOG.md` bajo `## 0.1.13 — not released yet`; no tocar comportamiento, tests ni otras violaciones (anotarlas en result-summary.md); commit.

AMBIGUEDADES

1. "o el armado del lote sellado": ofrece dos alternativas de extracción sin criterio para elegir; obligaría a inventar cuál corresponde.
2. "compartida con apply_changes si aplica": no define cuándo aplica; obligaría a decidir si `apply_changes` usa la misma lógica.
3. "módulos nuevos junto al original (mismo paquete)": no indica nombres, cantidad ni responsabilidad de cada módulo.
4. "los nombres que hoy se importan desde el módulo original se siguen importando desde ahí (reexport)": no especifica el mecanismo de reexport (`__all__`, import alias, etc.).
5. "si check.sh muestra otras, se anotan en result-summary.md": no da ruta ni formato de `result-summary.md`.
6. "Una línea en CHANGELOG.md": no fija el texto exacto; obligaría a redactarlo.

DRY-RUN

Lecturas: `src/sldb/mcp/write/tools.py`, `tests/test_clean_code_rules.py`, `tests/mcp/test_extension.py`, `tests/mcp/test_write_tools.py`, `CHANGELOG.md`, `tools/check.sh` y `git diff`. Cambios previstos: crear módulo(s) privados junto a `tools.py` con la corrida de validadores y la respuesta de rechazo; reducir `propose_changes` a ≤10 líneas de lógica; reexportar nombres públicos en `tools.py`; añadir la línea del CHANGELOG; commit. Dependencias: `uv`, extras `mcp`, `code` y `dev`, `pytest`. Validaciones futuras: los cuatro comandos de Validation; `git diff` para confirmar que no cambiaron tests de comportamiento; `tools/check.sh --fast`.

FUTURO

Decide un humano u otro nodo: nombres y número de módulos extraídos, si `apply_changes` comparte la extracción, redacción exacta del CHANGELOG y autorización del commit. El tester valida los comandos de Validation.
