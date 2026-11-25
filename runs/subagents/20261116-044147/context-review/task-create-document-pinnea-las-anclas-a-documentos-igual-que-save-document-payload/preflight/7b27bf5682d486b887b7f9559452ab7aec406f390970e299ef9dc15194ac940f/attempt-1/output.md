## REFORMULACION

Encargo ejecutable (`task.code`, no agregado): hacer que `create_document` pinnee las anclas `doc:Model:name` sin `@sha256` en campos `__doc_anchors__` (y en `from:` de procedencia si `save_document_payload` lo hace), reutilizando `pin_payload`/`pin_provenance` de `doc_anchor_pinning.py`, en el mismo punto relativo y orden que `payload_save.py`, incluida la ruta transaccional si existe. Resultado observable: un documento creado leído después muestra el valor con `@sha256` y `anchor_state` no `lost`; un destino no trackeado permanece como estaba. Repo: SLDB (`src/sldb/api/documents/`). Límites: no tocar el testigo `any` de findings ni `anchors check` previo a GO07. Incluye test en `tests/api/test_doc_anchors.py`, `CHANGELOG.md`, commit y aviso a deskops.

## AMBIGUEDADES

1. «si save_document_payload también lo hace» — condicional a verificar leyendo código; el input no afirma si aplica. Obligaría a inventar el alcance de provenance si no se lee.
2. «Lo mismo dentro de la transacción si create pasa por otro camino» — no consta que exista tal camino; obligaría a inventar su ubicación.
3. «un destino trackeado» — no define qué registro/marca lo determina; obligaría a inventar el criterio.
4. «anchor_state intact al leerlo» — no precisa el valor esperado (¿`pinned`?), solo “no lost”.
5. «deja el valor como estaba (lost), como en save» — remite al comportamiento de save, no descrito en el input.
6. «el from: de procedencia» aparece en Rationale, pero Goal solo cita campos `__doc_anchors__`; el alcance exacto queda dual.
7. `CHANGELOG.md` sin formato/ubicación de entrada.

## DRY-RUN

Lecturas: `payload_save.py` (30-60), `doc_anchor_pinning.py`, `create_document.py`, `grep -rn "create_document\|def create" src/sldb/api/documents/transaction*.py`. Cambios previstos: inserción de `pin_payload(location.store_path, model_type, payload)` antes de `_rendered`, `pin_provenance` sobre el texto si corresponde, y equivalente en la ruta transaccional; test nuevo con destino trackeado y no trackeado; entrada CHANGELOG. Dependencias: API real de `pin_payload`/`pin_provenance` y semántica de tracking. Validaciones futuras: `TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py` y `tests/api/test_on_write_entering.py`; commit y `deskops message send`.

## FUTURO

Un humano/otro nodo decide: aceptación de la hipótesis H-CC32-2, existencia y forma de la ruta transaccional, criterio de “trackeado” si el código no lo fija, formato del CHANGELOG y ejecución del commit/aviso.
