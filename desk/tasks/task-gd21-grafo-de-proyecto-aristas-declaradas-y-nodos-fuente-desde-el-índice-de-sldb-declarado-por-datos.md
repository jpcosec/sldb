---
id: task-gd21-grafo-de-proyecto-aristas-declaradas-y-nodos-fuente-desde-el-índice-de-sldb-declarado-por-datos
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
- src/sldb/api/edges/project_graph/project_graph_config.py
- src/sldb/api/edges/project_graph/project_graph_config_mapping.py
- src/sldb/api/edges/project_graph/project_graph.py
- src/sldb/api/edges/project_graph/project_texts.py
- src/sldb/api/edges/project_graph/inverse_edges.py
- src/sldb/api/edges/project_graph/project_graph_memo.py
- src/sldb/api/edges/project_graph/store_project_graph.py
- src/sldb/api/edges/project_graph/__init__.py
- src/sldb/api/stores/store_declaration.py
- src/sldb/api/stores/tracked_documents.py
- src/sldb/api/__init__.py
- src/sldb/cli/parsers/graph.py
- src/sldb/cli/parsers/graph_project.py
- src/sldb/cli/commands/graph.py
- src/sldb/cli/commands/graph_project.py
- src/sldb/cli/serve/routes.py
- src/sldb/cli/serve/project_graph_routes.py
- src/sldb/cli/serve/edges_routes.py
- tests/api/test_project_graph.py
- tests/api/test_project_graph_config.py
- tests/test_serve.py
- docs/architecture/project-graph.md
- CHANGELOG.md
- src/sldb/api/edges/project_graph/document_surface.py
- src/sldb/api/edges/project_graph/reference_field.py
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD21: Grafo de proyecto (aristas declaradas y nodos fuente) desde el índice de sldb, declarado por datos y servido

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD21 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG1. Depende de: nada. Gates requeridos: ninguno.

## Goal

_Describe the concrete result this task must produce._

La configuración del grafo de proyecto es dato puro: ProjectGraphConfig y sus dataclasses se cargan y vuelcan a YAML con ida y vuelta exacta, y se declaran en store.yaml bajo project_graph con validación propia; el hook closed_document pasa a ser un predicado closed: del lenguaje de sldb; ProjectGraph gana edges_to desde un mapa inverso memoizado por firma de shards y mtime de superficies; sldb.api.project_graph(store), CLI sldb graph project nodes|edges|missing con envelope, GET /project-graph/nodes|edges|missing y /edges?include_linked=false; docs/architecture/project-graph.md. Produce G_PROJECT_GRAPH.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/api/edges/project_graph/ (config, project_graph, mapa inverso y memo), src/sldb/api/stores/store_declaration.py, src/sldb/api/stores/tracked_documents.py, src/sldb/api/__init__.py, src/sldb/cli/parsers/graph*.py, src/sldb/cli/commands/graph*.py, src/sldb/cli/serve/routes.py, project_graph_routes.py (nuevo) y edges_routes.py, tests, docs/architecture/project-graph.md, CHANGELOG.md. Fuera: los extractores y el oráculo de deskops (CC33), nombres del caso deskops en src/sldb/api/edges/project_graph/, GD22 (aristas entrantes de escritura).

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD21). SCOPE: Parte de la rama wt/closeout-graph-sldb integrada en main (sldb 432e45d6: src/sldb/api/edges/project_graph/, api/stores/tracked_documents.py); si al promover no está integrada, el primer paso es integrarla tal cual (con su oráculo de equivalencia en deskops) y este nodo arranca después. Tres cambios sobre ella: (1) configuración como dato puro: ProjectGraphConfig y sus dataclasses (DocumentSurface, FileRule, FileExclusions, DeclaredFileTargets, ReferenceField, MentionPattern, SectionMentions, LineMentions, MissingTargetKind) se cargan y se vuelcan a YAML (from_mapping/to_mapping, ida y vuelta exacta) y se declaran en store.yaml bajo la clave project_graph (StoreDeclaration, api/stores/store_declaration.py:20, con validación propia: clave desconocida = error al cargar el store que la nombra); el hook closed_document deja de ser callable y pasa a ser un campo closed: predicado del lenguaje de sldb evaluado con where_matches sobre el payload del documento (api/where.py:10; con GO04 cerrado se evalúa sobre la facet sin re-extraer, sin cambiar esta API); una superficie sin closed nunca está cerrada. (2) aristas entrantes: ProjectGraph.edges_to(node_id) con el mismo registro de arista que edges_from (tipo, rol, origen schema|mention, ubicación ruta:línea para menciones), calculadas desde un mapa inverso construido una vez por firma de shards (store/edge_index/shard_signature.py) más el mtime de las superficies no modeladas; no hay mapas inversos parciales por tipo (CloseoutGraph de deskops arma uno solo para materializations). (3) superficie pública: sldb.api.project_graph(store) → ProjectGraph con la configuración del store; CLI sldb graph project nodes [--kind K] | edges --from ID | --to ID | missing, con envelope JSON; sldb serve: GET /project-graph/nodes?kind=, /project-graph/edges?from=|to=, /project-graph/missing (propuesta de deskops runs/subagents/20261105-closeout-graph-sldb/sldb-serve-note.md); además /edges acepta include_linked=false (edges_routes.py:39 hoy fija True). Memoización: el grafo de proyecto se recalcula solo si cambia la firma de shards o el mtime de alguna superficie o archivo incluido; una segunda llamada sin cambios no recorre el disco. Doc docs/architecture/project-graph.md con el esquema de la configuración y un ejemplo neutral (modelos de prueba, sin nombres de deskops).

