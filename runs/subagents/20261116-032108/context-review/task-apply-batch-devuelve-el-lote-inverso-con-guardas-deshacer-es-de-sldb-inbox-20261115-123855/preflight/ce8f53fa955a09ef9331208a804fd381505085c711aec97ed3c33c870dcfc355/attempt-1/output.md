## REFORMULACION
Nodo ejecutable `task.code` en el repo `/mnt/ssd/proyectos/SLDB_1/sldb` (TaskDoc de desk). Propósito: que `apply_batch` devuelva el lote inverso con guardas y que deshacer sea responsabilidad de sldb, no de consumidores. Resultado: `BatchReport` incluye un lote en la forma que acepta `apply_batch`; `apply_batch(report.inverse)` restaura el estado previo del store, cubriendo documentos y aristas; cada operación inversa lleva `expected_source_hash` del estado dejado por el lote; un cambio ajeno intermedio produce `ConflictError` sin escritura parcial; se registra procedencia. Límites: no expone la tool MCP `undo_changes` (otra tarea), no decide por consumidores/UI y deja abierta la decisión sobre snapshots de `Transaction`.

## AMBIGUEDADES
1. “BatchReport lleva el lote inverso, en la forma que acepta apply_batch”: no se define el esquema exacto del inverso (campos, tipos de operación, orden). Obliga a inventar el contrato o inferirlo del código.
2. “Decidir si se apoya en los snapshots que Transaction ya tiene para el rollback (pregunta de la nota)”: decisión explícitamente pendiente; obliga a elegir mecanismo sin criterio en el input.
3. “Procedencia del inverso registrada como cualquier escritura” frente a “deja el store idéntico al previo”: no aclara si “idéntico” incluye procedencia, historial o metadatos; obliga a definir igualdad lógica o byte a byte.
4. “actualizar en restaurar campos o texto previos”: no precisa si restaura todos los campos, solo los modificados, ni cómo tratar valores ausentes; obliga a inventar la semántica de actualización.

## DRY-RUN
Lecturas: TaskDoc, dependencia `task-apply-batch-guardas-expected-source-hash...`, tipos `BatchReport`/`apply_batch`, `Transaction`, tests y scripts. Cambios previstos: añadir el inverso al report, generarlo por operación, adjuntar hash post-lote, aceptar y aplicar el inverso con prevalidación atómica, registrar procedencia y tests de documentos, aristas, conflicto y ausencia de escritura parcial. Dependencias: guardas de la tarea previa, decisión sobre snapshots y MCP externo. Validaciones futuras: pytest por archivo, `tools/check.sh`, `sldb stores build --check`.

## FUTURO
La tarea dependiente aporta `apply_batch` con guardas `expected_source_hash`; otra tarea del MCP expone `undo_changes`; un humano/JP decide el uso de snapshots si sigue abierto; el revisor valida la aceptación.
