# result-summary — executor deskops-e-dd1bb55310fa

Task: `task-create-document-pinnea-las-anclas-a-documentos-igual-que-save-document-payload`. Pills: ninguno (sin conflicto pill/contrato).

## Cambios
- `src/sldb/api/documents/create_document.py`, función `create_document`:
  - `payload = pin_payload(location.store_path, registered.model_type, payload)` justo después de cargar el modelo, antes de `_rendered` y de `_admit` (que corre `check_entering`, las reglas `on_write`): mismo orden que `_save` de `payload_save.py` (pin_payload → reglas → render).
  - El texto sellado pasa por `pin_provenance(location.store_path, ...)` antes de `write_source_text`: mismo orden que `write_rendered_document` (stamp → pin_provenance → write).
  - Import de `pin_payload, pin_provenance` desde `sldb.api.documents.doc_anchor_pinning`; párrafo nuevo en el docstring.
- `Transaction.create` (`transaction.py`) → `create` de `transaction_ops.py` → `create_document`: hereda el pinneo; no se tocó nada ahí (verificado con grep y con el test de transacción).
- `tests/api/test_doc_anchors.py`: dos tests nuevos
  - `test_create_document_pins_the_anchor_without_a_later_save`: create solo (sin save) deja `subject == doc:TaskDoc:b@sha256:<contract hash>` y `subject__anchor_state == "intact"`; un destino no trackeado (`doc:TaskDoc:ghost`) queda sin hash y `lost`.
  - `test_a_transaction_create_pins_the_anchor`: lo mismo vía `api.transaction(...).create`.
  - Comprobado que ambos fallan con `create_document.py` revertido (2 failed) y pasan con el cambio.
- `CHANGELOG.md`: una línea en español bajo `## 0.1.13 — not released yet (no tag, not on PyPI)`, primera de la sección.

## Done When
- Los dos archivos de Validation pasan con el test nuevo: sí (22 passed, 7 passed; rc=0 ambos, ver `validation.log`).
- CHANGELOG: hecho. Commit: lo hace el coordinador con `deskops closeout commit` (prohibido al ejecutor).
- Aviso a deskops: **no enviado** (desvío deliberado). La convención pide que el cuerpo lleve el commit, que aún no existe porque el commit es del closeout. Comando listo para el coordinador tras el closeout (sustituir `<sha>`):
  `deskops message send --to deskops --kind suggestion --title "create_document pinnea las anclas a documentos igual que save_document_payload" "sldb create_document (y Transaction.create, que pasa por él) ahora pinnea con @sha256 los doc:Model:name sin hash de los campos __doc_anchors__ y del from: de procedencia antes de escribir, igual que save_document_payload (GO07). Un recibo creado y nunca reescrito queda con anchor_state intact si el destino está trackeado. deskops puede quitar el create + update en la misma transacción (H-CC32-2). Commit: <sha>."`

## Comandos corridos
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_doc_anchors.py` → rc=0 (22 passed)
- `TMPDIR=/dev/shm uv run --frozen --extra code --extra dev pytest -q tests/api/test_on_write_entering.py` → rc=0 (7 passed)
- Verificación negativa (no es de Validation): con el cambio revertido temporalmente vía `git apply -R` de un diff en el scratchpad, `pytest -k "create_document_pins or transaction_create"` → 2 failed; diff reaplicado.
- `uv run --frozen` no tocó `uv.lock` (su `M` es el cambio ajeno previo).

## Archivos tocados
- src/sldb/api/documents/create_document.py
- tests/api/test_doc_anchors.py
- CHANGELOG.md
- runs/subagents/20261116-exec-create-pin/validation.log, result-summary.md (entrega)

## Dudas
- No hay test de `from:` de procedencia en create: el render de un payload no produce un bloque de procedencia con `from:` propio, así que `pin_provenance` en create es por paridad con save (cubre un `from:` que el sello pudiera traer). La lógica de pin_provenance ya la prueba el test existente de save.
