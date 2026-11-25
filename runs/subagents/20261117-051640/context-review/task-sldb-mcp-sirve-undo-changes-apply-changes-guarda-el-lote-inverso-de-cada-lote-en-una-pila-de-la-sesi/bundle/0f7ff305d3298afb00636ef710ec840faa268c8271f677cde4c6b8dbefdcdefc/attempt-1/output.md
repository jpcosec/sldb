REFORMULACION
Propósito: servir `undo_changes` en sldb mcp (niveles 1-2), apoyándose en `BatchReport.inverse` que `apply_batch` ya devuelve (átomo 83c60239). Resultado: cada `apply_changes` exitoso apila su inverso en una pila en memoria, por sesión del servidor; `undo_changes(steps=1)` reaplica los N inversos más recientes vía `apply_batch` con las mismas guardas, rechaza sin escritura parcial ante conflicto y deja la pila intacta desde el lote fallido; se retira de `PENDING_TOOLS` y de `pending.py`. Repo: /mnt/ssd/proyectos/SLDB_1 (`src/sldb/mcp/write/`, `signals/catalog.py`, `tests/mcp/test_write_tools.py`, `docs/architecture/mcp.md`, `CHANGELOG.md`). Límites: sin persistencia entre sesiones, sin redo.

AMBIGUEDADES
1. "dry-run si las demás tools de escritura lo tienen": `pending.py` declara `dry_run` no público; no consta que exista ya en tools de escritura. Obliga a inventar si implementarlo.
2. "la pila vive en la sesión del servidor" / "por sesión, en memoria": no hay objeto de sesión en los archivos dados. Obliga a inventar dónde vive y cómo se identifica la sesión.
3. "un fallo deja la pila como estaba desde ese lote" (para `steps>1`): no dice si los lotes ya deshechos antes del fallo siguen deshechos. Obliga a inventar atomicidad multi-lote.
4. "devuelve lo deshecho": la forma de la respuesta no está definida.
5. Contradicción: el átomo afirma que `apply_batch` devuelve `inverse`; `pending.py` ("undo") dice "apply_batch does not return the inverse batch with guards yet". Obliga a decidir qué texto retirar.
6. "se rechaza con ConflictError": hoy el MCP traduce a `rejected["stale"]`; no queda claro si la tool devuelve excepción o dict.

DRY-RUN
Lecturas: los seis archivos listados, más `batch_inverse.py`, `pendings.py`, `tools.py` y el estado de sesión del servidor. Cambios previstos: módulo de pila, tool `undo_changes`, retirada de `PENDING_TOOLS`/`pending`, tests, docs y CHANGELOG. Dependencias: `report.inverse` y `apply_batch` para reaplicar. Validaciones futuras: los cinco comandos de Validation. Nada se ejecuta.

FUTURO
Un humano/coordinador decide identidad de sesión, forma de respuesta y semántica multi-lote; otro nodo ejecuta y corre las validaciones; el cierre retira `pending` y avisa a IR.
