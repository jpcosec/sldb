## REFORMULACION

Propósito: abrir un gancho público para que una extensión (specIR) imponga reglas de dominio antes de escribir vía MCP (IR05 D2-E: un agente no escribe verificación). Resultado: `BatchValidator` y `ServerContext.add_batch_validator(fn)`; `build_server` pasa el `ServerContext` a `WriteTools`, que lee `context.batch_validators` en cada llamada y las corre en `propose_changes` y `apply_changes`; un finding `level:"error"` produce rechazo `apply.rejected("domain", …)` con todos los findings y no escribe; las alertas se devuelven en la respuesta. Además: tests en `tests/mcp/test_extension.py`, validador de ejemplo en `example_extension.py`, contrato en `docs/architecture/mcp.md`, CHANGELOG y aviso a IR. Repo: SLDB_1 (`src/sldb`, `tests/mcp`, `docs/architecture`), nunca el repo IR. Límites: no mover `sldb.mcp` a `sldb.api`, no cambiar el sellado, no tocar IR; commit y push fuera del ejecutor.

## AMBIGUEDADES

1. "un rechazo usa apply.rejected("domain", ...) con los findings en detail" / "findings=<todos los findings…>" — no se da la firma de `apply.rejected` ni la forma de `detail` (lista o `{"findings": [...]}`); obliga a inventar el contrato de `detail` que el test fijará.
2. "propose_changes y apply_changes … responden rechazado con esos findings" — `propose_changes` no usa `apply.run_batch`; no se dice si reutiliza `apply.rejected` ni qué forma tiene esa respuesta (¿`{"dry_run": True, "written": False, "rejected": …}`?). Obliga a inventar el esquema del rechazo en propose.
3. "la respuesta normal gana una clave "domain_alerts"" — no aclara si aplica al dict del dry-run, al resultado de apply, o a ambos; obliga a elegir y a fijarlo en tests.
4. "fn(changes, context)" frente a "en apply, sobre proposal.changes" — no dice si los validadores reciben `Change` o dicts en apply; obliga a asumir tipos.
5. Validación nombra `tests/mcp/test_write_tools.py`, pero `files` no lo incluye y "los tres casos nuevos" no indica en qué archivo va cada caso; obliga a decidir el reparto de tests.

## DRY-RUN

Lecturas: `server.py`, `extension.py`, `context.py`, `write/tools.py`, `write/apply.py` (firma `rejected`), `changes.py`, `tests/mcp/test_extension.py`, `test_write_tools.py`, `example_extension.py`, helpers `mcp_session`/`mcp_world`, `docs/architecture/mcp.md`, CHANGELOG. Cambios previstos: lista y método en `context.py`; alias `BatchValidator` en `extension.py`; `WriteTools(context)` en `server.py`; validadores en `propose_changes` (tras `_require`/`_check_path`, antes del lote) y `apply_changes` (tras `require` y `sealer.check`); corrida completa de todos; rechazo con errores+alertas o clave `domain_alerts`; tests, ejemplo, doc, CHANGELOG. Dependencias: firma de `apply.rejected`, orden respecto a `sealer.check`, fixtures de store existentes. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/mcp/test_extension.py` y `…/test_write_tools.py`; closeout verifica commit y árbol limpio. Nada ejecutado.

## FUTURO

El ejecutor produce `runs/subagents/<run-dir>/result-summary.md` y el aviso a IR (o su línea "Aviso a IR" si el repo no está registrado). El coordinador hace `deskops closeout commit` con mensaje corto y decide el push; un humano valida el contrato público antes de que specIR lo consuma.
