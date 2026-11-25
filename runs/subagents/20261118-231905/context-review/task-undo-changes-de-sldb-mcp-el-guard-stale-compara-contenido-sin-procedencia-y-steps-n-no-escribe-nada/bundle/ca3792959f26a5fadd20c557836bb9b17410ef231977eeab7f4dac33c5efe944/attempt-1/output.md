## REFORMULACION

Propósito: corregir `undo_changes` de sldb MCP en tres frentes: (1) documentar el contrato de undo como “mismo contenido salvo procedencia”; (2) hacer que el guard stale compare contenido sin el bloque de procedencia; (3) hacer `undo_changes(steps=N)` atómico, validando la cadena antes de escribir y sin tocar la pila si algo se rechaza. Resultado: tests nuevos que fallan antes y pasan después, contrato en docs/CHANGELOG y nota a IR. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: dentro `src/sldb/mcp`, `src/sldb/api` (guard y pila), `tests/mcp`, CHANGELOG y `docs/architecture/mcp.md`; fuera cambiar el formato de procedencia o `source_hash` del índice, y specIR.

## AMBIGUEDADES

1. “el guard stale compara el contenido del documento sin el bloque de procedencia” y “hash del payload sin el bloque sldb de procedencia”: no precisa qué claves se excluyen (¿solo `sldb.at`/`via`? ¿`authority`, `by`?) ni si se elimina el bloque entero. Obliga a inventar la función de hash.
2. “encadenar los N inversos… en una sola llamada a apply_batch” frente a “apply_batch… chequea los guards y escribe… todo o nada”: no aclara si los guards se evalúan contra el estado previo o secuencialmente contra el estado que deja cada inverso. Obliga a inventar semántica de guards encadenados.
3. “con un rechazo forzado en el más viejo”: no indica cómo forzarlo (fixture, hash manipulado, monkeypatch) ni qué rechazo esperar.
4. “dejar el store y la pila como estaban”: no define cómo se verifica la pila intacta (API pública vs. introspección).

## DRY-RUN

Lecturas: `src/sldb/mcp/write/undo.py`, `src/sldb/api/documents/batch_inverse.py`, `apply_batch.py`, `tests/mcp`, `docs/architecture/mcp.md`, CHANGELOG y evidencia IR (`result-summary.md`, `undo-run3.log`, `test_mcp_undo.py`). Cambios previstos: función única de hash de contenido en `src/sldb/api/documents`; guard `expected_content_hash` en el inverso y su chequeo en `apply_batch`; encadenado de inversos y pop condicionado; dos tests nuevos; docs y CHANGELOG. Dependencias: semántica de guards de `apply_batch` bajo `store_lock`, formato de la pila y relajación de validación en IR04b. Validaciones futuras: `pytest tests/mcp` local; suite completa y `selfdoc check` por integrate.

## FUTURO

Integrate ejecuta `pytest -n 4` y `sldb selfdoc check`; un humano decide commit/closeout con `Task-Id`; IR recibe la nota y relaja su validación; IR04b se desbloquea.
