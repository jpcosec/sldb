# Executor deskops-e-7015d1ec50ff — undo_changes en sldb mcp (IR04b)

Resultado: **LISTO 0**. Todos los comandos de Validation dan rc=0 (salida completa en `validation.log`).
Sin commit, sin avisos, sin tocar `desk/` ni `.sldb/` (decisiones (6) del coordinador y el brief).

## Qué cambió

- `src/sldb/mcp/write/undo.py` (nuevo): clase `UndoStack` (una por sesión del servidor, en memoria y sin persistir).
  - `push(inverse)` apila el `BatchReport.inverse` de un lote aplicado.
  - `undo_changes(steps=1)` pide nivel CONTENT y aplica los inversos del más nuevo al más viejo con `api.apply_batch`.
  - `_undo_last()` aplica el inverso de arriba y lo saca de la pila solo si se escribió. Un `ConflictError` da `rejected: "stale"` (con `document`) y cualquier otro rechazo de SLDB pasa por `apply.refusal`.
  - Con `steps > 1` se detiene en el primer fallo: lo ya deshecho queda deshecho (`undone`, `written`), y el lote que falló y los anteriores siguen en la pila (`remaining`). Es la decisión (2).
  - Si `steps < 1` o `steps` supera el tamaño de la pila (también cuando está vacía), responde `rejected: "nothing_to_undo"` sin escribir nada.
  - Sin dry-run: `apply_changes` tampoco lo tiene (decisión (3)).
- `src/sldb/mcp/write/apply.py`:
  - `run_batch(store_path, proposal, undo)` hace `undo.push(report.inverse)` después de un `apply_batch` exitoso.
  - `TYPE_CHECKING` importa `UndoStack`.
- `src/sldb/mcp/write/tools.py`:
  - `WriteTools.__init__` crea `self.undo = UndoStack(...)`, que es la pila del estado de sesión, junto al `sealer` (decisión (1)).
  - `apply_changes` le pasa `self.undo` a `run_batch`.
  - Se actualizó el docstring de la clase.
- `src/sldb/mcp/write/pending.py`: se quitó `PENDING["undo"]`.
- `src/sldb/mcp/signals/catalog.py`: `PENDING_TOOLS` queda `{}` (tipado). La clase `not_implemented` sigue en el catálogo cerrado.
- `tests/mcp/test_write_tools.py`: helpers `retitled`, `two_items` y `written_by_someone_else`, y 4 tests nuevos:
  - `test_undo_changes_is_served_and_puts_the_store_back`: la tool está en `list_tools`. Crea, hace dos updates, deshace con `steps=1` y luego con `steps=2`. Los payloads y el conjunto de export_ids vuelven a ser los de antes y el archivo creado ya no existe.
  - `test_undo_after_someone_else_wrote_is_a_conflict_and_writes_nothing`: da `stale`, `written` false, `remaining` 1, el `tree_digest` no cambia y queda el título ajeno.
  - `test_undo_of_several_stops_at_the_first_that_fails`: con `steps=2` deshace el más nuevo y se para en el conflicto (`undone` 1, `remaining` 1). El lote fallido sigue en la pila.
  - `test_undo_with_nothing_to_undo_is_a_clear_refusal`: da `nothing_to_undo` y el `tree_digest` no cambia.
- `docs/architecture/mcp.md`: la tabla de niveles nombra `undo_changes`, y la sección «Undo (pending)» se reemplaza por «Undo», con la pila, la forma de las respuestas, la parada en el primer fallo, que no hay dry-run y qué pasa en nivel 0.
- `CHANGELOG.md`: entrada en 0.1.13.

### Fuera de la lista de archivos del contrato (necesarios; anotados)
- `src/sldb/mcp/registry.py`: `register_write` registra `writes.undo.undo_changes` con anotaciones `WRITES`. Sin esto, la tool no queda servida (Done When).
- `src/sldb/mcp/unmet.py`: `LEVEL_TOOLS` suma `"undo_changes": 1`. Así, en nivel 0 la respuesta explica qué nivel hace falta, en vez de «no tool».
- `src/sldb/mcp/server.py`: el docstring y `WRITE_INSTRUCTIONS` nombran `undo_changes`. Solo cambia el texto que lee el cliente.
- `tests/mcp/test_signals.py`: está en Validation y se contradecía con el punto (3) del Scope.
  - `test_the_catalog_is_closed` ahora pide que `undo_changes` no esté en `PENDING_TOOLS`.
  - `test_undo_changes_is_a_not_implemented_signal` se reemplaza por `test_undo_changes_at_level_0_is_a_signal_that_names_the_level`: en nivel 0, `unknown_tool` con «needs write level 1» queda en el log.
