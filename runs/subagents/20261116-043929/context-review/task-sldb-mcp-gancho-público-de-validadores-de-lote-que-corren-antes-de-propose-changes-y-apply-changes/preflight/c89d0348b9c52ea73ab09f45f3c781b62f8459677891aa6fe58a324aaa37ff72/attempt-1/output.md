REFORMULACION  
Propósito: exponer en sldb MCP un gancho público para que una extensión registre validadores de lote. Resultado: `ServerContext.add_batch_validator(fn)` y `BatchValidator`; `propose_changes` y `apply_changes` ejecutan los validadores antes de escribir; findings `error` rechazan sin escribir y `alert` se devuelven sin bloquear. Repo: `/mnt/ssd/proyectos/SLDB_1`, principalmente `src/sldb/mcp`, `tests/mcp`, `docs/architecture` y `CHANGELOG.md`. Límites: no mover `sldb.mcp` a `sldb.api`, no cambiar el sellado de propuestas, no tocar el repo IR.

AMBIGUEDADES  
1. “antes de su trabajo” frente a “en apply, sobre proposal.changes”: no queda claro si en `apply_changes` hay que cargar la propuesta antes de validar o validar antes de cualquier trabajo. Obligaría a inventar el orden y el tratamiento de una propuesta inexistente.  
2. “llaman a todos los validadores” y “si algún finding tiene level "error", responden rechazado con esos findings”: no define si se ejecutan todos tras un error ni si el `detail` incluye solo errores o también alerts. Obligaría a inventar agregación y contenido del rechazo.  
3. “los de level "alert" se devuelven en la respuesta sin bloquear”: no indica campo ni forma de respuesta. Obligaría a inventar el contrato de salida.  
4. “build_server pasa el context a WriteTools (o WriteTools recibe la lista de validadores)”: deja dos diseños posibles. Obligaría a elegir una API sin criterio explícito.  
5. “en el doc donde ya se describe sldb mcp”: no nombra archivo; si el grep devuelve varios, obligaría a decidir cuál es el canónico.

DRY-RUN  
Lecturas: `server.py`, `extension.py`, `context.py`, `write/tools.py`, `write/apply.py`, tests citados y docs de arquitectura. Cambios previstos: lista y método en `ServerContext`; alias `BatchValidator` y contrato en `extension.py`; conexión de `WriteTools` con el contexto; validación en `propose`/`apply`; tests de error, alert y ausencia de validadores; ejemplo, documentación y changelog. Dependencias: forma de `apply.rejected`, carga de propuesta y orden de extensión antes de la primera llamada. Validaciones futuras: los dos `pytest` indicados, bloqueo sin escritura, alert visible y comportamiento base sin validadores.

FUTURO  
El ejecutor produce código, tests, documentación y changelog; el cierre incluye commit y aviso a IR. IR consume el contrato; un humano decide si hay que elegir entre varios documentos candidatos.
