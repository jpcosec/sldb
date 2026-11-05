REFORMULACION
GO07 es un nodo de código (no agregado) del repo sldb. Propósito: que un campo declarado en `__doc_anchors__` o el `from:` de Provenance guarde un ancla `doc:Model:name@sha256:<hash>`, que sldb la pinnee al guardar, calcule su estado derivado y lo reporte. Resultado: pinneado; estados `intact/changed/lost`; `check_doc_anchors(store) -> list[Finding]`; extensión de `anchors check`; `anchor_state` en la proyección; validación al escribir; docs y CHANGELOG. Límites: sin `reconnected`; sin cablear `stores check` (GO08); sin persistir estados ni cambiar `EDGE_INDEX_VERSION`; `changed/lost` son alertas, nunca error.

AMBIGUEDADES
1. "solo admite vacío/null o valores con forma doc:Model:name[@sha256:<hash>]; otro texto es error de validación al escribir". No fija el formato de `<hash>` (longitud, hexadecimal) ni si `@sha256:` vacío o malformado es error; obliga a inventar la validación.
2. "el from: de Provenance, que pasa a admitir la forma con hash" y "en un campo __doc_anchors__ o en from: se completa". No dice si `from:` es escalar o lista, ni si se pinnean todos sus elementos, ni si un `from:` no-`doc:` se ignora o es error; obliga a decidir esa semántica.
3. "agrega a la facet payload ... una entrada derivada <campo>__anchor_state". No define qué pasa si el payload ya tiene un campo con ese nombre ni la precedencia; obliga a inventar la resolución de colisión.

DRY-RUN
Lecturas: GO04 (field_hashes/proyección), GO05 (lenguaje), modelos y Provenance, `anchors check`. Cambios previstos: atributo `__doc_anchors__` en modelo base; `provenance.py`; pinneado en `payload_save_steps.py`; entrada derivada en `edge_index`; `api/anchors/`; CLI `anchors.py`; `anchoring.md`; CHANGELOG. Dependencias: GO04, GO05, G_SEMANTICS (pending). Validaciones futuras: tests de aceptación (pinneado, changed/intact/lost, alertas, regla `any(^subject: ...)`, rechazo no-doc:, `provenance_changed`, docs/CHANGELOG). Sin ejecutar nada.

FUTURO
GO08 cablea `stores check`; GO05 evalúa `^subject`; GO02/G_SEMANTICS fija semántica y posible hash; el desk de sldb acepta la revisión; el TaskDoc fija nombres de tests y archivos.
