## REFORMULACION
El nodo debe hacer tolerante la carga pública de documentos en el repo `/mnt/ssd/proyectos/SLDB_1` (paquete `src/sldb`). Resultado: `load_runtime_documents` acepta `on_invalid="skip"` y devuelve documentos sanos más los inválidos identificados por ruta, modelo y error; el modo por defecto `"raise"` sigue fallando pero nombra la ruta; `EdgeIndex` añade `problem_details` estructurado sin alterar `problems`. Incluye tests y CHANGELOG. Límites: no cambiar `resolve_runtime_doc` (solo medir y anotar tiempo), no quitar `problems`, no tocar `graph_ui`.

## AMBIGUEDADES
1. «un tipo de retorno para el modo skip (dataclass RuntimeDocuments con documents e invalid)»: no aclara si `RuntimeDocuments` se devuelve siempre o solo con `skip`, ni cómo queda la firma compatible con el modo `raise`. Obligaría a inventar el contrato de retorno.
2. «en modo raise, la excepción incluye la ruta»: no fija clase de excepción ni formato exacto del mensaje. Obligaría a inventar tipo y redacción.
3. «una lista de (ruta, modelo, error)» frente a «RuntimeDocuments con documents e invalid»: no define el tipo concreto de cada elemento ni si `error` es excepción, texto o estructura. Obligaría a inventar el modelo de `invalid`.
4. «problem_details: list[EdgeProblem] (modelo pydantic con kind, document, detail)»: no indica cómo asignar `kind`, `document` y `detail` en cada punto existente que agrega strings. Obligaría a inventar categorías y valores.
5. «se mide en esta tarea y se anota el tiempo en el informe»: no identifica ubicación ni formato del informe. Obligaría a inventar el destino de la medición.

## DRY-RUN
Un ejecutor futuro leería `src/sldb/api/documents/runtime_documents.py`, `src/sldb/store/query.py`, `src/sldb/store/edge_index/edge_index.py`, los tests indicados y `CHANGELOG.md`; buscaría `problems.append` y `problems=` en `edge_index`. Cambiaría la API pública, añadiría `RuntimeDocuments`/exportación, `EdgeProblem` y `problem_details`, actualizaría puntos de población, tests y changelog. Depende de `accepted_only`, pydantic y fixtures de tests. Validaría con `pytest` sobre `test_api_documents.py`, `test_api_edges.py` y `test_doc_invalid_check.py`, y con `stores build --check`. Sin ejecutar nada.

## FUTURO
Otro nodo ejecutor implementará cambios y ejecutará validaciones. Un humano decidirá si el contrato público, nombres y formato de errores son aceptables, y revisará la medición de `resolve_runtime_doc` anotada.
