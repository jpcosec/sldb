REFORMULACION

GO07 es un nodo `delivery` de sldb (padre PK03) que pide anclas a documentos con hash de contrato: forma `doc:Model:name@sha256:<hash>` en campos declarados por el modelo en `__doc_anchors__` (str o list[str]) y en `from:` de Provenance; pinneado al guardar con el hash de contrato del destino, o sin hash si no existe; estados `intact/changed/lost`; `check_doc_anchors(store)` y extensión de `anchors check`; alerta `anchors/provenance_changed` para `from:`; entrada derivada `<campo>__anchor_state` en la facet payload de GO04; doc `anchoring.md` y CHANGELOG. Límites: severidad solo alert, sin `reconnected`, sin tocar el lenguaje, sin cablear `stores check` (GO08), sin definir modelos de recibo ni autenticación; nada se persiste aparte del texto del campo.

AMBIGUEDADES

1. «una regla any(^subject: anchor_state = "intact" and verdict = "accepted") sobre B evalúa true/false según el caso» — no define el modelo/schema de A ni que A tenga `verdict`, ni si el sujeto de la regla es B o A; obliga a inventar el documento de prueba y las combinaciones que dan true/false.

2. «un valor doc:Model:name sin @sha256 en un campo __doc_anchors__ o en from: se completa con el hash de contrato actual del destino» — no define qué ocurre con un valor de un campo `__doc_anchors__` que no tiene forma `doc:` (texto plano, vacío, malformado); obliga a inventar validación, error o estado.

3. «Finding alert con code anchors/provenance_changed» — solo nombra el caso `changed` para `from:`; obliga a inventar qué finding (código/severidad) emite un `from:` en estado `lost` y si ese estado se pinnea igual.

DRY-RUN

Lecturas: GO04 (facet payload y reconstrucción), GO05 (lectura del campo), modelo base y Provenance, `payload_save_steps`, `anchors.py`, `edge_index`, docs. Cambios previstos: atributo `__doc_anchors__` en modelo base; parseo/pinneado al guardar; `check_doc_anchors` en `api/anchors`; extensión de `anchors check`; `<campo>__anchor_state` en la proyección; `anchoring.md`; CHANGELOG. Dependencias: GO04 y GO05; gate `G_SEMANTICS` pending, por lo que no es ejecutable. Validaciones futuras: pytest en el host indicado; tests de pinning, `changed/intact/lost`, `provenance_changed`, regla con `anchor_state`, docs y CHANGELOG.

FUTURO

GO08 cablea `stores check` y es dueño de `api/stores`; GO02/GO05 fijan el contrato de hash y el lenguaje; el TaskDoc se promueve con `deskops add task --from-drawer`; el operador del desk de sldb escribe la disposición en `reviews/rN.md` y resuelve `G_SEMANTICS`; el dueño indica el host de pytest (robocop2 en esta serie). Nada se ejecuta: `execution_authorized: false`.