ACCEPTANCE: Un store temporal con modelos de prueba, una superficie no modelada, archivos fuente y una mención por regex declara project_graph en store.yaml y sldb graph project nodes/edges/missing devuelven los nodos y aristas esperados (fixture con resultado esperado); la configuración vuelca y carga ida y vuelta igual; una configuración con un callable o con una clave desconocida falla al cargar con un mensaje que nombra la clave; closed: status = "closed" marca cerrado un documento con ese campo y no otro; edges --to devuelve la mención con ruta:línea; una segunda consulta sin cambios hace cero llamadas a os.walk/rglob (contadas en el test) y tocar un archivo incluido hace que la siguiente recalcule; las tres rutas de /project-graph responden lo mismo que la CLI y /edges?include_linked=false excluye stores enlazados; el oráculo de equivalencia de la rama (extractores v1 de deskops) sigue verde contra la configuración que deskops declare (lo corre deskops en CC33; aquí basta con el fixture); grep de nombres del caso deskops en src/sldb/api/edges/project_graph/ vacío (regla 4); CHANGELOG; docs/architecture/project-graph.md. Produce G_PROJECT_GRAPH; nota de cierre a deskops (regla 7).

OUTPUT_SCOPE: src/sldb/api/edges/project_graph/, src/sldb/api/stores/store_declaration.py, src/sldb/api/stores/tracked_documents.py, src/sldb/api/__init__.py, src/sldb/cli/parsers/graph*.py, src/sldb/cli/commands/graph*.py, src/sldb/cli/serve/routes.py, src/sldb/cli/serve/project_graph_routes.py, src/sldb/cli/serve/edges_routes.py, tests/, docs/architecture/project-graph.md, CHANGELOG.md

REGLAS COMUNES (alcance.md):
1. Cada nodo se promueve con `deskops add task --from-drawer` en el desk de sldb, con `--task-type` y `files` completos; antes, preflight TaskDoc-only y cold-bundle (ritual-context-review). Las revisiones en frío las decide el supervisor; quien opera el desk dispone los hallazgos como correcciones del TaskDoc (`deskops edit task`) y resume en `coordinator-status.md`; nada a mano en `desk/` fuera de `drawer/plans` ni en `.sldb/`.
2. Se ejecuta en robocop2, en un worktree de sldb aparte del de grafo-operable (otras áreas: edges, documents, serve, stores). Validación: los tests de los archivos tocados (`pytest -q <archivos>`, uno a la vez); la suite completa la corre el supervisor sobre el resultado integrado. Un nodo no cierra con tests rojos ni saltados.
3. Toda capacidad nueva entra con: función pública en `sldb.api` (reexportada en `sldb/api/__init__.py`), comando CLI con envelope JSON, ruta de `sldb serve` cuando el consumidor la necesita, pruebas, entrada en `CHANGELOG.md` y doc en `docs/architecture/`. Nada queda solo en el código.
4. Genericidad: ningún nombre del caso deskops (TaskDoc, Board, ritual, pill, atom, closeout) aparece en `src/sldb/` ni en sus tests, salvo como dato en fixtures. Un grep lo comprueba en la aceptación de cada nodo.
5. Compatibilidad: ninguna salida existente de la CLI ni de `sldb serve` cambia (goldens existentes verdes); lo nuevo es aditivo. Si un nodo necesita cambiar un contrato existente (p. ej. `/save` pasa a ser atómico), lo nombra en su aceptación y en el CHANGELOG.
6. Ante un contrato ausente de un nodo GO no cerrado, el nodo registra la hipótesis en su TaskDoc, implementa la parte que no depende de él y no inventa la API de grafo-operable.
7. Cada nodo, al cerrar, manda nota a deskops (`deskops message send --to deskops --kind suggestion`) con la función, el comando y la ruta nuevos y el código de deskops que quedan sin motivo (tabla de arriba); así se satisface el gate `G_GDxx` del plan de deskops.
8. Promoción de nodos con hijos (`node_role: aggregate`): nunca se promueve el agregado; se promueven los hijos.

