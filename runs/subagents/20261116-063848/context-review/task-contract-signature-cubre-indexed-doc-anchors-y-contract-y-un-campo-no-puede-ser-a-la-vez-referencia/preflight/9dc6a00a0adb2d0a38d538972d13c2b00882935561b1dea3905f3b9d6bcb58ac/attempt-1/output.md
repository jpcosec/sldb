REFORMULACION  
Encargo ejecutable (task.code, no agregado) en el repo SLDB_1. Propósito: que contract_signature cubra __indexed__, __doc_anchors__ y __contract__, de modo que cambiarlos invalide shards y el rebuild reproyecte; y rechazar la doble declaración referencia/ancla. Resultado: firma modificada, problema nuevo en definition_problems, tests en tests/store/test_payload_projection.py y tests/api/test_doc_anchors.py, .sldb reconstruido, CHANGELOG, avisos a deskops y graph_ui, e informe en runs/subagents/<run-dir>/result-summary.md. Límites: no cambiar la proyección del payload ni el cálculo de aristas; no hacer push; el commit lo hace el coordinador.

AMBIGUEDADES  
1. "commitear el .sldb resultante en el mismo commit" y "se agregan al commit los archivos..." frente a "El commit lo hace el coordinador ... el ejecutor no hace push". Obliga a inventar si el ejecutor hace git add/stage del .sldb o solo deja los cambios.  
2. "con título 'sldb: contract_signature cambia, los stores se reconstruyen una vez'" frente a "lleva como título el de la tarea". Obliga a elegir entre ambos títulos para los avisos.  
3. `"contract": sorted(__contract__ o [])` no define si __contract__ es lista, mapa u otro iterable; obliga a asumir que sorted produce los nombres esperados.

DRY-RUN  
Lecturas: model_contract.py (contract_signature, _DECLARED, doc_anchor_fields), edge_node_record.py, doc_anchor_value.py (definition_problems), los dos tests, CHANGELOG y helpers/fixtures. Cambios previstos: añadir a la firma las tres claves ordenadas; actualizar docstring y descripción del campo; añadir el problema de doble declaración; tests de stale/rebuild y rechazo; entrada en CHANGELOG; ejecutar build de .sldb; preparar avisos e informe. Dependencias: helpers existentes, CLI sldb, deskops message send y store .sldb. Validaciones futuras: pytest de ambos archivos y `sldb stores build --check --store .sldb`.

FUTURO  
El coordinador materializa el commit closeout y decide el staging del .sldb; deskops y graph_ui reciben el aviso y reconstruyen sus stores; el ejecutor entrega result-summary.md. Nada de esto es ambigüedad del contrato.
