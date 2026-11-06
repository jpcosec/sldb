## REFORMULACION

Propósito: implementar anclas a documentos pinneadas con el hash de contrato de GO02, dentro del nodo GO07 del plan `grafo-operable`, sin alterar el lenguaje ni el shard. Resultado: campos `__doc_anchors__` y `Provenance.from` con forma `doc:Model:name@sha256:<hash>`, validación pydantic al escribir, pinneado al guardar, estados `intact/changed/lost`, `check_doc_anchors(store) -> list[Finding]`, comando `anchors check`, aristas `references`, entrada derivada `<campo>__anchor_state` en la facet payload, documentación y CHANGELOG. Repo/workspace: `desk`, archivo `desk/tasks/task-go07-anclas-a-documentos-con-hash-de-contrato.md`; código en `src/sldb/`. Límites: fuera el cableado en `stores check` y la evaluación incremental (GO08), cambios al lenguaje (GO05), formato del shard o `EDGE_INDEX_VERSION`, y `reconnected` para documentos. No es un agregado: no tiene hijos (`atoms: []`); es una tarea ejecutable de implementación.

## AMBIGUEDADES

1. Escalar frente a lista: «(h3) … `Provenance.from_` es `list[str]` (alias from), no un escalar como dice el contrato» frente a «from: de Provenance es escalar (str)». Obliga a inventar cuál contrato rige, si hay migración y cómo se valida cada elemento.
2. `from:` no-doc: «otro texto es error de validación al escribir; … también en from:» frente a «un from: que no empieza por doc: (p. ej. code:) no es ancla de documento y este nodo no lo toca». Obliga a decidir si `code:` se rechaza o se ignora.
3. Tipo `Finding`: «check_doc_anchors(store) → list[Finding]» sin definirlo. Obliga a inventar módulo, campos y severidad.
4. Aristas desde `from:`: «Todo campo `__doc_anchors__` … genera aristas references» no menciona `from:`. Obliga a inventar si `from:` también genera `references`.
5. Ancla sin hash y destino inexistente: «si el destino no existe, se guarda sin hash» y «un ancla sin hash cuyo destino ya existe se pinnea en la siguiente escritura». No define qué ocurre si el destino se crea después. Obliga a inventar la transición y su reporte.
6. Campos lista: «Varias anclas en un campo lista = un estado por elemento» no aclara aristas por elemento ni alineación con valores nulos. Obliga a inventar la semántica.

## DRY-RUN

Lecturas hipotéticas: task, `alcance.md`, `rules-language.md`, `graph-backend.md`, `rules.md`, modelos, `payload_save_steps.py`, `edge_index/`, API/CLI de anclas y tests. Cambios previstos: validadores y atributo `__doc_anchors__`, `Provenance.from`, pinneado al guardar, aristas `references`, proyección `<campo>__anchor_state`, `check_doc_anchors`, `anchors check`, docs, CHANGELOG y tests. Dependencias: `contract_hash` (GO02), `field_hashes` del índice (GO04), alias `anchor_state` (GO05), vocabulario `AnchorState`. Validaciones futuras: `pytest tests/api/test_doc_anchors.py`; tests existentes de anclas, provenance, proyección y lenguaje; `test_clean_code_rules.py`, `test_store_seams.py`, `tools/check_layers.py`; suite completa por el supervisor. Nada ejecutado.

## FUTURO

GO08 cablea `stores check`; GO05 ya define el alias; GO02/GO04 aportan hash e índice; el supervisor ejecuta la suite completa; la revisión en frío y la integración en `main` las decide un humano.
