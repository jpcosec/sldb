# result-summary — tester deskops-t-114b39f37570

Task: `task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload`. Pills: ninguno.
Veredicto global: **PASA** (lo que es del ejecutor). El commit y el aviso a deskops corresponden al closeout del coordinador (ver abajo).

## Validation (corrida propia, salida completa en `validation.log`)
| Comando | Resultado | Veredicto |
|---|---|---|
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_doc_anchors.py` | 22 passed, rc=0 (incluye los 2 tests nuevos) | PASA |
| `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py` | 7 passed, rc=0 | PASA |

`uv` funcionó; no hizo falta el fallback `uvx`. Único aviso: `PytestConfigWarning: asyncio_default_fixture_loop_scope` (preexistente, no relacionado).

## Done When, punto por punto
1. **Los dos archivos pasan con el test nuevo** — PASA. Tests nuevos: `test_create_document_pins_the_anchor_without_a_later_save` (create sin save → `subject == doc:TaskDoc:b@sha256:<contract hash>`, `anchor_state == intact`; destino `ghost` → sin hash, `lost`) y `test_a_transaction_create_pins_the_anchor` (vía `api.transaction(...).create`). Cubren el Goal y el borde "no trackeado" del Scope.
2. **CHANGELOG** — PASA. Una línea en español, primera bajo `## 0.1.13 — not released yet (no tag, not on PyPI)`, estilo de las vecinas (task, nota del inbox, antes/ahora, tests).
3. **Commit** — PENDIENTE (no del ejecutor): por convención lo hace el coordinador con `deskops closeout commit`. No verificable en esta fase.
4. **Aviso a deskops** — PENDIENTE (no del ejecutor en la práctica): el ejecutor no lo envió y lo justifica en su informe (el cuerpo debe llevar el commit, que aún no existe); dejó el comando listo con `<sha>`. Lo anoto como pendiente del closeout, no como fallo del cambio. El coordinador debe enviarlo tras el commit.

## Revisión del código (contra el Scope)
- `create_document`: `pin_payload` sobre el payload antes de `_rendered` y de `_admit` (que corre `check_entering`, las reglas `on_write`); `pin_provenance` sobre el texto sellado antes de `write_source_text`. Mismo orden relativo que `_save` (`payload_save.py`: pin_payload → reglas → render) y `write_rendered_document` (stamp → pin_provenance → write). En create las reglas corren tras el render, pero ya sobre el payload pinneado: equivalente para el Scope.
- `Transaction.create` (`transaction.py:79`) → `transaction_ops.create` (`:27`) → `create_document` (`:31`): verificado con grep; hereda el pinneo, correcto no tocarlo.
- `pin_provenance` en create es de hecho un no-op hoy: `stamped(...)` se llama sin `previous`, así que el bloque nuevo tiene `from_=[]`. Paridad con save sin efecto observable; el ejecutor lo declara en "Dudas". No es fallo.

## Casos no cubiertos por el ejecutor (script propio en `/dev/shm/tcp/test_edge_create_pin.py`, sin tocar el repo) — 4 passed, rc=0
- Campo-lista de `__doc_anchors__` (`Bundle.subjects`) con mezcla: trackeado sin hash → pinneado; `ghost` → igual; ya pinneado con hash viejo → no se re-pinnea. PASA.
- El dict del llamador no se muta (`pin_payload` devuelve copia). PASA.
- Ancla ya pinneada con hash obsoleto en create: se conserva tal cual y su `anchor_state` no es `intact`. PASA.
- El archivo en disco lleva el `@sha256` y `anchors check` no da findings tras create solo. PASA.
- Modelo sin `__doc_anchors__` con un valor `doc:...` en un campo normal: no se toca. PASA.

## Archivos fuera del contrato
`git status --short`: del ejecutor solo `create_document.py`, `test_doc_anchors.py`, `CHANGELOG.md` y su `runs/subagents/20261116-exec-create-pin/`. Resto ajeno según el brief (`apply_batch.py`, `lock.py`, `test_apply_batch_lock.py`, `uv.lock`, `desk/runtimes/`, `.herdr-coordination.md`, `runs/subagents/2026110*`/otros run dirs). Los cambios en `.sldb/` (`RunDoc.yaml`, `store_index.yaml`, `store.yaml`, `RunDoc/run-deskops-{e-dd1bb55310fa,t-114b39f37570}.yaml`) son el registro de los `run.md` de este despacho (executor y tester) por deskops, no del ejecutor; no están en la lista de ajenos del brief, lo anoto para el closeout. `uv run --frozen` no cambió `uv.lock` más allá de su `M` ajeno previo. PASA.

## Archivos que toqué
Solo `runs/subagents/20261116-test-create-pin/validation.log` y `result-summary.md`; script en `/dev/shm/tcp/`.
