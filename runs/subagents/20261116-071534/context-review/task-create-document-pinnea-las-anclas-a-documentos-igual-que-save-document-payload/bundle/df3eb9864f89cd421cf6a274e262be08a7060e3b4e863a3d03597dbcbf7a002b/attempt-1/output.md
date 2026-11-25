REFORMULACION
Propósito: que `create_document` pinnee las anclas `doc:Model:name` de campos `__doc_anchors__` y del `from:` de procedencia, con el mismo comportamiento y orden que `save_document_payload`, para que un documento recién creado no quede con `anchor_state: lost`. Resultado: cambio en `src/sldb/api/documents/create_document.py` —y en `transaction*.py` solo si `Transaction.create` no pasa por él—, test en `tests/api/test_doc_anchors.py`, línea en `CHANGELOG.md` y aviso a deskops. Repo: sldb. Límites: no cambiar el testigo de `any` en findings, no hacer `anchors check` sobre índices anteriores a GO07; el ejecutor no hace push.

AMBIGUEDADES
1. Validación: el TaskDoc exige solo «TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py» y «TMPDIR=/dev/shm pytest -q tests/api/test_on_write_entering.py», mientras el ritual de testing pide «full suite when shared behavior changed». Obligaría a inventar si el cambio, por tocar escritura compartida, exige la suite completa.
2. CHANGELOG: se pide una línea «bajo el encabezado "## 0.1.13 — not released yet"», pero no se dice qué hacer si ese encabezado no existe. Obligaría a inventar versión o ubicación.

DRY-RUN
Lecturas: `payload_save.py` (orden de `pin_payload` y `pin_provenance`), `doc_anchor_pinning.py`, `create_document.py`, `transaction*.py`, `tests/api/test_doc_anchors.py`, `test_on_write_entering.py`, `CHANGELOG.md` y la nota de inbox citada. Cambios previstos: llamar `pin_payload` sobre el payload antes de renderizar; renderizar; aplicar `pin_provenance` al texto antes de escribir, replicando el orden de `payload_save.py`; añadir test de destino trackeado (queda `@sha256` e `intact`) y no trackeado (queda `lost`), incluyendo procedencia; actualizar CHANGELOG. Dependencias: helpers/fixtures del test existente, `contract_hash`, `api.create_document`, funciones de pinneo. Validaciones futuras: los dos pytest indicados, auditoría de git, árbol limpio, informe en `runs/subagents/<run-dir>/result-summary.md` y aviso con `deskops message send --to deskops`.

FUTURO
El coordinador ejecuta el commit con `deskops closeout commit`; deskops recibe el aviso y decide retirar su `create + update`; closeout verifica tests, commit, átomos y árbol limpio.
