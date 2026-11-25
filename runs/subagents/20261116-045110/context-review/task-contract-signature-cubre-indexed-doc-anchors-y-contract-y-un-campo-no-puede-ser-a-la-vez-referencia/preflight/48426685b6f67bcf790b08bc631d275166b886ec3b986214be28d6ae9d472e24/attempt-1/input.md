FILE:desk/tasks/task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia.md
---
sldb:
  by: agent
  at: '2026-11-16T04:13:05Z'
  authority: generated
  via: create_document
id: task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references:
- desk/drawer/tasks/task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload.md
depends_on: []
pills: []
files:
- src/sldb/store/model_contract.py
- src/sldb/store/models/edge_node_record.py
- src/sldb/models/doc_anchor_value.py
- tests/store/test_payload_projection.py
- tests/api/test_doc_anchors.py
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms:
- atom-lo-que-la-clase-declara-se-relee-cada-vez-que-el-store-firma-el-modelo
from_drawer: desk/drawer/tasks/task-anclas-a-documentos-doc-anchors-fuera-de-la-firma-de-contrato-y-aristas-duplicadas-con-references.md
---

# contract_signature cubre __indexed__, __doc_anchors__ y __contract__, y un campo no puede ser a la vez referencia y ancla

## Rationale

_Explain why this task exists or the business driver behind it._

contract_signature (src/sldb/store/model_contract.py:89-102) firma solo los nombres de campos y __references__, __containment__ y __compositions__ (_DECLARED). Cambiar __indexed__ de un modelo no marca stale la proyección del payload (src/sldb/store/edge_index/payload_projection.py:35 usa indexed_fields), y agregar o cambiar __doc_anchors__ o __contract__ no hace que los documentos existentes ganen sus aristas de ancla (se escriben en los shards, src/sldb/store/edge_index/doc_contribution.py:63) hasta la próxima reconstrucción. Además un campo declarado en __references__ y en __doc_anchors__ produce dos aristas (declared_references.py y doc_anchor_edges.py:19) y definition_problems (src/sldb/models/doc_anchor_value.py:67) no lo rechaza. Hallazgos de GO04 (H1) y GO07 (H4, H11). Origen: drawer desk/drawer/tasks/task-anclas-a-documentos-doc-anchors-fuera-de-la-firma-de-contrato-y-aristas-duplicadas-con-references.md y desk/drawer/tasks/task-cambiar-indexed-de-un-modelo-no-marca-stale-la-proyeccion-del-payload.md.

## Goal

_Describe the concrete result this task must produce._

Cambiar __indexed__, __doc_anchors__ o __contract__ de un modelo cambia su contract_signature y deja stale los shards de sus documentos, que el rebuild reproyecta; un modelo que nombra el mismo campo en __references__ y en __doc_anchors__ es rechazado con SLDBModelError al registrarse.

## Scope

_State what is in scope and what is out of scope._

Entra: en contract_signature agregar al cuerpo firmado "indexed": sorted(__indexed__ o []), "doc_anchors": sorted(__doc_anchors__ o []) y "contract": sorted(__contract__ o []) (las tres claves siempre presentes, lista vacía si el modelo no las declara); actualizar la docstring y la descripción del campo contract_signature en src/sldb/store/models/edge_node_record.py:23; en definition_problems agregar el problema "field '<n>' is declared in both __references__ and __doc_anchors__". Tests en tests/store/test_payload_projection.py (cambiar __indexed__ marca stale y el rebuild proyecta el nuevo campo) y tests/api/test_doc_anchors.py (agregar __doc_anchors__ a un modelo con documentos ya indexados marca stale y el rebuild agrega la arista; doble declaración rechazada). Como la firma cambia para todos los modelos, todos los shards quedan stale una vez: correr sldb stores build sobre el store del repo y commitear el .sldb resultante en el mismo commit; anotarlo en CHANGELOG.md como cambio que fuerza un rebuild. No entra: cambiar cómo se proyecta el payload ni cómo se calculan las aristas de ancla.

## Implementation Path

_Outline the expected implementation route or affected surface._

1) Leer model_contract.py (contract_signature, _DECLARED, doc_anchor_fields línea 53), edge_node_record.py, doc_anchor_value.py (definition_problems) y los dos archivos de test. 2) Cambiar la firma. 3) Agregar el problema de doble declaración. 4) Tests. 5) TMPDIR=/dev/shm sldb stores build --store .sldb y stores build --check.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/store/test_payload_projection.py
- TMPDIR=/dev/shm pytest -q tests/api/test_doc_anchors.py
- TMPDIR=/dev/shm sldb stores build --check --store .sldb

## Done When

_Name the observable condition that makes the task complete._

Los tres comandos pasan con los tests nuevos; el .sldb del repo reconstruido va en el commit; CHANGELOG avisa que fuerza un rebuild; aviso a deskops y graph_ui con deskops message send (sus stores se reconstruyen una vez).

FILE:instruccion
Preflight solo-TaskDoc de la tarea task-contract-signature-cubre-indexed-doc-anchors-y-contract-y-un-campo-no-puede-ser-a-la-vez-referencia: reformula el encargo tal como lo leería un ejecutor sin ningún otro contexto, lista ambigüedades con cita textual del input y da el DRY-RUN sin ejecutar nada. No ejecutes nada.

