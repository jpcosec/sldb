## REFORMULACION

Nodo ejecutable `task.code`, no agregado. **Propósito:** servir `undo_changes` en sldb mcp: `apply_changes` apilará en memoria, por sesión del servidor, el `report.inverse` de cada lote exitoso; `undo_changes(steps=1)` aplicará los inversos con `apply_batch` y guardas de conflicto. **Resultado:** tool registrada, pila operativa, `undo_changes` fuera de pendientes/no servidos, pruebas y documentación actualizadas. **Repo:** `/mnt/ssd/proyectos/SLDB_1`. **Límites:** sin persistencia entre sesiones ni redo.

## AMBIGUEDADES

1. «la pila vive en la sesión del servidor» / «el estado de sesión del servidor»: no identifica módulo, API ni ciclo de vida concreto; obligaría a inventar dónde se guarda y cómo se aísla por sesión.
2. «un fallo deja la pila como estaba desde ese lote»: no define qué ocurre con `steps>1` si falla un inverso intermedio; obligaría a inventar si hay deshacer parcial, rollback o compensación.
3. «dry-run si las demás tools de escritura lo tienen»: no enumera cuáles ni el criterio exacto; obligaría a decidir por inspección qué significa “tenerlo”.
4. «aviso a IR (IR04b se reduce a verificarlo desde specIR)»: no fija canal ni formato del aviso; obligaría a inventar la notificación.

## DRY-RUN

**Lecturas:** `src/sldb/mcp/write/apply.py`, `pending.py`, `pendings.py`, `tools.py`, `signals/catalog.py`, estado de sesión del servidor, `src/sldb/api/documents/batch_inverse.py`, tests y docs citados. **Cambios previstos:** módulo de pila inversa, hook en `apply_changes`, tool `undo_changes`, retirada de pendientes/catálogo, dry-run condicionado, tests, `docs/architecture/mcp.md` y `CHANGELOG.md`. **Dependencias:** `apply_batch`, `report.inverse`, `ConflictError`, estado de sesión, extra `mcp`, regla de 80 líneas. **Validaciones futuras:** ejecutar los cinco comandos de Validation y `tools/check.sh --fast`. Sin ejecución.

## FUTURO

El ejecutor producirá implementación, tests, docs, CHANGELOG y commit; otro nodo o un humano validará el cierre y IR verificará IR04b desde specIR.
