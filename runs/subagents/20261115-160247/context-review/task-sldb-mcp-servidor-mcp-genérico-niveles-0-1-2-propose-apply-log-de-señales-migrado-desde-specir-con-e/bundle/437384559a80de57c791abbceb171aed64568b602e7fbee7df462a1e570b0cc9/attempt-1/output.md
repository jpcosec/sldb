## REFORMULACION
Propósito: migrar a sldb el servidor MCP genérico de specIR, porque “nunca reimplementar en un consumidor lo que es de sldb”. Resultado: `sldb mcp --store <dir> --level 0|1|2 --actor <quien>` por stdio, extra opcional `mcp`, tools de lectura, `propose_changes`/`apply_changes`, log de señales y punto de extensión para consumidores. Repo: sldb; origen: repo IR en los commits citados. Límites: migrar, no reescribir; quitar lo específico de specIR; no implementar `undo_changes`; niveles fijados al arrancar; sin mocks; log fuera de documentos trackeados; validaciones indicadas. Es una tarea ejecutable, no un agregado ni paquete no ejecutable.

## AMBIGUEDADES
1. “por ejemplo list_signals” frente a “y list_signals” en Done When: no queda claro si el nombre es obligatorio. Obligaría a inventar nombre/API de la tool del log.
2. “por ejemplo build_server con un registro de extensiones”: la firma y el contrato del registro no están definidos. Obligaría a inventar la API pública de extensión.
3. “nivel 1 contenido, nivel 2 reglas como dato”: no se explicita si nivel 2 también puede escribir contenido o solo reglas. Obligaría a inventar la matriz exacta de permisos por nivel.
4. “Cada entrada lleva momento, tool, argumentos, clase de señal, sugerencias y actor si lo hay”: no hay catálogo de clases ni formato de serialización. Obligaría a inventar taxonomía y esquema del log.

## DRY-RUN
Lecturas previstas: TaskDoc, rituales, Board, `contracts/layers.toml`, `pyproject.toml`, CLI, `sldb.api.apply_batch`, `sldb.api.matching`, y el paquete MCP de specIR en los commits indicados con sus tests y fixtures.
Cambios previstos: copiar módulos MCP y adaptar imports; registrar `sldb mcp` y extra perezoso; portar tests; añadir log y `list_signals`; añadir extensión con tool de ejemplo; documentar `undo_changes` como pendiente; actualizar docs/CHANGELOG.
Dependencias: `mcp>=2.2` opcional, `sldb.api`, cliente MCP real por stdio, copia aislada del store, inbox 20261115-123855 solo para declarar el pendiente.
Validaciones futuras: pytest por archivo con `TMPDIR=/dev/shm`, `tools/check.sh`, `sldb stores build --check`, `deskops graph missing`, y digests antes/después para probar que leer y registrar señales no escriben.

## FUTURO
El worker decide y justifica dónde vive el log. El operador fija nivel y actor. Otro nodo o JP resolverá el inverso de `apply_batch` en el inbox 20261115-123855. specIR registrará sus tools de dominio sobre el servidor de sldb.
