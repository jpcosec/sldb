## REFORMULACION
Encargo ejecutable en el repo SLDB_1 (`/mnt/ssd/proyectos/SLDB_1`): añadir a `sldb mcp` un gancho público para que una extensión registre validadores de lote mediante `ServerContext.add_batch_validator(fn)`. Resultado: `propose_changes` y `apply_changes` ejecutan todos los validadores antes de escribir; si hay findings `error`, responden `apply.rejected("domain", ...)` con los findings y no escriben; las `alert` no bloquean y se exponen como `domain_alerts`. Incluye tipo `BatchValidator`, conexión de `WriteTools` con el contexto, tests (error bloquea, alerta pasa, sin validadores igual que hoy), extensión de ejemplo, contrato en documentación de arquitectura y entrada de CHANGELOG. Límites: no mover `sldb.mcp` a `sldb.api`, no cambiar el sellado de propuestas, no tocar el repo IR, no hacer push; el commit lo hace el coordinador.

## AMBIGUEDADES
1. «El contrato se documenta en docs/architecture/mcp.md» frente a «grep "mcp" docs/architecture para elegir el doc donde va el contrato». Obliga a decidir si el destino es exactamente `mcp.md` o el doc que aparezca por grep.
2. «apply.rejected("domain", ...) con los findings en detail» frente a «apply.rejected("domain", "<n> domain check(s) failed", findings=<todos los findings...>)». Obliga a decidir si los findings van dentro de `detail` o como kwarg `findings`; leer `apply.py` debería resolverlo, pero el input no lo fija.
3. «"<n> domain check(s) failed"» no concreta si se conserva literalmente `check(s)` o se pluraliza según `n`. Obliga a inventar el texto exacto del mensaje.

## DRY-RUN
Lecturas: `src/sldb/mcp/server.py`, `extension.py`, `context.py`, `write/tools.py`, `write/apply.py`, tests `test_extension.py`, `test_write_tools.py` y `example_extension.py`; `docs/architecture/mcp.md`; `CHANGELOG.md`. Cambios previstos: lista y método en `ServerContext`; `BatchValidator` en `extension.py`; pasar el contexto a `WriteTools`; validar en `propose_changes` tras `_require` y `_check_path`, y en `apply_changes` tras `require` y `sealer.check`, sobre `proposal.changes`; tests, ejemplo, doc y CHANGELOG. Dependencias: firma actual de `WriteTools`, API de rechazo y helpers de store. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/mcp/test_extension.py` y `TMPDIR=/dev/shm pytest -q tests/mcp/test_write_tools.py`. Sin ejecutar nada.

## FUTURO
El coordinador asigna el `<run-dir>`, crea el commit de cierre y decide el push. El repo IR recibe o no el aviso; si no está registrado, el ejecutor lo anota en el informe. La aceptación final del cambio queda fuera de este nodo.