- `tests/mcp/test_extension.py:36` y `tests/mcp/test_mutability.py:14` fijaban la lista exacta de tools de un servidor de escritura y ahora incluyen `undo_changes`. Sin ese cambio fallaban (lo muestra la primera corrida extra en `validation.log`, rc=1). Después del ajuste, rc=0.

## Done When
- Los comandos de Validation pasan con los tests nuevos: los 5 dan rc=0 (ver abajo).
- `undo_changes` figura entre las tools servidas desde el nivel 1. Lo prueban `test_undo_changes_is_served_and_puts_the_store_back`, `test_extension` y `test_mutability`.
- CHANGELOG y docs: hechos.
- Commit y aviso a IR: no se hicieron, por la decisión (6) del coordinador («No hagas commit ni mandes avisos»). Quedan para el coordinador.

## Respuesta a la nota de IR 20261116-184421 (decisión (5); no escribí en desk/)
> sldb mcp sirve `undo_changes`, y la pila de lotes inversos vive en la sesión del servidor
> (`WriteTools.undo`, `sldb.mcp.write.undo.UndoStack`, en memoria, una por sesión, sin persistir ni redo).
> Cada `apply_changes` aplicado apila su `report.inverse`. `undo_changes(steps=1)`, desde el nivel 1, deshace los últimos
> lotes del más reciente al más antiguo con `apply_batch` y sus guardas: si hubo una escritura ajena, `rejected: "stale"`
> sin escritura de ese lote. Con `steps` > 1 se para en el primer fallo (`undone`/`remaining`). Si la pila no alcanza,
> `rejected: "nothing_to_undo"`. No hay dry-run. specIR no necesita una extensión: IR04b se reduce a verificarlo desde specIR.

## Comandos (rc)
| rc | comando |
| --- | --- |
| 0 | `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_write_tools.py` (12 passed, 1 xfailed, este último ya existía) |
| 0 | `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_signals.py` |
| 0 | `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev --extra mcp pytest -q tests/mcp/test_dry_run.py` |
| 0 | `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/test_clean_code_rules.py` |
| 0 | `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev bash tools/check.sh --fast` (TODAS LAS PUERTAS PASAN) |
| 1 → 0 | extra: `... --extra mcp pytest -q tests/mcp/test_extension.py tests/mcp/test_mutability.py`. Primero rc=1, porque `WRITE_TOOLS` estaba fijado sin `undo_changes`. Después del ajuste, rc=0 (15 passed). |

No corrí la suite completa ni `sldb stores build --check`: los corre el integrador, y Validation no los pide.

Líneas efectivas de los archivos tocados (máximo 80):
- `write/tools.py`: 77
- `write/undo.py`: 36
- `write/apply.py`: 38
- `server.py`: 35

Las funciones tienen 10 líneas de lógica o menos (`test_clean_code_rules` pasa).

## Archivos tocados (lista exacta)
- src/sldb/mcp/write/undo.py (nuevo)
- src/sldb/mcp/write/apply.py
- src/sldb/mcp/write/tools.py
- src/sldb/mcp/write/pending.py
- src/sldb/mcp/signals/catalog.py
- src/sldb/mcp/registry.py
- src/sldb/mcp/unmet.py
- src/sldb/mcp/server.py
- tests/mcp/test_write_tools.py
- tests/mcp/test_signals.py
- tests/mcp/test_extension.py
- tests/mcp/test_mutability.py
- docs/architecture/mcp.md
- CHANGELOG.md
- runs/subagents/20261116-exec-undo/validation.log, result-summary.md (entrega)

## Desvío y hallazgo (fuera de alcance, sin arreglar)
Un proceso servidor de larga vida (la fixture de sesión `writer`) propone con una guarda `expected_source_hash` vieja cuando otro proceso escribió el mismo documento después de su última lectura.
- Su primer `apply_changes` sale `stale` aunque la propuesta se hizo después de la escritura ajena. El reintento pasa.
- Se reproduce sin `undo_changes`: el writer aplica, otro proceso aplica sobre i1 y el siguiente propose+apply del writer da `stale` («expected 80ad…, found a94e…»). Lo reproduje con un test temporal que ya borré.
- Sospecha, sin verificar: la caché de índices/shards por (path, mtime_ns, size) de `sldb.store.io`, o lo que lee `store_fingerprint`. Es fallo seguro (rechaza, no escribe mal), pero un cliente MCP verá `stale` espurios mientras otro proceso escribe el store.
- En los tests, la escritura ajena se hace desde un proceso nuevo (`written_by_someone_else`), no desde la fixture `writer`. Sugiero abrir una nota.

Además, el contrato listaba 6 archivos y toqué 8 más (ver arriba). Ninguno lo autoriza el Scope de forma explícita, pero sin ellos la tool no queda servida, o Validation o los tests del mismo paquete fallan.
