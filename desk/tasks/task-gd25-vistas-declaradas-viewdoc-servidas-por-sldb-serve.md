---
id: task-gd25-vistas-declaradas-viewdoc-servidas-por-sldb-serve
status: draft
summary: ''
tags:
- workspace:desk
- artifact:task
current_node: ritual-execution
history: []
references: []
depends_on:
- task-gd21-grafo-de-proyecto-aristas-declaradas-y-nodos-fuente-desde-el-índice-de-sldb-declarado-por-datos
- task-gd23-selectores-de-documento-id-prefijo-glob-modelo-where-como-api-de-sldb
pills: []
files:
- src/sldb/models/notation/view_doc.py
- src/sldb/models/notation/view_param.py
- src/sldb/models/notation/view_section.py
- src/sldb/models/notation/view_section_parts.py
- src/sldb/models/notation/view_doc_checks.py
- src/sldb/api/views/__init__.py
- src/sldb/api/views/run_view.py
- src/sldb/api/views/list_views.py
- src/sldb/api/views/view_rows.py
- src/sldb/api/views/view_groups.py
- src/sldb/api/views/view_edges.py
- src/sldb/api/views/view_rules.py
- src/sldb/api/views/view_transitions.py
- src/sldb/api/views/view_revision.py
- src/sldb/api/__init__.py
- src/sldb/cli/parsers/views.py
- src/sldb/cli/commands/views.py
- src/sldb/cli/parsers/public.py
- src/sldb/cli/dispatcher.py
- src/sldb/cli/serve/views_routes.py
- src/sldb/cli/serve/routes.py
- tests/api/test_views.py
- tests/api/test_view_doc.py
- tests/test_serve.py
- docs/architecture/views.md
- CHANGELOG.md
task_type: task.code
inherits_from: []
inherit_acceptance_context: false
atoms: []
from_drawer: desk/drawer/plans/generalizar-desde-deskops/dag.yaml
---

# GD25: Vistas declaradas (ViewDoc) servidas por sldb serve

## Rationale

_Explain why this task exists or the business driver behind it._

Nodo GD25 del plan desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3 (autorizado por el dueño 2026-11-05, execution_authorized=true), hijo de PG3. Depende de: ['GD21', 'GD23']. Gates requeridos: G_GO05: Lenguaje de predicados unificado (GO05) cerrado en main de sldb (satisfied); G_GO06: RuleDoc, rules check y rules explain (GO06) cerrados en main de sldb (satisfied); G_GO08: Evaluación on_write/on_transition/on_check y edges_blocked (GO08) cerrados en main de sldb (satisfied).

## Goal

_Describe the concrete result this task must produce._

ViewDoc (el de SV01) tipa params y sections y valida al escribir; sldb.api.run_view(store, name, params) ejecuta las secciones (select de GD23, fields, edges, group_by con group_order, rules de GO06, transitions de GO08/GO09) y devuelve {view, params, revision, sections}; revision por hashes de lo leído; CLI sldb views run|list con envelope; GET /views y GET /views/<name> con ETag e If-None-Match → 304, sin tapar /views/projection* de SV02; sin punto de extensión en Python; docs/architecture/views.md.

## Scope

_State what is in scope and what is out of scope._

En alcance: src/sldb/models/notation/view_doc.py y módulos nuevos de tipado en src/sldb/models/notation/, src/sldb/api/views/ (nuevo), src/sldb/api/__init__.py, src/sldb/cli/parsers/views.py y commands/views.py (nuevos) con su registro en public.py y dispatcher.py, src/sldb/cli/serve/views_routes.py (nuevo) y routes.py, tests, docs/architecture/views.md, CHANGELOG.md. Fuera: register_view_provider y campos computed (DA1); cambiar las rutas /views/projection* de SV02; nombres del caso deskops en src/sldb/.

## Implementation Path

_Outline the expected implementation route or affected surface._

