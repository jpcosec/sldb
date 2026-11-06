## REFORMULACION

Propósito: nodo GO07 del plan grafo-operable (dag rev 9), hijo de PK03, en el repo sldb (`/dev/shm/sldb-desk`): añadir anclas a documentos pinneadas con el hash de contrato de GO02 y exponer su estado al lenguaje de GO05 sin tocar el shard de GO04. Resultado: atributo `__doc_anchors__` y `from:` con forma `doc:Model:name@sha256:<64 hex>` validados al escribir y pinneados al guardar; estados intact/changed/lost; `check_doc_anchors(store) -> list[Finding]` usado por `anchors check`; aristas `references` desde `__doc_anchors__`; entrada derivada `<campo>__anchor_state` en la facet payload; `docs/architecture/anchoring.md`, CHANGELOG y tests. Es un nodo ejecutable, no un agregado: no tiene átomos ni hijos que transferir. Límites: fuera el cableado en `stores check` y la evaluación incremental (GO08), cambios al lenguaje, al formato del shard o a `EDGE_INDEX_VERSION`, y `reconnected` para documentos.

## AMBIGUEDADES

1. «no se persiste en el shard, así que editar el destino no exige invalidar al contenedor» choca con que la proyección sí se persiste en el shard (CHANGELOG GO04). Obligaría a inventar dónde se calcula `<campo>__anchor_state`: mutar nodos en `compose_edge_index` o un accessor de lectura.
2. «se calcula desde los `field_hashes` del destino ya presentes en el índice (GO04)» frente a h1 «`contract_hash(modelo, field_hashes)`»: el índice guarda `contract_signature`, no `contract_hash`, y `contract_hash` exige la clase del destino; `check_doc_anchors(store)` no recibe `pythonpath`. Obligaría a inventar la resolución del modelo y el dato exacto.
3. «un elemento vacio o null no genera arista y su posicion en `__anchor_state` es null», pero la extracción descarta null: no se define si la clave `<campo>__anchor_state` existe vacía o falta. Obligaría a inventar ese caso.

## DRY-RUN

Lecturas: TaskDoc, rituales execution/testing/closeout y los archivos listados (`structured_doc`, `provenance`, `model_contract`, `doc_contribution`, `compose`, `payload_projection`, `payload_save_steps`, `anchors`, CLI `anchors`, `anchoring.md`, CHANGELOG, tests). Cambios previstos: validador pydantic de `__doc_anchors__` y `from:` en modelos/Provenance; comprobación de definición (campos str/list[str], sufijo reservado) en `model_contract`; pinneado en `payload_save_steps`; aristas `references` de `__doc_anchors__` en `edge_index`; `check_doc_anchors` y `Finding`; extensión de `anchors check`; entrada derivada en proyección/lectura; docs, CHANGELOG y tests de aceptación y rechazo. Dependencias: `contract_hash` (GO02), `field_hashes`/proyección (GO04), alias `anchor_state` y `eval` (GO05), `AnchorState`, `Finding`. Validaciones futuras: `pytest tests/api/test_doc_anchors.py`; tests de anclas, provenance, proyección y lenguaje sin cambios; `test_clean_code_rules`, `test_store_seams`, `check_layers`; suite completa por el supervisor. Nada ejecutado.

## FUTURO

GO08 cablea `stores check` y la evaluación incremental; el supervisor corre la suite completa; una revisión humana en frío acepta e integra en main; GO05 consume `anchor_state`; GO02/GO04 aportan hash de contrato y `field_hashes`.
