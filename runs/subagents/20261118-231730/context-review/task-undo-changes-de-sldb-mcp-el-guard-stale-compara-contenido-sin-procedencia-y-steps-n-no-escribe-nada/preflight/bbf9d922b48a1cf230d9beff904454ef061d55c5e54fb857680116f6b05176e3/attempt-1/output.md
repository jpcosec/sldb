REFORMULACION

Encargo ejecutable (task.debug, no agregado ni paquete): en el repo sldb (`/mnt/ssd/proyectos/SLDB_1/sldb`) corregir `undo_changes` de sldb-mcp. Propósito: desbloquear IR04b. Resultado observable: (1) contrato de undo documentado como “mismo contenido salvo procedencia” —deshacer re-sella `sldb.at`, `via` y hashes derivados—; (2) el guard stale compara contenido sin bloque de procedencia; (3) `undo_changes(steps=N)` valida toda la cadena antes de escribir: si un paso se rechaza, `written: False` y pila intacta. Superficie: `src/sldb/mcp/write/undo.py`, `src/sldb/api/documents/batch_inverse.py`, `src/sldb/api/documents/apply_batch.py`, tests/mcp, `docs/architecture/mcp.md`, CHANGELOG. Límites: no cambiar formato de procedencia ni `source_hash` del índice; specIR fuera. Entregable: dos tests nuevos que fallen antes, commit con Task-Id y aviso a IR.

AMBIGUEDADES

1. “el contenido del documento sin el bloque de procedencia”: no define qué es el bloque (¿todo `sldb`?, ¿solo `at`/`via`/`authority`?) ni canonicalización del payload. Obliga a inventar el hash.
2. “apply_batch lo chequea como guard nuevo ('expected_content_hash')”: no fija si sustituye, convive o precede a `expected_source_hash`, ni cómo trata guards mezclados. Obliga a inventar semántica.
3. “cada paso se compara contra el estado que dejaría el paso anterior”: no dice si el estado simulado re-sella procedencia ni cómo se representan documentos ausentes/creados. Obliga a inventar el simulador.
4. “los N inversos … en una sola llamada a apply_batch”: `apply_batch` recibe un lote; no aclara cómo fusionar N lotes con documentos solapados. Obliga a inventar el merge.
5. “después de su commit con Task-Id”: no especifica formato del Task-Id ni del mensaje. Obliga a inventar convención.
6. “si alguno se rechaza, no se escribe nada”: no cubre fallos distintos de `stale` ni errores de escritura. Obliga a inventar política.

DRY-RUN

Lecturas: los tres módulos citados, sus tests, `docs/architecture/mcp.md`, CHANGELOG y evidencia IR (solo lectura). Cambios previstos: helper único de hash de contenido en `api/documents`; guard `expected_content_hash` en el inverso y en `apply_batch`; encadenado y atomicidad de `steps=N`; tests (a) y (b); docs y CHANGELOG. Dependencias: `store_lock` y todo-o-nada existentes en `apply_batch`. Validaciones futuras: `pytest tests/mcp` y tests de archivos tocados; comprobar que (a) y (b) fallan antes.

FUTURO

`integrate` ejecuta suite completa (`pytest -n 4`) y `sldb selfdoc check`. IR recibe la nota y relaja la validación de IR04b. Un humano decide commit/merge.
