# Executor deskops-e-eda2f0fb7728 — gancho público de validadores de lote en sldb mcp

## Cambios (archivo y función)
- `src/sldb/mcp/extension.py`: nuevo alias `BatchValidator = Callable[[list[Any], Any], list[dict[str, Any]]]` junto a `Extension`, con el contrato del finding en el comentario.
- `src/sldb/mcp/context.py` (`ServerContext`): atributo `batch_validators: list[BatchValidator]` y método `add_batch_validator(validator)`.
- `src/sldb/mcp/server.py` (`build_server`): pasa `context=context` a `WriteTools`; docstring dice que las extensiones (validadores incluidos) se aplican antes de servir la primera llamada (ya ocurría: `build_server` devuelve el server antes de `run`).
- `src/sldb/mcp/write/tools.py` (`WriteTools`): `__init__` acepta `context: ServerContext | None = None` (por defecto sin validadores = comportamiento de hoy). `propose_changes` corre los validadores después de `_require` y `_check_path`, antes de construir el lote; `apply_changes` después de `require` y `sealer.check`, sobre `proposal.changes` (BatchChange). Helpers nuevos: `_domain_findings` (corre todos, sin cortar), `_has_errors`, `_domain_rejected` (`apply.rejected("domain", "<n> domain check(s) failed", findings=<todos>)`, n = cantidad de errores), `_with_alerts` (agrega `domain_alerts` al dry-run o al resultado de `run_batch` solo si hay findings).
- `tests/mcp/example_extension.py`: validador de ejemplo `domain_check` registrado con `context.add_batch_validator`, y herramienta `set_domain_check(level)` que fija qué devuelve (error/alert/nada) — necesaria para obtener una propuesta sellada que luego el validador rechace en apply.
- `tests/mcp/test_extension.py`: `EXTENSION_TOOLS` incluye `set_domain_check`; tres casos nuevos: `test_a_validator_error_blocks_propose_and_apply_and_writes_nothing`, `test_a_validator_alert_lets_the_batch_through_and_rides_in_the_answer`, `test_without_validators_propose_and_apply_answer_as_before` (server sin extensión sobre su propia copia).
- `docs/architecture/mcp.md` (autorizado por las Precisiones): subsección "Batch validators" bajo "Extension point" con el contrato estable (`Extension`, `BatchValidator`, `ServerContext.add_batch_validator`) y las formas de respuesta.
- `CHANGELOG.md`: una línea en español bajo `## 0.1.13 — not released yet`.

## Done When
- Los dos archivos de test pasan con los tres casos nuevos: test_extension 8 passed (rc=0); test_write_tools 8 passed, 1 xfailed (xfail strict preexistente, línea 157) (rc=0).
- Contrato de extensión documentado en `docs/architecture/mcp.md`.
- CHANGELOG: hecho. Commit: lo hace el coordinador con `deskops closeout commit` (no hice commit, según el brief).
- Mensaje a IR: NO enviado por mí — el cuerpo debe llevar el commit, que aún no existe, y el envío es parte del cierre. Texto propuesto para el coordinador:
  Aviso a IR: "sldb mcp: gancho público de validadores de lote" — una extensión registra `context.add_batch_validator(fn)` con `fn(changes, context) -> list[dict]` ({code, level, what, subject}); propose_changes y apply_changes lo corren antes de sellar/escribir; `error` → `rejected: "domain"` con `findings`; `alert` → `domain_alerts`. IR03b puede dejar de quitar/re-registrar propose_changes/apply_changes e importar internos de sldb.mcp. Contrato: docs/architecture/mcp.md. Commit: <sha del closeout>.

## Comandos (salida completa en validation.log)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/mcp/test_extension.py` → falló la colección por `ModuleNotFoundError: anyio` (falta el extra mcp; esta corrida no quedó en validation.log, que se reinició después).
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q <archivo>` (x2) → rc=2: `Extra mcp is not defined` según el `uv.lock` actual (modificado por cambios ajenos; no lo toqué).
- Respaldo del brief con el extra: `TMPDIR=/dev/shm uvx --from "pytest>=8" --with-editable ".[mcp,code]" pytest -q tests/mcp/test_extension.py` → rc=0 (8 passed).
- `TMPDIR=/dev/shm uvx --from "pytest>=8" --with-editable ".[mcp,code]" pytest -q tests/mcp/test_write_tools.py` → rc=0 (8 passed, 1 xfailed).

## Archivos tocados
src/sldb/mcp/context.py, src/sldb/mcp/extension.py, src/sldb/mcp/server.py, src/sldb/mcp/write/tools.py, tests/mcp/test_extension.py, tests/mcp/example_extension.py, docs/architecture/mcp.md, CHANGELOG.md (+ este informe y validation.log).

## Desvíos / dudas
- Ninguna contradicción entre pill y Precisiones; se siguió el pill (Change en propose, BatchChange en apply; `domain_alerts` en dry-run y en resultado de apply).
- `domain_alerts` se agrega a cualquier respuesta de `run_batch` cuando hay alertas (también si apply termina `stale` o `rules`), no solo a `applied: true`.
- El rechazo de dominio en apply ocurre antes del chequeo de staleness (lo hace `apply_batch`), como mandan las Precisiones.
- Entorno: `uv run --frozen` con el `uv.lock` actual no puede instalar el extra `mcp`; habría que mirarlo al cerrar (el lock lo cambió otro).