PRECISIONES DE PROMOCIÓN (2026-11-06):
q1 (base): la rama wt/closeout-graph-sldb ya está integrada en main (src/sldb/api/edges/project_graph/ con 38 módulos, api/stores/tracked_documents.py y tests/api/test_project_graph.py existen en fe36893f); el nodo arranca sobre ella sin paso previo de integración.
q2 (/edges): edges_routes.py hoy no pasa include_linked (edges_from/edges_to de api/edges/edge_reading.py:45,61 lo tienen con default True); /edges acepta el query param include_linked=false|true (default true, la salida actual no cambia) y lo pasa a edges_from/edges_to.
q3 (G_GO04): GO04 y GO05 están cerrados; closed: se evalúa con el lenguaje de sldb (sldb.api.where) sobre el payload de la proyección del índice, sin re-extraer el documento.
q4 (files): la lista es la mejor previsión al promover; un archivo autorizado que no se use se reporta en la entrega y el coordinador lo poda del TaskDoc; uno nuevo se pide antes.
PRECISIONES DEL PREFLIGHT (review-task-gd21-preflight-1, 2026-11-06):
q5 (closed_document, transición): hoy lo usa un consumidor real (deskops/graph/desk_graph.py:191 pasa closed_document= como callable). Para no romperlo antes de que deskops migre en CC33: el campo nuevo es closed (predicado del lenguaje); closed_document se conserva SOLO como argumento Python de ProjectGraphConfig, marcado deprecated (DeprecationWarning al construir), nunca se serializa ni se carga: from_mapping y store.yaml rechazan la clave closed_document como clave desconocida, y to_mapping de una configuración con closed_document levanta error que nombra closed_document. Si una configuración trae los dos, gana closed. Se borra cuando CC33 cierre (nota a deskops, regla 7). tests/api/test_project_graph.py:64 pasa a usar closed: y un test aparte cubre la transición (warning y rechazo en from_mapping/to_mapping).
q6 (memo): la firma de memoización es la firma de shards (store/edge_index/shard_signature.py) más (ruta, mtime_ns, size) de cada archivo que la última construcción leyó (superficies no modeladas y archivos que las FileRule incluyen después de FileExclusions) más el mtime_ns de cada directorio recorrido (así un archivo nuevo en una carpeta recorrida invalida). Los archivos excluidos no se observan. Comprobar la firma no recorre el disco con os.walk/rglob: usa stat sobre la lista guardada (el test cuenta os.walk/rglob, no stat).
q7 (HTTP igual a la CLI): cada GET /project-graph/* responde 200 con el mismo JSON que el comando equivalente con --format json (igualdad de datos, sin envelope), como GET /docs/select de GD23; parámetros faltantes o inválidos son 400 con {"ok": false, "error": ...}.
q8 (error de callable): from_mapping solo acepta escalares, listas y mapas YAML; un valor que no es eso, o una clave que no es campo de la dataclass, levanta error de carga cuyo mensaje nombra la ruta de la clave (p. ej. project_graph.surfaces[0].closed_document). to_mapping de un campo con un callable levanta error que nombra el campo.
q9 (validación): tests/test_store_seams.py se corre sin editarse (no va en files). La regla del grep es: ninguna línea agregada por el diff (git diff origin/main...HEAD, líneas +) contiene taskdoc|board|ritual|pill|atom|closeout, y src/sldb/api/edges/project_graph/ queda sin coincidencias; los módulos nuevos están permitidos.
PRECISIONES DEL COLD-BUNDLE (review-task-gd21-bundle-1, 2026-11-06):
q10 (G_PROJECT_GRAPH): es un gate del dag del plan; lo marca el coordinador de proyecto al cerrar. El ejecutor solo entrega la evidencia: sldb graph project nodes|edges|missing y GET /project-graph/* respondiendo desde project_graph en store.yaml, sin ningún callable en la configuración cargada.
q11 (pills y atoms): el TaskDoc no liga ninguno y no hacen falta; el contrato completo está en este TaskDoc.
q12 (vida del memo): caché por proceso, a nivel de módulo, con clave la ruta resuelta del store (como las demás cachés de sldb); "segunda consulta" es una segunda llamada a sldb.api.project_graph(store) en el mismo proceso, y también una segunda lectura del mismo objeto. Se invalida por la firma de q6 y la limpia la invalidación de cachés existente que usa GD24 (forget_caches), sin API nueva. No persiste en disco.
q13 (cargar): "cargar" es from_mapping, que es lo que usa también la carga de store.yaml; los dos caminos fallan igual (q8). Un callable solo puede llegar por un dict de Python pasado a from_mapping.
q14 (edges): --from y --to son mutuamente excluyentes y uno es obligatorio (grupo excluyente requerido de argparse: sin ninguno o con los dos, error de uso, exit 2). En HTTP, GET /project-graph/edges con ninguno o con los dos es 400.
q15 (closed_document): manda q5; el Goal describe el estado final (closed: como única forma declarable) y el argumento Python deprecated es transitorio hasta CC33.
PRECISIONES DE EJECUCIÓN (coordinador, 2026-11-06):
q16 (closed en la superficie): closed: str | None (predicado del lenguaje de sldb, default None = nunca cerrada) es un campo opcional de DocumentSurface; se agrega src/sldb/api/edges/project_graph/document_surface.py a files. No hay mapa kind->predicado en ProjectGraphConfig.
q17 (grep de project_graph vacío): la aceptación exige el grep de src/sldb/api/edges/project_graph/ vacío; las dos coincidencias preexistentes de reference_field.py:13-14 (ejemplos en descripciones de Field: materialization, source_atoms, atom:) se neutralizan con ejemplos genéricos (p. ej. contract, sources, topic:). Solo cambian esas descripciones; se agrega reference_field.py a files.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_project_graph.py
- TMPDIR=/dev/shm pytest -q tests/api/test_project_graph_config.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- grep -rniE 'taskdoc|board|ritual|pill|atom|closeout' src/sldb/api/edges/project_graph/ vacío (regla 4) y sin líneas nuevas en src/sldb/ contra origin/main al despachar
- sldb graph project nodes|edges --to ID|missing --format json sobre el store temporal del test (salida en el reporte de entrega)
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

Un store temporal con modelos de prueba, una superficie no modelada, archivos fuente y una mención por regex declara project_graph en store.yaml y sldb graph project nodes/edges/missing devuelven los nodos y aristas esperados (fixture con resultado esperado); la configuración vuelca y carga ida y vuelta igual; una configuración con un callable o con una clave desconocida falla al cargar con un mensaje que nombra la clave; closed: status = "closed" marca cerrado un documento con ese campo y no otro; edges --to devuelve la mención con ruta:línea; una segunda consulta sin cambios hace cero llamadas a os.walk/rglob (contadas en el test) y tocar un archivo incluido hace que la siguiente recalcule; las tres rutas de /project-graph responden lo mismo que la CLI y /edges?include_linked=false excluye stores enlazados; el oráculo de equivalencia de la rama (extractores v1 de deskops) sigue verde contra la configuración que deskops declare (lo corre deskops en CC33; aquí basta con el fixture); grep de nombres del caso deskops en src/sldb/api/edges/project_graph/ vacío (regla 4); CHANGELOG; docs/architecture/project-graph.md. Produce G_PROJECT_GRAPH; nota de cierre a deskops (regla 7).
