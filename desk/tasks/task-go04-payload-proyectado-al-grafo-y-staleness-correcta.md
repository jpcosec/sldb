---
id: task-go04-payload-proyectado-al-grafo-y-staleness-correcta
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on: []
pills: []
files:
- src/sldb/store/edge_index/node_ids.py
- src/sldb/store/edge_index/doc_contribution.py
- src/sldb/store/edge_index/shard_reading.py
- src/sldb/store/edge_index/edge_index.py
- src/sldb/store/edge_index/compose.py
- src/sldb/store/models/edge_node_record.py
- src/sldb/store/edge_sync.py
- src/sldb/store/graph/facet_match.py
- src/sldb/store/graph/executor.py
- src/sldb/store/query_engine/structural_queries.py
- src/sldb/store/model_contract.py
- docs/architecture/graph-backend.md
- CHANGELOG.md
- tests/store/test_payload_projection.py
task_type: code
inherits_from: []
inherit_acceptance_context: false
atoms: []
closeout_evidence:
- tests
- commit
- atom
- materialization
---

# GO04: Payload proyectado al grafo y staleness correcta

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GO04 del plan desk/drawer/plans/grafo-operable (dag.yaml rev 9), hijo de PK02. Hoy el grafo no lleva los campos del payload y EdgeIndex.stale no detecta cambios de contrato del modelo (inbox 20261102-065705). GO05 evalua el lenguaje de GO02 sobre esta proyeccion. Requiere G_SEAM (GO03, en main 804f1ad4).

## Goal

_Describe the concrete result this task must produce._

Cada nodo de documento del indice de aristas lleva la facet payload (escalares y listas de escalares, o __indexed__), field_hashes, source_hash y contract_signature; EDGE_INDEX_VERSION 5; stale por source_hash o firma de contrato; StructuredQuery filtra sobre la facet payload sin re-extraer; ninguna consulta existente cambia de resultado.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/store/edge_index/, src/sldb/store/edge_sync.py, src/sldb/store/graph/facet_match.py, src/sldb/store/graph/executor.py, src/sldb/store/query_engine/structural_queries.py, el registro del nodo (src/sldb/store/models/edge_node_record.py), la validacion de __indexed__ al cargar el modelo, docs/architecture/graph-backend.md (seccion de la proyeccion y sus omisiones), CHANGELOG.md, tests. Fuera: el lenguaje de GO02 sobre la proyeccion y los shims (GO05), anchor_state (GO07), cualquier cambio en el resultado de consultas existentes.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (dag.yaml rev 9, GO04 scope): Cada nodo de documento del índice de aristas lleva una facet payload: mapa plano campo → valor con los campos del payload cuyo valor es escalar (str, int, float, bool, null) o lista de escalares (incluida la lista vacía); diccionarios y listas con elementos no escalares se omiten de la proyección y se documenta; por defecto todos esos campos, o, si el modelo declara el atributo de clase __indexed__, exactamente los nombres listados en lugar del conjunto por defecto (un nombre ausente en el payload de un documento se omite; un nombre cuyo tipo declarado en el modelo (la anotación pydantic del campo) no es escalar ni lista de escalares es error al registrar o cargar la definición del modelo, no por documento). content_hash ya está en el nodo (hash_c); field_hashes se agrega como el mapa completo del documento (el mismo de document_entry), no solo los campos proyectados. Formato de shard: se agregan cuatro claves al registro del nodo, payload, field_hashes, source_hash y contract_signature; nada más cambia; EDGE_INDEX_VERSION pasa de 4 a 5; al abrir el store, un shard con versión menor se marca stale y su documento entra al dirty set; la reconstrucción ocurre en la siguiente reconstrucción del índice (la próxima escritura o stores build), con el dirty set existente. La invalidación la gobierna el source_hash del archivo (content_hash deriva de él): stale por source_hash o por contract_signature; la proyección se recalcula al reconstruir. Arreglar EdgeIndex.stale: el shard guarda source_hash del documento y la firma de contrato del modelo: sha256 del JSON canónico (claves ordenadas, UTF-8, sin espacios) de {fields: todos los nombres de campo del modelo tras la herencia (propios y heredados por base_models), ordenados (no solo los proyectados), references: nombres de __references__ ordenados, containment: nombres de __containment__ ordenados, compositions: nombres de __compositions__ ordenados; cada atributo ausente aporta la lista vacía}, solo nombres; stale cuando el source_hash del archivo difiere o la firma de contrato del modelo cargado difiere (inbox 20261102-065705); la comprobación se hace donde hoy se consulta EdgeIndex.stale: al abrir el store y antes de cada consulta o reconstrucción del índice. StructuredQuery acepta filtros sobre la facet payload con sus operadores actuales y la semántica que facet_match ya aplica a las facets existentes; sobre null solo deciden is_null e is_not_null (los demás dan false); sobre una lista, contains es pertenencia, eq/ne comparan la lista entera, gt/lt y starts_with dan false, is_null da false e is_not_null true; en structural_queries.py y en su executor (src/sldb/store/graph/executor.py, el que ejecuta StructuredQuery; no es el eval de GO03). Un filtro sobre un campo no proyectado (de nivel superior pero diccionario o lista no escalar, fuera de __indexed__, o inexistente en el modelo) es un error de consulta que nombra el campo; un campo proyectable ausente en todos los payloads da conjunto vacío; nunca re-extrae. GO04 no cambia el resultado de ninguna consulta existente. ACEPTACION: Tras una escritura, el nodo expone los campos proyectados y omite los anidados; editar el Markdown por fuera marca stale y la reconstrucción los actualiza; agregar un campo a __references__ marca stale; una consulta estructurada por campo (status = closed) responde con cero llamadas a Validator.extract (contadas en el test); EDGE_INDEX_VERSION = 5; un shard de versión 4 queda stale al abrir y se reconstruye en la siguiente escritura; los tests existentes de StructuredQuery pasan sin cambios; tamaño del índice en MB y número de shards de este repo antes y después, registrados en la sección Validation del TaskDoc y en CHANGELOG. Requiere G_SEAM. OUTPUT_SCOPE: src/sldb/store/edge_index/, src/sldb/store/edge_sync.py, src/sldb/store/graph/facet_match.py, src/sldb/store/graph/executor.py, src/sldb/store/query_engine/structural_queries.py, docs/architecture/graph-backend.md (sección de la proyección y sus omisiones), CHANGELOG.md REGLAS COMUNES: alcance.md de desk/drawer/plans/grafo-operable (regla 2: no cierra con tests rojos ni saltados; regla 3: toda capacidad nueva entra con spec, CLI con envelope JSON, pruebas, CHANGELOG y doc en docs/architecture; regla 5: nada se persiste del resultado de una regla; regla 6: ante un contrato ausente registrar la hipotesis en este TaskDoc, no inventar API). Costura y protocolo: docs/architecture/graph-backend.md (GO03, en main).

## Validation

_List the checks required before this task can close._

- pytest -k 'edge or stale or structural or facet or executor or graph' -q sin fallos ni saltados
- los tests existentes de StructuredQuery pasan sin cambios
- consulta status = closed con cero llamadas a Validator.extract (contadas)
- tamano del indice en MB y numero de shards de este repo antes y despues registrados en Validation y CHANGELOG
- suite completa sin rojos (una vez, al final del nodo)

## Done When

_Name the observable condition that makes the task complete._

Aceptacion de GO04 cumplida linea por linea, revision en frio aceptada, nodo integrado en main.
