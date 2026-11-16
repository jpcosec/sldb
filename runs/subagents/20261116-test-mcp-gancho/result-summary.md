# Tester deskops-t-7bf3eb7dc2d7 — gancho público de validadores de lote en sldb mcp

Veredicto global: **PASA** (salida completa en `validation.log`).

## Entorno
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q <archivo>` → **no sirve para estos tests**: `ModuleNotFoundError: anyio` (falta el extra `mcp`). No es culpa de los cambios ajenos: ni `uv.lock` actual ni el de HEAD tienen el paquete `mcp` (`grep -c 'name = "mcp"'` = 0 en ambos), aunque `pyproject.toml:43` declara el extra `mcp`. Conviene regenerar el lock aparte.
- Respaldo del brief con el extra: `TMPDIR=/dev/shm uvx --from "pytest>=8" --with-editable ".[mcp,code]" pytest -q <archivo>`.

## Validation
| Comando | Resultado | Veredicto |
|---|---|---|
| pytest -q tests/mcp/test_extension.py | 8 passed, rc=0 | PASA |
| pytest -q tests/mcp/test_write_tools.py | 8 passed, 1 xfailed (preexistente), rc=0 | PASA |
| -k validator -v | los 3 casos nuevos PASSED (error bloquea propose+apply sin escribir; alert pasa y viaja en domain_alerts; sin validadores como antes) | PASA |

## Done When
- Dos archivos de test pasan con los tres casos nuevos: **PASA** (ver arriba).
- Contrato de extensión documentado: **PASA** — `docs/architecture/mcp.md` sección "Batch validators" nombra `Extension`, `BatchValidator`, `ServerContext.add_batch_validator`, orden de chequeos y forma de respuestas; cuadra con el código.
- CHANGELOG: **PASA** — una línea en español bajo `## 0.1.13 — not released yet`.
- Commit: **pendiente del coordinador** (`deskops closeout commit`), como manda el contrato; no es del ejecutor.
- Mensaje a IR: **pendiente del cierre** — el ejecutor dejó el texto propuesto en su informe (necesita el sha del commit).

## Scope / Precisiones (revisado en el diff)
- `BatchValidator` en `extension.py` junto a `Extension`; `ServerContext.batch_validators` + `add_batch_validator`; `build_server` pasa `context=` a `WriteTools`; `WriteTools` lee `context.batch_validators` en cada llamada: OK.
- propose: validadores tras `_require` y `_check_path`, antes de construir el lote; apply: tras `require` y `sealer.check`, sobre `proposal.changes`: OK (confirmado también en caso borde).
- Rechazo `apply.rejected("domain", "<n> domain check(s) failed", findings=<todos>)`; `domain_alerts` solo con alertas: OK.

## Caso propio no cubierto por el ejecutor (`/dev/shm/tester-mcp-gancho/edge.py`, 14/14 OK)
In-process con `WriteTools` + `ServerContext` sobre el mundo de `mcp_world`:
- Dos validadores (uno da error solo en el 2.º de dos cambios, otro una alerta): corren ambos en orden, `findings` trae error y alerta, `n=1` cuenta solo errores, no hay `proposal`, ninguno de los dos archivos cambia.
- Propose pasa `UpdateDocument` (Change) y apply `BatchChange` al validador, con el mismo `context`.
- Error en apply sobre propuesta de 2 cambios: no escribe ninguno.
- Sello adulterado, ruta `.py` y lista vacía se rechazan antes de llamar a los validadores.
- Solo alertas en apply: aplica los dos y devuelve `domain_alerts`.
- Contexto sin validadores y `WriteTools` sin `context`: sin `domain_alerts`, como antes.

## Alcance de archivos
Tocados por el ejecutor: los 7 del contrato + `docs/architecture/mcp.md` (mandado por Scope/Precisiones). Además `.sldb/store.yaml`, `.sldb/core/models/RunDoc.yaml`, `.sldb/core/store_index.yaml` y `.sldb/core/documents/RunDoc/run-deskops-{e-eda2f0fb7728,t-7bf3eb7dc2d7}.yaml`: son el registro de los RunDoc de este despacho (ejecutor y tester), no cambios del ejecutor. Resto: cambios ajenos listados en el brief. Nada fuera de contrato.

## Observaciones (no bloquean)
- `domain_alerts` se añade también a respuestas `stale`/`rules` de `run_batch` (anotado por el ejecutor; coherente con la doc).
- Un validador que lanza excepción no se captura (fuera del contrato).
