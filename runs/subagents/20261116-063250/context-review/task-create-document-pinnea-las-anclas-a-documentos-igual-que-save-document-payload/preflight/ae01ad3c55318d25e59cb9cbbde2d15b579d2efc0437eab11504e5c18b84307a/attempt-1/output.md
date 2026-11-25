## REFORMULACION

**Propósito:** que `create_document` pinnee las anclas de documentos igual que `save_document_payload` (GO07): todo `doc:Model:name` sin `@sha256` en campos de `__doc_anchors__` o en el `from:` de procedencia recibe el hash de contrato del destino. **Resultado:** un documento creado cuyo ancla nombra un destino trackeado queda escrito pinneado (`anchor_state` intact al leer); un destino no trackeado queda como estaba (`lost`). **Repo:** `/mnt/ssd/proyectos/SLDB_1`, superficie `src/sldb/api/documents/` y `tests/api/test_doc_anchors.py`. **Límites:** fuera de alcance el testigo de `any` en findings y `anchors check` previo a GO07; el ejecutor no hace push; el commit lo hace el coordinador; el informe va a `runs/subagents/<run-dir>/result-summary.md`.

## AMBIGUEDADES

1. «con sldb.api (stores init, add_model, create_document) en tmp_path» — no se da firma ni import de `stores init`; obligaría a inventar cómo inicializar el store y registrar el destino trackeado.
2. «una línea en español bajo el encabezado "## 0.1.13 — not released yet"» — asume que el encabezado existe; si no, obliga a inventar sección y versión.
3. «un destino no trackeado deja el valor como estaba (lost), como en save» — no fija el literal esperado ni cómo se lee `anchor_state`; obliga a decidir el assert.
4. «pin_provenance sobre el texto renderizado antes de escribir» — «texto renderizado» no define parámetro ni retorno; si no coincide con `payload_save_steps.py:92`, habría que inventar la firma.

## DRY-RUN

**Lecturas:** `payload_save.py:30-60`, `payload_save_steps.py:92`, `doc_anchor_pinning.py` (`pin_payload`, `pin_provenance`), `create_document.py`, `grep -rn "def create" src/sldb/api/documents/transaction*.py`, `tests/api/test_doc_anchors.py`, `tests/api/test_on_write_entering.py`, `CHANGELOG.md`.
**Cambios previstos:** importar y llamar `pin_payload(location.store_path, model_type, payload)` antes de `_rendered`; `pin_provenance` sobre el texto renderizado antes de escribir; replicar en `Transaction.create`/`transaction_ops.create` solo si no delega en `create_document`; añadir dos tests (trackeado pinnea, no trackeado queda `lost`); línea en CHANGELOG.
**Dependencias:** índice del store para resolver destinos, módulo de pinneo GO07, fixtures del test existente, encabezado de CHANGELOG.
**Validaciones futuras:** `TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py` y `tests/api/test_on_write_entering.py`; informe; `deskops message send --to deskops`.

## FUTURO

El coordinador ejecuta `deskops closeout commit` (sin push). Deskops recibe el aviso y decide retirar su workaround create+update. Un humano decide las hipótesis 1 y 3, fuera de alcance. Otro nodo produce y archiva el `result-summary.md`.