CONTRATO DEL NODO (desk/drawer/plans/generalizar-desde-deskops/dag.yaml rev 3, GD25). SCOPE: Modelo ViewDoc (GP4): es el ViewDoc de SV01 (plan absorber-spec2viz-y-modelos-ui, sldb.models.notation_models, decisión SV-D3), no un modelo nuevo: GD25 tipa sus campos opcionales params y sections como sigue y agrega la validación; si SV01 no está en main al promover GD25, GD25 espera. Una ViewDoc sin sections es de proyección de grafo (SV02, rutas /views/projection*) y run_view la rechaza nombrándola; el nombre projection queda reservado (una ViewDoc llamada projection es rechazada al escribirla) para que GET /views/<name> no tape las rutas de SV02. Campos: name, params (lista de {name, required, default}), sections (lista ordenada de Section). Section = {key, select (selector de GD23; admite {param} con la sintaxis de sustitución de where_subject), fields (lista de campos de la facet a devolver; * = todos los proyectados), edges (lista opcional de {relation, direction out|in, as} que agrega a cada fila los export_id vecinos por edges_from/edges_to o ProjectGraph.edges_from/to de GD21), group_by (campo opcional; las filas salen agrupadas en el orden de una lista declarada group_order o, si falta, por valor), rules (lista opcional de nombres de RuleDoc: cada fila lleva findings = resultado de eval de GO06 para esas reglas), transitions (opcional {from_field, relation}: cada fila lleva holding = edges_holding con effects y findings (GO08/GO09) y blocked = edges_blocked, partiendo del nodo cuyo id es el valor de from_field)}. Sin punto de extensión en Python (DA1): un hecho que sldb no calcula (p. ej. de git) lo escribe el consumidor como documento del store (en deskops, recibo ReviewDoc kind evidence) y la vista lo lee con select, edges o rules como cualquier otro documento. Validación al escribir una ViewDoc: selectores y where parsean, rules nombran RuleDocs existentes, params referenciados existen. Ejecución: sldb.api.run_view(store, name, params) → {view, params, revision, sections: {key: rows | groups}}; revision = sha256 de los source_hash ordenados de todos los documentos leídos más los content_hash de la ViewDoc y de las RuleDocs usadas (y, si hay grafo de proyecto, su firma). CLI: sldb views run NAME [--param k=v ...] y sldb views list, con envelope. sldb serve: GET /views (lista) y GET /views/<name>?k=v con ETag = revision e If-None-Match → 304. Doc docs/architecture/views.md con un ejemplo neutral de tablero (estados como columnas, tarjetas por campo) sin nombres de deskops.

ACCEPTANCE: En un store temporal con un modelo Item (status, owner, depends_on), un ciclo de vida de prueba (RitualDoc/RelationDoc de prueba o modelos propios) y una RuleDoc: una ViewDoc tablero con group_by status y group_order declarado devuelve las columnas en ese orden; edges agrega depends_on entrantes y salientes; rules agrega findings con la cláusula; transitions devuelve holding con effects y blocked con su finding para un Item bloqueado; un parámetro {owner} filtra; un documento de prueba que hace de recibo de un hecho externo, enlazado a un Item, aparece en la fila del Item por edges sin código del consumidor; grep de register_view_provider y computed en src/sldb/api/views/ vacío; sldb views run y GET /views/<name> devuelven el mismo payload; GET con If-None-Match igual devuelve 304 y tras escribir un Item la revisión cambia; editar la RuleDoc también cambia la revisión; una ViewDoc con selector que no parsea es rechazada al escribirla; una ViewDoc llamada projection es rechazada; run_view sobre una ViewDoc de proyección (sin sections) da error que la nombra; las rutas /views/projection* de SV02 siguen respondiendo igual (sus tests verdes); tiempo de pared de la vista tablero sobre 200 Items en caliente < 1 s en robocop2 (registrado en la Validation del TaskDoc); CHANGELOG; docs/architecture/views.md; nota de cierre a deskops.

