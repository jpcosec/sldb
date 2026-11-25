REFORMULACION
Propósito: que `undo_changes` revierta lotes aplicados por otro proceso o sesión, apoyándose en el registro persistente del store y no en memoria. Resultado: cada lote aplicado deja en el store información suficiente para revertirlo y `undo_changes` funciona tras reiniciar. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: dentro `src/sldb/mcp/write/` (apply, undo) y el registro de escrituras; fuera MoveDoc de pron, proyecciones de sesión e interfaces. Es una tarea ejecutable de código, no un agregado.

AMBIGUEDADES
1. “el registro de movimientos persiste en el store” / “registro de escrituras ya es del sustrato”: no aclara si son el mismo artefacto; obligaría a inventar su equivalencia.
2. “cada lote aplicado quede registrado en el store con lo necesario para revertirlo”: no define frontera de lote, esquema, retención ni atomicidad; obligaría a inventar el contrato del journal.
3. “hash del store al valor anterior al lote”: no define algoritmo, canonicalización ni si incluye la entrada de undo; obligaría a inventar la semántica del hash.
4. “Deshacer un lote cuyo documento cambió después”: no define detección —versión, hash, mtime— ni qué cambios cuentan; obligaría a inventar la política de conflicto.
5. “desde un proceso distinto del que lo aplicó”: no fija concurrencia, bloqueo ni store concreto; obligaría a inventar garantías multiproceso.
6. “journal-authority.md y transactions.md”: rutas incompletas; obligaría a inventar su ubicación.

DRY-RUN
Lecturas: TaskDoc, ADR, documentos de journal y transacciones, `apply`/`undo` y registro del store. Cambios previstos: persistir metadatos de reversión por lote, adaptar `undo` para leerlos entre procesos, detectar conflicto y abortar sin escritura, añadir tests. Dependencias: journal del sustrato, store persistente y semántica transaccional existentes. Validaciones futuras: `pytest` sobre `test_mcp_undo_across_sessions.py` y `tests -k "mcp and undo"`; escenario aplicar/cerrar/reabrir/undo, doble undo inverso y rechazo sin escritura.

FUTURO
Otro nodo implementará código y tests; un humano decidirá, si no está documentado, granularidad de lote, semántica del hash y política de conflicto.
