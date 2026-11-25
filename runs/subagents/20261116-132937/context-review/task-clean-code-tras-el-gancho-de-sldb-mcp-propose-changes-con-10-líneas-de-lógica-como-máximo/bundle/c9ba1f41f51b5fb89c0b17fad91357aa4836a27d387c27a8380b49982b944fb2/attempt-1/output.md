## REFORMULACION

Propósito: corregir la violación de clean code introducida por task-sldb-mcp-gancho: `propose_changes`, en `src/sldb/mcp/write/tools.py`, tiene 11 líneas de lógica frente al máximo de 10. Resultado: `tests/test_clean_code_rules.py` y `bash tools/check.sh --fast` pasan, con el mismo comportamiento y API pública; los tests de comportamiento siguen verdes sin cambios; una línea en `CHANGELOG.md` bajo 0.1.13. Repo: SLDB_1. Límites: solo `tools.py`, módulos nuevos del mismo paquete y `CHANGELOG.md`; no cambiar comportamiento, tests de comportamiento ni otras violaciones (solo anotarlas).

## AMBIGUEDADES

1. “Extraer la corrida de validadores de dominio y la respuesta de rechazo (o el armado del lote sellado) a un método o función privada” ofrece dos alternativas; elegir una obliga a inventar el criterio.
2. “compartida con apply_changes si aplica”: no define cuándo aplica; obliga a inventar el criterio de compartición.
3. “si check.sh muestra otras, se anotan en result-summary.md”: no indica ruta ni formato; obliga a inventar ubicación y esquema.
4. “Una línea en CHANGELOG.md ... que diga que es un arreglo de clean code”: no fija texto exacto; obliga a inventar la redacción.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout, átomo, `tools.py`, `tests/test_clean_code_rules.py`, `tests/mcp/test_extension.py`, `tests/mcp/test_write_tools.py`, `CHANGELOG.md`, `tools/check.sh`, `git status/diff`. Cambios previstos: localizar las 11 líneas de `propose_changes`; extraer a función o método privado la corrida de validadores y el rechazo, o el sellado, creando un módulo hermano en `sldb/mcp/write`; reexportar desde `tools.py`; añadir la línea de CHANGELOG. Dependencias: `sldb.api`, `changes`, `mutability`, `write.apply/pendings/propose`, `PENDING`, `ServerContext`; sin dependencias nuevas. Validaciones futuras: los cuatro comandos de Validation; `git diff` sin tests de comportamiento; árbol limpio.

## FUTURO

Un humano decide las ambigüedades 1–4 antes de ejecutar. Otro nodo ejecutor implementa y corre las validaciones; testing/closeout verifica, registra otras violaciones, actualiza CHANGELOG y hace el commit. Este revisor no ejecuta nada.