OUTPUT_SCOPE: src/sldb/models/notation_models.py (solo el tipado de params y sections de ViewDoc y su validación), src/sldb/api/views/, src/sldb/api/__init__.py, src/sldb/cli/parsers/views.py, src/sldb/cli/commands/views.py, src/sldb/cli/serve/views_routes.py, src/sldb/cli/serve/routes.py, tests/, docs/architecture/views.md, CHANGELOG.md

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
q1 (gates): G_GO05, G_GO06 y G_GO08 están satisfied; GO09 y GO10 también cerrados en main. GD21 (ProjectGraph.edges_from/to) y GD23 (select_documents) están en main.
q2 (ubicación de ViewDoc): el modelo vive en src/sldb/models/notation/view_doc.py; src/sldb/models/notation_models.py solo lo reexporta y no se edita. El OUTPUT_SCOPE del dag dice notation_models.py: se lee como el modelo ViewDoc donde esté.
q3 (params): hoy ViewDoc.params es dict con default {} (SV01 lo dejó reservado para GD25) y nada en src/ lo usa. GD25 lo tipa como lista de {name, required, default} según el contrato; un valor None o ausente sigue siendo vacío (los ViewDoc de proyección existentes no traen params). Si algún ViewDoc existente del repo o de los tests trae params como mapa, se reporta antes de cambiar el tipo.
q4 (grupo CLI views): no existe; se registra en src/sldb/cli/parsers/public.py y src/sldb/cli/dispatcher.py (como tags en GD27), y tests/test_cli_every_command_has_a_handler.py debe quedar verde sin editarse.
q5 (rules nombran RuleDocs existentes): es una invariante que cruza documentos; el principio del dueño la manda a regla, pero no hay predicado para ella. En GD25 se comprueba al ejecutar la vista (run_view da error que nombra la RuleDoc ausente) y no al escribir la ViewDoc; las validaciones de un solo documento (selectores y where que parsean, params referenciados que existen, nombre projection reservado) son validadores pydantic de ViewDoc. Hipótesis para el dueño.
q6 (files): la lista es la mejor previsión al promover; un archivo autorizado que no se use se reporta en la entrega y el coordinador lo poda del TaskDoc; uno nuevo se pide antes.

## Validation

_List the checks required before this task can close._

- TMPDIR=/dev/shm pytest -q tests/api/test_views.py
- TMPDIR=/dev/shm pytest -q tests/api/test_view_doc.py
- TMPDIR=/dev/shm pytest -q tests/test_serve.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_notation_view_and_routes.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_notation_models_and_builtins.py
- TMPDIR=/dev/shm pytest -q tests/notations/test_payload_projection.py
- TMPDIR=/dev/shm pytest -q tests/test_store_seams.py
- TMPDIR=/dev/shm pytest -q tests/test_cli_every_command_has_a_handler.py
- grep -rn 'register_view_provider\|computed' src/sldb/api/views/ vacío
- grep de genericidad: ninguna línea agregada por el diff (git diff origin/main...HEAD) en src/ o tests/ contiene taskdoc|board|ritual|pill|atom|closeout (regla 4)
- sldb views run NAME --format json sobre el store temporal del test (salida en el reporte de entrega) y tiempo de pared de la vista tablero sobre 200 Items en caliente (< 1 s), registrado aquí
- nota de cierre a deskops por deskops message send --to deskops --kind suggestion (regla 7)
- TMPDIR=/dev/shm pytest -q tests/test_clean_code_rules.py antes de cada squash (recorre todo src/: funciones de 10 líneas de lógica como máximo, máximo 1 clase y 80 líneas efectivas por archivo)
- git fetch y rebase sobre origin/main antes de entregar; en CHANGELOG.md y src/sldb/api/__init__.py tomar la versión de main y agregar solo lo propio
- files: del TaskDoc coincide con el diff entregado (los autorizados que no se usen se reportan y el coordinador los poda antes de entregar)

## Done When

_Name the observable condition that makes the task complete._

En un store temporal con un modelo Item (status, owner, depends_on), un ciclo de vida de prueba (RitualDoc/RelationDoc de prueba o modelos propios) y una RuleDoc: una ViewDoc tablero con group_by status y group_order declarado devuelve las columnas en ese orden; edges agrega depends_on entrantes y salientes; rules agrega findings con la cláusula; transitions devuelve holding con effects y blocked con su finding para un Item bloqueado; un parámetro {owner} filtra; un documento de prueba que hace de recibo de un hecho externo, enlazado a un Item, aparece en la fila del Item por edges sin código del consumidor; grep de register_view_provider y computed en src/sldb/api/views/ vacío; sldb views run y GET /views/<name> devuelven el mismo payload; GET con If-None-Match igual devuelve 304 y tras escribir un Item la revisión cambia; editar la RuleDoc también cambia la revisión; una ViewDoc con selector que no parsea es rechazada al escribirla; una ViewDoc llamada projection es rechazada; run_view sobre una ViewDoc de proyección (sin sections) da error que la nombra; las rutas /views/projection* de SV02 siguen respondiendo igual (sus tests verdes); tiempo de pared de la vista tablero sobre 200 Items en caliente < 1 s en robocop2 (registrado en la Validation del TaskDoc); CHANGELOG; docs/architecture/views.md; nota de cierre a deskops.
