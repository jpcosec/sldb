## REFORMULACION
- **Propósito:** añadir a sldb MCP un gancho público para que una extensión registre validadores de lote que corran antes de `propose_changes` y `apply_changes`, de modo que IR03b pueda imponer reglas de dominio (`claims_verified`).
- **Resultado:** `ServerContext.add_batch_validator(fn)` y `BatchValidator`; `build_server` pasa el contexto a `WriteTools`; propose/apply ejecutan todos los validadores; con errores responden `apply.rejected("domain", ...)` sin escribir; con solo alertas añaden `domain_alerts`; contrato documentado, tres tests nuevos, extensión de ejemplo y CHANGELOG.
- **Repo:** sldb, workspace desk; el commit lo hace el coordinador con `deskops closeout commit`.
- **Límites:** no mover `sldb.mcp` a `sldb.api`, no cambiar el sellado de propuestas, no tocar el repo IR; solo los archivos listados.

## AMBIGUEDADES
1. **Excepciones de validadores.** Cita: «si algún finding tiene level "error", responden rechazado con esos findings y no escriben». No dice qué ocurre si `fn` lanza; obligaría a inventar si se propaga, se convierte en finding `error` o se registra como señal.
2. **Contenido de `subject`.** Cita: «Un finding es {"code", "level", "what", "subject"}». No define qué valor lleva `subject` (nombre, `Modelo:nombre`, dirección `sldb://...`); obligaría a inventarlo.
3. **Documento destino del contrato.** Cita: «El contrato se documenta en docs/architecture/mcp.md» frente a «grep "mcp" docs/architecture para elegir el doc donde va el contrato». Obliga a decidir cuál manda.
4. **Re-registro.** Cita: «context.add_batch_validator(fn)». No dice si añadir dos veces el mismo `fn` lo duplica; obligaría a inventar la política.
5. **Encabezado del CHANGELOG.** Cita: «bajo el encabezado "## 0.1.13 — not released yet"». Si no existe, no se indica crearlo; obligaría a inventar.

## DRY-RUN
- **Lecturas:** `server.py`, `extension.py`, `context.py`, `write/tools.py`, `write/apply.py`, `tests/mcp/test_extension.py`, `tests/mcp/example_extension.py`, `docs/architecture/mcp.md`, `CHANGELOG.md`.
- **Cambios previstos:** `BatchValidator` en `extension.py`; lista y método en `context.py`; contexto a `WriteTools` en `server.py`; ejecución de validadores en propose/apply; doc, tests, ejemplo y CHANGELOG.
- **Dependencias:** pytest, fixtures/helpers de los tests nombrados, deskops.
- **Validaciones futuras:** `TMPDIR=/dev/shm pytest -q tests/mcp/test_extension.py` y `TMPDIR=/dev/shm pytest -q tests/mcp/test_write_tools.py`; auditoría de contrato, CHANGELOG y closeout.

## FUTURO
El nodo es ejecutable (`task.code`), no agregado. Un ejecutor implementa y valida; el coordinador commitea con `deskops closeout`; el aviso a IR lo envía el ejecutor o va al informe; verificar el encabezado real del CHANGELOG y el doc destino queda del lado del ejecutor/humano.
