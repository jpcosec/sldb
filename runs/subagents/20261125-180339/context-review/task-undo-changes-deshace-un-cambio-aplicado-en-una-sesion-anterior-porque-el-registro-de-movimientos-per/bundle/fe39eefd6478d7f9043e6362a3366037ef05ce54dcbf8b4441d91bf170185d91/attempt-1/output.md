## REFORMULACION

Nodo `task.code` ejecutable del repo `sldb`. Propósito: que `undo_changes` funcione entre procesos/sesiones persistiendo en el store lo necesario para revertir cada lote aplicado. Resultado: aplicado un lote con un servidor, otro proceso sobre el mismo store restaura contenido y hash del store; dos deshaceres revierten dos lotes en orden inverso; un documento modificado después se rechaza sin escribir. Superficie: `src/sldb/mcp/write/` (apply, undo) y el registro de escrituras del store. Fuera: portar MoveDoc de pron, proyecciones de sesión y cualquier interfaz.

## AMBIGUEDADES

1. «el registro de movimientos persiste en el store» frente a «el registro de escrituras ya es del sustrato»: ¿son el mismo artefacto? Obliga a inventar si se extiende el write journal o se crea otro registro, contradiciendo «no en un registro paralelo».
2. «registrado en el store con lo necesario para revertirlo»: no define esquema. Obliga a inventar before-images, identificador de lote, orden, atomicidad e idempotencia.
3. «Deshacer un lote cuyo documento cambió después se rechaza con motivo»: no fija el criterio de detección. Obliga a inventar comparación por hash, versión o journal.
4. «el hash del store al valor anterior al lote»: no define qué es el hash del store ni si incluye la reversión del propio journal.
5. «Deshacer dos veces revierte dos lotes en orden inverso»: no dice si `undo_changes` toma lote explícito o revierte el último. Obliga a inventar su firma.
6. El input promete «las pills ligadas, los átomos ligados y los archivos que el TaskDoc nombra», pero `pills`, `atoms`, `files` están vacíos y los documentos citados no aparecen. Obliga a inventar su contenido o a incumplir la precondición de ejecución.
7. «tests/test_mcp_undo_across_sessions.py» no existe en el input ni figura en `files`: obliga a decidir si crearlo es parte del alcance.

## DRY-RUN

Un ejecutor futuro, tras resolver lo anterior, leería `pron-is-archived.md`, la sección «The write journal belongs to the substrate» de `sldb-absorbs-kgdb.md`, `journal-authority.md`, `transactions.md`, `src/sldb/mcp/write/apply.py`, `undo.py`, el módulo del write journal y los tests existentes. Cambiaría apply para registrar por lote before-images y metadatos en el store; undo para leerlos desde otro proceso, verificar conflicto, aplicar inversos en orden inverso y restaurar el hash; añadiría el test nombrado. Dependencias: API transaccional y semántica de hash del store, esquema del journal y regla de conflicto. Validaría con los dos `pytest` indicados. Sin ejecutar nada.

## FUTURO

Un humano/arquitecto decide esquema del journal, regla de conflicto y definición del hash. Otro nodo implementa y añade tests; closeout commitea atómicamente y retira pills obsoletas; phase ritual cierra la fase.
