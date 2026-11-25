## REFORMULACION

Propósito: que `propose_changes` rechace un lote antes de escribir si alguna relación viola tipos, cardinalidad o condición de su tipo. Resultado: rechazo con un motivo por violación, lote entero prevalidado como unidad, store intacto (hash sin cambio), `pendings` sin declarar esa validación como faltante y `dry_run` informando lo mismo. Repo: `/mnt/ssd/proyectos/SLDB_1/sldb`. Límites: dentro `src/sldb/mcp/write/` (propose, pendings, findings), `src/sldb/mcp/changes/assert_edge.py` y `sldb.api.apply_batch` con `dry_run`, reutilizando las comprobaciones de `check_edges`; fuera portar pron, registro persistente, deshacer entre sesiones e interfaces. Es una tarea `task.code` ejecutable, no un agregado.

## AMBIGUEDADES

1. «La validación previa usa esas mismas funciones sobre el estado que resultaría del lote» — no se define cómo proyectar ese estado sin escribir; obligaría a inventar un mecanismo de estado efímero.
2. «el hash del store no cambia» — no se especifica qué hash ni cómo calcularlo; obligaría a inventar el criterio de comparación.
3. «devuelvan cada uno un rechazo que nombra la relación y la violación» — formato del rechazo no definido; obligaría a inventar estructura y mensaje.
4. «apply_batch con dry_run informa lo mismo» — no se concreta canal ni forma de esa información.
5. «Un lote válido se comporta igual que antes» — «igual» es indeterminado; obligaría a inventar qué aspectos preservar.
6. «pendings deja de informar la validación de relaciones como faltante» — no se cita el mecanismo exacto; obligaría a inventar cómo se detecta ese faltante.

## DRY-RUN

Lecturas: `docs/architecture/rules.md`, `edges.md`, `mcp.md`; `src/sldb/mcp/write/{propose,pendings,findings}`; `src/sldb/mcp/changes/assert_edge.py`; `sldb.api.apply_batch`; `check_edges` y tests existentes. Cambios previstos: prevalidación en propose/assert_edge sobre estado proyectado, `dry_run` en apply_batch, ajuste de pendings, nuevo `tests/test_mcp_propose_rejects_invalid_edges.py`. Dependencias: `check_edges` y `RelationTypeDoc`. Validaciones futuras: pytest del test nuevo y `-k "mcp or apply_batch or check_edges"`, comprobación de hash y lote mixto.

## FUTURO

Un nodo ejecutor implementará y correrá las pruebas. Un humano decidirá formato del rechazo, definición del hash y alcance de «igual que antes» si las ambigüedades persisten.
